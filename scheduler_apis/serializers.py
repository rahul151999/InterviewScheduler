from rest_framework import serializers

from scheduler_apis.models import CandidateAvailability, InterviewerAvailability


class CandidateAvailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer to add candidate availability.
    """

    class Meta:
        model = CandidateAvailability

        fields = ['id', 'candidate', 'interview_date', 'start_time', 'end_time']

        extra_kwargs = {'candidate': {'required': False}}


class InterviewerAvailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer to add interviewer availability.
    """

    class Meta:
        model = InterviewerAvailability

        fields = ['id', 'interviewer', 'interview_date', 'start_time', 'end_time']

        extra_kwargs = {'interviewer': {'required': False}}
