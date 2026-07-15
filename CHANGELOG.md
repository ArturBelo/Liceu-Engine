# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- Initial project setup and architecture scaffolding.
- `pyproject.toml` with PEP 621 metadata.
- `engine/` core package with package layout and version management.
- Console logger infrastructure via `engine/logging/logger.py`.
- Exception hierarchy in `engine/exceptions/errors.py`.
- Domain entity `Knowledge` in `engine/core/knowledge.py`.
- In-memory repository implementation `KnowledgeRepository` in `engine/core/repository.py`.
- SQLite-backed repository implementation `SQLiteKnowledgeRepository` in `engine/core/sqlite_repository.py`.
- `KnowledgeService` service layer in `engine/core/service.py`.
- Search support for knowledge items in repository and SQLite repository.
- Pagination and sorting support for knowledge listing.
- Event bus infrastructure with `Event` and `EventBus` in `engine/events/`.
- Documentation scaffolding including `docs/architecture.md`.
- Unit tests covering knowledge entity, repository, service, SQLite repository, search, listing, logger, errors, and events.
- GitHub-related agent and instructions files for project guidance.

## [0.1.0-alpha] - 2026-07-15

### Added

- Base project structure for `Liceu Engine`.
- Core engine module and package initialization.
- Documentation and tests directories.
- Basic logging configuration.
- Exception hierarchy.
- Knowledge domain entity and repository layers.
- SQLite persistence support.
- Service layer and search/pagination features.
- Event bus infrastructure.
