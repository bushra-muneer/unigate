
FROM node:23.4-bookworm-slim

WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


ENV SHELL=/bin/bash

RUN curl -fsSL https://get.pnpm.io/install.sh | bash -

# Add pnpm to PATH
ENV PATH="/root/.local/share/pnpm:$PATH"

# Optional: prepare pnpm store for caching
ENV PNPM_HOME=/pnpm
RUN mkdir -p /pnpm/store

COPY ./ /app/

RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

CMD ["pnpm", "run", "dev"]