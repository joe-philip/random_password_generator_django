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
