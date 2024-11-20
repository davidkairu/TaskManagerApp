# Task Manager App

A simple and user-friendly Task Manager web application built with Flask. This app allows users to register, log in, and manage their tasks efficiently with features like task creation, editing, completion toggling, and deletion.

## Features

### User Authentication:
- Secure user registration and login.
- Session-based authentication to protect user data.

### Task Management:
- Add tasks with priority levels (High, Medium, Low).
- Edit task details.
- Toggle task completion status.
- Delete tasks.

### Database Integration:
- SQLite for task and user data storage.
- Persistent and relational data management.

### Responsive User Interface:
- Simple and intuitive design with CSS styling.

## Technologies Used

### Frontend:
- HTML5, CSS3 (via a static/style.css file).

### Backend:
- Flask (Python web framework).
- SQLite (database).

### Production:
- gunicorn for deploying the application.

## Setup and Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/TaskManager.git
cd TaskManager
```

### 2. Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # For macOS/Linux
.venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up the Database
Run the `db_setup.py` script to create the SQLite database and required tables:
```bash
python db_setup.py
```
Verify the database (`tasks.db`) is created with the `users` and `tasks` tables.

### 5. Run the Application
Start the Flask development server:
```bash
flask run
```
The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

You can also access the deployed version of the application at [https://taskmanagerapp-o3gl.onrender.com/](https://taskmanagerapp-o3gl.onrender.com/).

## Usage

### Register:
- Navigate to `/register` to create an account.
- Enter a unique username and password.

### Log In:
- Log in using your credentials at `/login`.

### Task Management:
- **Add a task**: Enter task details and select a priority.
- **Edit a task**: Click "Edit" next to a task and modify its details.
- **Mark as completed**: Toggle a task's completion status by clicking "Mark as Completed."
- **Delete a task**: Remove a task by clicking "Remove."

## Project Structure
```
TaskManager/
├── app.py                 # Main Flask application
├── db_setup.py            # Script to set up the SQLite database
├── tasks.db               # SQLite database file (auto-created by db_setup.py)
├── requirements.txt       # Python dependencies
├── Procfile               # Deployment configuration for Render/Heroku
├── README.md              # Project documentation
├── static/
│   ├── style.css          # CSS file for styling the app
├── templates/
│   ├── index.html         # Homepage template
│   ├── login.html         # Login page template
│   ├── register.html      # Registration page template
│   ├── edit.html          # Task editing page template
```

## Deployment

### Render Deployment

Push the project to GitHub:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

Go to Render and create a new Web Service.

Configure the deployment:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- Add a persistent disk if needed for SQLite.

## Contributing

1. Fork the repository.
2. Create a feature branch:
```bash
git checkout -b feature-name
```
3. Commit your changes:
```bash
git commit -m "Add feature-name"
```
4. Push the branch:
```bash
git push origin feature-name
```
5. Create a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or suggestions, contact:

- **Name**: David Kairu
- **Email**: [davidnjoroge560@gmail.com] 
- **GitHub**: [https://github.com/davidkairu](https://github.com/davidkairu)

