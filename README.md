# Devcontainer

Setup for spinning a dev container, that allows for creating an isolated coding environment.
The setup targets python and web development.

## Instalation

1. Make sure you have [Podman](https://podman.io/)  
   or [Docker](https://www.docker.com/) installed.

2. Clone the repository with

```bash
git clone https://github.com/doks5/devcontainer.git
```

3. cd into the directory

```bash
cd devcontainer
```

4. Build the container image

```bash
podman build -t <name-tag-for-the-image> -f Dockerfile
```

5. Start the container either as an isolated environment

```bash
podman run --name <name-for-the-container> -it <name-of-the-built-container-image>
```

or start it with a volume attached

```bash
podman run -v <path/on/local/filesystem>:/user/local/devenv -it <image-name> --name <container-name>
```
