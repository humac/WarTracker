FROM node:20-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (use legacy-peer-deps for React 19 compatibility)
RUN npm ci --legacy-peer-deps

# Copy application code
COPY . .

# Clean .next folder to avoid lock issues
RUN rm -rf .next

# Remove .env file - we use rewrites instead
RUN rm -f .env

# Expose port
EXPOSE 3000

# Build and start production server
RUN npm run build

# Default command (overridden in docker-compose)
CMD ["npm", "run", "start"]
