FROM node:16

ENV api_port=3091
ENV apihost=localhost


WORKDIR /apis/truelisting/api

COPY package.json /

# RUN npm install

COPY .. /

EXPOSE 3091

CMD ["npm", "start"]