TaskFlow
A modern, feature-rich task management application with a beautiful interface and powerful functionality.

🚀 Features
Core Functionality
✅ Task Management - Create, read, update, and delete tasks

📊 Dashboard - Overview with statistics and recent tasks

🔍 Smart Search - Find tasks by title or description

🎯 Filtering & Sorting - Filter by status and sort by various criteria

📈 Analytics - Visual charts and performance metrics

🎨 Beautiful UI - Modern design with gradients and animations

Advanced Features
Merge Sort Algorithm - Efficient sorting of tasks

Data Visualization - Pie charts, bar charts, and trend analysis

Responsive Design - Works perfectly on desktop and mobile devices

🛠️ Tech Stack
Frontend
HTML5 - Semantic markup

CSS3 - Modern styling with CSS variables and gradients

JavaScript ES6+ - Vanilla JavaScript with async/await

Font Awesome - Beautiful icons

Google Fonts - Inter font family

Backend
Python - Backend logic

Flask - Web framework

PostgreSQL - Database (configurable)

Matplotlib - Chart generation

📦 Installation
Prerequisites
Python 3.8+

PostgreSQL (or SQLite for development)

Modern web browser

Backend Setup
Clone the repository:

bash
git clone <repository-url>
cd taskflow
Install Python dependencies:

bash
pip install -r requirements.txt
Set up the database:

bash
python db/database.py
Start the Flask server:

bash
python app.py
The backend will be available at http://localhost:5000

Frontend Setup
Open index.html in your web browser

Or serve via a local web server:

bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve .
The frontend will be available at http://localhost:8000

🎯 Usage
Managing Tasks
Create Tasks: Click "New Task" button to add tasks with title, description, and due date

View Tasks: Browse all tasks or filter by status (pending/completed)

Complete Tasks: Click the checkmark button to mark tasks as complete

Edit Tasks: Click the edit button to modify task details

Delete Tasks: Click the trash button to remove tasks

Dashboard Features
Statistics Cards: View total tasks, pending, completed, and completion rate

Recent Tasks: See your most recently created tasks

Quick Stats: Overdue tasks, due this week, and priority overview

Charts: Visual representations of your task data

Search & Filter
Use the search bar to find tasks by keyword

Filter tasks by status using the sidebar navigation

Sort tasks by due date, creation date, title, or status

📁 Project Structure
taskflow/
├── frontend/
│   ├── index.html          # Main frontend application
│   ├── style.css           # Styles and responsive design
│   └── script.js           # Frontend JavaScript logic
├── main/
│   ├── app.py              # Flask backend server
├── core/
│   ├── tasks.py        # Task management logic
│   ├── merge_sort.py   # Sorting algorithm implementation
│   └── visualization.py # Chart generation
├── db/
│   └── database.py     # Database connection and setup
└── helpers/
    └── helper.py       # Utility functions

🔧 API Endpoints
Method	Endpoint	Description
GET	/api/tasks	Get all tasks with filtering
POST	/api/tasks	Create a new task
GET	/api/tasks/{id}	Get a specific task
PUT	/api/tasks/{id}	Update a task
DELETE	/api/tasks/{id}	Delete a task
GET	/api/tasks/search	Search tasks by keyword
GET	/api/stats	Get task statistics
GET	/api/charts	Get visualization charts

Adding Features
The modular architecture makes it easy to extend:

Add new task fields in the modal form

Create new chart types in visualization.py

Implement additional sorting algorithms

Add user authentication and multi-user support

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request