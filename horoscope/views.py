from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from .models import UserProfile, BirthChart, Subscription
from .astrology import calculate_birth_chart
from datetime import datetime, time
import pytz


# Dicionário com principais cidades brasileiras e suas coordenadas
CIDADES_BRASIL = {
    "São Paulo, SP": {"lat": -23.5505, "lng": -46.6333, "tz": "America/Sao_Paulo"},
    "Rio de Janeiro, RJ": {"lat": -22.9068, "lng": -43.1729, "tz": "America/Sao_Paulo"},
    "Brasília, DF": {"lat": -15.8267, "lng": -47.9218, "tz": "America/Sao_Paulo"},
    "Salvador, BA": {"lat": -12.9714, "lng": -38.5014, "tz": "America/Bahia"},
    "Fortaleza, CE": {"lat": -3.7327, "lng": -38.5270, "tz": "America/Fortaleza"},
    "Belo Horizonte, MG": {"lat": -19.9167, "lng": -43.9345, "tz": "America/Sao_Paulo"},
    "Manaus, AM": {"lat": -3.1190, "lng": -60.0217, "tz": "America/Manaus"},
    "Curitiba, PR": {"lat": -25.4284, "lng": -49.2733, "tz": "America/Sao_Paulo"},
    "Recife, PE": {"lat": -8.0476, "lng": -34.8770, "tz": "America/Recife"},
    "Porto Alegre, RS": {"lat": -30.0346, "lng": -51.2177, "tz": "America/Sao_Paulo"},
    "Goiânia, GO": {"lat": -16.6869, "lng": -49.2648, "tz": "America/Sao_Paulo"},
    "Belém, PA": {"lat": -1.4558, "lng": -48.5039, "tz": "America/Belem"},
    "Guarulhos, SP": {"lat": -23.4538, "lng": -46.5333, "tz": "America/Sao_Paulo"},
    "Campinas, SP": {"lat": -22.9099, "lng": -47.0626, "tz": "America/Sao_Paulo"},
    "São Luís, MA": {"lat": -2.5387, "lng": -44.2825, "tz": "America/Fortaleza"},
    "São Gonçalo, RJ": {"lat": -22.8268, "lng": -43.0534, "tz": "America/Sao_Paulo"},
    "Maceió, AL": {"lat": -9.6662, "lng": -35.7350, "tz": "America/Maceio"},
    "Duque de Caxias, RJ": {"lat": -22.7858, "lng": -43.3054, "tz": "America/Sao_Paulo"},
    "Natal, RN": {"lat": -5.7945, "lng": -35.2110, "tz": "America/Fortaleza"},
    "Teresina, PI": {"lat": -5.0892, "lng": -42.8016, "tz": "America/Fortaleza"},
}


def index(request):
    """Página inicial - landing page"""
    # Redirecionar usuários logados para o dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'horoscope/index.html')


def quiz_step1(request):
    """Etapa 1: Coleta de dados astrológicos"""
    # Redirecionar usuários logados para o dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        # Armazenar dados na sessão
        request.session['gender'] = request.POST.get('gender')
        request.session['birth_date'] = request.POST.get('birth_date')
        request.session['birth_time'] = request.POST.get('birth_time')
        request.session['birth_city'] = request.POST.get('birth_city')

        # Obter coordenadas da cidade
        city_data = CIDADES_BRASIL.get(request.POST.get('birth_city'))
        if city_data:
            request.session['birth_latitude'] = city_data['lat']
            request.session['birth_longitude'] = city_data['lng']
            request.session['birth_timezone'] = city_data['tz']

        return redirect('quiz_step2')

    context = {'cidades': CIDADES_BRASIL.keys()}
    return render(request, 'horoscope/quiz_step1.html', context)


def quiz_step2(request):
    """Etapa 2: Perfil emocional e objetivos"""
    # Redirecionar usuários logados para o dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Validar que o passo 1 foi completado
    if 'birth_date' not in request.session:
        messages.error(request, 'Por favor, complete o passo 1 primeiro.')
        return redirect('quiz_step1')

    if request.method == 'POST':
        request.session['feeling'] = request.POST.get('feeling')
        request.session['objective'] = request.POST.get('objective')
        return redirect('quiz_step3')

    # Feedback personalizado baseado nos dados da etapa 1
    feedback = None
    if 'birth_date' in request.session:
        birth_date_str = request.session.get('birth_date')
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        # Calcular signo solar simples
        month = birth_date.month
        day = birth_date.day

        # Lógica simplificada de signos
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            feedback = "Interessante… sua energia está muito alinhada com Áries, um signo de fogo cheio de paixão e coragem!"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            feedback = "Vejo que você é de Touro… sua estabilidade e determinação são forças poderosas!"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            feedback = "Câncer… sua sensibilidade e intuição são dons especiais que guiam seu caminho!"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            feedback = "Leão… seu brilho natural e carisma são impossíveis de ignorar!"
        # ... outros signos podem ser adicionados

    context = {'feedback': feedback}
    return render(request, 'horoscope/quiz_step2.html', context)


def quiz_step3(request):
    """Etapa 3: Registro de usuário"""
    # Redirecionar usuários logados para o dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Validar que os passos anteriores foram completados
    if 'birth_date' not in request.session or 'feeling' not in request.session:
        messages.error(request, 'Por favor, complete os passos anteriores primeiro.')
        return redirect('quiz_step1')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Validações
        if password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'horoscope/quiz_step3.html')

        if len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return render(request, 'horoscope/quiz_step3.html')

        try:
            # Criar usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Salvar dados do perfil
            profile = user.profile
            profile.gender = request.session.get('gender')
            profile.birth_date = datetime.strptime(
                request.session.get('birth_date'), '%Y-%m-%d'
            ).date()

            birth_time_str = request.session.get('birth_time')
            if birth_time_str:
                profile.birth_time = datetime.strptime(birth_time_str, '%H:%M').time()
            else:
                profile.birth_time = time(12, 0)  # Meio-dia como padrão

            profile.birth_city = request.session.get('birth_city')
            profile.birth_latitude = request.session.get('birth_latitude')
            profile.birth_longitude = request.session.get('birth_longitude')
            profile.birth_timezone = request.session.get('birth_timezone', 'America/Sao_Paulo')
            profile.current_feeling = request.session.get('feeling')
            profile.current_objective = request.session.get('objective')
            profile.save()

            # Login automático
            login(request, user)

            return redirect('quiz_step4')

        except IntegrityError:
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'horoscope/quiz_step3.html')

    return render(request, 'horoscope/quiz_step3.html')


@login_required
def quiz_step4(request):
    """Etapa 4: Escolha de plano de assinatura"""
    # Verificar se o usuário já completou o quiz
    if hasattr(request.user, 'profile') and request.user.profile.quiz_completed:
        messages.info(request, 'Você já completou o quiz.')
        return redirect('dashboard')

    # Validar que os passos anteriores foram completados
    if 'birth_date' not in request.session or 'feeling' not in request.session:
        messages.error(request, 'Por favor, complete o quiz desde o início.')
        return redirect('quiz_step1')

    if request.method == 'POST':
        plan = request.POST.get('plan')
        subscription = request.user.subscription
        subscription.plan = plan
        subscription.save()

        # Calcular mapa natal
        calculate_user_birth_chart(request.user)

        # Marcar quiz como completo
        profile = request.user.profile
        profile.quiz_completed = True
        profile.save()

        # Limpar sessão
        for key in ['gender', 'birth_date', 'birth_time', 'birth_city',
                    'birth_latitude', 'birth_longitude', 'birth_timezone',
                    'feeling', 'objective']:
            if key in request.session:
                del request.session[key]

        messages.success(request, 'Bem-vindo ao AstroLife! Seu mapa astral está pronto!')
        return redirect('dashboard')

    plans = [
        {'value': 'monthly', 'name': 'Mensal', 'price': 'R$ 19,99/mês', 'total': 'R$ 19,99'},
        {'value': 'semester', 'name': 'Semestral', 'price': 'R$ 13,99/mês', 'total': 'R$ 83,94 (6 meses)'},
        {'value': 'annual', 'name': 'Anual', 'price': 'R$ 11,99/mês', 'total': 'R$ 143,88 (12 meses)', 'badge': 'Melhor Oferta'},
        {'value': 'free', 'name': 'Gratuito', 'price': 'R$ 0,00', 'total': 'Acesso básico'},
    ]

    context = {'plans': plans}
    return render(request, 'horoscope/quiz_step4.html', context)


@login_required
def dashboard(request):
    """Dashboard principal - redireciona para perfil"""
    return redirect('dashboard_profile')


@login_required
def dashboard_profile(request):
    """Dashboard - Perfil e Personalidade (Mapa Astral)"""
    try:
        birth_chart = request.user.birth_chart
    except BirthChart.DoesNotExist:
        # Se não existe, calcular agora
        calculate_user_birth_chart(request.user)
        birth_chart = request.user.birth_chart

    profile = request.user.profile
    subscription = request.user.subscription

    context = {
        'profile': profile,
        'birth_chart': birth_chart,
        'subscription': subscription,
        'active_tab': 'profile',
    }

    return render(request, 'horoscope/dashboard_profile.html', context)


@login_required
def dashboard_predictions(request):
    """Dashboard - Previsões e Leituras"""
    try:
        birth_chart = request.user.birth_chart
    except BirthChart.DoesNotExist:
        calculate_user_birth_chart(request.user)
        birth_chart = request.user.birth_chart

    profile = request.user.profile
    subscription = request.user.subscription

    context = {
        'profile': profile,
        'birth_chart': birth_chart,
        'subscription': subscription,
        'active_tab': 'predictions',
    }

    return render(request, 'horoscope/dashboard_predictions.html', context)


@login_required
def billing(request):
    """Página de gerenciamento de plano e billing"""
    subscription = request.user.subscription
    profile = request.user.profile

    if request.method == 'POST':
        new_plan = request.POST.get('plan')
        if new_plan in ['free', 'monthly', 'semester', 'annual']:
            subscription.plan = new_plan
            subscription.status = 'active'
            subscription.save()
            messages.success(request, f'Plano alterado para {subscription.get_plan_display()} com sucesso!')
            return redirect('billing')

    plans = [
        {
            'value': 'free',
            'name': 'Gratuito',
            'price': 'R$ 0,00',
            'description': 'Acesso básico ao mapa astral',
            'features': [
                'Mapa astral básico',
                'Signos principais (Sol, Lua, Ascendente)',
                'Previsão diária',
            ]
        },
        {
            'value': 'monthly',
            'name': 'Mensal',
            'price': 'R$ 19,99/mês',
            'description': 'Acesso completo mensal',
            'features': [
                'Tudo do plano gratuito',
                'Previsões semanais e mensais',
                'Leituras completas (amor, carreira, etc)',
                'Atualizações diárias personalizadas',
                'Suporte prioritário',
            ]
        },
        {
            'value': 'semester',
            'name': 'Semestral',
            'price': 'R$ 13,99/mês',
            'total': 'R$ 83,94 cobrados semestralmente',
            'description': 'Economize 30% no plano semestral',
            'badge': 'Economia',
            'features': [
                'Tudo do plano mensal',
                '30% de desconto',
                'Relatórios mensais detalhados',
                'Acesso antecipado a novos recursos',
            ]
        },
        {
            'value': 'annual',
            'name': 'Anual',
            'price': 'R$ 11,99/mês',
            'total': 'R$ 143,88 cobrados anualmente',
            'description': 'Melhor custo-benefício',
            'badge': 'Melhor Oferta',
            'features': [
                'Tudo do plano semestral',
                '40% de desconto',
                'Consultoria astrológica mensal',
                'Relatórios anuais completos',
                'Acesso VIP a eventos exclusivos',
            ]
        },
    ]

    context = {
        'subscription': subscription,
        'profile': profile,
        'plans': plans,
        'current_plan': subscription.plan,
    }

    return render(request, 'horoscope/billing.html', context)


def calculate_user_birth_chart(user):
    """Calcula e salva o mapa natal do usuário"""
    profile = user.profile

    if not profile.birth_date or not profile.birth_time:
        return None

    # Calcular mapa natal
    chart_data = calculate_birth_chart(
        birth_date=profile.birth_date,
        birth_time=profile.birth_time,
        latitude=profile.birth_latitude,
        longitude=profile.birth_longitude,
        timezone_str=profile.birth_timezone
    )

    if chart_data:
        # Criar ou atualizar BirthChart
        birth_chart, created = BirthChart.objects.get_or_create(user=user)

        birth_chart.sun_sign = chart_data['sun_sign']
        birth_chart.moon_sign = chart_data['moon_sign']
        birth_chart.ascendant_sign = chart_data['ascendant_sign']
        birth_chart.sun_position = chart_data['sun_position']
        birth_chart.moon_position = chart_data['moon_position']
        birth_chart.ascendant_position = chart_data['ascendant_position']
        birth_chart.sun_description = chart_data['sun_description']
        birth_chart.moon_description = chart_data['moon_description']
        birth_chart.ascendant_description = chart_data['ascendant_description']
        birth_chart.leadership = chart_data['leadership']
        birth_chart.courage = chart_data['courage']
        birth_chart.charisma = chart_data['charisma']
        birth_chart.sensitivity = chart_data['sensitivity']
        birth_chart.intelligence = chart_data['intelligence']
        birth_chart.daily_prediction = chart_data['daily_prediction']
        birth_chart.weekly_prediction = chart_data['weekly_prediction']
        birth_chart.monthly_prediction = chart_data['monthly_prediction']
        birth_chart.love_reading = chart_data['love_reading']
        birth_chart.career_reading = chart_data['career_reading']
        birth_chart.money_reading = chart_data['money_reading']
        birth_chart.health_reading = chart_data['health_reading']
        birth_chart.chinese_astrology = chart_data['chinese_astrology']
        birth_chart.tarot_reading = chart_data['tarot_reading']
        birth_chart.numerology_reading = chart_data['numerology_reading']
        birth_chart.planets_reading = chart_data['planets_reading']
        birth_chart.compatibility_reading = chart_data['compatibility_reading']
        birth_chart.psychic_reading = chart_data['psychic_reading']

        birth_chart.save()
        return birth_chart

    return None


def user_login(request):
    """View de login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'horoscope/login.html')


def user_logout(request):
    """View de logout"""
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('index')
