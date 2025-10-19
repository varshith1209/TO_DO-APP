# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        print(f"Welcome email sent to {instance.username}")  # demo print
        # Uncomment below to send real email (requires email backend setup)
        """
        send_mail(
            subject='Welcome to MySite!',
            message=f'Hi {instance.username}, welcome to MySite!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )
        """

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        from .models import Profile
        Profile.objects.create(user=instance)
        print(f"Profile created for {instance.username}")
