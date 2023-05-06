import os
from datetime import datetime
import logging
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

def setup_log(log_level = "info"):
    os.makedirs("logs", exist_ok = True)

    # Logging
    timestamp = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
    logging.basicConfig(
        filename = os.path.join("logs", f"{timestamp}.log"),
        filemode = "w",
        level = getattr(logging, log_level.upper()),
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S%p"
    )

    # Set up logging to console
    console = logging.StreamHandler()
    console.setLevel(getattr(logging, log_level.upper()))
    # set a format which is simpler for console use
    formatter = logging.Formatter(fmt = "%(asctime)s - %(levelname)s: %(message)s", datefmt = "%Y-%m-%d %I:%M:%S%p")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

def last_nchars(string, n):
    return string[-n:]

def latest_log() -> str:
    log_files = [os.path.join("logs", log) for log in os.listdir("logs")]
    file_names = [last_nchars(log, 19) for log in log_files]
    file_name = max(file_names)
    with open(os.path.join("logs", file_name), "r") as log_file:
        log = log_file.read()
    return log

def email_log(run_date, recipients):
    
    run_date_date = datetime.strptime(run_date, "%Y-%m-%d")
    logging.info(f"Sending process log to {recipients}")

    log = latest_log()
    subject = f"Sudoku Solver"
    message = MIMEMultipart()
    message["From"] = "sudoku.solver@domain.com"
    message["To"] = ", ".join(recipients)

    if "ERROR" in log:
        subject = "ERROR: " + subject
        body = "Hi,\n\nThere was an error in the Sudoku solver. Please find attached the process log."
    else:
        subject = "SUCCESS: " + subject
        body = "Hi,\n\nThe Sudoku solver was successful. Please find attached the process log."
    
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Add output as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(log)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename=log_{run_date_date.strftime('%Y%m%d')}.log")
    message.attach(part)

    server = smtplib.SMTP("smtp.domain.com", 25)
    server.sendmail(message["From"], recipients, message.as_string())

    server.quit()
