FROM node:16

# Set environment variables
ENV api_port=3091
ENV api_host=localhost

WORKDIR /apis/truelisting/api
ENV GOOGLE_APPLICATION_CREDENTIALS=/apis/truelisting/api/extended-spark-381216-d0e2ae70606d.json


COPY package.json .
COPY package-lock.json .

RUN npm install
COPY . .

EXPOSE 3091

CMD ["npm", "start"]
