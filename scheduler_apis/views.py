from datetime import datetime, timedelta

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scheduler_apis.models import InterviewerAvailability, User, CandidateAvailability
from scheduler_apis.serializers import CandidateAvailabilitySerializer, InterviewerAvailabilitySerializer


class CandidateAvailabilityAPIView(generics.RetrieveAPIView):
    """
    To add candidate available slots
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateAvailabilitySerializer

    def post(self, request):
        request.data['candidate'] = self.request.user.id
        request.data['start_time'] = datetime.fromtimestamp(request.data['start_time'])
        request.data['end_time'] = datetime.fromtimestamp(request.data['end_time'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success"})


class InterviewerAvailabilityAPIView(generics.RetrieveAPIView):
    """
       To add interviewer available slots
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = InterviewerAvailabilitySerializer

    def post(self, request):
        request.data['interviewer'] = self.request.user.id
        request.data['start_time'] = datetime.fromtimestamp(request.data['start_time'])
        request.data['end_time'] = datetime.fromtimestamp(request.data['end_time'])
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success"})


class InterviewerScheduleAPIView(APIView):
    """
    To check availability of slots
    """

    def post(self, request):
        time_slots = []
        validated_data = self.request.data
        candidate_id = validated_data['candidate_id']
        interviewer_id = validated_data['interviewer_id']
        interview_date = validated_data['interview_date']

        candidate = User.objects.filter(id=candidate_id).first()
        candidate_availability = CandidateAvailability.objects.filter(candidate=candidate,
                                                                      interview_date=interview_date).first()

        interviewer = User.objects.filter(id=interviewer_id).first()
        interviewer_availability = InterviewerAvailability.objects.filter(interviewer=interviewer,
                                                                          interview_date=interview_date).first()

        # Checking whether candidate and interviewer is available on the particular date
        if candidate_availability and interviewer_availability:
            candidate_start_time = candidate_availability.start_time
            candidate_end_time = candidate_availability.end_time
            interviewer_start_time = interviewer_availability.start_time
            interviewer_end_time = interviewer_availability.end_time

            if candidate_start_time > interviewer_start_time and interviewer_end_time >= (
                    candidate_start_time + timedelta(hours=1)):
                slot_start_time = candidate_start_time
                while slot_start_time + timedelta(hours=1) <= interviewer_end_time:
                    time_slots.append(
                        (slot_start_time.strftime('%H:%M'), (slot_start_time + timedelta(hours=1)).strftime('%H:%M')))
                    slot_start_time = slot_start_time + timedelta(hours=1)

            elif candidate_start_time < interviewer_start_time and candidate_end_time >= (
                    interviewer_start_time + timedelta(hours=1)):
                slot_start_time = interviewer_start_time
                while slot_start_time + timedelta(hours=1) <= candidate_end_time:
                    time_slots.append(
                        (slot_start_time.strftime('%H:%M'), (slot_start_time + timedelta(hours=1)).strftime('%H:%M')))
                    slot_start_time = slot_start_time + timedelta(hours=1)

            else:
                time_slots = []

        return Response({"time_slots": time_slots})
