const kafka = require("./streams/kafka.js");
const { BigQuery } = require('@google-cloud/bigquery');

const bigquery = new BigQuery({
    projectId: 'extended-spark-381216',
    keyFilename: '/service-account-key.json',
});

async function main() {
    const sendDataToBigQuery = async(evtMessage) => {
        var key = evtMessage.key.toString();
        data = JSON.parse(evtMessage.value.toString());

        if(key == 'create-prediction'){
            const createPrediction = async(data) => {
                try{
                    const options = { skipInvalidRows: true, ignoreUnknownValues: true };
                    const [apiResponse] = await bigquery.dataset(datasetId).table(tableId).insert(dataToInsert, options);
                    console.log('Data inserted into BigQuery:', apiResponse);
                }catch (error) {
                    console.error('Error inserting data into BigQuery:', error);
                    throw error;
                }
            };
        }
    }

    kafka.postMicroConsumer(sendDataToBigQuery);
}

main().catch(console.error);