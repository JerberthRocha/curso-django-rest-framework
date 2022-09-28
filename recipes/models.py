from collections import defaultdict
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import F, Value
from django.db.models.functions import Concat
from tag.models import Tag
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id')


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(
        max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(verbose_name=_('Preparation Time'))
    preparation_time_unit = models.CharField(
        max_length=65,
        verbose_name=_('Preparation Time Unit')
    )
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(
        max_length=65,
        verbose_name=_('Servings Unit')
    )
    preparation_steps = models.TextField(verbose_name=_('Preparation Steps'))
    preparation_steps_is_html = models.BooleanField(
        default=False,
        verbose_name=_('Preparation Steps is HTML?')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published?')
    )
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/',
        blank=True,
        default='',
        verbose_name=_('Image')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name=_('Category')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Author')
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        default='',
        verbose_name=_('Tag')
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    @staticmethod
    def resize_image(image, new_width=1000):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return
        
        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(
            image_full_path,
            optimize=True,
            quanlity=50,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 1000)
            except FileNotFoundError:
                ...

        return saved

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
