from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    app_name: str = "Liceu Engine"
    version: str = "0.1.0"
    workspace: Path = field(default_factory=lambda: PROJECT_ROOT / "workspace")
    docs_path: Path = field(default_factory=lambda: PROJECT_ROOT / "docs")
    cache_path: Path = field(default_factory=lambda: PROJECT_ROOT / ".cache")
    database_path: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "engine.db")
