from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import CreateView, UpdateView,DetailView
from django.contrib.auth.views import LoginView
from .forms import StudentCreation, StudentEdit
from .models import Student
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from books.models import BorrowBook, Book
from django.urls import reverse, reverse_lazy
from django.contrib import messages

# Create your views here.

class Dashboard(LoginRequiredMixin, View):
    login_url = 'student/login'
    
    def get(self, request):
        student = request.user
        borrowed_books = BorrowBook.objects.filter(student=student)
        returned_all = BorrowBook.objects.filter(student=student, returned=False).exists()
        
        context =  {'borrowed_books': borrowed_books, 'returned_all':returned_all}
        return render(request, 'student/dashboard.html', context) 



class CustomLoginView(LoginView):
    
    def form_valid(self, form):
        super().form_valid(form)

        if self.request.user.is_superuser:
            return redirect('admin.dashboard') 
        else:
            return redirect('student.dashboard')



class StudentRegister(CreateView):
    model =  Student
    template_name = 'student/register.html'
    success_url = '/student/login'
    form_class = StudentCreation

    def form_valid(self, form):
        response = super().form_valid(form)

        student_id = self.object.student_id

        messages.success(self.request, f"You registered successfully and your Student ID is {student_id}")

        return response

class StudentProfile(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentEdit
    template_name = 'student/profile.html'
    context_object_name = 'student'
    success_url = '/student/dashboard'

    def get_object(self, queryset=None):

        return self.request.user



class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'student/change_password.html'
    
    success_url = reverse_lazy('login')  
    def form_valid(self, form):
        response = super().form_valid(form)

        self.request.session.flush()

        messages.success(self.request, "Password successfully changed. Login with your new password.")

        return response
