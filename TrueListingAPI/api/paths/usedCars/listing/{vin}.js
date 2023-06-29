
module.exports = function() {
    let operations = {
        GET,
    }

    async function GET(req,res,next){
        let vin = req.params.vin
        //Load in microservice here
        res.status(200).json(vehicleData);
    }
    
    GET.apiDoc = {
        summary: "gets vehicle listing",
        description: "gets vehicle listing based on vin",
        operationId: "get-vin-vehicle",
        responses: {
            200: {
                description: "get",
                content: {
                    "application/json":{
                        "schema": {
                            $ref: "#/components/schemas/vehicle"
                        }
                    }
                }
            }
        }
    }
    return operations;
}