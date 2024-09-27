from django.db.models import Model, DateTimeField, SlugField, CharField
from django.utils.text import slugify


class TimeBaseModel(Model):
    updated_at = DateTimeField(verbose_name="Yaratilgan Vaqti", auto_now=True)
    created_at = DateTimeField(verbose_name="Yangilangan Vaqti", auto_now_add=True)

    class Meta:
        abstract = True


class SlugBaseModel(Model):
    name = CharField(verbose_name="Nomi", max_length=255)
    slug = SlugField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'
        super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)

    def __str__(self):
        return self.name
