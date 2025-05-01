# GPU Memory Monitor

This Python script monitors NVIDIA GPU memory usage and sends email notifications when available memory exceeds a specified threshold.

## Prerequisites

- Python 3.x
- NVIDIA GPU
- NVIDIA drivers installed
- Gmail account (for sending notifications)

## Installation

1. Install the required Python packages:
```bash
pip install python-dotenv pynvml
```

2. Create a `dev.env` file in the project directory with your email credentials:
```
EMAIL=your.email@gmail.com
SMTP_USER=your.email@gmail.com
SMTP_PASS=your_app_password
```

**Important Note**: For Gmail, you need to use an App Password instead of your regular password. To generate an App Password:
1. Go to your Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification if not already enabled
4. Generate an App Password for "Mail"

## Usage

Run the script with default settings:
```bash
python gpu_monitor.py
```

### Command Line Arguments

- `--interval`: Polling interval in seconds (default: 60)
- `--threshold`: Free memory threshold in MB (default: 6000)
- `--once`: Run once and exit (default: True)
- `--smtp-server`: SMTP server address (default: smtp.gmail.com)
- `--smtp-port`: SMTP server port (default: 587)
- `--server_name`: Server name for email notifications (default: NTU_51)

Example with custom settings:
```bash
python gpu_monitor.py --interval 300 --threshold 8000 --server_name "MY_SERVER"
```

## How It Works

The script will:
1. Check available memory on all NVIDIA GPUs
2. Send an email notification when a GPU has free memory above the specified threshold
3. Exit after one check (with `--once`) or continue monitoring at the specified interval

## Email Notifications

You'll receive an email notification when a GPU has available memory above the threshold. The email will include:
- The server name
- GPU ID
- Amount of available memory
