# Network Security Practical Exam - Master Cram Sheet

> **Quick Navigation**: [SSHv2](#1-sshv2-secure-device-management) • [AAA & TACACS+/RADIUS](#2-aaa-authentication-authorization--accounting) • [Zone-Based Firewall (ZPF)](#3-zone-based-policy-firewall-zpf) • [Cisco ASA 5505](#4-cisco-asa-5505-firewall) • [Site-to-Site IPsec VPN](#5-site-to-site-ipsec-vpn) • [DHCP Server & Relay](#6-dhcp-server--relay-agent) • [Troubleshooting Matrix](#7-master-troubleshooting-matrix)

---

## 1. SSHv2 Secure Device Management

### Prerequisites & Syntax Sequence
```cisco
configure terminal
hostname R1                              ! 1. Hostname CANNOT be default 'Router'
ip domain-name security.local            ! 2. Required before crypto key generation
crypto key generate rsa modulus 1024     ! 3. Minimum recommended modulus (1024 or 2048)

username Admin privilege 15 secret Adminpa55   ! 4. Local administrative account

ip ssh version 2                         ! 5. Enforce SSHv2 only (drops SSHv1)
ip ssh time-out 60                       ! 6. Disconnect idle session after 60s
ip ssh authentication-retries 3          ! 7. Lockout/disconnect after 3 failures

line vty 0 4                             ! 8. Apply to virtual terminal lines
 login local                             ! 9. Authenticate against local username database
 transport input ssh                     ! 10. Disable Telnet completely
 exit
```

### Verification & Troubleshooting
```cisco
show ip ssh                              ! Verifies SSHv2 enabled, timeout, and retries
show ssh                                 ! Shows active inbound/outbound SSH sessions
show crypto key mypubkey rsa             ! Displays generated RSA public keys
```

---

## 2. AAA (Authentication, Authorization & Accounting)

### Core Theory Comparison (Exam High-Yield)
| Parameter | TACACS+ | RADIUS |
| :--- | :--- | :--- |
| **Standard** | Cisco Proprietary | Open IETF RFC Standard |
| **Transport Protocol / Port** | **TCP Port 49** | **UDP Ports 1812 (Auth/Authz) & 1813 (Acct)** *(Legacy: 1645/1646)* |
| **Encryption Scope** | **Entire Packet Body** encrypted (Header in clear) | **Password only** encrypted (Rest of packet in clear) |
| **Architecture** | **Separates** Auth, Authz, and Accounting | **Combines** Authentication and Authorization |
| **Granularity** | Per-command authorization supported | Packet-level / Service profile authorization |

### Fallback Logic Rule
> [!IMPORTANT]
> When configuring method lists (e.g., `group tacacs+ local`), the router queries the secondary method (`local`) **ONLY if the primary server is unreachable or times out**. If the server responds with an **Authentication Failure (Reject)**, authentication is immediately **DENIED**.

### Account Lockout (Handout p. 147)
```cisco
aaa local authentication attempts max-fail 3   ! Lock local user after 3 bad passwords
show aaa local user lockout                    ! View locked accounts
clear aaa local user lockout username Admin    ! Unlock account
```

### Complete AAA Configuration (Local + Server-Based)
```cisco
configure terminal
aaa new-model                                  ! Globally activates AAA subsystem

! Define External AAA Servers
tacacs server TACACS-SRV
 address ipv4 192.168.1.100
 key ciscoTACACSkey
 exit

radius server RADIUS-SRV
 address ipv4 192.168.1.200
 auth-port 1812
 acct-port 1813
 key ciscoRADIUSkey
 exit

! Grouping (Optional)
aaa group server tacacs+ TACACS-GRP
 server name TACACS-SRV
 exit

! 1. Authentication (Default list for VTY / Console)
aaa authentication login default group tacacs+ local
aaa authentication login CONSOLE-LOGIN local

! 2. Authorization (Exec shell & Config commands)
aaa authorization exec default group tacacs+ local
aaa authorization commands 15 default group tacacs+ local

! 3. Accounting (Audit trail for executive sessions)
aaa accounting exec default start-stop group tacacs+

! Apply to Lines
line con 0
 login authentication CONSOLE-LOGIN
 exit
line vty 0 4
 login authentication default
 exit
```

### Verification Commands
```cisco
show aaa servers                         ! View uptime, transactions, timeouts of AAA servers
show aaa sessions                        ! Active authenticated sessions
debug aaa authentication                 ! Real-time debugging of login negotiation
debug aaa authorization                  ! Real-time debugging of privilege checks
```

---

## 3. Zone-Based Policy Firewall (ZPF)

### The 4-Step Golden Rule
1. **Define Zones**: `zone security <NAME>`
2. **Define Class-Maps**: Match traffic via protocol or ACL (`class-map type inspect match-any <NAME>`)
3. **Define Policy-Maps**: Assign actions (`inspect`, `pass`, `drop`) (`policy-map type inspect <NAME>`)
4. **Create Zone-Pair & Attach Policy**: `zone-pair security <ZP-NAME> source <SRC> destination <DST>` -> `service-policy type inspect <POLICY-NAME>`
5. **Assign Interfaces to Zones**: `zone-member security <NAME>` under interface

### ZPF Actions
- **Inspect**: Cisco stateful packet inspection. Permits outbound traffic AND automatically creates dynamic temporary pinholes for returning reply packets.
- **Pass**: Unidirectional permit. Return traffic is **NOT** automatically allowed; requires explicit reverse rule.
- **Drop**: Discards traffic silently (or with `drop log`).

### Self-Zone Rules
- The **Self-Zone** is the router itself (all its IP addresses).
- Traffic between any zone and the Self-Zone is **permitted by default** (management traffic like SSH, OSPF, BGP) unless a zone-pair with the `self` zone is explicitly defined.

### Complete ZPF Template
```cisco
configure terminal

! Step 1: Create Zones
zone security IN-ZONE
zone security OUT-ZONE

! Step 2: Class Map (Traffic Classification)
class-map type inspect match-any HTTP-TRAFFIC
 match protocol http
 match protocol https
 match protocol dns
 match protocol icmp
 exit

! Step 3: Policy Map (Inspection Action)
policy-map type inspect IN-TO-OUT-POLICY
 class type inspect HTTP-TRAFFIC
  inspect
 exit
 class class-default
  drop
 exit

! Step 4: Zone-Pair Binding
zone-pair security IN-TO-OUT-ZP source IN-ZONE destination OUT-ZONE
 service-policy type inspect IN-TO-OUT-POLICY
 exit

! Step 5: Assign Interfaces
interface GigabitEthernet0/1
 zone-member security IN-ZONE
 exit
interface Serial0/0/1
 zone-member security OUT-ZONE
 exit
```

### Verification
```cisco
show policy-map type inspect zone-pair   ! Shows packet hits, inspect counters, active sessions
show zone security                       ! Displays configured security zones
show zone-pair security                  ! Displays source, destination, and attached policies
```

---

## 4. Cisco ASA 5505 Firewall

### Security Level Principles
- **Scale**: `0` (Lowest/Untrusted) to `100` (Highest/Trusted).
- **Default Flow Rule**:
  - High -> Low (`100` -> `0`): **Permitted automatically** + statefully tracked.
  - Low -> High (`0` -> `100` or `0` -> `70`): **Dropped automatically** unless an explicit inbound Access-List is applied to the interface (`access-group <ACL> in interface <NAME>`).
- **Same Security Level**: Dropped by default; enable via `same-security-traffic permit inter-interface`.

### Real IP Rule (ASA 8.3+)
> [!IMPORTANT]
> When writing ACLs for inbound traffic to a NATed host (like a DMZ Web Server), **always specify the host's REAL (Private) IP**, NOT its public translated IP address!

### Complete ASA 5505 Configuration
```cisco
enable
configure terminal
hostname CCNAS-ASA
domain-name ccnasecurity.com
enable password ciscoenpa55

! Layer 3 Interfaces
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
 no forward interface vlan 1             ! Base license requirement
 nameif dmz
 security-level 70
 exit

interface Ethernet0/2
 switchport access vlan 3
 exit

! Routing
route outside 0.0.0.0 0.0.0.0 209.165.200.225

! Dynamic PAT (Inside Network)
object network inside-net
 subnet 192.168.1.0 255.255.255.0
 nat (inside,outside) dynamic interface
 exit

! Static 1:1 NAT (DMZ Web Server)
object network dmz-server
 host 192.168.2.3
 nat (dmz,outside) static 209.165.200.227
 exit

! Modular Policy Framework (MPF) - ICMP Stateful Return Inspection
class-map inspection_default
 match default-inspection-traffic
 exit
policy-map global_policy
 class inspection_default
  inspect icmp
 exit
service-policy global_policy global

! Inbound ACL (Allows Outside Hosts to reach DMZ Server)
access-list OUTSIDE-DMZ permit icmp any host 192.168.2.3
access-list OUTSIDE-DMZ permit tcp any host 192.168.2.3 eq 80
access-group OUTSIDE-DMZ in interface outside

! AAA & SSH Management
username admin password adminpa55
aaa authentication ssh console LOCAL
crypto key generate rsa modulus 1024
ssh 192.168.1.0 255.255.255.0 inside
ssh 172.16.3.3 255.255.255.255 outside
ssh timeout 10
```

### Verification
```cisco
show nameif                              ! Shows VLAN-to-NameIF mapping & security levels
show ip address                          ! Interface IP configuration
show nat                                 ! NAT policy hit counts
show xlate                               ! Current translation slots in RAM
show conn                                ! Active TCP/UDP connection state table
show access-list                         ! ACL hit counts
```

---

## 5. Site-to-Site IPsec VPN

### IKE Phase 1 vs IKE Phase 2 Cheat Sheet
| Phase | Name | Protocol / Port | Purpose | Key Commands |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **ISAKMP SA** | UDP Port 500 | Negotiate secure management channel between peers | `crypto isakmp policy <n>`<br>`crypto isakmp key <key> address <peer>` |
| **Phase 2** | **IPsec SA** | ESP (IP Protocol 50) | Negotiate parameters to encrypt actual user data payload | `crypto ipsec transform-set <NAME>`<br>`crypto map <NAME> <seq> ipsec-isakmp` |

### Step-by-Step Configuration Template (Router R1 & R3)

#### On Router 1 (R1 - Local LAN: `192.168.1.0/24`, Peer: `10.2.2.2`, Remote LAN: `192.168.3.0/24`)
```cisco
configure terminal

! 1. Interesting Traffic ACL (Permits Local LAN to Remote LAN)
access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255

! 2. IKE Phase 1 Policy & Pre-Shared Key
crypto isakmp policy 10
 encryption aes 256                      ! Or aes, 3des
 hash sha                                ! Or md5, sha256
 authentication pre-share
 group 5                                 ! Diffie-Hellman Group (2, 5, or 14)
 lifetime 86400
 exit
crypto isakmp key vpnpa55 address 10.2.2.2

! 3. IKE Phase 2 Transform-Set & Crypto Map
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
! (In custom lab: crypto ipsec transform-set jojo esp-3des esp-sha-hmac)

crypto map VPN-MAP 10 ipsec-isakmp
 set peer 10.2.2.2
 set transform-set VPN-SET
 match address 110
 exit

! 4. Bind Crypto Map to WAN Egress Interface
interface Serial0/0/0
 crypto map VPN-MAP
 exit
```

#### On Router 3 (R3 - Local LAN: `192.168.3.0/24`, Peer: `10.1.1.2`, Remote LAN: `192.168.1.0/24`)
```cisco
configure terminal

! 1. Reciprocal Interesting Traffic ACL
access-list 110 permit ip 192.168.3.0 0.0.0.255 192.168.1.0 0.0.0.255

! 2. IKE Phase 1 Policy & Pre-Shared Key
crypto isakmp policy 10
 encryption aes 256
 hash sha
 authentication pre-share
 group 5
 exit
crypto isakmp key vpnpa55 address 10.1.1.2

! 3. IKE Phase 2 Transform-Set & Crypto Map
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac

crypto map VPN-MAP 10 ipsec-isakmp
 set peer 10.1.1.2
 set transform-set VPN-SET
 match address 110
 exit

! 4. Bind Crypto Map to WAN Egress Interface
interface Serial0/0/1
 crypto map VPN-MAP
 exit
```

### Verification & Diagnostic Flow
1. **Trigger the Tunnel**: Routers do NOT bring up the IPsec tunnel until interesting traffic arrives. Always send a ping across the LANs first (`ping 192.168.3.3` from PC-A).
2. **Check Phase 1 State**:
   ```cisco
   show crypto isakmp sa
   ```
   *Success Output*: State must be **`QM_IDLE`** (Quick Mode Idle). If stuck in `MM_NO_STATE` or `MM_KEY_EXCH`, check pre-shared key, encryption, and peer IP address.
3. **Check Phase 2 Counters**:
   ```cisco
   show crypto ipsec sa
   ```
   *Success Output*: `#pkts encrypt: >0`, `#pkts decrypt: >0`.

---

## 6. DHCP Server & Relay Agent

### Router as DHCP Server
```cisco
configure terminal
ip dhcp excluded-address 192.168.1.1 192.168.1.10   ! Reserve gateways/servers
ip dhcp pool LAN-POOL
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 8.8.8.8
 domain-name security.local
 lease 7 0 0                                       ! 7 days lease
 exit
```

### Router as DHCP Relay Agent (IP Helper)
When clients are on LAN 1, but the DHCP Server is located in a central server room:
```cisco
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 ip helper-address 10.10.10.254                    ! Forwards broadcast DHCP as unicast
 no shutdown
 exit
```

---

## 7. Master Troubleshooting Matrix

| Symptom / Issue | Probable Cause | Diagnostic Command | Immediate Fix |
| :--- | :--- | :--- | :--- |
| **SSH connection refused** | Missing crypto key, missing domain-name, or VTY lines lack `transport input ssh` | `show ip ssh`, `show run \| sec line vty` | Configure `ip domain-name`, run `crypto key generate rsa modulus 1024`, add `transport input ssh` to `line vty 0 4`. |
| **AAA lockout / No access** | Misconfigured method list lock-out or no local fallback | `show aaa local user lockout` | Ensure `local` is at end of method list: `aaa authentication login default group tacacs+ local`. |
| **ZPF drops returning HTTP / Ping** | Action configured as `pass` instead of `inspect`, or missing reverse inspection rule | `show policy-map type inspect zone-pair` | Change action inside policy-map to `inspect`. |
| **IPsec SA never negotiates (0 pkts)** | No traffic has matched the interesting ACL, or mismatched peer IP | `show access-list 110`, `show crypto map` | Issue a ping between LAN endpoints to generate interesting packets. Ensure ACL matches source and destination subnets symmetrically. |
| **IPsec Phase 1 fails (`MM_NO_STATE`)** | Pre-shared key mismatch, ISAKMP encryption/DH mismatch, or intermediate firewall blocking UDP 500 | `debug crypto isakmp` | Verify `crypto isakmp key` string and peer address on both sides. |
| **ASA drops outbound ping replies** | ICMP inspection is disabled in default Modular Policy Framework | `show run policy-map` | Add `inspect icmp` under `policy-map global_policy` -> `class inspection_default`. |
| **ASA drops outside traffic to DMZ Server** | Missing inbound ACL or ACL references public IP instead of private IP | `show access-list` | In ASA 8.3+, write ACL using real IP: `access-list OUTSIDE-DMZ permit ... host 192.168.2.3`. |
