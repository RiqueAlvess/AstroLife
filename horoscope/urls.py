from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/passo-1/', views.quiz_step1, name='quiz_step1'),
    path('quiz/passo-2/', views.quiz_step2, name='quiz_step2'),
    path('quiz/passo-3/', views.quiz_step3, name='quiz_step3'),
    path('quiz/passo-4/', views.quiz_step4, name='quiz_step4'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mapa-astral/', views.natal_chart, name='natal_chart'),
    path('previsoes/', views.predictions, name='predictions'),
    path('leituras/', views.readings, name='readings'),
    path('configuracoes/', views.settings, name='settings'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
