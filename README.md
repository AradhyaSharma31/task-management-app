🌟 TaskFlow

A modern, feature-rich task management application with a beautiful interface and powerful functionality.

🚀 Features
🧩 Core Functionality

✅ Task Management – Create, read, update, and delete tasks

📊 Dashboard – Overview with statistics and recent tasks

🔍 Smart Search – Find tasks by title or description

🎯 Filtering & Sorting – Filter by status and sort by various criteria

📈 Analytics – Visual charts and performance metrics

🎨 Beautiful UI – Modern design with gradients and animations

⚙️ Advanced Features

⚡ Merge Sort Algorithm – Efficient sorting of tasks

📉 Data Visualization – Pie charts, bar charts, and trend analysis

📱 Responsive Design – Works perfectly on desktop and mobile devices

🛠️ Tech Stack
💻 Frontend

HTML5 – Semantic markup

CSS3 – Modern styling with CSS variables and gradients

JavaScript (ES6+) – Vanilla JS with async/await

Font Awesome – Beautiful icons

Google Fonts – Inter font family

🔧 Backend

Python – Backend logic

Flask – Web framework

PostgreSQL – Database (configurable, supports SQLite for dev)

Matplotlib – Chart generation

📦 Installation
🧰 Prerequisites

Python 3.8+

PostgreSQL (or SQLite for local development)

Modern web browser

⚙️ Backend Setup
# Clone the repository
git clone <repository-url>
cd taskflow

# Install dependencies
pip install -r requirements.txt

# Set up the database
python db/database.py

# Start the Flask server
python app.py


Backend runs at http://localhost:5000

💻 Frontend Setup
# Option 1: Open directly
open frontend/index.html

# Option 2: Serve locally
# Using Python
python -m http.server 8000

# Or using Node.js
npx serve .


Frontend runs at http://localhost:8000

🎯 Usage
🗂️ Managing Tasks

Create Tasks: Click "New Task" to add a task (title, description, due date)

View Tasks: Browse all tasks or filter by status (Pending/Completed)

Complete Tasks: Click ✅ to mark as complete

Edit Tasks: Click ✏️ to modify task details

Delete Tasks: Click 🗑️ to remove tasks

📊 Dashboard

Statistics Cards: Total tasks, pending, completed, and completion rate

Recent Tasks: View recently created tasks

Quick Stats: Overdue tasks, due this week, and priority overview

Charts: Visual insights for task data

🔍 Search & Filter

Use the search bar to find tasks by keyword

Filter by status (pending/completed)

Sort by due date, creation date, title, or status

📁 Project Structure
taskflow/
├── frontend/
│   ├── index.html          # Main frontend application
│   ├── style.css           # Styles and responsive design
│   └── script.js           # Frontend JavaScript logic
│
├── main/
│   └── app.py              # Flask backend server
│
├── core/
│   ├── tasks.py            # Task management logic
│   ├── merge_sort.py       # Sorting algorithm implementation
│   └── visualization.py    # Chart generation
│
├── db/
│   └── database.py         # Database connection and setup
│
└── helpers/
    └── helper.py           # Utility functions

🔧 API Endpoints
Method	Endpoint	Description
GET	/api/tasks	Get all tasks (with filters)
POST	/api/tasks	Create a new task
GET	/api/tasks/{id}	Get a specific task
PUT	/api/tasks/{id}	Update a task
DELETE	/api/tasks/{id}	Delete a task
GET	/api/tasks/search	Search tasks by keyword
GET	/api/stats	Get task statistics
GET	/api/charts	Get visualization charts
🧩 Adding Features

TaskFlow’s modular design makes extension easy:

➕ Add new task fields in the modal form

📊 Create new chart types in visualization.py

⚙️ Implement more sorting algorithms

🔐 Add authentication and multi-user support

🤝 Contributing

Fork the repository

Create a new branch

git checkout -b feature/amazing-feature


Commit your changes

git commit -m "Add amazing feature"


Push to your branch

git push origin feature/amazing-feature


Open a Pull Request 🎉