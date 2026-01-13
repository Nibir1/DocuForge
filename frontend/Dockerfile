# Development Dockerfile
FROM node:20-slim

WORKDIR /app

# Copy package files first for caching
COPY package*.json ./

RUN npm install

# Copy the rest of the code
COPY . .

# Expose Vite's default port
EXPOSE 5173

# Host flag is required to expose outside container
CMD ["npm", "run", "dev", "--", "--host"]