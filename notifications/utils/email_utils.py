import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .email_settings import get_email_settings

def send_emails(subject, message, recipient_list, html_message=None):
    settings = get_email_settings()
    
    msg = MIMEMultipart("alternative") if html_message else MIMEMultipart()
    msg['From'] = settings['DEFAULT_FROM_EMAIL']
    msg['To'] = ", ".join(recipient_list)
    msg['Subject'] = subject

    # Add plain and HTML parts
    if html_message:
        msg.attach(MIMEText(message or html_message, 'plain'))
        msg.attach(MIMEText(html_message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to Gmail SMTP
        server = smtplib.SMTP(settings['EMAIL_HOST'], settings['EMAIL_PORT'])
        server.ehlo()  # Identify ourselves
        server.starttls()  # Start TLS
        server.ehlo()  # Re-identify as encrypted connection
        server.login(settings['EMAIL_HOST_USER'], settings['EMAIL_HOST_PASSWORD'])
        
        server.sendmail(
            from_addr=settings['DEFAULT_FROM_EMAIL'],
            to_addrs=recipient_list,
            msg=msg.as_string()
        )
        server.quit()
        print("✅ Email sent successfully.")
        return True

    except Exception as e:
        print("❌ Failed to send email:", str(e))
        return False