from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import uuid

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (('admin','Admin'),('manager','Manager'),('user','User'))

    role = models.CharField(max_length = 20, choices = ROLE_CHOICES, default = 'user')
    is_approved = models.BooleanField(default= False)
    slug = models.SlugField( blank = True, null = True, unique = True)
    file = models.FileField(upload_to = 'task_files/',null = True,blank = True)
    images = models.ImageField(upload_to = 'task_images/',null = True,blank= True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.username)
            original_post = self.slug
            while CustomUser.objects.filter(slug = self.slug).exists():
                self.slug = f'{original_post} - {uuid.uuid4().hex[:6]}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=False)
    due_date = models.DateField(null=True, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title
