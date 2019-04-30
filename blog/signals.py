from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from .models import Post


def slugify_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slugify_pre_save_receiver, sender=Post)