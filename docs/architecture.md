# Arquitetura da Liceu Engine

## Visão geral da arquitetura

A Liceu Engine é um núcleo de gestão de conhecimento pessoal projetado para evoluir ao longo do tempo sem depender de uma plataforma específica. O projeto separa claramente a lógica de negócios do núcleo, a documentação e os testes, permitindo crescimento controlado e integrações futuras.

## Objetivos da Engine

- Organizar conhecimento de forma estruturada e duradoura.
- Suportar diferentes plataformas de saída sem acoplamento ao núcleo.
- Permitir evoluções incrementais com foco em clareza e reutilização.
- Servir como base para gestão de conhecimento pessoal ao longo da vida acadêmica e profissional.

## Princípios arquiteturais

- Independência de plataforma: o núcleo não deve depender de Notion, Obsidian ou qualquer saída específica.
- Modularidade: cada responsabilidade deve viver em um módulo ou pacote próprio.
- Simplicidade: a estrutura deve ser clara e intuitiva.
- Evolução contínua: a arquitetura deve suportar crescimento e novas integrações sem reescrita completa.
- Código organizado: arquivos pequenos e responsabilidade única para cada módulo.

## Organização dos módulos atuais

- `engine/`: pacote principal do núcleo da Engine.
- `engine/__init__.py`: exporta versão e define o pacote.
- `engine/__main__.py`: ponto de execução mínimo para iniciar o pacote.
- `engine/version.py`: versão da aplicação.
- `engine/core/`: espaço reservado para a lógica central do domínio.
- `engine/config/`: espaço reservado para configuração e carregamento de ambiente.
- `engine/utils/`: espaço reservado para utilitários gerais.

## Diretrizes para crescimento futuro

- Adicionar funcionalidades ao núcleo dentro de `engine/core/` sem misturar com integração de plataformas.
- Usar `engine/config/` para centralizar parâmetros, validações e carregamento de configurações.
- Colocar helpers reutilizáveis em `engine/utils/` para evitar duplicação.
- Implementar integrações com Notion, Obsidian ou Markdown em pacotes separados se necessário, preservando o núcleo limpo.
- Manter a documentação atualizada conforme novos módulos e responsabilidades forem adicionados.
