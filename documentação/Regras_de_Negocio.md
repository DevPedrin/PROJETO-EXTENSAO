# Regras de Negócio — Portal Segurança Digital

---

## HISTÓRICO DE REVISÕES

| Data | Versão | Descrição | Autor |
|---|---|---|---|
| 21/05/2026 | 1 | Criação do documento com as regras de negócio identificadas no projeto. | Equipe Portal Segurança Digital |

---

## Sumário

1. [Objetivo](#1-objetivo)
2. [Definições](#2-definições)
   - 2.1. [RN001 – Controle de acesso ao formulário de denúncia](#21-rn001--controle-de-acesso-ao-formulário-de-denúncia)
   - 2.2. [RN002 – Opção de denúncia anônima](#22-rn002--opção-de-denúncia-anônima)
   - 2.3. [RN003 – Unicidade de usuário no cadastro](#23-rn003--unicidade-de-usuário-no-cadastro)
   - 2.4. [RN004 – Redirecionamento pós-autenticação](#24-rn004--redirecionamento-pós-autenticação)
   - 2.5. [RN005 – Recursos de acessibilidade](#25-rn005--recursos-de-acessibilidade)
   - 2.6. [RN006 – Filtros de delegacias e canais oficiais](#26-rn006--filtros-de-delegacias-e-canais-oficiais)
   - 2.7. [RN007 – Alerta global de segurança](#27-rn007--alerta-global-de-segurança)

---

## 1. Objetivo

O objetivo deste documento é descrever as regras de negócio do projeto **Portal Segurança Digital**.

O Portal Segurança Digital é uma plataforma web de utilidade pública desenvolvida como projeto de extensão do Instituto Federal do Tocantins (IFTO), com foco na prevenção de golpes e fraudes digitais. O sistema oferece conteúdos educativos, canais de denúncia, informações sobre delegacias e vídeos orientativos para a população.

Essas regras de negócio estão identificadas pelo código **RN**.

---

## 2. Definições

### 2.1. RN001 – Controle de acesso ao formulário de denúncia

Esta regra define o controle de acesso à funcionalidade de registro de denúncia no portal.

- O formulário de registro de denúncia **somente será exibido para usuários autenticados** (com sessão ativa no sistema).
- Ao acessar a página `/denuncia/` sem estar autenticado, o sistema **não exibirá o formulário**. Em seu lugar, será apresentado um bloco informativo com ícone de cadeado e a seguinte mensagem:
  > *"Para iniciar o preenchimento da denúncia, por favor, faça login na plataforma."*
- Será exibido um botão **"Fazer Login"** que redirecionará o usuário para a página de login, preservando o endereço de destino no parâmetro `?next=` da URL, para que após o login o usuário seja retornado automaticamente à página de denúncia.

---

### 2.2. RN002 – Opção de denúncia anônima

Esta regra define o comportamento da opção de anonimato no formulário de denúncia.

- Mesmo que o usuário esteja autenticado, o sistema deve oferecer a opção de **realizar a denúncia de forma anônima**, por meio de uma caixa de seleção (checkbox) presente no formulário, com o seguinte texto:
  > *"Desejo fazer esta denúncia de forma anônima (não vincular meu usuário)"*
- Quando esta opção estiver marcada, o registro da denúncia **não deverá ser vinculado ao usuário logado**.
- O sistema deve registrar a denúncia sem associação de identidade, garantindo o sigilo do denunciante.

---

### 2.3. RN003 – Unicidade de usuário no cadastro

Esta regra será utilizada para garantir a unicidade dos nomes de usuário na plataforma.

- Ao submeter o formulário de cadastro, o sistema deve **verificar se o `username` informado já existe** na base de dados.
- Caso o nome de usuário já esteja cadastrado, o sistema **deve bloquear o registro** e retornar a tela de cadastro com a seguinte mensagem de erro:
  > *"Usuário já existe"*
- Apenas após a confirmação de que o `username` é único, o sistema poderá criar a conta e autenticar o usuário automaticamente.

---

### 2.4. RN004 – Redirecionamento pós-autenticação

Esta regra define os comportamentos de redirecionamento após as ações de autenticação do usuário.

As seguintes regras de redirecionamento devem ser aplicadas:

- **Após o login bem-sucedido:**
  - Caso exista parâmetro `next` na requisição POST, o usuário deve ser redirecionado para a URL indicada neste parâmetro.
  - Caso o parâmetro `next` não esteja presente, o usuário deve ser redirecionado para a página inicial do portal (`portal:home`).
  - Caso as credenciais sejam inválidas, o sistema deve retornar à tela de login com a seguinte mensagem de erro:
    > *"Usuário ou senha inválidos."*

- **Após o registro (cadastro) bem-sucedido:**
  - O sistema deve autenticar o usuário automaticamente após a criação da conta.
  - O usuário deve ser redirecionado para a página inicial do portal (`portal:home`).

- **Após o logout:**
  - O sistema deve encerrar a sessão do usuário.
  - O usuário deve ser redirecionado para a página inicial do portal (`portal:home`).

---

### 2.5. RN005 – Recursos de acessibilidade

Esta regra define os recursos de acessibilidade que devem estar disponíveis em todas as páginas do portal.

- O portal deve apresentar, em **todas as páginas**, uma barra de acessibilidade no topo da tela com as seguintes opções:
  - **Aumentar texto (A+):** ao ser acionada, o sistema deve aumentar o tamanho da fonte do documento para 120% do tamanho padrão.
  - **Restaurar texto (A):** ao ser acionada, o sistema deve restaurar o tamanho da fonte do documento para 100% (tamanho padrão).
  - **Alto Contraste:** ao ser acionada, o sistema deve aplicar um filtro de inversão de cores e rotação de matiz (`invert(1) hue-rotate(180deg)`) no corpo da página, facilitando a leitura por pessoas com baixa visão. Uma segunda ativação deve remover o filtro e restaurar o visual original.
- A barra de acessibilidade deve ser exibida com o texto identificador: *"Portal de Utilidade Pública — Instituto Federal do Tocantins"*.

---

### 2.6. RN006 – Filtros de delegacias e canais oficiais

Esta regra define o comportamento dos filtros interativos na página de delegacias.

- A página de delegacias deve apresentar um painel de filtros que permita ao usuário refinar a lista de delegacias e órgãos exibidos, com os seguintes critérios:

  - **Tipo de órgão:** combo com as seguintes opções:
    - Todos os tipos *(padrão)*
    - Delegacia de Crimes Cibernéticos
    - Delegacia de Atendimento ao Idoso
    - Procon
    - Canal Online

  - **Busca por nome:** campo de texto livre que filtra os itens pelo nome do órgão.

  - **Município:** combo com as opções:
    - Palmas — TO (foco exclusivo)

- Os filtros devem ser aplicados dinamicamente, sem necessidade de recarregar a página (via JavaScript).
- Cada item da lista de delegacias deve conter os atributos `data-tipo` e `data-cidade` para suportar a filtragem no lado do cliente.

---

### 2.7. RN007 – Alerta global de segurança

Esta regra define a exibição de um alerta de segurança fixo em todas as páginas do portal.

- Em **todas as páginas** do portal deve ser exibida uma faixa de alerta informativa, posicionada logo abaixo do cabeçalho (header), com o seguinte conteúdo:
  > *"**Atenção:** Nenhuma instituição bancária ou órgão público solicita senhas, códigos ou transferências por telefone ou mensagem. Desconfie sempre e confirme por outros canais antes de qualquer ação."*
- A faixa deve ser visualmente destacada em relação ao restante do conteúdo da página, com ícone de informação.
- A faixa deve ser gerada pelo template base (`base.html`) e, portanto, herdada automaticamente por todas as páginas que o estendem.

---

*Documento gerado com base na análise do código-fonte do projeto Portal Segurança Digital — IFTO Extensão I, 2026.*
