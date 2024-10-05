# Dental Stall Scraper

The Dentalstall Scraper Tool is a web scraping utility for collecting product information from the Dentalstall website. The tool scrapes product details such as product ID, title, price, and images, and then stores this data in a local file. It also caches the product details in Redis for efficient future access and sends notifications about newly scraped and updated products via logging, email, and SMS.


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Logging](#logging)
- [Enhancements](#enhancements)

## Features

- **Scraping**: Fetch product details including ID, title, price, and images.
- **Caching**: Cache product details using Redis with a configurable expiration.
- **Logging**: Log important events such as scraping activity and notifications in a file and console.
- **Notifications**: Extendable notifications for logging, email, and SMS updates about the scraping results.
- **Storage**: Save product details into a local JSON file. Extendable implementation to use other databases.
- **Retries**: It re-tries to scrape a particular page for N times, which is configurable in `settings.py` as `dentalstall_max_retries`.

## Installation

1. **Clone the repository**:

   ```bash
   git clone git@github.com:dojutsu-user/dental-stall-scraper.git
   cd dental-stall-scraper
   ```

2. **Install dependencies using Pipenv**:

   ```bash
   pipenv install
   ```

3. **Activate the virtual environment**:

   ```bash
   pipenv shell
   ```

## Usage

1. **Set up environment variables**:

   Update `.env.dev` file in the root directory:
   
   ```bash
   APP_NAME="Dentalstall Scraper Tool"
   ENVIRONMENT="development"
   PROXY="http://your.proxy:port" # Optional
   STATIC_TOKEN="your_static_token"
   MAX_PAGE_LIMIT=10
   REDIS_HOST="localhost"
   REDIS_PORT=6379
   REDIS_DB=0
   ```

2. **Run the application**:

    Make sure that the redis is up and running. To check if redis is running, run the following in a different terminal:
    ```bash
    ❯ redis-cli ping
    ```
    Start the server

   ```bash
   uvicorn main:app --reload
   ```

3. **Access the API**:

   You can initiate the scraping process by sending a POST request to `/scrape` endpoint with the total pages to scrape. Please note that although it accepts `total_pages` as input but the number of *maximum pages* that can be scraped is configured in the `.env.dev` file.

   Example using `curl`:

   ```bash
   curl --location --request POST 'http://127.0.0.1:8000/scrape' --header 'Authorization: Bearer your-secure-token' --header 'Content-Type: application/json' --data-raw '{"total_pages": 6}'```

## Configuration


The configuration is managed via environment variables as described in the Installation section. Adjust the settings according to your environment and preferences.

## Logging

The application uses the `logging` module to log important events and errors. Logs are stored in the specified log file and also printed to the console.

## Enhancements

While the Dentalstall Scraper Tool is functional, there are several areas that can be enhanced for better performance, scalability, and usability:

### Asynchronous Scraping:

The current scraper uses a synchronous approach, which can slow down the scraping process, especially when dealing with a large number of pages or products. Switching to an asynchronous approach using libraries like aiohttp and asyncio could greatly improve performance.

### Retry and Timeout Handling:

The retry logic for scraping pages is basic. Adding more sophisticated retry mechanisms with exponential backoff, along with proper timeout handling, can make the scraper more robust.

### Distributed Scraping:

For larger-scale scraping tasks, distributing the scraping process across multiple machines or containers using tools like Celery or Redis Queue can make the system more scalable.

### Error Reporting and Monitoring:

Implementing proper error reporting with services like Sentry can help detect and debug issues in production environments. Adding monitoring capabilities could also help track system performance and health.

### Authentication Enhancements:

The API uses a static token for authentication. Enhancing it with OAuth2 or JWT-based authentication could provide a more secure way to handle access control.

### Rate Limiting and Proxy Management:

Scraping too quickly might result in being blocked by the target website. Implementing rate-limiting or rotating proxies (e.g., using a pool of IPs) can help avoid this issue.

### Unit and Integration Tests:

The project can benefit from comprehensive unit and integration tests to ensure each component (scraper, cache, notifications, etc.) works as expected. This will also help in identifying regressions when new features are added.

### Dockerization:

Containerizing the application using Docker would allow for easier deployment and scaling. A Dockerfile and docker-compose setup can streamline the process of setting up Redis, the FastAPI app, and other components in isolated containers.
