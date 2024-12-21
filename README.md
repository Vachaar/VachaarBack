# VachaarBack
**The back-end repo of Vachaar project**

## Steps to Set Up and Run the Project

<details>

<summary>
<strong>
Docker Compose
</strong>
</summary>

   ### Prerequisites
1. Ensure that Docker and Docker Compose are installed on your system.
2. Verify installation by running:
   ```bash
   docker --version
   docker-compose --version
   ```

### Build and Start the Project
1. Navigate to the project's root directory:
   ```bash
   cd /path/to/project
   ```
2. Build and bring up the containers:
   ```bash
   docker-compose up --build
   ```
3. Access the application at `http://localhost:80/` (replace `80` with the configured port in `docker-compose.yml`) .

### Shut Down the Project
1. Stop and remove the containers:
   ```bash
   docker-compose down
   ```

### Additional Docker Compose Commands
1. View running containers:
   ```bash
   docker ps
   ```
2. Stop specific services:
   ```bash
   docker compose stop <service_name>
   ```
3. Restart services:
   ```bash
   docker compose restart <service_name>
   ```

</details>

---

<details>

<summary>
<strong>
VENV
</strong>
</summary>

### Prerequisites
1. Ensure Python (3.8 or later) is installed on your system.
2. Confirm installation by checking Python version:
   ```bash
   python --version
   ```

### Creating and Activating Virtual Environment
1. Navigate to the project's root directory:
   ```bash
   cd /path/to/project
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
4. Confirm activation by checking the Python version:
   ```bash
   python --version
   ```

### Installing Dependencies
1. Install project dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

### Starting the Application
1. Run the application:
   ```bash
   python manage.py runserver
   ```
2. Click on the provided link to redirect to the app

### Deactivating the Environment
1. To deactivate the virtual environment, simply run:
   ```bash
   deactivate
   ```

</details>

---

## Pre-Commit

<details>

<summary>
<strong>
Pre-Commit SetUp
</strong>
</summary>

### Pre-Commit Hooks Setup
Pre-commit hooks help maintain code quality by running checks such as linting and formatting before committing changes.

### Installing Pre-Commit
1. Install the `pre-commit` package:
   ```bash
   pip install pre-commit
   ```
2. Set up pre-commit for the repository:
   ```bash
   pre-commit install
   ```

### Running Pre-Commit Hooks Manually
You can manually run pre-commit hooks against all files using:
   ```bash
      pre-commit run --all-files
   ```

</details>