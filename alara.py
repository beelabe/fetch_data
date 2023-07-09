

import requests
import pandas as pd
from prefect import flow, task, Flow, artifacts

# Define a decorator function that takes a task function and returns a wrapped function
def error_checking(func):
    # Define the wrapped function that takes the same arguments as the task function
    def wrapper(*args, **kwargs):
        try:
            # Call the original task function and return its result
            return func(*args, **kwargs)
        except Exception as e:
            # Log the exception and publish it as a markdown artifact with a key based on the task name
            print(f"Task {func.__name__} failed with error: {e}")
            artifacts.create_markdown_artifact(f"## Error in {func.__name__}\n\n{e}", key="error")
            # Re-raise the exception
            raise e
    # Return the wrapped function
    return wrapper

# Define a task to fetch data from an external API using the decorator
@task(name="fetch_data")
@error_checking
def fetch_data(url: str):
    # Use requests to send a GET request to the API
    response = requests.get(url)
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Return the JSON data as a list of dictionaries
        return response.json()
    else:
        # Raise an exception with the status code and reason
        raise Exception(f"Failed to fetch data from {url}: {response.status_code} {response.reason}")

# Define a task to process the fetched data using the decorator
@task(name="process_data")
@error_checking
def process_data(data: list):
    # Use pandas to create a DataFrame from the data
    df = pd.DataFrame(data)
    # Filter out specific fields (for example, only keep id and title columns)
    df = df[["id", "title"]]
    print(df)
    # Return the processed DataFrame
    return df

# Define a task to publish the processed data as a table artifact using the decorator
@task(name="publish_data")
@error_checking
def publish_data(data: pd.DataFrame):
    # Use prefect.artifacts.create_markdown to create a table artifact from the DataFrame
    artifacts.create_markdown_artifact(data.to_markdown(), key="processed-data")

# Define a flow to orchestrate the tasks
@flow
def data_flow(url: str):
    # Call the fetch_data task with the url parameter
    data = fetch_data(url)
    # Call the process_data task with the data output
    processed_data = process_data(data)
    # Call the publish_data task with the processed_data output
    publish_data(processed_data)

# Run the flow with a sample url parameter
if __name__ == "__main__":
    data_flow.run()
