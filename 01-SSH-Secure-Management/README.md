# Module 01: SSH Secure Device Management

## Overview
Based directly on **Learning Outcome 1.2 (Pages 46–48)** of the course handout, this module covers the 4-step process required to configure SSHv2 on Cisco routers and switches to replace unencrypted Telnet management.

---

## The 4 Mandatory Configuration Steps
1. **Host & Domain Naming**: A unique `hostname` and `ip domain-name` are required before RSA keys can be generated (the FQDN `hostname.domain-name` forms the keypair label).
2. **RSA Asymmetric Key Generation**: Generated via `crypto key generate rsa general-keys modulus 1024`. (Minimum recommended modulus is 1024 bits; 2048 for high security).
3. **Local Database User**: `username <name> privilege 15 secret <password>`.
4. **VTY Line Hardening**: Under `line vty 0 4`, enforce `login local` and `transport input ssh`.

---

## Hardening Options
- `ip ssh version 2`: Disables deprecated SSHv1 and forces SSHv2 with Diffie-Hellman key exchange and strong MAC.
- `ip ssh time-out 60`: Reduces authentication window to 60 seconds (default is 120s).
- `ip ssh authentication-retries 3`: Disconnects clients after 3 failed login attempts.

---

## Files in this Directory
- [`configs/SSH_Router_Config.txt`](configs/SSH_Router_Config.txt): Copy-paste configuration block for Cisco routers.
- [`configs/SSH_Switch_Config.txt`](configs/SSH_Switch_Config.txt): Copy-paste configuration block for Cisco Catalyst switches.
- [`Verification_Commands.txt`](Verification_Commands.txt): Status, inspection, and debug commands.
