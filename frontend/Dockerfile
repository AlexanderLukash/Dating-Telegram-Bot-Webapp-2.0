# Вказуємо базовий образ
FROM node:18-alpine

# Встановлюємо залежності
RUN apk add --no-cache g++ make py3-pip libc6-compat

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл package.json і package-lock.json
COPY package*.json ./

# Встановлюємо залежності
RUN npm install 

# Копіюємо всі інші файли в робочу директорію
COPY . .

# Відкриваємо порт
EXPOSE 3000

# Запускаємо Next.js у режимі розробки
CMD ["npm", "run", "dev"]
