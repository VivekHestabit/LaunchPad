FROM node:20-alpine


RUN apk add --no-cache curl 

WORKDIR /app

COPY package*.json ./
RUN npm install --only==production

COPY . .

USER node

EXPOSE 5000

CMD [ "node", "index.js" ]