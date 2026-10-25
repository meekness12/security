# Cisco Packet Tracer 4.4.1.1 - Configuring a Zone-Based Policy Firewall (ZPF)

## Activity Overview
- **File**: `4.4.1.1 Packet Tracer - Configuring a Zone-Based Policy Firewall (ZPF).pka`
- **Target Device**: Edge Router `R3`
- **Objective**: Implement a Zone-Based Policy Firewall (ZPF) allowing internal hosts (`IN-ZONE`) to reach external networks (`OUT-ZONE`) while dropping unsolicited traffic initiated from external networks.
- **Completion Goal**: 100%

---

## Pre-Configured Credentials

| Credential Type | Username / Level | Password |
| :--- | :--- | :--- |
| **Enable Secret** | Privileged EXEC Mode | `ciscoenpa55` |
| **Console Line** | Console 0 | `ciscoconpa55` |
| **VTY Lines** | Lines 0 to 4 | `ciscovtypa55` |
| **Local User** | `Admin` | `Adminpa55` |

---

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Zone Assignment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** | `G0/1`<br>`S0/0/0` (DCE) | `192.168.1.1`<br>`10.1.1.1` | `255.255.255.0`<br>`255.255.255.252` | N/A<br>N/A | External Network |
| **R2** | `S0/0/0`<br>`S0/0/1` (DCE) | `10.1.1.2`<br>`10.2.2.2` | `255.255.255.252`<br>`255.255.255.252` | N/A<br>N/A | External Network |
| **R3** | `G0/1`<br>`S0/0/1` | `192.168.3.1`<br>`10.2.2.1` | `255.255.255.0`<br>`255.255.255.252` | N/A<br>N/A | **`IN-ZONE`**<br>**`OUT-ZONE`** |
| **PC-A** | `NIC` | `192.168.1.3` | `255.255.255.0` | `192.168.1.1` | External Server |
| **PC-C** | `NIC` | `192.168.3.3` | `255.255.255.0` | `192.168.3.1` | Internal Client |

---

## Execution Guide: Step by Step

### Part 1: Baseline Network Connectivity Verification

1. **Test ICMP across the network from PC-A**:
   - Open **PC-A** > **Desktop** > **Command Prompt**.
   - Execute:
     ```cmd
     ping 192.168.3.3
     ```
   - *Result*: Should succeed with 4/4 replies (verifies baseline static routing is operational).

2. **Test SSH from PC-C to R2**:
   - Open **PC-C** > **Desktop** > **Command Prompt**.
   - Execute:
     ```cmd
     ssh -l Admin 10.2.2.2
     ```
   - When prompted for Password, enter: `Adminpa55`.
   - *Result*: You enter `R2>`.
   - Type `exit` to close the SSH session.

3. **Test HTTP from PC-C to PC-A Server**:
   - Open **PC-C** > **Desktop** > **Web Browser**.
   - In the URL bar, type: `192.168.1.3` and press **Go**.
   - *Result*: The Packet Tracer welcome page displays. Close the browser.

---

### Part 2: Security License & Firewall Zones on R3

#### Step 1: Enable the Security Technology Package on R3
Open **R3** > **CLI** tab and enter privileged EXEC mode:
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
Press **[Enter]** to confirm reload. Wait 5-10 seconds for R3 to boot back up.

#### Step 2: Create Firewall Zones
Re-enter config mode on R3:
```cisco
enable
ciscoenpa55
configure terminal
zone security IN-ZONE
exit
zone security OUT-ZONE
exit
```

---

### Part 3: Identify Traffic Using a Class-Map

#### Step 1: Extended ACL 101 for Internal Traffic
Define internal traffic originating from the `192.168.3.0/24` network:
```cisco
access-list 101 permit ip 192.168.3.0 0.0.0.255 any
```

#### Step 2: Class-Map Matching ACL 101
Create an inspect class-map that matches traffic identified in ACL 101:
```cisco
class-map type inspect match-all IN-NET-CLASS-MAP
 match access-group 101
exit
```

---

### Part 4: Specify Firewall Policies (Policy-Map)

Create the inspect policy-map, reference the class-map, and specify the `inspect` action:
```cisco
policy-map type inspect IN-2-OUT-PMAP
 class type inspect IN-NET-CLASS-MAP
  inspect
 exit
exit
```
*(IOS will print informational message: `%No specific protocol configured in class IN-NET-CLASS-MAP for inspection. All protocols will be inspected.`)*

---

### Part 5: Apply Firewall Policies to Zone-Pair and Interfaces

#### Step 1 & 2: Create Zone-Pair and Attach Service-Policy
```cisco
zone-pair security IN-2-OUT-ZPAIR source IN-ZONE destination OUT-ZONE
 service-policy type inspect IN-2-OUT-PMAP
 exit
```

#### Step 3: Assign Interfaces to Zones
```cisco
interface GigabitEthernet0/1
 zone-member security IN-ZONE
 exit

interface Serial0/0/1
 zone-member security OUT-ZONE
 exit
```

#### Step 4: Save Configuration
```cisco
end
copy running-config startup-config
```

---

### Part 6: Test Firewall Functionality (IN-ZONE -> OUT-ZONE)

1. **Ping PC-A from PC-C**:
   - On **PC-C** Command Prompt: `ping 192.168.1.3`
   - *Result*: Replies received (`4/4`, 0% loss). The firewall permits and tracks outbound ICMP.

2. **SSH from PC-C to R2 & View Sessions on R3**:
   - On **PC-C** Command Prompt: `ssh -l Admin 10.2.2.2` (Password: `Adminpa55`).
   - While session is connected, on **R3 CLI**, run:
     ```cisco
     show policy-map type inspect zone-pair sessions
     ```
   - *Result*: Shows an active established session from `192.168.3.3` to `10.2.2.2:22`.
   - On **PC-C**: Type `exit` to close the SSH session.

3. **HTTP from PC-C to PC-A Server & View Sessions on R3**:
   - On **PC-C** Web Browser: Enter `192.168.1.3` and click **Go**.
   - On **R3 CLI**, run:
     ```cisco
     show policy-map type inspect zone-pair sessions
     ```
   - *Result*: Shows an active HTTP connection from `192.168.3.3` to `192.168.1.3:80`.
   - Close the browser on PC-C.

---

### Part 7: Test Firewall Functionality (OUT-ZONE -> IN-ZONE)

1. **Ping PC-C from PC-A (External Host)**:
   - On **PC-A** Command Prompt: `ping 192.168.3.3`
   - *Result*: **Request timed out** (Packets: Sent = 4, Lost = 4, 100% loss). Unsolicited inbound traffic is dropped by default.

2. **Ping PC-C from R2**:
   - On **R2 CLI**: `ping 192.168.3.3`
   - *Result*: `.....` Success rate is 0 percent (0/5).

---

### Part 8: Verify Activity Completion

In the Cisco Packet Tracer Activity window, click **Check Results**.
- **Completion**: 100%
- Assessment Items: All items green and checked.
