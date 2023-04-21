# Astro Dodge

Astro Dodge is a web application that tracks Near Earth Objects (NEOs) using NASA's Open APIs. It allows users to create an account, track specific objects on a watchlist, and send feedback to the developer.

## Technologies Used

Astro Dodge is built using the following technologies:

- Flask: A minimal Python web framework used to build the backend logic
- Postgres: A relational database used to store user data
- Bulma CSS: A CSS framework used for styling the frontend
- Poetry: A Python dependency management tool
- Docker: A containerization platform used for deployment

## Hosting

Astro Dodge is hosted on [DigitalOcean](https://www.digitalocean.com/).

## Local Installation

### Using Docker

If you have Docker installed, you can run the following commands to build and start the Astro Dodge web application:

1. Clone the repository: `git clone https://github.com/kev-odin/astro-dodge.git`
2. Build the Docker image: `docker build -t astro-dodge .`
3. Run the Docker container: `docker run -p 5000:5000 astro-dodge`

This will start the Astro Dodge web application and it will be accessible at http://localhost:5000/.

### Without Docker

If you don't have Docker installed, you can follow these steps to install and run the Astro Dodge web application:

1. Clone the repository: `git clone https://github.com/kev-odin/astro-dodge.git`
2. Install dependencies using Poetry: `poetry install`
3. Start the development server: `poetry run flask run`

This will start the Astro Dodge web application and it will be accessible at http://localhost:5000/.

## Automated Updates

Astro Dodge uses NASA's Open APIs to track NEOs, and the data is updated regularly. The web application is set up to automatically update the NEO data every 24 hours to ensure that users have the latest information.

## Testing

Astro Dodge includes unit tests and functional tests developed using Pytest. To run the tests, use the following command:

```
poetry run pytest
```

This will execute the tests and output the results to the console.

## Mobile-Friendly Design

Astro Dodge is designed to be mobile-friendly, with responsive design that ensures the application looks great and functions well on any device.

## CI/CD with GitHub Actions

Astro Dodge uses GitHub Actions for Continuous Integration and Continuous Deployment. When code is pushed to the main branch, GitHub Actions automatically runs the tests and builds and deploys a Docker image of the application to DigitalOcean.

## Contributing

If you would like to contribute to Astro Dodge, please submit a pull request.

## License

Astro Dodge is licensed under the [MIT License](https://github.com/username/astro-dodge/blob/main/LICENSE).