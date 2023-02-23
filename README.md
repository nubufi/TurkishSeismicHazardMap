# Turkish Seismic Hazard Map API
This API allows users to get PGA, PGV, SS, and S1 values from the Turkish seismic hazard map at corresponding latitude and longitude coordinates.

## Getting Started
To use this API, you will need to have Docker installed on your local machine. You can download and install Docker from the official website.

To build the Docker image for the API, navigate to the directory where the code is located and run the following command:

`docker build -t seismic-hazard-api .
`

This will build the Docker image and tag it with the name seismic-hazard-api.

To start the Docker container and run the API, run the following command:

`docker run -p 8000:8000 seismic-hazard-api`

This will start the container and map port 8000 on your local machine to port 8000 in the container. You can access the API by visiting http://localhost:8000 in your web browser.

## Usage
To get the seismic hazard values at a specific latitude and longitude coordinate, send a GET request to the /seismic_hazard endpoint with the latitude and longitude parameters in the query string. The API will return a JSON object with the corresponding PGA, PGV, SS, and S1 values.

## Acknowledgements
This API was built using the seismic hazard map data provided by the Disaster and Emergency Management Authority of Turkey (AFAD).
