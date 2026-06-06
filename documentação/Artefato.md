# Artefato — Portal Segurança Digital

---

## HISTÓRICO DE REVISÕES

| Data | Versão | Descrição | Autor |
|---|---|---|---|
| 21/05/2026 | 1 | Criação do documento com as funções implementadas no projeto. | Equipe Portal Segurança Digital |

---

## Sumário

1. [Exibir Página Inicial](#1-exibir-página-inicial)
2. [Consultar Delegacias e Canais Oficiais](#2-consultar-delegacias-e-canais-oficiais)
3. [Registrar Denúncia](#3-registrar-denúncia)
4. [Consultar Estatísticas](#4-consultar-estatísticas)
5. [Consultar Vídeos Educativos](#5-consultar-vídeos-educativos)
6. [Autenticar Usuário (Login)](#6-autenticar-usuário-login)
7. [Cadastrar Usuário (Registro)](#7-cadastrar-usuário-registro)
8. [Encerrar Sessão (Logout)](#8-encerrar-sessão-logout)
9. [Legenda](#9-legenda)

---

## Portal Segurança Digital

### 1. Exibir Página Inicial

#### 1.1. Objetivo
Apresentar a página inicial do portal com informações sobre os principais tipos de golpes digitais, números de emergência e chamadas para ação de proteção ao cidadão.

#### 1.2. Acesso
`/` (raiz do portal)

#### 1.3. Permissão de acesso
Acesso público — não requer autenticação.

#### 1.4. Lógica de processamento
- Ao acessar a URL raiz do portal, o sistema renderiza o template `portal/home.html`, estendido do template base `portal/base.html`.
- Não há validações impeditivas para esta página.
- O conteúdo exibido é estático, não depende de consultas ao banco de dados.

#### 1.5. Descrição da interface

| Descrição | Tp | Tm | Ob | Aç | Regras de Apresentação |
|---|---|---|---|---|---|
| **Seção Hero** | — | — | — | — | Apresenta o título principal da página, subtítulo descritivo e dois botões de chamada para ação. |
| Tag identificadora | A | — | — | — | Exibe o texto: *"Serviço de Utilidade Pública"* |
| Título principal | A | — | — | — | Exibe o texto: *"Proteja-se contra Golpes e Fraudes Digitais"* |
| Descrição do portal | A | — | — | — | Texto descritivo sobre o objetivo do portal. |
| Botão "Conhecer os Principais Golpes" | — | — | — | L | Redireciona o usuário para a seção `#golpes` na mesma página (âncora interna). |
| Botão "Registrar uma Denúncia" | — | — | — | L | Redireciona o usuário para a página de denúncia (`portal:denuncia`). |
| **Painel de Números de Emergência** | — | — | — | — | Apresentado ao lado da seção Hero. |
| Polícia Militar | A | — | — | — | Exibe o número: **190** |
| Polícia Civil | A | — | — | — | Exibe o número: **197** |
| Procon | A | — | — | — | Exibe o número: **151** |
| Banco Central | A | — | — | — | Exibe o número: **145** |
| **Seção de Golpes Digitais** | — | — | — | — | Apresenta os principais tipos de golpes em cards com classificação de risco. |
| Card "Golpe do WhatsApp" | A | — | — | — | Classificação: **Risco Alto**. Descreve o golpe e exibe link "Saiba mais e como se proteger". |
| Card "Falso Funcionário de Banco" | A | — | — | — | Classificação: **Risco Alto**. Descreve o golpe e exibe link "Saiba mais e como se proteger". |
| Card "Golpe do Pix" | A | — | — | — | Classificação: **Risco Alto**. Descreve o golpe e exibe link "Saiba mais e como se proteger". |
| Card "Promoções e Prêmios Falsos" | A | — | — | — | Classificação: **Atenção**. Descreve o golpe e exibe link "Saiba mais e como se proteger". |
| Card "Links e Páginas Falsas" | A | — | — | — | Classificação: **Atenção**. Descreve o golpe e exibe link "Saiba mais e como se proteger". |
| Card "Como se Proteger no Dia a Dia" | A | — | — | — | Classificação: **Orientação**. Exibe dicas gerais de segurança digital. |

#### 1.6. Tabelas utilizadas
Não se aplica — conteúdo estático.

---

### 2. Consultar Delegacias e Canais Oficiais

#### 2.1. Objetivo
Apresentar a lista de delegacias especializadas e canais oficiais para registro de ocorrências relacionadas a crimes digitais, com recursos de filtragem interativa.

#### 2.2. Acesso
`/delegacias/`  
Navegação: Menu principal → **Delegacias**

#### 2.3. Permissão de acesso
Acesso público — não requer autenticação.

#### 2.4. Lógica de processamento
- Ao acessar a URL `/delegacias/`, o sistema renderiza o template `portal/delegacias.html`.
- Os dados de delegacias são estáticos no template HTML e os filtros são processados via JavaScript no lado do cliente.
- O sistema aplica os filtros de tipo, texto e cidade dinamicamente, sem recarregar a página. **RN006**

#### 2.5. Descrição da interface

| Descrição | Tp | Tm | Ob | Aç | Regras de Apresentação |
|---|---|---|---|---|---|
| **Painel de Filtros** | — | — | — | — | Apresentado à esquerda da listagem de delegacias. |
| Filtrar por tipo | O | — | N | S | Combo com as opções: *Todos os tipos*, *Delegacia de Crimes Cibernéticos*, *Delegacia de Atendimento ao Idoso*, *Procon*, *Canal Online*. Filtra a lista ao ser alterado. **RN006** |
| Buscar por nome | A | — | N | P | Campo de texto livre. Filtra os itens da lista pelo nome do órgão ao ser digitado. **RN006** |
| Filtrar por município | O | — | N | S | Combo com as opções: *Todos os municípios*, *Palmas*, *Araguaína*, *Gurupi*, *Porto Nacional*. Filtra a lista ao ser alterado. **RN006** |
| **Lista de Delegacias** | — | — | — | — | Apresentada à direita do painel de filtros. Cada item contém: nome, endereço, telefone, horário e botão de ação. |
| Nome da delegacia/canal | A | — | — | — | Apresenta o nome completo do órgão ou canal. |
| Endereço | A | — | — | — | Apresenta o logradouro e município. Ícone de localização à esquerda. |
| Telefone | A | — | — | — | Apresenta o número de telefone do órgão. Ícone de telefone à esquerda. |
| Horário de funcionamento | A | — | — | — | Apresenta o horário de atendimento. Ícone de estrela à esquerda. |
| Botão "Ver no mapa" / "Acessar site" | — | — | — | L | Para delegacias físicas: botão "Ver no mapa". Para canais online: botão "Acessar site". |

#### 2.6. Tabelas utilizadas
Não se aplica — conteúdo estático com filtragem client-side.

---

### 3. Registrar Denúncia

#### 3.1. Objetivo
Permitir que cidadãos autenticados registrem denúncias de golpes e fraudes digitais, com a opção de realizar a denúncia de forma anônima.

#### 3.2. Acesso
`/denuncia/`  
Navegação: Menu principal → **Denunciar**

#### 3.3. Permissão de acesso
- **Visualização da página:** pública — qualquer usuário pode acessar a URL.
- **Acesso ao formulário:** restrito a usuários autenticados. **RN001**

#### 3.4. Lógica de processamento
- Ao acessar a URL `/denuncia/`, o sistema renderiza o template `portal/denuncia.html`.
- O sistema verifica se o usuário está autenticado (`user.is_authenticated`):
  - **Caso autenticado:** o formulário de denúncia é exibido completo para preenchimento.
  - **Caso não autenticado:** o formulário é substituído por um bloco informativo com botão de login, preservando o retorno à página de denúncia após a autenticação. **RN001**

#### 3.5. Descrição da interface

| Descrição | Tp | Tm | Ob | Aç | Regras de Apresentação |
|---|---|---|---|---|---|
| **Bloco informativo** | — | — | — | — | Apresentado à esquerda do formulário, para todos os usuários. |
| Texto de instrução | A | — | — | — | Exibe orientações sobre o preenchimento e a opção de anonimato. |
| Caixa de dica importante | A | — | — | — | Apresenta o texto: *"Se você foi vítima de um crime, registre também um Boletim de Ocorrência na delegacia mais próxima ou pelo site da Polícia Civil do Tocantins."* |
| **Formulário de Denúncia** (usuário autenticado) | — | — | — | — | Exibido somente para usuários com sessão ativa. **RN001** |
| Tipo de golpe | O | — | S | S | Combo com as opções: *Golpe do WhatsApp / Redes Sociais*, *Falso funcionário de banco*, *Golpe do Pix*, *Promoção ou Prêmio falso*, *Link ou página falsa*, *Outro*. Campo obrigatório. |
| Data da ocorrência | N | 10 | N | P | Campo de data no formato DD/MM/AAAA. |
| Cidade | A | — | N | P | Campo de texto. Placeholder: *"Ex.: Palmas — TO"*. |
| Descrição do ocorrido | A | — | S | P | Caixa de texto (textarea). Campo obrigatório. Placeholder descritivo orientando o preenchimento. |
| Nome (opcional) | A | — | N | P | Campo de texto. Placeholder: *"Pode deixar em branco"*. |
| Faixa etária | O | — | N | S | Combo com as opções: *18 a 29 anos*, *30 a 44 anos*, *45 a 59 anos*, *60 anos ou mais*. |
| Denúncia anônima | O | — | N | S | Caixa de seleção (checkbox). Quando marcada, a denúncia não é vinculada ao usuário logado. **RN002** |
| Botão "Enviar Denúncia" | — | — | — | S | Submete o formulário. |
| **Bloco de acesso restrito** (usuário não autenticado) | — | — | — | — | Exibido no lugar do formulário quando o usuário não está autenticado. **RN001** |
| Ícone de cadeado | — | — | — | — | Ícone visual indicando proteção do formulário. |
| Título "Formulário Protegido" | A | — | — | — | Texto: *"Formulário Protegido"* |
| Mensagem orientativa | A | — | — | — | Texto: *"Para iniciar o preenchimento da denúncia, por favor, faça login na plataforma."* |
| Botão "Fazer Login" | — | — | — | L | Redireciona para `accounts/login/?next=/denuncia/`. **RN001, RN004** |

#### 3.6. Tabelas utilizadas
> **Nota:** O back-end de persistência do formulário está previsto para implementação futura. Atualmente o formulário é apresentado mas não há gravação em banco de dados.

---

### 4. Consultar Estatísticas

#### 4.1. Objetivo
Apresentar dados e estatísticas relacionados às denúncias e golpes registrados no portal.

#### 4.2. Acesso
`/estatisticas/`  
Navegação: Menu principal → **Estatísticas**

#### 4.3. Permissão de acesso
Acesso público — não requer autenticação.

#### 4.4. Lógica de processamento
- Ao acessar a URL `/estatisticas/`, o sistema renderiza o template `portal/estatisticas.html`.
- A página está prevista para exibir dados agregados de denúncias registradas no sistema.

#### 4.5. Descrição da interface
> **Nota:** A interface de estatísticas está em desenvolvimento. O conteúdo completo será definido conforme a implementação do back-end de denúncias.

#### 4.6. Tabelas utilizadas
> A serem definidas conforme implementação do módulo de denúncias.

---

### 5. Consultar Vídeos Educativos

#### 5.1. Objetivo
Apresentar uma galeria de vídeos educativos sobre segurança digital, com conteúdo acessível a cidadãos de todas as idades.

#### 5.2. Acesso
`/videos/`  
Navegação: Menu principal → **Vídeos**

#### 5.3. Permissão de acesso
Acesso público — não requer autenticação.

#### 5.4. Lógica de processamento
- Ao acessar a URL `/videos/`, o sistema renderiza o template `portal/videos.html`.
- O conteúdo da galeria é estático, organizado em cards de vídeo.

#### 5.5. Descrição da interface

| Descrição | Tp | Tm | Ob | Aç | Regras de Apresentação |
|---|---|---|---|---|---|
| **Grade de Vídeos** | — | — | — | — | Apresenta os cards de vídeo em grade responsiva. |
| Card de Vídeo | — | — | — | — | Cada card exibe: thumbnail com número do vídeo, botão de play, duração, título e descrição. |
| Thumbnail do vídeo | — | — | — | — | Área visual com cor de fundo diferenciada por vídeo, número sequencial e ícone de play centralizado. |
| Duração | A | — | — | — | Apresenta a duração estimada do vídeo (ex.: *"4 min"*). |
| Título do vídeo | A | — | — | L | Apresenta o título do conteúdo. Exemplos: *"Como Funciona o Golpe do WhatsApp"*, *"Segurança no Uso do Pix"*, *"10 Hábitos de Segurança Digital"*, *"Como Usar Este Portal de Denúncia"*. |
| Descrição do vídeo | A | — | — | — | Breve descrição do conteúdo abordado no vídeo. |

#### 5.6. Tabelas utilizadas
Não se aplica — conteúdo estático.

> **Nota:** Os IDs de vídeo (`data-video-id`) estão como placeholder e devem ser substituídos pelos IDs reais dos vídeos no YouTube em versão futura.

---

### 6. Autenticar Usuário (Login)

#### 6.1. Objetivo
Permitir que usuários cadastrados acessem o portal com suas credenciais para utilizar funcionalidades restritas, como o registro de denúncias.

#### 6.2. Acesso
`/accounts/login/`  
Navegação: Menu principal → **Entrar** ou link no bloco de denúncia restrita.

#### 6.3. Permissão de acesso
Acesso público — não requer autenticação prévia.

#### 6.4. Lógica de processamento
- **Método GET:** o sistema renderiza o template `accounts/login.html` com o formulário de login vazio.
- **Método POST:** o sistema realiza as seguintes verificações:
  - Recupera os campos `username` e `password` da requisição.
  - Autentica as credenciais via `django.contrib.auth.authenticate`.
  - **Caso as credenciais sejam válidas:** inicia a sessão do usuário (`login()`), verifica o parâmetro `next` e redireciona conforme **RN004**.
  - **Caso as credenciais sejam inválidas:** retorna o template de login com a mensagem de erro: *"Usuário ou senha inválidos."*

#### 6.5. Descrição da interface

| Descrição | Tp | Tm | Ob | Aç | Regras de Apresentação |
|---|---|---|---|---|---|
| **Formulário de Login** | — | — | — | — | — |
| Nome de usuário | A | — | S | P | Campo de texto para o `username`. |
| Senha | A | — | S | P | Campo de senha (caracteres ocultos). |
| Mensagem de erro | A | — | — | — | Exibida abaixo do formulário quando as credenciais são inválidas. Texto: *"Usuário ou senha inválidos."* **RN004** |
| Botão "Entrar" | — | — | — | S | Submete o formulário de autenticação. |
| Link "Cadastrar-se" | — | — | — | L | Redireciona para a página de registro (`accounts/register/`). |

#### 6.6. Tabelas utilizadas
- `accounts_user` (model `User`, extende `auth_user` do Django)

---

### 7. Cadastrar Usuário (Registro)

#### 7.1. Objetivo
Permitir que novos usuários criem uma conta no portal para acessar funcionalidades restritas.

#### 7.2. Acesso
`/accounts/register/`

#### 7.3. Permissão de acesso
Acesso público — não requer autenticação prévia.

#### 7.4. Lógica de processamento
- **Método GET:** o sistema renderiza o template `accounts/register.html` com o formulário de cadastro vazio.
- **Método POST:** o sistema realiza as seguintes verificações:
  - Recupera os campos `username` e `password` da requisição.
  - Verifica se já existe usuário cadastrado com o `username` informado. **RN003**
    - **Caso o username já exista:** retorna o template de registro com a mensagem de erro: *"Usuário já existe"*.
  - **Caso o username esteja disponível:** cria o usuário via `User.objects.create_user()`, autentica automaticamente e redireciona para a página inicial. **RN004**

#### 7.5. Descrição da interface

| Descrição | Tp | Tm | Ob | Aç | Regras de Apresentação |
|---|---|---|---|---|---|
| **Formulário de Cadastro** | — | — | — | — | — |
| Nome de usuário | A | — | S | P | Campo de texto para definição do `username`. |
| Senha | A | — | S | P | Campo de senha (caracteres ocultos). |
| Mensagem de erro | A | — | — | — | Exibida quando o nome de usuário já está em uso. Texto: *"Usuário já existe"*. **RN003** |
| Botão "Cadastrar" | — | — | — | S | Submete o formulário de registro. |
| Link "Já tenho conta" | — | — | — | L | Redireciona para a página de login (`accounts/login/`). |

#### 7.6. Tabelas utilizadas
- `accounts_user` (model `User`, extende `auth_user` do Django)

---

### 8. Encerrar Sessão (Logout)

#### 8.1. Objetivo
Encerrar a sessão do usuário autenticado no portal.

#### 8.2. Acesso
`/accounts/logout/`  
Navegação: Menu principal → **Sair** (exibido somente para usuários autenticados).

#### 8.3. Permissão de acesso
Requer usuário autenticado.

#### 8.4. Lógica de processamento
- Ao acessar a URL `/accounts/logout/`, o sistema executa `logout(request)`, encerrando a sessão do usuário.
- Após o encerramento da sessão, o sistema redireciona o usuário para a página inicial do portal (`portal:home`). **RN004**

#### 8.5. Descrição da interface
Não há interface — a ação é executada imediatamente ao acionar o link **"Sair"** presente na barra de navegação.

#### 8.6. Tabelas utilizadas
- `django_session` (sessões gerenciadas pelo Django)

---

## 9. Legenda

| Tp | Descrição |
|---|---|
| A | Alfanumérico |
| N | Numérico |
| O | Opção (combo/select) |
| — | Não se aplica |

| Ob | Descrição |
|---|---|
| S | Obrigatório |
| N | Não obrigatório |
| — | Não se aplica |

| Aç | Descrição |
|---|---|
| P | Pesquisar / Filtrar |
| S | Submeter / Salvar |
| L | Link / Navegação |
| — | Não se aplica |

---

*Documento gerado com base na análise do código-fonte do projeto Portal Segurança Digital — IFTO Extensão I, 2026.*
