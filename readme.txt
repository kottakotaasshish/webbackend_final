Cloud Service Access Management System

----------------------------------------------------------------------------------------------------------------------------------------

Team Members

Vuppal Tarun Sai (CWID - 827778861)
Ashish Kottakota (CWID - 878640879) 

----------------------------------------------------------------------------------------------------------------------------------------

Project Overview
The Cloud Service Access Management System is a backend application built using FastAPI for managing access to cloud services based on user subscriptions.
The system regulates access to various cloud APIs based on subscription plans and enforces usage limits, providing an efficient way to manage customer access and permissions.

----------------------------------------------------------------------------------------------------------------------------------------

Git link - https://github.com/kottakotaasshish/webbackend_final

----------------------------------------------------------------------------------------------------------------------------------------

Features
Role-Based Access Control (RBAC):

Admins can manage subscription plans and permissions.
Customers can subscribe to plans and access APIs within their permissions.
Subscription Plan Management:

Admins can create, modify, and delete subscription plans.
Plans include attributes such as API permissions and usage limits.
Permission Management:

Admins can add, modify, and delete permissions for APIs.
Usage Tracking:

Tracks the number of API requests per user.
Enforces usage limits based on subscription plans.
Access Control:

Ensures users can only access APIs within their plan’s permissions.
Restricts access once usage limits are reached.
Simulated Cloud Services:

APIs (service1 to service6) are managed for demonstration purposes.

----------------------------------------------------------------------------------------------------------------------------------------

Technologies Used
Backend Framework: FastAPI
Database: MySQL
ORM: SQLAlchemy
Authentication: JWT (JSON Web Tokens)
Language: Python 3.9+

----------------------------------------------------------------------------------------------------------------------------------------

Setup Instructions

1. Prerequisites
Python 3.9 or above
MySQL installed and running
A code editor (e.g., Visual Studio Code)

2. Clone the Repository

git clone <repository-link>
cd cloud_service_management

3. Create and Activate Virtual Environment

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install Dependencies

pip install -r requirements.txt

5. Set Up the Database
Create a MySQL Database:

CREATE DATABASE cloud_management;
Update .env File: Ensure your .env file contains the correct database credentials:

DATABASE_URL=mysql+pymysql://<username>:<password>@localhost/cloud_management
Initialize the Database: Tables will be created automatically when the server runs.

6. Run the Application
Start the FastAPI server:

uvicorn main:app --reload
The application will run at http://127.0.0.1:8000.

----------------------------------------------------------------------------------------------------------------------------------------

How to Use the APIs
1. Access Swagger UI
Visit the Swagger documentation at:

http://127.0.0.1:8000/docs

2. Authenticate
Admin Login:
Use POST /api/login with the admin credentials.
Copy the access_token and click Authorize in Swagger UI.
Customer Login:
Use POST /api/login with customer credentials.

3. Admin Endpoints
Manage Subscription Plans:
Create, modify, and delete plans using /api/plans.
Manage Permissions:
Add, modify, and delete permissions using /api/permissions.
Reset User Usage:
Use /api/usage/reset/{username} to reset a user's API usage.
View Usage Overview:
Use /api/usage/overview to view all users’ usage.

4. Customer Endpoints
Subscribe to a Plan:
Use POST /api/subscriptions to subscribe to a plan.
View Subscription Details:
Use GET /api/subscriptions/{username} to view the current subscription.
Access APIs:
Use endpoints /api/service1 to /api/service6 for cloud service access.
View Usage:
Use GET /api/usage/{username} to view API usage statistics.

----------------------------------------------------------------------------------------------------------------------------------------

Testing the APIs
Follow these steps to test the APIs:

Admin Functions:
    Login as Admin and create subscription plans and permissions.
    Assign plans to users and manage permissions.

Customer Functions:
    Login as a Customer and subscribe to a plan.
    Access APIs and demonstrate usage tracking and limits.
Access Control:
    Test unauthorized access scenarios.
    Demonstrate access denied for exceeded limits and restricted APIs.

----------------------------------------------------------------------------------------------------------------------------------------
