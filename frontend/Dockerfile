FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Invece di build, usa dev
CMD ["npm", "run", "dev"]