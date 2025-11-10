from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    OBJECTIVE_CHOICES = [
        ('paixao', 'Paixão'),
        ('dinheiro', 'Dinheiro'),
        ('saude', 'Saúde'),
        ('autoconhecimento', 'Autoconhecimento'),
    ]

    FEELING_CHOICES = [
        ('feliz', 'Feliz'),
        ('ansioso', 'Ansioso'),
        ('estressado', 'Estressado'),
        ('motivado', 'Motivado'),
        ('outro', 'Outro'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Dados astrológicos
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    birth_time = models.TimeField(null=True, blank=True)
    birth_city = models.CharField(max_length=200, null=True, blank=True)
    birth_latitude = models.FloatField(null=True, blank=True)
    birth_longitude = models.FloatField(null=True, blank=True)
    birth_timezone = models.CharField(max_length=100, default='America/Sao_Paulo')

    # Perfil emocional
    current_feeling = models.CharField(max_length=20, choices=FEELING_CHOICES, null=True, blank=True)
    current_objective = models.CharField(max_length=30, choices=OBJECTIVE_CHOICES, null=True, blank=True)

    # Quiz completo
    quiz_completed = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Perfil"


class BirthChart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='birth_chart')

    # Signos principais
    sun_sign = models.CharField(max_length=20, null=True, blank=True)
    moon_sign = models.CharField(max_length=20, null=True, blank=True)
    ascendant_sign = models.CharField(max_length=20, null=True, blank=True)

    # Posições em graus
    sun_position = models.FloatField(null=True, blank=True)
    moon_position = models.FloatField(null=True, blank=True)
    ascendant_position = models.FloatField(null=True, blank=True)

    # Traits combinados (JSON field seria ideal, mas vamos usar TextField para simplificar)
    leadership = models.FloatField(default=0)
    courage = models.FloatField(default=0)
    charisma = models.FloatField(default=0)
    sensitivity = models.FloatField(default=0)
    intelligence = models.FloatField(default=0)

    # Descrições
    sun_description = models.TextField(null=True, blank=True)
    moon_description = models.TextField(null=True, blank=True)
    ascendant_description = models.TextField(null=True, blank=True)

    # Previsões
    daily_prediction = models.TextField(null=True, blank=True)
    weekly_prediction = models.TextField(null=True, blank=True)
    monthly_prediction = models.TextField(null=True, blank=True)

    # Horóscopo completo poético
    love_reading = models.TextField(null=True, blank=True)
    career_reading = models.TextField(null=True, blank=True)
    money_reading = models.TextField(null=True, blank=True)
    health_reading = models.TextField(null=True, blank=True)
    chinese_astrology = models.TextField(null=True, blank=True)
    tarot_reading = models.TextField(null=True, blank=True)
    numerology_reading = models.TextField(null=True, blank=True)
    planets_reading = models.TextField(null=True, blank=True)
    compatibility_reading = models.TextField(null=True, blank=True)
    psychic_reading = models.TextField(null=True, blank=True)

    # Timestamps
    calculated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Mapa Natal"


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('monthly', 'Mensal - R$ 19,99'),
        ('semester', 'Semestral - R$ 13,99/mês'),
        ('annual', 'Anual - R$ 11,99/mês'),
        ('free', 'Gratuito'),
    ]

    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('expired', 'Expirada'),
        ('cancelled', 'Cancelada'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

    def is_premium(self):
        return self.plan != 'free' and self.status == 'active'


# Signals para criar automaticamente perfil e assinatura quando um usuário é criado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Subscription.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    if hasattr(instance, 'subscription'):
        instance.subscription.save()
