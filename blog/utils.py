import string
import random
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    this is for django project and it assumes your instance
    has a model with a slug field and a title character field
    :param instance:
    :param new_slug:
    :return:
    """

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    randstr = random_string_generator(size=4)
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = f'{slug}-{randstr}'
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


