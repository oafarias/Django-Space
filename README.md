# 🌌 Alura Space

Plataforma de galeria de fotografias astronômicas desenvolvida com Django. Permite que usuários autenticados explorem imagens do espaço organizadas por categorias como Nebulosa, Estrela, Galáxia e Planeta.

## 🚀 Funcionalidades

- Cadastro e autenticação de usuários
- Galeria de fotografias publicadas
- Busca por nome de fotografia
- Visualização detalhada de cada imagem
- Painel administrativo para gerenciar publicações

## 🛠️ Tecnologias

- [Python 3](https://www.python.org/)
- [Django 4.1](https://www.djangoproject.com/)
- [Pillow](https://python-pillow.org/) – processamento de imagens
- [python-dotenv](https://github.com/theskumar/python-dotenv) – variáveis de ambiente
- SQLite (banco de dados padrão para desenvolvimento)

## ⚙️ Configuração e instalação

### 1. Clone o repositório

```bash
git clone https://github.com/oafarias/Django-Space.git
cd Django-Space
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` e preencha:

| Variável        | Descrição                                              | Exemplo                  |
|-----------------|--------------------------------------------------------|--------------------------|
| `SECRET_KEY`    | Chave secreta do Django (única e aleatória)            | `django-insecure-...`    |
| `DEBUG`         | Ativar modo debug (`True` para dev, `False` para prod) | `True`                   |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por vírgula                | `localhost,127.0.0.1`    |

Para gerar uma `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Crie um superusuário (opcional, para acessar o admin)

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse em: [http://localhost:8000](http://localhost:8000)

O painel administrativo está disponível em: [http://localhost:8000/admin](http://localhost:8000/admin)

## 🧪 Testes

Para executar os testes automatizados:

```bash
python manage.py test galeria usuarios
```

## 📁 Estrutura do projeto

```
Django-Space/
├── galeria/          # App de galeria de fotografias
│   ├── models.py     # Modelo Fotografia
│   ├── views.py      # Views: index, imagem, buscar
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── usuarios/         # App de autenticação
│   ├── forms.py      # LoginForms, CadastroForms
│   ├── views.py      # Views: login, cadastro, logout
│   ├── urls.py
│   └── tests.py
├── setup/            # Configuração do projeto Django
│   ├── settings.py
│   └── urls.py
├── templates/        # Templates HTML
├── static/           # Arquivos estáticos (CSS, JS, imagens)
├── .env.example      # Modelo de variáveis de ambiente
├── manage.py
└── requirements.txt
```

## 🔐 Segurança

- Todas as rotas da galeria requerem autenticação
- As senhas são armazenadas com hash pelo Django
- A `SECRET_KEY` é carregada via variável de ambiente (nunca commite o arquivo `.env`)
- Em produção, defina `DEBUG=False` e configure `ALLOWED_HOSTS` corretamente
