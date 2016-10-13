from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from .models import Question, Choice


@receiver(post_save, sender=Question)
@receiver(post_save, sender=Choice)
def mcq_post_save(sender, **kwargs):
    # Mark MCQs as changed
    cache.set('mcqs_flag', False)
