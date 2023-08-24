from django.urls import path
from .views import BookListView, BookDetailView, BorrowBookView, ReturnBookView, AddBook, UpdateBook, DeleteBook
urlpatterns = [
    path('', BookListView.as_view(), name='book.list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book.details'),
    path('borrow/<int:book_id>/', BorrowBookView.as_view(), name='book.borrow'),
    path('return/<int:book_id>/', ReturnBookView.as_view(), name='book.return'),

    path('add/', AddBook.as_view(), name='book.create'),
    path('edit/<int:pk>/', UpdateBook.as_view(), name='book.edit'),
    path('delete/<int:pk>/', DeleteBook.as_view(), name='book.delete'),
]
