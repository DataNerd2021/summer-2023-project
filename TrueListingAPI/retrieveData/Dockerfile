FROM node:16

WORKDIR /getData

COPY package.json /

RUN npm install

COPY . .

CMD ["node", "index.js"]