const { Kafka } = require('kafkajs');

const brokerAddress = "broker1:29092";
const truelistingTopic = "truelisting";

const kafka = new Kafka({   // We made a kafka client here, but didn't tell how to connect
    brokers: [brokerAddress],
    clientId: "truelisting-api-producer",
})

const producer = kafka.producer();

exports.produceTrueListingMessage = async(truelistingEvent, data) =>{
    const connect = await producer.connect();
    const producerData = await producer.send({
        topic: truelistingTopic,
        messages: [
            {
                key: truelistingEvent,
                value: JSON.stringify(data)
            }
        ]
    })
}