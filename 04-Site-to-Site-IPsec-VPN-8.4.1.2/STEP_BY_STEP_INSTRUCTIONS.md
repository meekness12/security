# Cisco Packet Tracer 8.4.1.2 - Configure and Verify a Site-to-Site IPsec VPN Using CLI

## Activity Overview
- **File**: `8.4.1.2 Packet Tracer - Configure and Verify a Site-to-Site IPsec VPN using CLI.pka`
- **Target Devices**: Edge Routers `R1` and `R3`
- **Transit Device**: Router `R2` (Pass-through, unconfigured for VPN)
- **Objective**: Implement a site-to-site IPsec VPN tunnel between R1 and R3 across an unprotected WAN, encrypting traffic between internal LANs (`192.168.1.0/24` and `192.168.3.0/24`) while allowing uninteresting traffic (`192.168.2.0/24`) to transit normally.
- **Completion Goal**: 100%

---

## Pre-Configured Credentials & Parameters

| Credential Type | Parameter | Value |
| :--- | :--- | :--- |
| **Enable Secret** | Password | `ciscoenpa55` |
| **Console Line** | Password | `ciscoconpa55` |
| **VTY Lines** | Password | `ciscovtypa55` |
| **SSH Account** | Username / Password | `SSHadmin` / `ciscosshpa55` |
| **Routing Protocol** | OSPF Process ID | `101` (Active across all routers) |
| **ISAKMP Policy Number** | Policy ID | `10` |
| **IKE Phase 1 Encryption** | Algorithm / Hash | `AES 256` / `SHA-1` |
| **IKE Phase 1 Key Exchange** | Diffie-Hellman Group | `Group 5` |
| **ISAKMP Pre-Shared Key** | Secret Key | `vpnpa55` |
| **IPsec Phase 2 Transform-Set** | Name / Transforms | `VPN-SET` (`esp-aes esp-sha-hmac`) |
| **Crypto Map Name / Seq** | Name / Sequence / Type | `VPN-MAP 10 ipsec-isakmp` |
| **Interesting Traffic ACL** | Extended ACL Number | `110` |

---

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** | `G0/0`<br>`S0/0/0` (DCE) | `192.168.1.1`<br>`10.1.1.2` | `255.255.255.0`<br>`255.255.255.252` | N/A<br>N/A | Site 1 Edge (Peer: `10.2.2.2`) |
| **R2** | `G0/0`<br>`S0/0/0`<br>`S0/0/1` (DCE) | `192.168.2.1`<br>`10.1.1.1`<br>`10.2.2.1` | `255.255.255.0`<br>`255.255.255.252`<br>`255.255.255.252` | N/A<br>N/A<br>N/A | Transit Core (Pass-Through) |
| **R3** | `G0/0`<br>`S0/0/1` | `192.168.3.1`<br>`10.2.2.2` | `255.255.255.0`<br>`255.255.255.252` | N/A<br>N/A | Site 2 Edge (Peer: `10.1.1.2`) |
| **PC-A** | `NIC` | `192.168.1.3` | `255.255.255.0` | `192.168.1.1` | LAN 1 Workstation |
| **PC-B** | `NIC` | `192.168.2.3` | `255.255.255.0` | `192.168.2.1` | LAN 2 Workstation |
| **PC-C** | `NIC` | `192.168.3.3` | `255.255.255.0` | `192.168.3.1` | LAN 3 Workstation |

---

## Execution Guide: Step by Step

### Part 1: Configure IPsec Parameters on Router R1

#### Step 1: Test Baseline Connectivity
Open **PC-A** > **Desktop** > **Command Prompt**:
```cmd
ping 192.168.3.3
```
*Result*: 4/4 replies received (verifies OSPF end-to-end routing is working before configuring VPN).

#### Step 2: Enable Security License on R1
Open **R1** > **CLI** tab:
```cisco
enable
ciscoenpa55
configure terminal
license boot module c1900 technology-package securityk9
```
When prompted:
```
Do you accept the End User License Agreement (EULA)? [yes/no]: yes
```
Save configuration and reload:
```cisco
exit
copy running-config startup-config
reload
```
Press **[Enter]** to confirm reload. Wait ~5-10 seconds for R1 to reboot.

#### Step 3: Identify Interesting Traffic on R1
Enter privileged EXEC and config mode on R1:
```cisco
enable
ciscoenpa55
configure terminal
access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255
```

#### Step 4: Configure IKE Phase 1 ISAKMP Policy on R1
```cisco
crypto isakmp policy 10
 encryption aes 256
 authentication pre-share
 group 5
 exit
crypto isakmp key vpnpa55 address 10.2.2.2
```

#### Step 5: Configure IKE Phase 2 IPsec Policy on R1
```cisco
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac

crypto map VPN-MAP 10 ipsec-isakmp
 description VPN connection to R3
 set peer 10.2.2.2
 set transform-set VPN-SET
 match address 110
 exit
```

#### Step 6: Bind Crypto Map to Outgoing WAN Interface
```cisco
interface Serial0/0/0
 crypto map VPN-MAP
 exit
end
copy running-config startup-config
```

---

### Part 2: Configure IPsec Parameters on Router R3

#### Step 1: Enable Security License on R3
Open **R3** > **CLI** tab:
```cisco
enable
ciscoenpa55
configure terminal
license boot module c1900 technology-package securityk9
```
When prompted:
```
Do you accept the End User License Agreement (EULA)? [yes/no]: yes
```
Save configuration and reload:
```cisco
exit
copy running-config startup-config
reload
```
Press **[Enter]** to confirm reload. Wait ~5-10 seconds for R3 to reboot.

#### Step 2: Identify Interesting Traffic on R3 (Reciprocating ACL)
Enter privileged EXEC and config mode on R3:
```cisco
enable
ciscoenpa55
configure terminal
access-list 110 permit ip 192.168.3.0 0.0.0.255 192.168.1.0 0.0.0.255
```

#### Step 3: Configure IKE Phase 1 ISAKMP Policy on R3
```cisco
crypto isakmp policy 10
 encryption aes 256
 authentication pre-share
 group 5
 exit
crypto isakmp key vpnpa55 address 10.1.1.2
```

#### Step 4: Configure IKE Phase 2 IPsec Policy on R3
```cisco
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac

crypto map VPN-MAP 10 ipsec-isakmp
 description VPN connection to R1
 set peer 10.1.1.2
 set transform-set VPN-SET
 match address 110
 exit
```

#### Step 5: Bind Crypto Map to Outgoing WAN Interface
```cisco
interface Serial0/0/1
 crypto map VPN-MAP
 exit
end
copy running-config startup-config
```

---

### Part 3: Verify the IPsec VPN

#### Step 1: Check Tunnel State Before Interesting Traffic
On **R1 CLI**:
```cisco
show crypto ipsec sa
```
*Expected*: `#pkts encaps: 0, #pkts encrypt: 0, #pkts decaps: 0, #pkts decrypt: 0`.

#### Step 2: Generate Interesting Traffic
On **PC-A Command Prompt**:
```cmd
ping 192.168.3.3
```
*Expected*: Replies received from `192.168.3.3`.

#### Step 3: Check Tunnel State After Interesting Traffic
On **R1 CLI**:
```cisco
show crypto ipsec sa
```
*Expected*: `#pkts encaps: 4, #pkts encrypt: 4, #pkts decaps: 4, #pkts decrypt: 4`.
Also check IKE Phase 1 SA:
```cisco
show crypto isakmp sa
```
*Expected*: Status `QM_IDLE` with peer `10.2.2.2`.

#### Step 4: Generate Uninteresting Traffic
On **PC-A Command Prompt**:
```cmd
ping 192.168.2.3
```
*Expected*: Replies received from `192.168.2.3` (PC-B).

#### Step 5: Verify Uninteresting Traffic Bypass
On **R1 CLI**:
```cisco
show crypto ipsec sa | include #pkts encaps
```
*Expected*: Counter remains at `4`. Uninteresting traffic was not sent through the tunnel.

#### Step 6: Verify Completion
Click **Check Results** in Packet Tracer Activity window -> **100% Completion**.
