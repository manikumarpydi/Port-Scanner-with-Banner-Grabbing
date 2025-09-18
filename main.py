import socket

socket.setdefaulttimeout(2)

def ReturnBanner(ip, port):
    try:
        sock = socket.socket()
        sock.connect((ip, port))
        banner = sock.recv(1024).decode(errors='ignore').strip()
        print(banner)
        sock.close()
        return banner
    except Exception as e: 
        print('Error : ' + str(e))
        return ""

# Check for vulnerability on known server banners
def checkVulns(banner):
    try:
        with open("vulnarableBanner.txt", 'r') as VulnarableFTPlist:
            for line in VulnarableFTPlist:
                if line.strip() in banner:
                    print("[ + ] server is Vulnerable: " + banner)
                    return True
        return False
    except FileNotFoundError:
        print("vulnarableBanner.txt file not found!")
        return False

def main():
    print('Welcome to FTP Banner grabbing script')
    IP = input('Host IP : ')
    PortList = [21, 22, 23, 25, 80, 110, 443]
    PortNames = {21: 'ftp', 22: 'ssh', 23: 'Telnet', 25: 'smtp', 80: 'HTTP', 110: 'POP3', 443: 'HTTPS'}
    
    for port in PortList:
        banner = ReturnBanner(IP, port)
        if banner:
            print(f'[ + ] {IP}: {banner}')
            vulnerable = checkVulns(banner)
            if not vulnerable:
                print('\tNo known vulnerabilities found.')
        else:
            print(f'[ - ] CAN\'T CONNECT {IP} ON PORT {PortNames.get(port, port)}')

if __name__ == '__main__':
    main()
