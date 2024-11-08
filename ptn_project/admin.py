from django.contrib import admin

from ptn_project.models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(CollaboratorMiddleTable)
admin.site.register(UserFeedback)
admin.site.register(FeedbackImage)
admin.site.register(AIFeedbackSummary)
admin.site.register(Discussion)
admin.site.register(DiscussionImage)
admin.site.register(Comment)
admin.site.register(InComment)