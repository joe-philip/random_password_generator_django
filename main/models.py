from django.db import models

# Create your models here.


class ContactUs(models.Model):
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=150, null=True)
    email = models.EmailField(max_length=254, null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField()

    class Meta:
        db_table = 'contact_us'
        verbose_name = 'Contact us'
        verbose_name_plural = 'Contact us'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Skills(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'skills'
        verbose_name = 'Skill'

    def __str__(self) -> str: return self.name


class SocialMedia(models.Model):
    link = models.URLField()
    icon = models.CharField(max_length=20)

    class Meta:
        db_table = 'social_media'
        verbose_name = 'Social media'

    def __str__(self) -> str: return self.icon


class Profile(models.Model):
    banner_img = models.ImageField(upload_to='banner/')
    profile_img = models.ImageField(upload_to='profile_img')
    info = models.TextField()
    skills = models.ManyToManyField(Skills)
    social_media = models.ManyToManyField(SocialMedia)

    class Meta:
        db_table = 'profile'
        verbose_name = 'Profile'

    def __str__(self) -> str: return f'{self.id}'


class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    logo = models.ImageField(upload_to='work_experience/logos')
    company_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'work_experience'
        verbose_name = 'Work experience'

    def __str__(self) -> str: return self.title


class WorkExperienceAdditionalData(models.Model):
    experience = models.ForeignKey(WorkExperience, on_delete=models.CASCADE)
    key = models.CharField(max_length=20)
    value = models.TextField()

    class Meta:
        db_table = 'work_experience_additional_data'
        verbose_name = 'Work experience additional data'

    def __str__(self) -> str: return f'{self.key}: {self.value}'


class WorkExperienceRolesAndResponsibilities(models.Model):
    experience = models.ForeignKey(WorkExperience, on_delete=models.CASCADE)
    label = models.TextField()

    class Meta:
        db_table = 'work_experience_roles_and_responsibilities'
        verbose_name = 'Work experience role and responsibility'
        verbose_name = 'Work experience roles and responsibilities'

    def __str__(self) -> str: return self.label


class Projects(models.Model):
    title = models.CharField(max_length=50)
    title_link = models.URLField(null=True)
    description = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'

    def __str__(self) -> str: return self.title


class ProjectLinks(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.PROTECT)
    label = models.CharField(max_length=50)
    link = models.URLField()

    class Meta:
        db_table = 'project_links'
        verbose_name = 'Project link'

    def __str__(self) -> str: return f'{self.id}'
