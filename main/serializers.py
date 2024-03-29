from collections import OrderedDict

from rest_framework import serializers

from root.utils.utils import get_age

from .models import (ContactInfo, Profile, ProjectLinks, Projects,
                     WorkExperience, WorkExperienceAchievements,
                     WorkExperienceAdditionalData,
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


class WorkExperienceAchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperienceAchievements
        exclude = ('experience',)


class WorkExperienceSerializer(serializers.ModelSerializer):
    work_experience_additional_data = serializers.SerializerMethodField()
    work_experience_roles_and_responsibilities = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()

    def get_work_experience_additional_data(self, instance: WorkExperience) -> OrderedDict or list:
        queryset = WorkExperienceAdditionalData.objects.filter(
            experience=instance
        )
        return WorkExperienceAdditionalDataSerializer(queryset, many=True).data

    def get_work_experience_roles_and_responsibilities(self, instance: WorkExperience) -> OrderedDict or list:
        queryset = WorkExperienceRolesAndResponsibilities.objects.filter(
            experience=instance
        )
        return WorkExperienceRolesAndResponsibilitiesSerializer(queryset, many=True).data

    def get_achievements(self, instance: WorkExperience) -> OrderedDict or list:
        queryset = WorkExperienceAchievements.objects.filter(
            experience=instance
        )
        return WorkExperienceAchievementsSerializer(queryset, many=True).data

    class Meta:
        model = WorkExperience
        exclude = ('profile',)


class ProjectSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    def get_links(self, instance: Projects) -> OrderedDict:
        queryset = ProjectLinks.objects.filter(project=instance)
        return ProjectLinksSerializer(queryset, many=True).data

    class Meta:
        model = Projects
        exclude = ('profile',)

    def to_representation(self, instance: Projects) -> OrderedDict:
        data = super().to_representation(instance)
        data['description'] = instance.dynamic_project_info
        return data


class ProjectLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLinks
        exclude = ('project',)


class ProfileSerializer(serializers.ModelSerializer):
    work_experience = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()

    def get_work_experience(self, instance: Profile) -> OrderedDict or list:
        queryset = WorkExperience.objects.filter(
            profile=instance
        ).order_by('-created_at')
        return WorkExperienceSerializer(queryset, context=self.context, many=True).data

    def get_projects(self, instance: Profile) -> OrderedDict or list:
        queryset = Projects.objects.filter(
            profile=instance
        ).order_by('-created_at')
        return ProjectSerializer(queryset, many=True).data

    def get_contact_info(self, instance: Profile) -> OrderedDict or list:
        queryset = ContactInfo.objects.filter(profile=instance)
        return ContactInfoSerializer(queryset, many=True).data

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1

    def to_representation(self, instance: Profile) -> OrderedDict:
        data = super().to_representation(instance)
        if dob := instance.dob:
            data['contact_info'].append(
                {
                    'id': 0,
                    'key': 'Age',
                    'value': get_age(dob)
                }
            )
        return data


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        exclude = ('profile',)
