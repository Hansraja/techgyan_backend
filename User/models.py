from django.db import models

# Create your models here.
from django.core import validators
from django.utils.deconstruct import deconstructible

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from User.Utils.config import UserManager
from nanoid import generate

@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[a-zA-Z0-9_]{3,30}$"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and _ characters."
    )
    flags = 0

class User(AbstractBaseUser, PermissionsMixin):
    key = models.CharField(max_length=24, unique=True, editable=False)
    username_validator = UsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=190,
        unique=True,
        help_text=_('Required. 190 characters or fewer. Letters, digits and _ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },)
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=254,
        help_text=_('Required. Enter a valid email address.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    image = models.ForeignKey('Common.Image', on_delete=models.SET_NULL, null=True, blank=True)
    sex = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    saved_stories = models.ManyToManyField('Content.Story', related_name='saved_by', blank=True)
    saved_posts = models.ManyToManyField('Content.Post', related_name='saved_by', blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = generate(size=24)
        super().save(*args, **kwargs)
        
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)