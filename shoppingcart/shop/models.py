from django.db import models
import os

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.cover_image:
            if os.path.isfile(self.cover_image.path):
                os.remove(self.cover_image.path)
        super().delete(*args, **kwargs)