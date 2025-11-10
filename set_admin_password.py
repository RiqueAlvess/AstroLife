import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astrolife.settings')
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    print('Senha do admin definida com sucesso!')
    print('Username: admin')
    print('Password: admin123')
except User.DoesNotExist:
    print('Usuário admin não encontrado')
