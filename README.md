Task Management Application

A comprehensive task management system with task completion reporting functionality built with Django and Django REST Framework.


Features

Role-Based Access Control: SuperAdmin, Admin, and User roles with different permission levels
Task Management: Create, assign, update, and track tasks
Task Completion Reports: Users submit reports and worked hours when completing tasks
JWT Authentication: Secure API access with JSON Web Tokens
Admin Panel: Custom admin interface for managing users and tasks


System Requirements

Python 3.8 or higher
Django 4.2 or higher
Django REST Framework 3.14 or higher
Other dependencies as listed in requirements.txt


Installation

Clone the repository:
git clone <repository-url>
cd task-management-app

Create and activate a virtual environment:
python -m venv venv


# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run migrations:
python manage.py makemigrations
python manage.py migrate

Create a SuperAdmin user:
python manage.py createsuperuser
Note: This command creates a user with SuperAdmin role.
Start the development server:
python manage.py runserver

Access the application at http://127.0.0.1:8000/

Project Structure
TASKPROJECT/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── taskapp/
│   ├── __init__.py
│   ├── _pycache__/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── tokens.py
│   ├── url.py
│   └── views.py
└── taskproject/
    ├── __init__.py
    ├── _pycache__/
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py


API Endpoints

Authentication

POST /api/token/: Obtain JWT token

Request body: {"username": "your_username", "password": "your_password"}
Response: {"access": "access_token", "refresh": "refresh_token"}


POST /api/token/refresh/: Refresh JWT token

Request body: {"refresh": "refresh_token"}
Response: {"access": "new_access_token"}


GET /api/me/: Get current user details

Headers: Authorization: Bearer <access_token>
Response: User details


Tasks

GET /api/user-tasks/: Get all tasks assigned to the authenticated user

Headers: Authorization: Bearer <access_token>
Response: List of task objects


PUT /api/tasks/update-status/{id}/: Update task status (including marking as completed)

Headers: Authorization: Bearer <access_token>
Request body:
json{
  "status": "Completed",
  "completion_report": "Task completed successfully. Fixed all issues.",
  "worked_hours": 5.5
}

Response: Updated task object


GET /api/tasks/{id}/report/: View task completion report (Admin/SuperAdmin only)

Headers: Authorization: Bearer <access_token>
Response: Task report details


GET /api/tasks/: List all tasks (Admin/SuperAdmin only)

Headers: Authorization: Bearer <access_token>
Response: List of all tasks


POST /api/tasks/: Create a new task (Admin/SuperAdmin only)

Headers: Authorization: Bearer <access_token>
Request body: Task details
Response: Created task


GET/PUT/DELETE /api/tasks/{id}/: Get, update or delete a specific task (Admin/SuperAdmin only)

Headers: Authorization: Bearer <access_token>
Response: Task details


User Management

GET /api/users/: List all users (SuperAdmin only)

Headers: Authorization: Bearer <access_token>
Response: List of users


POST /api/users/: Create a new user (SuperAdmin only)

Headers: Authorization: Bearer <access_token>
Request body: User details
Response: Created user


GET/PUT/DELETE /api/users/{id}/: Get, update or delete a specific user (SuperAdmin only)

Headers: Authorization: Bearer <access_token>
Response: User details


GET /api/admin/users/: Get users assigned to an admin (Admin only)

Headers: Authorization: Bearer <access_token>
Response: List of assigned users



Web Interface URLs
Authentication Pages

Login: http://127.0.0.1:8000/ or http://127.0.0.1:8000/login/

Dashboard Pages

SuperAdmin Dashboard: http://127.0.0.1:8000/superadmin/dashboard/
Admin Dashboard: http://127.0.0.1:8000/admin_dashboard/
User Dashboard: http://127.0.0.1:8000/user/dashboard/

Management Pages

User Tasks View: http://127.0.0.1:8000/my-tasks/
Manage Users (SuperAdmin): http://127.0.0.1:8000/users/
Manage Admins (SuperAdmin): http://127.0.0.1:8000/admins/
Admin Tasks Management: http://127.0.0.1:8000/admin_tasks/
Manage Tasks: http://127.0.0.1:8000/tasks/
Task Report Page: http://127.0.0.1:8000/tasks/{id}/report-page/

Role-Based Access

SuperAdmin

Access URL: http://127.0.0.1:8000/superadmin/dashboard/
Can manage all users (create, delete, assign roles)
Can manage all admins (create, delete, assign roles)
Can assign users to admins
Can view and manage all tasks
Can view all completion reports

Admin

Access URL: http://127.0.0.1:8000/admin_dashboard/
Can assign tasks to their users
Can view and manage tasks assigned to their users
Can view completion reports of their users' tasks
Cannot manage user roles

User

Access URL: http://127.0.0.1:8000/user/dashboard/
Can view assigned tasks
Can update task status
Can submit completion reports with worked hours

User Management
Creating Users
SuperAdmin can create new users through the management interface:

Navigate to http://127.0.0.1:8000/users/
Click "Add User" or use the form provided
Fill in the required details and select the appropriate role
Save the new user

Assigning Roles

SuperAdmin can update a user's role:

Navigate to the users page
Edit the user
Change the role dropdown to Admin or User
Save changes


SuperAdmin can assign users to an admin:

Navigate to the admins management page
Select an admin
Assign users from the available users list
Save changes



Creating Admin Users

SuperAdmin can create admin users:

Navigate to http://127.0.0.1:8000/admins/
Click "Add Admin" or use the form provided
Fill in the required details
Save the new admin



Task Management
Creating Tasks

Admin or SuperAdmin can create tasks:

Navigate to http://127.0.0.1:8000/tasks/ or http://127.0.0.1:8000/admin_tasks/
Click "Add Task" or use the form provided
Fill in the task details (title, description, due date)
Assign to a user
Set initial status (typically "Pending")
Save the task



Viewing Tasks

Users can view their assigned tasks:

Navigate to http://127.0.0.1:8000/my-tasks/
All assigned tasks will be displayed with their details


Admins can view tasks assigned to their users:

Navigate to http://127.0.0.1:8000/admin_tasks/
All tasks assigned to their users will be displayed


SuperAdmins can view all tasks:

Navigate to http://127.0.0.1:8000/tasks/
All tasks in the system will be displayed



Completing Tasks
Users can mark tasks as completed:

Web Interface:

Navigate to http://127.0.0.1:8000/my-tasks/
Click on the task you want to update status
Set status from dropdown
Click on the task you want to mark as completed
Set status to "Completed"
Fill in the completion report and worked hours
Submit the form


API:

Make a PUT request to /api/tasks/update-status/{id}/
Include the completion report and worked hours in the request body
Set status to "Completed"



Viewing Task Reports
Admins and SuperAdmins can view task completion reports:

Web Interface:

Navigate to http://127.0.0.1:8000/tasks/{id}/report-page/
View the completion report and worked hours


API:

Make a GET request to /api/tasks/{id}/report/
View the completion report details


