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

1.  O usuário acessa uma página ou envia um formulário pelo navegador;
2.  O Django recebe a solicitação e consulta as rotas definidas em
    `config/urls.py`;
3.  As rotas da aplicação são encaminhadas para `gestao/urls.py`;
4.  A URL seleciona a função correspondente em `gestao/views.py`;
5.  A view verifica a solicitação, utiliza os formulários quando há
    dados de entrada e acessa os modelos para consultar ou persistir
    informações;
6.  Nas movimentações de estoque, a view chama a função especializada em
    `gestao/servicos.py`;
7.  O ORM do Django traduz as operações dos modelos para comandos do
    banco SQLite;
8.  A view seleciona um template e envia os dados necessários para sua
    renderização;
9.  O Django devolve o HTML ao navegador.

Nem toda solicitação percorre todos esses componentes. Uma consulta
simples, por exemplo, pode passar diretamente da view para o ORM; uma
movimentação de estoque também utiliza a camada de serviços.

------------------------------------------------------------------------

## 2. Estrutura de diretórios e arquivos

A estrutura de referência do projeto é apresentada abaixo. Arquivos
gerados localmente, como o banco SQLite e o ambiente virtual, não fazem
parte do código-fonte versionado.

```text
gestaofacil/
│
├── manage.py
├── requirements.txt
├── README.md
├── ARQUITETURA.md
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
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_clientes.py
│       ├── 0002_pedidos.py
│       ├── 0003_estoque.py
│       └── 0004_endereco_cliente.py
│
├── templates/
│   ├── base.html
│   ├── painel.html
│   ├── registration/
│   │   └── login.html
│   ├── partials/
│   │   ├── _menu.html
│   │   └── _paginacao.html
│   ├── clientes/
│   │   ├── _campo.html
│   │   ├── lista.html
│   │   ├── form.html
│   │   └── detalhe.html
│   ├── pedidos/
│   │   ├── lista.html
│   │   ├── form.html
│   │   └── detalhe.html
│   └── estoque/
│       ├── lista.html
│       ├── form.html
│       └── detalhe.html
│
└── static/
    └── css/
        ├── app.css
        └── layout_moderno.css
```

### 2.1. Arquivos da raiz

| Arquivo | Responsabilidade |
|---|---|
| `manage.py` | Ponto de entrada para comandos Django: servidor, migrações, usuários e testes. |
| `requirements.txt` | Fixa a dependência Python `Django==5.2.19`. |
| `README.md` | Apresenta o MVP, suas funcionalidades e a instalação/execução local. |
| `ARQUITETURA.md` | Documenta a organização do código, os modelos, as views e os fluxos da v0.1.1-alpha. |
| `.gitignore` | Exclui arquivos locais, incluindo `.venv/`, `db.sqlite3*`, `.env*`, `__pycache__/` e configurações do editor. |

### 2.2. Diretório `config/`

Esse diretório reúne as configurações gerais do projeto Django.

| Arquivo | Responsabilidade |
|---|---|
| `settings.py` | Configuração de aplicações, middlewares, templates, SQLite, autenticação, idioma, fuso e arquivos estáticos. |
| `urls.py` | Rotas gerais: administração, login, logout e encaminhamento para `gestao.urls`. |
| `asgi.py` | Configuração ASGI. |
| `wsgi.py` | Configuração WSGI. |
| `__init__.py` | Identifica `config` como pacote Python. |

O banco utiliza SQLite (`db.sqlite3` na raiz), o idioma é `pt-br` e o
fuso horário é `America/Sao_Paulo`. `STATICFILES_DIRS` aponta para
`static/`, que armazena as duas folhas de estilo.

A configuração de desenvolvimento utiliza `DEBUG=True`, a chave definida
em `DJANGO_SECRET_KEY` quando presente (ou uma chave de fallback de uso
local) e `ALLOWED_HOSTS` restritos aos endereços locais. Isso não é uma
configuração preparada para implantação pública.

### 2.3. Diretório `gestao/`

Esse diretório concentra o comportamento de negócio.

| Arquivo | Responsabilidade |
|---|---|
| `models.py` | Entidades, campos, relacionamentos, ordenações e restrições de banco. |
| `forms.py` | Formulários e validações; inclui CEP, UF e controles de quantidade. |
| `views.py` | Processa requisições, buscas, filtros, paginação, indicadores, alterações e renderização de páginas. |
| `servicos.py` | Registra movimentações de estoque preservando a consistência entre saldo e histórico. |
| `urls.py` | Associa as rotas de clientes, pedidos, estoque e painel às views. |
| `tests.py` | Cinco testes automatizados de fluxos centrais. |
| `admin.py` | Não registra os modelos comerciais no Django Admin; o gerenciamento desses dados usa telas próprias. |
| `apps.py` | Configura a aplicação Django `gestao`. |
| `__init__.py` | Identifica `gestao` como pacote Python. |
| `migrations/` | Migrações incrementais, incluindo `0004_endereco_cliente.py`. |

------------------------------------------------------------------------

## 3. Modelo de dados

Os modelos estão definidos em `gestao/models.py`. Eles representam as
quatro entidades principais do domínio da aplicação.

### 3.1. Cliente

Representa uma pessoa cadastrada no sistema. Seus dados são armazenados na tabela `cliente` e ordenados primeiramente por `nome` e, em seguida, pela chave primária (`id`).

Campos principais:

- `nome`: nome do cliente, obrigatório (`CharField`, até 120 caracteres).
- `telefone`: telefone opcional (até 30 caracteres).
- `observacoes`: anotações opcionais (até 500 caracteres).
- **`cep`**: CEP opcional (até 9 caracteres; formato de apresentação `00000-000`).
- **`logradouro`**: rua, avenida ou outro logradouro (até 150 caracteres).
- **`numero`**: número do endereço armazenado como texto (até 20 caracteres, permitindo `S/N`).
- **`complemento`**: informação complementar, como bloco ou apartamento (até 120 caracteres).
- **`bairro`**: bairro (até 100 caracteres).
- **`cidade`**: cidade (até 100 caracteres).
- **`uf`**: sigla da unidade federativa (até dois caracteres).

Os sete campos de endereço foram acrescentados pela migração
`0004_endereco_cliente.py` e são opcionais (`blank=True`, `default=""`).
A verificação do formato de CEP e a seleção/validação da UF ocorrem na
camada de formulário, não em uma integração externa de consulta de CEP.

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

As listas acrescentaram buscas com `icontains` e filtros
de status/saldo; esses recursos não foram acompanhados da declaração de
índices compostos adicionais. O uso de `select_related("cliente")` nas
consultas relevantes evita buscas repetidas dos dados dos clientes ao
renderizar pedidos, sem transformar o acesso em uma consulta N+1 nesses
percursos.

Índices compostos adicionais podem ser avaliados futuramente a partir
dos filtros, ordenações e planos de execução das consultas mais
frequentes. A decisão de adicioná-los deve considerar o volume de dados
e o custo de manutenção dos próprios índices.

------------------------------------------------------------------------

## 4. Formulários e validação dos dados

Os formulários estão em `gestao/forms.py`. Eles validam os dados recebidos
antes de as views persistirem ou alterarem os registros. A apresentação
visual está nos templates e não substitui a validação no servidor.

| Formulário | Finalidade e validações principais |
|---|---|
| `ClienteForm` | Cadastra e edita nome, telefone, endereço e observações. O nome é obrigatório, o endereço é opcional, o CEP é validado e normalizado e a UF é escolhida em um `Select`. |
| `PedidoForm` | Cadastra/edita cliente, descrição, quantidade inteira positiva, data de entrega e observações. |
| `ItemEstoqueForm` | Cadastra nome, unidade e estoque mínimo decimal não negativo, com até três casas decimais. |
| `MovimentacaoForm` | Recebe tipo, quantidade decimal positiva (mínimo `0,001`), observações e chave UUID oculta da operação. |

**Validações específicas do endereço:**

- `ClienteForm.clean_cep()`: aceita oito dígitos, com ou sem hífen, e
  normaliza o CEP preenchido para `00000-000`; o campo pode ficar vazio.
- `ClienteForm.clean_uf()`: converte a sigla para maiúsculas e verifica
  se está entre as 27 unidades federativas. O widget `forms.Select`
  apresenta os nomes dos estados e do Distrito Federal, armazenando as
  respectivas siglas de duas letras. Não existe consulta automática de
  endereço a partir do CEP.
- Os demais campos de endereço são opcionais; `numero` é texto para
  comportar representações como `S/N`.

**Demais validações:** `PedidoForm` exige quantidade inteira maior ou
igual a 1. `ItemEstoqueForm` e `MovimentacaoForm` trabalham com
`DecimalField` localizado, permitindo entrada decimal com vírgula; as
quantidades são convertidas para milésimos antes do armazenamento.

Na interface, `templates/clientes/form.html` renderiza os campos
individualmente, divididos em **Informações pessoais**, **Endereço** e
**Observações**. O componente `templates/clientes/_campo.html` exibe
rótulo, controle, texto de ajuda e erros de cada campo, preservando a
validação original dos formulários Django.

Os formulários são processados pelas views. Dados inválidos fazem a
página ser reexibida com erros associados aos campos; dados válidos
seguem para a operação correspondente.

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

As views coordenam as requisições. Consultam os modelos, validam os dados
com formulários e retornam templates ou redirecionamentos. As telas
internas exigem autenticação por `@login_required`.

### 6.1. Painel --- `painel`

- Calcula o **total de clientes**, os **pedidos pendentes**, os **pedidos
  em produção** e os **itens com estoque baixo**, utilizando `count()` e
  filtros no ORM. Os valores não são armazenados em uma tabela de
  indicadores.
- Recupera até **seis pedidos não finalizados**, em ordem de entrega;
  usa `select_related("cliente")` para carregar o cliente juntamente
  com o pedido.
- Recupera até **seis itens para reposição**, definidos pela condição
  `saldo_milesimos__lte=F("estoque_minimo_milesimos")`. A contagem
  do indicador considera **todos** os itens nessa condição, não somente
  os seis exibidos.
- Renderiza `templates/painel.html` com cartões de indicadores e duas
  listas resumidas.
- Os números são atualizados com um novo carregamento da página; não há
  atualização em tempo real por WebSocket ou atualização periódica.

### 6.2. Clientes

- `clientes_lista`: recebe `q` pela URL (`GET`), limita a consulta de
  busca a 100 caracteres, pesquisa nome **ou** telefone usando `Q()` e
  `icontains` e apresenta **dez registros por página** com `Paginator`.
- `cliente_form`: apresenta o formulário organizado em três grupos;
  salva novos registros ou atualiza os existentes somente após
  `ClienteForm.is_valid()`.
- `cliente_detalhe`: apresenta contato, endereço opcional, observações
  e pedidos associados. Na ausência de pedidos, oferece uma ação para
  criar o primeiro.

### 6.3. Pedidos

- `pedidos_lista`: consulta os pedidos com `select_related("cliente")`;
  permite busca (`q`) pela descrição **ou** nome do cliente e filtro
  `status` (`PENDENTE`, `EM_PRODUCAO`, `FINALIZADO`), com **dez registros
  por página**. Valores de filtro desconhecidos são ignorados.
- `pedido_form`: cadastra ou edita pedidos. Pedidos finalizados não
  podem ser editados, mesmo se seu estado mudar antes da atualização.
- `pedido_detalhe`: apresenta os dados do pedido e utiliza
  `select_related("cliente")`.
- `pedido_status`: recebe POST, compara o estado esperado enviado pelo
  formulário ao estado atual e só realiza a transição se ambos
  coincidirem. Assim, evita avançar novamente um pedido com uma
  solicitação baseada em status desatualizado.

### 6.4. Estoque

- `estoque_lista`: recebe busca `q` por nome do item e filtro `situacao`
  (`baixo` quando saldo <= mínimo; `normal` quando saldo > mínimo),
  com **dez itens por página**. O filtro usa `F()` para comparar duas
  colunas do banco.
- `estoque_novo`: cadastra o item e converte o estoque mínimo
  informado no formulário para milésimos.
- `estoque_detalhe`: apresenta o saldo, a unidade e o histórico;
  recebe a entrada/saída e chama `registrar_movimentacao` de
  `gestao/servicos.py`. A resposta pode indicar movimentação registrada,
  repetida, saldo insuficiente ou limite excedido.

**Paginação compartilhada:** as três views de listagem usam
`Paginator(..., 10).get_page(request.GET.get("page"))`. O contexto
inclui `page_obj` e os filtros selecionados. O componente
`templates/partials/_paginacao.html` usa `{% querystring %}` (Django
5.2) para conservar os parâmetros de busca e filtro ao navegar entre
as páginas. As pesquisas e os filtros são **server-side**, não filtros
implementados apenas no navegador.

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

O código utiliza SQLite e não utiliza `select_for_update()`;
esse mecanismo não produz bloqueio de linha no
backend SQLite. Caso a aplicação evolua para um banco com suporte a
bloqueios de linha e passe a exigir esse tipo de estratégia, a
concorrência deverá ser reavaliada conforme o banco utilizado.

Os testes incluídos verificam saídas superiores ao saldo, repetição de
uma operação e preservação do saldo em cenários sequenciais. Eles não
representam um teste de carga nem uma simulação de múltiplas requisições
simultâneas.

------------------------------------------------------------------------

## 8. Templates e interface --- diretório `templates/`

Os templates são arquivos HTML renderizados pelo Django. O layout atual
adota componentes reutilizáveis, uma navegação responsiva e maior
controle sobre a apresentação dos formulários e das listagens.

| Arquivo | Finalidade na v0.1.1-alpha |
|---|---|
| `base.html` | Estrutura compartilhada; carrega os dois CSS, define ícones SVG locais, sidebar, cabeçalho, menu móvel, salto para o conteúdo e mensagens do Django. |
| `partials/_menu.html` | Links de Painel, Clientes, Pedidos e Estoque, com destaque da seção ativa via `request.resolver_match.url_name` e `aria-current="page"`. |
| `partials/_paginacao.html` | Navegação por páginas, contagem de registros e manutenção dos filtros com `{% querystring %}`. |
| `painel.html` | Dashboard com quatro indicadores do banco, atalhos, pedidos em aberto e itens para reposição. |
| `registration/login.html` | Tela de autenticação redesenhada, incluindo indicação de credenciais inválidas; continua utilizando o `LoginView` nativo. |
| `clientes/lista.html` | Pesquisa por nome/telefone, tabela responsiva, cidade/UF e estado vazio. |
| `clientes/form.html` | Cadastro/edição organizado em Informações pessoais, Endereço e Observações. |
| `clientes/_campo.html` | Componente para exibir rótulo, campo, texto de ajuda e erros individuais. |
| `clientes/detalhe.html` | Telefone, endereço, observações e histórico de pedidos; orientação quando não há pedidos. |
| `pedidos/lista.html` | Pesquisa por descrição/cliente, filtro de status, etiquetas e paginação. |
| `pedidos/form.html` | Cadastro e edição de pedidos. |
| `pedidos/detalhe.html` | Detalhes, status e ações disponíveis para o pedido. |
| `estoque/lista.html` | Pesquisa por nome, filtro de situação, saldo/mínimo, etiquetas e paginação. |
| `estoque/form.html` | Cadastro de um novo item. |
| `estoque/detalhe.html` | Saldo, formulário de movimentação e histórico, incluindo estado vazio. |

O template `base.html` é estendido pelas demais páginas com `{% extends
"base.html" %}`. Usuários autenticados recebem menu lateral no desktop,
barra superior e menu recolhível em telas estreitas; a página de login
utiliza o layout para visitantes. Os ícones de navegação são símbolos
SVG definidos localmente em `base.html`, sem dependência de biblioteca
externa.

As listagens usam tabelas com cabeçalhos e indicação visual de status;
o CSS adapta sua apresentação para telas menores. Quando não existem
registros ou uma pesquisa retorna zero resultados, os templates
apresentam textos explicativos e, quando aplicável, atalhos para criar
novos registros ou limpar filtros.

O Django continua responsável por renderizar os formulários e validar
os dados. Formulários que alteram registros incluem `{% csrf_token %}`.
O `base.html` utiliza as mensagens do framework (`messages`) para
exibir sucesso, avisos e erros com estilos próprios. As mensagens
associadas a formulários inválidos permanecem junto aos respectivos
campos. Há elementos de acessibilidade, como salto para o conteúdo,
rótulos, navegação sem JavaScript, `aria-current`, `role="alert"`
para avisos e regras CSS que respeitam preferência por movimento reduzido.
Esses recursos **não** constituem uma auditoria completa de
acessibilidade ou garantia de conformidade WCAG.

------------------------------------------------------------------------

## 9. Arquivos estáticos --- diretório `static/`

A pasta `static/css/` contém duas folhas de estilo versionadas:

| Arquivo | Responsabilidade |
|---|---|
| `app.css` | Base visual e estilos originais: componentes de formulário, painéis, botões, listas e personalizações do cadastro de clientes. |
| `layout_moderno.css` | Camada de refinamento: sidebar, cabeçalho, login, dashboard, tabelas e estados vazios, mensagens, responsividade e detalhes de acessibilidade. |

Os dois arquivos são carregados por `templates/base.html`, **nessa
ordem**:

```django
<link rel="stylesheet" href="{% static 'css/app.css' %}">
<link rel="stylesheet" href="{% static 'css/layout_moderno.css' %}">
```

Por ser carregado depois, `layout_moderno.css` pode complementar ou
sobrescrever determinadas declarações da folha anterior. Ícones SVG
reutilizáveis ficam embutidos em `base.html`, e não em arquivos remotos.
O projeto não depende de Bootstrap, React ou biblioteca de ícones
baixada em tempo de execução.

------------------------------------------------------------------------

## 10. Migrações do banco de dados

As migrações em `gestao/migrations/` registram as alterações do esquema
e permitem reconstruir as tabelas em uma nova instalação. A v0.1.1-alpha
contém **quatro** migrações de negócio:

| Arquivo | Alteração registrada |
|---|---|
| `0001_clientes.py` | Criação da tabela de clientes com nome, telefone e observações. |
| `0002_pedidos.py` | Criação dos pedidos e relacionamento com clientes. |
| `0003_estoque.py` | Criação dos itens e das movimentações de estoque, incluindo suas restrições. |
| `0004_endereco_cliente.py` | Adição de CEP, logradouro, número, complemento, bairro, cidade e UF à tabela de clientes. |

A quarta migração **complementa** a primeira, preservando o histórico
e permitindo atualizar uma instalação que já utilizava o esquema
anterior. Não é necessário editar ou reaplicar `0001_clientes.py` para
adicionar esses campos.

Para aplicar migrações pendentes:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

O arquivo `db.sqlite3` é gerado localmente e ignorado pelo Git. As
migrações são versionadas; **os registros dos usuários e os dados de
negócio não são compartilhados** entre computadores pelo repositório.
O Django também aplica suas próprias migrações para autenticação,
sessões e administração.

------------------------------------------------------------------------

## 11. Testes automatizados --- `gestao/tests.py`

O repositório contém a classe `FluxosGestaoFacilTest`, baseada em
`django.test.TestCase`. Na v0.1.1-alpha, a suíte versionada possui
**cinco métodos de teste**:

| Método | Cenário coberto |
|---|---|
| `test_painel_exige_login` | Redirecionamento de usuário não autenticado. |
| `test_cadastra_cliente_e_valida_nome` | Rejeição de nome vazio e cadastro de cliente válido. |
| `test_pedido_aparece_no_historico_e_nao_avanca_duas_vezes` | Cadastro, histórico do cliente e proteção contra repetição de transição de status usando estado esperado antigo. |
| `test_saida_atinge_minimo_e_repeticao_preserva_o_saldo` | Entrada, saída, repetição, recusa de saldo insuficiente e alerta de reposição. |
| `test_quantidade_decimal_com_virgula` | Quantidade decimal informada com vírgula. |

Execução no Windows/PowerShell:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

O Django utiliza um banco de testes separado do banco local de
trabalho.

A leitura do código permite identificar os casos presentes; ela não
substitui a execução da suíte no ambiente de quem instalar o projeto.

**Limite da cobertura:** a aplicação atualmente não inclui testes automatizados
específicos para os sete campos de endereço, o menu de UF, as quatro
contagens do painel, a busca, os filtros, a paginação ou a
responsividade. Essas funcionalidades estão implementadas, mas sua
cobertura automatizada não deve ser presumida. Também não há testes de
carga ou concorrência real sob estresse, tampouco comprovação de comportamento sob múltiplas requisições simultâneas.

------------------------------------------------------------------------

## 12. Como acompanhar uma funcionalidade no código

Os caminhos abaixo apresentam uma sequência sugerida para estudar
cada parte do sistema.

### 12.1. Cadastro de cliente

1. `gestao/urls.py` — localizar `/clientes/novo/` e `/clientes/<id>/editar/`.
2. `gestao/views.py` — localizar `cliente_form`, responsável pelo GET/POST.
3. `gestao/forms.py` — observar `ClienteForm`, `clean_cep()`, `clean_uf()` e o `Select` de UF.
4. `gestao/models.py` — consultar `Cliente` e seus campos de endereço.
5. `gestao/migrations/0004_endereco_cliente.py` — observar como o banco passou a armazenar os campos adicionais.
6. `templates/clientes/form.html` — verificar os três grupos visuais do formulário.
7. `templates/clientes/_campo.html` — verificar a exibição reutilizável dos campos e erros.
8. `templates/clientes/detalhe.html` — verificar os dados exibidos após o cadastro.

### 12.2. Cadastro e atualização de pedido

1. `gestao/urls.py` — localizar as rotas de pedidos.
2. `gestao/views.py` — localizar `pedido_form`, `pedido_detalhe` e `pedido_status`.
3. `gestao/forms.py` — consultar `PedidoForm`.
4. `gestao/models.py` — consultar `Pedido`, seus status, relacionamento com `Cliente` e propriedade `proximo_status`.
5. `templates/pedidos/` — verificar listagem, formulário e detalhes.
6. `templates/clientes/detalhe.html` — verificar os pedidos associados ao cliente.

### 12.3. Entrada e saída de estoque

1. `gestao/urls.py` — localizar as rotas de estoque.
2. `gestao/views.py` — localizar `estoque_novo` e `estoque_detalhe`.
3. `gestao/forms.py` — consultar `ItemEstoqueForm` e `MovimentacaoForm`.
4. `gestao/servicos.py` — acompanhar `registrar_movimentacao`.
5. `gestao/models.py` — consultar `ItemEstoque` e `MovimentacaoEstoque`.
6. `templates/estoque/` — verificar cadastro, saldo e histórico.
7. `templates/painel.html` — verificar os indicadores e itens com saldo baixo.

### 12.4. Autenticação

1. `config/settings.py` — verificar as configurações de autenticação.
2. `config/urls.py` — localizar as rotas `entrar/` e `sair/`.
3. `templates/registration/login.html` — verificar o formulário e os erros de login.
4. `templates/base.html` — verificar o layout autenticado, o menu móvel, as mensagens e o formulário de logout com POST e CSRF.
5. `templates/partials/_menu.html` — observar a navegação e o destaque da rota atual.
6. `gestao/views.py` — observar `login_required` nas views internas.

### 12.5. Busca, filtros, paginação e indicadores

1. `gestao/views.py` — estudar `clientes_lista`, `pedidos_lista`, `estoque_lista` e `painel`.
2. `Q`, `icontains` e `F()` — observar como os filtros são executados no banco.
3. `Paginator(..., 10)` — verificar como as listas são divididas em páginas.
4. `templates/partials/_paginacao.html` — verificar `{% querystring %}` e a preservação dos filtros.
5. `templates/clientes/lista.html`, `templates/pedidos/lista.html` e `templates/estoque/lista.html` — verificar campos de busca, filtros, etiquetas e estados vazios.
6. `templates/painel.html` — localizar os quatro contadores e as duas listas resumidas.
7. `static/css/layout_moderno.css` — observar as regras visuais e os pontos de quebra para diferentes larguras.

------------------------------------------------------------------------

## 13. Observações sobre o escopo e a evolução

O projeto foi desenvolvido como um MVP acadêmico para execução e
demonstração local. Por isso, algumas decisões devem ser compreendidas
dentro desse escopo:

- O banco **SQLite** fica na máquina que executa o sistema. Não existe
  sincronização entre instalações e nem implantação pública configurada.
- As páginas são renderizadas pelo Django; não há aplicação nativa para
  celular, API REST separada ou frontend JavaScript independente.
- A interface foi adaptada para diferentes larguras, incluindo menu
  móvel, tabelas responsivas e estados vazios. Isso não significa que
  tenha passado por auditoria formal de acessibilidade.
- A autenticação é nativa do Django; **não** há cadastro público de
  usuários, perfis com papéis distintos ou isolamento de clientes,
  pedidos e estoque por empresa/conta. Todas as contas autenticadas
  acessam a mesma base de dados de negócio.
- O endereço do cliente é opcional e digitado manualmente. O CEP é
  validado por formato; não há integração automática com consulta de
  CEP, geocodificação ou mapas.
- Os pedidos e o estoque são funcionalidades **independentes**:
  finalizar um pedido não gera baixa automática de materiais, e não há
  vínculo de consumo de estoque por pedido.
- O histórico do cliente é uma lista de pedidos; não há auditoria
  histórica de cada mudança de status.
- Os indicadores e filtros são calculados no carregamento das páginas,
  não transmitidos em tempo real.
- Itens de estoque podem ser cadastrados e movimentados; a versão
  analisada não expõe telas próprias para editar ou excluir itens, nem
  para excluir clientes ou pedidos.
- Não há módulo financeiro, emissão fiscal, integração de pagamento,
  importação/exportação ou integração com APIs externas.
- O serviço de estoque usa transações, atualizações condicionais e uma
  chave única por operação, mas o projeto não apresenta testes de
  concorrência real, carga ou estresse.
- Os cinco testes automatizados existentes não cobrem todas as
  funcionalidades adicionadas nas últimas etapas.

**Desempenho e evolução:** a paginação limita as listagens a dez itens
por página e o painel mostra até seis registros em cada seção, mas
isso não garante, por si só, desempenho sob grandes volumes de dados.
Índices específicos para novos filtros, otimização de consultas,
separação por usuários/organizações, ampliação dos testes e eventual
migração para outro banco de dados devem ser considerados quando o
sistema evoluir.

**Segurança:** a configuração de referência mantém `DEBUG=True`, uma
chave de fallback para desenvolvimento e hosts locais. Esses parâmetros
precisam de revisão antes de qualquer implantação pública. Dados reais
de clientes exigem cuidados proporcionais de acesso, privacidade,
backup e proteção de informações pessoais.

------------------------------------------------------------------------

## 14. Documentação complementar

Para executar o projeto em um novo computador, consulte o `README.md` na
raiz do repositório. Ele apresenta os pré-requisitos, a criação do
ambiente virtual, a instalação das dependências, a execução das
migrações, a criação do usuário e o início do servidor.

Este guia complementa o README: enquanto o README orienta a instalação e
a execução, este documento explica como o código está dividido e onde
localizar a implementação das funcionalidades **na v0.1.1-alpha**. As
descrições foram verificadas contra o código-fonte desta versão, sem
presumir funcionalidades futuras ou testes ainda não incorporados.

**Repositório do projeto:** https://github.com/enagonius/gestaofacil
