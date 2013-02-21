# Greenlight Server

Greenlight Server is a RESTful Django API that allows any client system to interface with a given Open 311 API.


## Documentation

 - `GET /services/`
 - `GET /requests/`
 - `POST /requests/`
 - `GET /requests/<id>`
 

## Configuration

The only required configuration parameter is `OPEN311_API_KEY`, which is taken from the local environment and can be set as follows:

	export OPEN311_API_KEY="your Open311 API key"
	
	