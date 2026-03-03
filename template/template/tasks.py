import os
import pathlib
import shlex
import shutil
import subprocess

CI_PROVIDER = "{{ copier__ci_provider }}"
SEMANTIC_RELEASE = {{ "True" if copier__enable_semantic_release else "False" }}
SECRET_SCANNING = {{ "True" if copier__enable_secret_scanning else "False" }}
TASK_RUNNER = "{{ copier__task_runner }}"
CONFIGURE_REPO = {{ "True" if copier__configure_repo else "False" }}
REPO_PROVIDER = "{{ copier__repo_provider }}"
REPO_ORG = "{{ copier__repo_org }}"
REPO_NAME = "{{ copier__repo_name }}"
REPO_URL = "{{ copier__repo_url }}"
CREATE_REPO = {{ "True" if copier__create_repo else "False" }}
REPO_VISIBILITY = "{{ copier__repo_visibility }}"

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
    if not CONFIGURE_REPO:
        return
    repo_url = REPO_URL.strip()
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


def maybe_create_repo() -> None:
    if not CREATE_REPO:
        return

    if not CONFIGURE_REPO:
        return
    if not REPO_ORG.strip() or not REPO_NAME.strip():
        print(WARNING + "Repo org/name not set. Skipping repo creation." + TERMINATOR)
        return
    repo_name = f"{REPO_ORG.strip()}/{REPO_NAME.strip()}"

    if REPO_PROVIDER == "github":
        if not shutil.which("gh"):
            print(WARNING + "gh CLI is not installed. Skipping repo creation." + TERMINATOR)
            return

        gh_env = os.environ.copy()
        gh_env["GH_HOST"] = "github.com"

        repo_exists = subprocess.run(
            ["gh", "repo", "view", repo_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=gh_env,
        )
        if repo_exists.returncode == 0:
            print(INFO + f"GitHub repository {repo_name} already exists." + TERMINATOR)
            return

        print(
            INFO
            + f"Creating GitHub repository {repo_name} ({REPO_VISIBILITY})..."
            + TERMINATOR
        )
        create_repo = subprocess.run(
            ["gh", "repo", "create", repo_name, f"--{REPO_VISIBILITY}"],
            capture_output=True,
            text=True,
            env=gh_env,
        )
        if create_repo.returncode != 0:
            error = create_repo.stderr.strip() or create_repo.stdout.strip() or "unknown error"
            print(
                WARNING
                + f"Failed to create GitHub repository {repo_name}: {error}"
                + TERMINATOR
            )
            return
        print(SUCCESS + f"GitHub repository {repo_name} created." + TERMINATOR)
        return

    if REPO_PROVIDER == "gitlab":
        if not shutil.which("glab"):
            print(WARNING + "glab CLI is not installed. Skipping repo creation." + TERMINATOR)
            return

        glab_env = os.environ.copy()
        glab_env["GITLAB_HOST"] = "gitlab.com"
        repo_exists = subprocess.run(
            ["glab", "repo", "view", repo_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=glab_env,
        )
        if repo_exists.returncode == 0:
            print(INFO + f"GitLab repository {repo_name} already exists." + TERMINATOR)
            return

        print(
            INFO
            + f"Creating GitLab repository {repo_name} ({REPO_VISIBILITY})..."
            + TERMINATOR
        )
        create_repo = subprocess.run(
            ["glab", "repo", "create", repo_name, f"--{REPO_VISIBILITY}"],
            capture_output=True,
            text=True,
            env=glab_env,
        )
        if create_repo.returncode != 0:
            error = create_repo.stderr.strip() or create_repo.stdout.strip() or "unknown error"
            print(
                WARNING
                + f"Failed to create GitLab repository {repo_name}: {error}"
                + TERMINATOR
            )
            return
        print(SUCCESS + f"GitLab repository {repo_name} created." + TERMINATOR)
        return

    print(
        WARNING
        + f"Repo creation not implemented for provider '{REPO_PROVIDER}'. Skipping."
        + TERMINATOR
    )


def main() -> None:
    init_git_repo()
    maybe_create_repo()
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
