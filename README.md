# 🌟 AstroLife - Sistema de Horóscopo Completo

Sistema Django completo de horóscopo e mapa astral com interface moderna, tema cósmico e mobile-first.

## ✨ Funcionalidades

- 🎯 **Quiz Interativo**: Fluxo de 4 etapas para coleta de dados astrológicos
- 🌌 **Mapa Astral Completo**: Cálculo preciso usando Swiss Ephemeris
- 💫 **Leituras Personalizadas**: Amor, carreira, dinheiro, saúde e muito mais
- 🔮 **Previsões**: Diárias, semanais e mensais
- 📊 **Perfil de Personalidade**: Análise de traços baseados nos signos
- 🐉 **Astrologia Chinesa**: Integração com signos chineses
- 🃏 **Tarot e Numerologia**: Leituras complementares
- 💰 **Sistema de Assinaturas**: Múltiplos planos
- 🎨 **Design Cósmico**: Interface moderna com Tailwind CSS

## 🚀 Tecnologias

- **Backend**: Django 5.x + Python 3.11
- **Frontend**: HTML5 + Tailwind CSS (via CDN)
- **Banco de Dados**: SQLite
- **Cálculos Astrológicos**: PySwisseph
- **Timezones**: PyTZ

## 📦 Instalação

### Requisitos

- Python 3.11 ou superior
- pip

### Passo a Passo

1. Clone o repositório:
```bash
git clone <repository-url>
cd AstroLife
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute as migrações:
```bash
python manage.py migrate
```

4. Crie um superusuário (opcional):
```bash
python manage.py createsuperuser
```

Ou use as credenciais pré-configuradas:
- **Username**: admin
- **Password**: admin123

5. Inicie o servidor:
```bash
python manage.py runserver
```

6. Acesse o aplicativo:
- **Site**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

## 🎯 Fluxo do Usuário

### 1. Landing Page
- Apresentação do serviço
- Features e benefícios
- Call-to-action

### 2. Quiz - Passo 1: Dados Astrológicos
- Sexo
- Data de nascimento
- Hora de nascimento (opcional)
- Cidade de nascimento (20 cidades brasileiras)

### 3. Quiz - Passo 2: Perfil Emocional
- Como você está se sentindo?
- O que você deseja alcançar?
- Feedback personalizado baseado no signo solar

### 4. Quiz - Passo 3: Criar Conta
- Nome de usuário
- Email
- Senha
- Validação em tempo real

### 5. Quiz - Passo 4: Escolha de Plano
- Gratuito (básico)
- Mensal: R$ 19,99
- Semestral: R$ 13,99/mês
- Anual: R$ 11,99/mês (melhor oferta)

### 6. Dashboard
Acesso completo ao mapa astral com:
- Sol, Lua e Ascendente
- Perfil de personalidade (5 traços)
- Previsões (diárias, semanais, mensais)
- Leituras de: Amor, Carreira, Dinheiro, Saúde
- Astrologia Chinesa
- Tarot e Numerologia
- Compatibilidade amorosa
- Leitura psíquica

## 🔧 Estrutura do Projeto

```
AstroLife/
├── astrolife/              # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── horoscope/              # App principal
│   ├── models.py           # UserProfile, BirthChart, Subscription
│   ├── views.py            # Views do quiz e dashboard
│   ├── urls.py             # Rotas
│   ├── admin.py            # Admin customizado
│   ├── astrology.py        # Lógica de cálculo astrológico
│   └── templates/
│       └── horoscope/
│           ├── base.html
│           ├── index.html
│           ├── quiz_step1.html
│           ├── quiz_step2.html
│           ├── quiz_step3.html
│           ├── quiz_step4.html
│           ├── dashboard.html
│           └── login.html
├── manage.py
├── requirements.txt
└── README.md
```

## 🎨 Design

### Tema Cósmico
- Gradientes: Roxo, azul e rosa
- Background: Animação de estrelas
- Glass morphism nos cards
- Animações suaves
- Mobile-first responsive

### Cores Principais
- `#667eea` - Roxo principal
- `#764ba2` - Roxo escuro
- `#f093fb` - Rosa claro
- Background gradiente: `#0a0e27` → `#1a1042` → `#2d1b69`

## 📊 Models

### UserProfile
- Dados pessoais e astrológicos
- Local de nascimento (lat/lng/timezone)
- Perfil emocional
- Status do quiz

### BirthChart
- Signos (Sol, Lua, Ascendente)
- Posições planetárias
- Traços de personalidade
- Todas as leituras completas

### Subscription
- Planos de assinatura
- Status (ativo/expirado/cancelado)
- Datas de início e fim

## 🔐 Autenticação

Sistema completo de autenticação Django:
- Registro de usuário no quiz
- Login/Logout
- Proteção de rotas com `@login_required`
- Sessões para dados temporários do quiz

## 🌍 Cidades Suportadas

20 principais cidades brasileiras com coordenadas e timezones:
- São Paulo, Rio de Janeiro, Brasília, Salvador
- Fortaleza, Belo Horizonte, Manaus, Curitiba
- Recife, Porto Alegre, Goiânia, Belém
- E mais...

## 🔮 Cálculos Astrológicos

Utilizando **PySwisseph** (Swiss Ephemeris):
- Cálculo preciso de posições planetárias
- Sistema de casas Placidus
- Conversão de timezones
- Julian Day calculations

### Signos Implementados
Todos os 12 signos com:
- Descrições detalhadas
- Tags de personalidade (Liderança, Coragem, Carisma, Sensibilidade, Inteligência)
- Compatibilidades

### Leituras Geradas
- **Previsões**: Aleatórias mas contextualmente relevantes
- **Amor**: Baseado em Sol + Lua
- **Carreira**: Baseado em Sol + Ascendente
- **Dinheiro**: Planejamento e finanças
- **Saúde**: Bem-estar físico e mental
- **Astrologia Chinesa**: Baseada no ano de nascimento
- **Tarot**: Cartas simbólicas
- **Numerologia**: Baseada na data de nascimento
- **Planetas**: Influências planetárias
- **Compatibilidade**: Por elemento
- **Leitura Psíquica**: Mensagens simbólicas

## 🛠️ Personalização

### Adicionar Novas Cidades
Edite `horoscope/views.py` e adicione ao dicionário `CIDADES_BRASIL`:

```python
"Cidade, UF": {
    "lat": -00.0000,
    "lng": -00.0000,
    "tz": "America/Timezone"
}
```

### Modificar Leituras
Edite `horoscope/astrology.py` e ajuste as funções:
- `gerar_previsao_motivacional()`
- `gerar_leitura_amor()`
- `gerar_leitura_carreira()`
- E outras...

## 🐛 Troubleshooting

### Erro ao calcular mapa astral
- Verifique se o PySwisseph está instalado corretamente
- Confirme que as coordenadas estão corretas
- Verifique o timezone

### Templates não encontrados
- Confirme que o app está em `INSTALLED_APPS`
- Verifique a estrutura de diretórios em `templates/`

### Erro de CSRF
- Certifique-se de incluir `{% csrf_token %}` em todos os formulários

## 📝 Admin Django

Acesse `/admin` para gerenciar:
- Usuários e perfis
- Mapas astrais
- Assinaturas

## 🚀 Próximos Passos

Melhorias possíveis:
- Integração com API de geolocalização
- Envio de emails com previsões diárias
- Sistema de pagamento real (Stripe, Mercado Pago)
- Compartilhamento em redes sociais
- Comparação de compatibilidade entre usuários
- Gráfico visual do mapa astral
- Exportação em PDF
- App mobile (React Native / Flutter)

## 📄 Licença

Este projeto é livre para uso educacional e pessoal.

## 👨‍💻 Autor

Desenvolvido com ❤️ e ✨

---

**Nota**: Este é um projeto de demonstração. Para uso em produção, implemente:
- Variáveis de ambiente para SECRET_KEY
- Banco de dados PostgreSQL
- Sistema de cache (Redis)
- CDN para arquivos estáticos
- HTTPS
- Sistema de backup
- Monitoramento e logs
