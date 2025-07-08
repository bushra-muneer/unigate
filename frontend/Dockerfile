FROM node:23.4-bookworm-slim

WORKDIR /app

# Install pnpm directly to avoid Corepack issues
RUN npm install -g pnpm

COPY ./ /app/

# Optional: speed up installs with a cache mount
RUN --mount=type=cache,id=pnpm,target=/root/.pnpm-store pnpm install --frozen-lockfile

CMD ["pnpm", "run", "dev"]

