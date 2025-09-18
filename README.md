
```markdown
# Port Scanner with Banner Grabbing (Streamlit)

## Description

This project is a Python-based network port scanner integrated with a real-time Streamlit dashboard. It scans specified ports on a target IP or hostname, performs banner grabbing to identify services running on open ports, and displays the results interactively in the dashboard.

## Features

- IP and hostname validation before scanning
- Multi-threaded scanning of common ports
- Banner grabbing to identify service information from open ports
- Real-time progress bar and dynamic result updates
- Simple and user-friendly web interface using Streamlit

## Installation

Make sure Python 3 is installed. Install dependencies with:

```
pip install streamlit
```

## Usage

Run the app with:

```
streamlit run app.py
```

Enter a valid IP address or hostname and click "Start Scan" to scan common ports.

## Example Test Targets

- Localhost: `127.0.0.1`  
- Google DNS: `8.8.8.8`  
- Example website: `93.184.216.34`

## Notes

Use this tool responsibly—only scan machines and networks where you have permission.

## License

 MIT License
```
