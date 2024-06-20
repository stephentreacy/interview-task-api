# Weather Sensor App

## Overview
The Weather Sensor App is a REST API application developed with FastAPI and Python. It is designed to collect and query weather sensor data from various sensors.

## Design Decisions
### SQLite Database
SQLite was chosen as the database for this project due to its simplicity and ease of setup. It allows for a lightweight, file-based database solution that is ideal for development and testing phases.

### Testing Approach
The testing strategy employed in parts of this project leans towards integration tests rather than pure unit tests. This approach allows for a more comprehensive validation of the application's functionality by utilizing an in-memory SQLite database for testing.

## Running the Application

### Prerequisites
- Docker or 
- Python 3.12

### Steps
1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/stephentreacy/interview-task-api.git
   ```
2. Navigate to the project directory.

The API can be run using Docker (recommended):

3. Build the Docker image:
   ```sh
   docker build -t weather-app .
   ```
4. Run the application:
   ```sh
   docker run -v weather_db:/usr/src/app/data --rm -p 8000:8000 weather-app
   ```
Alternatively,

3. You can set up a .venv and install the dependencies using:
   ```sh
   pip install -r requirements.txt
   ```   

4. And then run the application locally with:
   ```sh
   fastapi run
   ```   

## Using the API
Once the application is running, you can interact with the API through the Swagger UI by accessing: http://127.0.0.1:8000/docs

The Swagger UI provides a user-friendly interface to build and send requests to the API. It allows you to explore the available endpoints, try out different operations, and view the responses.

NOTES: Where enums are used selecting "--" will send "" and not leave it blank. Sending P1D will get the data for the last 1 day.



## Running the tests

### Prerequisites
- Docker or 
- Python 3.12+

### Steps
1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/stephentreacy/interview-task-api.git
   ```
2. Navigate to the project directory.

The tests can be run using Docker (recommended):

3. Build the Docker image:
   ```sh
   docker build -f Dockerfile.test -t weather-app-test .
   ```
4. Run the application:
   ```sh
   docker run --rm weather-app-test
   ```
Alternatively, without docker: 

3. You can set up a .venv and install the dependencies using:
   ```sh
   pip install -r requirements.txt -r requirements-dev.txt
   ```   

4. Set the DATABASE_URL env variable: 
   ```sh
   export DATABASE_URL=sqlite+aiosqlite:///:memory:
   ```   
5. And then run the tests locally with:
   ```sh
   pytest --cov=app
   ```   
This will also provide a coverage report. To see an HTML coverage report, click [here](https://drive.google.com/drive/folders/1-cBVjn6vx-jvo5hs8dJ53LPwHWNmqcsx).