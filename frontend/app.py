import sys
from datetime import datetime, timedelta

import pandas as pd

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QMessageBox,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QTextEdit,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QGroupBox,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from backend.database import (
    create_database,

    addUser,
    deleteUser,
    showAccountDetails,
    getUserId,
    checkLoginCredentials,
    getUserBodyweight,

    addExercise,
    getUserExercises,
    deleteExercise,

    addWorkout,
    getUserWorkouts,
    deleteWorkout,
    displayRecentWorkout,

    addWorkoutSet,
    getWorkoutSets,
    deleteWorkoutSet,

    getWeeklyMuscleGroupFrequency,
    getExerciseHistory,
)


# =========================================================
# MATPLOTLIB CANVAS
# =========================================================

class ChartCanvas(FigureCanvasQTAgg):

    def __init__(self):
        self.figure = Figure(figsize=(7, 5))
        self.axes = self.figure.add_subplot(111)

        super().__init__(self.figure)

    def clearChart(self):
        self.axes.clear()
        self.draw()


# =========================================================
# MAIN APPLICATION
# =========================================================

class GymApp(QMainWindow):

    def __init__(self):
        super().__init__()

        create_database()

        self.user_id = None
        self.username = None
        self.password = None

        self.setWindowTitle("GymApp")
        self.resize(1200, 800)

        self.pages = QStackedWidget()

        self.setCentralWidget(self.pages)

        self.login_page = self.createLoginPage()
        self.register_page = self.createRegisterPage()
        self.main_page = self.createMainApplication()

        self.pages.addWidget(self.login_page)
        self.pages.addWidget(self.register_page)
        self.pages.addWidget(self.main_page)

        self.pages.setCurrentWidget(self.login_page)


    # =====================================================
    # LOGIN
    # =====================================================

    def createLoginPage(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        layout.addStretch()

        title = QLabel("GymApp")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
        """)

        subtitle = QLabel("Track. Analyze. Improve.")
        subtitle.setAlignment(Qt.AlignCenter)

        username_label = QLabel("Username")
        self.login_username = QLineEdit()

        password_label = QLabel("Password")
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(
            QLineEdit.Password
        )

        login_button = QPushButton("Login")

        register_button = QPushButton(
            "Create Account"
        )

        login_button.clicked.connect(
            self.loginUser
        )

        register_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.register_page
            )
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        layout.addWidget(username_label)
        layout.addWidget(self.login_username)

        layout.addWidget(password_label)
        layout.addWidget(self.login_password)

        layout.addSpacing(15)

        layout.addWidget(login_button)
        layout.addWidget(register_button)

        layout.addStretch()

        return page


    def loginUser(self):

        username = (
            self.login_username
            .text()
            .strip()
        )

        password = (
            self.login_password
            .text()
            .strip()
        )

        if not username or not password:

            QMessageBox.warning(
                self,
                "Login",
                "Enter both username and password."
            )

            return

        if not checkLoginCredentials(
            username,
            password
        ):

            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password."
            )

            return

        self.user_id = getUserId(
            username,
            password
        )

        self.username = username
        self.password = password

        self.refreshAllPages()

        self.pages.setCurrentWidget(
            self.main_page
        )

        self.content_pages.setCurrentWidget(
            self.dashboard_page
        )


    # =====================================================
    # REGISTER
    # =====================================================

    def createRegisterPage(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        form = QFormLayout()

        self.register_name = QLineEdit()

        self.register_age = QSpinBox()
        self.register_age.setRange(1, 120)

        self.register_bodyweight = (
            QDoubleSpinBox()
        )

        self.register_bodyweight.setRange(
            1,
            1000
        )

        self.register_bodyweight.setSuffix(
            " lb"
        )

        self.register_username = QLineEdit()

        self.register_password = QLineEdit()
        self.register_password.setEchoMode(
            QLineEdit.Password
        )

        form.addRow(
            "Name:",
            self.register_name
        )

        form.addRow(
            "Age:",
            self.register_age
        )

        form.addRow(
            "Body Weight:",
            self.register_bodyweight
        )

        form.addRow(
            "Username:",
            self.register_username
        )

        form.addRow(
            "Password:",
            self.register_password
        )

        create_button = QPushButton(
            "Create Account"
        )

        back_button = QPushButton(
            "Back to Login"
        )

        create_button.clicked.connect(
            self.createAccount
        )

        back_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.login_page
            )
        )

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(create_button)
        layout.addWidget(back_button)

        return page


    def createAccount(self):

        name = self.register_name.text().strip()

        age = self.register_age.value()

        bodyweight = (
            self.register_bodyweight.value()
        )

        username = (
            self.register_username
            .text()
            .strip()
        )

        password = (
            self.register_password
            .text()
            .strip()
        )

        if not name or not username or not password:

            QMessageBox.warning(
                self,
                "Create Account",
                "Please fill out all fields."
            )

            return

        success = addUser(
            name,
            age,
            bodyweight,
            username,
            password
        )

        if not success:

            QMessageBox.warning(
                self,
                "Create Account",
                "That username already exists."
            )

            return

        QMessageBox.information(
            self,
            "Account Created",
            "Account created successfully."
        )

        self.login_username.setText(
            username
        )

        self.register_name.clear()
        self.register_username.clear()
        self.register_password.clear()

        self.pages.setCurrentWidget(
            self.login_page
        )


    # =====================================================
    # MAIN APPLICATION
    # =====================================================

    def createMainApplication(self):

        page = QWidget()

        main_layout = QHBoxLayout(page)

        # -------------------------
        # SIDEBAR
        # -------------------------

        sidebar = QVBoxLayout()

        title = QLabel("GymApp")

        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        dashboard_button = QPushButton(
            "Dashboard"
        )

        exercise_button = QPushButton(
            "Exercises"
        )

        workouts_button = QPushButton(
            "Workouts"
        )

        sets_button = QPushButton(
            "Workout Sets"
        )

        analytics_button = QPushButton(
            "Analytics"
        )

        account_button = QPushButton(
            "Account"
        )

        logout_button = QPushButton(
            "Logout"
        )

        sidebar.addWidget(title)

        sidebar.addSpacing(20)

        sidebar.addWidget(
            dashboard_button
        )

        sidebar.addWidget(
            exercise_button
        )

        sidebar.addWidget(
            workouts_button
        )

        sidebar.addWidget(
            sets_button
        )

        sidebar.addWidget(
            analytics_button
        )

        sidebar.addWidget(
            account_button
        )

        sidebar.addStretch()

        sidebar.addWidget(
            logout_button
        )

        # -------------------------
        # CONTENT
        # -------------------------

        self.content_pages = QStackedWidget()

        self.dashboard_page = (
            self.createDashboardPage()
        )

        self.exercise_page = (
            self.createExercisePage()
        )

        self.workout_page = (
            self.createWorkoutPage()
        )

        self.workout_set_page = (
            self.createWorkoutSetPage()
        )

        self.analytics_page = (
            self.createAnalyticsPage()
        )

        self.account_page = (
            self.createAccountPage()
        )

        self.content_pages.addWidget(
            self.dashboard_page
        )

        self.content_pages.addWidget(
            self.exercise_page
        )

        self.content_pages.addWidget(
            self.workout_page
        )

        self.content_pages.addWidget(
            self.workout_set_page
        )

        self.content_pages.addWidget(
            self.analytics_page
        )

        self.content_pages.addWidget(
            self.account_page
        )

        dashboard_button.clicked.connect(
            self.openDashboard
        )

        exercise_button.clicked.connect(
            self.openExercises
        )

        workouts_button.clicked.connect(
            self.openWorkouts
        )

        sets_button.clicked.connect(
            self.openWorkoutSets
        )

        analytics_button.clicked.connect(
            self.openAnalytics
        )

        account_button.clicked.connect(
            self.openAccount
        )

        logout_button.clicked.connect(
            self.logout
        )

        main_layout.addLayout(
            sidebar,
            1
        )

        main_layout.addWidget(
            self.content_pages,
            5
        )

        return page


    # =====================================================
    # DASHBOARD
    # =====================================================

    def createDashboardPage(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        self.dashboard_title = QLabel(
            "Dashboard"
        )

        self.dashboard_title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        self.dashboard_bodyweight = QLabel()

        self.dashboard_recent = QLabel()

        layout.addWidget(
            self.dashboard_title
        )

        layout.addSpacing(20)

        layout.addWidget(
            self.dashboard_bodyweight
        )

        layout.addWidget(
            self.dashboard_recent
        )

        layout.addStretch()

        return page


    def refreshDashboard(self):

        if self.user_id is None:
            return

        self.dashboard_title.setText(
            f"Welcome, {self.username}"
        )

        bodyweight = getUserBodyweight(
            self.user_id
        )

        self.dashboard_bodyweight.setText(
            f"Current Bodyweight: "
            f"{bodyweight} lb"
        )

        workout = displayRecentWorkout(
            self.user_id
        )

        if workout:

            self.dashboard_recent.setText(
                f"Recent Workout: "
                f"{workout[1]}\n"
                f"{workout[2]}"
            )

        else:

            self.dashboard_recent.setText(
                "No workouts recorded yet."
            )


    # =====================================================
    # EXERCISES
    # =====================================================

    def createExercisePage(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel("Exercises")

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        self.exercise_table = QTableWidget()

        self.exercise_table.setColumnCount(3)

        self.exercise_table.setHorizontalHeaderLabels([
            "ID",
            "Exercise",
            "Muscle Group"
        ])

        self.exercise_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        form = QHBoxLayout()

        self.exercise_name_input = QLineEdit()

        self.exercise_name_input.setPlaceholderText(
            "Exercise name"
        )

        self.exercise_muscle_combo = QComboBox()

        self.exercise_muscle_combo.addItems([
            "Chest",
            "Back",
            "Legs",
            "Arms",
            "Shoulders",
            "Abs"
        ])

        add_button = QPushButton(
            "Add Exercise"
        )

        delete_button = QPushButton(
            "Delete Selected"
        )

        add_button.clicked.connect(
            self.addExerciseFromGUI
        )

        delete_button.clicked.connect(
            self.deleteSelectedExercise
        )

        form.addWidget(
            self.exercise_name_input
        )

        form.addWidget(
            self.exercise_muscle_combo
        )

        form.addWidget(add_button)
        form.addWidget(delete_button)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(
            self.exercise_table
        )

        return page


    def refreshExercises(self):

        if self.user_id is None:
            return

        exercises = getUserExercises(
            self.user_id
        )

        self.exercise_table.setRowCount(
            len(exercises)
        )

        for row, exercise in enumerate(
            exercises
        ):

            for column, value in enumerate(
                exercise
            ):

                self.exercise_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(
                        str(value)
                    )
                )

        self.refreshExerciseCombo()


    def addExerciseFromGUI(self):

        name = (
            self.exercise_name_input
            .text()
            .strip()
        )

        muscle_group = (
            self.exercise_muscle_combo
            .currentText()
        )

        if not name:

            QMessageBox.warning(
                self,
                "Exercise",
                "Enter an exercise name."
            )

            return

        if addExercise(
            self.user_id,
            name,
            muscle_group
        ):

            self.exercise_name_input.clear()

            self.refreshExercises()

        else:

            QMessageBox.warning(
                self,
                "Exercise",
                "That exercise already exists."
            )


    def deleteSelectedExercise(self):

        row = (
            self.exercise_table
            .currentRow()
        )

        if row < 0:

            QMessageBox.warning(
                self,
                "Delete Exercise",
                "Select an exercise first."
            )

            return

        exercise_id = int(
            self.exercise_table
            .item(row, 0)
            .text()
        )

        deleteExercise(
            self.user_id,
            exercise_id
        )

        self.refreshExercises()


    # =====================================================
    # WORKOUTS
    # =====================================================

    def createWorkoutPage(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel("Workouts")

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        form = QFormLayout()

        self.workout_date_input = QDateEdit()

        self.workout_date_input.setDate(
            QDate.currentDate()
        )

        self.workout_date_input.setCalendarPopup(
            True
        )

        self.workout_notes_input = QTextEdit()

        self.workout_notes_input.setMaximumHeight(
            100
        )

        add_button = QPushButton(
            "Add Workout"
        )

        delete_button = QPushButton(
            "Delete Selected Workout"
        )

        add_button.clicked.connect(
            self.addWorkoutFromGUI
        )

        delete_button.clicked.connect(
            self.deleteSelectedWorkout
        )

        form.addRow(
            "Date:",
            self.workout_date_input
        )

        form.addRow(
            "Notes:",
            self.workout_notes_input
        )

        self.workout_table = QTableWidget()

        self.workout_table.setColumnCount(3)

        self.workout_table.setHorizontalHeaderLabels([
            "ID",
            "Date",
            "Notes"
        ])

        self.workout_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        layout.addWidget(self.workout_table)

        return page


    def refreshWorkouts(self):

        if self.user_id is None:
            return

        workouts = getUserWorkouts(
            self.user_id
        )

        self.workout_table.setRowCount(
            len(workouts)
        )

        for row, workout in enumerate(
            workouts
        ):

            for column, value in enumerate(
                workout
            ):

                self.workout_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(
                        str(value)
                    )
                )

        self.refreshWorkoutCombo()


    def addWorkoutFromGUI(self):

        date = (
            self.workout_date_input
            .date()
            .toString("yyyy-MM-dd")
        )

        notes = (
            self.workout_notes_input
            .toPlainText()
            .strip()
        )

        addWorkout(
            self.user_id,
            date,
            notes
        )

        self.workout_notes_input.clear()

        self.refreshWorkouts()
        self.refreshDashboard()


    def deleteSelectedWorkout(self):

        row = (
            self.workout_table
            .currentRow()
        )

        if row < 0:

            QMessageBox.warning(
                self,
                "Workout",
                "Select a workout first."
            )

            return

        workout_id = int(
            self.workout_table
            .item(row, 0)
            .text()
        )

        deleteWorkout(
            self.user_id,
            workout_id
        )

        self.refreshWorkouts()
        self.refreshDashboard()


    # =====================================================
    # WORKOUT SETS
    # =====================================================

    def createWorkoutSetPage(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel("Workout Sets")

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        form = QFormLayout()

        self.set_workout_combo = QComboBox()

        self.set_exercise_combo = QComboBox()

        self.set_number_input = QSpinBox()
        self.set_number_input.setRange(
            1,
            100
        )

        self.set_weight_input = QDoubleSpinBox()

        self.set_weight_input.setRange(
            0,
            2000
        )

        self.set_weight_input.setSuffix(
            " lb"
        )

        self.bodyweight_button = QPushButton(
            "Use Bodyweight"
        )

        self.bodyweight_button.clicked.connect(
            self.useBodyweight
        )

        self.set_reps_input = QSpinBox()

        self.set_reps_input.setRange(
            1,
            1000
        )

        add_button = QPushButton(
            "Add Set"
        )

        delete_button = QPushButton(
            "Delete Selected Set"
        )

        add_button.clicked.connect(
            self.addWorkoutSetFromGUI
        )

        delete_button.clicked.connect(
            self.deleteSelectedSet
        )

        self.set_workout_combo.currentIndexChanged.connect(
            self.refreshWorkoutSetTable
        )

        form.addRow(
            "Workout:",
            self.set_workout_combo
        )

        form.addRow(
            "Exercise:",
            self.set_exercise_combo
        )

        form.addRow(
            "Set Number:",
            self.set_number_input
        )

        form.addRow(
            "Weight:",
            self.set_weight_input
        )

        form.addRow(
            "",
            self.bodyweight_button
        )

        form.addRow(
            "Reps:",
            self.set_reps_input
        )

        self.workout_set_table = QTableWidget()

        self.workout_set_table.setColumnCount(
            5
        )

        self.workout_set_table.setHorizontalHeaderLabels([
            "Set ID",
            "Exercise",
            "Set",
            "Weight",
            "Reps"
        ])

        self.workout_set_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        layout.addWidget(
            self.workout_set_table
        )

        return page


    def refreshWorkoutCombo(self):

        self.set_workout_combo.clear()

        if self.user_id is None:
            return

        workouts = getUserWorkouts(
            self.user_id
        )

        for workout in workouts:

            workout_id = workout[0]
            date = workout[1]
            notes = workout[2]

            label = f"{date} - {notes}"

            self.set_workout_combo.addItem(
                label,
                workout_id
            )


    def refreshExerciseCombo(self):

        self.set_exercise_combo.clear()

        if self.user_id is None:
            return

        exercises = getUserExercises(
            self.user_id
        )

        for exercise in exercises:

            self.set_exercise_combo.addItem(
                exercise[1],
                exercise[0]
            )


    def useBodyweight(self):

        bodyweight = getUserBodyweight(
            self.user_id
        )

        if bodyweight is not None:

            self.set_weight_input.setValue(
                bodyweight
            )


    def addWorkoutSetFromGUI(self):

        workout_id = (
            self.set_workout_combo
            .currentData()
        )

        exercise_id = (
            self.set_exercise_combo
            .currentData()
        )

        if workout_id is None:

            QMessageBox.warning(
                self,
                "Workout Set",
                "Add a workout first."
            )

            return

        if exercise_id is None:

            QMessageBox.warning(
                self,
                "Workout Set",
                "Add an exercise first."
            )

            return

        addWorkoutSet(
            workout_id,
            exercise_id,
            self.set_number_input.value(),
            self.set_weight_input.value(),
            self.set_reps_input.value()
        )

        self.refreshWorkoutSetTable()


    def refreshWorkoutSetTable(self):

        workout_id = (
            self.set_workout_combo
            .currentData()
        )

        if workout_id is None:

            self.workout_set_table.setRowCount(
                0
            )

            return

        sets = getWorkoutSets(
            workout_id
        )

        self.workout_set_table.setRowCount(
            len(sets)
        )

        for row, workout_set in enumerate(
            sets
        ):

            for column, value in enumerate(
                workout_set
            ):

                self.workout_set_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(
                        str(value)
                    )
                )


    def deleteSelectedSet(self):

        row = (
            self.workout_set_table
            .currentRow()
        )

        if row < 0:

            QMessageBox.warning(
                self,
                "Workout Set",
                "Select a set first."
            )

            return

        set_id = int(
            self.workout_set_table
            .item(row, 0)
            .text()
        )

        deleteWorkoutSet(
            self.user_id,
            set_id
        )

        self.refreshWorkoutSetTable()


    # =====================================================
    # ANALYTICS
    # =====================================================

    def createAnalyticsPage(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel("Analytics")

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        self.analytics_exercise_combo = (
            QComboBox()
        )

        self.analytics_date = QDateEdit()

        self.analytics_date.setDate(
            QDate.currentDate()
        )

        self.analytics_date.setCalendarPopup(
            True
        )

        button_layout = QHBoxLayout()

        muscle_button = QPushButton(
            "Weekly Frequency"
        )

        overload_button = QPushButton(
            "Progressive Overload"
        )

        one_rm_button = QPushButton(
            "Estimated 1RM"
        )

        statistics_button = QPushButton(
            "Statistics"
        )

        muscle_button.clicked.connect(
            self.showWeeklyFrequencyChart
        )

        overload_button.clicked.connect(
            self.showOverloadChart
        )

        one_rm_button.clicked.connect(
            self.showOneRMChart
        )

        statistics_button.clicked.connect(
            self.showStatistics
        )

        button_layout.addWidget(
            muscle_button
        )

        button_layout.addWidget(
            overload_button
        )

        button_layout.addWidget(
            one_rm_button
        )

        button_layout.addWidget(
            statistics_button
        )

        self.chart_canvas = ChartCanvas()

        self.statistics_label = QLabel()

        layout.addWidget(title)

        layout.addWidget(
            QLabel("Exercise:")
        )

        layout.addWidget(
            self.analytics_exercise_combo
        )

        layout.addWidget(
            QLabel(
                "Select any date for weekly analysis:"
            )
        )

        layout.addWidget(
            self.analytics_date
        )

        layout.addLayout(
            button_layout
        )

        layout.addWidget(
            self.chart_canvas
        )

        layout.addWidget(
            self.statistics_label
        )

        return page


    def refreshAnalyticsExercises(self):

        self.analytics_exercise_combo.clear()

        if self.user_id is None:
            return

        exercises = getUserExercises(
            self.user_id
        )

        for exercise in exercises:

            self.analytics_exercise_combo.addItem(
                exercise[1],
                exercise[0]
            )


    def showWeeklyFrequencyChart(self):

        selected = (
            self.analytics_date
            .date()
            .toPython()
        )

        start_date = selected - timedelta(
            days=selected.weekday()
        )

        end_date = start_date + timedelta(
            days=6
        )

        data = getWeeklyMuscleGroupFrequency(
            self.user_id,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

        self.chart_canvas.axes.clear()

        if not data:

            self.chart_canvas.axes.set_title(
                "No workout data for this week"
            )

            self.chart_canvas.draw()

            return

        df = pd.DataFrame(
            data,
            columns=[
                "muscle_group",
                "frequency"
            ]
        )

        self.chart_canvas.axes.bar(
            df["muscle_group"],
            df["frequency"]
        )

        self.chart_canvas.axes.axhline(
            y=2,
            linestyle="--",
            label="Goal: 2x"
        )

        self.chart_canvas.axes.set_title(
            "Weekly Muscle Group Frequency"
        )

        self.chart_canvas.axes.set_ylabel(
            "Workouts"
        )

        self.chart_canvas.axes.grid(
            axis="y",
            linestyle="--",
            alpha=0.4
        )

        self.chart_canvas.axes.legend()

        self.chart_canvas.figure.tight_layout()

        self.chart_canvas.draw()


    def getSelectedExerciseHistory(self):

        exercise_id = (
            self.analytics_exercise_combo
            .currentData()
        )

        exercise_name = (
            self.analytics_exercise_combo
            .currentText()
        )

        if exercise_id is None:

            return None, None

        data = getExerciseHistory(
            self.user_id,
            exercise_id
        )

        return exercise_name, data


    def showOverloadChart(self):

        exercise_name, data = (
            self.getSelectedExerciseHistory()
        )

        if not data:
            return

        df = pd.DataFrame(
            data,
            columns=[
                "workout_date",
                "weight",
                "reps"
            ]
        )

        df["workout_date"] = pd.to_datetime(
            df["workout_date"]
        )

        progression = (
            df.groupby(
                "workout_date"
            )["weight"]
            .max()
            .reset_index()
        )

        self.chart_canvas.axes.clear()

        self.chart_canvas.axes.plot(
            progression["workout_date"],
            progression["weight"],
            marker="o",
            linewidth=2
        )

        self.chart_canvas.axes.set_title(
            f"{exercise_name} Progressive Overload"
        )

        self.chart_canvas.axes.set_ylabel(
            "Highest Weight (lb)"
        )

        self.chart_canvas.axes.grid(
            linestyle="--",
            alpha=0.4
        )

        self.chart_canvas.figure.tight_layout()

        self.chart_canvas.draw()


    def showOneRMChart(self):

        exercise_name, data = (
            self.getSelectedExerciseHistory()
        )

        if not data:
            return

        df = pd.DataFrame(
            data,
            columns=[
                "workout_date",
                "weight",
                "reps"
            ]
        )

        df["workout_date"] = pd.to_datetime(
            df["workout_date"]
        )

        df["estimated_1rm"] = df.apply(
            lambda row:
                row["weight"]
                if row["reps"] == 1
                else row["weight"]
                * (1 + row["reps"] / 30),
            axis=1
        )

        progression = (
            df.groupby(
                "workout_date"
            )["estimated_1rm"]
            .max()
            .reset_index()
        )

        self.chart_canvas.axes.clear()

        self.chart_canvas.axes.plot(
            progression["workout_date"],
            progression["estimated_1rm"],
            marker="o",
            linewidth=2
        )

        self.chart_canvas.axes.set_title(
            f"{exercise_name} Estimated 1RM"
        )

        self.chart_canvas.axes.set_ylabel(
            "Estimated 1RM (lb)"
        )

        self.chart_canvas.axes.grid(
            linestyle="--",
            alpha=0.4
        )

        self.chart_canvas.figure.tight_layout()

        self.chart_canvas.draw()


    def showStatistics(self):

        exercise_name, data = (
            self.getSelectedExerciseHistory()
        )

        if not data:
            return

        df = pd.DataFrame(
            data,
            columns=[
                "workout_date",
                "weight",
                "reps"
            ]
        )

        df["volume"] = (
            df["weight"]
            * df["reps"]
        )

        maximum = df["weight"].max()
        minimum = df["weight"].min()

        statistics = (
            f"{exercise_name} Statistics\n\n"
            f"Total Workouts: "
            f"{df['workout_date'].nunique()}\n"
            f"Total Sets: {len(df)}\n\n"
            f"Mean Weight: "
            f"{df['weight'].mean():.1f} lb\n"
            f"Median Weight: "
            f"{df['weight'].median():.1f} lb\n"
            f"Minimum: {minimum:.1f} lb\n"
            f"Maximum: {maximum:.1f} lb\n"
            f"Range: "
            f"{maximum - minimum:.1f} lb\n"
            f"Average Reps: "
            f"{df['reps'].mean():.1f}\n"
            f"Total Volume: "
            f"{df['volume'].sum():.1f} lb"
        )

        self.statistics_label.setText(
            statistics
        )


    # =====================================================
    # ACCOUNT PAGE
    # =====================================================

    def createAccountPage(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel("Account")

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        self.account_details = QLabel()

        delete_button = QPushButton(
            "Delete Account"
        )

        delete_button.clicked.connect(
            self.deleteCurrentAccount
        )

        layout.addWidget(title)
        layout.addWidget(
            self.account_details
        )

        layout.addStretch()

        layout.addWidget(
            delete_button
        )

        return page


    def refreshAccount(self):

        if self.username is None:
            return

        user = showAccountDetails(
            self.username,
            self.password
        )

        if not user:
            return

        self.account_details.setText(
            f"User ID: {user[0]}\n"
            f"Name: {user[1]}\n"
            f"Age: {user[2]}\n"
            f"Body Weight: {user[3]} lb\n"
            f"Username: {user[4]}"
        )


    def deleteCurrentAccount(self):

        result = QMessageBox.question(
            self,
            "Delete Account",
            "Are you sure you want to "
            "delete your account?"
        )

        if result != QMessageBox.Yes:
            return

        if deleteUser(self.user_id):

            QMessageBox.information(
                self,
                "Account",
                "Account deleted."
            )

            self.logout()


    # =====================================================
    # PAGE NAVIGATION
    # =====================================================

    def openDashboard(self):

        self.refreshDashboard()

        self.content_pages.setCurrentWidget(
            self.dashboard_page
        )


    def openExercises(self):

        self.refreshExercises()

        self.content_pages.setCurrentWidget(
            self.exercise_page
        )


    def openWorkouts(self):

        self.refreshWorkouts()

        self.content_pages.setCurrentWidget(
            self.workout_page
        )


    def openWorkoutSets(self):

        self.refreshWorkoutCombo()
        self.refreshExerciseCombo()
        self.refreshWorkoutSetTable()

        self.content_pages.setCurrentWidget(
            self.workout_set_page
        )


    def openAnalytics(self):

        self.refreshAnalyticsExercises()

        self.content_pages.setCurrentWidget(
            self.analytics_page
        )


    def openAccount(self):

        self.refreshAccount()

        self.content_pages.setCurrentWidget(
            self.account_page
        )


    # =====================================================
    # REFRESH
    # =====================================================

    def refreshAllPages(self):

        self.refreshDashboard()
        self.refreshExercises()
        self.refreshWorkouts()
        self.refreshWorkoutCombo()
        self.refreshExerciseCombo()
        self.refreshAnalyticsExercises()
        self.refreshAccount()


    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        self.user_id = None
        self.username = None
        self.password = None

        self.login_username.clear()
        self.login_password.clear()

        self.pages.setCurrentWidget(
            self.login_page
        )


# =========================================================
# START APPLICATION
# =========================================================

def runApp():

    app = QApplication(sys.argv)

    window = GymApp()

    window.show()

    sys.exit(
        app.exec()
    )