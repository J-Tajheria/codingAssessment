"""
This project contains the backend code written using Flask API,
to set up the DB and the routing to communicate with the frontend.
"""
import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# list of event names
service_types = [
    "Contact Management",  "CryptoSync", "I/O Gateway", "Packet Forwarding", "TDA File Manager",
    "Cloud Storage", "Data Backup", "Email Hosting", "Project Management", "API Gateway",
    "Document Collaboration", "Video Conferencing", "Task Automation", "E-commerce Platform",
    "Web Hosting", "Content Delivery Network (CDN)", "Customer Relationship Management (CRM)",
    "Social Media Management", "Identity Management", "Remote Desktop Access",
    "Inventory Management", "Network Monitoring", "Performance Analytics", "Financial Reporting",
    "Virtual Private Network (VPN)", "Load Balancing", "Domain Registration",
    "Web Application Firewall (WAF)", "Search Engine Optimization (SEO)",
    "Software Development Kit (SDK)", "Test Automation", "Payment Processing", "Chatbot Service",
    "Business Intelligence", "Subscription Billing","Online Learning Platform", "Fleet Management", 
    "Resource Scheduling", "Threat Detection","Web Scraping", "Real-Time Data Processing", 
    "Remote Backup", "Help Desk Support", "Digital Asset Management", "Data Warehousing"
]

# List of status'
status = ["Active", "Pending", "Completed", "Failed", "Not Started"]

# Current date time
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# MYSQL Configuration
configuration = {
    'user': 'root',
    'password': '',
    'host': 'localhost', 
    'database': 'mydatabase'
}

def random_data_generation():
    """
    Function which randomly generates data to be injected into the DB.

    Args: No arguments are passed to function.

    returns: A database with randomly generated data injected through SQL queries.
    """
    try:
        connection = mysql.connector.connect(
            user=configuration['user'],
            password=configuration['password'],
            host=configuration['host']
        )

        mycursor = connection.cursor()

        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {configuration['database']}")
        print(f"Database '{configuration['database']}' checked/created successfully.")

        mycursor.execute(f"USE {configuration['database']}")

        #  Create Table in SQL
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS eventsTable (
            id INT AUTO_INCREMENT PRIMARY KEY,
            eventsName VARCHAR(100) NOT NULL,
            status VARCHAR(100) NOT NULL,
            created_at TIMESTAMP
            )
        '''

        mycursor.execute(create_table_query)

        print("Table checked/created successfully.")

        values = []

        for _ in range(15):
            service_type = random.choice(service_types)
            status_injection = random.choice(status)
            random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
            random_timestamp = start_date + timedelta(seconds=random_seconds)

            values.append((service_type, status_injection, random_timestamp,))

        sql_statement = "INSERT INTO eventsTable (eventsName, status, created_at) VALUES (%s, %s, %s)"
        mycursor.executemany(sql_statement, values)
        connection.commit()
        print(mycursor.rowcount, "was inserted.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    finally:
        mycursor.close()
        connection.close()

@app.route('/events', methods=['GET'])
def get_events():
    """
    Fetches all the data currently stored in the DB.

    Returns: All the data currently stored in the DB.
    """
    try:
        connection = mysql.connector.connect(
            user=configuration['user'],
            password=configuration['password'],
            host=configuration['host'],
            database=configuration['database']
        )
        mycursor = connection.cursor()

        # Extract data from DB
        mycursor.execute("SELECT id, eventsName, status, created_at FROM eventsTable")
        rows = mycursor.fetchall()

        events = [
            { "id": row[0], "eventsName": row[1], "status": row[2], "created_at": row[3].strftime('%Y-%m-%d %H:%M:%S')}
            for row in rows
        ]

        return jsonify(events)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        mycursor.close()
        connection.close()

@app.route('/events', methods=['POST'])
def add_event():
    """
    Adds a new event to the events database

    Args: It takes event name and status given through inputs by the user.

    Returns: A success message
    """
    try:
        connection = mysql.connector.connect(
            user=configuration['user'],
            password=configuration['password'],
            host=configuration['host'],
            database=configuration['database']
        )
        mycursor = connection.cursor()

        # Get data from request
        data = request.get_json()
        event_name = data.get('eventsName')
        event_status = data.get('status')
        created_at = data.get('created_at', datetime.now())

        # Extract data from DB
        insertion_query = "INSERT INTO eventsTable (eventsName, status, created_at) VALUES (%s, %s, %s)"
        mycursor.execute(insertion_query, (event_name, event_status, created_at ))
        connection.commit()

        return jsonify({"message": "Event successfully added.", "id": mycursor.lastrowid}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        mycursor.close()
        connection.close()

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """
    Deletes an event from the events database

    Args: It takes the id of the event selected to be deleted.

    Returns: A success message that is has been deleted.
    """
    try:
        connection = mysql.connector.connect(
            user=configuration['user'],
            password=configuration['password'],
            host=configuration['host'],
            database=configuration['database']
        )
        mycursor = connection.cursor()

        # Extract data from DB
        delete_query = "DELETE FROM eventsTable WHERE id = %s"
        mycursor.execute(delete_query, (event_id, ))
        connection.commit()

        if mycursor.rowcount > 0:
            return jsonify({"message": f"Event with ID {event_id} deleted successfully."}), 200
        else:
            return jsonify({"message": f"No event found with ID {event_id}."}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        mycursor.close()
        connection.close()

if __name__ == '__main__':
    random_data_generation()

    app.run(debug=True)
