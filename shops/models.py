from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import uuid
from django.utils import timezone
from auditlog.registry import auditlog


class ShopManager(BaseUserManager):
    def create_shop(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Shops(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    shop_uuid = models.UUIDField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    objects = ShopManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perpms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Locals(models.Model):
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, to_field='shop_uuid')
    name = models.CharField(unique=True, max_length=50)


class Faces(models.Model):
    landmarks = models.CharField(max_length = 2500)
    created_at = models.DateTimeField(default=timezone.now())
    active = models.BooleanField(default=True)


class Faces_in_shops(models.Model):
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, to_field='shop_uuid')
    face = models.ForeignKey(Faces, on_delete=models.CASCADE, to_field='id')
    local = models.ForeignKey(Locals, on_delete=models.CASCADE, to_field='id')
    counts = models.IntegerField()
    time = models.DateTimeField(default=timezone.now())


auditlog.register(Faces)
auditlog.register(Shops)
auditlog.register(Locals)
auditlog.register(Faces_in_shops)
