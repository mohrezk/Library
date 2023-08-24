from django.shortcuts import render
from django.views import View
from student.models import Student
from books.models import Book, BorrowBook
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
# from .forms import PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.


class AdminOnly(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser



class AdminDashboardView(AdminOnly, View):
    # def test_func(self):
    #     return self.request.user.is_superuser

    def get(self, request):
        # books = BorrowBook.objects.all()
        books = BorrowBook.objects.filter(returned=False)
        return render(request, 'admin_dashboard/dashboard.html', {'books': books})


class Students(AdminOnly, View):
    template_name = "admin_dashboard/students.html"

    def get(self, request):
        search_query = request.GET.get('query')
        students = Student.objects.all()

        if search_query:
            students = students.filter(student_id=search_query)
            

        context = {
            'students': students,
            'search_query': search_query,
        }
        
        return render(request, self.template_name, context)



class StudentDetails(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'student/details.html'
    context_object_name = 'student'
    login_url = '/student/login'



class PasswordChange(LoginRequiredMixin, AdminOnly, PasswordChangeView):
    template_name = 'admin_dashboard/change_password.html'
    
    success_url = reverse_lazy('login')  
    def form_valid(self, form):
        response = super().form_valid(form)

        self.request.session.flush()

        messages.success(self.request, "Password successfully changed. Login with your new password.")

        return response

