from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from . import models
from.models import UserImage, Categories, PendingProject, ApprovedProject, Notifications, PendingResume
from.models import ApprovedResume, Proposals, Messages, Ongoingproject, Completedproject, Reviews, Blog
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def home(request):
    if 'username' in request.session:
        return redirect(index)
    else:
        return render(request, 'home.html')

def signup(request):
    return render(request, 'login-signup.html')

def registration(request):
    if request.method == 'POST':
        fname = request.POST['fn']
        lname = request.POST['ln']
        username = request.POST['un']
        email = request.POST['email']
        password = request.POST['pass']
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect(signup)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect(signup)
        else:

            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.last_name = lname
            ui = UserImage(user=myuser, uname=username)
            ui.save()
            myuser.save()
            messages.success(request, 'successfully registered...')
            return redirect(signup)


def signin(request):
    if request.method == 'POST':
        uname = request.POST['user']
        pass1 = request.POST['password']
        user = authenticate(username=uname, password=pass1)
        if user is not None:
            if user.is_staff == True:
                login(request, user)
                return redirect(adminindex)
            else:
                request.session['username'] = user.username
                login(request, user)
                return redirect(index)
        else:
            messages.success(request, 'Username or Password is Incorrect')
            return redirect(signup)
    else:
        return redirect(signup)


def passwordreset(request):
    return render(request, 'password-reset.html')

def newpass(request):
    if request.method == 'POST':
        email = request.POST['email']
        if not User.objects.filter(email=email):
            messages.error(request, 'No user found with this email!')
            return redirect(passwordreset)
        else:
            usr = User.objects.get(email=email)
            uname = usr.username
            current_site = get_current_site(request)
            subject = 'Password Reset Email..'
            message = render_to_string('email/forgot-password.html', {
                'user': uname,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(usr.pk)),
                'token': generate_token.make_token(usr),
            })
            usr.email_user(subject, message)
            messages.success(request, 'Password reset link is send to your email..')
            return redirect(passwordreset)


def resetsection(request,   uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usr = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        usr = None

    if usr is not None and generate_token.check_token(usr, token):
        return render(request, 'email/set-new-password.html', {'us': usr})
    else:
        return HttpResponse('Activation link is invalid!')


def resetsuccess(request, pk):
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        usr = User.objects.get(pk=pk)
        usr.set_password(pass1)
        usr.save()
        messages.success(request, 'your password is changed..')
        return redirect(signup)

@login_required()
def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        us = user.username
        noti = Notifications.objects.filter(user=us)
        data = Categories.objects.all()
        prj = ApprovedProject.objects.all()[:5]
        blo = Blog.objects.all()[:3]
        return render(request, 'index.html', {'category': data, 'notification': noti, 'project': prj, 'blog': blo})

@login_required()
def deletenotifi(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        us = user.username
        noti = Notifications.objects.filter(user=us)
        noti.delete()
        return redirect(index)


@login_required()
def updateprofile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            newpic = request.FILES.get('newpic')
            newusername = request.POST['newusername']
            newemail = request.POST['newemail']
            newfirst = request.POST['newfirst']
            newlast = request.POST['newlast']
            User.objects.filter(id=request.user.id).update(username=newusername, email=newemail, first_name=newfirst, last_name=newlast)
            usr = UserImage.objects.get(user__id=request.user.id)
            if 'newpic' not in request.FILES:
                usr.image = usr.image
            else:
                usr.image = newpic
            usr.uname = newusername
            usr.save()
            messages.success(request, 'Your Profile is Successfully Updated')
            return redirect(settings)
        else:
            return redirect(settings)
    else:
        return redirect(settings)

@login_required()
def changepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            oldpass = request.POST['oldpass']
            newpassword = request.POST['newpassword']
            user = User.objects.get(id=request.user.id)
            un = user.username
            check = user.check_password(oldpass)
            if check == True:
                user.set_password(newpassword)
                user.save()
                messages.success(request, 'Your Password is Changed')
                user = User.objects.get(username=un)
                login(request, user)
                return redirect(settings)
            else:
                messages.error(request, 'Incorrect current password')
                return redirect(settings)
        else:
            return redirect(settings)
    else:
        return redirect(settings)

@login_required()
def deleteaccount(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            delpass = request.POST['pass']
            user = User.objects.get(id=request.user.id)
            check = user.check_password(delpass)
            if check == True:
                user.delete()
                return redirect(signup)
            else:
                messages.error(request, 'Incorrect password')
                return redirect(settings)
        else:
            return redirect(settings)
    else:
        return redirect(settings)


@login_required()
def dashboard(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        us = user.username
        pcount = ApprovedProject.objects.filter(user=us).count()
        noti = Notifications.objects.filter(user=us)
        ong = Ongoingproject.objects.filter(user=us).count()
        myong = Ongoingproject.objects.filter(hireduser=us).count()
        mycomp = Completedproject.objects.filter(hireduser=us).count()
        bidswon = int(myong)+int(mycomp)
        cprj = Completedproject.objects.filter(user=us).count()
        plisted = int(pcount)+int(ong)+int(cprj)
        rev = Reviews.objects.filter(hireduser=us).count()
        return render(request, 'dashboard.html', {'notification': noti, 'plisted': plisted, 'bidswon': bidswon,
                                                  'completed': cprj, 'reviews': rev})

@login_required()
def deletenotification(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        us = user.username
        noti = Notifications.objects.filter(user=us)
        noti.delete()
        return redirect(dashboard)


@login_required()
def postproject(request):
    data = Categories.objects.all()
    return render(request, 'post-project.html', {'category': data})

@login_required()
def addresume(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        us = user.username
        data = Categories.objects.all()
        return render(request, 'add-resume.html', {'category': data})

@login_required()
def settings(request):
    return render(request, 'settings.html')

@login_required()
def message(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        us = user.username
        msend = Messages.objects.filter(sender=us)
        mrecieve = Messages.objects.filter(receiver=us)
        return render(request, 'message.html', {'message': msend, 'rmessage': mrecieve})

@login_required()
def reviews(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        rev = Reviews.objects.filter(hireduser=user)
        return render(request, 'reviews.html', {'review': rev})

@login_required()
def manageprojects(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        uname = user.username
        pprj = PendingProject.objects.filter(user=uname)
        aprj = ApprovedProject.objects.filter(user=uname)
        ogprj = Ongoingproject.objects.filter(user=uname)
        cprj = Completedproject.objects.filter(user=uname)
        return render(request, 'manage-projects.html', {'project': pprj, 'approved': aprj, 'ongoing':ogprj,
                                                        'completed': cprj})

@login_required()
def myprojects(request):
    if request.user.is_authenticated:
        usr = User.objects.get(id=request.user.id)
        us = usr.username
        ongp = Ongoingproject.objects.filter(hireduser=us)
        cprj = Completedproject.objects.filter(hireduser=us)
        return render(request, 'my-projects.html', {'ongoing': ongp, 'completed': cprj})

@login_required()
def proposals(request):
    if request.user.is_authenticated:
        usr = User.objects.get(id=request.user.id)
        prop = Proposals.objects.filter(projuser=usr)
        return render(request, 'proposals.html', {'proposals': prop})


@login_required()
def viewprofile(request, projsender):
    if request.user.is_authenticated:
        prof = ApprovedResume.objects.get(projsender=projsender)
        return render(request, 'view-profile.html', {'freelancer': prof})
    else:
        return redirect(signup)


@login_required()
def sendmessageprop(request, pk):
    ar = Proposals.objects.get(pk=pk)
    us = ar.projsender
    usr = User.objects.get(username=us)
    return render(request, 'msgsend.html', {'prop': ar, 'name': usr})

@login_required()
def messagesended(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fname = request.POST['fullname']
            msg = request.POST['message']
            ar = Proposals.objects.get(pk=pk)
            us = ar.projsender
            utitle = ar.ptitle
            ucurrency = ar.currency
            uprice = ar.price
            ap = User.objects.get(username=us)
            hfname = ap.first_name
            hlname = ap.last_name
            sen = UserImage.objects.get(uname=us)
            receiverimg = sen.image
            usre = User.objects.get(id=request.user.id)
            usr = UserImage.objects.get(user=usre)
            img = usr.image
            mesg = Messages(sender=usre, img=img, receiver=us, message=msg)
            mesg.save()
            apdele = ApprovedProject.objects.get(title=utitle)
            optitle = utitle
            opposted = apdele.date_added
            opcategory = apdele.category
            opcurrency = ucurrency
            rate = uprice
            ophireduser = us
            opfullname = hfname
            opimage = receiverimg
            ongp = Ongoingproject(user=usre, title=optitle, posted=opposted, category=opcategory, currency=opcurrency,
                                  rate=rate, hireduser=ophireduser, hfname=hfname, hlname=hlname, himage=opimage)
            ongp.save()
            notifi = 'is hired you for this project'
            noti = Notifications(user=us, opuser=usre, ptitle=optitle, notification=notifi)
            noti.save()
            delprop = Proposals.objects.filter(ptitle=utitle)
            delprop.delete()
            apdele.delete()
            return redirect(message)
        else:
            return redirect(proposals)
    else:
        return redirect(signup)

@login_required()
def projectcompleted(request, pk):
    if request.user.is_authenticated:
        ong = Ongoingproject.objects.get(pk=pk)
        cuser = ong.user
        ctitle = ong.title
        ccategory = ong.category
        chiredon = ong.hiredon
        ccurrency = ong.currency
        crate = ong.rate
        chireduser = ong.hireduser
        chfname = ong.hfname
        chlname = ong.hlname
        chimage = ong.himage
        cprj = Completedproject(user=cuser, title=ctitle, category=ccategory, currency=ccurrency, rate=crate,
                                hiredon=chiredon, hireduser=chireduser, hfname=chfname, hlname=chlname,
                                himage=chimage)
        cprj.save()
        notifi = 'You Completed the project successfully'
        noti = Notifications(user=chireduser, ptitle=ctitle, notification=notifi)
        noti.save()
        ong.delete()
        return redirect(manageprojects)
    else:
        return redirect(signup)



@login_required()
def writereview(request, pk):
    cprj = Completedproject.objects.get(pk=pk)
    return render(request, 'write-review.html', {'completed':cprj})

@login_required()
def savereview(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            rating = request.POST['rate']
            review = request.POST['review']
            usr = User.objects.get(id=request.user.id)
            uimg = UserImage.objects.get(user__id=request.user.id)
            usrimg = uimg.image
            fname = usr.first_name
            lname = usr.last_name
            cp = Completedproject.objects.get(pk=pk)
            huser = cp.hireduser
            htitle = cp.title
            sr = Reviews(rfname=fname, rlname=lname, ruser=usr, rimg=usrimg, hireduser=huser, title=htitle,
                         rating=rating, review=review)
            notifi = 'is add a review for your work'
            noti = Notifications(user=huser, opuser=fname, ptitle=htitle, notification=notifi)
            noti.save()
            sr.save()
            return redirect(manageprojects)
        else:
            return redirect(manageprojects)
    else:
        return redirect(signup)








@login_required()
def previewprofile(request):
    if request.user.is_authenticated:
        usr = User.objects.get(id=request.user.id)
        ares = ApprovedResume.objects.get(user=usr)
        return render(request, 'preview-profile.html', {'r': ares})
    else:
        return redirect(signup)

@login_required()
def editresume(request):
    if request.user.is_authenticated:
        usr = User.objects.get(id=request.user.id)
        ares = ApprovedResume.objects.get(user__id=request.user.id)
        data = Categories.objects.all()
        return render(request, 'edit-resume.html', {'category': data, 'r': ares})


@login_required()
def saveeditresume(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            rname = request.POST['flname']
            rdesignation = request.POST['dsg']
            rcurrency = request.POST['acurrency']
            rrate = request.POST['rate']
            rgender = request.POST['sex']
            rcategory = request.POST['acategory']
            alocation = request.POST['loc']
            aoverview = request.POST['over']
            img = request.FILES.get('npic')
            askill1 = request.POST['skill1']
            askill2 = request.POST['skill2']
            askill3 = request.POST['skill3']
            askill4 = request.POST['skill4']
            askill5 = request.POST['skill5']
            alang1 = request.POST['lang1']
            alang2 = request.POST['lang2']
            alang3 = request.POST['lang3']
            alang4 = request.POST['lang4']
            aextitle = request.POST['extitle']
            aexcompany = request.POST['excom']
            aexstart = request.POST['exstart']
            aexend = request.POST['exend']
            aexsummary = request.POST['exsum']
            aedtitle = request.POST['edtitle']
            aeduniversity = request.POST['eduni']
            aedend = request.POST['edend']
            aedsummary = request.POST['edsum']
            amylink = request.POST['youlink']
            alink1 = request.POST['link1']
            alink2 = request.POST['link2']
            alink3 = request.POST['link3']
            alink4 = request.POST['link4']
            user = User.objects.get(id=request.user.id)
            er = ApprovedResume.objects.get(user__id=request.user.id)
            er.fullname = rname
            if 'npic' not in request.FILES:
                er.userimg = er.userimg
            else:
                er.userimg = img
            er.designation = rdesignation
            er.currency = rcurrency
            er.rate = rrate
            er.gender = rgender
            er.category = rcategory
            er.location = alocation
            er.overview = aoverview
            er.skill1 = askill1
            er.skill2 = askill2
            er.skill3 = askill3
            er.skill4 = askill4
            er.skill5 = askill5
            er.lang1 = alang1
            er.lang2 = alang2
            er.lang3 = alang3
            er.lang4 = alang4
            er.extitle = aextitle
            er.excompany = aexcompany
            er.exstart = aexstart
            er.exend = aexend
            er.exsummary = aexsummary
            er.edtitle = aedtitle
            er.eduniversity = aeduniversity
            er.edend = aedend
            er.edsummary = aedsummary
            er.mylink = amylink
            er.slink1 = alink1
            er.slink2 = alink2
            er.slink3 = alink3
            er.slink4 = alink4
            er.save()
            messages.success(request, 'Your Resume is updated')
            return redirect(editresume)
        else:
            return redirect(editresume)
    else:
        return redirect(signup)




@login_required()
def projects(request):
    data = Categories.objects.all()
    prj = ApprovedProject.objects.all()
    return render(request, 'projects.html', {'category': data, 'projects': prj})


@login_required()
def searchprojects(request):
    if request.method == 'POST':
        cat = request.POST['category']
        prj = ApprovedProject.objects.filter(category=cat)
        data = Categories.objects.all()
        return render(request, 'projects.html', {'category': data, 'projects': prj})



@login_required()
def freelancers(request):
    data = Categories.objects.all()
    fre = ApprovedResume.objects.all()
    return render(request, 'freelancers.html', {'category': data, 'freelancer': fre})


@login_required()
def searchfreelancers(request):
    if request.method == 'POST':
        cat = request.POST['category']
        fre = ApprovedResume.objects.filter(category=cat)
        data = Categories.objects.all()
        return render(request, 'freelancers.html', {'category': data, 'freelancer': fre})


@login_required()
def projectdetails(request, slug):
    proj = ApprovedProject.objects.get(slug=slug)
    tit = proj.title
    prop = Proposals.objects.filter(ptitle=tit)
    return render(request, 'project-details.html', {'project': proj, 'prop':prop})



@login_required()
def sendproposal(request, slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pprice = request.POST['price']
            pdays = request.POST['days']
            pletter = request.POST['cletter']
            user = User.objects.get(id=request.user.id)
            uf = user.first_name
            proj = ApprovedProject.objects.get(slug=slug)
            usr = UserImage.objects.get(user__id=request.user.id)
            uimg = usr.image
            ptitle = proj.title
            puser = proj.user
            pcurrency = proj.currency
            prop = Proposals(ptitle=ptitle, projuser=puser, projsender=user, senderimg=uimg, currency=pcurrency,
                             price=pprice, days=pdays, description=pletter)
            prop.save()
            notifi = 'send a proposal for your project'
            noti = Notifications(user=puser, opuser=uf, ptitle=ptitle, notification=notifi)
            noti.save()
            return redirect(projects)
        else:
            return redirect(projectdetails)
    else:
        return redirect(signup)




def freelancerdetails(request,slug):
    ares = ApprovedResume.objects.get(slug=slug)
    uname = ares.user
    com = Completedproject.objects.filter(hireduser=uname).count()
    ong = Ongoingproject.objects.filter(hireduser=uname).count()
    bwon = int(com)+int(ong)
    rcount = Reviews.objects.filter(hireduser=uname).count()
    rev = Reviews.objects.filter(hireduser=uname)
    return render(request, 'view-profile.html', {'freelancer': ares, 'review': rev, 'completed': com,
                                                 'bidswon': bwon, 'feedbacks': rcount})



@login_required()
def hiremessage(request, slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nam = request.POST['nam']
            msg = request.POST['message']
            usre = User.objects.get(id=request.user.id)
            unam = usre.username
            usr = UserImage.objects.get(user=usre)
            img = usr.image
            free = ApprovedResume.objects.get(slug=slug)
            fnam = free.user
            smg = Messages(sender=unam, img=img, receiver=fnam, message=msg)
            smg.save()
            return redirect(message)



def blogs(request):
    posts = Blog.objects.all()
    return render(request, 'blog.html', {'posts': posts})


def blogdetails(request, slug):
    post = Blog.objects.get(slug=slug)
    return render(request, 'blog-details.html', {'post':post})


def contactus(request):
    return render(request, 'contact.html')

@login_required()
def pendingprojects(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ptitle = request.POST['ptitle']
            pcategory = request.POST['pcategory']
            pcurrency = request.POST['pcurrency']
            pmin = request.POST['pmin']
            pmax = request.POST['pmax']
            skill1 = request.POST['skill1']
            skill2 = request.POST['skill2']
            skill3 = request.POST['skill3']
            skill4 = request.POST['skill4']
            skill5 = request.POST['skill5']
            pstarts = request.POST['pdate']
            pdescription = request.POST['pdescription']
            user = User.objects.get(id=request.user.id)
            img = UserImage.objects.get(user__id=request.user.id)
            usrimg = img.image
            pp = PendingProject(user=user, userimg=usrimg, title=ptitle, category=pcategory, currency=pcurrency,
                                minrate=pmin, maxrate=pmax, skill1=skill1, skill2=skill2, skill3=skill3, skill4=skill4,
                                skill5=skill5, jobstart=pstarts, description=pdescription)
            pp.save()
            usr = User.objects.get(is_staff=True)
            nusr = usr.username
            notifi = 'user is submitted a project for approval'
            ns = Notifications(user=nusr, notification=notifi, opuser=user)
            ns.save()
            messages.success(request, 'Bidlance team is check your project within 1 or 2 days, After List it')
            return redirect(postproject)
        else:
            return redirect(postproject)
    else:
        return redirect(signup)


@login_required()
def pendingresume(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            rname = request.POST['flname']
            rdesignation = request.POST['dsg']
            rcurrency = request.POST['acurrency']
            rrate = request.POST['rate']
            rgender = request.POST['sex']
            rcategory = request.POST['acategory']
            alocation = request.POST['loc']
            img = request.FILES['npic']
            aoverview = request.POST['over']
            askill1 = request.POST['skill1']
            askill2 = request.POST['skill2']
            askill3 = request.POST['skill3']
            askill4 = request.POST['skill4']
            askill5 = request.POST['skill5']
            alang1 = request.POST['lang1']
            alang2 = request.POST['lang2']
            alang3 = request.POST['lang3']
            alang4 = request.POST['lang4']
            aextitle = request.POST['extitle']
            aexcompany = request.POST['excom']
            aexstart = request.POST['exstart']
            aexend = request.POST['exend']
            aexsummary = request.POST['exsum']
            aedtitle = request.POST['edtitle']
            aeduniversity = request.POST['eduni']
            aedend = request.POST['edend']
            aedsummary = request.POST['edsum']
            amylink = request.POST['youlink']
            alink1 = request.POST['link1']
            alink2 = request.POST['link2']
            alink3 = request.POST['link3']
            alink4 = request.POST['link4']
            user = User.objects.get(id=request.user.id)
            em = user.email
            rp = PendingResume(user=user, userimg=img, fullname=rname, email=em, designation=rdesignation,
                               currency=rcurrency, rate=rrate, gender=rgender, category=rcategory, location=alocation,
                               overview=aoverview, skill1=askill1,skill2=askill2, skill3=askill3, skill4=askill4,
                               skill5=askill5, lang1=alang1, lang2=alang2, lang3=alang3, lang4=alang4, extitle=aextitle,
                               excompany=aexcompany, exstart=aexstart, exend=aexend, exsummary=aexsummary,
                               edtitle=aedtitle, eduniversity=aeduniversity, edend=aedend, edsummary=aedsummary,
                               mylink=amylink, slink1=alink1, slink2=alink2, slink3=alink3, slink4=alink4)
            rp.save()
            usr = User.objects.get(is_staff=True)
            nusr = usr.username
            notifi = 'user is submitted a resume for approval'
            ns = Notifications(user=nusr, notification=notifi, opuser=user)
            ns.save()
            return redirect(addresume)
        else:
            return redirect(addresume)
    else:
        return redirect(signup)






@login_required()
def editproject(request, pk):
    if request.user.is_authenticated:
        data = Categories.objects.all()
        pending = PendingProject.objects.get(pk=pk)
        return render(request, 'edit-project.html', {'pending': pending, 'category': data})


@login_required()
def saveeditproject(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            category = request.POST['newcategory']
            currency = request.POST['newcurrency']
            min = request.POST['newmin']
            max = request.POST['newmax']
            skill1 = request.POST['newskill1']
            skill2 = request.POST['newskill2']
            skill3 = request.POST['newskill3']
            skill4 = request.POST['newskill4']
            skill5 = request.POST['newskill5']
            starts = request.POST['newdate']
            description = request.POST['newdescription']
            pro = PendingProject.objects.get(pk=pk)
            pro.category = category
            pro.currency = currency
            pro.minrate = min
            pro.maxrate = max
            pro.skill1 = skill1
            pro.skill2 = skill2
            pro.skill3 = skill3
            pro.skill4 = skill4
            pro.skill5 = skill5
            pro.jobstart = starts
            pro.description = description
            pro.save()
            messages.success(request, 'your project is Edited')
            return redirect(manageprojects)
        else:
            return redirect(editproject)
    else:
        return redirect(signup)



@login_required()
def userprojdelete(request, slug):
    if request.user.is_authenticated:
        dele = ApprovedProject.objects.get(slug=slug)
        tit = dele.title
        delprop = Proposals.objects.get(ptitle=tit)
        delprop.delete()
        dele.delete()
        return redirect(manageprojects)
    else:
        return redirect(signup)







def signout(request):
    logout(request)
    return redirect(home)





def adminindex(request):
    us = User.objects.get(is_staff=True)
    usr = us.username
    noti = Notifications.objects.filter(user=usr)
    ucount = User.objects.filter(is_staff=False).count()
    acount = ApprovedProject.objects.all().count()
    arcount = ApprovedResume.objects.all().count()
    account = Completedproject.objects.all().count()
    return render(request, 'author/index.html', {'notification': noti, 'ucount': ucount, 'acount': acount,
                                                 'arcount': arcount, 'account': account})

@login_required()
def clearnotifications(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        us = user.username
        noti = Notifications.objects.filter(user=us)
        noti.delete()
        return redirect(adminindex)


@login_required()
def adminsettings(request):
    return render(request, 'author/settings.html')

@login_required()
def adminprofileedit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nusername = request.POST['newusername']
            nemail = request.POST['newemail']
            nfirst = request.POST['newfirst']
            nlast = request.POST['newlast']
            image = request.FILES.get('newpic')
            user = User.objects.all()
            User.objects.filter(id=request.user.id).update(username=nusername, email=nemail, first_name=nfirst, last_name=nlast)
            data = UserImage.objects.get(user__id=request.user.id)
            data.uname = nusername
            if 'newpic' not in request.FILES:
                data.image = data.image
            else:
                data.image = image
            data.save()
            messages.success(request, 'your profile is updated')
            return redirect(adminsettings)
        else:
            return redirect(adminsettings)
    else:
        return redirect(signup)

@login_required()
def adminchangepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            curpass = request.POST['cpass']
            newpassword = request.POST['npass']
            user = User.objects.get(id=request.user.id)
            un = user.username
            check = user.check_password(curpass)
            if check == True:
                user.set_password(newpassword)
                user.save()
                messages.success(request, 'Your Password is Changed')
                user = User.objects.get(username=un)
                login(request, user)
                return redirect(adminsettings)
            else:
                return redirect(adminsettings)
        else:
            return redirect(adminsettings)
    else:
        return redirect(signup)



@login_required()
def admincategories(request):
    cat = Categories.objects.all()
    return render(request, 'author/categories.html', {'category': cat})

@login_required()
def addcategory(request):
    if request.method == 'POST':
        new = request.POST['new']
        ad = Categories(category = new)
        ad.save()
        return redirect(admincategories)



@login_required()
def deletecategory(request, pk):
    dele = Categories.objects.get(pk=pk)
    dele.delete()
    return redirect(admincategories)


@login_required()
def adminprojects(request):
    pcount = PendingProject.objects.all().count()
    acount = ApprovedProject.objects.all().count()
    pprj = PendingProject.objects.all()
    aprj = ApprovedProject.objects.all()
    ocount = Ongoingproject.objects.all().count()
    ccount = Completedproject.objects.all().count()
    oprj = Ongoingproject.objects.all()
    cprj = Completedproject.objects.all()
    return render(request, 'author/projects.html', {'pending': pprj, 'pcount': pcount, 'acount': acount,
                                                    'approved': aprj, 'ongoing': oprj, 'completed': cprj,
                                                    'ocount': ocount, 'ccount': ccount})


def projectapprove(request, slug):
    if request.user.is_authenticated:
        data = PendingProject.objects.get(slug=slug)
        auser = data.user
        title = data.title
        aimg = data.userimg
        category = data.category
        currency = data.currency
        mrate = data.minrate
        marate = data.maxrate
        skill1 = data.skill1
        skill2 = data.skill2
        skill3 = data.skill3
        skill4 = data.skill4
        skill5 = data.skill5
        jobstart = data.jobstart
        description = data.description

        ap = ApprovedProject(user=auser, userimg=aimg, title=title, category=category,
                        currency=currency, minrate=mrate, maxrate=marate, skill1=skill1, skill2=skill2,
                        skill3=skill3, skill4=skill4,
                        skill5=skill5, jobstart=jobstart, description=description)
        ap.save()
        notifi = 'your Project is Approved'
        noti = Notifications(user=auser, ptitle=title, notification=notifi)
        noti.save()
        data.delete()
        return redirect(adminprojects)
    else:
        return redirect(signup)


def projectdelete(request, slug):
    if request.user.is_authenticated:
        data = PendingProject.objects.get(slug=slug)
        usr = data.user
        utitle = data.title
        notifi = 'your Project is Rejected'
        noti = Notifications(user=usr, ptitle=utitle, notification=notifi)
        noti.save()
        data.delete()
        return redirect(adminprojects)
    else:
        return redirect(signup)



@login_required()
def adminusers(request):
    usr = User.objects.filter(is_staff=False)
    usrimg = UserImage.objects.all()
    return render(request, 'author/users.html', {'data': usr})


@login_required()
def adminfreelancers(request):
    usr = ApprovedResume.objects.all()
    return render(request, 'author/freelancers.html', {'resume': usr})

@login_required()
def adminverifyresume(request):
    res = PendingResume.objects.all()
    return render(request, 'author/verify-resume.html', {'presume': res})


def approveresume(request, slug):
    if request.user.is_authenticated:
        dat = PendingResume.objects.get(slug=slug)
        ruser = dat.user
        rimg = dat.userimg
        rname = dat.fullname
        remail = dat.email
        rdesignation = dat.designation
        rcurrency = dat.currency
        rrate = dat.rate
        rgender = dat.gender
        rcategory = dat.category
        rlocation = dat.location
        roverview = dat.overview
        rskill1 = dat.skill1
        rskill2 = dat.skill2
        rskill3 = dat.skill3
        rskill4 = dat.skill4
        rskill5 = dat.skill5
        rlang1 = dat.lang1
        rlang2 = dat.lang2
        rlang3 = dat.lang3
        rlang4 = dat.lang4
        rextitle = dat.extitle
        rexcompany = dat.excompany
        rexstart = dat.exstart
        rexend = dat.exend
        rexsummary = dat.exsummary
        redtitle = dat.edtitle
        reduniversity = dat.eduniversity
        redend = dat.edend
        redsummary = dat.edsummary
        rmylink = dat.mylink
        rslink1 = dat.slink1
        rslink2 = dat.slink2
        rslink3 = dat.slink3
        rslink4 = dat.slink4
        usr = User.objects.get(username=ruser)
        ar = ApprovedResume(user=usr, userimg=rimg, fullname=rname, email=remail, designation=rdesignation,
                            currency=rcurrency, rate=rrate, gender=rgender, category=rcategory, location=rlocation,
                            overview=roverview, skill1=rskill1, skill2=rskill2, skill3=rskill3, skill4=rskill4,
                            skill5=rskill5, lang1=rlang1, lang2=rlang2, lang3=rlang3, lang4=rlang4, extitle=rextitle,
                            excompany=rexcompany, exstart=rexstart, exend=rexend, exsummary=rexsummary,
                            edtitle=redtitle, eduniversity=reduniversity, edend=redend, edsummary=redsummary,
                            mylink=rmylink, slink1=rslink1, slink2=rslink2, slink3=rslink3, slink4=rslink4)
        ar.save()
        notifi = 'your resume is Verified'
        noti = Notifications(user=ruser, notification=notifi)
        noti.save()
        dat.delete()
        return redirect(adminfreelancers)
    else:
        return redirect(signup)


@login_required()
def rejectresume(request, slug):
    if request.user.is_authenticated:
        dat = PendingResume.objects.get(slug=slug)
        un = dat.user
        notifi = 'your Resume is Rejected'
        noti = Notifications(user=un, notification=notifi)
        noti.save()
        dat.delete()
        return redirect(adminverifyresume)
    else:
        return redirect(signup)



@login_required()
def adminaddblog(request):
    return render(request, 'author/add-blog.html')

@login_required()
def blogsave(request):
    if request.method == 'POST':
        title = request.POST['btitle']
        description = request.POST['bdscp']
        pic = request.FILES.get('bpic')
        bl = Blog(title=title, description=description, bimg=pic)
        bl.save()
        messages.success(request, 'Blog Added Successfully')
        return redirect(adminaddblog)
    else:
        return redirect(adminaddblog)



@login_required()
def adminaddadmin(request):
    return render(request, 'author/add-admin.html')

@login_required()
def addadmin(request):
    if request.method =='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['em']
        password = request.POST['pass']
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_staff = True
        myuser.save()
        ui = UserImage(user=myuser, uname=username)
        ui.save()
        messages.success(request, 'successfully created admin account')
        return redirect(adminaddadmin)
    else:
        return redirect(adminaddadmin)
