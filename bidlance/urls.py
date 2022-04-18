"""projectbidlance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/signup', views.signup, name='login/signup'),
    path('sign-up', views.registration, name='sign-up'),
    path('password-reset', views.passwordreset, name='password-reset'),
    path('resetpass', views.newpass, name='resetpass'),
    path('password-reset/<uidb64>/<token>/', views.resetsection, name='password-reset'),
    path('set-new-pass/<int:pk>', views.resetsuccess, name='set-new-pass'),
    path('login', views.signin, name='login'),
    path('index', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('post-a-project', views.postproject, name='post-a-project'),
    path('add-freelancer-resume', views.addresume, name='add-freelancer-resume'),
    path('settings', views.settings, name='settings'),
    path('logout', views.signout, name='logout'),
    path('messages', views.message, name='messages'),
    path('reviews', views.reviews, name='reviews'),
    path('manage-projects', views.manageprojects, name='manage-projects'),
    path('my-projects', views.myprojects, name='my-projects'),
    path('incoming-proposals', views.proposals, name='incoming-proposals'),
    path('preview-profile', views.previewprofile, name='preview-profile'),
    path('edit-resume', views.editresume, name='edit-resume'),
    path('saveedit-resume', views.saveeditresume, name='saveedit-resume'),
    path('projects', views.projects, name='projects'),
    path('search-projects', views.searchprojects, name='search-projects'),
    path('freelancers', views.freelancers, name='freelancers'),
    path('search-freelancers', views.searchfreelancers, name='search-freelancers'),
    path('project-details/<slug:slug>', views.projectdetails, name='project-details'),
    path('project-delete/<slug:slug>', views.userprojdelete, name='project-delete'),
    path('send-proposal/<slug:slug>', views.sendproposal, name='send-proposal'),
    path('view-profile/<str:projsender>', views.viewprofile, name='view-profile'),
    path('hire-message/<slug:slug>', views.hiremessage, name='hire-message'),
    path('send-msg/<int:pk>', views.sendmessageprop, name='send-msg'),
    path('msg-send/<int:pk>', views.messagesended, name='msg-send'),
    path('project-completed/<int:pk>', views.projectcompleted, name='project-completed'),
    path('write-review/<int:pk>', views.writereview, name='write-review'),
    path('save-review/<int:pk>', views.savereview, name='save-review'),
    path('freelancer-details/<slug:slug>', views.freelancerdetails, name='freelancer-details'),
    path('blog', views.blogs, name='blog'),
    path('blogdetails/<slug:slug>', views.blogdetails, name='blogdetails'),
    path('contact-us', views.contactus, name='contact-us'),
    path('update-profile', views.updateprofile, name='update-profile'),
    path('change-pass', views.changepassword, name='change-pass'),
    path('delete-account', views.deleteaccount, name='delete-account'),
    path('pending-projects', views.pendingprojects, name='pending-projects'),
    path('pending-resume', views.pendingresume, name='pending-resume'),
    path('<int:pk>/', views.editproject, name='edit-project'),
    path('saveedit<int:pk>/', views.saveeditproject, name='saveedit'),
    path('delete-notification', views.deletenotification, name='delete-notification'),
    path('delete-notifi', views.deletenotifi, name='delete-notifi'),








    path('bidlanceadmin/index', views.adminindex, name='bidlanceadmin/index'),
    path('bidlanceadmin/settings', views.adminsettings, name='bidlanceadmin/settings'),
    path('bidlanceadmin/categories', views.admincategories, name='bidlanceadmin/categories'),
    path('bidlanceadmin/add-category', views.addcategory, name='bidlanceadmin/add-category'),
    path('bidlanceadmin/delete<int:pk>', views.deletecategory, name='bidlanceadmin/delete'),
    path('bidlanceadmin/projects', views.adminprojects, name='bidlanceadmin/projects'),
    path('bidlanceadmin/clear-notification', views.clearnotifications, name='bidlanceadmin/clear-notification'),
    path('bidlanceadmin/approve-project<slug:slug>', views.projectapprove, name='bidlanceadmin/approve-project'),
    path('bidlanceadmin/delete-project<slug:slug>', views.projectdelete,name='bidlanceadmin/delete-project'),
    path('bidlanceadmin/update-profile', views.adminprofileedit, name='bidlanceadmin/update-profile'),
    path('bidlanceadmin/change-password', views.adminchangepassword, name='bidlanceadmin/change-password'),
    path('bidlanceadmin/add-admin', views.addadmin, name='bidlanceadmin/add-admin'),
    path('bidlanceadmin/users', views.adminusers, name='bidlanceadmin/users'),
    path('bidlanceadmin/freelancers', views.adminfreelancers, name='bidlanceadmin/freelancers'),
    path('bidlanceadmin/verifyresume', views.adminverifyresume, name='bidlanceadmin/verifyresume'),
    path('bidlanceadmin/approve-resume<slug:slug>', views.approveresume, name='bidlanceadmin/approve-resume'),
    path('bidlanceadmin/reject-resume<slug:slug>', views.rejectresume, name='bidlanceadmin/reject-resume'),
    path('bidlanceadmin/addblog', views.adminaddblog, name='bidlanceadmin/addblog'),
    path('bidlanceadmin/blog-save', views.blogsave, name='bidlanceadmin/blog-save'),
    path('bidlanceadmin/addadmin', views.adminaddadmin, name='bidlanceadmin/addadmin')

]
