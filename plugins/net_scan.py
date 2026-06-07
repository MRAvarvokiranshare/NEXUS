import socket

def run():
    print("\n🌐 NETWORK SCANNER")

    host = input("Enter domain: ")

    try:
        ip = socket.gethostbyname(host)
        print(f"IP Address: {ip}")
    except:
        print("Invalid host")
