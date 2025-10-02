# EmployeeAttendanceTracker-Backend

This project is a service for managing employee attendance.

You are currently looking at the **backend**, built with **Python**, **Flask**, and **SQLAlchemy**.



## ✨ Features
-   🔐 **User Authentication**: Secure login for administrators and employees.
-   🕒 **Clock In/Out**: Employees can register entry and exit times.
-   📊 **Attendance Records**: Store and query presence and absence logs.
-   📅 **Schedule Management**: Administrators can configure working hours.



## ⚙️ Prerequisites

### ✅ Required
-   🐍 **Python** 3.10 or higher
-   📦 All dependencies listed in `requirements.txt`

### 🧩 Optional
-   🌀 **Git** to clone this repository
-   🛠️ **Make** to run server maintenance tasks quickly



## 📥 Installation and Setup
Clone the repository:
```sh
git clone https://github.com/brunodsf05/EmployeeAttendanceTracker-Backend.git
cd EmployeeAttendanceTracker-Backend
```

> [!NOTE]  
> Each code block with commands has a Make alias you can run instead. Example: `make i`

Then install the dependencies and initialize the database.
```sh
# make i
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
```

### 🔑 Environment Variables
These are required. Copy `.env.example` to `.env` and fill in the values.
The variables are read after each `flask run`.



## 🛠️ Maintenance
This section assumes you have completed _Installation and Setup_.

### 🗄️ Database
If you want to modify some **database models** run:

```sh
# make m
flask db migrate
flask db upgrade
```

### 🏃‍♂️‍➡️ Running the Server
Start the development server:

```sh
# make r
flask run
```



## 📂 Project Structure
-   📌 `app.py` Main Flask application file
-   ⚙️ `config.py` Application configuration
-   🔗 `extensions.py` Initialization of extensions (SQLAlchemy, JWT, etc.)
-   🗃️ `models/` Database ORM models
-   🌐 `resources/` REST API endpoints
-   🖼️ `templates/` HTML templates (admin web interface)
-   📋 `web/` Forms and functions related to the web interface
-   🧪 `mockdata.py` Script to generate sample data