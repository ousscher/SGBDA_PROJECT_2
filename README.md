# Patient Information Management System with Cassandra

This project demonstrates the implementation of a patient information management system using a wide-column database in Cassandra. The system is designed to handle large-scale, distributed data efficiently.

## Getting Started

Follow the steps below to set up and run the project locally.

### Prerequisites

- Docker and Docker Compose installed on your machine
- Python installed on your machine
- Required Python packages specified in `requirements.txt`

### Setup Instructions

1. **Run the Docker Container**

   Start the Cassandra database container:

   ```bash
   docker-compose up -d
   ```

   Allow the container some time to initialize.

2. **Load the Database Schema**

   Copy the schema definition file (`ddl.cql`) into the Cassandra container and execute it:

   ```bash
   docker cp ddl.cql cassandra:/tmp/ddl.cql
   docker exec -it cassandra cqlsh -f /tmp/ddl.cql
   ```

3. **Install Python Dependencies**

   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create the Database**

   Run the Python script to create the database:

   ```bash
   python script.py
   ```

5. **Load Sample Data**

   Copy the data manipulation file (`dml.cql`) into the Cassandra container and execute it:

   ```bash
   docker cp dml.cql cassandra:/tmp/dml.cql
   docker exec -it cassandra cqlsh -f /tmp/dml.cql
   ```

## Project Structure

- `docker-compose.yml`: Configuration file for setting up the Cassandra container
- `ddl.cql`: CQL file containing the database schema definitions
- `dml.cql`: CQL file containing sample data for the database
- `script.py`: Python script for initializing the database and performing operations
- `requirements.txt`: File specifying the Python dependencies

## Usage

After completing the setup, you can use the system to manage patient information efficiently. The system leverages Cassandra’s wide-column architecture to ensure high performance and scalability.
