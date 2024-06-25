from django.db import models
import os

# class BookGenre(models.Model):
#     genre = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    description = models.CharField(max_length=5000, null=True, blank=True, default='Sin descripción')
    # genres = models.ManyToManyField(BookGenre, related_name='books')

    def __str__(self):
        return self.title
    
    def delete(self):
        if self.cover_image:
            if os.path.isfile(self.cover_image.path):
                os.remove(self.cover_image.path)
        super().delete()

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

