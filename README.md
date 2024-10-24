# codingAssessment

This repository contains the code for a coding assessment. This system allows a user to add, display and delete events from the system, with the frontend interacting with the backend through APIs.

Technologies Used:
Backend: Flask (Python) 
Frontend: Angular
Database: MySQL

## SetUp:
Before running the project, ensure you have the following installed:
```
Python (v3.7 or higher)
Node.js (v12 or higher) and npm
MySQL Server
Angular CLI (optional for development)
```

## Backend:
1. Clone the repo
    ```
    git clone https://github.com/J-Tajheria/codingAssessment.git
    ```
2. cd into the backend:
    ```
        cd codingAssessment/Backend
    ```
3. Create a virtual environment:
    ```
        python -m venv venv
    ```
    Activate it:
    ```
        venv\Scripts\activate #Windows
    ```
    or
    ```
    source venv/bin/activate #Mac
    ```

4. 
    ```
    pip install -r /requirements.txt
    ```
5. Make sure you have MySQL installed and running.
6. Update the MySQL configuration in app.py with your MySQL credentials:
    ```
    configuration = {
        'user': 'root',       # Update with your MySQL username
        'password': 'your_password',  # Update with your MySQL password
        'host': 'localhost',
        'database': 'mydatabase'
    }
    ```
7. Run the server:
    ```
    python app.py / python3 app.py dependent on your python version.
    ```

## Frontend
1. In a different terminal with the server still running, navigate to the frontend.
    ```
    cd frontend
    ```
2. Install the required Node.js packages:
    ```
    npm install
    ```
3. Run the client:
    ```
    ng serve
    ```

Access the Application
Open your browser and go to http://localhost:4200. The frontend will communicate with the Flask backend on http://127.0.0.1:5000.
