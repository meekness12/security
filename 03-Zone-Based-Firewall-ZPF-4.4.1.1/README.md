# Module 03: Zone-Based Policy Firewall (ZPF) - Activity 4.4.1.1

## Overview
Alinged with **Learning Unit 6 (Pages 185–205)** of the course handout and Cisco Packet Tracer Activity `4.4.1.1`, this lab configures a stateful Zone-Based Policy Firewall on edge router **R3** (`Cisco 1941`).

---

## 4-Step ZPF Architecture Workflow
1. **Define Security Zones**:
   - `zone security IN-ZONE`
   - `zone security OUT-ZONE`
2. **Classify Traffic with Extended ACL & Class-Map**:
   - `access-list 101 permit ip 192.168.3.0 0.0.0.255 any`
   - `class-map type inspect match-all IN-NET-CLASS-MAP` -> `match access-group 101`
3. **Define Policy Action via Policy-Map**:
   - `policy-map type inspect IN-2-OUT-PMAP`
   - `class type inspect IN-NET-CLASS-MAP` -> `inspect` (Invokes CBAC stateful tracking)
4. **Apply to Zone-Pair and Interfaces**:
   - `zone-pair security IN-2-OUT-ZPAIR source IN-ZONE destination OUT-ZONE`
   - `service-policy type inspect IN-2-OUT-PMAP`
   - `interface G0/1` -> `zone-member security IN-ZONE`
   - `interface S0/0/1` -> `zone-member security OUT-ZONE`

---

## Deliverables in this Directory
- [`4.4.1.1 Packet Tracer - Configuring a Zone-Based Policy Firewall (ZPF).pka`](4.4.1.1%20Packet%20Tracer%20-%20Configuring%20a%20Zone-Based%20Policy%20Firewall%20%28ZPF%29.pka): Original Packet Tracer Activity file.
- [`R3_Stage1_License.txt`](R3_Stage1_License.txt): Router R3 `securityk9` activation & reboot script.
- [`R3_Stage2_ZPF_Config.txt`](R3_Stage2_ZPF_Config.txt): Complete copy-paste ZPF configuration.
- [`Verification_Commands.txt`](Verification_Commands.txt): Session inspection (`show policy-map type inspect zone-pair sessions`) and ping block verification.
- [`4.4.1.1_ZPF_Configuration_Guide.docx`](4.4.1.1_ZPF_Configuration_Guide.docx): Complete Word documentation guide.
- [`STEP_BY_STEP_INSTRUCTIONS.md`](STEP_BY_STEP_INSTRUCTIONS.md): Detailed markdown walkthrough.
