FROM apache/airflow:latest

# Switch to root user to install system packages
USER root

# Update package list and install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client-17

# Switch back to airflow user
USER airflow

# Install the Docker provider for Airflow without using --user
RUN pip install apache-airflow-providers-docker
    