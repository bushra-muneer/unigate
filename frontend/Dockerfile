FROM node:23.4-bookworm-slim

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy only package files first (for layer caching)
COPY package.json pnpm-lock.yaml ./

# Install deps
RUN pnpm install

# Now copy the rest of the code
COPY . .

# Start dev server
CMD ["pnpm", "dev"]
