from django.urls import path
from apps.authorization.views import RegistrationView, ProfileView

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('profile/<pk>/', ProfileView.as_view())
]
