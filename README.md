# 🎬 Cinema Booking System (Python CLI Project)

A secure, multi-threaded command-line cinema booking system built with Python.  
This project simulates a movie ticket reservation system featuring cryptographic user authentication, real-time seat selection, and an automated background notification service.

---

## 🚀 Features

- 🔒 **Cryptographic Authentication:** User passwords are encrypted using `SHA-256` hashing (never stored as plain text).
- 📂 **Dual-File Logging (Audit Trail):** Features a distinct logging separation—`user_db.txt` acts as a clean user database, while `log.txt` tracks raw system operations.
- 🔔 **Asynchronous Notification Service:** Uses background `threading` to monitor and approve active ticket appointments automatically.
- 🧵 **Thread-Safe File I/O:** Implements `threading.Lock` to guarantee secure file writes, eliminating the risk of race conditions.
- 🎟️ **Dynamic Movie Listing:** Displays available sessions, real-time dates, and ticket pricing.
- 💺 **Interactive Seat Selection:** A simulated 5x5 cinema hall grid management (`theater_seats`).
- ⛔ **Business Logic Constraints:** Age restriction check (18+) during sign-up and a strict 15-day booking limitation rule.
- 👤 **User Information:** Fetches GitHub user profiles and lists account details like creation date and credentials.

---

## 🛠️ Technologies & Core Modules Used

- **Python 3** (Core Language)
- **hashlib:** For SHA-256 password hashing.
- **threading:** For the background service and `Lock()` synchronization.
- **datetime:** For timestamps and timedelta calculations.
- **os:** For safe file path resolution across environments.

---

## 📂 How to Run

1. Make sure Python 3 is installed.
2. Clone the repository and execute the main script:

```bash
python main.py
```
