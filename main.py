import subprocess
import time

print("Starting Chat Application...")

# start server
print("Starting server...")
server_process = subprocess.Popen(["python", "server/server.py"])

# wait for server to start
time.sleep(2)

# start login window
print("Starting login window...")
subprocess.Popen(["python", "client/login_ui.py"])