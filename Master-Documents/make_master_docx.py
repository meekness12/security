import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

def create_master_document(output_path):
    doc = docx.Document()
    
    # Page setup - Margins 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header and Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Network Security Practical Examination Reference Manual | 2026")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Confidential Academic Preparation - GitHub Repository: github.com/meekness12/security")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    PRIMARY = RGBColor(26, 54, 93)     # Deep Navy
    SECONDARY = RGBColor(13, 148, 136) # Teal
    TEXT_COLOR = RGBColor(51, 65, 85)  # Slate
    CODE_COLOR = RGBColor(15, 23, 42)  # Dark Navy
    MUTED_GRAY = RGBColor(100, 116, 139)

    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", 
                         color="CBD5E1", sz="4"):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="{top}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="{left}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="{bottom}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:right w:val="{right}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            </w:tcBorders>
        ''')
        tcPr.append(tcBorders)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(36)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(26)
        run.font.bold = True
        run.font.color.rgb = PRIMARY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(28)
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.italic = True
        run.font.color.rgb = SECONDARY
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = SECONDARY
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            brun = p.add_run(bold_prefix)
            brun.font.name = "Calibri"
            brun.font.size = Pt(10)
            brun.font.bold = True
            brun.font.color.rgb = PRIMARY
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = TEXT_COLOR
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            brun = p.add_run(bold_prefix)
            brun.font.name = "Calibri"
            brun.font.size = Pt(10)
            brun.font.bold = True
            brun.font.color.rgb = PRIMARY
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = TEXT_COLOR
        return p

    def add_code(text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="CBD5E1", sz="4")
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        lines = text.strip().split("\n")
        for i, line in enumerate(lines):
            run = p.add_run(line + ("\n" if i < len(lines)-1 else ""))
            run.font.name = "Consolas"
            run.font.size = Pt(8.5)
            run.font.color.rgb = CODE_COLOR
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(4)

    def add_callout(text, title="EXAM TIP"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "EFF6FF")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        set_cell_borders(cell, left="single", color="2563EB", sz="24")
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        trun = p.add_run(f"[{title}] ")
        trun.font.name = "Calibri"
        trun.font.size = Pt(9.5)
        trun.font.bold = True
        trun.font.color.rgb = RGBColor(37, 99, 235)
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(30, 58, 138)
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(4)

    def create_styled_table(headers, rows_data):
        tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        # Header row
        hdr_cells = tbl.rows[0].cells
        for col_idx, h_text in enumerate(headers):
            cell = hdr_cells[col_idx]
            set_cell_background(cell, "1A365D")
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="CBD5E1", sz="4")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(h_text)
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
        # Data rows
        for r_idx, row in enumerate(rows_data):
            row_cells = tbl.rows[r_idx + 1].cells
            bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row):
                cell = row_cells[c_idx]
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=80, bottom=80, left=140, right=140)
                set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="E2E8F0", sz="4")
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(str(val))
                run.font.name = "Calibri"
                run.font.size = Pt(9)
                run.font.color.rgb = TEXT_COLOR
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(6)

    # ==================== COVER / TITLE ====================
    add_title("Network Security Engineering & Practical Exam Guide")
    add_subtitle("Comprehensive Cisco IOS & ASA Security Reference Manual\nAligned with Course Handout (Units 5–7) & Cisco Packet Tracer Practical Labs")
    
    add_p("This master compilation contains the complete technical specifications, architectural diagrams, step-by-step CLI implementations, verification workflows, and troubleshooting diagnostic procedures required for the Network Security practical examination. All configurations are verified 100% in Cisco Packet Tracer.")
    
    add_callout("Review Section 8 (Master Cram Sheet) for rapid revision of core command syntax, security levels, and Phase 1 vs Phase 2 negotiation parameters prior to entering the exam.", "EXAM READINESS")

    doc.add_page_break()

    # ==================== MODULE 1 ====================
    add_h1("Module 1: SSHv2 Secure Administrative Management")
    add_p("Telnet transmits all administrative authentication credentials and CLI commands in unencrypted plaintext across the network fabric. Cisco IOS routers and switches must be secured using SSH version 2 to ensure cryptographic confidentiality, session integrity, and peer authentication.")
    
    add_h2("Prerequisites & Configuration Sequence")
    add_bullet(" Configure an explicit, unique device hostname (the default 'Router' prevents key generation).", "1. Unique Hostname:")
    add_bullet(" Configure an IP domain name (e.g., 'ip domain-name security.local').", "2. IP Domain Name:")
    add_bullet(" Generate RSA crypto key pairs with at least 1024 bits modulus (2048 recommended for production).", "3. RSA Key Generation:")
    add_bullet(" Create a local administrator account with privilege level 15 secret.", "4. Local Credentials:")
    add_bullet(" Enforce SSHv2 ('ip ssh version 2') and configure timeout and retries.", "5. Hardening Parameters:")
    add_bullet(" Apply 'login local' and 'transport input ssh' on line vty 0 4.", "6. VTY Enforcement:")

    add_h2("Complete Router Hardening Script")
    add_code("""configure terminal
hostname R1
ip domain-name security.local
crypto key generate rsa modulus 1024

username Admin privilege 15 secret Adminpa55
enable secret ciscoenpa55

ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3

line con 0
 password ciscoconpa55
 login
 logging synchronous
 exit

line vty 0 4
 login local
 transport input ssh
 exec-timeout 5 0
 logging synchronous
 exit

service password-encryption
banner motd # AUTHORIZED ACCESS ONLY - UNLAWFUL ACCESS WILL BE PROSECUTED #
end
copy running-config startup-config""")

    add_h2("Verification Commands")
    add_bullet(" Verifies SSH version 2 is active, timeout (60s), and retries (3).", "show ip ssh:")
    add_bullet(" Displays current active inbound and outbound SSH sessions.", "show ssh:")
    add_bullet(" Displays the generated RSA public key details.", "show crypto key mypubkey rsa:")

    # ==================== MODULE 2 ====================
    add_h1("Module 2: AAA Authentication, Authorization & Accounting")
    add_p("Authentication, Authorization, and Accounting (AAA) provides a modular, scalable security framework for controlling who is permitted access (Authentication), what actions they can perform (Authorization), and recording what they did (Accounting).")
    
    add_h2("TACACS+ vs. RADIUS Comparison Matrix")
    headers_aaa = ["Security Characteristic", "TACACS+ (Cisco Proprietary)", "RADIUS (Open Standard IETF)"]
    rows_aaa = [
        ["Transport Protocol / Port", "TCP Port 49 (Reliable connection-oriented)", "UDP Ports 1812 (Auth) & 1813 (Acct)"],
        ["Packet Encryption Scope", "Entire Packet Body encrypted (Header clear)", "Password Only encrypted (Rest in clear)"],
        ["Functional Architecture", "Separates Authentication, Authorization & Acct", "Combines Authentication & Authorization"],
        ["Command Authorization", "Granular per-command authorization supported", "Coarse-grained service profile authorization"],
        ["Primary Use Case", "Device Administrative Access (CLI)", "Network Access / VPN / 802.1X Port Access"]
    ]
    create_styled_table(headers_aaa, rows_aaa)

    add_callout("Fallback Logic: The secondary method in a method list (e.g., 'group tacacs+ local') is ONLY evaluated if the primary server times out or is unreachable. If the server sends an explicit REJECT, authentication is denied immediately.", "CRITICAL EXAM CONCEPT")

    add_h2("Local Account Lockout Configuration (Handout p. 147)")
    add_code("""configure terminal
aaa local authentication attempts max-fail 3
exit
! Verification & Management:
show aaa local user lockout
clear aaa local user lockout username Admin""")

    add_h2("Complete Server-Based AAA Configuration Script")
    add_code("""configure terminal
aaa new-model

! Define TACACS+ Server
tacacs server TACACS-SRV
 address ipv4 192.168.1.100
 key ciscoTACACSkey
 exit

! Define RADIUS Server
radius server RADIUS-SRV
 address ipv4 192.168.1.200
 auth-port 1812
 acct-port 1813
 key ciscoRADIUSkey
 exit

! Authentication Method Lists
aaa authentication login default group tacacs+ local
aaa authentication login CONSOLE-LOGIN local

! Authorization Method Lists
aaa authorization exec default group tacacs+ local
aaa authorization commands 15 default group tacacs+ local

! Accounting Method Lists
aaa accounting exec default start-stop group tacacs+

! Bind to Lines
line con 0
 login authentication CONSOLE-LOGIN
 exit

line vty 0 4
 login authentication default
 exit
end""")

    # ==================== MODULE 3 ====================
    add_h1("Module 3: Cisco Packet Tracer 4.4.1.1 - Zone-Based Policy Firewall (ZPF)")
    add_p("Zone-Based Policy Firewall (ZPF) replaces legacy interface-based stateful inspection (CBAC) with an intuitive, flexible security zone paradigm. Interfaces are assigned to zones, and directional inspection policies are applied between zone pairs.")

    add_h2("The ZPF 4-Step Engineering Lifecycle")
    add_bullet(" Create security zones ('IN-ZONE', 'OUT-ZONE').", "Step 1 - Define Zones:")
    add_bullet(" Classify traffic protocols using a class-map ('HTTP-TRAFFIC').", "Step 2 - Classify Traffic:")
    add_bullet(" Specify the firewall action ('inspect') in a policy-map.", "Step 3 - Define Policy:")
    add_bullet(" Create a zone-pair and attach the policy-map ('IN-TO-OUT-ZP').", "Step 4 - Attach to Zone-Pair:")
    add_bullet(" Assign physical/VLAN interfaces to their respective zones.", "Step 5 - Bind Interfaces:")

    add_h2("Router R3 Complete ZPF Implementation")
    add_code("""! Stage 1: Security Technology License Activation
enable
configure terminal
license boot module c1900 technology-package securityk9
! Enter 'yes' to accept EULA
exit
copy running-config startup-config
reload

! Stage 2: ZPF Configuration on R3
enable
configure terminal

! 1. Define Internal and External Zones
zone security IN-ZONE
zone security OUT-ZONE

! 2. Classify Internal Web/DNS/ICMP Traffic
access-list 101 permit ip 192.168.3.0 0.0.0.255 any

class-map type inspect match-any HTTP-TRAFFIC
 match protocol http
 match protocol https
 match protocol dns
 match protocol icmp
 exit

! 3. Configure Stateful Inspection Policy
policy-map type inspect IN-TO-OUT-POLICY
 class type inspect HTTP-TRAFFIC
  inspect
 exit
 class class-default
  drop
 exit

! 4. Create Zone-Pair and Attach Inspection Policy
zone-pair security IN-TO-OUT-ZP source IN-ZONE destination OUT-ZONE
 service-policy type inspect IN-TO-OUT-POLICY
 exit

! 5. Assign Physical Interfaces to Security Zones
interface GigabitEthernet0/1
 zone-member security IN-ZONE
 exit

interface Serial0/0/1
 zone-member security OUT-ZONE
 exit

end
copy running-config startup-config""")

    add_h2("Verification Commands")
    add_code("""show policy-map type inspect zone-pair
show zone security
show zone-pair security""")

    # ==================== MODULE 4 ====================
    add_h1("Module 4: Cisco Packet Tracer 8.4.1.2 - Site-to-Site IPsec VPN using CLI")
    add_p("IPsec provides network-layer cryptographic security across untrusted networks. It consists of IKE Phase 1 (ISAKMP SA for management tunnel) and IKE Phase 2 (IPsec SA for data tunnel).")

    add_h2("Phase 1 vs Phase 2 Parameter Matrix")
    headers_vpn = ["Parameter", "IKE Phase 1 (ISAKMP)", "IKE Phase 2 (IPsec)"]
    rows_vpn = [
        ["Policy / Container Name", "crypto isakmp policy 10", "crypto map VPN-MAP 10 ipsec-isakmp"],
        ["Encryption Algorithm", "AES 256", "esp-aes (in transform-set)"],
        ["Hash / Integrity", "SHA-1 (Default)", "esp-sha-hmac"],
        ["Authentication", "pre-share (Key: vpnpa55)", "Encapsulating Security Payload (ESP)"],
        ["Diffie-Hellman Group", "Group 5 (1536-bit modulus)", "Inherited from Phase 1 or PFS Group"],
        ["Scope of Protection", "Router-to-Router Management Channel", "End-Host Data Payload (ACL 110)"]
    ]
    create_styled_table(headers_vpn, rows_vpn)

    add_h2("Router R1 Configuration")
    add_code("""enable
configure terminal

! 1. Define Interesting Traffic ACL
access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255

! 2. IKE Phase 1 (ISAKMP Policy & Key)
crypto isakmp policy 10
 encryption aes 256
 authentication pre-share
 group 5
 exit
crypto isakmp key vpnpa55 address 10.2.2.2

! 3. IKE Phase 2 (Transform-Set & Crypto Map)
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac

crypto map VPN-MAP 10 ipsec-isakmp
 description VPN connection to R3
 set peer 10.2.2.2
 set transform-set VPN-SET
 match address 110
 exit

! 4. Bind Crypto Map to WAN Interface
interface Serial0/0/0
 crypto map VPN-MAP
 exit

end
copy running-config startup-config""")

    add_h2("Router R3 Configuration (Reciprocating Peer)")
    add_code("""enable
configure terminal

! 1. Reciprocal Interesting Traffic ACL
access-list 110 permit ip 192.168.3.0 0.0.0.255 192.168.1.0 0.0.0.255

! 2. IKE Phase 1 (ISAKMP Policy & Key)
crypto isakmp policy 10
 encryption aes 256
 authentication pre-share
 group 5
 exit
crypto isakmp key vpnpa55 address 10.1.1.2

! 3. IKE Phase 2 (Transform-Set & Crypto Map)
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac

crypto map VPN-MAP 10 ipsec-isakmp
 description VPN connection to R1
 set peer 10.1.1.2
 set transform-set VPN-SET
 match address 110
 exit

! 4. Bind Crypto Map to WAN Interface
interface Serial0/0/1
 crypto map VPN-MAP
 exit

end
copy running-config startup-config""")

    add_h2("Verification Procedure")
    add_bullet(" Must display 'QM_IDLE' with the remote peer address.", "show crypto isakmp sa:")
    add_bullet(" Look for '#pkts encaps > 0' and '#pkts decaps > 0' after pinging across the tunnel.", "show crypto ipsec sa:")

    # ==================== MODULE 5 ====================
    add_h1("Module 5: Cisco Packet Tracer 9.3.1.1 - Cisco ASA 5505 Firewall")
    add_p("The Cisco ASA 5505 Adaptive Security Appliance enforces stateful inspection based on interface security levels (0 to 100). Higher-to-lower traffic flows are permitted implicitly; lower-to-higher flows require explicit access lists.")

    add_h2("Core Architectural Rules")
    add_bullet(" Inside (100) > DMZ (70) > Outside (0). Unsolicited outside packets are dropped by default.", "Security Levels:")
    add_bullet(" Base license limits ASA 5505 to two fully forwarded VLANs. VLAN 3 requires 'no forward interface vlan 1'.", "Base License VLAN 3:")
    add_bullet(" In Cisco ASA version 8.3 and later, access-lists reference the REAL PRIVATE IP of destination hosts.", "Real IP in ACLs:")
    add_bullet(" ASA does NOT inspect ICMP return packets statefully by default. 'inspect icmp' in global_policy is required.", "MPF ICMP Inspection:")

    add_h2("Complete ASA 5505 Configuration Script")
    add_code("""enable
! Press [Enter] for initial blank password
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

! VLAN 3: DMZ Interface (Level 70, Isolated from VLAN 1)
interface vlan 3
 ip address 192.168.2.1 255.255.255.0
 no forward interface vlan 1
 nameif dmz
 security-level 70
 exit

interface Ethernet0/2
 switchport access vlan 3
 exit

! Static Default Route via ISP Gateway R1
route outside 0.0.0.0 0.0.0.0 209.165.200.225

! Dynamic PAT (Inside Network to Outside Interface)
object network inside-net
 subnet 192.168.1.0 255.255.255.0
 nat (inside,outside) dynamic interface
 exit

! Static 1:1 NAT (DMZ Web Server Public Translation)
object network dmz-server
 host 192.168.2.3
 nat (dmz,outside) static 209.165.200.227
 exit

! Modular Policy Framework (MPF) - ICMP Inspection
class-map inspection_default
 match default-inspection-traffic
 exit
policy-map global_policy
 class inspection_default
  inspect icmp
 exit
service-policy global_policy global

! DHCP Server for Inside Clients
dhcpd address 192.168.1.5-192.168.1.36 inside
dhcpd dns 209.165.201.2 interface inside
dhcpd enable inside

! AAA Local Authentication & SSH Access
username admin password adminpa55
aaa authentication ssh console LOCAL
crypto key generate rsa modulus 1024
ssh 192.168.1.0 255.255.255.0 inside
ssh 172.16.3.3 255.255.255.255 outside
ssh timeout 10

! Outside Inbound ACL Permitting HTTP & ICMP to DMZ Server
access-list OUTSIDE-DMZ permit icmp any host 192.168.2.3
access-list OUTSIDE-DMZ permit tcp any host 192.168.2.3 eq 80
access-group OUTSIDE-DMZ in interface outside

write memory""")

    add_h2("ASA Verification Commands")
    add_bullet(" Shows VLAN-to-NameIF mapping and security level assignments.", "show nameif:")
    add_bullet(" Shows translation hit counts for Dynamic PAT and Static NAT.", "show nat:")
    add_bullet(" Displays active translation table slots.", "show xlate:")
    add_bullet(" Displays active connection state table.", "show conn:")
    add_bullet(" Displays hit counters for the OUTSIDE-DMZ access-list.", "show access-list:")

    # ==================== MODULE 6 ====================
    add_h1("Module 6: Site-to-Site IPsec VPN Custom Topology (Handout p. 226)")
    add_p("This topology represents the custom university practical assessment scenario consisting of HQ Router, ISP Transit Router, and Branch Router. The objective is to build an IPsec tunnel between HQ and Branch using policy number 12, pre-shared key 'jojo123', transform-set 'jojo', and ACL 120.")

    add_h2("Custom Parameter Specifications")
    headers_custom = ["Parameter", "HQ Router", "Branch Router"]
    rows_custom = [
        ["ISAKMP Policy ID", "crypto isakmp policy 12", "crypto isakmp policy 12"],
        ["Encryption / Hash", "3DES / SHA", "3DES / SHA"],
        ["Diffie-Hellman Group", "Group 2 (1024-bit)", "Group 2 (1024-bit)"],
        ["Pre-Shared Key", "jojo123 (peer 10.0.0.6)", "jojo123 (peer 10.0.0.1)"],
        ["Transform-Set Name", "jojo (esp-3des esp-sha-hmac)", "jojo (esp-3des esp-sha-hmac)"],
        ["Crypto Map Name / Seq", "jojo 12 ipsec-isakmp", "jojo 12 ipsec-isakmp"],
        ["Interesting Traffic ACL", "ACL 120 (192.168.10.0 -> 192.168.20.0)", "ACL 120 (192.168.20.0 -> 192.168.10.0)"]
    ]
    create_styled_table(headers_custom, rows_custom)

    add_h2("HQ Router Configuration")
    add_code("""enable
configure terminal
hostname HQ

interface GigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
 exit

interface Serial0/1/0
 ip address 10.0.0.1 255.255.255.252
 no shutdown
 exit

ip route 0.0.0.0 0.0.0.0 10.0.0.2

access-list 120 permit ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255

crypto isakmp policy 12
 encryption 3des
 hash sha
 authentication pre-share
 group 2
 exit

crypto isakmp key jojo123 address 10.0.0.6
crypto ipsec transform-set jojo esp-3des esp-sha-hmac

crypto map jojo 12 ipsec-isakmp
 set peer 10.0.0.6
 set transform-set jojo
 match address 120
 exit

interface Serial0/1/0
 crypto map jojo
 exit

end
copy running-config startup-config""")

    add_h2("Branch Router Configuration")
    add_code("""enable
configure terminal
hostname Branch

interface GigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
 exit

interface Serial0/1/0
 ip address 10.0.0.6 255.255.255.252
 no shutdown
 exit

ip route 0.0.0.0 0.0.0.0 10.0.0.5

access-list 120 permit ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255

crypto isakmp policy 12
 encryption 3des
 hash sha
 authentication pre-share
 group 2
 exit

crypto isakmp key jojo123 address 10.0.0.1
crypto ipsec transform-set jojo esp-3des esp-sha-hmac

crypto map jojo 12 ipsec-isakmp
 set peer 10.0.0.1
 set transform-set jojo
 match address 120
 exit

interface Serial0/1/0
 crypto map jojo
 exit

end
copy running-config startup-config""")

    # ==================== MODULE 7 ====================
    add_h1("Module 7: DHCP Server & Relay Infrastructure")
    add_p("Automatic host configuration via DHCP is a foundational network service. This module covers configuring a Cisco IOS router as a DHCP server as well as deploying a DHCP relay agent (ip helper-address) to service remote LAN segments across a routed boundary.")

    add_h2("Router as DHCP Server Configuration")
    add_code("""configure terminal
! Exclude statically assigned default gateway and server addresses
ip dhcp excluded-address 192.168.1.1 192.168.1.10

! Define the DHCP Pool
ip dhcp pool CORPORATE-LAN
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 8.8.8.8 1.1.1.1
 domain-name corporate.local
 lease 7 0 0
 exit""")

    add_h2("DHCP Relay Agent Configuration (IP Helper)")
    add_p("DHCP Discover and Request packets are Layer 2 broadcasts (`255.255.255.255`). Routers drop broadcasts by default. The `ip helper-address` command intercepts incoming UDP broadcast broadcasts on port 67/68 and forwards them as unicast packets directly to the central DHCP server.")
    add_code("""interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 ip helper-address 10.10.10.254
 no shutdown
 exit""")

    add_h2("Verification Commands")
    add_bullet(" Displays all active leased IP addresses and client MAC addresses.", "show ip dhcp binding:")
    add_bullet(" Shows pool utilization, total leased addresses, and pool size.", "show ip dhcp pool:")
    add_bullet(" Displays conflicting IP addresses detected via gratuitous ARP.", "show ip dhcp conflict:")

    # ==================== MODULE 8 ====================
    doc.add_page_break()
    add_title("Section 8: Master Exam Cram Sheet & Diagnostic Matrix")
    add_subtitle("Rapid-Fire Revision Card for Practical Lab Examination")

    add_h2("Essential IOS & ASA Command Quick Reference")
    headers_cmd = ["Technology", "Key Configuration Command", "Primary Verification Command"]
    rows_cmd = [
        ["SSHv2", "crypto key generate rsa modulus 1024\ntransport input ssh", "show ip ssh\nshow ssh"],
        ["Local Account Lockout", "aaa local authentication attempts max-fail 3", "show aaa local user lockout"],
        ["AAA Authentication", "aaa authentication login default group tacacs+ local", "debug aaa authentication"],
        ["TACACS+ Server", "tacacs server <NAME>\n address ipv4 <IP>\n key <KEY>", "show aaa servers"],
        ["RADIUS Server", "radius server <NAME>\n address ipv4 <IP>\n auth-port 1812 key <KEY>", "show aaa servers"],
        ["ZPF Class-Map", "class-map type inspect match-any <NAME>\n match protocol http", "show class-map type inspect"],
        ["ZPF Policy-Map", "policy-map type inspect <NAME>\n class type inspect <CM>\n  inspect", "show policy-map type inspect"],
        ["ZPF Zone-Pair", "zone-pair security <NAME> source <S> destination <D>\n service-policy type inspect <PM>", "show policy-map type inspect zone-pair"],
        ["ASA Security Level", "interface vlan <N>\n nameif <inside|outside|dmz>\n security-level <0-100>", "show nameif\nshow ip address"],
        ["ASA Dynamic PAT", "object network inside-net\n subnet <NET> <MASK>\n nat (inside,outside) dynamic interface", "show nat\nshow xlate"],
        ["ASA Static NAT", "object network dmz-srv\n host <REAL-IP>\n nat (dmz,outside) static <PUB-IP>", "show nat\nshow xlate"],
        ["ASA Inbound ACL", "access-list <NAME> permit tcp any host <REAL-IP> eq 80\naccess-group <NAME> in interface outside", "show access-list"],
        ["ASA ICMP Inspection", "policy-map global_policy\n class inspection_default\n  inspect icmp", "show run policy-map"],
        ["IPsec Phase 1", "crypto isakmp policy 10\n encryption aes 256\n group 5\ncrypto isakmp key <KEY> address <PEER>", "show crypto isakmp sa (Status: QM_IDLE)"],
        ["IPsec Phase 2", "crypto ipsec transform-set <NAME> esp-aes esp-sha-hmac\ncrypto map <NAME> 10 ipsec-isakmp", "show crypto ipsec sa (#pkts encrypt > 0)"],
        ["DHCP Server", "ip dhcp pool <NAME>\n network <NET> <MASK>\n default-router <GW>", "show ip dhcp binding"]
    ]
    create_styled_table(headers_cmd, rows_cmd)

    add_h2("Practical Exam Troubleshooting Matrix")
    headers_tb = ["Symptom", "Probable Root Cause", "Immediate Resolution"]
    rows_tb = [
        ["SSH connection refused", "Domain name not set, RSA key not generated, or missing 'transport input ssh'.", "Set 'ip domain-name test.com', generate 1024-bit key, and add 'transport input ssh' to line vty."],
        ["AAA lockout on VTY/Console", "Server unreachable and no 'local' fallback specified in method list.", "Always ensure 'local' is at end of method list: 'group tacacs+ local'."],
        ["ZPF blocks returning traffic", "Action in policy-map was configured as 'pass' instead of 'inspect'.", "Change policy action to 'inspect' so stateful reverse pinholes are dynamically created."],
        ["IPsec tunnel stays down (0 pkts)", "No traffic matched ACL, or peer IP/pre-shared key mismatch.", "Ping across LANs to trigger interesting traffic. Check 'show crypto isakmp sa'. Ensure keys match."],
        ["IPsec Phase 1 stuck in MM_NO_STATE", "Phase 1 parameter mismatch (encryption, hash, DH group) or wrong peer IP.", "Run 'debug crypto isakmp'. Verify encryption and pre-shared key on both ends."],
        ["ASA blocks outbound pings", "Default MPF does not inspect ICMP return traffic.", "Add 'inspect icmp' under 'policy-map global_policy' -> 'class inspection_default'."],
        ["ASA blocks outside access to DMZ", "ACL references public translated IP instead of real private IP.", "In ASA 8.3+, write ACL using private IP: 'permit tcp any host 192.168.2.3 eq 80'."]
    ]
    create_styled_table(headers_tb, rows_tb)

    # Save file
    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out_dir = r"C:\Users\user\Downloads\security\Master-Documents"
    out_file = os.path.join(out_dir, "Network_Security_Master_Exam_Guide.docx")
    create_master_document(out_file)
