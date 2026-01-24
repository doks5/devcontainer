"""
This script manages the git credentials and certificates
setup needed to be able to clone repositories and push
changes to repositories.

Usage:
   To use the script just run `python <path/to/git_setup.py>`
"""

import os
import re
import sys
import subprocess
import shlex
import shutil
import json
from pathlib import Path

dir_path = Path(__file__).parent
assets = dir_path / "assets"
configuration = dir_path / "config.json"

# Check for the existance of the configuration elements
if assets.exists() and not assets.is_dir():
    print("Missing `assets` folder. Terminating script")
    sys.exit(1)

if configuration.exists() and not configuration.is_file():
    print("Missing configuration file. Terminating script")
    sys.exit(1)


# Read git configuration file
with open(configuration, mode="r", encoding="utf-8") as read_conf:
    git_config = json.load(read_conf)


# Execute a shell command when setting up git.
def run_command(command: list, additional_args: dict | None = None) -> str:
    if additional_args:
        process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **additional_args
        )
    else:
        process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

    if process.returncode != 0:
        raise Exception(f"Git configuration failed with: {process.stdout.decode()}")

    return process.stdout.decode().strip()


#####
# Configure git user identity.
#####
if "name" in git_config:
    cmd = shlex.split(f'git config --global user.name "{git_config.get("name")}"')
    run_command(cmd)

# Configure user's email
if "email" in git_config:
    cmd = shlex.split(f'git config --global user.email "{git_config.get("email")}"')
    run_command(cmd)

# Configure user's editor
if "editor" in git_config:
    cmd = shlex.split(f'git config --global core.editor "{git_config.get("editor")}"')
    run_command(cmd)


#####
# Configure git user ssh key.
#####
def prepare_ssh_agent() -> None:
    cmd = shlex.split('eval "$(ssh-agent -s)"')
    run_command(cmd, {"shell": True})


def add_ssh_key(key_path: Path) -> None:
    cmd = shlex.split(f"ssh-add {key_path}")
    run_command(cmd)


def remove_ssh_key(ssh_file: Path) -> None:
    try:
        os.remove(ssh_file)
        print(f"{ssh_file} ssh file deleted.")
    except PermissionError:
        print(f"WARNING || Cannot delete file {ssh_file}. Permission denied.")


def set_up_ssh() -> None:
    home = Path().home()
    ssh_dir = home / ".ssh"
    ssh_file = git_config["ssh-file"]
    ssh_file_path = assets / ssh_file

    target = ssh_dir / ssh_file
    if target.exists():
        print(
            f"There is already a file with the name > {ssh_file} < ",
            f"in the > {ssh_dir} < directory.",
        )
        return

    prepare_ssh_agent()
    shutil.copy2(ssh_file_path, ssh_dir)
    add_ssh_key(target)
    remove_ssh_key(ssh_file_path)


if "ssh-file" in git_config:
    ssh_conf = assets / git_config["ssh-file"]
    if ssh_conf.exists() and ssh_conf.is_file():
        set_up_ssh()
    else:
        print("No ssh file specified. Skipping this step.")


#####
# Import gpg key for signing commits.
#####
gpg_files = []


def remove_keys(gpg_key_files: list[Path]) -> None:
    if gpg_key_files:
        for file in gpg_key_files:
            try:
                file.unlink()
            except FileNotFoundError:
                print(f"File > {file.name} < does not exist.")


def import_gpg_key(key: Path) -> None:
    cmd = shlex.split(f"gpg --import {key}")
    run_command(cmd)


if "gpg-private" in git_config:
    gpg_private = assets / git_config["gpg-private"]
    if gpg_private.exists() and gpg_private.is_file():
        import_gpg_key(gpg_private)
        gpg_files.append(gpg_private)
    else:
        print("No GPG key specified. Exiting script...")
        sys.exit(0)


if "gpg-public" in git_config:
    gpg_public = assets / git_config["gpg-public"]
    if gpg_public.exists() and gpg_public.is_file():
        import_gpg_key(gpg_public)
        gpg_files.append(gpg_public)


if "gpg-ownership" in git_config:
    gpg_ownership = assets / git_config["gpg-ownership"]
    if gpg_ownership.exists() and gpg_ownership.is_file():
        ownership_cmd = shlex.split(f"gpg --import-ownertrust {gpg_ownership}")
        run_command(ownership_cmd)
        gpg_files.append(gpg_ownership)


# Remove the gpg keys after they are imported.
if "gpg-remove-keys" in git_config and git_config.get("gpg-remove-keys"):
    remove_keys(gpg_files)


#####
# Configure gpg signing key for git
#####
def get_gpg_key_id() -> str:
    cmd = shlex.split("gpg --list-secret-keys --keyid-format=long")

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Matches lines like: sec  rsa4096/ABCDEF1234567890 2026-01-01 [SC]
        match = re.search(r"/([0-9A-F]{16})\s+\d{4}-\d{2}-\d{2}", res.stdout)
        if match:
            return match.group(1)
        raise ValueError("No secret key found")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"GPG list key failed: {e.stderr}")


def set_up_git_gpg_signing_key(key_id: str) -> None:
    cmd = shlex.split(f"git config --global user.signingkey {key_id}")
    run_command(cmd)


key = get_gpg_key_id()
set_up_git_gpg_signing_key(key)
