import tkinter as tk
from tkinter import messagebox
import requests
import random
from twilio.rest import Client
from cryptography.fernet import Fernet  # For encryption
from flask_limiter import Limiter  # For rate limiting
from flask_babel import Babel  # For internationalization
import logging

# Initialize Flask app for rate limiting
limiter = Limiter(app)
app = Flask(__name__)

# Initialize Flask-Babel for internationalization
babel = Babel(app)

# Initialize logger
logging.basicConfig(filename='app.log', level=logging.INFO)

# Function to generate a random phone number based on the country
def generate_phone_number(country_code):
    """
    Generates a random phone number based on the country code.

    Parameters:
        country_code (str): The country code ('UK', 'US', etc.).

    Returns:
        str: The generated phone number.
    """
    if country_code == 'UK':
        area_code = random.choice(['020', '0121', '0161', '0113', '029', '0131', '0141', '0151'])  # Example UK area codes
        subscriber_number = ''.join(random.choices('0123456789', k=7))  # 7-digit subscriber number
        return f"+44{area_code}{subscriber_number}"
    elif country_code == 'US':
        area_code = random.choice(['201', '212', '347', '646', '718', '917', '929'])  # Example US area codes
        subscriber_number = ''.join(random.choices('0123456789', k=7))  # 7-digit subscriber number
        return f"+1{area_code}{subscriber_number}"
    # Add more countries as needed
    else:
        return None

# Backend Functions
def register_user():
    """
    Registers a user by sending the username and password to the backend server.
    Displays a message box with the registration status.
    """
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    
    # Encrypt password before sending
    cipher_suite = Fernet(b'your_key_here')  # Change key
    encrypted_password = cipher_suite.encrypt(password.encode())
    
    data = {'username': username, 'password': encrypted_password.decode()}
    try:
        response = requests.post('http://localhost:3000/register', json=data)
        response.raise_for_status()
        messagebox.showinfo("Registration", f"User {username} registered successfully!")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Registration failed: {e}")

def login_user():
    """
    Logs in a user by sending the username and password to the backend server.
    Displays a message box with the login status.
    """
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    
    # Encrypt password before sending
    cipher_suite = Fernet(b'your_key_here')  # Change key
    encrypted_password = cipher_suite.encrypt(password.encode())
    
    data = {'username': username, 'password': encrypted_password.decode()}
    try:
        response = requests.post('http://localhost:3000/login', json=data)
        response.raise_for_status()
        token = response.json()['token']
        messagebox.showinfo("Login", f"Welcome back, {username}!")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Login failed: {e}")

def make_payment():
    """
    Processes a payment by sending the token and amount to the backend server.
    Distributes 25 pence for every pound made by the company to the resource pool contributions.
    Displays a message box with the payment status.
    """
    token = token_entry.get()
    amount = amount_entry.get()
    if not token or not amount:
        messagebox.showerror("Error", "Please enter both token and amount.")
        return
    
    # Check for special package: £25 a month unlimited call and number package
    if amount.lower() == 'unlimited':
        total_revenue = 25  # Monthly subscription cost
        user_share = total_revenue * 0.025  # User's share based on contribution ratio
        company_share = total_revenue - user_share  # Company's share
        # Distribute 25 pence for every pound made by the company to the resource pool contributions
        resource_contribution = company_share * 0.25
        messagebox.showinfo("Payment", f"Thank you for subscribing to the unlimited call and number package!")
        messagebox.showinfo("Payment", f"Your monthly subscription cost is £{total_revenue}.")
        messagebox.showinfo("Payment", f"Your share: £{user_share}, Company's share: £{company_share}.")
        messagebox.showinfo("Payment", f"£{company_share} contributed to the resource pool.")
    else:
        try:
            response = requests.post('http://localhost:3000/payment', json={'token': token, 'amount': amount})
            response.raise_for_status()
            # Calculate user's share based on contribution ratio (2.5 pence per pound)
            total_amount = float(amount)
            user_share = total_amount * 0.025
            # Calculate company's share
            company_share = total_amount - user_share
            # Distribute 25 pence for every pound made by the company to the resource pool contributions
            resource_contribution = company_share * 0.25
            messagebox.showinfo("Payment", f"Payment of £{amount} made successfully!")
            messagebox.showinfo("Payment", f"Your share: £{user_share}, Company's share: £{company_share}.")
            messagebox.showinfo("Payment", f"£{company_share} contributed to the resource pool.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Payment failed: {e}")

def monitor_resources():
    """
    Fetches resource usage information from the backend server and displays it in a message box.
    """
    try:
        response = requests.get('http://localhost:3000/monitor')
        response.raise_for_status()
        data = response.json()
        messagebox.showinfo("Resource Monitoring", f"CPU Usage: {data['cpuUsage']}%, Free Memory: {data['freeMem']} bytes, Total Memory: {data['totalMem']} bytes")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch resource usage: {e}")

def make_call():
    """
    Initiates a call using the Twilio API.
    Expects a JSON payload with the recipient's phone number.
    """
    recipient_number = recipient_entry.get()
    if not recipient_number:
        messagebox.showerror("Error", "Please enter recipient's phone number.")
        return account_sid = 'your_account_sid_here'  # Your Twilio account SID
auth_token = 'your_auth_token_here'  # Your Twilio auth token
client = Client(account_sid, auth_token)

    try:
        call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',  # Example TwiML URL
            to=recipient_number,
            from_=generate_phone_number('UK'),  # Generate a random UK phone number
            method='GET'
        )
        messagebox.showinfo("Call", f"Call initiated to {recipient_number}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initiate call: {e}")

# GUI
root = tk.Tk()
root.title("VoIP SaaS Application")

# Header
header_label = tk.Label(root, text="Voice of the People", font=("Helvetica", 16, "bold"))
header_label.grid(row=0, column=0, columnspan=2, pady=10)

# User registration frame
register_frame = tk.Frame(root, padx=10, pady=10)
register_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
tk.Label(register_frame, text="Username:").grid(row=0, column=0, sticky="e")
username_entry = tk.Entry(register_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Label(register_frame, text="Password:").grid(row=1, column=0, sticky="e")
password_entry = tk.Entry(register_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)
register_btn = tk.Button(register_frame, text="Register", command=register_user)
register_btn.grid(row=2, columnspan=2, pady=5)

# User login frame
login_frame = tk.Frame(root, padx=10, pady=10)
login_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
tk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="e")
tk.Entry(login_frame).grid(row=0, column=1, padx=5, pady=5)
tk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="e")
tk.Entry(login_frame, show="*").grid(row=1, column=1, padx=5, pady=5)
login_btn = tk.Button(login_frame, text="Login", command=login_user)
login_btn.grid(row=2, columnspan=2, pady=5)

# Payment frame
payment_frame = tk.Frame(root, padx=10, pady=10)
payment_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
tk.Label(payment_frame, text="Token:").grid(row=0, column=0, sticky="e")
token_entry = tk.Entry(payment_frame)
token_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Label(payment_frame, text="Amount:").grid(row=1, column=0, sticky="e")
amount_entry = tk.Entry(payment_frame)
amount_entry.grid(row=1, column=1, padx=5, pady=5)
payment_btn = tk.Button(payment_frame, text="Make Payment", command=make_payment)
payment_btn.grid(row=2, columnspan=2, pady=5)

# Resource monitoring frame
monitor_frame = tk.Frame(root, padx=10, pady=10)
monitor_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
monitor_btn = tk.Button(monitor_frame, text="Monitor Resources", command=monitor_resources)
monitor_btn.pack()

# Call placement frame
call_frame = tk.Frame(root, padx=10, pady=10)
call_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
tk.Label(call_frame, text="Recipient's Phone Number:").grid(row=0, column=0, sticky="e")
recipient_entry = tk.Entry(call_frame)
recipient_entry.grid(row=0, column=1, padx=5, pady=5)
call_btn = tk.Button(call_frame, text="Make Call", command=make_call)
call_btn.grid(row=1, columnspan=2, pady=5)

# Footer
footer_label = tk.Label(root, text="© 2024 Property of @TheMadHattersPlayground.com", font=("Helvetica", 8))
footer_label.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()