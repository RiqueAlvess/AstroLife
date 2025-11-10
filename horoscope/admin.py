from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import UserProfile, BirthChart, Subscription


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ('user', 'birth_date', 'birth_city', 'quiz_completed', 'created_at')
    list_filter = ('gender', 'quiz_completed', 'current_objective', 'current_feeling')
    search_fields = ('user__username', 'user__email', 'birth_city')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Dados Astrológicos', {
            'fields': ('gender', 'birth_date', 'birth_time', 'birth_city',
                      'birth_latitude', 'birth_longitude', 'birth_timezone')
        }),
        ('Perfil Emocional', {
            'fields': ('current_feeling', 'current_objective')
        }),
        ('Status', {
            'fields': ('quiz_completed', 'created_at', 'updated_at')
        }),
    )


@admin.register(BirthChart)
class BirthChartAdmin(ModelAdmin):
    list_display = ('user', 'sun_sign', 'moon_sign', 'ascendant_sign', 'calculated_at')
    list_filter = ('sun_sign', 'moon_sign', 'ascendant_sign')
    search_fields = ('user__username',)
    readonly_fields = ('calculated_at', 'updated_at')

    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Signos Principais', {
            'fields': ('sun_sign', 'sun_position', 'sun_description',
                      'moon_sign', 'moon_position', 'moon_description',
                      'ascendant_sign', 'ascendant_position', 'ascendant_description')
        }),
        ('Traços de Personalidade', {
            'fields': ('leadership', 'courage', 'charisma', 'sensitivity', 'intelligence')
        }),
        ('Previsões', {
            'fields': ('daily_prediction', 'weekly_prediction', 'monthly_prediction')
        }),
        ('Leituras Completas', {
            'fields': ('love_reading', 'career_reading', 'money_reading', 'health_reading',
                      'chinese_astrology', 'tarot_reading', 'numerology_reading',
                      'planets_reading', 'compatibility_reading', 'psychic_reading'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('calculated_at', 'updated_at')
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date')
    list_filter = ('plan', 'status')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Assinatura', {
            'fields': ('plan', 'status', 'start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
