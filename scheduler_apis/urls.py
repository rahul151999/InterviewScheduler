from django.urls import path

from scheduler_apis.views import CandidateAvailabilityAPIView, InterviewerScheduleAPIView, \
    InterviewerAvailabilityAPIView

urlpatterns = [
    # Endpoint to add candidate available slots
    path('candidate/time_slot/', CandidateAvailabilityAPIView.as_view(), name='candidate-time-slot'),
    # Endpoint to add interviewer available slots
    path('interviewer/time_slot/', InterviewerAvailabilityAPIView.as_view(), name='interviewer-time-slot'),
    # Endpoint to check available slots
    path('schedule/interview/', InterviewerScheduleAPIView.as_view(), name='schedule-interview'),
]
