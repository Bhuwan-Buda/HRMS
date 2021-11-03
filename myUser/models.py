from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

LEVELS = (
    ('S', 'School'),
    ('C', 'College'),
    ('U', 'University')
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)


class UserManager(BaseUserManager):
    def create_user(self, email, fullname, address, password=None):
        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            address=address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, address, password=None):
        user = self.create_user(
            email, fullname, address, password
        )
        user.is_admin=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    fullname = models.CharField(max_length=100)
    contactNo = models.CharField(unique=True, null=True, max_length=20)
    address = models.CharField(max_length=100)
    isUser = models.BooleanField(default=False)
    isEmployee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'address']

    def __str__(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Education(models.Model):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=None)
    img = models.ImageField(upload_to='user/', default=None)
    institutionName = models.CharField(max_length=120)
    majorCourse = models.CharField(max_length=40)
    level = models.CharField(max_length=1, choices=LEVELS, default=None)
    country = models.CharField(max_length=100, default=None)
    file = models.FileField(default=None, upload_to='documents/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.fullname

    class Meta:
        db_table = 'education'


class Skill(models.Model):
    skill = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.fullname

    class Meta:
        db_table = 'skill'


class Experience(models.Model):
    experience = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.fullname

    class Meta:
        db_table = 'experience'
