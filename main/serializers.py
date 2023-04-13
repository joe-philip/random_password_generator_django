from rest_framework import serializers


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
            fail_silently=True
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
