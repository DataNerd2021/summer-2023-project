const kafka = require("./streams/kafka.js");
const { BigQuery } = require('@google-cloud/bigquery');

const bigquery = new BigQuery({
    projectId: 'extended-spark-381216',
    keyFilename: 'extended-spark-381216-d0e2ae70606d.json',
});

async function main() {
    const sendDataToBigQuery = async(evtMessage) => {
        var key = evtMessage.key.toString();
        var data = JSON.parse(evtMessage.value.toString());

        if(key == 'create-prediction'){
            const createPrediction = async(data) => {
                try{
                    console.log('running prediction query...................__');
                    const options = { skipInvalidRows: true, ignoreUnknownValues: true };
                    const [rows] = await bigquery.query(`
                    WITH year_encoded AS(SELECT ${data.year} AS year),
                    make_encoded AS( 
                    SELECT DISTINCT features.make 
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.make = '${data.make}'),
                    
                    model_encoded AS( 
                    SELECT DISTINCT features.model 
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.model = '${data.model}'),
                    
                    trim_encoded AS( 
                    SELECT DISTINCT features.trim
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.trim = '${data.trim}'),
                    
                    mileage_encoded AS( 
                    SELECT ${data.mileage} AS mileage),
                    
                    engine_encoded AS( 
                    SELECT DISTINCT features.engine
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.engine = '${data.engine}'),
                    
                    fuel_type_encoded AS( 
                    SELECT DISTINCT features.fuel_type
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.fuel_type = '${data.fuel}'),
                    
                    transmission_encoded AS( 
                    SELECT DISTINCT features.transmission
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.transmission = '${data.transmission}'
                    LIMIT 1),
                    
                    drivetrain_encoded AS( 
                    SELECT DISTINCT features.drivetrain
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.drivetrain = '${data.drivetrain}'
                    LIMIT 1),
                    
                    exterior_color_encoded AS( 
                    SELECT DISTINCT features.exterior_color
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.exterior_color = '${data.exteriorColor}'),
                    
                    interior_color_encoded AS( 
                    SELECT DISTINCT features.interior_color
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.interior_color = '${data.interiorColor}'),
                    
                    city_encoded AS( 
                    SELECT DISTINCT features.city
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.city = '${data.city}'),
                    
                    state_encoded AS( 
                    SELECT DISTINCT features.state
                    FROM 'regression_tree_features.preprocessed_features' AS features
                    JOIN 'training_data.filtered_training_data' AS training ON features.vin = training.vin
                    WHERE training.state = '${data.state}'),
                    
                    user_inputs AS(
                    SELECT * FROM year_encoded
                    CROSS JOIN
                    make_encoded
                    CROSS JOIN
                    model_encoded
                    CROSS JOIN
                    trim_encoded
                    CROSS JOIN
                    mileage_encoded
                    CROSS JOIN 
                    engine_encoded
                    CROSS JOIN
                    fuel_type_encoded
                    CROSS JOIN
                    transmission_encoded
                    CROSS JOIN
                    drivetrain_encoded
                    CROSS JOIN
                    exterior_color_encoded
                    CROSS JOIN 
                    interior_color_encoded
                    CROSS JOIN
                    city_encoded
                    CROSS JOIN
                    state_encoded),
                    
                    predictions AS(
                    SELECT *
                    FROM ML.PREDICT(MODEL 'used_car_model.price_prediction_model', (SELECT * FROM user_inputs)))
                    
                    SELECT predicted_price FROM predictions
                    
                    `,options);
                    console.log("price:");
                    rows.forEach(element => {
                        console.log(element.predicted_price)
                    });
                }catch (error) {
                    console.error('Error running query data into BigQuery:', error);
                    throw error;
                }
            };
        }
    }

    kafka.postMicroConsumer(sendDataToBigQuery);
}

main().catch(console.error);