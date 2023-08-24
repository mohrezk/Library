from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BorrowBook
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from student.models import Student
from django.contrib import messages
from .forms import BookForm

from django.utils import timezone
from django.views import View
# Create your views here.


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/list.html'
    context_object_name = 'books'
    login_url = '/student/login'


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/details.html'
    context_object_name = 'book'
    login_url = '/student/login'


class AddBook(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/create.html'
    success_url = '/books'


class UpdateBook(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/edit.html'
    context_object_name = 'book'
    success_url = '/books'


class DeleteBook(DeleteView):
    model = Book
    template_name = 'books/delete.html'
    success_url = '/books'


class BorrowBookView(View):
    template_name = 'books/borrow.html'

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        
        student = get_object_or_404(Student, pk=request.user.id)
        already_borrowed = BorrowBook.objects.filter(student=student, returned=False).exists()

        context = {'book': book, 'already_borrowed': already_borrowed}
        return render(request, self.template_name, context)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        student = get_object_or_404(Student, pk=request.user.id)
        already_borrowed = BorrowBook.objects.filter(student=student, returned=False).exists()

        if not already_borrowed and book.available_copies > 0:
            return_date = request.POST.get('return_date', None)
            BorrowBook.objects.create(student=student, book=book, return_date=return_date)
            book.available_copies -= 1
            book.save()

        return redirect("/student/dashboard")


class ReturnBookView(View):
    template_name = 'books/return.html'

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)

        return render(request, self.template_name, {'book': book})
        
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        student = get_object_or_404(Student, pk=request.user.id)

        borrowed_book = BorrowBook.objects.get(student=student, book=book, returned=False)

        book.available_copies += 1
        book.save()

        borrowed_book.return_date = timezone.now() 
        borrowed_book.returned = True
        borrowed_book.save()

        return redirect("/student/dashboard")



# @login_required
# def return_book(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)
#     student = get_object_or_404(Student, pk=request.user.id)


#     borrowed_book = BorrowBook.objects.get(student=student, book=book)

#     book.available_copies += 1
#     book.save()

#     borrowed_book.delete()

#     return redirect("/student/dashboard")

# @login_required
# def borrow_book(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)
#     student = get_object_or_404(Student, pk=request.user.id)

#     already_borrowed = BorrowBook.objects.filter(student=student).exists()

#     if not already_borrowed and book.available_copies > 0:
#         BorrowBook.objects.create(student=student, book=book)
#         book.available_copies -= 1
#         book.save()
    

#     return redirect("/student/dashboard")



