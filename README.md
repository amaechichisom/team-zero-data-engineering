# **DataFestAfrica Hackathon 2024 TEAM ZERO**: Improving Academic Outcomes for Secondary Education

---

## 🎯 **Project Brief**

### **Project Title**:  
**Building a Data-Driven Solution for Laurel High School**

This project was developed for the **DataFestAfrica Hackathon 2024** as part of **TEAM ZERO**, focusing on enhancing academic outcomes for **Laurel High School** through a data-driven approach. The goal is to empower educators and administrators to make informed decisions based on student performance data, teacher assessments, and other critical academic metrics.

---

## 📝 **Introduction**

### **Problem Statement**  
Laurel High School faces significant challenges that impact the academic performance of its students. These include inadequate infrastructure, insufficient teacher availability, and a lack of resources for both students and teaching staff. As a result, students underperform in national exams like JAMB and WASSCE, leading to poor academic outcomes.

### **Project Objective**  
This project aims to tackle the above challenges by creating a data-driven solution that uses advanced data analysis and automation techniques to identify the critical factors affecting student performance. Through this, actionable insights can be generated for school administrators, allowing them to take steps that will improve educational outcomes.

### **Goals**
1. **Identify Areas of Improvement**: Analyze data to highlight key factors influencing student outcomes.
2. **Automate Data Pipelines**: Use automated data pipelines to collect, transform, and store data.
3. **Build Predictive Models**: Leverage machine learning models to predict students at risk of failing.
4. **Generate Actionable Insights**: Provide administrators with insights and strategies to address performance gaps.
5. **Enhance Academic Resources**: Use data to improve infrastructure, teacher availability, and resource allocation.

---

## 🛠️ **Tools & Technologies**

- **Docker** & **Docker Compose**: For containerizing the entire application setup.
- **Python**: Backend services built with Flask.
- **PostgreSQL**: Two PostgreSQL volumes for ELT and Airflow storage.
- **Amazon S3**: Storage for incoming data files via the Flask API.
- **Apache Airflow**: To automate data extraction, loading, and transformation (ELT).
- **DBT**: For data modeling and transformation within the pipeline.
- **AWS EC2**: Hosts the environment where Docker Compose is executed to run the containers.

---

## 📂 **Project Structure**

```plaintext
project-directory/
│
├── README.md                   # Project documentation
├── LICENSE                     # Project license file
│
├── airflow/                    # Airflow setup for DAGs and automation
├── backend/                    # Flask app hosting data API for researchers
├── dbt/                        # DBT project for data transformation models
├── elt/                        # Scripts for data extraction, loading, transformation
├── logs/                       # Logs of data pipeline
├── .gitignore                  # Gitignore for sensitive files
├── docker-compose.yaml         # Docker Compose for entire setup
├── Dockerfile                  # Dockerfile for building Flask app
└── start.sh                    # Script to start services

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Project Components](#project-components)
- [Automation Pipeline Overview](#automation-pipeline-overview)
- [Data Flow](#data-flow)
- [File Descriptions](#file-descriptions)
- [Results and Findings](#results-and-findings)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## 🔧 Installation and Setup


### Step 1: Clone the repository
```bash
git clone https://github.com/Kennedy87670/DataFestAfrica2024.git
cd DataFestAfrica2024
```

### Step 2: Install Docker and Docker Compose
Ensure that Docker and Docker Compose are installed on your machine. Follow the Docker installation guide for your system.

### Step 3: Run the Services
```bash
docker-compose run --rm init-airflow
docker-compose up
```

### Step 4: Access the Flask Backend API Documentation
After starting the services, access the API documentation via the following URL:

```bash
http://localhost:5000/apidocs
```

## Project Components

### Backend (Flask API)
The backend service, built using Flask, allows researchers to upload CSV datasets, which are sent to an Amazon S3 bucket for storage. The API supports full CRUD operations for managing data submissions.

### Airflow
Airflow runs a cron job every 5 minutes to automatically pull the uploaded datasets from the S3 bucket, load them into PostgreSQL, and transform them into structured tables.

### DBT
Once the data is stored in PostgreSQL, DBT performs transformations to create fact and dimension tables based on predefined metrics. These tables provide useful insights into key factors such as student performance, teacher availability, and more.

## Automation Pipeline Overview
The project implements an end-to-end automated pipeline that connects different components of the infrastructure:

1. Flask API: Researchers submit CSV datasets, which are stored in Amazon S3.
2. Airflow DAG: Airflow fetches the data every 5 minutes, transforming it and storing it in PostgreSQL.
3. DBT Models: DBT transforms raw data into meaningful fact and dimension tables.
4. Automated Insights: The processed data provides administrators with insights into student performance and other key metrics.

## Data Flow
PostgreSQL Storage: Two Postgres volumes are used:
- One for Airflow, which manages metadata and job scheduling.
- One for ELT and DBT, storing student records and analysis tables.

### AWS Infrastructure Diagram
![AWS Infrastructure Diagram](https://datathon-zero.s3.eu-west-1.amazonaws.com/aws-architecture.png "AWS Infrastructure")

### Entity-Relationship Diagram
![Entity-Relationship Diagram](https://datathon-zero.s3.eu-west-1.amazonaws.com/entity-relationship-diagram.png "ER Diagram")

Suggested Diagrams:
- Entity-Relationship Diagram: To show relationships between tables in the database (students, teachers, scores, etc.).
- AWS Architecture Diagram: To depict how the EC2 instance, S3, and Docker services interact in the project.

## File Descriptions
- `backend/`: Contains the Flask app for handling researcher uploads.
- `airflow/`: Airflow DAG files for running ETL jobs.
- `dbt/`: DBT transformation models to structure data for reporting.
- `elt/`: Scripts that define the ELT process for data extraction, loading, and transformation.

## Results and Findings
### Key Insights from the Data:
- Strong predictors of student performance include teacher experience, parental involvement, and study hours.
- Infrastructure quality and access to resources were also significant indicators of student success.

### Automation Success:
- Airflow and DBT seamlessly handled data extraction, transformation, and modeling, making the pipeline fully automated and robust.

## Acknowledgments
- DataFestAfrica Hackathon 2024 for providing the platform for this project.
- TEAM ZERO for collaborative efforts in building this solution.
- Laurel High School (fictional) for the problem context and use case.

## License
This project is licensed under the MIT License. See the LICENSE file for details.