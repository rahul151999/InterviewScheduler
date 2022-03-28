from django.contrib import admin

from scheduler_apis.models import User, InterviewerAvailability, CandidateAvailability

admin.site.register(User)
admin.site.register(InterviewerAvailability)
admin.site.register(CandidateAvailability)
