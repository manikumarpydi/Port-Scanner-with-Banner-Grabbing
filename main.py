import socket
import threading
from flask import Flask, render_template, request

app = Flask(__name__)

def grab_banner(s):
    try:
        banner = s.recv(1024).decode().strip()
        return banner
    except:
        return None

def scan_port(target, port, results):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect((target, port))
        banner = grab_banner(s)
        if banner:
            results.append(f"Port {port} open: {banner}")
        else:
            results.append(f"Port {port} open")
    except:
        pass
    finally:
        s.close()

def scan_ports(target, start_port, end_port):
    threads = []
    results = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port, results))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        target = request.form.get("target")
        start_port = int(request.form.get("start_port", 1))
        end_port = int(request.form.get("end_port", 1024))
        results = scan_ports(target, start_port, end_port)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
