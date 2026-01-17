# Online Voting System with Election & Candidate Management

A **web-based Online Voting System** built with **Flask** that allows secure, paperless voting for elections. Designed for **colleges, organizations, or clubs**, this platform simplifies election management with candidate tracking, email verification, and real-time results.

---

## 🔹 Features

- **User Authentication**: Register and log in using your email.  
- **Email Verification**: Users must verify via OTP sent to their email before voting.  
- **Election Management**: Admin can create, edit, and activate multiple elections.  
- **Candidate Management**: Admin can add, edit, or remove candidates per election.  
- **Voting System**: Users can securely cast votes (one vote per election).  
- **Real-Time Results**: Automatic counting and instant display of results.  
- **Admin Dashboard**: Monitor elections, candidates, and voter activity.  
- **Animations & Visual Feedback**: Modern interactive UI using HTML/CSS.

---

## 🔹 Tech Stack

- **Backend**: Python, Flask  
- **Database**: SQLite  
- **Frontend**: HTML, CSS, Bootstrap (optional)  
- **Email**: SMTP via Gmail for OTP verification  

---

## 🔹 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/Rithish4610/Online-voting-system.git
cd Online-voting-system
Create a virtual environment

python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux / macOS


Install dependencies

pip install -r requirements.txt


Configure Email OTP

Open app.py

Update email config:

app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'


⚠️ Use a Gmail App Password (not your normal Gmail password)

Run the app

python app.py


Open in browser: http://127.0.0.1:5000

🔹 Usage

Register with your email and create a password.

Check your email for the OTP verification code.

Login after verification.

Vote in active elections.

Admin can manage elections and candidates via /admin routes.
