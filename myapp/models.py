
from django.db import models

# Create your models here.


class user(models.Model):
    id = models.AutoField(primary_key=True)
    book= models.CharField(max_length=30)
    author= models.CharField(max_length=30)
    publication= models.CharField(max_length=45)
    booktypes = models.CharField(max_length=45)
    date= models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ['-id']  # Default ordering by ID
        

    
    def __str__(self):
        return f"{self.book}"





    