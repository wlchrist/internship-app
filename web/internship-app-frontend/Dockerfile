# Build stage
FROM node:18-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json* ./
COPY . .

RUN npm install
RUN npm run build

# Production image
FROM node:18-alpine
WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/.next .next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

RUN npm install --production

EXPOSE 3000
CMD ["npm", "run", "start"]
