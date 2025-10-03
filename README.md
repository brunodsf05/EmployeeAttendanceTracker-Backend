# EmployeeAttendanceTracker-Backend

This project is a service for managing employee attendance.

You are currently looking at the **backend**, built with **Python**, **Flask**, and **SQLAlchemy**.



## ✨ Features
-   🔐 **User Authentication**: Secure login for administrators.
-   🏢 **Company management**: Change company name and location with ease.
-   🧑‍💼 **Employees management**: Add employees or deactivate them.
-   📊 **Attendance Records**: Query presence and absence logs for each employee.
-   ⌛ **Powerful testing**: Change the server time to quickly test the clock in/out system.



## ⚙️ Prerequisites

### ✅ Required
-   🐍 **Python** 3.10 or higher
-   📦 All dependencies listed in `requirements.txt`

### 🧩 Optional
-   🌀 **Git** to clone this repository
-   🛠️ **Make** to run server maintenance tasks quickly



## 📥 Installation and Setup

### 🌀 Clone the repository
```sh
git clone https://github.com/brunodsf05/EmployeeAttendanceTracker-Backend.git
cd EmployeeAttendanceTracker-Backend
```

### 🔑 Environment Variables
Depending on what you want to do...
-   **I want to quickly test this project:**
    1.  Copy `.env.example` to `.env`. The database is stored in memory.

-   **I want to deploy this project in a more serious way:**
    1.  Copy `.env.example` to `.env`.
    2.  Modify the variables. Especially the secrets.

### 📦 Dependencies and DB
Install the dependencies and initialize the database.

> [!NOTE]  
> From now every code blocks with commands has a Make alias you can run instead of everything else. Example: `make i`

```sh
# make i
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
```



## 🛠️ Maintenance
This section assumes you have completed _Installation and Setup_.

### 🗄️ Database
If you want to modify some **database models** or use a different **database** run:

```sh
# make m
flask db migrate
flask db upgrade
```

### 🏃‍♂️‍➡️ Running the Server
Some hostings automatically execute **Flask** for you, but anyways, if you are in a testing environment run:

```sh
# make r
flask run --host=0.0.0.0 --port=5000 # THis will allow any device in yout network connecto to the server
```

If you need mock data, open a new terminal (yes, while flask is running in the background) and open a flask shell:
```sh
flask shell
```

Inside copy the next line to create all the necessary models.
```python
mockdata_create()
```

> [!IMPORTANT]  
> If you are testing and want to restart the database with mockdata_create(), it is recommended to delete all rows.
> To do so: 1. Delete `instance` and `migrations` folder. 2. Execute again `flask db init && flask db migrate && flask db upgrade`.



## 📂 Project Structure
-   📌 `app.py` Main Flask application file
-   ⚙️ `config.py` Application configuration
-   🔗 `extensions.py` Initialization of extensions (SQLAlchemy, JWT, etc.)
-   🗃️ `models/` Database ORM models
-   🌐 `resources/` REST API endpoints
-   🖼️ `templates/` HTML templates (admin web interface)
-   📋 `web/` Forms and functions related to the web interface
-   🧪 `mockdata.py` Script to generate sample data