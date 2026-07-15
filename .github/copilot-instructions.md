# Liceu Engine - Instruções para IA

## Objetivo

O Liceu Engine é um software de longo prazo desenvolvido para criar, organizar e evoluir um sistema pessoal de gestão do conhecimento.

O projeto deve ser tratado como um software profissional.

Nunca gerar soluções temporárias quando existir uma solução arquiteturalmente correta.

---

# Filosofia

Scientia ordinata potentia est.

O conhecimento deve permanecer organizado por décadas.

Toda decisão deve priorizar:

- Clareza
- Organização
- Escalabilidade
- Simplicidade
- Reutilização

---

# Linguagem

Todo código deve ser escrito em inglês.

Exemplos:

builder.py
knowledge.py
config.py

Nunca utilizar nomes de variáveis em português.

A documentação pode ser escrita em português.

---

# Estilo

Seguir PEP 8.

Utilizar type hints sempre que possível.

Preferir dataclasses quando apropriado.

Evitar duplicação de código.

Preferir composição à herança quando fizer sentido.

---

# Estrutura

O projeto deve ser organizado em módulos pequenos.

Cada arquivo deve possuir uma única responsabilidade.

Evitar arquivos gigantes.

---

# Dependências

Adicionar novas bibliotecas apenas quando realmente necessárias.

Preferir bibliotecas maduras e amplamente utilizadas.

---

# Testes

Toda funcionalidade relevante deve possuir testes.

---

# Documentação

Toda API pública deve possuir documentação.

Comentários devem explicar decisões, nunca o óbvio.

---

# Git

Utilizar Conventional Commits.

Exemplos:

feat:
fix:
docs:
refactor:
test:
chore:

---

# Arquitetura

O núcleo do projeto nunca deve depender do Notion.

A Engine deve ser independente da plataforma.

Notion, Obsidian e Markdown serão apenas implementações.

---

# Objetivo Final

Criar um software capaz de organizar conhecimento durante toda a vida do usuário.

Toda alteração deve aproximar o projeto desse objetivo.