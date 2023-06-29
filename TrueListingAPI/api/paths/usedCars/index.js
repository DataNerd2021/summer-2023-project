
module.exports = function() {
    let operations = {
        GET,
    }

    async function GET(req,res,next){
        //load in microservice
        res.status(200).json(object);
    }

    GET.apiDoc = {
        summary: "Gets all vehicles in TrueListing database information",
        description: "Retrieve all vehicles information that exists",
        operationId: "get-truelistings",
        responses: {
            200: {
                description: "OK",
                content: {
                    "application/json": {
                        schema: {
                            type: "array",
                            items: {
                                $ref: '#/components/schemas/vehicles'
                            }
                        }
                    }
                }
            }
        }
    }
    return operations;
}