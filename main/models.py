import requests
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
    name = models.CharField(max_length=30, unique=True)

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
    name = models.CharField(max_length=20)
    job_role = models.CharField(max_length=30)
    banner_img = models.ImageField(upload_to='banner/')
    profile_img = models.ImageField(upload_to='profile_img')
    info = models.TextField()
    skills = models.ManyToManyField(Skills)
    social_media = models.ManyToManyField(SocialMedia)
    resume = models.FileField(upload_to='resume')
    dob = models.DateField(null=True)

    class Meta:
        db_table = 'profile'
        verbose_name = 'Profile'

    def __str__(self) -> str: return self.name


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
        verbose_name_plural = 'Work experience roles and responsibilities'

    def __str__(self) -> str: return self.label


class WorkExperienceAchievements(models.Model):
    experience = models.ForeignKey(WorkExperience, on_delete=models.CASCADE)
    label = models.CharField(max_length=30)

    class Meta:
        db_table = 'work_experience_achievements'
        verbose_name = 'Work experience achievement'

    def __str__(self) -> str: return self.label


class Projects(models.Model):
    class ProjectStoreTypeChoices(models.IntegerChoices):
        VS_CODE_MARKETPLACE = 1, 'vs_code_marketplace'
        PYPI = 2, 'PyPI'
        NA = 3, 'NA'

    class RepoTypeChoices(models.IntegerChoices):
        GITLAB = 1, 'gitlab'
        GITHUB = 2, 'github'
        NA = 3, 'NA'
    title = models.CharField(max_length=50)
    title_link = models.URLField(null=True)
    description = models.TextField(null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    project_store_type = models.IntegerField(
        ProjectStoreTypeChoices.choices,
        default=3
    )
    store_url = models.URLField(null=True)
    repo_url = models.URLField(null=True)
    repo_type = models.IntegerField(
        RepoTypeChoices.choices,
        default=3
    )

    @property
    def dynamic_project_info(self) -> str:
        if self.project_store_type == 2 and self.store_url:
            response = requests.get(self.store_url).json()
            return response.get('info', '').get('summary', '')
        return self.description

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

    def __str__(self) -> str: return self.label


class ContactInfo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    key = models.CharField(max_length=40)
    value = models.CharField(max_length=40)

    class Meta:
        db_table = 'contact_info'
        verbose_name = 'Contact info'

    def __str__(self) -> str: return f'{self.key}: {self.value}'
