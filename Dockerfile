FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY backend/package*.json ./backend/
COPY frontend/package*.json ./frontend/
COPY package.json .

# Install dependencies
RUN cd backend && npm install --only=production
RUN cd frontend && npm install --only=production

# Copy source code
COPY backend ./backend
COPY frontend ./frontend

# Expose port
EXPOSE 3001

# Set working directory to backend
WORKDIR /app/backend

# Start command
CMD ["npm", "start"]
