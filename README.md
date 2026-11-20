# Senac 2026.2 – Projeto Integrador – Grupo 26
# GestãoFácil
O GestãoFácil é uma aplicação web desenvolvida para simplificar a administração de pequenos negócios. O sistema foca em três pilares principais: gestão de carteira de clientes, acompanhamento de pedidos e monitoramento inteligente de estoque com alertas automáticos de escassez.

## Funcionalidades
### Autenticação
-   Login e logout de usuários.
-   Proteção das páginas de negócio para usuários autenticados.
-   Utilização do sistema de autenticação nativo do Django.

### Clientes
-   Cadastro e edição de clientes.
-   Consulta da lista e dos detalhes de cada cliente.
-   Registro de telefone e observações.
-   Consulta dos pedidos associados a cada cliente.

### Pedidos
-   Cadastro e edição de pedidos vinculados a clientes.
-   Registro da descrição, quantidade, data de entrega e observações.
-   Consulta de pedidos e de seus detalhes.
-   Acompanhamento do status do pedido:
    -   **Pendente**;
    -   **Em produção**;
    -   **Finalizado**.
-   Consulta do histórico de pedidos de cada cliente.

O sistema apresenta o status atual de cada pedido e permite avançar
pelas etapas previstas. O histórico do cliente reúne seus pedidos; ele
não representa uma linha do tempo de todas as alterações de status.

### Estoque
-   Cadastro de itens de estoque.
-   Utilização das unidades kg, g, L, mL e unidade.
-   Registro manual de entradas e saídas.
-   Consulta do saldo e do histórico de movimentações.
-   Configuração de estoque mínimo.
-   Exibição de alerta quando o saldo atinge ou fica abaixo do estoque
    mínimo.
-   Validação para impedir saídas superiores ao saldo disponível.

### Painel
-   Visualização de pedidos ainda não finalizados.
-   Identificação de itens que precisam de reposição.

## Tecnologias

-----------------------------------------------------------------------
  - **Python 3.13 ou 3.12:** linguagem e ambiente de execução.
  - **Django 5.2.19:** framework web, rotas, autenticação, formulários e ORM.
  - **SQLite:** bbanco de dados local.
  - **HTML:** estrutura das páginas.
  - **CSS:** estilização da interface.
  - **Git:** versionamento e hospedagem do código-fonte.
  -----------------------------------------------------------------------

As dependências Python estão registradas em `requirements.txt`.

**Não é necessário instalar PostgreSQL, MySQL ou outro servidor de banco
de dados.** O projeto utiliza SQLite localmente.

Para mais informações, consulte `ARQUITETURA.md`.

## Instalação e execução local
1. Clone ou extraia o repositório principal;
2. Abra o PowerShell na pasta que contém `manage.py`;
3. Instale Python 3.13 (recomendado) ou 3.12 antes de executar.
4. Crie o ambiente virtual:
```powershell
py -3.13 -m venv .venv
```
Substitua por 3.12, caso essa seja a versão instalada em sua máquina.
5. Instalar dependências:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
6. Verificar a configuração:
``` powershell
.\.venv\Scripts\python.exe manage.py check
```
7. Criar tabelas do banco de dados:
```powershell
.\.venv\Scripts\python.exe manage.py migrate
```
8. Criar usuário:
```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser --username ADMINISTRADOR
```
Substitua ADMINISTRADOR pelo nome de usuário desejado.

Informe o e-mail solicitado e escolha uma senha. A senha não aparece no
terminal enquanto é digitada; esse comportamento é normal.

O usuário criado poderá acessar a aplicação e o painel administrativo do
Django.

Se o usuário já tiver sido criado anteriormente naquele banco, não
execute novamente esse comando. Caso precise redefinir a senha, utilize:

``` powershell
.\.venv\Scripts\python.exe manage.py changepassword demo
```
9. Iniciar servidor local:
```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/), digite `ADMINISTRADOR` (nome de usuário escolhido anteriormente) e use a senha escolhida durante a criação do usuário.

## Estrutura
- `config/` configura Django, SQLite, autenticação e rotas.
- `gestao/` contém modelos, formulários, telas, serviço de estoque, migrações e testes.
- `templates/` contém as páginas HTML.
- `static/` contém o CSS.
- `db.sqlite3` é criado em cada computador. O Git ignora o banco e a pasta do ambiente virtual.

## Autores
Aline Pereira Barbosa
Diogo Américo Gomes Diógenes
Gabriel Ferreira Machado
Guilherme de Souza Medeiros
Hiago Protásio dos Passos Sales
João Gabriel Lopes Trindade
Vinícius Evangelista de Souza
