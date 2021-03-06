# LX Classroom
A project for conducting online courses implemented using the Django and DRF frameworks.
## Installation
1. Clone the repository.  
2. Install the required dependencies.  
3. Create your .env file and specify secret key.
```python
SECRET_KEY = '...'
```
## Dependencies
* Django==4.0
* djangorestframework==3.13.1
* djangorestframework-simplejwt==5.0.0
* drf-spectacular==0.21.1
* drf-spectacular-sidecar==2021.12.13
* python-decouple==3.5
## Features
* All application logic is available through the API.
* Implemented authentication using tokens.
* Documentation in accordance with OpenAPI 3.0 available through 'Swagger-UI' and 'Redoc' interfaces.