const {produceTrueListingMessage} = require("../../../streams/kafka")

module.exports = function() {
    let operations = {
        POST,
    }

    async function POST(req,res,next){
        let vehicle = {
            vin: req.body.vin,
            header: req.body.header,
            trim: req.body.trim,
            price: req.body.price,
            location: req.body.location,
            mileage: req.body.mileage,
            exterior_color: req.body.exterior_color,
            interior_color: req.body.interior_color,
            fuel_type: req.body.fuel_type,
            mpg: req.body.mpg,
            transmission: req.body.transmission,
            drivetrain: req.body.drivetrain,
            engine: req.body.engine,
        }
        const vehicleToStream = await produceTrueListingMessage("create-vehicle", vehicle)
        //load in microservice here
        res.status(201).json(read);
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