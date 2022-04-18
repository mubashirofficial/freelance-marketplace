from django.contrib import admin
from.models import UserImage, Categories, PendingProject, ApprovedProject, Notifications, PendingResume
from.models import ApprovedResume, Proposals, Messages, Ongoingproject, Completedproject, Reviews, Blog
# Register your models here.
admin.site.register(UserImage)
admin.site.register(Categories)
admin.site.register(PendingProject)
admin.site.register(ApprovedProject)
admin.site.register(Notifications)
admin.site.register(PendingResume)
admin.site.register(ApprovedResume)
admin.site.register(Proposals)
admin.site.register(Messages)
admin.site.register(Ongoingproject)
admin.site.register(Completedproject)
admin.site.register(Reviews)
admin.site.register(Blog)



