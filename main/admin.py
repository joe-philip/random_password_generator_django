from django.contrib import admin

from .models import ContactUs, Profile, Skills, SocialMedia

# Register your models here.


class ContactUsAdmin(admin.ModelAdmin):
    search_fields = list_display = (
        'first_name',
        'last_name',
        'phone_number',
        'email',
        'subject',
        'message'
    )

    class Meta:
        model = ContactUs


admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile)
admin.site.register(Skills)
admin.site.register(SocialMedia)
