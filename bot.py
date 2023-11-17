import os
import math
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.parsemode import ParseMode
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Load environment variables
load_dotenv()

digits = "0123456789"
correct_otp = ""

def generate_otp():
    global correct_otp
    for i in range(6):
        correct_otp += digits[math.floor(random.random() * 10)]

def send_otp_email(email_id):
    # HTML template for the email body
    email_template = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: 'Arial', sans-serif;
            text-align: center;
            background-color: #f4f4f4;
            padding: 20px;
          }}
          .container {{
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 80%;
            margin: auto;
          }}
          h2 {{
            color: #3498db;
          }}
          button {{
            background-color: #3498db;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h2>{correct_otp} is your OTP</h2>
          <button onclick="copyToClipboard()">Copy OTP</button>
          <script>
            function copyToClipboard() {{
              var textArea = document.createElement("textarea");
              textArea.value = '{correct_otp}';
              document.body.appendChild(textArea);
              textArea.select();
              document.execCommand('copy');
              document.body.removeChild(textArea);
              alert('OTP copied to clipboard!');
            }}
          </script>
        </div>
      </body>
    </html>
    """

    # Create the MIME object
    msg = MIMEMultipart()

    # Attach the HTML part to the email body
    msg.attach(MIMEText(email_template, 'html'))

    # SMTP setup
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(os.getenv("GMAIL_USERNAME"), os.getenv("GMAIL_PASSWORD"))

    # Set email details
    msg['From'] = os.getenv("GMAIL_USERNAME")
    msg['To'] = email_id
    msg['Subject'] = 'Your OTP'

    # Send the email
    s.sendmail(os.getenv("GMAIL_USERNAME"), email_id, msg.as_string())

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I am your OTP bot. Use /getotp to receive a new OTP.")

def get_otp(update: Update, context: CallbackContext) -> None:
    global correct_otp
    generate_otp()
    send_otp_email(update.message.from_user.username)
    update.message.reply_text("OTP sent to your email. Use /verifyotp to enter the OTP.")

def verify_otp(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.split("/verifyotp ")[1]
    if user_input == correct_otp:
        update.message.reply_text("OTP verified!")
    else:
        update.message.reply_text("Incorrect OTP. Please try again.")

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater("5949185294:AAEAgjv-VAIEYmWfEb8IoQX8rAKdos1FEHc")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getotp", get_otp))
    dp.add_handler(MessageHandler(Filters.regex(r'/verifyotp [0-9]{6}'), verify_otp))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
