# Trending GitHub Repos Tracker

## Overview
Trending GitHub Repos Tracker is a FastAPI application that fetches trending GitHub repositories and shares them on Telex. It supports different programming languages and posts updates to a Telex channel at set intervals.

## Features
 📌Fetches trending GitHub repositories.
 📌Supports different programming languages.
 📌Posts updates to a Telex channel at set intervals.

## Preview

 ![Preview Image](https://raw.githubusercontent.com/telexintegrations/Trending-Github-Repos/refs/heads/main/assets/Screenshot%202025-02-22%20231548.png)


## Endpoints

### GET /
Returns a welcome message indicating that the app is running successfully.

### GET /integration.json
Returns integration details including app name, description, logo, URL, and settings.

### GET /test
Fetches and returns the top 5 trending GitHub repositories for a specified programming language (default is Python).

### POST /tick
Triggers the fetching and posting of trending GitHub repositories to a specified return URL.

## Installation

1. Clone the repository:
    ```sh
    git clone 
    cd HNG-Telex
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    uvicorn main:app --reload
    ```

## Usage
- Access the application at `http://127.0.0.1:8000`.
- Use the provided endpoints to interact with the application.

