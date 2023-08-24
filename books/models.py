from django.db import models
from student.models import Student
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    available_copies = models.IntegerField()
    image = models.ImageField(upload_to='books/images',  null=True, blank=True)

    def __str__(self):
        return self.title

    def get_image_url(self):
        return  f"/media/{self.image}"



class BorrowBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    
    returned = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title
