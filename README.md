# EDOL Monorepo

This is the EDOL monorepo. The source code is mainly Python. [pyproject.toml](pyproject.toml) has details about some dependencies.

## Getting Started

This project uses [devbox](https://github.com/jetify-com/devbox) to manage its development environment. Devbox is an alternative to devcontainers that doesn't require Docker.

Install devbox:
```sh
curl -fsSL https://get.jetpack.io/devbox | bash
```

Start the devbox shell:
```sh 
devbox shell
```

Run a script in the devbox environment:
```sh
devbox run <script>
```

For scripts and packages see [devbox.json](devbox.json)