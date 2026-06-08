# Rascunho Regras de Negócio - Sistema de Denúncias

## PRINCÍPIO DO SISTEMA
- Proteção do denunciante
- Controle contra abuso
- Moderação obrigatória

---

## USUÁRIOS

### Cadastro:
- Nome
- Email (único)
- Senha
- Telefone (opcional)

### Regras:
- Usuário deve estar autenticado para denunciar
- Pode editar dados e senha
- Pode ser suspenso

## TIPOS DE USUÁRIO

### Usuário comum:
- Criar denúncia
- Escolher anonimato
- Anexar arquivos
- Ver próprias denúncias
- Ver vídeos educativos

### Moderador:
- Aprovar/rejeitar denúncias
- Classificar denúncias
- Vincular/alterar delegacia
- Gerenciar vídeos
- Não vê autor de denúncia anônima

### Admin:
- Gerenciar usuários
- Alterar cargos
- Ver estatísticas
- Não vê autor de denúncia anônima

---
## DENÚNCIAS

### Criação:
- Apenas usuários logados
- Contém:
  - Descrição
  - Título (opcional)
  - Delegacia (opcional)
  - Anexos (opcionais)
  - Anonimato

### Tipos:
- Anônima
- Identificada

### Anonimato:
- Nunca exposto para usuários, moderadores ou admins
- Mantido internamente pelo sistema

### Status:
- Pendente
- Aprovada
- Rejeitada

### Visibilidade:
- Pendente: só autor vê
- Aprovada: pode ser exibida sem dados sensíveis
- Rejeitada: só autor vê

### Moderação:
- Moderador aprova/rejeita
- Pode classificar e vincular delegacia
- Não pode alterar conteúdo original

## ANTI-ABUSO
- Sistema permite punição de usuários
- Possível limite de denúncias

## ANEXOS
- Permitidos: imagens e documentos
- Proibido: vídeos
- Acesso controlado

---

## DELEGACIAS
- Tipos:
  - Civil
  - Militar
  - Mulher
  - Criança e Adolescente
- Usuário pode vincular ou não
- Moderador pode alterar depois

---

## VÍDEOS EDUCATIVOS
- Acesso público
- Gerenciado por moderadores/admins
- Apenas links externos(urls do youtube vime, não gurdar videos na aplicação)

---

## PRIVACIDADE
- Dados do denunciante protegidos
- Nunca expostos em denúncias anônimas
- Acesso restrito no sistema

---

## REGRAS IMPORTANTES
- Denúncias falsas podem gerar punição
- Conteúdo só é público após moderação
- Conteúdo original não pode ser alterado