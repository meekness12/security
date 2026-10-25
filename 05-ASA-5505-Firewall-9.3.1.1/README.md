# Lab 9.3.1.1: Configuring ASA Basic Settings and Firewall Using CLI

![Packet Tracer](https://img.shields.io/badge/Cisco_Packet_Tracer-v8.x-blue?logo=cisco)
![CCNA Security](https://img.shields.io/badge/CCNA_Security-2.0-green)
![Status](https://img.shields.io/badge/Status-100%25_Verified-success)

---

## Executive Summary
This laboratory provides hands-on implementation of the **Cisco ASA 5505 Adaptive Security Appliance** using the Command-Line Interface (CLI). Key competencies covered include defining 3-zone security architectures (Inside, Outside, DMZ) using Layer 3 VLAN interfaces, configuring Dynamic Port Address Translation (PAT) and Static 1:1 NAT using modern Network Object syntax, enforcing stateful inspection via the Modular Policy Framework (MPF), securing remote administrative access via AAA/SSH, and writing perimeter Access Control Lists (ACLs).

---

## Topology & Architectural Seams

```
[PC-B: Inside Client (DHCP)]
        │
   (E0/1: VLAN 1)
     [CCNAS-ASA] ────── (E0/2: VLAN 3) ────── [DMZ Server: 192.168.2.3]
   (E0/0: VLAN 2)                                (Public: 209.165.200.227)
        │
   (G0/0: 209.165.200.225)
     [Router R1] (Outside CPE Gateway)
   (S0/0/0: 10.1.1.1)
        │
     [Router R2] (Internet Backbone)
        │
     [Router R3] (Remote Admin ISP)
        │
[PC-C: Remote Admin (172.16.3.3)]
```

---

## IP Addressing & Interface Security Levels

| Device | Interface | IP Address | Subnet Mask | Security Level | Zone / Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ASA 5505** | `Vlan 1` (`E0/1`)<br>`Vlan 2` (`E0/0`)<br>`Vlan 3` (`E0/2`) | `192.168.1.1`<br>`209.165.200.226`<br>`192.168.2.1` | `255.255.255.0`<br>`255.255.255.248`<br>`255.255.255.0` | **100**<br>**0**<br>**70** | **`inside`** (Highest trust)<br>**`outside`** (Untrusted WAN)<br>**`dmz`** (Demilitarized Zone) |
| **R1** | `G0/0`<br>`S0/0/0` | `209.165.200.225`<br>`10.1.1.1` | `255.255.255.248`<br>`255.255.255.252` | N/A | Outside Next-Hop Gateway |
| **R2** | `S0/0/0`<br>`S0/0/1` | `10.1.1.2`<br>`10.2.2.2` | `255.255.255.252`<br>`255.255.255.252` | N/A | Transit WAN Core |
| **R3** | `G0/1`<br>`S0/0/1` | `172.16.3.1`<br>`10.2.2.1` | `255.255.255.0`<br>`255.255.255.252` | N/A | Remote ISP Gateway |
| **DMZ Server** | `NIC` | `192.168.2.3` | `255.255.255.0` | 70 | Web/ICMP Server (NAT: `209.165.200.227`) |
| **PC-B** | `NIC` | `DHCP Client` | `255.255.255.0` | 100 | Corporate Workstation |
| **PC-C** | `NIC` | `172.16.3.3` | `255.255.255.0` | 0 | Remote Administrator Workstation |

---

## Core ASA Security Architecture Rules

1. **Default Security Level Flow**:
   - Traffic passing from a **higher** security level to a **lower** security level (e.g., Inside `100` -> Outside `0`) is **allowed implicitly** and tracked statefully.
   - Traffic passing from a **lower** security level to a **higher** security level (e.g., Outside `0` -> DMZ `70` or Inside `100`) is **denied by default** unless explicitly permitted by an inbound Access Control List (`access-group ... in`).
2. **ASA 5505 Base License VLAN Constraint**:
   - The Base License only permits two full VLANs; a third VLAN (`Vlan 3` / DMZ) must include `no forward interface vlan 1` to prevent direct Layer 2 forwarding between DMZ and Inside.
3. **ASA 8.3+ Real IP in Access Lists**:
   - Modern Cisco ASA software uses the **real private IP address** in ACL statements, NOT the public post-NAT translated address. E.g., `access-list OUTSIDE-DMZ permit icmp any host 192.168.2.3`.
4. **Stateful ICMP Inspection**:
   - By default, ASA does not inspect ICMP return traffic statefully. The Modular Policy Framework (`policy-map global_policy` -> `inspect icmp`) must be explicitly configured to allow outbound pings to receive replies without an inbound ACL.

---

## Complete CLI Configuration

Enter privileged EXEC mode on the ASA (default initial password is blank, press Enter):

```cisco
enable
! Press [Enter] for blank password
configure terminal

! ----------------------------------------------------
! 1. Hostname, Domain Name & Enable Secret
! ----------------------------------------------------
hostname CCNAS-ASA
domain-name ccnasecurity.com
enable password ciscoenpa55

! ----------------------------------------------------
! 2. Layer 3 VLAN Interfaces & Security Levels
! ----------------------------------------------------
interface vlan 1
 nameif inside
 ip address 192.168.1.1 255.255.255.0
 security-level 100
 exit

interface vlan 2
 nameif outside
 ip address 209.165.200.226 255.255.255.248
 security-level 0
 exit

interface vlan 3
 ip address 192.168.2.1 255.255.255.0
 no forward interface vlan 1
 nameif dmz
 security-level 70
 exit

interface Ethernet0/2
 switchport access vlan 3
 exit

! ----------------------------------------------------
! 3. Default Gateway Routing
! ----------------------------------------------------
route outside 0.0.0.0 0.0.0.0 209.165.200.225

! ----------------------------------------------------
! 4. Dynamic PAT (Inside Network to Outside Interface)
! ----------------------------------------------------
object network inside-net
 subnet 192.168.1.0 255.255.255.0
 nat (inside,outside) dynamic interface
 exit

! ----------------------------------------------------
! 5. Static 1:1 NAT (DMZ Web Server Public Translation)
! ----------------------------------------------------
object network dmz-server
 host 192.168.2.3
 nat (dmz,outside) static 209.165.200.227
 exit

! ----------------------------------------------------
! 6. Modular Policy Framework (MPF) - ICMP Inspection
! ----------------------------------------------------
class-map inspection_default
 match default-inspection-traffic
 exit

policy-map global_policy
 class inspection_default
  inspect icmp
 exit

service-policy global_policy global

! ----------------------------------------------------
! 7. Inside DHCP Server Service
! ----------------------------------------------------
dhcpd address 192.168.1.5-192.168.1.36 inside
dhcpd dns 209.165.201.2 interface inside
dhcpd enable inside

! ----------------------------------------------------
! 8. AAA Local Authentication & SSH Hardening
! ----------------------------------------------------
username admin password adminpa55
aaa authentication ssh console LOCAL

crypto key generate rsa modulus 1024
! If prompted to replace key, enter 'no'

ssh 192.168.1.0 255.255.255.0 inside
ssh 172.16.3.3 255.255.255.255 outside
ssh timeout 10

! ----------------------------------------------------
! 9. Perimeter Inbound ACL for DMZ Server Access
! ----------------------------------------------------
access-list OUTSIDE-DMZ permit icmp any host 192.168.2.3
access-list OUTSIDE-DMZ permit tcp any host 192.168.2.3 eq 80
access-group OUTSIDE-DMZ in interface outside

write memory
```

---

## Verification & Troubleshooting

### 1. Verify Interface Status & Security Levels
```cisco
CCNAS-ASA# show nameif
Interface                Name                     Security
Vlan1                    inside                   100
Vlan2                    outside                    0
Vlan3                    dmz                       70

CCNAS-ASA# show ip address
System IP Addresses:
Interface                Name                   IP address      Subnet mask     Method 
Vlan1                    inside                 192.168.1.1     255.255.255.0   manual
Vlan2                    outside                209.165.200.226 255.255.255.248 manual
Vlan3                    dmz                    192.168.2.1     255.255.255.0   manual
```

### 2. Verify Active NAT Rules & XLATE Table
```cisco
CCNAS-ASA# show nat
Manual NAT Policies (0)
Auto NAT Policies (2)
1 (inside) to (outside) source dynamic inside-net interface 
    translate_hits = 4,Untrans_hits = 0
2 (dmz) to (outside) source static dmz-server 209.165.200.227 
    translate_hits = 4, Untrans_hits = 0

CCNAS-ASA# show xlate
2 in use, 2 most used
Flags: D - DNS, d - dynamic, G - group, I - inbound, i - dynamic additional,
       r - identity, s - static, T - test.
NAT from inside:192.168.1.0/24 to outside:209.165.200.226/29 flags d
NAT from dmz:192.168.2.3 to outside:209.165.200.227 flags s
```

### 3. Verify Active Inbound Access List
```cisco
CCNAS-ASA# show access-list OUTSIDE-DMZ
access-list OUTSIDE-DMZ; 2 elements; name hash: 0x4dfb2ad4
access-list OUTSIDE-DMZ line 1 extended permit icmp any host 192.168.2.3 (hitcnt=4) 0x1f1f238d
access-list OUTSIDE-DMZ line 2 extended permit tcp any host 192.168.2.3 eq www (hitcnt=1) 0x2e08a491
```

### 4. End-to-End Connectivity Tests
- **From PC-B (Inside)**:
  - Acquire IP via DHCP: `ipconfig /renew` -> Receives `192.168.1.5`
  - Ping ISP Gateway: `ping 209.165.200.225` -> Replies received (tests Dynamic PAT + MPF ICMP inspection).
  - SSH to ASA: `ssh -l admin 192.168.1.1` -> Connects.
- **From PC-C (Outside Remote Admin)**:
  - Ping DMZ Web Server: `ping 209.165.200.227` -> Replies received (tests Inbound ACL + Static NAT).
  - Access Web Server: Open browser -> URL: `http://209.165.200.227` -> Cisco Packet Tracer page displays.
  - SSH to ASA Outside: `ssh -l admin 209.165.200.226` -> Connects.
