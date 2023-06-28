
# Project Name

EIT Final Project - Desenvolvimento de uma aplicação web que permite uma maior ligação ao tecido empresarial da região e a toda a comunidade académica, visando a divulgação e gestão das atividades de prestação de serviço externo do IPV.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)

## Overview

Aplicação web que permite uma maior ligação ao tecido empresarial da região e a toda a comunidade académica, visando a divulgação e gestão das atividades de prestação de serviço externo do IPV.

## Installation

Follow these step-by-step instructions to install and set up your Django project locally. Include any prerequisites or dependencies required, such as Python version, Django version, and other libraries.

### Prerequisites

- Install the Python extension for your code editor (e.g., Visual Studio Code).
- Install Python 3.9.1 (or a superior version).
- On Windows, ensure that the location of your Python interpreter is included in the PATH environment variable.

### Clone the Repository

Clone the repository using Git:

- git clone https://github.com/pt-ipv-estgl-lab/stakeholders.git

### Navigate to the Project Directory

Navigate to the project directory in your terminal or command prompt:

- cd project-directory(stakeholders)

### Install Dependencies

Create a virtual environment and activate it:

- python -m venv .venv # Create virtual environment
- .venv\Scripts\activate # Activate virtual environment

Install the required dependencies from the `requirements.txt` file:

- pip install -r requirements.txt

Update pip in the virtual environment by running the following command:

- python -m pip install --upgrade pip

Open the project folder in VS Code by running:

- code .

### Start the Development Server

Start the development server to run your Django project:

- python manage.py runserver

Access the application at http://localhost:8000
Create an account or log in with existing credentials.
### Perform Migrations

Run the necessary migrations for your Django project:

- python manage.py makemigrations
- python manage.py migrate
- python manage.py collectstatic




