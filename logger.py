from datetime import datetime

def log(prompt, msg):
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print(f"[{prompt} {dt_string}]: {msg}")

def info(msg):
    log("INFO", msg)

def warn(msg):
    log("WARNING", msg)

def error(msg):
    log("ERROR", msg)