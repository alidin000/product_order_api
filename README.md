# product_order_api
# Warehouse Management API

## Prerequisites

1. **Docker**: Ensure that Docker is installed on your machine. You can download it from [Docker's official website](https://www.docker.com/get-started).
2. **Docker Compose**: Docker Compose is usually included with Docker Desktop, but you can also install it separately if needed. Follow the installation guide [here](https://docs.docker.com/compose/install/).

## Steps to Run the Application

1. **Clone the Repository**:
   If you haven't already, clone the repository containing your FastAPI project:
   ```bash
      git clone <repository-url>
      cd <repository-directory>
2. **Build the Docker Images**:  
  Navigate to your project directory where the `docker-compose.yml` file is located. Build the images using Docker Compose:
    ```bash
        docker-compose build
 3. **Start the Services**:  
  Start the FastAPI application and PostgreSQL database:
    ```bash
        docker-compose up
        
4. **You can also access the interactive API documentation (Swagger UI) at**:
    ```bash
        http://localhost:8000/docs

5. **Run Tests: To run the tests defined in your application, you can execute the following command inside the container**:

    ```bash
        docker-compose exec web pytest