# Dockerfile.dev
FROM node:18-alpine

# System dependencies for better compatibility
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy full source for dev work
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1
EXPOSE 3000

# Start dev server
CMD ["npm", "run", "dev"]
