# GestãoFácil

## Executar no Windows

Abra o PowerShell na pasta que contém `manage.py`. Instale Python 3.13 antes de executar.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser --username demo
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/), digite `demo` e use a senha escolhida durante a criação do usuário. Em uma instalação que já tem o usuário, pule a linha `createsuperuser`.

## Executar no macOS ou Linux

Com Python 3.13 instalado, execute os mesmos comandos usando `python3.13 -m venv .venv` na primeira linha e `./.venv/bin/python` no início das demais. O projeto também funciona com Python 3.12.

## Testar

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

## Estrutura

- `config/` configura Django, SQLite, autenticação e rotas.
- `gestao/` contém modelos, formulários, telas, serviço de estoque, migrações e testes.
- `templates/` contém as páginas HTML.
- `static/` contém o CSS.
- `db.sqlite3` é criado em cada computador. O Git ignora o banco e a pasta do ambiente virtual.
