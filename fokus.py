from shutil import copyfile 
import http.server
import socketserver
import sys
import os

hosts = "/etc/hosts"
backup = "./backup"

blacklist = ["wykop.pl", "reddit.com", "news.ycombinator.com", "facebook.com"]

def backup_hosts():
    copyfile(hosts, backup)

def restore_backup():
    copyfile(backup, hosts)
    os.remove(backup)

def append_blacklist():
    with open(hosts, "a") as f:
        f.write("# Blocked by fokus:\n")
        for entry in blacklist:
            f.write(f"0.0.0.0 {entry}\n")

def server():
    PORT = 80
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Blocking hosts active.")
        print(f"Serving stats page at port: {PORT}")
        # Serve stats and info here
        httpd.serve_forever()

backup_hosts()
append_blacklist()
try:
    server()
except KeyboardInterrupt:
    print("Restoring backup hosts.")
    restore_backup()
    sys.exit("")
