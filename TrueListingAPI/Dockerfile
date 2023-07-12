FROM node:16

# Set environment variables
ENV api_port=3091
ENV api_host=localhost

WORKDIR /apis/truelisting/api

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY GetCarData.py ./GetTrueListingMicroservice/

EXPOSE 3091

CMD ["npm", "start"]
