# Lab 8.4.1.2: Configure and Verify a Site-to-Site IPsec VPN using CLI

![Packet Tracer](https://img.shields.io/badge/Cisco_Packet_Tracer-v8.x-blue?logo=cisco)
![CCNA Security](https://img.shields.io/badge/CCNA_Security-2.0-green)
![Status](https://img.shields.io/badge/Status-100%25_Verified-success)

---

## Executive Summary
This laboratory guides you through deploying an enterprise-grade Site-to-Site IPsec VPN between edge routers **R1** and **R3** across an untrusted transit core router (**R2**). The implementation protects confidential data transmitted between branch networks `192.168.1.0/24` and `192.168.3.0/24` while permitting uninteresting transit traffic (`192.168.2.0/24`) to route normally in plaintext.

---

## Topology & Architectural Seams

```
[PC-A: 192.168.1.3]
        │
   (G0/0: 192.168.1.1)
     [Router R1] 
   (S0/0/0: 10.1.1.2)
        │
   [=== IPsec VPN Tunnel ===]
        │
   (S0/0/0: 10.1.1.1)
     [Router R2] (Transit ISP / OSPF Pass-through)
   (S0/0/1: 10.2.2.1)
        │
   [=== IPsec VPN Tunnel ===]
        │
   (S0/0/1: 10.2.2.2)
     [Router R3]
   (G0/0: 192.168.3.1)
        │
[PC-C: 192.168.3.3]
```

*Note: PC-B (`192.168.2.3`) connects to R2's LAN and serves as the destination for testing uninteresting, unencrypted transit traffic.*

---

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Function / Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** | `G0/0`<br>`S0/0/0` (DCE) | `192.168.1.1`<br>`10.1.1.2` | `255.255.255.0`<br>`255.255.255.252` | N/A<br>N/A | Site 1 Edge Router (Peer: `10.2.2.2`) |
| **R2** | `G0/0`<br>`S0/0/0`<br>`S0/0/1` (DCE) | `192.168.2.1`<br>`10.1.1.1`<br>`10.2.2.1` | `255.255.255.0`<br>`255.255.255.252`<br>`255.255.255.252` | N/A<br>N/A<br>N/A | Transit Core (Pass-Through) |
| **R3** | `G0/0`<br>`S0/0/1` | `192.168.3.1`<br>`10.2.2.2` | `255.255.255.0`<br>`255.255.255.252` | N/A<br>N/A | Site 2 Edge Router (Peer: `10.1.1.2`) |
| **PC-A** | `NIC` | `192.168.1.3` | `255.255.255.0` | `192.168.1.1` | Site 1 Workstation |
| **PC-B** | `NIC` | `192.168.2.3` | `255.255.255.0` | `192.168.2.1` | Transit Workstation (Uninteresting test) |
| **PC-C** | `NIC` | `192.168.3.3` | `255.255.255.0` | `192.168.3.1` | Site 2 Workstation |

---

## Core IPsec Concepts & Parameters

### 1. IKE Phase 1 (ISAKMP SA)
Establishes a secure bidirectional management channel between the two router endpoints.
- **Policy Number**: `10`
- **Encryption**: `AES 256`
- **Hash**: `SHA` (default: SHA-1)
- **Authentication**: `pre-share` (Pre-Shared Key: `vpnpa55`)
- **Key Exchange**: Diffie-Hellman `Group 5` (1536-bit)
- **Lifetime**: 86,400 seconds (default)

### 2. IKE Phase 2 (IPsec SA)
Establishes unidirectional Security Associations that negotiate data tunnel encryption parameters.
- **Transform-Set**: `VPN-SET` (`esp-aes esp-sha-hmac`)
- **Crypto Map**: `VPN-MAP 10 ipsec-isakmp`
- **Interesting Traffic**: Defined via Extended ACL `110`
- **Applied Interface**: Outbound WAN interface (`Serial0/0/0` on R1, `Serial0/0/1` on R3)

---

## Step-by-Step Implementation

### Step 1: Security Technology License Activation (R1 & R3)
Cisco ISR 1900 routers require the `securityk9` evaluation package enabled to support crypto commands.

**Execute on R1 and R3:**
```cisco
enable
ciscoenpa55
configure terminal
license boot module c1900 technology-package securityk9
! Enter 'yes' when prompted for the EULA
exit
copy running-config startup-config
reload
```

---

### Step 2: Router R1 Configuration
After reload, enter privileged EXEC mode on **R1**:

```cisco
enable
ciscoenpa55
configure terminal

! 1. Define Interesting Traffic ACL
access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255

! 2. Configure IKE Phase 1 (ISAKMP)
crypto isakmp policy 10
 encryption aes 256
 authentication pre-share
 group 5
 exit
crypto isakmp key vpnpa55 address 10.2.2.2

! 3. Configure IKE Phase 2 (Transform-Set and Crypto Map)
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac

crypto map VPN-MAP 10 ipsec-isakmp
 description VPN connection to R3
 set peer 10.2.2.2
 set transform-set VPN-SET
 match address 110
 exit

! 4. Apply Crypto Map to Outgoing Interface
interface Serial0/0/0
 crypto map VPN-MAP
 exit

end
copy running-config startup-config
```

---

### Step 3: Router R3 Configuration
Enter privileged EXEC mode on **R3**:

```cisco
enable
ciscoenpa55
configure terminal

! 1. Define Reciprocal Interesting Traffic ACL
access-list 110 permit ip 192.168.3.0 0.0.0.255 192.168.1.0 0.0.0.255

! 2. Configure IKE Phase 1 (ISAKMP)
crypto isakmp policy 10
 encryption aes 256
 authentication pre-share
 group 5
 exit
crypto isakmp key vpnpa55 address 10.1.1.2

! 3. Configure IKE Phase 2 (Transform-Set and Crypto Map)
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac

crypto map VPN-MAP 10 ipsec-isakmp
 description VPN connection to R1
 set peer 10.1.1.2
 set transform-set VPN-SET
 match address 110
 exit

! 4. Apply Crypto Map to Outgoing Interface
interface Serial0/0/1
 crypto map VPN-MAP
 exit

end
copy running-config startup-config
```

---

## Verification & Testing Procedure

### 1. Verify Before Triggering Traffic
On **R1 CLI**:
```cisco
show crypto ipsec sa
```
*Expected*: Packet counters are zero (`#pkts encaps: 0, #pkts encrypt: 0, #pkts decaps: 0, #pkts decrypt: 0`).

### 2. Trigger Interesting Traffic
From **PC-A Command Prompt**:
```cmd
ping 192.168.3.3
```
*Expected*: The first ping packet may time out during IKE negotiation (ARP/ISAKMP), followed by success (`Reply from 192.168.3.3: bytes=32 time=... TTL=...`).

### 3. Verify Active IPsec SA & ISAKMP SA
On **R1 CLI**:
```cisco
show crypto isakmp sa
```
*Expected State*: `QM_IDLE` with peer `10.2.2.2` (Quick Mode Idle indicates Phase 1 completed successfully).

```cisco
show crypto ipsec sa
```
*Expected Output*:
```text
interface: Serial0/0/0
    Crypto map tag: VPN-MAP, local addr 10.1.1.2
    protected vrf: (none)
    local  ident (addr/mask/prot/port): (192.168.1.0/255.255.255.0/0/0)
    remote ident (addr/mask/prot/port): (192.168.3.0/255.255.255.0/0/0)
    current_peer 10.2.2.2 port 500
    #pkts encaps: 4, #pkts encrypt: 4, #pkts digest: 4
    #pkts decaps: 4, #pkts decrypt: 4, #pkts verify: 4
```

### 4. Verify Bypass of Uninteresting Traffic
From **PC-A Command Prompt**:
```cmd
ping 192.168.2.3
```
*Expected*: Replies succeed from PC-B.

On **R1 CLI**:
```cisco
show crypto ipsec sa | include #pkts encaps
```
*Expected*: `#pkts encaps: 4` (Counter does **not** increment; uninteresting traffic bypassed the tunnel).

---

## Quick Reference / Troubleshooting

| Command | Purpose |
| :--- | :--- |
| `show crypto isakmp policy` | Lists configured Phase 1 ISAKMP policies |
| `show crypto isakmp sa` | Verifies Phase 1 tunnel state (`QM_IDLE` is healthy) |
| `show crypto ipsec transform-set` | Displays active Phase 2 transform suites |
| `show crypto ipsec sa` | Verifies Phase 2 packet encapsulation/encryption counters |
| `show crypto map` | Displays crypto map bindings, peers, and ACLs |
| `debug crypto isakmp` | Real-time troubleshooting for Phase 1 failures (mismatched PSK/DH) |
| `debug crypto ipsec` | Real-time troubleshooting for Phase 2 failures (mismatched transform/ACL) |
