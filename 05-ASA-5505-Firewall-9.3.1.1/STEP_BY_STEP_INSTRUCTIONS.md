# Cisco Packet Tracer 9.3.1.1 - Configuring ASA Basic Settings and Firewall Using CLI

## Activity Overview
- **File**: `9.3.1.1 Packet Tracer - Configuring ASA Basic Settings and Firewall Using CLI.pka`
- **Target Security Device**: Cisco ASA 5505 (`CCNAS-ASA`)
- **Connected Networks**:
  - `inside` (VLAN 1, Security Level 100, `192.168.1.0/24`)
  - `outside` (VLAN 2, Security Level 0, `209.165.200.224/29`)
  - `dmz` (VLAN 3, Security Level 70, `192.168.2.0/24`)
- **Completion Goal**: 100%

---

## Pre-Configured Credentials & IP Schema

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Security Level / Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** | `G0/0`<br>`S0/0/0` (DCE) | `209.165.200.225`<br>`10.1.1.1` | `255.255.255.248`<br>`255.255.255.252` | N/A<br>N/A | Outside Gateway<br>Transit to R2 |
| **R2** | `S0/0/0`<br>`S0/0/1` (DCE) | `10.1.1.2`<br>`10.2.2.2` | `255.255.255.252`<br>`255.255.255.252` | N/A<br>N/A | Internet Backbone |
| **R3** | `G0/1`<br>`S0/0/1` | `172.16.3.1`<br>`10.2.2.1` | `255.255.255.0`<br>`255.255.255.252` | N/A<br>N/A | Remote Management ISP |
| **ASA 5505** | `Vlan 1` (`E0/1`)<br>`Vlan 2` (`E0/0`)<br>`Vlan 3` (`E0/2`) | `192.168.1.1`<br>`209.165.200.226`<br>`192.168.2.1` | `255.255.255.0`<br>`255.255.255.248`<br>`255.255.255.0` | N/A<br>N/A<br>N/A | **`inside`** (100)<br>**`outside`** (0)<br>**`dmz`** (70) |
| **DMZ Server** | `NIC` | `192.168.2.3` | `255.255.255.0` | `192.168.2.1` | Static NAT: `209.165.200.227` |
| **PC-B** | `NIC` | `DHCP Client` | `255.255.255.0` | `192.168.1.1` | Inside Workstation |
| **PC-C** | `NIC` | `172.16.3.3` | `255.255.255.0` | `172.16.3.1` | Remote Admin Workstation |

**Credentials**:
- ASA Enable Password: `ciscoenpa55` (set in Part 2; initial password is blank)
- Console Password: `ciscoconpa55`
- Admin User: `admin` / Password: `adminpa55`

---

## Step-by-Step Execution Guide

### Part 1: Exploration
1. In Packet Tracer, observe initial completion starts at **20%** (default factory parameters).
2. Click **ASA** > **CLI** tab.
3. Enter privileged EXEC mode:
   ```cisco
   enable
   ! Press [Enter] when prompted for initial blank password
   ```

---

### Part 2: Basic ASA Settings & Interface Security Levels
Enter config mode on the ASA:
```cisco
configure terminal
hostname CCNAS-ASA
domain-name ccnasecurity.com
enable password ciscoenpa55

! VLAN 1: Inside Interface (Level 100)
interface vlan 1
 nameif inside
 ip address 192.168.1.1 255.255.255.0
 security-level 100
 exit

! VLAN 2: Outside Interface (Level 0)
interface vlan 2
 nameif outside
 ip address 209.165.200.226 255.255.255.248
 security-level 0
 exit
```

---

### Part 3: Routing, Address Translation, and Inspection Policy
```cisco
! Static Default Route via ISP Gateway R1
route outside 0.0.0.0 0.0.0.0 209.165.200.225

! Dynamic PAT (Overload inside-net onto outside interface)
object network inside-net
 subnet 192.168.1.0 255.255.255.0
 nat (inside,outside) dynamic interface
 exit

! MPF: Enable ICMP Stateful Return Inspection
class-map inspection_default
 match default-inspection-traffic
 exit
policy-map global_policy
 class inspection_default
  inspect icmp
 exit
service-policy global_policy global
```

---

### Part 4: DHCP, AAA Authentication, and Secure Remote Access
```cisco
! Configure DHCP Server for Inside Network
dhcpd address 192.168.1.5-192.168.1.36 inside
dhcpd dns 209.165.201.2 interface inside
dhcpd enable inside

! Local Authentication Database & AAA for SSH
username admin password adminpa55
aaa authentication ssh console LOCAL

! RSA Key Generation (Preserve existing keys if prompted)
crypto key generate rsa modulus 1024
no

! Authorize SSH Access & Set Timeout
ssh 192.168.1.0 255.255.255.0 inside
ssh 172.16.3.3 255.255.255.255 outside
ssh timeout 10
```

---

### Part 5: DMZ Interface, Static NAT, and Access Control Lists (ACLs)
```cisco
! VLAN 3: DMZ Interface (Level 70, Isolated from VLAN 1)
interface vlan 3
 ip address 192.168.2.1 255.255.255.0
 no forward interface vlan 1
 nameif dmz
 security-level 70
 exit

! Assign Physical Port Ethernet 0/2 to DMZ VLAN 3
interface Ethernet0/2
 switchport access vlan 3
 exit

! Static 1:1 NAT Mapping for DMZ Web Server
object network dmz-server
 host 192.168.2.3
 nat (dmz,outside) static 209.165.200.227
 exit

! Outside Access-List Permitting ICMP & HTTP to Private DMZ IP
access-list OUTSIDE-DMZ permit icmp any host 192.168.2.3
access-list OUTSIDE-DMZ permit tcp any host 192.168.2.3 eq 80
access-group OUTSIDE-DMZ in interface outside

write memory
```

---

### Part 6: Client Configuration on PC-B
1. Click **PC-B** > **Desktop** > **IP Configuration**.
2. Select the **DHCP** radio button.
3. Confirm PC-B successfully leases an IP from the ASA DHCP pool (`192.168.1.5 - 192.168.1.36`, gateway `192.168.1.1`, DNS `209.165.201.2`).

---

### Part 7: Verification & Scoring
1. **Ping Outside from PC-B**:
   - On **PC-B Command Prompt**: `ping 209.165.200.225` -> Replies received (`4/4`).
2. **SSH from Inside PC-B**:
   - On **PC-B Command Prompt**: `ssh -l admin 192.168.1.1` (Password: `adminpa55` -> Connected).
3. **SSH from Remote PC-C**:
   - On **PC-C Command Prompt**: `ssh -l admin 209.165.200.226` (Password: `adminpa55` -> Connected).
4. **Scoring Check**:
   - In Packet Tracer, click **Check Results** -> **Completion: 100%**.
