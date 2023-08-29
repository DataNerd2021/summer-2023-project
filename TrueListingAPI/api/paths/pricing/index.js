const {produceTrueListingMessage} = require("../../../streams/kafka")

module.exports = function() {
    let operations = {
        POST,
    }

    async function POST(req,res,next){
        let vehicle = {
            year: req.body.year,
            make: req.body.make,
            model: req.body.model,
            trim: req.body.trim,
            mileage: req.body.mileage,
            engine: req.body.engine,
            fuelType: req.body.fuelType,
            transmission: req.body.transmission,
            drivetrain: req.body.drivetrain,
            exteriorColor: req.body.exteriorColor,
            interiorColor: req.body.interiorColor,
            state: req.body.state,
            city: req.body.city,
        }
        const vehicleToStream = await produceTrueListingMessage("create-vehicle", vehicle)
        res.status(201);
    }
    
    POST.apiDoc = {
        summary: "Create a new price listing estimation",
        description: "Creates a new vehicle estimation based on parameters",
        operationId: "post-vehicle",
        responses: {
            201: {
                description: "Created",
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