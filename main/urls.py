from django.urls import path

from . import views

urlpatterns = [
    path('contact_us', views.ContactUsAPI.as_view()),
    path('random_password', views.RandomPasswordAPI.as_view()),
    path('profile', views.ProfileAPI.as_view())
]
