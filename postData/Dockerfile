FROM node:16

WORKDIR /post

COPY package.json /post


RUN npm install
COPY . .

CMD ["node", "index.js"]