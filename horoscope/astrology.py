import swisseph as se
import datetime
import pytz
import random


# Configurar Swiss Ephemeris path (usando caminho padrão)
se.set_ephe_path('/usr/share/ephe')


# Lista de signos
SIGNOS = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"
]

# Descrições dos signos
DESCRICAO_SIGNOS = {
    "Áries": "Líder nato, impulsivo e cheio de energia. Gosta de desafios e iniciativa.",
    "Touro": "Calmo, persistente e amante do conforto. Valoriza estabilidade e beleza.",
    "Gêmeos": "Comunicativo, curioso e adaptável. Busca aprender e trocar ideias.",
    "Câncer": "Sensível, protetor e emocional. Valoriza laços afetivos e o lar.",
    "Leão": "Confiante, expressivo e generoso. Gosta de brilhar e inspirar os outros.",
    "Virgem": "Analítico, prático e detalhista. Busca aperfeiçoamento constante.",
    "Libra": "Diplomático, equilibrado e sociável. Gosta de harmonia e estética.",
    "Escorpião": "Intenso, profundo e transformador. Vive tudo com emoção e mistério.",
    "Sagitário": "Aventureiro, otimista e filosófico. Ama a liberdade e o aprendizado.",
    "Capricórnio": "Disciplinado, responsável e ambicioso. Foca em resultados concretos.",
    "Aquário": "Original, idealista e independente. Pensa no coletivo e no futuro.",
    "Peixes": "Empático, sonhador e artístico. Vive guiado pela emoção e intuição."
}

# Tags de personalidade por signo
TAGS_SIGNOS = {
    "Áries": {"Liderança": 95, "Coragem": 90, "Carisma": 70, "Sensibilidade": 40, "Inteligência": 60},
    "Touro": {"Liderança": 60, "Coragem": 65, "Carisma": 55, "Sensibilidade": 80, "Inteligência": 75},
    "Gêmeos": {"Liderança": 70, "Coragem": 65, "Carisma": 90, "Sensibilidade": 60, "Inteligência": 85},
    "Câncer": {"Liderança": 45, "Coragem": 50, "Carisma": 70, "Sensibilidade": 95, "Inteligência": 70},
    "Leão": {"Liderança": 100, "Coragem": 95, "Carisma": 90, "Sensibilidade": 55, "Inteligência": 75},
    "Virgem": {"Liderança": 65, "Coragem": 60, "Carisma": 50, "Sensibilidade": 70, "Inteligência": 95},
    "Libra": {"Liderança": 60, "Coragem": 55, "Carisma": 95, "Sensibilidade": 80, "Inteligência": 85},
    "Escorpião": {"Liderança": 80, "Coragem": 85, "Carisma": 65, "Sensibilidade": 70, "Inteligência": 90},
    "Sagitário": {"Liderança": 85, "Coragem": 90, "Carisma": 80, "Sensibilidade": 60, "Inteligência": 80},
    "Capricórnio": {"Liderança": 90, "Coragem": 80, "Carisma": 55, "Sensibilidade": 50, "Inteligência": 85},
    "Aquário": {"Liderança": 75, "Coragem": 70, "Carisma": 80, "Sensibilidade": 65, "Inteligência": 95},
    "Peixes": {"Liderança": 40, "Coragem": 45, "Carisma": 75, "Sensibilidade": 100, "Inteligência": 70}
}


def calculate_birth_chart(birth_date, birth_time, latitude, longitude, timezone_str='America/Sao_Paulo'):
    """
    Calcula o mapa natal completo

    Args:
        birth_date: datetime.date object
        birth_time: datetime.time object
        latitude: float
        longitude: float
        timezone_str: string com timezone

    Returns:
        dict com todos os dados calculados
    """
    try:
        # Combinar data e hora
        birth_datetime = datetime.datetime.combine(birth_date, birth_time)

        # Converter para UTC
        tz = pytz.timezone(timezone_str)
        data_local = tz.localize(birth_datetime)
        data_ut = data_local.astimezone(pytz.utc)

        # Calcular Julian Day
        jd_ut = se.utc_to_jd(
            int(data_ut.year),
            int(data_ut.month),
            int(data_ut.day),
            int(data_ut.hour),
            int(data_ut.minute),
            int(data_ut.second),
            se.GREG_CAL
        )
        jd = jd_ut[1]

        # Calcular casas e ascendente (usando sistema Placidus)
        cusp, ascmc = se.houses(jd, latitude, longitude, b'P')
        asc_graus = ascmc[0]

        # Posição do Sol e da Lua
        pos_sol = se.calc_ut(jd, se.SUN)[0][0]
        pos_lua = se.calc_ut(jd, se.MOON)[0][0]

        # Determinar signos
        signo_solar = SIGNOS[int(pos_sol // 30)]
        signo_lunar = SIGNOS[int(pos_lua // 30)]
        signo_asc = SIGNOS[int(asc_graus // 30)]

        # Combinar tags de personalidade
        tags = combinar_tags(signo_solar, signo_asc, signo_lunar)

        # Gerar previsões
        daily = gerar_previsao_motivacional(signo_solar, signo_asc, signo_lunar, 'diario')
        weekly = gerar_previsao_motivacional(signo_solar, signo_asc, signo_lunar, 'semanal')
        monthly = gerar_previsao_motivacional(signo_solar, signo_asc, signo_lunar, 'mensal')

        # Gerar leituras completas
        love = gerar_leitura_amor(signo_solar, signo_lunar)
        career = gerar_leitura_carreira(signo_solar, signo_asc)
        money = gerar_leitura_dinheiro(signo_solar, signo_asc)
        health = gerar_leitura_saude(signo_lunar)
        chinese = gerar_astrologia_chinesa(birth_date.year)
        tarot = gerar_leitura_tarot()
        numerology = gerar_numerologia(birth_date)
        planets = gerar_leitura_planetas(signo_solar, signo_lunar, signo_asc)
        compatibility = gerar_compatibilidade(signo_solar)
        psychic = gerar_leitura_psiquica()

        return {
            'sun_sign': signo_solar,
            'moon_sign': signo_lunar,
            'ascendant_sign': signo_asc,
            'sun_position': pos_sol,
            'moon_position': pos_lua,
            'ascendant_position': asc_graus,
            'sun_description': DESCRICAO_SIGNOS[signo_solar],
            'moon_description': DESCRICAO_SIGNOS[signo_lunar],
            'ascendant_description': DESCRICAO_SIGNOS[signo_asc],
            'leadership': tags['Liderança'],
            'courage': tags['Coragem'],
            'charisma': tags['Carisma'],
            'sensitivity': tags['Sensibilidade'],
            'intelligence': tags['Inteligência'],
            'daily_prediction': daily,
            'weekly_prediction': weekly,
            'monthly_prediction': monthly,
            'love_reading': love,
            'career_reading': career,
            'money_reading': money,
            'health_reading': health,
            'chinese_astrology': chinese,
            'tarot_reading': tarot,
            'numerology_reading': numerology,
            'planets_reading': planets,
            'compatibility_reading': compatibility,
            'psychic_reading': psychic,
        }
    except Exception as e:
        print(f"Erro ao calcular mapa natal: {e}")
        return None


def combinar_tags(signo_sol, signo_asc, signo_lua):
    """Combina as tags de personalidade dos três signos principais"""
    tags = {}
    for tag in TAGS_SIGNOS[signo_sol]:
        valor = (TAGS_SIGNOS[signo_sol][tag] * 0.5 +
                 TAGS_SIGNOS[signo_asc][tag] * 0.3 +
                 TAGS_SIGNOS[signo_lua][tag] * 0.2)
        tags[tag] = round(valor, 1)
    return tags


def gerar_previsao_motivacional(signo_sol, signo_asc, signo_lua, periodo):
    """Gera previsões motivacionais"""
    frases = {
        "diario": [
            "Hoje, sua energia interior está alinhada para criar novas oportunidades. Siga sua intuição e não tenha medo de mostrar sua autenticidade.",
            "Pequenos passos feitos com consciência hoje abrirão portas inesperadas. Permita-se sonhar e agir com coragem.",
            "É um dia para ouvir seu coração e explorar atividades que tragam alegria genuína. Inspire e seja inspirado.",
            "Hoje, permita-se sentir profundamente e agir com consciência. Sua sensibilidade é seu guia, e a coragem interior abre caminhos que parecem difíceis.",
            "A energia do dia favorece introspecção e planejamento. Pequenos gestos, decisões pensadas e um toque de intuição farão toda a diferença."
        ],
        "semanal": [
            "Esta semana, os astros sugerem que você se concentre em seus objetivos de longo prazo. Inspire os outros pelo exemplo, não pela palavra.",
            "Momento de reflexão e expansão pessoal. Sua sensibilidade combinada à ação pode gerar conquistas duradouras.",
            "A semana pede atenção às relações e oportunidades que surgem. Confie em sua criatividade e siga seu instinto.",
            "Uma semana de transformações sutis. Preste atenção aos sinais e mantenha-se aberto a novas possibilidades."
        ],
        "mensal": [
            "Neste mês, você alcança um ponto de virada. Projetos e sonhos antigos podem finalmente tomar forma. Confie na sua visão.",
            "O período é propício para crescer emocional e espiritualmente. Reflita, planeje e aja com autenticidade.",
            "É um mês de grandes insights e oportunidades. Siga sua intuição, priorize o que realmente importa e permita-se brilhar.",
            "O mês traz renovação e clareza. Deixe ir o que não serve mais e abrace o novo com coragem e esperança."
        ]
    }
    return random.choice(frases[periodo])


def gerar_leitura_amor(signo_sol, signo_lua):
    """Gera leitura de amor personalizada"""
    leituras = [
        "Suas emoções são intensas e protetoras. Para quem busca amor, abrace vulnerabilidade e sinceridade. Pequenos gestos de afeto falarão mais alto que palavras. Se já estiver em um relacionamento, cuide da comunicação e do equilíbrio entre independência e conexão.",
        "O amor floresce quando você se permite ser autêntico. Sua sensibilidade atrai pessoas que valorizam profundidade emocional. Momentos de intimidade e conversas sinceras fortalecem os laços afetivos.",
        "A paixão está no ar, mas o equilíbrio é essencial. Demonstre seus sentimentos sem perder sua essência. A reciprocidade e o respeito mútuo são a base de relacionamentos duradouros.",
        "Seu coração está aberto para novas experiências. Se busca amor, esteja atento aos sinais sutis. Se já está comprometido, renove votos de carinho e cumplicidade."
    ]
    return random.choice(leituras)


def gerar_leitura_carreira(signo_sol, signo_asc):
    """Gera leitura de carreira personalizada"""
    leituras = [
        "A disciplina e a energia se combinam: hoje é dia de focar em metas concretas e assumir liderança. Projetos antigos podem finalmente ganhar tração se você ousar tomar iniciativa.",
        "Sua capacidade analítica e visão estratégica estão em alta. É momento de apresentar suas ideias e buscar reconhecimento pelo seu trabalho. Confie no seu potencial.",
        "Oportunidades profissionais surgem quando você demonstra confiança e competência. Não tenha medo de assumir responsabilidades e mostrar seu valor.",
        "O trabalho em equipe e a colaboração trazem resultados surpreendentes. Sua habilidade de liderar e inspirar outros será reconhecida."
    ]
    return random.choice(leituras)


def gerar_leitura_dinheiro(signo_sol, signo_asc):
    """Gera leitura de finanças"""
    leituras = [
        "Organização e planejamento serão aliados poderosos. Evite decisões impulsivas; avalie riscos com cuidado e invista em estratégias que tragam estabilidade. Pequenas ações consistentes gerarão frutos duradouros.",
        "Momento favorável para revisar investimentos e buscar novas fontes de renda. Sua criatividade pode se transformar em lucro se você agir com disciplina.",
        "A prudência financeira é essencial agora. Evite gastos desnecessários e foque em construir uma base sólida para o futuro.",
        "Oportunidades financeiras aparecem, mas exigem análise cuidadosa. Confie na sua intuição, mas também faça as contas."
    ]
    return random.choice(leituras)


def gerar_leitura_saude(signo_lua):
    """Gera leitura de saúde"""
    leituras = [
        "Ouça seu corpo e cuide da mente. Momentos de introspecção e relaxamento são essenciais. Atividades físicas leves, meditação ou conexão com a natureza equilibram a sensibilidade emocional e fortalecem sua energia vital.",
        "Sua saúde está conectada ao seu estado emocional. Pratique autocuidado e reserve tempo para atividades que tragam paz interior.",
        "O equilíbrio entre corpo e mente é fundamental. Exercícios regulares, alimentação saudável e momentos de lazer contribuem para seu bem-estar.",
        "Preste atenção aos sinais do corpo. Descanso adequado e hidratação são essenciais para manter sua vitalidade."
    ]
    return random.choice(leituras)


def gerar_astrologia_chinesa(ano_nascimento):
    """Gera leitura da astrologia chinesa baseada no ano"""
    animais = ["Rato", "Boi", "Tigre", "Coelho", "Dragão", "Serpente",
               "Cavalo", "Cabra", "Macaco", "Galo", "Cão", "Porco"]

    # Cálculo simplificado (1900 = Rato)
    indice = (ano_nascimento - 1900) % 12
    animal = animais[indice]

    descricoes = {
        "Rato": "Inteligente e adaptável, você possui grande capacidade de superar desafios com criatividade.",
        "Boi": "Trabalhador e persistente, sua dedicação é sua maior força.",
        "Tigre": "Corajoso e competitivo, você enfrenta desafios de frente com determinação.",
        "Coelho": "Gentil e diplomático, você valoriza harmonia e relacionamentos.",
        "Dragão": "Poderoso e carismático, você nasceu para liderar e inspirar.",
        "Serpente": "Sábio e intuitivo, você enxerga além das aparências.",
        "Cavalo": "Livre e energético, você busca aventuras e novos horizontes.",
        "Cabra": "Criativo e sensível, você valoriza beleza e expressão artística.",
        "Macaco": "Inteligente e versátil, você se adapta facilmente a novas situações.",
        "Galo": "Confiante e organizado, você gosta de ordem e eficiência.",
        "Cão": "Leal e honesto, você valoriza amizades verdadeiras e justiça.",
        "Porco": "Generoso e sincero, você busca o bem-estar de todos ao seu redor."
    }

    return f"Seu signo chinês é {animal}. {descricoes[animal]} O ano presente reforça a importância da disciplina e da ambição. Aproveite para criar estruturas sólidas em sua vida pessoal e profissional, mas sem perder a leveza do seu coração."


def gerar_leitura_tarot():
    """Gera leitura de tarot"""
    cartas = [
        ("O Sol", "iluminação, clareza e vitalidade. Momentos de alegria e realização estão ao seu alcance, mas a ação consciente é necessária para transformar oportunidades em conquistas."),
        ("A Estrela", "esperança, inspiração e renovação. Confie no universo e permita que sua luz interior guie seu caminho."),
        ("A Lua", "intuição, mistérios e emoções profundas. Preste atenção aos seus sonhos e mensagens do inconsciente."),
        ("O Mago", "manifestação, poder pessoal e criatividade. Você tem todas as ferramentas necessárias para criar a realidade que deseja."),
        ("A Imperatriz", "abundância, criatividade e nutrição. É tempo de cultivar seus projetos e relacionamentos com amor e dedicação."),
        ("O Carro", "determinação, foco e vitória. Mantenha o controle e siga em frente com confiança."),
    ]
    carta, significado = random.choice(cartas)
    return f"A carta que guia você hoje é {carta}: {significado}"


def gerar_numerologia(birth_date):
    """Gera leitura numerológica baseada na data de nascimento"""
    # Soma todos os dígitos da data até reduzir a um número
    soma = sum(int(d) for d in str(birth_date.day) + str(birth_date.month) + str(birth_date.year))
    while soma > 9:
        soma = sum(int(d) for d in str(soma))

    significados = {
        1: "liderança, independência e inovação. Você é pioneiro e tem coragem para iniciar novos projetos.",
        2: "cooperação, diplomacia e equilíbrio. Você é mediador natural e valoriza harmonia.",
        3: "criatividade, expressão e otimismo. Você tem talento para comunicação e arte.",
        4: "estabilidade, organização e trabalho duro. Você constrói bases sólidas para o futuro.",
        5: "liberdade, aventura e versatilidade. Você busca experiências variadas e mudanças.",
        6: "responsabilidade, família e serviço. Você é cuidador natural e valoriza relacionamentos.",
        7: "introspecção, sabedoria e autoconhecimento. Reflita sobre seus objetivos, confie na intuição e permita que insights profundos guiem suas decisões.",
        8: "poder, ambição e sucesso material. Você tem capacidade para grandes realizações.",
        9: "humanitarismo, compaixão e finalização. Você busca fazer diferença no mundo."
    }

    return f"O número do seu dia é {soma} – {significados[soma]}"


def gerar_leitura_planetas(signo_sol, signo_lua, signo_asc):
    """Gera leitura de influências planetárias"""
    return f"A influência da Lua em {signo_lua} sugere disciplina e foco emocional, enquanto o Sol em {signo_sol} reforça sua essência e propósito de vida. O Ascendente em {signo_asc} impulsiona sua forma de se apresentar ao mundo. Harmonize emoção, identidade e ação para avançar com segurança."


def gerar_compatibilidade(signo_sol):
    """Gera leitura de compatibilidade amorosa"""
    compatibilidades = {
        "Áries": "Sua combinação com signos de Ar (Gêmeos, Libra, Aquário) traz leveza e comunicação. Signos de Fogo (Leão, Sagitário) compartilham sua paixão e energia.",
        "Touro": "Sua combinação com signos de Terra (Virgem, Capricórnio) traz estabilidade. Signos de Água (Câncer, Escorpião, Peixes) oferecem profundidade emocional.",
        "Gêmeos": "Sua combinação com signos de Ar (Libra, Aquário) estimula troca intelectual. Signos de Fogo (Áries, Leão, Sagitário) trazem entusiasmo.",
        "Câncer": "Sua combinação com signos de Terra (Touro, Virgem, Capricórnio) traz estabilidade e segurança. Signos de Água (Escorpião, Peixes) compartilham sensibilidade emocional.",
        "Leão": "Sua combinação com signos de Fogo (Áries, Sagitário) amplifica paixão e criatividade. Signos de Ar (Gêmeos, Libra, Aquário) admiram seu brilho.",
        "Virgem": "Sua combinação com signos de Terra (Touro, Capricórnio) valoriza praticidade. Signos de Água (Câncer, Escorpião, Peixes) trazem profundidade.",
        "Libra": "Sua combinação com signos de Ar (Gêmeos, Aquário) estimula harmonia intelectual. Signos de Fogo (Leão, Sagitário) trazem paixão equilibrada.",
        "Escorpião": "Sua combinação com signos de Água (Câncer, Peixes) oferece intimidade profunda. Signos de Terra (Touro, Virgem, Capricórnio) trazem estabilidade.",
        "Sagitário": "Sua combinação com signos de Fogo (Áries, Leão) compartilha aventura e otimismo. Signos de Ar (Gêmeos, Libra, Aquário) estimulam expansão.",
        "Capricórnio": "Sua combinação com signos de Terra (Touro, Virgem) valoriza construção sólida. Signos de Água (Câncer, Escorpião, Peixes) suavizam rigidez.",
        "Aquário": "Sua combinação com signos de Ar (Gêmeos, Libra) estimula inovação. Signos de Fogo (Áries, Leão, Sagitário) compartilham visão futurista.",
        "Peixes": "Sua combinação com signos de Água (Câncer, Escorpião) oferece conexão emocional profunda. Signos de Terra (Touro, Virgem, Capricórnio) trazem ancoragem."
    }
    return compatibilidades.get(signo_sol, "Você possui compatibilidade única com diversos signos.")


def gerar_leitura_psiquica():
    """Gera leitura psíquica simbólica"""
    leituras = [
        "Hoje, concentre-se em sua intuição. Respostas que procura não estão no mundo externo, mas na conexão entre coração e mente. Pequenas decisões de hoje podem gerar grandes mudanças futuras.",
        "Uma energia de transformação está ao seu redor. Preste atenção aos sinais sutis e confie no processo. O universo conspira a seu favor.",
        "Sua sensibilidade está aguçada. Use-a para compreender situações e pessoas ao seu redor. A verdade se revela através da intuição.",
        "Momento de conexão com seu eu superior. Meditação, reflexão e silêncio trazem clareza e orientação para o caminho à frente."
    ]
    return random.choice(leituras)
