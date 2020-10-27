from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)



class YamDBUser(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'
    ROLE_MAX_LENGTH = max((len(c[0]) for c in Role.choices))
    
    # нельзя заводить с пустой почтой
    # каждый пользователь должен иметь уникальную почту
    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length = ROLE_MAX_LENGTH,
        choices=Role.choices,
        default=Role.USER,
    )

    def __str__(self):
        if self.username:
            name = f'{self.username}:{self.email}'
        else:
            name = self.email
        return name


