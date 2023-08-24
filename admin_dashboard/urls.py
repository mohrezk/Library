from django.urls import path, include
from .views import AdminDashboardView, Students, StudentDetails, PasswordChange

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin.dashboard'),
    path('students/', Students.as_view(), name="admin_dashboard.students"),
    path('students/<int:pk>/', StudentDetails.as_view(), name='student.details'),
    path('change-password/', PasswordChange.as_view(), name='change_password'),
    # path('borrow/', BorrowedBooks.as_view(), name="admin_dashboard.borrow")

]
