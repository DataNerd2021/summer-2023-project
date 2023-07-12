const {execSync} = require('child_process');
const path = require('path');


function getListingData(){
    console.log(__dirname);
    const scriptPath = path.join(__dirname, '..', '..', 'GetTrueListingMicroservice', 'GetCarData.py');
    const result = execSync(`python ${scriptPath}`).toString();
    const data = JSON.parse(result);
    return data;
}


module.exports = function() {
    let operations = {
        GET,
    }

    async function GET(req,res,next){
        const ListingData = getListingData()
        res.status(200).json(ListingData);
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