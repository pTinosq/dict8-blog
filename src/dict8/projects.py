import json
import os
import uuid
from pathlib import Path
from typing import NamedTuple

PHASES = (1, 2, 3, 4)


class ProjectInfo(NamedTuple):
    id: str
    slug: str
    name: str
    description: str


class ProjectStore:
    def __init__(
        self,
        root: Path | None = None,
    ) -> None:
        self.root = root or Path(
            os.environ.get("DICT8_BLOG_PROJECTS_DIR", "")
            or str(Path.home() / "dict8-blog-projects")
        )
        self.index_path = self.root / "index.json"

    def load_index(self) -> dict:
        if not self.index_path.exists():
            return {"projects": [], "active_id": None}
        return json.loads(self.index_path.read_text())

    def save_index(self, data: dict) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(data, indent=2))

    def list_projects(self) -> list[ProjectInfo]:
        data = self.load_index()
        return [
            ProjectInfo(
                id=p["id"],
                slug=p["slug"],
                name=p["name"],
                description=p["description"],
            )
            for p in data["projects"]
        ]

    def create_project(self, slug: str, name: str, description: str) -> "Project":
        data = self.load_index()
        slug_lower = slug.strip().lower().replace(" ", "-")
        if any(p["slug"] == slug_lower for p in data["projects"]):
            raise ValueError(f"Project slug already exists: {slug_lower}")
        project_id = str(uuid.uuid4())
        data["projects"].append(
            {
                "id": project_id,
                "slug": slug_lower,
                "name": name.strip(),
                "description": description.strip(),
            }
        )
        self.save_index(data)
        proj = Project(self, project_id, slug_lower, name.strip(), description.strip())
        proj.ensure_manifest()
        return proj

    def get_project(self, project_id: str) -> "Project | None":
        data = self.load_index()
        for p in data["projects"]:
            if p["id"] == project_id:
                return Project(self, p["id"], p["slug"], p["name"], p["description"])
        return None

    def get_active_project(self) -> "Project | None":
        data = self.load_index()
        active_id = data.get("active_id")
        if active_id is None:
            return None
        return self.get_project(active_id)

    def set_active_project(self, project_id: str) -> None:
        data = self.load_index()
        if not any(p["id"] == project_id for p in data["projects"]):
            raise ValueError(f"Unknown project id: {project_id}")
        data["active_id"] = project_id
        self.save_index(data)


class Project:
    def __init__(
        self,
        store: ProjectStore,
        project_id: str,
        slug: str,
        name: str,
        description: str,
    ) -> None:
        self.store = store
        self.id = project_id
        self.slug = slug
        self.name = name
        self.description = description
        self.root_dir = store.root / project_id
        self.manifest_path = self.root_dir / "manifest.json"

    def manifest(self) -> dict:
        if not self.manifest_path.exists():
            return {
                "slug": self.slug,
                "name": self.name,
                "description": self.description,
                "phase_files": {str(p): f"phase_{p}.md" for p in PHASES},
                "blog_file": "blog.md",
            }
        return json.loads(self.manifest_path.read_text())

    def save_manifest(self, data: dict) -> None:
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(json.dumps(data, indent=2))

    def ensure_manifest(self) -> None:
        self.save_manifest(self.manifest())

    def path_for(self, key: str) -> Path:
        manifest = self.manifest()
        if key == "blog":
            return self.root_dir / manifest["blog_file"]
        return self.root_dir / manifest["phase_files"][str(key)]

    def get_context_for_phase(self, phase: int) -> str:
        if phase not in PHASES:
            return ""
        path = self.path_for(str(phase))
        return path.read_text() if path.exists() else ""

    def set_context_for_phase(self, phase: int, content: str) -> None:
        if phase not in PHASES:
            return
        path = self.path_for(str(phase))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def get_blog(self) -> str:
        path = self.path_for("blog")
        return path.read_text() if path.exists() else ""

    def set_blog(self, content: str) -> None:
        path = self.path_for("blog")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


default_store = ProjectStore()


def get_active_project() -> Project | None:
    return default_store.get_active_project()


def set_active_project(project_id: str) -> None:
    default_store.set_active_project(project_id)


def list_projects() -> list[ProjectInfo]:
    return default_store.list_projects()


def create_project(slug: str, name: str, description: str) -> Project:
    return default_store.create_project(slug, name, description)


def get_project(project_id: str) -> Project | None:
    return default_store.get_project(project_id)
