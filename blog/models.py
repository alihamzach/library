from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from datetime import datetime,timedelta

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def with_perm(
            self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class MyUser(AbstractUser):
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class BusinessSettings(models.Model):
    business_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    currency = models.CharField(max_length=5)
    contact_number = models.CharField(max_length=15)
    rent_per_day = models.IntegerField()
    logo = models.ImageField(upload_to='abc')

    def __str__(self):
        return self.business_name


class Student(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    course = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    identification_number = models.CharField(max_length=13, null=True, blank=True)

    def __str__(self):
        return self.name


class BookDetail(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    pages = models.CharField(max_length=15)
    price = models.BigIntegerField()
    quantity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class BookingOrder(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book_detail = models.ForeignKey(BookDetail, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    from_date = models.DateField()
    to_date = models.DateField()
    rent_per_day = models.IntegerField(null=True, blank=True)
    days = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    request = models.BooleanField(default=False)

    def __str__(self):
        return self.student.name

# from django.db import models

# class FineCollect(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     collected_date = models.DateField()
#
#     def __str__(self):
#         return f"Fine collected from {self.student.name}"
#
#
# class BorrowBook(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     book_detail = models.ForeignKey(BookDetail, on_delete=models.CASCADE)
#     borrowed_date = models.DateField()
#     return_date = models.DateField(null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.student.name} borrowed {self.book_detail.title}"


def expiry():
    return datetime.today() + timedelta(days=15)


class IssueBook(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, null=True, blank=True, related_name="issue_book_user"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, blank=True, related_name="issue_book"
    )
    book1 = models.CharField(max_length=20)
    issue_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)

    def __str__(self):
        return self.student.name