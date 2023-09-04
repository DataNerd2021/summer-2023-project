const apiDoc={
    openapi: "3.0.1",
    info: {
        title: "TrueListingAPI",
        description: "This API provides information pertaining to Vehice listings",
        version: "1.0.0"
    },
    paths: {},
    components: {
        parameters: {
            vin: {
                name: "vin",
                in: "path",
                schema: {
                    $ref: "#/components/schemas/vin"
                }
            },
            
        },
        schemas: {
            vin: {
                type: "integer"
            },
            vehicle: {
                type: "object",
                properties: {
                    vin: {
                        $ref: "#/components/schemas/vin"
                    },
                    header: {
                        title: "header",
                        type: "string",
                        description: "the model of vehicle"
                    },
                    trim: {
                        title: "trim",
                        type: "string",
                        description: "Defines the trim of vehicle"
                    },
                    price: {
                        title: "price",
                        type: "string",
                        maxLength: 18,
                        description: "price of the vehicle"
                    },
                    location: {
                        title: "location",
                        type: "string",
                        description: "current location vehicle is listed at"
                    },
                    mileage: {
                        title: "mileage",
                        type: "string",
                        description: "current mileage of vehicle"
                    },
                    exterior_color: {
                        title: "exterior_color",
                        type: "string",
                        description: "color of vehicle"
                    },
                    interior_color: {
                        title: "interior_color",
                        type: "string",
                        description: "color of interior of vehicle"
                    },
                    fuel_type: {
                        title: "fuel_type",
                        type: "string",
                        description: "fuel type of vehicle"
                    },
                    mpg: {
                        title: "mpg",
                        type: "string",
                        description: "mpg of vehicle"
                    },
                    transmission: {
                        title: "transmission",
                        type: "string",
                        description: "defines the transmission of vehicle"
                    },
                    drivetrain: {
                        title: "drivetrain",
                        type: "string",
                        description: "drivetrain of vehicle"
                    },
                    engine: {
                        title: "engine",
                        type: "string",
                        description: "engine of vehicle"
                    },
                }
            },
            vehicles:{
                type: "array"
            },
            
        },
        securitySchemes: {
            userAuth: {
                type: "http",
                scheme: "bearer",
                bearerFormat: "JWT"
            }
        },
    },
    
}

module.exports = apiDoc;


