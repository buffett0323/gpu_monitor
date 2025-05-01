import smtplib
import time
import os
import socket
from email.mime.text import MIMEText
from pynvml import *
from dotenv import load_dotenv

# Load environment variables from dev.env
load_dotenv('dev.env')


# CONFIG
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 10))  # seconds
MEMORY_THRESHOLD_MB = int(os.getenv('MEMORY_THRESHOLD_MB', 6000)) # 6GB
EMAIL = os.getenv('EMAIL')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
SERVER_NAME = os.getenv('SERVER_NAME')


def send_email(gpu_id, free_mem):
    msg = MIMEText(f"GPU {gpu_id} has {free_mem} MB free in {SERVER_NAME}!")
    msg['Subject'] = f'GPU {gpu_id} Memory Available in {SERVER_NAME}'
    msg['From'] = SMTP_USER
    msg['To'] = EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)



def check_gpus(sent_email):
    nvmlInit()
    device_count = nvmlDeviceGetCount()

    for i in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(i)
        mem = nvmlDeviceGetMemoryInfo(handle)
        free_mem_mb = mem.free / 1024**2

        print(f"GPU {i}: Free {free_mem_mb:.2f} MB")
        
        
        if free_mem_mb > MEMORY_THRESHOLD_MB:
            send_email(i, int(free_mem_mb))
            print(f"Email sent for GPU {i}")
            sent_email = True
            break

    nvmlShutdown()
    return sent_email

if __name__ == "__main__":
    sent_email = False
    
    while not sent_email:
        
        sent_email = check_gpus(sent_email)
        time.sleep(CHECK_INTERVAL)