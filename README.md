# Astro Dodge

Astro Dodge is a web application that tracks Near Earth Objects (NEOs) using NASA's Open APIs. It allows users to create an account, track specific objects on a watchlist, and and learn more details about a specific object.
## Description
<!-- 
Provide a short description explaining the what, why, and how of your project. Use the following questions as a guide:

- What was your motivation?
- Why did you build this project? (Note: the answer is not "Because it was a homework assignment.")
- What problem does it solve?
- What did you learn? -->

![astro-dodge](https://img.shields.io/website?down_color=red&down_message=offline&style=for-the-badge&up_color=green&up_message=online&url=https%3A%2F%2Fastro-dodge.kchungdev.com)
![astro-dodge](https://img.shields.io/github/last-commit/kev-odin/astro-dodge?style=for-the-badge)
![astro-dodge](https://img.shields.io/github/languages/count/kev-odin/astro-dodge?style=for-the-badge)
![astro-dodge](https://img.shields.io/github/languages/top/kev-odin/astro-dodge?style=for-the-badge)
![astro-dodge](https://img.shields.io/github/repo-size/kev-odin/astro-dodge?style=for-the-badge)
![astro-dodge](https://img.shields.io/github/license/kev-odin/astro-dodge?style=for-the-badge)
![astro-dodge](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F-grey?style=for-the-badge)

## Table of Contents (Optional)
<!-- If your README is long, add a table of contents to make it easy for users to find what they need.
 -->
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Installation
<!-- What are the steps required to install your project? Provide a step-by-step description of how to get the development environment running. -->

### Docker Compose
1. Copy this repository and run the command: `docker compose up`  
2. This will build the images necessary to run this project.  

### Docker
A ready to use Docker image should be hosted in the GitHub Packages Container Registry.  
1. Simply pull the image from this repository with: `docker pull ghcr.io/kev-odin/astro-dodge:latest`  
2. Run the image with this command: `docker run astro-dodge:latest`  
3. Then open your web browser and enter `localhost:5000` in the address bar.

### Local Install
If you don't have Docker installed, you can follow these steps to install and run the Astro Dodge web application:

1. Clone the repository: `git clone https://github.com/kev-odin/astro-dodge.git`
2. Install dependencies using Poetry: `poetry install`
3. Start the development server: `poetry run flask run`

This will start the Astro Dodge web application and it will be accessible at http://localhost:5000/.

## Features
<!-- 
Provide instructions and examples for use. Include screenshots as needed.

To add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:

    ```md
    ![alt text](assets/images/screenshot.png)
    ```
 -->
 ![astro-home](assets/images/astro-home.gif)
### Mobile-Friendly Design

Astro Dodge is designed to be mobile-friendly, with responsive design that ensures the application looks great and functions well on any device.

### CI/CD with GitHub Actions

Astro Dodge uses GitHub Actions for Continuous Integration and Continuous Deployment. When code is pushed to the main branch, GitHub Actions automatically runs the tests and builds a Docker image that is stored in the GitHub Container Registry.

## Tech Stack
![Python](https://img.shields.io/badge/Python-grey?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-grey?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-grey?style=for-the-badge&logo=flask&logoColor=white)
![postgresql](https://img.shields.io/badge/postgresql-grey?style=for-the-badge&logo=postgresql&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-grey?style=for-the-badge&logo=pytest&logoColor=white)
![insomnia](https://img.shields.io/badge/insomnia-grey?style=for-the-badge&logo=insomnia&logoColor=white)
![Bulma](https://img.shields.io/badge/Bulma-grey?style=for-the-badge&logo=bulma&logoColor=white)
![DigitalOcean](https://img.shields.io/badge/DigitalOcean-grey?style=for-the-badge&logo=digitalocean&logoColor=white)
![github actions](https://img.shields.io/badge/github_actions-grey?style=for-the-badge&logo=githubactions&logoColor=white)

## How to Contribute
If you are intrested in contributing to this project, feel free to create an issue, fork the repository, and create a pull request. If new features are added, write relevant unit and integration tests to ensure code coverage.

## Tests
To run tests, you will need `poetry` installed. Learn more about the installation process ![here](https://python-poetry.org/docs/).  
Run this command: `poetry run pytest`

## License
Astro Dodge is licensed under the [MIT License](https://github.com/username/astro-dodge/blob/main/LICENSE).