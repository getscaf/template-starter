import os
import pathlib
import shlex
import subprocess

CI_PROVIDER = "{{ copier__ci_provider }}"
SEMANTIC_RELEASE = {{ "True" if copier__enable_semantic_release else "False" }}
SECRET_SCANNING = {{ "True" if copier__enable_secret_scanning else "False" }}
TASK_RUNNER = "{{ copier__task_runner }}"

ROOT = pathlib.Path(".")
TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
SUCCESS = "\x1b[1;32m [SUCCESS]: "


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


def run_init_script() -> None:
    run(["bash", "./scripts/init-dev.sh"])


def init_git_repo() -> None:
    if (ROOT / ".git").exists():
        return
    print(INFO + "Initializing git repository..." + TERMINATOR)
    print(INFO + f"Current working directory: {os.getcwd()}" + TERMINATOR)
    subprocess.run(
        shlex.split("git -c init.defaultBranch=main init . --quiet"), check=True
    )
    print(SUCCESS + "Git repository initialized." + TERMINATOR)


def configure_git_remote() -> None:
    repo_url = "{{ copier__repo_url }}"
    if repo_url:
        print(INFO + f"repo_url: {repo_url}" + TERMINATOR)
        existing_origin = subprocess.run(
            shlex.split("git remote get-url origin"),
            capture_output=True,
            text=True,
        )
        if existing_origin.returncode == 0:
            current_origin = existing_origin.stdout.strip()
            print(
                INFO
                + f"Remote origin already configured ({current_origin}). Skipping add."
                + TERMINATOR
            )
            return
        command = f"git remote add origin {repo_url}"
        subprocess.run(shlex.split(command), check=True)
        print(SUCCESS + f"Remote origin={repo_url} added." + TERMINATOR)
    else:
        print(
            WARNING
            + "No repo_url provided. Skipping git remote configuration."
            + TERMINATOR
        )


def main() -> None:
    init_git_repo()
    configure_git_remote()
    run_init_script()

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
