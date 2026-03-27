FROM opensuse/tumbleweed

ENV WORK_ENV=/user/local/devenv
ENV SYSTEM_FILES="${WORK_ENV}/system"
ENV SYSTEM_CONFIGS="${SYSTEM_FILES}/.config"
ENV XDG_CONFIG_HOME="${SYSTEM_CONFIGS}"

WORKDIR /home
COPY scripts/system/ $SYSTEM_FILES

RUN zypper refresh && zypper dup -y && zypper install -y glibc \
    gawk \
    git \
    lazygit \
    fzf \
    curl \
    fd \
    wget \
    neovim \
    ripgrep \
    cargo \
    nodejs \
    npm \
    openssh \
    python313 \
    python3-devel

RUN rm -rf ~/.local/share/nvim \
    && rm -rf ~/.local/state/nvim \
    && rm -rf ~/.cache/nvim \
    && mkdir /root/.ssh

RUN cargo install tree-sitter-cli \
    && curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net |sh \
    && mv tectonic $SYSTEM_FILES

RUN zypper --non-interactive --gpg-auto-import-keys addrepo https://download.opensuse.org/repositories/graphics/openSUSE_Tumbleweed/graphics.repo \
    && zypper --non-interactive --gpg-auto-import-keys refresh \
    && zypper --non-interactive --gpg-auto-import-keys install -y ImageMagick

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && source $HOME/.local/bin/env

RUN python3 -m venv "${SYSTEM_FILES}/pyenv"

ENV PATH="${SYSTEM_FILES}:${SYSTEM_FILES}/pyenv/bin:${PATH}"

CMD ["bash"]
