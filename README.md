# Friend Connection API

This is a FastAPI-based backend application for a friend connection platform. It provides various endpoints for user authentication, friend management, status updates, and user profile management.

## Features

- User authentication (login, registration)
- Friend management (send friend request, approve or reject friend requests, list friends)
- Status updates (Add,Edit and View status updates)
- User profile management
- Health check endpoint

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [Prisma](https://www.prisma.io/): Next-generation ORM for Python and Node.js
- [Uvicorn](https://www.uvicorn.org/): A lightning-fast ASGI server
- [Python 3.9+](https://www.python.org/)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.9 or higher

## Setting Up the Project

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/friend-connection-api.git
   cd friend-connection-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables. Create a `.env` file in the root directory and add the following:
   ```
   DATABASE_URL="your-database-url"
   SECRET_KEY="your-secret-key"
   ```

5. Run the Prisma migrations:
   ```
   prisma db push
   ```

## Running the Application

To run the application, use the following command:

```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the application is running, you can access the automatically generated API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment

App is deployed on render platform and can be accessed here: 

- https://friend-connection-app-be.onrender.com/docs
- https://friend-connection-app-be.onrender.com/redoc

## Health Check

Health check is setup with the help of: 
- https://console.cron-job.org/ 

It makes an HTTP request to `/health` endpoint after every 10 minute.
This also makes sure that the app does not go down on render due to periods of inactivity.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
