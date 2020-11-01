from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class YamDBUser(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    ROLE_MAX_LENGTH = max((len(c[0]) for c in Role.choices))
    AUTO_CREATE_USERNAME_PREFIX = 'yamdbuser-'

    # нельзя заводить с пустой почтой
    # каждый пользователь должен иметь уникальную почту
    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        if self.username:
            name = f'{self.username}:{self.email}'
        else:
            name = self.email
        return name


# если при создании пользователя не задан username, то
# то создаём уникальное имя
def random_username(sender, instance, **kwargs):
    if not instance.username:
        unique_username = (
            f'{YamDBUser.AUTO_CREATE_USERNAME_PREFIX}'
            f'{uuid.uuid4().hex[:10]}'
        )
        instance.username = unique_username


models.signals.pre_save.connect(random_username, sender=YamDBUser)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40, unique=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40, unique=True, null=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(max_length=2000, blank=True, null=True)
    genre = models.ForeignKey(Genre, blank=True, null=True,
                              on_delete=models.SET_NULL,
                              verbose_name="Жанр",
                              related_name="titles")
    category = models.ForeignKey(Category, blank=True, null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name="Категория",
                                 related_name="titles")

    def __str__(self):
        title = f'Произведение {self.name}'
        return title


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(YamDBUser,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор',
                               db_column='author')
    score = models.IntegerField('Рейтинг')
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date', ]

    def __str__(self):
        review = f'Отзыв {self.author} на {self.title}'
        return review


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Отзыв')
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(YamDBUser,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор',
                               db_column='author')
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date', ]

    def __str__(self):
        fragment = str(self.text)[:20]
        comment = f'Комментарий {self.author} с текстом {fragment}'
        return comment
