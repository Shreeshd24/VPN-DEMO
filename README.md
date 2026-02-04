# VPN-DEMO
Secure VPN implementation using Kali Linux and networking concepts.
# Custom VPN Implementation using Python

## 📌 Overview
This project demonstrates a custom VPN implementation using Python,
TLS encryption, and TUN virtual interface handling.
A Flask-based GUI is provided to manage server and client operations.

---

## 🛠 Technologies Used
- Python
- Flask
- TLS (SSL certificates)
- Linux TUN Interface
- Wireshark (Traffic Analysis)

---

## 🏗 Architecture
![Architecture](screenshots/architecture.png)

---

## 🖥 GUI Dashboard
The web interface allows starting and stopping the VPN server and client.

![GUI](screenshots/gui_dashboard.png)

---

## 🚀 Server Execution
The server creates a TUN interface and listens for secure TLS connections.

![Server Running](screenshots/server_running.png)

---

## 🔗 Client Connection
The client connects securely to the server over TLS.

![Client Connected](screenshots/client_connected.png)

---

## 📡 VPN Connectivity Test
Successful ping over VPN tunnel showing 0% packet loss.

![Ping Test](screenshots/ping_test.png)

---

## 🔍 Traffic Analysis (Wireshark)
Captured packets to verify secure communication.

![Wireshark](screenshots/wireshark_capture.png)

---

## 🔐 Security Practices
- Sensitive certificates and private keys are excluded from the repository.
- .gitignore is used to prevent uploading confidential files.

---

## 👨‍💻 Author
Shreesh D
