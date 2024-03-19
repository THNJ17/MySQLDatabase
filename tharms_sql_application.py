import mysql.connector
from mysql.connector import errorcode
import datetime

# SQL Database Project

#Establishing a connection with the database, accepting password from main
def establish_connection(password):
    try:
        connection = mysql.connector.connect(
            user='root',
            password=password,
            host='localhost',
            database='tharms_db'
        )
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid Credentials")
            return None
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Invalid Database")
            return None
    else:
        print("Connection successful \n")
        return connection
#name kinda explanatory, it exists to display an enrolled student id's courses
def display_enrolled_courses(connection, student_id):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT course_id FROM enrollments WHERE student_id = %s", (student_id,))
        enrolled_courses = cursor.fetchall()

        if not enrolled_courses:
            print("Student is not currently enrolled in any courses.")
            cursor.close()

        print(f"Enrolled Courses for Student ID {student_id}:")
        for enrollment in enrolled_courses:
            print(f"Course Name: {enrollment[0]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()

#displays the courses for users (particularly instructors and students and their needing to see courses for certain decisions
#like enrolling or dropping courses)
def display_courses(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT course_id, course_name FROM courses")
        courses = cursor.fetchall()

        print("Available Courses:")
        for course in courses:
            print(f"Course ID: {course[0]}, Course Name: {course[1]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()

#contains all the students' menu choices for the database
def student(connection):
    #gets the time to update the timestamp for any changes
    last_update = datetime.date.today()

    #establish a cursor for database interaction
    cursor = connection.cursor()
    student_id = int(input("Enter Student ID: "))
    status = False
    #Student option menu
    while not status:
        menu = int(input("Menu Options:[ (1 - Enroll in a course) (2- Student ID's currently enrolled courses) (3 - Drop a course) (4- exit back to first menu) ]: "))
        if menu == 1:
            # Grabs the data from display_courses so students can see the courses offered
            display = display_courses(connection)
            course_id = input("Enter the Course ID you want to enroll in: ")
            #enrolls a student
            try:
                cursor.execute("INSERT INTO enrollments (student_id, course_id, last_update) VALUES (%s, %s, %s)",
                               (student_id, course_id, last_update))
                connection.commit()
                print("Enrollment successful.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()

        elif menu == 2:
            #grabs all the courses the student is enrolled in, making it easier to display what courses they are in
            display_enrolled_courses(connection, student_id)

        elif menu == 3:
            #so the user can see the current courses the student id is enrolled in, making it easier on them
            display_enrolled_courses(connection, student_id)
            #drops a course the student is in
            try:
                course_id = input("Enter the course ID to drop: ")
                cursor.execute("DELETE FROM enrollments WHERE student_id = %s AND course_id = %s",
                               (student_id, course_id))
                connection.commit()
                print("Course dropped successfully.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()


        elif menu == 4:
            #exits the student menu loop to jump back into the main menu loop
            status = True

        else:
            print("Please select a valid number. \n")

            cursor.close()


#create users function, designed to create a new user/entity in specific tables (users, students, instructors, admins)
def create_users(connection, cursor, last_update):
    status = False
    cursor = connection.cursor()


    while not status:
        entity = input("Create a user entity, student entity, instructor entity, or admin entity"
                       "\n Please type user, student, instructor, or admin for their respective prompts. type exit to exit ").lower()
        if entity == "user":
            try:
                user_id = input("Enter user ID: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                access_level = input("Enter access level: ")
                email = input("Enter email: ")
                cursor.execute("INSERT INTO users (`user_id`, `username`, `password`, `first_name`, `last_name`, `access_level`, `email`, `last_update`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                               (user_id, username, password, first_name, last_name, access_level, email, last_update))
                connection.commit()
                print("Created.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "student":
            try:
                student_id = input("Enter student ID: ")
                user_id = input("Enter user ID: ")
                cursor.execute(
                    "INSERT INTO students (`student_id`, `user_id`, `enrollment_date`) VALUES (%s, %s, %s)",
                    (student_id, user_id, last_update))
                connection.commit()
                print("Created.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "instructor":
            try:
                instructor_id = input("Enter instructor ID: ")
                user_id = input("Enter user ID: ")
                cursor.execute(
                    "INSERT INTO instructors (`instructor_id`, `user_id`, `last_update`) VALUES (%s, %s, %s)",
                    (instructor_id, user_id, last_update))
                connection.commit()
                print("Created.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "admin":
            try:
                admin_id = input("Enter admin ID: ")
                user_id = input("Enter user ID: ")
                cursor.execute(
                    "INSERT INTO admins (`admin_id`, `user_id`, `last_update`) VALUES (%s, %s, %s)",
                    (admin_id, user_id, last_update))
                connection.commit()
                print("Created.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "exit":
            status = True

        else:
            print("Invalid input")

#Gets, reads, and displays information about specific entity
def read_users(connection, cursor, last_update):
    status = False
    cursor = connection.cursor()

    while not status:
        entity = input("Read a user entity, student entity, instructor entity, or admin entity"
                       "\n Please type user, student, instructor, or admin for their respective prompts. type exit to exit ").lower()
        if entity == "user":
            try:
                user_id = input("Enter user ID to retrieve information: ")
                cursor.execute("SELECT * FROM users WHERE `user_id` = %s", (user_id,))
                result = cursor.fetchone()

                if result:
                    print("User Information:")
                    print(f"User ID: {result[0]}")
                    print(f"Username: {result[1]}")
                    print(f"Password: {result[2]}")
                    print(f"First Name: {result[3]}")
                    print(f"Last Name: {result[4]}")
                    print(f"Access Level: {result[5]}")
                    print(f"Email: {result[6]}")
                    print(f"Last Update: {result[7]}")
                else:
                    print("User not found.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        elif entity == "student":
            try:
                student_id = input("Enter student ID to retrieve information: ")
                cursor.execute("SELECT * FROM students WHERE `student_id` = %s", (student_id,))
                result = cursor.fetchone()

                if result:
                    print("Student Information:")
                    print(f"Student ID: {result[0]}")
                    print(f"User ID: {result[1]}")
                    print(f"Enrollment Date: {result[2]}")
                else:
                    print("Student not found.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        elif entity == "instructor":
            try:
                instructor_id = input("Enter instructor ID to retrieve information: ")
                cursor.execute("SELECT * FROM instructors WHERE `instructor_id` = %s", (instructor_id,))
                result = cursor.fetchone()

                if result:
                    print("Instructor Information:")
                    print(f"Instructor ID: {result[0]}")
                    print(f"User ID: {result[1]}")
                    print(f"Last Update: {result[2]}")
                else:
                    print("Instructor not found.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        elif entity == "admin":
            try:
                admin_id = input("Enter admin ID to retrieve information: ")
                cursor.execute("SELECT * FROM admins WHERE `admin_id` = %s", (admin_id,))
                result = cursor.fetchone()

                if result:
                    print("Admin Information:")
                    print(f"Admin ID: {result[0]}")
                    print(f"User ID: {result[1]}")
                    print(f"Last Update: {result[2]}")
                else:
                    print("Admin not found.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        elif entity == "exit":
            status = True
        else:
            print("Invalid input")

#Updates specific entity
def update_users(connection, cursor, last_update):
    status = False
    cursor = connection.cursor()

    while not status:
        entity = input(
            "Update a user entity, student entity, instructor entity, or admin entity"
                       "\n Please type user, student, instructor, or admin for their respective prompts. type exit to exit ").lower()
        if entity == "user":
            try:
                user_id = input("Enter user ID to update: ")
                username = input("Enter new username: ")
                password = input("Enter new password: ")
                first_name = input("Enter new first name: ")
                last_name = input("Enter new last name: ")
                access_level = input("Enter new access level: ")
                email = input("Enter new email: ")
                cursor.execute("UPDATE users SET `username` = %s, `password` = %s, `first_name` = %s, `last_name` = %s, `access_level` = %s, `email` = %s, `last_update` = %s WHERE `user_id` = %s",
                               (username, password, first_name, last_name, access_level, email, last_update, user_id))
                connection.commit()
                print("Updated.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "student":
            try:
                student_id = input("Enter student ID to update: ")
                user_id = input("Enter user ID to update: ")
                cursor.execute(
                    "UPDATE students SET `user_id` = %s, `last_update` = %s WHERE `student_id` = %s",
                    (user_id, last_update, student_id))
                connection.commit()
                print("Updated.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "instructor":
            try:
                instructor_id = input("Enter instructor ID to update: ")
                user_id = input("Enter user ID to update: ")
                cursor.execute(
                    "UPDATE instructors SET `user_id` = %s, `last_update` = %s WHERE `instructor_id` = %s",
                    (user_id, last_update, instructor_id))
                connection.commit()
                print("Updated.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "admin":
            try:
                admin_id = input("Enter admin ID to update: ")
                user_id = input("Enter user ID to update: ")
                cursor.execute(
                    "UPDATE admins SET `user_id` = %s, `last_update` = %s WHERE `admin_id` = %s",
                    (user_id, last_update, admin_id))
                connection.commit()
                print("Updated.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "exit":
            status = True
        else:
            print("Invalid input")


#deletes specific entities
def delete_users(connection, cursor, last_update):
    status = False
    cursor = connection.cursor()

    while not status:
        entity = input("Delete a user entity, student entity, instructor entity, or admin entity"
                       "\n Please type user, student, instructor, or admin for their respective prompts. type exit to exit ").lower()
        if entity == "user":
            try:
                user_id = input("Enter user ID to delete: ")
                cursor.execute("DELETE FROM users WHERE `user_id` = %s", (user_id,))
                connection.commit()
                print("Deleted.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "student":
            try:
                student_id = input("Enter student ID to delete: ")
                cursor.execute("DELETE FROM students WHERE `student_id` = %s", (student_id,))
                connection.commit()
                print("Deleted.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "instructor":
            try:
                instructor_id = input("Enter instructor ID to delete: ")
                cursor.execute("DELETE FROM instructors WHERE `instructor_id` = %s", (instructor_id,))
                connection.commit()
                print("Deleted.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "admin":
            try:
                admin_id = input("Enter admin ID to delete: ")
                cursor.execute("DELETE FROM admins WHERE `admin_id` = %s", (admin_id,))
                connection.commit()
                print("Deleted.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif entity == "exit":
            status = True
        else:
            print("Invalid input")

#The CRUD function for compensations
def instructor_comp(connection, cursor, last_update):
    status = False
    while not status:
        decision = int(input("1 - Create new compensation 2 - Update compensation 3 - Read compensation 4 - Delete compensation 5 - Exit: "))
        try:
            if decision == 1:
                instructor_id = input("Enter instructor ID: ")
                enrollment_bonus = float(input("Enter enrollment bonus: "))
                coursesuccess_bonus = float(input("Enter course success bonus: "))
                cursor.execute(
                    "INSERT INTO compensations (`instructor_id`, `enrollment_bonus`, `coursesuccess_bonus`, `last_update`) VALUES (%s, %s, %s, %s)",
                    (instructor_id, enrollment_bonus, coursesuccess_bonus, last_update))
                connection.commit()
                print("Compensation created.")
            elif decision == 2:
                compensation_id = input("Enter compensation ID to update: ")
                enrollment_bonus = float(input("Enter new enrollment bonus: "))
                coursesuccess_bonus = float(input("Enter new course success bonus: "))
                cursor.execute(
                    "UPDATE compensations SET enrollment_bonus = %s, coursesuccess_bonus = %s, last_update = %s WHERE compensation_id = %s",
                    (enrollment_bonus, coursesuccess_bonus, last_update, compensation_id))
                connection.commit()
                print("Compensation updated.")
            elif decision == 3:
                compensation_id = input("Enter compensation ID to read: ")
                cursor.execute("SELECT * FROM compensations WHERE compensation_id = %s", (compensation_id,))
                result = cursor.fetchone()
                if result:
                    print("Compensation Information:")
                    print(f"Compensation ID: {result[0]}")
                    print(f"Instructor ID: {result[1]}")
                    print(f"Enrollment Bonus: {result[2]}")
                    print(f"Course Success Bonus: {result[3]}")
                    print(f"Last Update: {result[4]}")
                else:
                    print("Compensation not found.")
            elif decision == 4:
                compensation_id = input("Enter compensation ID to delete: ")
                cursor.execute("DELETE FROM compensations WHERE compensation_id = %s", (compensation_id,))
                connection.commit()
                print("Compensation deleted.")
            elif decision == 5:
                status = True
                print("Exiting.")
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()

#menu for admins and decision tree that takes them to the specific CRUD function for entities
def manage_users(connection, cursor, last_update):
    status = False
    # dictionary for menu for manage user choices
    menu_options = {1: create_users, 2: update_users, 3: read_users, 4: delete_users}
    while not status:
        try:
            menu_choice = int(input(
                "Menu Options:[ (1 - Create Entity) (2- Update Entity) (3 - Read Entity) (4- Delete Entity) 5 to exit ]:"))
            if menu_choice == 5:
                status = True
            else:
                # Use the dictionary to call the menu for the admin
                menu_options[menu_choice](connection, cursor, last_update)
        # errors for if the user inputs an invalid number or something like a string
        except KeyError:
            print("Invalid menu option. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def admin(connection):
    last_update = datetime.date.today()
    #establish a cursor for database interaction
    cursor = connection.cursor()
    status = False
    #dictionary for menu for admins
    menu_options = {1: manage_users, 2: instructor_comp, 3: manage_courses, 4: manage_enroll, 5: "exit"}
    while not status:
        try:
            menu_choice = int(input("Menu Options:[ (1 - Manage Entities (Users, Students, Instructors, etc.) (2- Manage Instructor Compensation) (3- Manage Courses) (4- Manage Enrollments) (5- exit back to first menu) ]:"))
            if menu_choice == 5:
                status = True
            else:
                #Use the dictionary to call the menu for the admin
                menu_options[menu_choice](connection, cursor, last_update)
        #errors for if the user inputs an invalid number or something like a string
        except KeyError:
            print("Invalid menu option. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def manage_courses(connection, cursor,): #last_update
    status = False
    while not status:

        choice = input("1- Create a course 2- Update a course 3- Read a course 4- Delete a course 5- exit: ")

        if choice == '1':
            try:
                course_id = input("Enter course ID: ")
                course_name = input("Enter course name: ")
                course_subject = input("Enter course subject: ")
                instructor_id = int(input("Enter instructor ID: "))

                cursor.execute(
                    "INSERT INTO courses (`course_id`, `course_name`, `course_subject`, `instructor_id`) VALUES (%s, %s, %s, %s)",
                    (course_id, course_name, course_subject, instructor_id))
                connection.commit()
                print("Course creation successful.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()

        elif choice == '2':
            try:
                course_id = input("Enter course ID to update: ")
                course_name = input("Enter new course name: ")
                course_subject = input("Enter new course subject: ")
                instructor_id = int(input("Enter new instructor ID: "))

                cursor.execute(
                    "UPDATE courses SET course_name = %s, course_subject = %s, instructor_id = %s WHERE course_id = %s",
                    (course_name, course_subject, instructor_id, course_id))
                connection.commit()
                print("Course update successful.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()

        elif choice == '3':
            cursor.execute("SELECT * FROM courses")
            courses = cursor.fetchall()

            print("Courses:")
            for course in courses:
                print(
                    f"Course ID: {course[0]}, Course Name: {course[1]}, Subject: {course[2]}, Instructor ID: {course[3]}")

        elif choice == '4':
            try:
                course_id = input("Enter course ID to delete: ")
                cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
                connection.commit()
                print("Course deletion successful.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif choice == '5':
            status = True
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def manage_enroll(connection, cursor, last_update):
    status = False
    while not status:
        choice = int(input("1 - Create an enrollment 2- Update a student and their progress 3- Check on a students progress 4- Delete an enrollment 5- exit: "))

        if choice == 1:
            try:
                student_id = input("Enter student ID: ")
                course_id = input("Enter course ID: ")
                progress_percent = input("Enter progress percent: ")
                completion_status = input("Enter completion status (0 for incomplete, 1 for complete): ")

                cursor.execute(
                    "INSERT INTO enrollments (`student_id`, `course_id`, `progress_percent`, `completion_status`, `last_update`) VALUES (%s, %s, %s, %s, %s)",
                    (student_id, course_id, progress_percent, completion_status, last_update))
                connection.commit()
                print("Enrollment creation successful.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif choice == 2:
            try:
                student_id = input("Enter Student ID to update: ")
                course_id = input("Enter Course ID to update:")
                new_progress_percent = input("Enter new student progress percent: ")
                new_completion_status = input("Enter new completion status (0 for incomplete, 1 for complete): ")

                cursor.execute(
                    "UPDATE enrollments SET progress_percent = %s, completion_status = %s, last_update = %s WHERE student_id = %s AND course_id = %s",
                    (new_progress_percent, new_completion_status, last_update, student_id, course_id))
                connection.commit()
                print("Enrollment update successful.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif choice == 3:
            student_id = input("Enter the student ID to see their progress in their courses: ")
            cursor.execute("SELECT * FROM enrollments WHERE student_id = %s", (student_id,))
            enrollments = cursor.fetchall()

            if not enrollments:
                print(f"No enrollments found for Student ID {student_id}.")
            else:
                print(f"Enrollments for Student ID {student_id}:")
                for enrollment in enrollments:
                    print(
                        f"Student ID: {enrollment[0]}, Course ID: {enrollment[1]} Progress Percent: {enrollment[2]}, Completion Status: {enrollment[3]}, Last Update: {enrollment[4]}")
        elif choice == 4:
            try:
                student_id = int(input("Enter student ID to delete: "))
                course_id = input("Enter the course ID to delete")
                cursor.execute("DELETE FROM enrollments WHERE student_id = %s AND course_id = %s", (student_id, course_id))
                connection.commit()
                print("Enrollment deletion successful.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        elif choice == 5:
            status = True
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def instructor(connection):
    status = False
    cursor = connection.cursor()
    last_update = datetime.date.today()
    while not status:

        choice = int(input("Instructor Menu: 1- Courses, 2- Enrollment/Student Progress 3- Exit: "))

        if choice == 1:
            manage_courses(connection, cursor)
        elif choice == 2:
            manage_enroll(connection, cursor, last_update)
        elif choice == 3:
            status = True
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def main():
    status = False
    print("Welcome to the database")
    password = input("Please enter your MySQL password here: ")
    connect = establish_connection(password)

    if connect:
        while not status:
            choice = int(input("Press 1 for student menu options, 2 for instructor menu options, 3 for administrator menu options, and 4 to quit the program: \n"))
            if choice == 1:
                student(connect)
            elif choice == 2:
                instructor(connect)
            elif choice == 3:
                admin(connect)
            elif choice == 4:
                print("Goodbye \n")
                status = True
                connect.close()
                print("Connection closed")
            else:
                print("Please select a valid number \n")

main()