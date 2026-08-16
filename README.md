# Gym Progress Tracker

A desktop workout tracking and analytics application built with **Python, SQLite, PySide6, Pandas, and Matplotlib**.

Gym Progress Tracker allows users to create an account, manage exercises, record workouts and individual sets, and analyze their training progress through statistics and visualizations.

The project was built to combine database management, Python application logic, data analysis, and a desktop graphical interface into one complete application.

---

## Features

### User Accounts
- Create an account
- Login/logout
- View account information
- Delete account
- User-specific workout data

### Exercise Management
- Add exercises
- Assign exercises to muscle groups
- View saved exercises
- Delete exercises

Supported muscle groups include:

- Chest
- Back
- Legs
- Arms
- Shoulders
- Abs

### Workout Tracking
- Create workouts by date
- Add workout notes
- View previous workouts
- Delete workouts
- View most recent workout

### Workout Sets
Track individual sets including:

- Exercise
- Set number
- Weight
- Repetitions
- Bodyweight exercises

Sets are associated with both a workout and an exercise through the SQLite database.

### Analytics

GymApp analyzes stored workout data and provides several training visualizations.

#### Weekly Muscle Group Frequency

Displays how frequently each muscle group was trained during a selected week and compares it against a goal of training each muscle group twice per week.

#### Progressive Overload

Tracks the highest weight used for an exercise across multiple workouts to visualize strength progression over time.

#### Estimated One-Rep Max

Calculates and graphs estimated one-rep max progression using workout weight and repetition data.

The estimate uses the Epley formula:

```text
Estimated 1RM = Weight × (1 + Reps / 30)
```

#### Exercise Statistics

Provides statistics based on recorded exercise history, including measurements such as average, minimum, and maximum training values.

#### What-If Projection

Allows users to project future lifting weight based on a starting weight, planned increase, and number of progression periods.

---

## Screenshots

### Login

<img width="1488" height="1024" alt="Screenshot 2026-08-15 192347" src="https://github.com/user-attachments/assets/cb4dec05-40b8-4c79-8f7a-1e58da516fef" />

### Workout Set Tracking

<img width="1488" height="1039" alt="Screenshot 2026-08-15 192411" src="https://github.com/user-attachments/assets/4c5da05b-9b79-45db-b234-9963993675df" />

### Training Analytics

<img width="1486" height="1033" alt="Screenshot 2026-08-15 192447" src="https://github.com/user-attachments/assets/45b2d863-07b1-4c24-8ba7-edef634d7af8" />

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| SQLite | Persistent relational database |
| SQL | CRUD operations, filtering, joins, and data retrieval |
| PySide6 | Desktop graphical user interface |
| Pandas | Workout data processing and statistics |
| Matplotlib | Training graphs and visualizations |
| QSS | Desktop application styling |
| PyInstaller | Windows executable packaging |

---

## Project Structure


### `main.py`

Entry point for the desktop application.

It launches the PySide6 frontend.

### `frontend/app.py`

Contains the graphical user interface, including:

- Login and registration
- Navigation
- Forms
- Tables
- Workout management
- Exercise management
- Analytics interface
- Matplotlib integration

### `frontend/style.qss`

Contains the application's visual styling.

The interface uses a crimson, gray, black, and white color scheme inspired by Washington State University.

### `backend/database.py`

Handles communication between Python and SQLite.

Responsibilities include:

- Database connections
- User management
- Exercise management
- Workout management
- Workout set management
- SQL queries
- Analytics data retrieval

### `backend/charts.py`

Contains workout analytics and visualization logic using Pandas and Matplotlib.

### `sql/schema.sql`

Defines the relational database structure used by the application.

### `cli.py`

Contains the original command-line version of GymApp.

The CLI was retained to show the application's progression from a terminal-based interface to a full desktop GUI.

---

## Database Structure

GymApp uses a relational SQLite database built around four primary tables:
```

### Users

Stores account information and bodyweight.

### Exercises

Stores exercises created by each user and their associated muscle groups.

### Workouts

Stores workout sessions, dates, and notes.

### Workout Sets

Connects exercises with workouts and stores:

```text
set number
weight
repetitions
```

Foreign keys are enabled to maintain relationships between records, with cascading deletion used where appropriate.

```

The frontend collects user input through PySide6 widgets and sends the requested operations to the backend.

The backend executes SQL queries against SQLite and returns the requested information.

Workout history can then be processed using Pandas and visualized using Matplotlib inside the desktop interface.

---

## Running From Source

### 1. Clone the repository

```bash
git clone <repository-url>
cd GymApp
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run GymApp

```bash
python main.py
```

---

## Requirements

The primary external dependencies are:

```text
PySide6
pandas
matplotlib
```

Python standard-library modules such as `sqlite3`, `datetime`, `pathlib`, and `os` are also used.

---

## Windows Application

GymApp can also be packaged as a standalone Windows executable using PyInstaller.

The executable allows the application to be launched directly without running:

```bash
python main.py
```

User database information is stored separately in the user's local application-data directory so workout information remains persistent between application launches.

---

## What I Learned

Building GymApp gave me experience connecting multiple areas of software development within a single project, including:

- Designing relational SQL tables
- Writing SQL queries and joins
- Implementing CRUD operations
- Connecting Python to SQLite
- Organizing backend and frontend code
- Working with Python classes and functions
- Processing data with Pandas
- Creating visualizations with Matplotlib
- Building event-driven desktop interfaces with PySide6
- Connecting GUI events to backend operations
- Managing persistent application data
- Packaging a Python application as a Windows executable

One of the main goals of this project was understanding how the different layers of an application communicate rather than treating the database, backend, analytics, and frontend as separate concepts.

---

## Future Improvements

GymApp V1 is feature complete, but possible future improvements include:

- Password hashing and improved authentication security
- Editing existing workouts and sets
- Additional analytics
- Exporting workout history
- More advanced progression recommendations
- Additional user customization

---

## Author

**Anthony Alperov**

Software Engineering Student  
Washington State University
