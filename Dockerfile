FROM opensuse/tumbleweed

ENV WORK_ENV=/user/local/devenv
ENV SYSTEM_FILES="${WORK_ENV}/system"
ENV SYSTEM_CONFIGS="${SYSTEM_FILES}/.config"
ENV XDG_CONFIG_HOME="${SYSTEM_CONFIGS}"

WORKDIR $WORK_ENV
COPY scripts/system /user/local/devenv/

RUN zypper dup -y && zypper install -y git \
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
    python3-devel

RUN rm -rf "${SYSTEM_CONFIGS}/nvim" \
    && rm -rf ~/.local/share/nvim \
    && rm -rf ~/.local/state/nvim \
    && rm -rf ~/.cache/nvim

RUN mkdir $SYSTEM_FILES \
    && cargo install tree-sitter-cli \
    && git clone https://github.com/LazyVim/starter "${SYSTEM_CONFIGS}/nvim" \
    && rm -rf "${SYSTEM_CONFIGS}/nvim/.git" \
    && curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net |sh \
    && mv tectonic $SYSTEM_FILES

RUN zypper --non-interactive --gpg-auto-import-keys addrepo https://download.opensuse.org/repositories/graphics/openSUSE_Tumbleweed/graphics.repo \
    && zypper --non-interactive --gpg-auto-import-keys refresh \
    && zypper --non-interactive --gpg-auto-import-keys install -y ImageMagick

RUN python3 -m venv "${SYSTEM_FILES}/pyenv"

ENV PATH="${SYSTEM_FILES}:${SYSTEM_FILES}/pyenv/bin:${PATH}"

RUN python /user/local/devenv/system/git/git_setup.py

CMD ["bash"]
