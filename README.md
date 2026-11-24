# Senac 2026.2 – Projeto Integrador – Grupo 26
# GestãoFácil

O GestãoFácil é uma aplicação web desenvolvida para simplificar a administração de pequenos negócios. O sistema foca em três pilares principais: gestão de clientes, acompanhamento de pedidos e controle de estoque.

## Instalação e execução local

Os passos abaixo utilizam **Windows/PowerShell**. Requisitos: Python 3.13 (recomendado) ou 3.12 e Git (se for clonar o repositório). Caso prefira, é possível usar **Code → Download ZIP** no GitHub e extrair os arquivos.

1. Clone o repositório principal ou faça download e extraia;
2. Abra o PowerShell na pasta que contém `manage.py`;
3. Crie o ambiente virtual:
```powershell
py -3.13 -m venv .venv
```
Substitua por 3.12, caso essa seja a versão instalada em sua máquina.
4. Instalar dependências:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
5. Verificar a configuração do Django:
``` powershell
.\.venv\Scripts\python.exe manage.py check
```
6. Criar ou atualizar tabelas do banco de dados local:
```powershell
.\.venv\Scripts\python.exe manage.py migrate
```
7. Criar usuário para acessar a aplicação, substituindo `ADMINISTRADOR` por um nome de usuário à escolha.:
```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser --username ADMINISTRADOR
```
Informe o e-mail solicitado (pode ser fictício, já que a aplicação não está conectada a um servidor ainda) e escolha uma senha. A senha não aparece no terminal enquanto é digitada.

O usuário criado poderá acessar a aplicação e o painel administrativo do
Django.

Se a conta já existir naquele banco e seja preciso redefinir a senha, utilize:
``` powershell
.\.venv\Scripts\python.exe manage.py changepassword ADMINISTRADOR
```
8. Iniciar servidor local:
```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/) e entre com as credenciais criadas.

Para parar o servidor, pressione `Ctrl + C` no terminal.

## Funcionalidades

### Autenticação
-   Login e logout de usuários;
-   Proteção das páginas do negócio para usuários autenticados;
-   Contas criadas por comando administrativo do sistema de autenticação nativo do Django;
-   Tela de login amigável, identificação da conta conectada na interface e mensagens de erro.

### Clientes
-   Cadastro, consulta e edição de clientes;
-   Registro de nome, telefone, endereço e observações;
-   Busca por nome ou telefone, com listagem paginada e exibição de cidade/UF;
-   Consulta dos pedidos associados a cada cliente.

### Pedidos
-   Cadastro e edição de pedidos vinculados a clientes;
-   Registro da descrição, quantidade, data de entrega e observações;
-   Busca pela descrição do pedido ou pelo nome do cliente;
-   Acompanhamento do status do pedido:
    -   Pendente;
    -   Em produção;
    -   Finalizado.
-   Consulta do histórico de pedidos de cada cliente.

### Estoque
-   Cadastro de itens nas unidades kg, g, L, mL e unidade;
-   Registro manual de entrada e saída de estoque;
-   Consulta do saldo e do histórico de movimentações;
-   Configuração de estoque mínimo e alerta visual ao atingir um saldo menor igual a esse valor;
-   Validação para impedir saídas superiores ao saldo disponível.

### Painel
-   Visualização do total de clientes, pedidos pendentes, pedidos em produção e itens com estoque baixo;
-   Indicadores calculados a partir do banco de dados;
-   Atalhos para cadastrar clientes e pedidos;
-   Navegação por menu lateral no desktop e menu recolhível em mobile;
-   Mensagens de sucesso, erro e estados vazios padronizadas.

## Tecnologias
- **Python 3.13 ou 3.12:** linguagem e ambiente de execução;
- **Django 5.2.19:** framework web, rotas, autenticação, formulários, templates, ORM e paginação;
- **SQLite:** banco de dados local;
- **HTML:** estrutura e renderização das páginas no servidor;
- **CSS:** estilização da interface, componentes visuais e responsividade;
- **SVG:** ícones sem necessidade de bibliotecas externas;
- **Git:** versionamento e hospedagem do código-fonte.

As dependências Python estão registradas em `requirements.txt`.

**Não é necessário instalar PostgreSQL, MySQL ou outro servidor de banco
de dados.** O projeto utiliza SQLite localmente.

## Estrutura

- `config/`: configura do Django, SQLite, autenticação e rotas principais;
- `gestao/`: Python para gerenciar modelos, formulários, validações, views, consultas, serviço de estoque, migrações e testes;
- `templates/`: páginas HTML com estrutura compartilhada, menus, mensagens, listas, renderização;
- `static/`: CSS organizando estilos, complementos e comportamentos estéticos;
- `.gitignore`: ignora o ambiente virtual, o banco local e outros arquivos temporários;
- `db.sqlite3`: criado localmente em cada computador.

Para conhecer as responsabilidades dos arquivos, o modelo de dados e os fluxos internos, consulte **[ARQUITETURA.md](ARQUITETURA.md)**.

## Autores
Aline Pereira Barbosa

Diogo Américo Gomes Diógenes

Gabriel Ferreira Machado

Guilherme de Souza Medeiros

Hiago Protásio dos Passos Sales

João Gabriel Lopes Trindade

Vinícius Evangelista de Souza
