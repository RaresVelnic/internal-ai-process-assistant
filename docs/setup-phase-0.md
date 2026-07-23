# Phase 0: Development Environment Setup

This document records the initial development environment setup for the Internal AI Process Assistant project.

The goal of Phase 0 was to create a clean, reproducible Linux development environment that can be used for backend development, Docker-based workflows, SSH access, and future AI integration work.

## Host Environment

- Host OS: Windows 11 Pro
- Virtualization: Oracle VirtualBox
- Development editor: Visual Studio Code on Windows
- Remote workflow: VS Code Remote SSH
- Version control: Git and GitHub

## Virtual Machine Configuration

- Guest OS: Ubuntu Server 26.04 LTS
- CPU allocation: 4 vCPU
- Memory allocation: 8192 MB
- Disk: 80 GB dynamically allocated VDI
- Network mode: NAT
- SSH access: host loopback port forwarded to guest SSH port

The VM was intentionally configured as a server environment without a graphical desktop.

## Remote Development Workflow

Development is done from Windows using VS Code Remote SSH.

The local editor connects to the Ubuntu VM over SSH and opens the project directory inside the Linux environment.

This keeps the project isolated from other local development environments while still allowing a comfortable editor workflow.

## Python Environment

The project uses a local virtual environment inside the repository.

Initial setup:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install pytest ruff
    python -m pip install -e .

Verified versions during Phase 0:

    Python 3.14.4
    pip 26.1.2
    pytest 9.1.1
    ruff 0.15.22

The project does not install Python packages globally. Project dependencies should be installed inside `.venv`.

## Docker Environment

Docker was installed from the official Docker repository.

Verified versions during Phase 0:

    Docker 29.6.2
    Docker Compose v5.3.1

Useful checks:

    docker ps
    docker run hello-world
    docker compose version

Docker was configured so the development user can run Docker commands without `sudo`.

## Git and GitHub

The repository is hosted on GitHub:

    https://github.com/RaresVelnic/internal-ai-process-assistant

GitHub CLI is installed and authenticated in the VM.

Useful checks:

    git status
    git log --oneline --decorate -3
    gh auth status

Commit metadata uses the GitHub no-reply email address instead of a personal email address.

## Project Foundation

The initial project foundation includes:

    src/internal_ai_process_assistant/
    tests/
    .env.example
    pyproject.toml
    README.md
    .gitignore

The Python package uses a `src/` layout.

Current validation commands:

    pytest
    ruff check .

Expected result:

    pytest: tests pass
    ruff: all checks passed

## Security Notes

No passwords, API keys, tokens, private SSH keys, or local secrets should be committed to the repository.

The repository includes `.env.example` for documenting environment variables, but real `.env` files are ignored by Git.

Project input, workspace, and output directories are ignored by Git and should be treated as controlled runtime data areas.

## Phase 0 Decisions

### Use a VirtualBox VM instead of WSL for this project

Reason: the project benefits from a clean, reproducible Linux server environment that can be demonstrated independently from existing WSL projects.

Rejected alternative: using an existing WSL distribution directly.

Impact: slightly more setup work, but better isolation and a clearer portfolio story.

### Use NAT with SSH port forwarding

Reason: NAT is simple, stable, and sufficient for local development.

Rejected alternative: bridged networking.

Impact: SSH access is routed through a host loopback port instead of exposing the VM directly on the local network.

### Use Ubuntu Server without a GUI

Reason: the application is backend-oriented and will run through SSH, Docker, and VS Code Remote SSH.

Rejected alternative: Ubuntu Desktop.

Impact: lower resource usage and closer alignment with server deployment practices.

### Use Docker from the official Docker repository

Reason: it provides the current Docker Engine and Docker Compose plugin versions.

Rejected alternative: Ubuntu's `docker.io` package.

Impact: installation requires adding the Docker repository, but gives a production-relevant Docker setup.

### Use a `src/` Python layout

Reason: it avoids accidental imports from the repository root and reflects common Python packaging practice.

Rejected alternative: putting the package directly in the repository root.

Impact: the project must be installed with `python -m pip install -e .` inside the virtual environment.

### Use GitHub no-reply email for commits

Reason: this avoids exposing a personal email address in public commit metadata.

Rejected alternative: using a personal email address in Git commits.

Impact: commits still remain associated with the GitHub account while reducing unnecessary public exposure.

## Phase 0 Completion Criteria

Phase 0 is considered complete when:

- the VM boots successfully;
- SSH from Windows works;
- VS Code Remote SSH opens the project folder;
- Git and GitHub are configured;
- Docker runs without `sudo`;
- the Python virtual environment works;
- tests pass;
- Ruff passes;
- documentation is committed and pushed to GitHub.