# Module 07: DHCP Server & Gateway Infrastructure (Option A)

## Overview
This module documents the **1 Router, 1 Server, 1 Switch, and 4 PCs** network topology deployed under **Option A**:
- **Router R1** (Cisco 2911): Default Gateway (`192.168.1.1/24` on `G0/0`).
- **Server0** (Cisco Server-PT): Dedicated DHCP Server (`serverPool` with start IP `192.168.1.20`, pool size 50).
- **Switch SW1** (Cisco 2960): Access layer switching (`Fa0/1` - `Fa0/6`).
- **Clients PC0 - PC3**: Dynamic DHCP clients dynamically leasing `192.168.1.20` through `192.168.1.23`.

---

## Addressing Schema
| Device | Interface | IP Address | Subnet Mask | Gateway | Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** | `G0/0` | `192.168.1.1` | `255.255.255.0` | N/A | LAN Default Gateway |
| **Server0** | `Fa0` | `192.168.1.10` | `255.255.255.0` | `192.168.1.1` | DHCP Server (`serverPool`) |
| **PC0** | `Fa0` | `192.168.1.20` (DHCP) | `255.255.255.0` | `192.168.1.1` | DHCP Client |
| **PC1** | `Fa0` | `192.168.1.21` (DHCP) | `255.255.255.0` | `192.168.1.1` | DHCP Client |
| **PC2** | `Fa0` | `192.168.1.22` (DHCP) | `255.255.255.0` | `192.168.1.1` | DHCP Client |
| **PC3** | `Fa0` | `192.168.1.23` (DHCP) | `255.255.255.0` | `192.168.1.1` | DHCP Client |

---

## Deliverables in this Directory
- [`scripts/full_build.js`](scripts/full_build.js): Complete Packet Tracer Script-Engine builder script.
- [`scripts/R1_config.txt`](scripts/R1_config.txt): Router R1 CLI gateway commands.
- [`scripts/SW1_config.txt`](scripts/SW1_config.txt): Switch SW1 management config.
- [`scripts/topology.js`](scripts/topology.js): Topology layout generator.
- [`DHCP_1Router_1Server_4PCs_Report.docx`](DHCP_1Router_1Server_4PCs_Report.docx): Detailed lab report with verification evidence and diagrams.
