const { BigQuery } = require('@google-cloud/bigquery');

const bigquery = new BigQuery({
    projectId: 'extended-spark-381216',
    keyFilename: process.env.GOOGLE_APPLICATION_CREDENTIALS,
});

async function fetchDataFromBigQuery() {
    const query = ' SELECT * FROM `extended-spark-381216.training_data.clean_training_data` LIMIT 5';
    try {
        const [rows] = await bigquery.query(query);
        console.log('Data retrieved from BigQuery:', rows);
        return rows;
    } catch (error) {
        console.error('Error fetching data from BigQuery:', error);
        throw error;
    }
}

module.exports = { fetchDataFromBigQuery, }