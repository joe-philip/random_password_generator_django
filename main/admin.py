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


class ProjectsAdmin(admin.ModelAdmin):
    list_filter = ('profile',)


class WorkExperienceRolesAndResponsibilitiesAdmin(admin.ModelAdmin):
    list_filter = ('experience',)


class WorkExperienceAdditionalDataAdmin(admin.ModelAdmin):
    list_filter = ('experience',)


class WorkExperienceAdmin(admin.ModelAdmin):
    list_filter = ('profile',)


admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile)
admin.site.register(Skills)
admin.site.register(SocialMedia)
admin.site.register(WorkExperience)
admin.site.register(
    WorkExperienceAdditionalData,
    WorkExperienceAdditionalDataAdmin
)
admin.site.register(
    WorkExperienceRolesAndResponsibilities,
    WorkExperienceRolesAndResponsibilitiesAdmin
)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(ProjectLinks, ProjectLinksAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
