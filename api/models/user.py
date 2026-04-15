from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models





phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Phone number must be entered in the format: '+998xxxxxxxxx'. Up to 9 digits allowed."
)

LANG_CHOICES = (
        ('uz', "O'zbek"),
        ('en', 'English'),
        ('ru', 'Русский'),
    )


tarif = (
    ('standard', 'Standard'),
    ('premium', 'Premium'),
    ('pro', 'Pro'),
)
class User(AbstractUser):
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    sharif = models.CharField(max_length=20, null=True, blank=True)

    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='uz', null=True)
    tarif = models.CharField(max_length=20, choices=tarif, default="Standard", null=True, blank=False)

    image = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'  # Mana shu qator Djangoga "username o'rniga emailni ishlat" deydi
    REQUIRED_FIELDS = ['username']  # Email doimiy bo'lgani uchun bu bo'sh bo'lishi mumkin

    def __str__(self):
        return self.first_name if self.first_name else self.username

