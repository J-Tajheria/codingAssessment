from flask import Flask, jsonify
import random
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import errorcode
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

status = ["Active", "Pending", "Completed", "Failed", "Not Started"]

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

def randomDataGeneration():
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
        createTableQuery = '''
            CREATE TABLE IF NOT EXISTS eventsTable (
            id INT AUTO_INCREMENT PRIMARY KEY,
            eventsName VARCHAR(100) NOT NULL,
            status VARCHAR(100) NOT NULL,
            created_at TIMESTAMP
            )
        '''

        mycursor.execute(createTableQuery)

        print("Table checked/created successfully.")

        values = []

        for _ in range(50):
            serviceType = random.choice(service_types)
            statusInjection = random.choice(status)
            random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
            random_timestamp = start_date + timedelta(seconds=random_seconds)

            values.append((serviceType, statusInjection, random_timestamp,))

        SQL_Statement = "INSERT INTO eventsTable (eventsName, status, created_at) VALUES (%s, %s, %s)"
        mycursor.executemany(SQL_Statement, values)
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

