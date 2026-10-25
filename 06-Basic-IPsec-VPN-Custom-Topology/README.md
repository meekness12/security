# Module 06: Basic Site-to-Site IPsec VPN (Custom 3-Router Topology)

## Overview
Based directly on the course handout (**Learning Unit 7, page 226**), this lab demonstrates a basic Site-to-Site IPsec VPN tunnel between **HQ** and **Branch** across an intermediate **ISP** transit router.

---

## Addressing Schema
- **HQ LAN**: `10.0.0.0/24` (Gateway: `10.0.0.1`, PC0: `10.0.0.10`)
- **HQ WAN**: `20.1.1.2/30` (`Serial0/2/0`)
- **ISP WAN (HQ side)**: `20.1.1.1/30` (`Serial0/2/0`)
- **ISP WAN (Branch side)**: `50.1.1.1/30` (`Serial0/2/1`)
- **Branch WAN**: `50.1.1.2/30` (`Serial0/2/0`)
- **Branch LAN**: `11.0.0.0/24` (Gateway: `11.0.0.1`, PC1: `11.0.0.10`)

---

## Cryptographic Parameters
- **ISAKMP Policy**: `12`
  - Authentication: `pre-share`
  - Encryption: `3des`
  - Hash: `md5`
  - Diffie-Hellman Group: `group 1`
  - Lifetime: `3600` seconds
- **Pre-Shared Key**: `jojo123`
- **Transform-Set**: `jojo` (`esp-3des esp-md5-hmac`)
- **Crypto ACL**: `120` (`permit ip 10.0.0.0 0.255.255.255 11.0.0.0 0.255.255.255`)
- **Crypto Map**: `jojo 12 ipsec-isakmp` bound to `Serial0/2/0`

---

## Deliverables in this Directory
- [`configs/HQ_Router_Config.txt`](configs/HQ_Router_Config.txt): Copy-paste configuration for HQ.
- [`configs/Branch_Router_Config.txt`](configs/Branch_Router_Config.txt): Copy-paste configuration for Branch.
- [`configs/ISP_Router_Config.txt`](configs/ISP_Router_Config.txt): Copy-paste configuration for ISP.
- [`Verification_Commands.txt`](Verification_Commands.txt): Step-by-step verification commands.
- [`Site_to_Site_IPsec_VPN.pkt`](Site_to_Site_IPsec_VPN.pkt): Cisco Packet Tracer topology file.
- [`Site_to_Site_IPsec_VPN_Report.docx`](Site_to_Site_IPsec_VPN_Report.docx): Detailed lab report with real CLI execution screenshots.
