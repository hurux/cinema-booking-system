import time
from datetime import datetime, timedelta
import threading
import os
import hashlib

users = {}
appointments = {}
appointment_date = None
status = None
notification_sent = False

file_lock = threading.Lock()
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
user_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_db.txt")

movies = {
   "Inception": {
      "sessions": ["12:00", "15:00"],
      "dates": ["30-06-2026"],
      "price": ["200"]
   },
   "Interstellar": {
      "sessions": ["14:00", "17:00"],
      "dates": ["15-07-2026"],
      "price": ["250"]
   },
   "The Matrix": {
      "sessions": ["10:00", "11:00"],
      "dates": ["27-08-2026"],
      "price": ["300"]
   }
}

theater_seats = [
   ["Empty", "Empty", "Empty", "Empty", "Empty"],
   ["Empty", "Empty", "Empty", "Empty", "Empty"],
   ["Empty", "Empty", "Empty", "Empty", "Empty"],
   ["Empty", "Empty", "Empty", "Empty", "Empty"],
   ["Empty", "Empty", "Empty", "Empty", "Empty"]
]

current_user = None
   

def Database(info, user_name=None, user_pass=None):
   with file_lock:
      try:
         timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
         with open(log_path, "a", encoding="utf-8") as file:
            print(f"[{timestamp}] {info}", file=file)
            file.flush()
            os.fsync(file.fileno())

         if user_name is not None and user_pass is not None:
            with open(user_db_path, "a", encoding="utf-8") as user_db_file:
               print(f"[{timestamp}] {user_name} : {user_pass}", file=user_db_file)
               user_db_file.flush()
               os.fsync(user_db_file.fileno())
      except Exception as e:
         print(f"Error! : {e}")


def Notification_service():
   global appointments

   try:
      while True:
         time.sleep(5)

         for user, details in list(appointments.items()):
            if details["status"] == "Active" and not details.get("notification_sent", False):
               print(f"[NOTIFICATION] The ticket for {user} has been approved for the movie '{details['movie']}'!")

               appointments[user]["notification_sent"] = True

               Database(f"[Notification Service] -> Approved User: {user}")

   except Exception as e:
      print(f"Error! {e}")


def Register():
   global users

   print("-----Registration Page-----")

   try:
      name = input("Enter your name: ").strip()
      age = int(input("Enter your age: "))
      password = input("Enter your password: ")

      if not name or not age or not password:
         print("Please do not leave any fields empty!")
         return

      elif name in users:
         print("This username is already in use!")
         return

      elif age < 18:
         print("Users under the age of 18 are not allowed to log in.")
         return
      
      hashed_pass = hash_password(password)

      account_creation_date = datetime.now().strftime("%d/%m/%Y %H:%M")

      users[name] = {
         "password": hashed_pass,
         "age": age,
         "account_creation_date": account_creation_date
      }

      Database(f"[Registration] -> {name}", user_name=name, user_pass=hashed_pass)

   except ValueError:
      print("Error! Please enter a valid number.")


def hash_password(password):
   try:
      byte_password = password.encode('utf-8')
      hash_password = hashlib.sha256(byte_password).hexdigest()
      return hash_password
   except Exception as e:
      print(f"Error! : {e}")


def Login():
   global users, current_user

   try:
      print("-----Login Page-----")

      name = input("Enter your name: ").strip()
      password = input("Enter your password: ")

      hashed_pass = hash_password(password)

      if name not in users:
         print("User not found. Please register first.")
         return

      elif users[name]["password"] != hashed_pass:
         print("Incorrect password!")
         return

      elif current_user is not None:
         print("There is already an active session!")
         return

      current_user = name

      print(f"Login successful! Welcome, {name}.")
      Database(f"[Login] -> {name}")

   except ValueError:
      print("Error! Please enter a valid number.")


def Logout():
   global current_user

   try:
      if current_user is None:
         return

      previous_user = current_user
      current_user = None

      print("Logged out successfully. We hope to see you again!")
      Database(f"[Logout] -> {previous_user}")

   except Exception as e:
      print(f"Error! : {e}")


def cinema_information():
   global current_user

   try:
      for movie, details in movies.items():
         print(
            f"Movie: {movie} - "
            f"Sessions: {details['sessions']} - "
            f"Dates: {details['dates']} - "
            f"Price: {details['price']}"
         )

      Database(f"[Cinema Information] -> {current_user}")

   except Exception as e:
      print(f"Error! : {e}")

def user_information():
   global current_user

   try:
      if current_user is None:
         print("Please log in first.")
         return
      
      for name, details in users.items():
         print(
            f"Name: {name} - \n"
            f"Password: {details['password']} - \n"
            f"Account Creation Date: {details['account_creation_date']}"
         )
      
   except Exception as e:
      print(f"Error! : {e}")

def fifteen_day_check():
   if current_user not in appointments or "appointment_date" not in appointments[current_user]:
      return

   last_appointment = appointments[current_user]["appointment_date"]
   elapsed_time = datetime.now() - last_appointment

   return elapsed_time.days



def penalty_check():
   global current_user, appointments

   try:
      if current_user not in appointments:
         return True

      result = fifteen_day_check()

      if result is not None and result < 15:
         appointments[current_user]["status"] = "Penalized"

      current_status = appointments[current_user]["status"]

      if current_status in ["Active", "Cancelled"]:
         return True

      elif current_status == "Penalized":
         print("Error! The 15-day penalty period has not expired yet.")
         return False

   except Exception as e:
      print(f"System Error! : {e}")
      return False
   

def create_appointment():
   global current_user, appointments, theater_seats, notification_sent

   try:
      if current_user is None:
         print("Please log in first.")
         return

      print("[SYSTEM] You are being connected to customer service. (NOTE: Calls may be recorded.)")
      time.sleep(1.5)

      print(f"Hello {current_user}! How can I help you today?")
      print("Press 1 to create an appointment, or 2 to view opening and closing hours.")

      choice = int(input(">"))

      match choice:
         case 1:
            if not penalty_check():
               return

            print("If you do not attend your booked session or fail to cancel your ticket, you will not be able to purchase another ticket at this cinema for 15 days.")
            print("Please wait...")
            time.sleep(1)

            print("Please enter the movie name, date, and select your seat.")

            movie_name = input("Movie name: ")
            date = input("Date: ")
            seat_row = int(input("Seat row (1-5): "))
            seat_column = int(input("Seat column (1-5): "))

            row_index = seat_row - 1
            column_index = seat_column - 1

            if movie_name not in movies:
               print("Movie not found. Please check the cinema information.")
               return

            elif date not in movies[movie_name]["dates"]:
               print("The selected date is not available for this movie.")
               return

            elif row_index < 0 or row_index > 4 or column_index < 0 or column_index > 4:
               print("Error! Please enter seat numbers between 1 and 5.")
               return

            elif theater_seats[row_index][column_index] != "Empty":
               print("This seat is already reserved. Please choose another seat.")
               return

            confirmation = input("Your appointment is ready. Do you want to confirm it? (Y/N): ")

            if confirmation.lower() != "y":
               return

            seat_letters = ["A", "B", "C", "D", "E"]
            seat_section = seat_letters[row_index]
            seat_number = f"{seat_section}-{column_index + 1}"

            print("Your appointment has been created successfully!")
            print(f"Your seat number is: {seat_number}. Please keep it for your records.")

            appointment_date = datetime.now()

            theater_seats[row_index][column_index] = seat_number
            status = "Active"

            appointments[current_user] = {
               "movie": movie_name,
               "date": date,
               "status": status,
               "appointment_date": appointment_date,
               "seat_number": seat_number,
               "notification_sent": notification_sent
            }

            Database(f"[Appointment Created] -> {current_user}")

         case 2:
            print("08:00 -> 00:00")

         case _:
            print("Invalid selection. Please choose 1 or 2.")

   except Exception as e:
      print(f"Error! : {e}")


def appointment_report():
   global appointments, current_user

   try:
      if not appointments:
         print("There are no appointments registered in the system.")
         return

      for user, details in list(appointments.items()):
         formatted_date = details["appointment_date"].strftime("%d.%m.%Y %H:%M")

         print(f"Customer: {user}")
         print(f"  🎬 Movie: {details['movie']}")
         print(f"  📅 Date: {details['date']}")
         print(f"  🚨 Status: {details['status']}")
         print(f"  🕒 Booking Date: {formatted_date}")
         print("-" * 30)

      Database(f"[Appointment Report] -> {current_user}")

   except Exception as e:
      print(f"Error! : {e}")



def cancel_appointment():
   global appointments, current_user, theater_seats

   try:
      if current_user is None:
         print("Please log in first.")
         return

      if current_user not in appointments or appointments[current_user]["status"] == "Cancelled":
         print("No active appointment found to cancel.")
         return

      confirmation = input("Are you sure you want to cancel your appointment? (Y/N): ")

      if confirmation.lower() != "y":
         print("Cancellation process aborted.")
         return

      seat_to_remove = appointments[current_user]["seat_number"]
      seat_removed = False

      for row in range(5):
         for column in range(5):
            if theater_seats[row][column] == seat_to_remove:
               theater_seats[row][column] = "Empty"
               seat_removed = True
               break

         if seat_removed:
            break

      appointments[current_user]["status"] = "Cancelled"

      print("Your appointment has been cancelled successfully, and your seat has been released.")
      Database(f"[Appointment Cancellation] -> {current_user}")

   except Exception as e:
      print(f"Error! : {e}")



if __name__ == "__main__":
   print("System is starting...")

   notification_thread = threading.Thread(target=Notification_service, daemon=True)
   notification_thread.start()

   while True:
      print("\n================ MENU ================")

      if current_user:
         print(f" Active Session: [ {current_user} ]")
      else:
         print(" Active Session: [ Not Logged In ]")

      print("======================================")
      print("1. Register")
      print("2. Login")
      print("3. Logout")
      print("4. Show Movies")
      print("5. Create Ticket / Appointment")
      print("6. View Appointment Report")
      print("7. View User İnformation")
      print("8. Cancel Appointment")
      print("0. Exit Program")
      print("======================================")

      choice = input("Select an option (0-7): ").strip()

      if choice == "1":
         Register()

      elif choice == "2":
         Login()

      elif choice == "3":
         Logout()

      elif choice == "4":
         cinema_information()

      elif choice == "5":
         create_appointment()

      elif choice == "6":
         appointment_report()

      elif choice == "7":
         user_information()

      elif choice == "8":
         cancel_appointment()

      elif choice == "0":
         print("Shutting down the system. Have a nice day!")
         break

      else:
         print("Invalid choice! Please enter a number between 0 and 7.")
