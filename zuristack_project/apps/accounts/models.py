from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify  # for slug

from .managers import CustomUserManager
from . import utils


# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields here
    username = None
    email = models.EmailField(unique=True)  # 

    slug = models.SlugField(blank=True, unique=True)

    USERNAME_FIELD = 'email'  # primary identifier for the user 
    REQUIRED_FIELDS = []  # required fields for the user

    objects = CustomUserManager()  # 

    class Meta:
        ordering = ['email']
        verbose_name = 'user'  # verbose name for the user

    def __str__(self):
        return self.email

    # Create a default slug /username for users if blank.
    def gen_random_slug(self):
        random_slug = slugify(self.first_name + self.last_name + utils.generate_random_id(5))

        while CustomUser.objects.filter(slug=random_slug).exists():
            random_slug = slugify(self.first_name + self.last_name + utils.generate_random_id(5))

        return random_slug

    def save(self, *args, **kwargs):
        # Check for a slug, if not create one.
        if not self.slug:
            self.slug = self.gen_random_slug()
        # Save
        super().save(*args, **kwargs)
