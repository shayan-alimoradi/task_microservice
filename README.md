# Advanced Task Management Microservice

This microservice is designed to manage tasks within an advanced project management application, utilizing microservices architecture, asynchronous task processing, real-time notifications via WebSocket, caching with Redis, and Docker containerization.

## Features

- **Django Project Setup**: Initializes a Django project with PostgreSQL as the primary database.
- **Task Model**: Defines a Task model with fields for id, project (ForeignKey to Project), title, description, status, created_at, updated_at, and due_date.
- **Comment Model**: Includes a Comment model with fields for id, task (ForeignKey to Task), author, content, and created_at.
- **API Endpoints**:
  - **GET /api/tasks-list/**: Lists all tasks.
  - **POST /api/task-create/**: Creates a new task.
  - **GET /api/task/<id>/**: Retrieves a single task by ID.
  - **PUT /api/task/<id>/**: Updates a task by ID.
  - **DELETE /api/task/<id>/**: Deletes a task by ID.
  - **POST /api/task/<id>/comments/**: Adds a comment to a task.
  - **GET /api/task/<id>/create-comment/**: Lists all comments for a task.
- **Asynchronous Task Processing with Celery**:
  - Utilizes Celery with RabbitMQ as the message broker.
  - Celery tasks:
    - Sends email reminders for tasks due within the next 24 hours.
    - Sends daily project summary reports.
  - Schedules Celery tasks using Celery Beat.
- **WebSocket for Real-Time Notifications**:
  - Implements Django Channels for WebSocket support.
  - WebSocket endpoint **/ws/notifications/** for real-time notifications.
  - Notifies clients of task creation, updates, deletions, comments, and project summary reports.
- **Caching with Redis**:
  - Configures Redis for caching frequently accessed data.
  - Caches lists of tasks and projects to reduce database load.
  - Implements cache invalidation strategies.
- **Testing**:
  - Unit tests for each API endpoint using Django’s TestCase class.
  - Tests for Celery tasks to ensure proper scheduling and execution.
  - WebSocket testing to verify real-time notifications.
  - Tests to validate Redis caching and invalidation logic.
- **Docker**:
  - Provides Dockerfile and docker-compose.yml for easy deployment.
  - docker-compose.yml includes services for Django app, PostgreSQL, RabbitMQ, Redis, and Celery workers.

## Setup and Installation

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shayan-alimoradi/task_microservice
   cd task_microservice

2. Set up environment variables:
    ```bash
    Create a .env file in the root directory with the following variables:

    plaintext
    EMAIL_HOST_USER=youremail
    EMAIL_HOST_PASSWORD=yourpassword

3. Build and run the application:
    First run this command to create a network
    ```
    docker network create project-network
    ```
    ```bash
    docker-compose up -d --build
    ```

4. Create a superuser (optional):
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5. Access the application and swagger:
    ```bash
    The API endpoints will be available at http://localhost:8001/.
    ```
    ```bash
    The swagger will be available at http://localhost:8001/swagger/.
    ```
    ```bash
    The redoc will be available at http://localhost:8001/redoc/.
    ```

6. Testing

    To run tests for API endpoints and Redis caching:
    ```bash
    docker-compose exec -it task_backend python manage.py test
    ```
    To run tests for Celery tasks:
    ```bash
    docker-compose exec -it task_backend pytest task/api/tests/test_celery.py
    ```
    To run tests for Real-Time notifications:
    ```bash
    docker-compose exec -it task_backend pytest task/api/tests/test_consumers.py
    ```
<br/>

# Integration with Project Management Microservice
Ensure the Project Management Microservice is running to fully utilize task management functionalities.