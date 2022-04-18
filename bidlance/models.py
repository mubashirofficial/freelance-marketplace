from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from autoslug import AutoSlugField
from django.db.models import Max
from django.db.models.signals import pre_save


class Categories(models.Model):
    category = models.CharField(max_length=40)


class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='default', default='default/default.jpg')
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 150 or img.width > 145:
            output_size = (150, 145)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Notifications(models.Model):
    user = models.CharField(max_length=50)
    opuser = models.CharField(max_length=50)
    ptitle = models.CharField(max_length=200)
    notification = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']


class PendingProject(models.Model):
    user = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)
    userimg = models.ImageField()
    category = models.CharField(max_length=30)
    currency = models.CharField(max_length=10)
    minrate = models.IntegerField()
    maxrate = models.IntegerField()
    skill1 = models.CharField(max_length=50)
    skill2 = models.CharField(max_length=50)
    skill3 = models.CharField(max_length=50)
    skill4 = models.CharField(max_length=50)
    skill5 = models.CharField(max_length=50)
    jobstart = models.CharField(max_length=20)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.userimg.path)

        if img.height > 150 or img.width > 145:
            output_size = (150, 145)
            img.thumbnail(output_size)
            img.save(self.userimg.path)


class ApprovedProject(models.Model):
    user = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)
    userimg = models.ImageField()
    category = models.CharField(max_length=30)
    currency = models.CharField(max_length=10)
    minrate = models.IntegerField()
    maxrate = models.IntegerField()
    skill1 = models.CharField(max_length=50)
    skill2 = models.CharField(max_length=50)
    skill3 = models.CharField(max_length=50)
    skill4 = models.CharField(max_length=50)
    skill5 = models.CharField(max_length=50)
    jobstart = models.CharField(max_length=20)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.userimg.path)

        if img.height > 150 or img.width > 145:
            output_size = (150, 145)
            img.thumbnail(output_size)
            img.save(self.userimg.path)


class PendingResume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userimg = models.ImageField()
    fullname = models.CharField(max_length=80)
    slug = AutoSlugField(populate_from='user', unique=True, null=True, default=None)
    email = models.EmailField(max_length=100)
    designation = models.CharField(max_length=80)
    currency = models.CharField(max_length=10)
    rate = models.IntegerField()
    gender = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    overview = models.TextField()
    skill1 = models.CharField(max_length=50)
    skill2 = models.CharField(max_length=50)
    skill3 = models.CharField(max_length=50)
    skill4 = models.CharField(max_length=50)
    skill5 = models.CharField(max_length=50)
    lang1 = models.CharField(max_length=50)
    lang2 = models.CharField(max_length=50)
    lang3 = models.CharField(max_length=50)
    lang4 = models.CharField(max_length=50)
    extitle = models.CharField(max_length=100)
    excompany = models.CharField(max_length=100)
    exstart = models.CharField(max_length=50)
    exend = models.CharField(max_length=50)
    exsummary = models.TextField()
    edtitle = models.CharField(max_length=100)
    eduniversity = models.CharField(max_length=50)
    edend = models.CharField(max_length=50)
    edsummary = models.TextField()
    mylink = models.URLField(max_length=200)
    slink1 = models.URLField(max_length=200)
    slink2 = models.URLField(max_length=200)
    slink3 = models.URLField(max_length=200)
    slink4 = models.URLField(max_length=200)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.userimg.path)

        if img.height > 150 or img.width > 152:
            output_size = (150, 152)
            img.thumbnail(output_size)
            img.save(self.userimg.path)


class ApprovedResume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userimg = models.ImageField()
    fullname = models.CharField(max_length=80)
    slug = AutoSlugField(populate_from='user', unique=True, null=True, default=None)
    email = models.EmailField(max_length=100)
    designation = models.CharField(max_length=80)
    currency = models.CharField(max_length=10)
    rate = models.IntegerField()
    gender = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    overview = models.TextField()
    skill1 = models.CharField(max_length=50)
    skill2 = models.CharField(max_length=50)
    skill3 = models.CharField(max_length=50)
    skill4 = models.CharField(max_length=50)
    skill5 = models.CharField(max_length=50)
    lang1 = models.CharField(max_length=50)
    lang2 = models.CharField(max_length=50)
    lang3 = models.CharField(max_length=50)
    lang4 = models.CharField(max_length=50)
    extitle = models.CharField(max_length=100)
    excompany = models.CharField(max_length=100)
    exstart = models.CharField(max_length=50)
    exend = models.CharField(max_length=50)
    exsummary = models.TextField()
    edtitle = models.CharField(max_length=100)
    eduniversity = models.CharField(max_length=50)
    edend = models.CharField(max_length=50)
    edsummary = models.TextField()
    mylink = models.URLField(max_length=200)
    slink1 = models.URLField(max_length=200)
    slink2 = models.URLField(max_length=200)
    slink3 = models.URLField(max_length=200)
    slink4 = models.URLField(max_length=200)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.userimg.path)

        if img.height > 150 or img.width > 152:
            output_size = (150, 152)
            img.thumbnail(output_size)
            img.save(self.userimg.path)


class Proposals(models.Model):
    ptitle = models.CharField(max_length=200)
    projuser = models.CharField(max_length=50)
    projsender = models.CharField(max_length=50)
    senderimg = models.ImageField()
    currency = models.CharField(max_length=20)
    price = models.IntegerField()
    number = models.CharField(max_length=30)
    days = models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.senderimg.path)

        if img.height > 150 or img.width > 152:
            output_size = (150, 152)
            img.thumbnail(output_size)
            img.save(self.senderimg.path)


class Messages(models.Model):
    sender = models.CharField(max_length=50)
    img = models.ImageField()
    receiver = models.CharField(max_length=50)
    message = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']


class Ongoingproject(models.Model):
    user = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    posted = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)
    rate = models.IntegerField()
    hiredon = models.DateField(auto_now_add=True)
    hireduser = models.CharField(max_length=50)
    hfname = models.CharField(max_length=50)
    hlname = models.CharField(max_length=50)
    himage = models.ImageField()

    class Meta:
        ordering = ['-hiredon']


class Completedproject(models.Model):
    user = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)
    rate = models.IntegerField()
    hiredon = models.CharField(max_length=20)
    hireduser = models.CharField(max_length=50)
    hfname = models.CharField(max_length=50)
    hlname = models.CharField(max_length=50)
    himage = models.ImageField()
    completed = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-completed']


class Reviews(models.Model):
    rfname = models.CharField(max_length=50)
    rlname = models.CharField(max_length=50)
    ruser = models.CharField(max_length=50)
    rimg = models.ImageField()
    hireduser = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    rating = models.IntegerField()
    review = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)
    bimg = models.ImageField()
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

