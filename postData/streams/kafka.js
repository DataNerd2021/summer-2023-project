const { Kafka } = require('kafkajs');

const brokerAddress = "pricebroker:29092";

const kafka = new Kafka({   // We made a kafka client here, but didn't tell how to connect
    brokers: [brokerAddress],
    clientId: "postMicro-consumer",
})

const consumer = kafka.consumer({groupId: "postMicro-consumer"})

exports.postMicroConsumer = async(handler) => {
    await consumer.connect();
    await consumer.subscribe({topics:["pricing"]});
    console.log("Starting consuming --------")
    consumer.run({
        eachMessage: async({topic, partition, message, heartbeat, pause}) => handler(message)
    })
    return consumer;

}