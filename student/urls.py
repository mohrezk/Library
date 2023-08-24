# from .views import StudentProfile, StudentRegister
from django.urls import path, include
from .views import Dashboard, StudentRegister, StudentProfile, CustomLoginView, PasswordChange
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    
    path('dashboard/', Dashboard.as_view(), name='student.dashboard'),
    path('register/', StudentRegister.as_view(), name='student.register'),
    path('profile/', StudentProfile.as_view(), name='student.profile'),
    path('change-password', PasswordChange.as_view(), name='student.change_password')
]