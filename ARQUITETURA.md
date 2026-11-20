# Guia de organização do código-fonte

> **Objetivo deste documento:** apresentar a organização interna do
> GestãoFácil, explicar a responsabilidade de cada diretório e arquivo e
> indicar o caminho para acompanhar as principais funcionalidades no
> código.
>
> **Tecnologias da versão documentada:** Python 3.13, Django 5.2.19, SQLite,
> HTML e CSS.

------------------------------------------------------------------------

## 1. Visão geral da arquitetura

O GestãoFácil é uma aplicação web desenvolvida com Django. O navegador
apresenta as páginas HTML e envia as solicitações do usuário; o Django
recebe essas solicitações, executa as validações e regras da aplicação,
consulta ou atualiza o banco de dados SQLite e devolve uma página HTML
como resposta.

A aplicação utiliza a arquitetura tradicional de páginas renderizadas no
servidor (*server-side rendering*). Portanto, o frontend não é uma
aplicação JavaScript independente nem uma API REST separada: as páginas
HTML são renderizadas pelos templates do Django.

O código está organizado em duas partes principais:

-   **`config/` - configuração do projeto Django:** concentra as
    configurações gerais e o roteamento principal.
-   **`gestao/` - aplicação de negócio:** concentra os modelos,
    formulários, views, regras de serviço, rotas, migrações e testes do
    GestãoFácil.

Os diretórios `templates/` e `static/` complementam essa estrutura: o
primeiro contém as páginas HTML e o segundo contém os recursos
estáticos, como a folha de estilos CSS.

### 1.1. Fluxo geral de uma solicitação

1.  O usuário acessa uma página ou envia um formulário pelo navegador.
2.  O Django recebe a solicitação e consulta as rotas definidas em
    `config/urls.py`.
3.  As rotas da aplicação são encaminhadas para `gestao/urls.py`.
4.  A URL seleciona a função correspondente em `gestao/views.py`.
5.  A view verifica a solicitação, utiliza os formulários quando há
    dados de entrada e acessa os modelos para consultar ou persistir
    informações.
6.  Nas movimentações de estoque, a view chama a função especializada em
    `gestao/servicos.py`.
7.  O ORM do Django traduz as operações dos modelos para comandos do
    banco SQLite.
8.  A view seleciona um template e envia os dados necessários para sua
    renderização.
9.  O Django devolve o HTML ao navegador.

Nem toda solicitação percorre todos esses componentes. Uma consulta
simples, por exemplo, pode passar diretamente da view para o ORM; uma
movimentação de estoque também utiliza a camada de serviços.

------------------------------------------------------------------------

## 2. Estrutura de diretórios e arquivos

A estrutura de referência do projeto é apresentada abaixo. Arquivos
gerados localmente, como o banco SQLite e o ambiente virtual, não fazem
parte do código-fonte versionado.

``` text
gestaofacil/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── gestao/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── servicos.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   │
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_clientes.py
│       ├── 0002_pedidos.py
│       └── 0003_estoque.py
│
├── templates/
│   ├── base.html
│   ├── painel.html
│   │
│   ├── registration/
│   │   └── login.html
│   │
│   ├── clientes/
│   │   ├── lista.html
│   │   ├── form.html
│   │   └── detalhe.html
│   │
│   ├── pedidos/
│   │   ├── lista.html
│   │   ├── form.html
│   │   └── detalhe.html
│   │
│   └── estoque/
│       ├── lista.html
│       ├── form.html
│       └── detalhe.html
│
└── static/
    └── css/
        └── app.css
```

### 2.1. Arquivos da raiz

  -----------------------------------------------------------------------
  Arquivo                             Responsabilidade
  ----------------------------------- -----------------------------------
  `manage.py`                         Ponto de entrada para comandos
                                      administrativos do Django, como
                                      iniciar o servidor, executar
                                      migrações, criar usuários e rodar
                                      testes.

  `requirements.txt`                  Registra as dependências Python do
                                      projeto. Na versão de referência,
                                      fixa o Django em `5.2.19`.

  `README.md`                         Apresenta o projeto e as instruções
                                      de instalação, execução e teste.

  `.gitignore`                        Impede que arquivos locais e
                                      temporários, como `.venv/`,
                                      `__pycache__/` e `db.sqlite3`,
                                      sejam incluídos no versionamento.
  -----------------------------------------------------------------------

### 2.2. Diretório `config/`

Esse diretório representa a configuração geral do projeto Django.

  -----------------------------------------------------------------------
  Arquivo                             Responsabilidade
  ----------------------------------- -----------------------------------
  `settings.py`                       Define as configurações gerais,
                                      aplicações instaladas, middlewares,
                                      templates, banco de dados, idioma,
                                      fuso horário, arquivos estáticos e
                                      parâmetros de autenticação.

  `urls.py`                           Define as rotas de entrada do
                                      projeto, incluindo administração,
                                      login, logout e encaminhamento para
                                      as rotas da aplicação `gestao`.

  `asgi.py`                           Disponibiliza a configuração ASGI
                                      do projeto.

  `wsgi.py`                           Disponibiliza a configuração WSGI
                                      do projeto.

  `__init__.py`                       Identifica `config` como um pacote
                                      Python.
  -----------------------------------------------------------------------

Na configuração de referência, o banco utiliza o mecanismo SQLite e o
arquivo local `db.sqlite3`, localizado na raiz do projeto. O idioma está
definido como português do Brasil e o fuso horário como
`America/Sao_Paulo`.

As configurações de desenvolvimento da versão de referência incluem
`DEBUG=True` e uma chave secreta de fallback destinada ao uso local.
Esses parâmetros não devem ser considerados uma configuração pronta para
produção ou exposição pública na internet.

### 2.3. Diretório `gestao/`

Esse é o diretório central da aplicação. Nele estão os componentes que
implementam as funcionalidades do GestãoFácil.

  -----------------------------------------------------------------------
  Arquivo                             Responsabilidade
  ----------------------------------- -----------------------------------
  `models.py`                         Define as entidades, seus campos,
                                      relacionamentos, ordenações e
                                      restrições de integridade.

  `forms.py`                          Define os formulários e valida os
                                      dados enviados pelo usuário antes
                                      de serem processados.

  `views.py`                          Recebe as solicitações direcionadas
                                      pelas URLs, coordena as operações e
                                      seleciona os templates de resposta.

  `servicos.py`                       Centraliza a operação de registro
                                      de movimentações de estoque e seus
                                      cuidados de integridade.

  `urls.py`                           Relaciona os endereços da aplicação
                                      às respectivas funções de view.

  `tests.py`                          Contém testes automatizados dos
                                      principais fluxos da aplicação.

  `admin.py`                          No código de referência, contém
                                      apenas um comentário explicando que
                                      os cadastros comerciais utilizam
                                      telas próprias; os modelos
                                      comerciais não são registrados ali.

  `apps.py`                           Contém a configuração da aplicação
                                      Django `gestao`.

  `__init__.py`                       Identifica `gestao` como um pacote
                                      Python.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 3. Modelo de dados

Os modelos estão definidos em `gestao/models.py`. Eles representam as
quatro entidades principais do domínio da aplicação.

### 3.1. Cliente

Representa uma pessoa cadastrada no sistema.

Campos principais:

-   `nome`: nome do cliente.
-   `telefone`: telefone, opcional.
-   `observacoes`: informações adicionais, opcionais.

A ordenação padrão é por nome e, em seguida, pela chave primária (`id`).
O modelo utiliza a tabela `cliente`.

### 3.2. Pedido

Representa um pedido associado a um cliente.

Campos principais:

-   `cliente`: relacionamento com `Cliente`, por meio de uma chave
    estrangeira.
-   `descricao`: descrição do pedido.
-   `quantidade`: quantidade solicitada.
-   `data_entrega`: data prevista para entrega.
-   `status`: situação atual do pedido.
-   `observacoes`: informações adicionais, opcionais.

Os status disponíveis são:

-   `PENDENTE` --- Pendente.
-   `EM_PRODUCAO` --- Em produção.
-   `FINALIZADO` --- Finalizado.

O relacionamento utiliza `on_delete=PROTECT`, evitando que um cliente
com pedidos relacionados seja excluído diretamente. A ordenação padrão
considera `data_entrega` e `id`. O modelo também possui restrições para
impedir quantidade não positiva e status fora dos valores previstos.

A propriedade `proximo_status` determina a próxima transição permitida:
de pendente para em produção e de em produção para finalizado. Um pedido
finalizado não possui próximo status.

### 3.3. ItemEstoque

Representa um material ou item controlado pelo estoque.

Campos principais:

-   `nome`: identificação do item.
-   `unidade`: unidade de medida.
-   `saldo_milesimos`: saldo armazenado em milésimos da unidade.
-   `estoque_minimo_milesimos`: limite mínimo, também armazenado em
    milésimos.

As unidades disponíveis no código de referência são kg, g, L, mL e
unidade.

O saldo e o estoque mínimo são armazenados como números inteiros em
milésimos, evitando depender de operações com números de ponto flutuante
para representar quantidades fracionárias. As propriedades `saldo` e
`estoque_minimo` apresentam esses valores como números decimais. A
propriedade `estoque_baixo` verifica se o saldo é menor ou igual ao
estoque mínimo.

### 3.4. MovimentacaoEstoque

Registra cada entrada ou saída de um item.

Campos principais:

-   `item`: relacionamento com `ItemEstoque`.
-   `tipo`: entrada ou saída.
-   `quantidade_milesimos`: quantidade movimentada em milésimos.
-   `criada_em`: data e hora de criação automática.
-   `observacoes`: informação complementar, opcional.
-   `chave_operacao`: identificador UUID da operação.

O relacionamento com o item utiliza `on_delete=PROTECT`. A ordenação
padrão apresenta as movimentações mais recentes primeiro, considerando a
data de criação e a chave primária.

O modelo possui restrições para impedir quantidades não positivas e para
impedir a repetição da mesma combinação de item e chave de operação.

### 3.5. Relacionamentos

Os relacionamentos principais são:

-   Um cliente pode possuir vários pedidos. Cada pedido pertence a um
    cliente.
-   Um item de estoque pode possuir várias movimentações. Cada
    movimentação pertence a um item.

Representação simplificada:

``` text
CLIENTE 1 ───────── N PEDIDO

ITEM_ESTOQUE 1 ──── N MOVIMENTACAO_ESTOQUE
```

As relações são implementadas por chaves estrangeiras (`ForeignKey`) no
Django.

### 3.6. Ordenação e índices

Os modelos utilizam a opção `ordering` para definir a ordenação padrão
dos registros. Essa opção determina a ordem das consultas, mas não cria,
por si só, um índice específico para os campos ordenados.

As chaves primárias e estrangeiras possuem indexação padrão no Django. O
modelo de movimentações também declara uma restrição de unicidade
composta por item e chave da operação.

Índices compostos adicionais podem ser avaliados futuramente a partir
dos filtros, ordenações e planos de execução das consultas mais
frequentes. A decisão de adicioná-los deve considerar o volume de dados
e o custo de manutenção dos próprios índices.

------------------------------------------------------------------------

## 4. Formulários e validação dos dados

Os formulários estão definidos em `gestao/forms.py`. Eles separam a
apresentação e a validação dos dados recebidos das operações executadas
pelas views.

  -----------------------------------------------------------------------
  Formulário                          Finalidade
  ----------------------------------- -----------------------------------
  `ClienteForm`                       Cadastrar e editar nome, telefone e
                                      observações de clientes.

  `PedidoForm`                        Cadastrar e editar cliente,
                                      descrição, quantidade, data de
                                      entrega e observações do pedido.

  `ItemEstoqueForm`                   Cadastrar o nome, a unidade e o
                                      estoque mínimo de um item.

  `MovimentacaoForm`                  Receber o tipo, a quantidade, as
                                      observações e a chave UUID de uma
                                      movimentação.
  -----------------------------------------------------------------------

O `PedidoForm` exige quantidade inteira positiva. O `ItemEstoqueForm`
utiliza um campo decimal para o estoque mínimo, com até três casas
decimais. O `MovimentacaoForm` aceita quantidades decimais com até três
casas e exige valor mínimo de `0,001`.

Os formulários são processados pelas views. Quando os dados são
inválidos, o Django devolve a página com os erros associados aos campos;
quando são válidos, a view prossegue com a operação correspondente.

------------------------------------------------------------------------

## 5. Rotas e controle das solicitações

O roteamento é dividido entre `config/urls.py` e `gestao/urls.py`.

### 5.1. Rotas gerais --- `config/urls.py`

  Endereço     Finalidade
  ------------ ------------------------------------------------
  `/admin/`    Painel administrativo padrão do Django.
  `/entrar/`   Tela de autenticação.
  `/sair/`     Encerramento da sessão por solicitação POST.
  `/`          Encaminha para as rotas da aplicação `gestao`.

### 5.2. Rotas da aplicação --- `gestao/urls.py`

  --------------------------------------------------------------------------
  Endereço                   View associada          Finalidade
  -------------------------- ----------------------- -----------------------
  `/`                        `painel`                Painel inicial.

  `/clientes/`               `clientes_lista`        Lista de clientes.

  `/clientes/novo/`          `cliente_form`          Cadastro de cliente.

  `/clientes/<id>/`          `cliente_detalhe`       Detalhes e histórico do
                                                     cliente.

  `/clientes/<id>/editar/`   `cliente_form`          Edição de cliente.

  `/pedidos/`                `pedidos_lista`         Lista de pedidos.

  `/pedidos/novo/`           `pedido_form`           Cadastro de pedido.

  `/pedidos/<id>/`           `pedido_detalhe`        Detalhes do pedido.

  `/pedidos/<id>/editar/`    `pedido_form`           Edição de pedido.

  `/pedidos/<id>/status/`    `pedido_status`         Atualização do status
                                                     do pedido.

  `/estoque/`                `estoque_lista`         Lista de itens de
                                                     estoque.

  `/estoque/novo/`           `estoque_novo`          Cadastro de item.

  `/estoque/<id>/`           `estoque_detalhe`       Detalhes, movimentações
                                                     e histórico do item.
  --------------------------------------------------------------------------

`<id>` representa o identificador numérico do registro.

As views de negócio utilizam o decorador `login_required`, exigindo
autenticação. A atualização do status do pedido também utiliza
`require_POST`, restringindo a operação ao método POST.

------------------------------------------------------------------------

## 6. Camada de views --- `gestao/views.py`

As views coordenam a lógica de cada solicitação. Elas recebem os dados
da requisição, chamam formulários e modelos, e retornam uma página ou
redirecionamento.

### 6.1. Painel --- `painel`

-   Recupera até seis pedidos que ainda não foram finalizados.
-   Utiliza `select_related("cliente")` para carregar os dados do
    cliente junto aos pedidos exibidos.
-   Recupera os itens cujo saldo é menor ou igual ao estoque mínimo.
-   Renderiza `templates/painel.html`.

### 6.2. Clientes

-   `clientes_lista`: consulta os clientes e apresenta a listagem.
-   `cliente_form`: apresenta o formulário de cadastro ou edição e salva
    os dados válidos.
-   `cliente_detalhe`: apresenta os dados de um cliente e os pedidos
    associados a ele.

### 6.3. Pedidos

-   `pedidos_lista`: apresenta os pedidos e utiliza
    `select_related("cliente")` para carregar os dados relacionados.
-   `pedido_form`: cadastra ou edita pedidos. A edição de pedidos
    finalizados é impedida.
-   `pedido_detalhe`: apresenta os dados do pedido e utiliza
    `select_related("cliente")`.
-   `pedido_status`: recebe uma solicitação POST e tenta avançar o
    status para a próxima etapa permitida. A atualização considera
    também o status esperado enviado pelo formulário, evitando que uma
    solicitação baseada em um status antigo avance o pedido
    indevidamente.

### 6.4. Estoque

-   `estoque_lista`: apresenta os itens cadastrados.
-   `estoque_novo`: cadastra um item e converte o estoque mínimo para a
    representação inteira em milésimos.
-   `estoque_detalhe`: apresenta o saldo e o histórico de movimentações;
    recebe o formulário de entrada ou saída e encaminha a operação para
    `registrar_movimentacao`, em `gestao/servicos.py`.

------------------------------------------------------------------------

## 7. Serviço de movimentação de estoque --- `gestao/servicos.py`

A função `registrar_movimentacao(item, dados)` concentra a operação de
entrada e saída de estoque.

Essa lógica foi separada da view para manter a regra de movimentação em
um componente próprio, que pode ser chamado pela camada de apresentação
e testado de maneira mais direta.

A função executa as seguintes etapas:

1.  Converte a quantidade recebida para milésimos, utilizando a
    representação inteira adotada pelo modelo.
2.  Recupera a chave UUID da operação e prepara a consulta que verifica
    se ela já foi registrada para aquele item.
3.  Abre uma transação com `transaction.atomic()`.
4.  Para uma saída, executa uma atualização condicional: o saldo só é
    reduzido se for maior ou igual à quantidade solicitada.
5.  Para uma entrada, executa uma atualização condicional que impede
    ultrapassar o limite de armazenamento definido no código.
6.  Utiliza uma expressão `F()` para realizar a soma ou subtração no
    banco de dados, em vez de calcular a alteração com um saldo
    previamente carregado na aplicação.
7.  Se o saldo for atualizado, cria o registro correspondente em
    `MovimentacaoEstoque`, dentro da mesma transação.
8.  Se ocorrer uma violação de integridade relacionada à chave única da
    operação, a transação é revertida e a função identifica a
    movimentação já registrada.
9.  Devolve um resultado que permite à view apresentar a mensagem
    correspondente.

### 7.1. Integridade e concorrência

A combinação de transação atômica, atualização condicional com `F()` e
restrição de unicidade reduz riscos de inconsistência entre o saldo e o
histórico de movimentações.

A atualização condicional faz com que a disponibilidade do saldo seja
verificada pelo próprio banco no momento da operação de escrita. A
transação mantém a atualização do saldo e o registro do histórico como
uma única unidade de trabalho: se a gravação da movimentação falhar, a
alteração do saldo é revertida.

A chave UUID, combinada à restrição única por item, também impede que a
mesma operação seja registrada duas vezes para o mesmo item.

O código de referência utiliza SQLite. Não utiliza
`select_for_update()`; esse mecanismo não produz bloqueio de linha no
backend SQLite. Caso a aplicação evolua para um banco com suporte a
bloqueios de linha e passe a exigir esse tipo de estratégia, a
concorrência deverá ser reavaliada conforme o banco utilizado.

Os testes incluídos verificam saídas superiores ao saldo, repetição de
uma operação e preservação do saldo em cenários sequenciais. Eles não
representam um teste de carga nem uma simulação de múltiplas requisições
simultâneas.

------------------------------------------------------------------------

## 8. Templates e interface --- diretório `templates/`

Os templates são os arquivos HTML que o Django utiliza para construir as
páginas apresentadas no navegador.

  -----------------------------------------------------------------------
  Arquivo                             Finalidade
  ----------------------------------- -----------------------------------
  `base.html`                         Estrutura compartilhada, cabeçalho,
                                      navegação, mensagens e inclusão do
                                      CSS.

  `painel.html`                       Painel com pedidos em aberto e
                                      itens para reposição.

  `registration/login.html`           Formulário de autenticação.

  `clientes/lista.html`               Listagem de clientes.

  `clientes/form.html`                Cadastro e edição de clientes.

  `clientes/detalhe.html`             Dados do cliente e histórico de
                                      pedidos.

  `pedidos/lista.html`                Listagem de pedidos.

  `pedidos/form.html`                 Cadastro e edição de pedidos.

  `pedidos/detalhe.html`              Dados, status e ações disponíveis
                                      para o pedido.

  `estoque/lista.html`                Listagem de itens e indicação de
                                      estoque baixo.

  `estoque/form.html`                 Cadastro de item de estoque.

  `estoque/detalhe.html`              Saldo, formulário de movimentação e
                                      histórico do item.
  -----------------------------------------------------------------------

O template `base.html` funciona como estrutura comum. As demais páginas
utilizam herança de templates com `extends`, evitando repetir toda a
estrutura HTML.

Os formulários que alteram dados utilizam o token `{% csrf_token %}`,
integrado à proteção CSRF do Django.

------------------------------------------------------------------------

## 9. Arquivos estáticos --- diretório `static/`

O diretório contém os recursos estáticos da aplicação.

Na versão de referência, a folha de estilos principal é:

``` text
static/css/app.css
```

Esse arquivo define a apresentação visual de elementos como cabeçalho,
navegação, painéis, formulários, botões, mensagens, listas e etiquetas
de status.

A folha de estilos é carregada pelo template `base.html` por meio do
sistema de arquivos estáticos do Django.

------------------------------------------------------------------------

## 10. Migrações do banco de dados

As migrações ficam em `gestao/migrations/`. Elas registram as alterações
na estrutura dos modelos e permitem reproduzir o esquema do banco em
outra instalação.

  -----------------------------------------------------------------------
  Arquivo                             Alteração registrada
  ----------------------------------- -----------------------------------
  `0001_clientes.py`                  Criação da tabela de clientes.

  `0002_pedidos.py`                   Criação da tabela de pedidos e
                                      relacionamento com clientes.

  `0003_estoque.py`                   Criação das tabelas de itens de
                                      estoque e movimentações, incluindo
                                      suas restrições.
  -----------------------------------------------------------------------

As migrações da aplicação são versionadas junto ao código. O arquivo
`db.sqlite3`, por outro lado, é criado localmente quando as migrações
são executadas e não precisa ser compartilhado pelo repositório.

O Django também possui migrações próprias para seus componentes
internos, como autenticação, sessões e administração.

------------------------------------------------------------------------

## 11. Testes automatizados --- `gestao/tests.py`

O arquivo contém a classe `FluxosGestaoFacilTest`, que utiliza
`django.test.TestCase`.

Os testes de referência cobrem os seguintes cenários:

  ------------------------------------------------------------------------------------------------
  Método de teste                                              O que verifica
  ------------------------------------------------------------ -----------------------------------
  `test_painel_exige_login`                                    Confirma que o painel redireciona
                                                               usuários não autenticados para a
                                                               tela de login.

  `test_cadastra_cliente_e_valida_nome`                        Verifica a validação do nome e o
                                                               cadastro de cliente.

  `test_pedido_aparece_no_historico_e_nao_avanca_duas_vezes`   Verifica o cadastro, a presença do
                                                               pedido no histórico do cliente e a
                                                               proteção contra avanço repetido do
                                                               status com o mesmo status esperado.

  `test_saida_atinge_minimo_e_repeticao_preserva_o_saldo`      Verifica entrada, saída, repetição
                                                               de movimentação, recusa de saldo
                                                               insuficiente e alerta no painel.

  `test_quantidade_decimal_com_virgula`                        Verifica o registro de quantidade
                                                               decimal informada com vírgula.
  ------------------------------------------------------------------------------------------------

Para executar os testes, utiliza-se:

``` powershell
.\.venv\Scripts\python.exe manage.py test
```

O Django cria um banco temporário para a execução dos testes, sem
utilizar os registros do banco local de demonstração.

**Limite da cobertura:** esses testes verificam os fluxos descritos na
tabela. Eles não equivalem a testes de carga, testes de estresse ou
comprovação de comportamento sob múltiplas requisições simultâneas.

------------------------------------------------------------------------

## 12. Como acompanhar uma funcionalidade no código

Para facilitar a leitura, os caminhos abaixo indicam a sequência
recomendada para estudar cada parte.

### 12.1. Cadastro de cliente

1.  `gestao/urls.py` --- localizar `clientes/novo/`.
2.  `gestao/views.py` --- localizar `cliente_form`.
3.  `gestao/forms.py` --- consultar `ClienteForm`.
4.  `gestao/models.py` --- consultar o modelo `Cliente`.
5.  `templates/clientes/form.html` --- verificar como o formulário é
    apresentado.
6.  `templates/clientes/detalhe.html` --- verificar a página exibida
    após o cadastro.

### 12.2. Cadastro e atualização de pedido

1.  `gestao/urls.py` --- localizar as rotas de pedidos.
2.  `gestao/views.py` --- localizar `pedido_form`, `pedido_detalhe` e
    `pedido_status`.
3.  `gestao/forms.py` --- consultar `PedidoForm`.
4.  `gestao/models.py` --- consultar `Pedido`, seus status,
    relacionamento com `Cliente` e propriedade `proximo_status`.
5.  `templates/pedidos/` --- verificar listagem, formulário e detalhes.
6.  `templates/clientes/detalhe.html` --- verificar a apresentação do
    histórico de pedidos.

### 12.3. Entrada e saída de estoque

1.  `gestao/urls.py` --- localizar as rotas de estoque.
2.  `gestao/views.py` --- localizar `estoque_novo` e `estoque_detalhe`.
3.  `gestao/forms.py` --- consultar `ItemEstoqueForm` e
    `MovimentacaoForm`.
4.  `gestao/servicos.py` --- acompanhar `registrar_movimentacao`.
5.  `gestao/models.py` --- consultar `ItemEstoque` e
    `MovimentacaoEstoque`.
6.  `templates/estoque/` --- verificar cadastro, saldo e histórico.
7.  `templates/painel.html` --- verificar a apresentação dos itens que
    atingiram o estoque mínimo.

### 12.4. Autenticação

1.  `config/settings.py` --- verificar as configurações de autenticação.
2.  `config/urls.py` --- localizar as rotas `entrar/` e `sair/`.
3.  `templates/registration/login.html` --- verificar o formulário de
    login.
4.  `templates/base.html` --- verificar a navegação exibida para
    usuários autenticados.
5.  `gestao/views.py` --- observar o uso de `login_required` nas views
    de negócio.

------------------------------------------------------------------------

## 13. Observações sobre o escopo e a evolução

O projeto foi desenvolvido como um MVP acadêmico para execução e
demonstração local. Por isso, algumas decisões devem ser compreendidas
dentro desse escopo:

-   O banco de dados utilizado é SQLite, criado localmente.
-   A interface é renderizada pelo Django por meio de templates HTML.
-   A autenticação utiliza os recursos nativos do Django.
-   As operações de estoque possuem validações e mecanismos de
    integridade descritos neste guia.
-   Os testes automatizados cobrem os fluxos indicados na seção 11, mas
    não substituem testes de carga ou de concorrência sob estresse.
-   Índices adicionais, mudança de banco de dados, implantação em
    servidor e endurecimento das configurações de segurança podem ser
    avaliados conforme os requisitos de uma futura versão.

As configurações de desenvolvimento presentes no projeto ---
especialmente `DEBUG=True`, a chave secreta de fallback e os hosts
locais --- não devem ser utilizadas sem revisão em uma implantação
pública.

------------------------------------------------------------------------

## 14. Documentação complementar

Para executar o projeto em um novo computador, consulte o `README.md` na
raiz do repositório. Ele apresenta os pré-requisitos, a criação do
ambiente virtual, a instalação das dependências, a execução das
migrações, a criação do usuário e o início do servidor.

Este guia complementa o README: enquanto o README orienta a instalação e
a execução, este documento explica como o código está dividido e onde
localizar a implementação das funcionalidades.

**Repositório do projeto:** https://github.com/enagonius/gestaofacil
