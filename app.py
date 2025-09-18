import socket
import threading
import queue
import streamlit as st

# Common ports to scan
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 993, 995, 3306, 3389]

st.title("Port Scanner with Banner Grabbing and Validation")

target_ip = st.text_input("Enter IP address or hostname to scan", "")

scan_button = st.button("Start Scan")

if 'scan_results' not in st.session_state:
    st.session_state.scan_results = []
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'error' not in st.session_state:
    st.session_state.error = ""

def validate_host(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.gaierror:
        return False

def scan_port(ip, port, output_queue):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:  # Port is open
                try:
                    sock.sendall(b'HEAD / HTTP/1.0\r\n\r\n')  # Try HTTP banner grab
                except:
                    pass
                try:
                    banner = sock.recv(1024).decode(errors='ignore').strip()
                    if not banner:
                        banner = "No banner received"
                except:
                    banner = "No banner received"
                output_queue.put((port, banner))
    except Exception as e:
        output_queue.put((port, f"Error: {str(e)}"))

if scan_button:
    st.session_state.scan_results = []
    st.session_state.progress = 0
    st.session_state.error = ""

    if not target_ip.strip():
        st.session_state.error = "Please enter an IP address or hostname."
    elif not validate_host(target_ip):
        st.session_state.error = f"Invalid hostname or IP: {target_ip}"
    else:
        ports_to_scan = COMMON_PORTS

        placeholder = st.empty()
        progress_bar = st.progress(0)
        
        output_queue = queue.Queue()
        threads = []

        for port in ports_to_scan:
            t = threading.Thread(target=scan_port, args=(target_ip, port, output_queue))
            t.start()
            threads.append(t)

        for i, t in enumerate(threads):
            t.join()
            st.session_state.progress = int((i + 1) / len(ports_to_scan) * 100)
            progress_bar.progress(st.session_state.progress)

            while not output_queue.empty():
                port, banner = output_queue.get()
                st.session_state.scan_results.append((port, banner))

            # live update results while scanning
            with placeholder.container():
                st.write("### Open ports with banners:")
                for p, b in sorted(st.session_state.scan_results):
                    st.write(f"Port {p}: {b}")

        progress_bar.progress(100)
        with placeholder.container():
            st.write("### Scan complete.")
            for p, b in sorted(st.session_state.scan_results):
                st.write(f"Port {p}: {b}")

if st.session_state.error:
    st.error(st.session_state.error)
elif not scan_button:
    st.info("Enter an IP address or hostname and click Start Scan.")
