import os
import pathlib
import shutil
import subprocess

CI_PROVIDER = "{{ copier__ci_provider }}"
SEMANTIC_RELEASE = {{ "True" if copier__enable_semantic_release else "False" }}
SECRET_SCANNING = {{ "True" if copier__enable_secret_scanning else "False" }}
TASK_RUNNER = "{{ copier__task_runner }}"

ROOT = pathlib.Path(".")


def remove(path: str) -> None:
    p = ROOT / path
    if p.exists():
        if p.is_file() or p.is_symlink():
            p.unlink()
        else:
            for child in sorted(p.rglob("*"), reverse=True):
                if child.is_file() or child.is_symlink():
                    child.unlink()
                elif child.is_dir():
                    child.rmdir()
            p.rmdir()


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def init_semantic_release_dependencies() -> None:
    if not SEMANTIC_RELEASE:
        return

    if shutil.which("docker"):
        uid = os.getuid()
        gid = os.getgid()
        run(
            [
                "docker",
                "run",
                "--rm",
                "--user",
                f"{uid}:{gid}",
                "-w",
                "/app",
                "-v",
                f"{ROOT.resolve()}:/app",
                "-e",
                "npm_config_cache=/tmp/.npm",
                "node:lts",
                "/bin/bash",
                "-c",
                "xargs npm install < dependencies-init.txt",
            ]
        )
        run(
            [
                "docker",
                "run",
                "--rm",
                "--user",
                f"{uid}:{gid}",
                "-w",
                "/app",
                "-v",
                f"{ROOT.resolve()}:/app",
                "-e",
                "npm_config_cache=/tmp/.npm",
                "node:lts",
                "/bin/bash",
                "-c",
                "xargs npm install --save-dev < dependencies-dev-init.txt",
            ]
        )
        return

    if shutil.which("npm"):
        run(["bash", "-lc", "xargs npm install < dependencies-init.txt"])
        run(["bash", "-lc", "xargs npm install --save-dev < dependencies-dev-init.txt"])
        return

    print("Warning: semantic-release dependencies were not installed (docker and npm not found).")


def main() -> None:
    init_semantic_release_dependencies()

    if TASK_RUNNER != "make":
        remove("Makefile")
    if TASK_RUNNER != "task":
        remove("Taskfile.yml")
    if TASK_RUNNER != "just":
        remove("justfile")

    if CI_PROVIDER != "github":
        remove(".github")
    if CI_PROVIDER != "gitlab":
        remove(".gitlab-ci.yml")

    if not SEMANTIC_RELEASE:
        remove("package.json")
        remove("dependencies-init.txt")
        remove("dependencies-dev-init.txt")
        remove(".releaserc.json")
        remove("CHANGELOG.md")
        remove(".github/workflows/semantic-release.yaml")
        remove(".github/workflows/semantic-pull-request.yaml")

    if not SECRET_SCANNING:
        remove(".github/workflows/secret-scan.yaml")


if __name__ == "__main__":
    main()
