# Module 02: Triple AAA (Authentication, Authorization & Accounting)

## Overview
Based directly on **Learning Unit 5 (Pages 144–184)** of the course handout, this module covers both self-contained **Local AAA Authentication** and enterprise **Server-Based AAA** using **TACACS+** and **RADIUS**.

---

## 1. AAA Fundamentals (The Three Pillars)
- **Authentication**: *Who is the user?* (Verifies identity via username/password, token, or digital certificate).
- **Authorization**: *What can the user do?* (Restricts commands, privilege levels, and services like EXEC shells or network access).
- **Accounting**: *What did the user do?* (Logs login/logout times, executed commands, and packet/byte counts for auditing and billing).

---

## 2. TACACS+ vs. RADIUS Comparison (High-Yield Exam Topic)

| Feature | TACACS+ (Terminal Access Controller Access-Control System Plus) | RADIUS (Remote Authentication Dial-In User Service) |
| :--- | :--- | :--- |
| **Standard** | Cisco Proprietary | Open IETF Standard (RFC 2865, 2866) |
| **Transport Protocol** | **TCP** (Port 49) | **UDP** (Ports 1812/1813 or 1645/1646) |
| **Encryption** | **Entire Packet Body** is encrypted (only standard header is clear) | **Password Only** is encrypted (rest of packet in cleartext) |
| **AAA Modularity** | **Separates** Authentication, Authorization, and Accounting | **Combines** Authentication and Authorization |
| **Primary Use Case** | Device Administration & Granular Per-Command Control | Network Access (802.1X, VPNs, Dial-in, VoIP) |

---

## 3. Method List Logic & Fallback Behavior
- Cisco IOS evaluates method lists sequentially from left to right:
  ```cisco
  aaa authentication login default group tacacs+ group radius local enable
  ```
- **Crucial Rule**: The next method in the list is queried **ONLY if the previous method is unreachable or returns an error (no response)**. If a server responds with an explicit **REJECT / ACCESS-DENIED**, the authentication process terminates immediately and fallback methods are **NOT** consulted.

---

## Files in this Directory
- [`configs/AAA_Local_Config.txt`](configs/AAA_Local_Config.txt): Local authentication, named method lists, and account lockout.
- [`configs/AAA_Server_TACACS_RADIUS_Config.txt`](configs/AAA_Server_TACACS_RADIUS_Config.txt): Server-based TACACS+ and RADIUS setup, authorization, and accounting.
- [`Verification_Commands.txt`](Verification_Commands.txt): Status checks, server tests, and real-time debug commands.
