from django.contrib import admin

from .models import (ContactInfo, ContactUs, Profile, ProjectLinks, Projects,
                     Skills, SocialMedia, WorkExperience,
                     WorkExperienceAdditionalData,
                     WorkExperienceRolesAndResponsibilities)

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


class ContactInfoAdmin(admin.ModelAdmin):
    list_filter = ('profile',)


class ProjectLinksAdmin(admin.ModelAdmin):
    list_filter = ('project', 'project__profile')


admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile)
admin.site.register(Skills)
admin.site.register(SocialMedia)
admin.site.register(WorkExperience)
admin.site.register(WorkExperienceAdditionalData)
admin.site.register(WorkExperienceRolesAndResponsibilities)
admin.site.register(Projects)
admin.site.register(ProjectLinks, ProjectLinksAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
