from collections import OrderedDict

from rest_framework import serializers

from .models import (Profile, WorkExperience, WorkExperienceAdditionalData,
                     WorkExperienceRolesAndResponsibilities)


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import ContactUs

        model = ContactUs
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'subject',
            'message'
        )

    def send_email(self):
        from threading import Thread

        from django.conf import settings
        from django.core.mail import send_mail

        mail_data = dict(
            subject=f'New response {self.validated_data.get("subject")}',
            message=self.validated_data.get('message'),
            recipient_list=settings.EMAIL_RECIEPENTS,
            fail_silently=False,
            from_email='joe.philip@hotmail.co.in'
        )
        Thread(target=send_mail, kwargs=mail_data).start()


class RandomPasswordSerializer(serializers.Serializer):
    password_length = serializers.IntegerField(default=8)
    upper_case = serializers.BooleanField(default=False)
    lower_case = serializers.BooleanField(default=False)
    numeric = serializers.BooleanField(default=False)
    symbols = serializers.BooleanField(default=False)

    def validate_password_length(self, value):
        if value >= 8:
            return value
        raise serializers.ValidationError(
            'Password length should atleast be 8 characters')

    def validate(self, attrs):
        if True in attrs.values():
            return super().validate(attrs)
        raise serializers.ValidationError('Select atleast one')


class WorkExperienceAdditionalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperienceAdditionalData
        exclude = ('experience',)


class WorkExperienceRolesAndResponsibilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperienceRolesAndResponsibilities
        exclude = ('experience',)


class WorkExperienceSerializer(serializers.ModelSerializer):
    work_experience_additional_data = serializers.SerializerMethodField()
    work_experience_roles_and_responsibilities = serializers.SerializerMethodField()

    def get_work_experience_additional_data(self, instance: WorkExperience) -> OrderedDict:
        queryset = WorkExperienceAdditionalData.objects.filter(
            experience=instance
        )
        return WorkExperienceAdditionalDataSerializer(queryset, many=True).data

    def get_work_experience_roles_and_responsibilities(self, instance: WorkExperience) -> OrderedDict:
        queryset = WorkExperienceRolesAndResponsibilities.objects.filter(
            experience=instance
        )
        return WorkExperienceRolesAndResponsibilitiesSerializer(queryset, many=True).data

    class Meta:
        model = WorkExperience
        exclude = ('profile',)


class ProfileSerializer(serializers.ModelSerializer):
    work_experience = serializers.SerializerMethodField()

    def get_work_experience(self, instance: Profile) -> OrderedDict:
        queryset = WorkExperience.objects.filter(profile=instance)
        return WorkExperienceSerializer(queryset, context=self.context, many=True).data

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1
