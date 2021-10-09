from django.db import models


# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length = 200, null = False)
    slug = models.SlugField(max_length=15, null = False, unique = True)
    description = models.TextField()

    def __str__(self):
        return self.title