# Network Security Practical Examination Portfolio & Lab Repository

[![Cisco Packet Tracer](https://img.shields.io/badge/Cisco_Packet_Tracer-v8.x-blue?logo=cisco&logoColor=white)](https://www.netacad.com)
[![CCNA Security](https://img.shields.io/badge/CCNA_Security-2.0-green.svg)](https://www.cisco.com)
[![ASA 5505](https://img.shields.io/badge/Firewall-Cisco_ASA_5505-red.svg)](https://www.cisco.com)
[![Verification](https://img.shields.io/badge/Labs_Status-100%25_Verified-success.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Complete, verified repository of Cisco IOS & ASA security configurations, topologies, step-by-step implementation guides, and professional Word documentation aligned with **Network Security Course Handout (Units 5–7)** and official Cisco Packet Tracer practical examinations.

---

## ⚡ High-Priority Exam Quick Links

- 📋 **[Master Exam Cram Sheet](EXAM_CRAM_SHEET.md)** - Rapid-fire cheat sheet for SSHv2, AAA, ZPF, ASA 5505, IPsec VPN, and DHCP.
- 📘 **[Master Combined Word Guide](Master-Documents/Network_Security_Master_Exam_Guide.docx)** - Full 8-module comprehensive reference manual in `.docx` format ready for offline reading or printing.

---

## 📂 Repository Architecture & Lab Modules

| Module Directory | Topic & Course Seam | Target Devices | Lab File Included | Key Deliverables |
| :--- | :--- | :--- | :--- | :--- |
| **[`01-SSH-Secure-Management`](01-SSH-Secure-Management/)** | SSHv2 & Device Hardening *(Handout Unit 1.2)* | Cisco ISR 1941, Catalyst 2960 | Configuration Scripts | RSA key generation, login local, transport input ssh, timeout/retries. |
| **[`02-AAA-Authentication-Authorization`](02-AAA-Authentication-Authorization/)** | AAA Subsystem *(Handout Unit 5)* | Cisco ISR Routers, TACACS+/RADIUS | Configuration Scripts | TACACS+ (TCP 49), RADIUS (UDP 1812/1813), Account Lockout, Exec Authorization. |
| **[`03-Zone-Based-Firewall-ZPF-4.4.1.1`](03-Zone-Based-Firewall-ZPF-4.4.1.1/)** | Zone-Based Policy Firewall *(Handout Unit 6)* | Cisco ISR 1941 (`R3`) | `.pka` Activity | 4-step ZPF workflow, securityk9 evaluation license, inspect HTTP/HTTPS/DNS/ICMP. |
| **[`04-Site-to-Site-IPsec-VPN-8.4.1.2`](04-Site-to-Site-IPsec-VPN-8.4.1.2/)** | Site-to-Site IPsec VPN CLI *(Handout Unit 7)* | Cisco ISR 1941 (`R1`, `R3`) | `.pka` Activity | IKE Phase 1 (ISAKMP AES-256 DH 5), Phase 2 (VPN-SET, VPN-MAP), ACL 110. |
| **[`05-ASA-5505-Firewall-9.3.1.1`](05-ASA-5505-Firewall-9.3.1.1/)** | ASA 5505 CLI & Firewall *(Handout Unit 6)* | Cisco ASA 5505 (`CCNAS-ASA`) | `.pka` Activity | Security levels (100, 70, 0), Dynamic PAT, Static NAT, MPF ICMP inspection, Real IP ACL. |
| **[`06-Basic-IPsec-VPN-Custom-Topology`](06-Basic-IPsec-VPN-Custom-Topology/)** | Custom Exam IPsec VPN *(Handout p. 226)* | HQ, ISP Transit, Branch | `.pkt` Topology | Custom policy 12, PSK `jojo123`, transform-set `jojo`, ACL 120, static routing. |
| **[`07-DHCP-Server-Infrastructure`](07-DHCP-Server-Infrastructure/)** | Option A DHCP Topology | Router R1, Switch SW1, Server | JS Automation Scripts | Dedicated DHCP Server, IP pool `192.168.1.0/24`, Gateway `192.168.1.1`, 4 PC clients. |
| **[`Master-Documents`](Master-Documents/)** | Consolidated Documentation | All Modules | `.docx` Reports | Master Exam Guide + individual lab reports with complete command listings. |

---

## 🔑 Global Credentials & Pre-Configured Passwords

| Access Level / Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Privileged EXEC (Enable Secret)** | — | `ciscoenpa55` | Required on all routers and switches (`enable`) |
| **Console Line (line con 0)** | — | `ciscoconpa55` | Password for physical serial/console access |
| **VTY Lines (line vty 0 4)** | — | `ciscovtypa55` | Password for legacy telnet lines |
| **SSH Local Administrator** | `Admin` / `admin` | `Adminpa55` / `adminpa55` | Local database user for SSH access |
| **SSH Alternative User (Lab 8.4.1.2)** | `SSHadmin` | `ciscosshpa55` | Pre-configured on Lab 8.4.1.2 routers |
| **IPsec Pre-Shared Key (Lab 8.4.1.2)** | — | `vpnpa55` | ISAKMP Phase 1 shared secret |
| **IPsec Pre-Shared Key (Custom p. 226)** | — | `jojo123` | ISAKMP Phase 1 shared secret for HQ & Branch |
| **ASA 5505 Default Enable Password** | — | *(Blank / Enter)* | Initial factory default; set to `ciscoenpa55` in lab |

---

## 🌐 Well-Known Port Numbers & Protocols

| Protocol | Transport | Port Number(s) | Primary Use |
| :--- | :--- | :--- | :--- |
| **SSH** | TCP | **Port 22** | Encrypted administrative remote shell |
| **Telnet** | TCP | **Port 23** | Plaintext remote shell (disabled for security) |
| **TACACS+** | TCP | **Port 49** | Cisco proprietary AAA service (entire packet encrypted) |
| **RADIUS Authentication** | UDP | **Port 1812** *(Legacy: 1645)* | Open standard AAA authentication & authorization |
| **RADIUS Accounting** | UDP | **Port 1813** *(Legacy: 1646)* | Open standard AAA session accounting |
| **DHCP Server / Client** | UDP | **Ports 67 (Server) / 68 (Client)** | Dynamic host IP configuration |
| **IKE / ISAKMP (IPsec)** | UDP | **Port 500** | IPsec Phase 1 management negotiation |
| **IPsec ESP** | IP Protocol | **Protocol 50** | Encrypted IPsec payload transmission |
| **IPsec AH** | IP Protocol | **Protocol 51** | Authenticated (non-encrypted) IPsec transmission |

---

## 🛠️ Verification & Diagnostic Quick Commands

### SSH
```cisco
show ip ssh
show ssh
```

### AAA & Lockout
```cisco
show aaa servers
show aaa sessions
show aaa local user lockout
clear aaa local user lockout username <user>
debug aaa authentication
```

### Zone-Based Policy Firewall (ZPF)
```cisco
show zone security
show zone-pair security
show policy-map type inspect zone-pair
```

### Site-to-Site IPsec VPN
```cisco
show crypto isakmp policy
show crypto isakmp sa                    ! Verify Phase 1: Status must be QM_IDLE
show crypto ipsec transform-set
show crypto ipsec sa                    ! Verify Phase 2: Look for #pkts encrypt / decrypt > 0
show crypto map
debug crypto isakmp
debug crypto ipsec
```

### Cisco ASA 5505
```cisco
show nameif                             ! Displays security levels (100, 70, 0)
show ip address
show nat                                ! Translation policy hit counts
show xlate                              ! Active translation slots
show conn                               ! Active stateful connection table
show access-list                        ! ACL hit counts
```

---

## 🚀 How to Practice with This Repository

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/meekness12/security.git
   cd security
   ```
2. **Open Packet Tracer Activities**:
   - Double-click any `.pka` or `.pkt` file inside folders `03-Zone-Based-Firewall-ZPF-4.4.1.1`, `04-Site-to-Site-IPsec-VPN-8.4.1.2`, `05-ASA-5505-Firewall-9.3.1.1`, or `06-Basic-IPsec-VPN-Custom-Topology`.
3. **Copy & Paste Configurations**:
   - Each folder contains ready-to-paste CLI files (`.txt`) and comprehensive `STEP_BY_STEP_INSTRUCTIONS.md`.
4. **Offline Reading**:
   - Open [`Master-Documents/Network_Security_Master_Exam_Guide.docx`](Master-Documents/Network_Security_Master_Exam_Guide.docx) in Microsoft Word or LibreOffice.

---

## 📄 License
This repository is licensed under the [MIT License](LICENSE).
