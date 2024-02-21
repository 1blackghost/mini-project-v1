import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_verification_email(receiver_address, verification_link):
    # Email configuration
    sender_address = 'your_email@gmail.com'  # Enter your email address
    sender_password = "cjnr ptgo cooi wvrj"
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = receiver_address
    msg['Subject'] = 'Email Verification'

    # Email body
    email_body = f"""
    <html>
    <body>
        <p>Dear user,</p>
        <p>Please click the following link to verify your email address:</p>
        <p><a href="{verification_link}">Verify Email</a></p>
        <p>If you didn't request this, please ignore this email.</p>
        <p>Regards,<br>Your Company</p>
    </body>
    </html>
    """

    # Attach email body as HTML
    msg.attach(MIMEText(email_body, 'html'))

    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        # Login to SMTP server
        server.login(sender_address, sender_password)
        # Send email
        server.sendmail(sender_address, receiver_address, msg.as_string())
        print('Email sent successfully')
    except Exception as e:
        print(f'Error: Unable to send email. {e}')
    finally:
        # Close SMTP session
        server.quit()

# Example usage:
receiver_email = 'ashishjosephp666@gmail.com'  # Enter recipient's email address
verification_link = 'ashishjosephnew@gmail.com'  # Example verification link
send_verification_email(receiver_email, verification_link)

