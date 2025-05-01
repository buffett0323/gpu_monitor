import os
import time
import smtplib
import argparse
from email.mime.text import MIMEText
from dotenv import load_dotenv
from pynvml import *



def send_email(gpu_id, free_mem, args):
    msg = MIMEText(f"GPU {gpu_id} has {free_mem} MB free!")
    msg['Subject'] = f'{args.server_name} GPU {gpu_id} Available'
    msg['From'] = args.smtp_user
    msg['To'] = args.email

    with smtplib.SMTP(args.smtp_server, args.smtp_port) as server:
        server.starttls()
        server.login(args.smtp_user, args.smtp_pass)
        server.send_message(msg)


def check_gpus(threshold, args):
    nvmlInit()
    device_count = nvmlDeviceGetCount()
    notify = False

    for i in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(i)
        mem = nvmlDeviceGetMemoryInfo(handle)
        free_mem_mb = mem.free // 1024**2

        print(f"GPU {i}: {free_mem_mb:.2f} MB free")
        if free_mem_mb > threshold:
            send_email(i, free_mem_mb, args)
            notify = True

    nvmlShutdown()
    return notify



def main():
    # Load user-level config from dev.env
    load_dotenv("dev.env")
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="GPU Memory Monitor")
    parser.add_argument("--interval", type=int, default=60, help="Polling interval in seconds")
    parser.add_argument("--threshold", type=int, default=6000, help="Free memory threshold in MB")
    parser.add_argument("--once", type=bool, default=True, action="store_true", help="Run once and exit")
    parser.add_argument("--smtp-server", default="smtp.gmail.com", help="SMTP server address")
    parser.add_argument("--smtp-port", type=int, default=587, help="SMTP server port")
    parser.add_argument("--server_name", default="NTU_51", help="Server name")
    
    # Put those Params in dev.env
    parser.add_argument("--email", default=os.getenv("EMAIL"), help="Email address")
    parser.add_argument("--smtp-user", default=os.getenv("SMTP_USER"), help="SMTP user")
    parser.add_argument("--smtp-pass", default=os.getenv("SMTP_PASS"), help="SMTP password")
    args = parser.parse_args()

    while True:
        triggered = check_gpus(args.threshold, args)
        if args.once or triggered:
            break
        time.sleep(args.interval)



if __name__ == "__main__":
    main()