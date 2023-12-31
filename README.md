# fetch_data
## Data Flow

This script defines a flow using Prefect to fetch data from an external API, process it using Pandas, and publish the processed data as a table artifact.

## Requirements

- Python 3
- Prefect 2
- Requests
- Pandas

## Usage

1. Install the required dependencies by running `pip install prefect requests pandas`.
2. Docker engine installed and running.

The script defines a flow named `data_flow` that takes a `url` parameter to fetch data from an external API. The flow consists of three tasks:

1. `fetch_data`: This task sends a GET request to the specified URL using the `requests` library and returns the JSON data as a list of dictionaries.
2. `process_data`: This task takes the fetched data as input, creates a Pandas DataFrame, filters out specific fields, and returns the processed DataFrame.
3. `publish_data`: This task takes the processed DataFrame as input and publishes it as a table artifact using Prefect's artifact API.

The script also defines an `error_checking` decorator function that wraps each task function to catch any exceptions that may occur during execution. If an exception is caught, it is logged and published as a markdown artifact with a key based on the task name.

The flow can be run by calling its `run` method with a sample URL parameter, as shown at the end of the script.

## Deployment

To set up the deployment and flow in Prefect, follow these steps:

```prefect deployment build alara.py:data_flow -p test-work-pool -q test-work-queue -n alara-docker-deploy -ib docker-container/test-docker-block -o docker-deployment.yaml --apply```

The above command does the following:

1) Creates a deployment definition YAML file for the data_flow flow defined in the `alara.py` script. 
2) The `-p` and `-q` flags specify the work pool and work queue names, respectively. 
3) The `-n` flag specifies the name of the deployment as `alara-docker-deploy`. 
4) The `-ib` flag specifies the infrastructure block to use, in this case `docker-container/test-docker-block`.
5) The `-o` flag specifies the output file for the generated YAML file as `docker-deployment.yaml`. 
6) Finally, the `--apply` flag applies the deployment immediately after building it.

Here's an example of starting a worker according to the given example:
```prefect worker start -p 'test-work-pool'```

Run the flow with the following command:

```prefect deployment run data-flow/alara-docker-deploy --param url=https://jsonplaceholder.typicode.com/posts```
