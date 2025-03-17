# Weather API Demo

This project is a simple Weather API that fetches weather information for a given city from a BigQuery dataset. It provides two main endpoints:

-   `/meteocris`: Returns detailed weather information (city name, clouds, main weather data, weather descriptions).
-   `/temperature`: Returns the temperature for a given city.

## Features

-   **Data Source:** Utilizes Google BigQuery as the data source for weather information.
-   **City-Based Queries:** Retrieves weather data based on the city name provided in the request.
-   **Error Handling:** Includes robust error handling for missing city names, cities not found in the dataset, and internal server errors.
-   **Clean Input:** Cleans city name inputs, removing non-alphabetic characters to ensure accuracy
-   **Containerized:** Designed to be deployed as a containerized application.
-   **Cloud Deployment:**  Configured for deployment on Google Cloud using Cloud Run and Cloud Deploy.
- **Environment Variables** uses two environment variables `PROJECT_ID` and `DATASET_ID`
- **Two API Endpoint**: `/meteocris` and `/temperature`

## Getting Started

### Prerequisites

-   **Google Cloud Account:** You need a Google Cloud account with a project set up.
-   **Google Cloud SDK:** Ensure you have the Google Cloud SDK installed and configured.
-   **BigQuery Dataset:** A BigQuery dataset with a table named `forecasting_history` containing the necessary weather data (city name, temperature, etc.).
-   **Python 3:** Python 3.x installed on your development machine.
-   **Docker:** Docker installed and running for building container images.
- **Artifact Registry**: An Artifact Registry repository to store your container image
- **Cloud Deploy** is configured.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Set up Environment Variables:**
    ```bash
    export PROJECT_ID="your-project-id"
    export DATASET_ID="your-dataset-id"
    ```
   Remember replace `your-project-id` and `your-dataset-id` with your proper values.

3.  **Install Python Dependencies:**

    Navigate to the `api-weather` folder and install the dependencies:

    ```bash
    cd api-weather
    pip install -r requirements.txt
    ```

### Running Locally

1.  **Run the Flask Application:**

    ```bash
    python main.py
    ```

    This will start the Flask development server. By default, it runs on `http://0.0.0.0:8080/`.

2.  **Test the API:**
   For `/meteocris`:
    ```bash
    curl "http://0.0.0.0:8080/meteocris?cityname=London"
    ```
   For `/temperature`:
    ```bash
    curl "http://0.0.0.0:8080/temperature?cityname=London"
    ```
   Replace `"London"` with any city in your database.

### Building and Deploying with Cloud Build and Cloud Deploy

1.  **Configure Project and Region:**

    ```bash
    export PROJECT_ID=$(gcloud config get-value project)
    export REGION=europe-west1
    ```
   Change `europe-west1` with your desired region.

2.  **Run the setup Script:**

    Navigate to the project root directory and execute the `setup.sh` script:

    ```bash
    ./setup.sh
    ```

    This script does the following:

    -   Enables necessary Google Cloud services.
    -   Creates Cloud Deploy and Artifact Registry repositories.
    -   Submits a Cloud Build job to build the Docker image.
    - Creates a release in Cloud Deploy
    - Promotes to pre-env the release.

3.  **Skaffold**
    - This application also can be deploy with skaffold. For that you need have skaffold install in your environment.
    - Run `skaffold dev -p dev` for deploy in dev environment.
    - Run `skaffold dev -p pre` for deploy in pre environment.
    - Run `skaffold dev -p prod` for deploy in prod environment.

## API Endpoints

### `/meteocris`

-   **Method:** `GET`
-   **Parameters:**
    -   `cityname` (string, required): The name of the city.
-   **Response:**
    -   **Success (200 OK):** Returns a JSON string with the weather information.
    -   **City Not Found (404 Not Found):** Returns the message "City not found".
    - **Internal error(500):** Returns the message "An internal error occurred =O"
    -   **Example**
        ```json
        [{"city":{"coord":{"lon":-0.1257,"lat":51.5085},"country":"GB","id":2643743,"name":"London","population":1000000},"clouds":{"all":99},"main":{"feels_like":289.94,"grnd_level":1018,"humidity":81,"pressure":1019,"sea_level":1019,"temp":292.5,"temp_kf":0,"temp_max":292.5,"temp_min":292.5},"weather":[{"description":"overcast clouds","icon":"04n","id":804,"main":"Clouds"}],"wind":{"deg":203,"gust":3.98,"speed":2.78}}]
        ```

### `/temperature`

-   **Method:** `GET`
-   **Parameters:**
    -   `cityname` (string, required): The name of the city.
-   **Response:**
    -   **Success (200 OK):** Returns the temperature as a string (in Kelvin).
    -   **City Name Required (400 Bad Request):** Returns the message "City name is required".
    -   **City Not Found (404 Not Found):** Returns the message "City not found".
    -   **Internal Error (500 Internal Server Error):** Returns the message "An internal error occurred".
    - **Example**
        ```bash
        292.5
        ```

## Updating the Temperature Unit

Currently, the `/temperature` endpoint returns the temperature in Kelvin. To change this to Celsius:

1.  **Modify `main.py`:**

    -   In the `get_temperature` function, add a line to convert the temperature from Kelvin to Celsius:

    ```python
    # ... inside the try block, after getting the temperature:
    temperature_celsius = temperature - 273.15
    return str(temperature_celsius)
    ```
    
2. Update your image container, and deploy the new version.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the [Apache 2.0 License](LICENSE).

## Contact
xstabel