from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.contrib.auth.hashers import make_password
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(
        self,
        nama,
        email,
        password,
        role,
        is_staff=False,
        is_superuser=False
    ):
        user = self.model(
            nama=nama,
            email=email,
            password=password,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(
        self,
        nama,
        email,
        password,
        role="Super User",
        is_staff=True,
        is_superuser=True
    ):
        user = self.create_user(
            nama=nama,
            email=email,
            password=password,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        return user
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    objects = UserManager()

    Role = (
        ("User","User"),
        ("Admin","Admin"),
        ("Super User","Super User")
    )

    nama=models.CharField(max_length=150)
    email=models.EmailField(unique=True,max_length=150)
    role = models.CharField(choices=Role,max_length=50)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nama","password"]

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nama