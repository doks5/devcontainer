# Devcontainer

Setup for spinning a dev container, that allows for creating an isolated coding environment.
The setup targets python and web development.

## Installation

1. Make sure you have [Podman](https://podman.io/) or [Docker](https://www.docker.com/) installed.

2. Clone the repository with

```bash
git clone https://github.com/doks5/devcontainer.git
```

3. cd into the directory

```bash
cd devcontainer
```

4. (Optional) If using SSH and/or GPG keys, make sure the key files are placed in
   the `scripts/system/git/assets` folder and that the appropriate fields in the config
   file `scripts/system/git/config.json` are filled in.

5. Build the container image

```bash
podman build -t <name-tag-for-the-image> -f Dockerfile
```

6. Start the container either as an isolated environment

```bash
podman run --name <name-for-the-container> -it <name-of-the-built-container-image>
```

or start it with a volume attached

```bash
podman run --name <container-name> -v <path/on/local/filesystem>:/home -it <image-name>
```

7. (Optional) If you have specified ssh and/or gpg keys, and other git-related
   configuration, once inside the container execute

```bash
python /user/local/devenv/system/git/git_setup.py
```

8. If you exit the container, it stops. To restart it, type

```bash
podman start -ai <container-name>
```
