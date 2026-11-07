# Gateway VOD MediaCipher SimulCrypt - COMPREHENSIVE TEST CASES
# APEX3K-NE System - Updated Reference Implementation

**Document Version:** 2.0  
**Date:** 2026-11-04  
**Platform:** APEX3K-NE Network Element with APEX-NE EM  
**Purpose:** Complete test case coverage with APEX3K-NE specific UI paths and procedures  
**Total Test Cases:** 50+

---

## EXECUTIVE SUMMARY & SYSTEM REFERENCE

This comprehensive test case document covers all 8 requirements with specific APEX3K-NE configuration paths and procedures based on the reference implementation documentation.

### APEX3K-NE System Overview
- **Network Element:** APEX3K-NE
- **Management Interface:** APEX-NE EM (Element Manager)
Input Method: Unicast video streams via GigE
- **VOD Streamer:** M3-Server (sends streams to Virtual IP)
- **Configuration Tool:** APEX-NE EM web/desktop application
- **Packet Analysis:** MPEG Tracker (connected after APEX3K RF output)
- **Maximum CAS Configuration:** 1 Internal MediaCipher + 3 External SuperCAS

### Key Configuration References
**SimulCrypt at Chassis Level:**
- Path: **APEX-NE EM >> Simulcrypt >> General >> "Mediacipher Simulcrypt" : Enable/Disable**

**ECMG Server Configuration:**
- Path: **APEX-NE EM >> Simulcrypt >> HOST configuration** (ECMG server IP)

**CAS Configuration:**
- Path: **APEX-NE EM >> Simulcrypt >> CAS configuration** (Max 3 external CAS)
- Action: **Add the ECMG and assign to the CAS**

**Gateway VOD Configuration:**
- Enable GVOD: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Config >> Enable Gateway VOD parameter**
- Configure Virtual IP (Ingress): Where GVOD input streams received
- Configure Output IP: Where APEX3K-NE sends TS output

**Blade-Level SimulCrypt:**
- Path: **APEX3K-NE >> Blade >> Select Blade<1> >> Gateway VOD MC Simulcrypt = Enable/Disable**

**CTE Encryption:**
- Path: **APEX3K-NE EM >> Chassis >> VOD >> CTE configuration**

**Pre-encrypted & DTCP:**
- Path: **APEX3K-NE EM >> VOD >> Session control configurations**
- Options: Follow DTCP Descriptor (Enable/Disable), Pre-encrypted Checking (Enable/Disable)
- **Pre-encrypted Checking ENABLED:** Input with CA_descriptor → Pass-through with SAME CA_descriptor (no re-encryption)
- **Pre-encrypted Checking DISABLED:** Input CA_descriptor → Stripped and replaced with CTE CA_descriptor (re-encryption)

---

## Requirement Coverage Matrix

| Requirement ID | Title | Test Cases | APEX3K-NE Path | Status |
| --- | --- | --- | --- | --- |
| **REL1.2.15-010** | Global Configuration | 7 | Simulcrypt >> General / Blade >> Config | ✓ UPDATED |
| **REL1.2.15-020** | CTE Encryption SCTE-52 | 3 | Chassis >> VOD >> CTE | ✓ |
| **REL1.2.15-030** | ECM Insertion & PMT | 25 | Simulcrypt >> CAS Config | ✓ EXTENSIVE |
| **REL1.2.15-040** | Transport Stream Capacity | 4 | Blade >> Gateway VOD | ✓ |
| **REL1.2.15-050** | Pre-encrypted & DTCP | 10 | VOD >> Session control | ✓ UPDATED |
| **REL1.2.15-060** | Encryption Status Display | 3 | Blades >> GVOD status | ✓ UPDATED |
| **REL1.2.15-070** | SDM Plug-in & MIB | 3 | SDM Interface / config.ini | ✓ UPDATED |
| **REL1.2.15-080** | Aurora Networks Branding | 2 | GUI / About | ✓ UPDATED |

---

## 1.0 REL1.2.15-010: Global Configuration Option

### 1.0.1 Test Case: Enable MediaCipher SimulCrypt at Chassis Level (APEX3K-NE)
**Test ID:** TC_REL1.2.15-010_001  
**Severity:** CRITICAL  
#### 1.0.1.2 Objectives
**Objective:** Verify MediaCipher SimulCrypt enabled globally at chassis level via APEX-NE EM

#### 1.0.1.1 Initial Condition
- APEX3K-NE installed and operational
- APEX-NE EM accessible and authenticated
- No Gateway VOD streams currently configured with MediaCipher SimulCrypt
- Administrator access available

#### 1.0.1.3 Procedure
1. Launch APEX-NE EM application
2. From main menu, navigate to: **Simulcrypt >> General**
3. Locate field "Mediacipher Simulcrypt"
4. Verify current value (should show Enable/Disable toggle or radio buttons)
5. If currently Disabled, select **Enable**
6. Verify confirmation dialog appears (if applicable)
7. Click **Save** or **Apply** button
8. Wait for confirmation message (target: < 3 seconds)
9. Verify status shows "Configuration applied successfully"
10. Navigate back to verify persistence: **Simulcrypt >> General**
11. Confirm "Mediacipher Simulcrypt" still shows **Enable**
12. Schedule system shutdown/restart
13. Power down APEX3K-NE, wait 2 minutes
14. Power on APEX3K-NE and wait for full boot (typically 5-10 minutes)
15. Re-authenticate to APEX-NE EM
16. Navigate to: **Simulcrypt >> General**
17. Verify "Mediacipher Simulcrypt" still shows **Enable** (persistence confirmed)


18. Verify **PASS CRITERIA:** Setting saved and applied without errors, All transport streams show encrypted status, Setting survives APEX3K-NE restart, No per-stream configuration needed
#### 1.0.1.4 Expected Results
- Configuration enabled successfully on first attempt
- Confirmation appears within 3 seconds
- Configuration persists across system restart
- No error messages or warnings
- System logs show configuration change event with timestamp
- **Monitoring Points:** Monitor in APEX-NE EM: Simulcrypt >> General >> Mediacipher Simulcrypt = Enable, Check system logs: [Timestamp] Configuration: Mediacipher Simulcrypt enabled by [User], Monitor MPEG Tracker for ECM PID presence (if streams active)

---

### 1.0.2 Test Case: Enable MediaCipher SimulCrypt at Blade Level (APEX3K-NE)
**Test ID:** TC_REL1.2.15-010_002  
**Severity:** CRITICAL  
#### 1.0.2.2 Objectives
**Objective:** Verify blade-level SimulCrypt configuration via APEX3K-NE EM for isolated per-blade control

#### 1.0.2.1 Initial Condition
- Multi-blade APEX3K-NE system operational
- APEX-NE EM accessible for both blades
- Separate Gateway VOD configurations per blade
- Administrator access available

#### 1.0.2.3 Procedure
1. Launch APEX-NE EM application
2. Navigate to: **Blade >> Select Blade<1> >> Configuration**
3. Locate field "Enable Gateway VOD parameter"
4. Select **Enable** if not already enabled
5. In the same screen, configure:
   - **Virtual IP:** Enter Ingress IP (example: 192.168.1.100)
   - **Output IP:** Enter Output IP (example: 192.168.1.101)
6. Click **Save** for Blade<1>
7. Navigate to: **Blade >> Select Blade<1> >> Gateway VOD MC Simulcrypt**
8. Select **Enable** (this is blade-level SimulCrypt enable)
9. Click **Save**
10. Navigate to: **Blade >> Select Blade<2> >> Configuration**
11. Verify Gateway VOD enabled (should show same settings)
12. Navigate to: **Blade >> Select Blade<2> >> Gateway VOD MC Simulcrypt**
13. Verify this shows **Disable** (or different state than Blade<1>)
14. If present, check Blade<3> similarly
15. Create test VOD stream on Blade<1>:
    - Stream 1-A: Verify encrypted with MediaCipher
16. Create test VOD stream on Blade<2>:
    - Stream 2-A: Verify NOT encrypted (if blade config is Disable)
17. Monitor both streams simultaneously to confirm isolation


18. Verify **PASS CRITERIA:** Blade-level configuration independent and isolated, Each blade maintains separate encryption state, No cross-blade configuration interference, Output streams match blade-level configuration
#### 1.0.2.4 Expected Results
- Blade<1> Gateway VOD MC Simulcrypt = Enable
- Blade<2> Gateway VOD MC Simulcrypt = Disable (or different state)
- Blade<1> streams encrypted
- Blade<2> streams NOT encrypted (or per configured state)
- No cross-blade interference
- Configuration isolated per blade
- **Monitoring Points:** Verify via APEX-NE EM: Blade > Blade<1> > Config > Gateway VOD MC Simulcrypt, Verify via APEX-NE EM: Blade > Blade<2> > Config > Gateway VOD MC Simulcrypt, Monitor MPEG Tracker output from both blades, Verify ECM PID presence/absence per blade configuration

---

### 1.0.3 Test Case: Disable MediaCipher SimulCrypt at Chassis Level
**Test ID:** TC_REL1.2.15-010_003  
**Severity:** HIGH  
#### 1.0.3.2 Objectives
**Objective:** Verify graceful disable of MediaCipher SimulCrypt globally at chassis level

#### 1.0.3.1 Initial Condition
- MediaCipher SimulCrypt currently enabled: **Simulcrypt >> General = Enable**
- Multiple Gateway VOD streams actively encrypted
- MPEG Tracker monitoring output streams
- STBs receiving encrypted streams

#### 1.0.3.3 Procedure
1. Verify current state: Navigate to **Simulcrypt >> General**
2. Confirm "Mediacipher Simulcrypt" = **Enable**
3. Monitor active streams in MPEG Tracker (document ECM PIDs present)
4. Navigate to: **Simulcrypt >> General**
5. Select "Mediacipher Simulcrypt" = **Disable**
6. Click **Save** or **Apply**
7. Wait for configuration to propagate (typically < 2 seconds)
8. Monitor MPEG Tracker output for ECM PID changes
9. Observe output streams for brief signal interruption (expected < 1 second)
10. Verify all existing streams stop ECM insertion (ECM PID should disappear)
11. Create new VOD stream:
    - Stream NEW-1: Verify created without encryption
    - Verify no ECM PIDs in new stream
12. Monitor system logs for disable event
13. Verify STB reception continues (graceful transition)


14. Verify **PASS CRITERIA:** Configuration change applied within 5 seconds, New streams created without encryption, Existing streams handled gracefully, System remains stable after disabling, No error messages
#### 1.0.3.4 Expected Results
- Configuration disabled successfully
- Existing streams gracefully transition to unencrypted
- New streams created without encryption
- Service continuity maintained
- ECM generation stops (ECMG no longer generating)
- Minimal service interruption (< 5 seconds per stream)
- **Monitoring Points:** Monitor APEX-NE EM: Simulcrypt >> General >> Mediacipher Simulcrypt = Disable, Track MPEG Tracker output: ECM PIDs should disappear, Monitor ECMG server: ECM generation should stop, Check system logs for disable event

---

### 1.0.4 Test Case: Verify No Per-Stream Configuration Option Exists
**Test ID:** TC_REL1.2.15-010_004  
**Severity:** CRITICAL  
#### 1.0.4.2 Objectives
**Objective:** Confirm absence of per-transport-stream encryption configuration in APEX3K-NE EM

#### 1.0.4.1 Initial Condition
- Gateway VOD enabled: **Blade >> Select Blade<1> >> Config >> Enable Gateway VOD**
- 5+ transport stream mappings exist: **Blade >> Select Blade<1> >> Gateway VOD Status** (verify TS and Mappings table)
- APEX-NE EM fully accessible

#### 1.0.4.3 Procedure
1. Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status**
2. Display list of all transport streams and mappings in the table
3. Select Stream Mapping #1 (click to open configuration)
4. Review ALL available configuration tabs/sections for this stream:
   - General/Properties
   - Input Configuration
   - Output Configuration
   - Encryption (should NOT exist)
   - Security/CAS (should NOT exist)
   - Advanced Options
5. Search configuration screen for keywords: "encryption", "SimulCrypt", "CAS", "ECM", "security"
6. Document any found (should be zero)
7. Close and select Stream Mapping #2
8. Repeat search for encryption options (should be zero)
9. Repeat for Mappings #3, #4, #5
10. Check APEX-NE EM Help/Documentation for per-stream encryption options
11. Search Help for: "per-stream", "stream encryption", "individual stream"
12. Document results (should show no per-stream encryption option)


13. Verify **PASS CRITERIA:** No encryption option found in stream configuration screens, Verified across minimum 5 different streams, Help documentation confirms absence, Complete absence of per-stream controls confirmed
#### 1.0.4.4 Expected Results
- Zero per-stream encryption configuration options found
- Zero encryption-related fields in any stream mapping
- Help documentation confirms no per-stream option exists
- Only global/chassis and blade-level configurations available
- All streams inherit settings from global level
- **Monitoring Points:** Scan all stream configuration menus systematically, Check VOD Mapping configuration screen thoroughly, Review APEX-NE EM Help and user guides, Document any findings of per-stream encryption (should be zero)

---

### 1.0.5 Test Case: Gateway VOD Enabled - Regular TS Mappings Hidden on Blade
**Test ID:** TC_REL1.2.15-010_005  
**Severity:** MEDIUM  
#### 1.0.5.2 Objectives
**Objective:** Verify that enabling Gateway VOD on a blade makes other TS types unavailable for configuration on that blade (TS mapping configuration is restricted when GVOD is enabled)

#### 1.0.5.1 Initial Condition
- APEX3K-NE multi-blade system operational (minimum 2 blades)
- Blade<1> has existing TS mappings configured (regular/standard TS)
- Blade<2> also has TS mappings configured
- APEX-NE EM fully accessible
- Gateway VOD disabled on Blade<1> (other TS types available)

#### 1.0.5.3 Procedure
1. Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> TS >> Mappings** (or regular TS configuration)
2. Verify that other TS types are currently available for configuration on Blade<1>
3. Document the TS types and mappings visible (e.g., 10 mappings)
4. Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Config**
5. Locate "Enable Gateway VOD" parameter
6. Change setting: **Disable >> Enable**
7. Click **Save** or **Apply**
8. Wait for configuration propagation (< 5 seconds)
9. Navigate back to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> TS >> Mappings** (or regular TS configuration location)
10. Verify behavior: Other TS types configuration should NOT be available (not accessible/not displayed)
11. Confirm that configuration interface shows "GVOD enabled - other TS types not available" or similar message/behavior
12. Attempt to navigate to other TS types configuration location:
    - Path: **APEX3K-NE EM >> Blades >> Select Blade<1> >> TS >> Mappings** (or similar)
    - Should show "Not available" or disabled state, or be completely hidden
    - Configuration access should be restricted
13. Verify Blade<2> is NOT affected:
    - Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<2> >> TS >> Mappings** (or regular TS configuration)
    - Other TS types should STILL BE AVAILABLE and visible on Blade<2>
14. Disable Gateway VOD on Blade<1>:
    - Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Config**
    - Set **Enable Gateway VOD = Disable**
    - Click **Save**
15. Navigate back to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> TS >> Mappings** (or regular TS configuration location)
16. Verify other TS types are NOW AVAILABLE again for configuration
17. Document that disabling Gateway VOD restores other TS types configuration availability


18. Verify **PASS CRITERIA:** Other TS types configuration unavailable when Gateway VOD enabled, Other TS types configuration available when Gateway VOD disabled, Isolation confirmed between blades, Toggle functionality works correctly, No configuration loss when toggling
#### 1.0.5.4 Expected Results
- Other TS types available before Gateway VOD enabled
- After enabling Gateway VOD, other TS types NOT available for configuration on Blade<1>
- Configuration interface properly restricts access to other TS types
- Blade<2> other TS types unaffected by Blade<1> GVOD setting
- Disabling Gateway VOD restores other TS types configuration availability
- Configuration is properly isolated per-blade
- No error messages during toggling
- **Monitoring Points:** Monitor: **Blade<1> >> Config >> Enable Gateway VOD** parameter, Check: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** display after enabling (TS and Mappings table), Verify: **Blade<2> >> TS >> Mappings** (or regular location) remains visible, Document: Visibility state changes during enable/disable cycle

---

## 2.0 REL1.2.15-020: CTE Encryption SCTE-52

### 2.0.1 Test Case: CTE-SCTE-52 Encryption Configuration and Verification
**Test ID:** TC_REL1.2.15-020_001  
**Severity:** HIGH  
#### 2.0.1.2 Objectives
**Objective:** Verify CTE encryption using SCTE-52 algorithm is configured in APEX3K-NE

#### 2.0.1.1 Initial Condition
- APEX3K-NE has CTE module installed
- SCTE-52 support confirmed in system
- MediaCipher SimulCrypt enabled
- MPEG Tracker available for TS analysis

**Test Steps:**
1. Navigate to: **APEX3K-NE EM >> Chassis >> VOD >> CTE configuration**
2. Verify CTE module is present and enabled
3. Verify SCTE-52 algorithm is selected/configured
4. Create test Gateway VOD stream
5. Monitor output TS on MPEG Tracker (minimum 1 minute monitoring)
6. Analyze packets for:
   - Control words present
   - Encryption algorithm metadata (should show SCTE-52)
   - Key structure matches SCTE-52 spec
   - Valid CRC values
7. Verify PAT (Program Association Table) present
8. Verify PMT contains proper CA descriptors

#### 2.0.1.4 Expected Results
- CTE encryption with SCTE-52 active
- Control words correctly inserted
- Encryption algorithm matches specification
- PAT and PMT properly configured
- MPEG Tracker analysis confirms SCTE-52

### 2.0.2 Test Case: SCTE-52 Compliance Across Multiple Streams (APEX3K-NE)
**Test ID:** TC_REL1.2.15-020_002  
**Severity:** HIGH  
#### 2.0.2.2 Objectives
**Objective:** Verify SCTE-52 compliance uniformity across all APEX3K-NE Gateway VOD streams

#### 2.0.2.1 Initial Condition
- CTE encryption configured at **APEX3K-NE EM >> Chassis >> VOD >> CTE configuration**
- 10+ Gateway VOD streams active

**Test Steps:**
1. Start 10 different Gateway VOD streams via M3-Server to Virtual IP
2. For each stream:
   - Monitor output on MPEG Tracker
   - Analyze encryption algorithm
   - Verify key structure matches SCTE-52
   - Check control word insertion pattern
   - Validate CRC checksums
3. Create compliance report documenting results
4. Compare consistency across all 10 streams

#### 2.0.2.4 Expected Results
- All 10 streams use SCTE-52 encryption
- Key structure consistent and valid across all
- Control words properly inserted in all
- 100% SCTE-52 compliance achieved

### 2.0.3 Test Case: CTE-SCTE-52 Uniformity Across System
**Test ID:** TC_REL1.2.15-020_003  
**Severity:** MEDIUM  
#### 2.0.3.2 Objectives
**Objective:** Verify uniform CTE-SCTE-52 encryption across all Gateway VOD streams

#### 2.0.3.1 Initial Condition
- MediaCipher SimulCrypt enabled at: **Simulcrypt >> General = Enable**
- 20+ streams active with various configurations

**Test Steps:**
1. Query APEX3K-NE for all active Gateway VOD streams
2. For each stream, extract encryption metadata via MPEG Tracker
3. Verify all streams use CTE encryption
4. Verify all streams use SCTE-52 algorithm
5. Generate uniformity report

#### 2.0.3.4 Expected Results
- All 20+ streams use CTE-SCTE-52
- 100% consistency achieved
- Zero deviations from standard

**Requirement:** For each Gateway VOD transport stream using MediaCipher SimulCrypt, the NE shall insert ECMs for MediaCipher and all globally configured external SuperCAS systems and shall update the associated PMT accordingly. The NE shall support one internal MediaCipher CAS and up to three external SuperCAS systems.

**APEX3K-NE Configuration:**
- **MediaCipher:** 1 internal CAS (when **Simulcrypt >> General = Enable**)
- **External SuperCAS:** Up to 3 via **Simulcrypt >> CAS configuration** (Maximum 3 external)
- **ECMG Server:** Configure at **Simulcrypt >> HOST configuration** (ECMG server IP)
- **CAS-ECMG Assignment:** **Simulcrypt >> Add the ECMG and assign to the CAS**

---


---

## 3.0 REL1.2.15-030: ECM Insertion & PMT

### 3.0.1 Test Case: ECM Insertion for Internal MediaCipher CAS (APEX3K-NE)
**Test ID:** TC_REL1.2.15-030_001  
**Severity:** CRITICAL  
#### 3.0.1.2 Objectives
**Objective:** Verify ECM insertion for MediaCipher CAS on APEX3K-NE

#### 3.0.1.1 Initial Condition
- MediaCipher SimulCrypt enabled: **Simulcrypt >> General = Enable**
- Gateway VOD configured: **Blade >> Select Blade<1> >> Config >> Enable Gateway VOD**
- Single VOD stream active
- ECMG server configured: **Simulcrypt >> HOST configuration**
- MPEG Tracker monitoring output

**Test Steps:**
1. Verify ECMG server running and accessible
2. Start VOD stream input via M3-Server to Virtual IP
3. Monitor stream in: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** (TS and Mappings table - should appear)
4. Monitor transport stream output on MPEG Tracker (minimum 100 packets)
5. Analyze captured packets:
   - Search for ECM (0x80) tables
   - Identify ECM PID assigned
   - Verify MediaCipher system ID in ECM
   - Verify ECM insertion frequency (typical: 120ms intervals, approximately 8 ECM packets per second)
   - Validate ECM structure per DVB-CSA2
6. Verify ECM credentials present
7. Monitor frequency consistency

#### 3.0.1.4 Expected Results
- ECM tables detected in transport stream
- ECM PID correctly identified
- ECM frequency within spec (120ms intervals, ~8 packets/second)
- ECM syntax valid per DVB-CSA2
- MediaCipher credentials in ECM
- MPEG Tracker confirms ECM presence
- **Monitoring Points:** MPEG Tracker: Verify ECM packets and PID, APEX-NE EM: Monitor ECMG connectivity at **Simulcrypt >> HOST configuration**, Check ECM error rate (target: < 0.01%)

---

### 3.0.2 Test Case: Multiple Streams - Individual ECMs per Stream
**Test ID:** TC_REL1.2.15-030_002
**Severity:** HIGH
#### 3.0.2.2 Objectives
**Objective:** Verify that 5-10 simultaneous Gateway VOD streams receive individual ECMs with correct MediaCipher ID

#### 3.0.2.1 Initial Condition
- MediaCipher SimulCrypt enabled: **Simulcrypt >> General = Enable**
- Gateway VOD configured and ENABLED: **Blade >> Select Blade<1> >> Config >> Enable Gateway VOD = ON**
  - Note: When GVOD is enabled on this blade, other TS types (DVB-C, DVB-S, etc.) are NOT available for configuration on this blade
- ECMG server configured: **Simulcrypt >> HOST configuration**
- M3-Server capable of sending 5-10 simultaneous unicast streams
- MPEG Tracker connected and operational

#### 3.0.2.3 Procedure
1. Navigate to: **APEX3K-NE EM >> Simulcrypt >> General** and confirm MediaCipher SimulCrypt = **Enable**
2. Navigate to: **APEX3K-NE EM >> Simulcrypt >> HOST configuration** and verify ECMG server is configured and online
3. Launch M3-Server and configure 5-10 different unicast streams with unique program numbers (e.g., PN 1000-1009)
4. Send all streams simultaneously to the Virtual IP (ingress) configured in Gateway VOD
5. Wait 5-10 seconds for streams to ingress into APEX3K-NE
6. Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** and verify all 5-10 streams appear in TS and Mappings table with status **Active**
7. Connect MPEG Tracker to the output of APEX3K-NE RF card
8. For each stream, capture 500+ TS packets and analyze:
   - Filter for ECM tables (table ID 0x80)
   - Identify unique ECM PIDs for each stream
   - Extract MediaCipher system ID from each ECM
9. Document all 5-10 ECM PIDs and their associated streams
10. Verify each stream has received at least 2-3 ECM packets
11. Verify ECM frequency consistent (120ms intervals, approximately 8 ECM packets per second per DVB spec)
12. Export MPEG Tracker analysis and save results


13. Verify **PASS CRITERIA:** 100% of 5-10 streams have ECMs inserted, Each stream ECM PID is unique, MediaCipher system ID present and correct in all ECMs, ECM frequency consistent (120ms intervals, ~8 packets/second) across all streams
#### 3.0.2.4 Expected Results
- All 5-10 streams appear in APEX3K-NE Gateway VOD Status as Active
- Each stream generates unique ECM packets with distinct PID
- Each ECM contains correct MediaCipher CAS system ID
- ECM packets detected for all 5-10 streams in MPEG Tracker output
- ECM insertion frequency within specification (120ms intervals, ~8 packets/second)
- No ECM collisions or duplicate PIDs across streams

### 3.0.3 Test Case: PMT Update - ECM Descriptor Addition
**Test ID:** TC_REL1.2.15-030_003
**Severity:** HIGH
#### 3.0.3.2 Objectives
**Objective:** Verify PMT is updated with ECM descriptor when encryption is enabled, and PMT version increments

#### 3.0.3.1 Initial Condition
- Gateway VOD configured and ENABLED
  - Note: When GVOD is enabled on this blade, other TS types (DVB-C, DVB-S, etc.) are NOT available for configuration on this blade
- Single VOD stream ready to start
- MPEG Tracker connected
- Initial PMT version documented (before starting encrypted stream)

#### 3.0.3.3 Procedure
1. Start unencrypted VOD stream input via M3-Server to Virtual IP
2. Wait 2-3 seconds and connect MPEG Tracker to APEX3K-NE output
3. Capture 200 TS packets and locate PMT (table ID 0x02)
4. Document initial PMT:
   - PMT version number (typically 0)
   - Program number
   - PCR PID
   - ES (Elementary Stream) PIDs
   - Current descriptors present
5. Stop stream on M3-Server (keep APEX3K-NE running)
6. Navigate to: **APEX3K-NE EM >> Simulcrypt >> General** and verify MediaCipher SimulCrypt = **Enable**
7. Restart same VOD stream on M3-Server with encryption enabled
8. Wait 3-5 seconds for re-ingestion
9. Monitor 200 new TS packets from output on MPEG Tracker
10. Locate new PMT (should appear quickly after stream restart)
11. Document new PMT:
    - New PMT version number (should be 1 or higher)
    - Compare version to initial PMT
    - Identify new/added descriptors
    - Search for CA descriptor (tag 0x09) with MediaCipher CAS system ID
    - Note ECM PID reference in descriptor
12. Verify descriptor structure:
    - Descriptor tag = 0x09 (CA descriptor)
    - CAS system ID = MediaCipher ID (typically 0x4AD0 or configured value)
    - ECM PID field contains valid PID
13. Compare PMT content (exclude version field):
    - Verify ES information unchanged (except descriptor addition)
    - Confirm PCR PID unchanged
    - Verify only descriptors added, no removal of existing elements


14. Verify **PASS CRITERIA:** PMT version incremented from baseline, CA descriptor with MediaCipher system ID present in PMT, ECM PID valid and referenced correctly, PMT structure valid per DVB-SI specification
#### 3.0.3.4 Expected Results
- PMT version incremented (increased by at least 1)
- New CA descriptor added to PMT with MediaCipher system ID
- ECM PID correctly referenced in CA descriptor
- PMT syntax valid per DVB standard
- All ES information preserved
- MPEG Tracker confirms PMT descriptor presence

### 3.0.4 Test Case: External SuperCAS 1 - ECM Insertion
**Test ID:** TC_REL1.2.15-030_004
**Severity:** HIGH
#### 3.0.4.2 Objectives
**Objective:** Verify ECM insertion for 1st external SuperCAS when configured at Simulcrypt >> CAS configuration

#### 3.0.4.1 Initial Condition
- MediaCipher SimulCrypt enabled
- Gateway VOD configured and ENABLED on Blade<1>
  - Note: When GVOD is enabled on this blade, other TS types (DVB-C, DVB-S, etc.) are NOT available for configuration on this blade
- No external SuperCAS configured yet (only internal MediaCipher)
- ECMG server capable of handling external CAS (SuperCAS)
- M3-Server ready with test stream

#### 3.0.4.3 Procedure
1. Verify current configuration:
   - Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
   - Document current CAS list (should show only Internal MediaCipher initially)
2. Click **Add** or **Configure CAS** button
3. Select or enter 1st external SuperCAS details:
   - CAS Type: **External SuperCAS**
   - CAS System ID: **0x4B46** (Nagravision) or configured SuperCAS ID
   - ECMG IP/Port: Configure external ECMG server details
4. Assign ECMG to this CAS (if separate assignment required)
5. Click **Save** or **Apply**
6. Wait for confirmation message (target: < 3 seconds)
7. Verify configuration persists: Navigate back to **CAS configuration** and confirm 1st SuperCAS listed
8. Start VOD stream on M3-Server (stream should now be encrypted for both MediaCipher and SuperCAS1)
9. Monitor: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** for stream appearing
10. Connect MPEG Tracker to output and capture 500+ TS packets
11. Analyze captured packets:
    - Search for ECM tables (0x80)
    - Identify all ECM PIDs present
    - Should have minimum 2 ECM PIDs: one for MediaCipher, one for SuperCAS1
12. For SuperCAS1 ECM, verify:
    - CAS system ID = 0x4B46 (or configured SuperCAS ID)
    - ECM data structure valid per SuperCAS specification
    - ECM frequency within spec (120ms intervals, ~8 packets/second)
13. Extract and document both ECM streams:
    - ECM PID 1: MediaCipher (system ID 0x4AD0)
    - ECM PID 2: SuperCAS1 (system ID 0x4B46)


14. Verify **PASS CRITERIA:** CAS configuration accepts 1st external SuperCAS without error, ECMs generated for both internal and 1st external CAS, SuperCAS1 ECM PID unique and distinct from MediaCipher, Stream continues without interruption
#### 3.0.4.4 Expected Results
- 1st external SuperCAS successfully added to CAS configuration
- VOD stream now receives ECMs for both MediaCipher and SuperCAS1
- Two distinct ECM PIDs present in transport stream
- SuperCAS1 CAS system ID correctly present in its ECM
- Both ECM streams have valid structure and frequency

### 3.0.5 Test Case: External SuperCAS 2 - ECM Insertion
**Test ID:** TC_REL1.2.15-030_005
**Severity:** HIGH
#### 3.0.5.2 Objectives
**Objective:** Verify 2nd external SuperCAS ECM insertion and verify both SuperCAS1 and SuperCAS2 ECMs present

#### 3.0.5.1 Initial Condition
- Test Case 3.0.4 passed (1st SuperCAS operational)
- Gateway VOD configured and ENABLED on Blade<1>
  - Note: When GVOD is enabled on this blade, other TS types are NOT available for configuration
- 1st external SuperCAS (SuperCAS1) configured and verified
- 2nd external SuperCAS available (different CAS system ID)
- VOD stream still active with SuperCAS1 ECMs

#### 3.0.5.3 Procedure
1. With stream still active (from 3.4), navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
2. Verify SuperCAS1 currently listed with its CAS system ID
3. Click **Add** or **Configure CAS** button
4. Configure 2nd external SuperCAS:
   - CAS Type: **External SuperCAS**
   - CAS System ID: **0x4BB8** (Kudelski) or alternate SuperCAS ID
   - ECMG IP/Port: Configure external ECMG server for SuperCAS2
5. Assign ECMG to SuperCAS2
6. Click **Save** or **Apply**
7. Wait 3-5 seconds for configuration update
8. Navigate back to verify both SuperCAS1 and SuperCAS2 listed in **CAS configuration**
9. Monitor stream in: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** - should show as Active and updated
10. Stop and restart VOD stream on M3-Server (or allow current stream to continue if automatic re-encryption applied)
11. Connect MPEG Tracker to output and capture 500+ TS packets
12. Search for ECM tables and identify all ECM PIDs:
    - Should have minimum 3 ECM PIDs: MediaCipher + SuperCAS1 + SuperCAS2
13. For each ECM, verify CAS system ID:
    - ECM 1: MediaCipher (0x4AD0)
    - ECM 2: SuperCAS1 (0x4B46)
    - ECM 3: SuperCAS2 (0x4BB8)
14. Document all 3 ECM PIDs and verify each has continuous insertion (120ms frequency, ~8 packets/second)
15. Extract 50 packets of each ECM type and verify structure validity


16. Verify **PASS CRITERIA:** CAS configuration accepts 2nd external SuperCAS, Total of 3 ECMs present (1 internal + 2 external), All three ECM PIDs unique and distinct, Each ECM correctly identifies its CAS system, Stream stability maintained throughout configuration change
#### 3.0.5.4 Expected Results
- 2nd external SuperCAS successfully added to configuration
- Stream now receives ECMs for MediaCipher, SuperCAS1, and SuperCAS2
- Three distinct ECM PIDs present in transport stream
- Each ECM contains correct CAS system ID
- All ECM streams have valid structure and consistent frequency
- Original SuperCAS1 ECM continues unaffected

### 3.0.6 Test Case: External SuperCAS 3 - Maximum Config (4 Total CAS)
**Test ID:** TC_REL1.2.15-030_006
**Severity:** HIGH
#### 3.0.6.2 Objectives
**Objective:** Configure 3rd external SuperCAS to reach maximum system configuration (1 Internal MediaCipher + 3 External SuperCAS = 4 total CAS) and verify all 4 CAS ECMs inserted

#### 3.0.6.1 Initial Condition
- Test Case 3.0.5 passed (SuperCAS1 and SuperCAS2 operational)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- 1st and 2nd external SuperCAS configured with working ECMs
- VOD stream active with 3 ECMs (MediaCipher + SuperCAS1 + SuperCAS2)
- 3rd external SuperCAS available

#### 3.0.6.3 Procedure
1. With stream still active, navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
2. Verify MediaCipher, SuperCAS1, and SuperCAS2 currently listed
3. Click **Add** or **Configure CAS** button to add 3rd SuperCAS
4. Configure 3rd external SuperCAS:
   - CAS Type: **External SuperCAS**
   - CAS System ID: **0x5601** (Conax) or alternate SuperCAS ID
   - ECMG IP/Port: Configure external ECMG server for SuperCAS3
5. Assign ECMG to SuperCAS3
6. Click **Save** or **Apply**
7. Wait 5 seconds for configuration update and ECM re-generation
8. Navigate back to **CAS configuration** and verify all 4 CAS listed:
   - Internal MediaCipher
   - External SuperCAS1 (0x4B46)
   - External SuperCAS2 (0x4BB8)
   - External SuperCAS3 (0x5601)
9. Monitor: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** - stream status should remain Active
10. Connect MPEG Tracker and capture 500+ TS packets
11. Search for all ECM tables:
    - Should identify 4 distinct ECM PIDs total
12. For each ECM, extract and verify:
    - ECM 1: MediaCipher (0x4AD0)
    - ECM 2: SuperCAS1 (0x4B46)
    - ECM 3: SuperCAS2 (0x4BB8)
    - ECM 4: SuperCAS3 (0x5601)
13. Verify each ECM:
    - Correct CAS system ID
    - Valid structure per DVB specification
    - Consistent insertion frequency (120ms intervals, ~8 ECM packets/second)
    - PID unique and distinct from others
14. Monitor PMT for CA descriptors:
    - Should have 4 CA descriptors total
    - Each descriptor references correct CAS system ID and ECM PID
15. Calculate total ECM bandwidth:
    - Measure total ECM packets per second (target: ~8 packets/second per ECM)
    - Document bandwidth impact on stream


16. Verify **PASS CRITERIA:** CAS configuration successfully accepts 3rd external SuperCAS, Total of 4 ECM PIDs present and verified, All ECM PIDs unique and consistent, All CAS system IDs correct and verified, PMT properly updated with all 4 CA descriptors, Stream remains stable throughout
#### 3.0.6.4 Expected Results
- 3rd external SuperCAS successfully configured
- Maximum configuration reached (4 total CAS systems)
- All 4 CAS ECMs present in transport stream
- Each ECM correctly identified with its CAS system ID
- PMT contains 4 CA descriptors with correct CAS IDs and ECM PIDs
- Stream bandwidth accommodates all 4 ECM streams
- No stream discontinuities or errors

### 3.0.7 Test Case: Reject 4th External SuperCAS (System Limit)
**Test ID:** TC_REL1.2.15-030_007
**Severity:** HIGH
#### 3.0.7.2 Objectives
**Objective:** Verify system enforces maximum limit of 3 external SuperCAS through UI constraint (total max: 1 internal + 3 external = 4)

#### 3.0.7.1 Initial Condition
- Test Case 3.0.6 passed (4 CAS systems operational)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- Maximum configuration reached (1 Internal + 3 External)
- 4 ECMs actively inserted for all CAS
- APEX-NE EM interface accessible

#### 3.0.7.3 Procedure
1. Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
2. Verify all 4 CAS listed (MediaCipher + 3 external SuperCAS):
   - 1 Internal MediaCipher (0x4AD0)
   - 3 External SuperCAS rows filled
3. Observe CAS configuration table structure:
   - Verify CAS table has exactly 3 rows for external SuperCAS configuration
   - Note that 4th row is NOT available (UI enforces max 3 external CAS)
4. Verify stream still active: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** shows stream as Active
5. Verify MPEG Tracker showing all 4 ECM streams active
6. Attempt to add 4th external SuperCAS:
   - Look for **Add** or **Configure CAS** button
   - If button is disabled/grayed out: Document that button is disabled when max reached
   - If no 4th row available: Confirm only 3 rows exist in CAS table
   - Attempt to click any non-existent add function: Should not be possible
7. Verify UI prevents 4th CAS addition through one of these mechanisms:
   - Add button disabled when max CAS reached
   - No 4th row available in CAS configuration table
   - Gray-out/disabled state for exceeding limits
8. Verify error handling (if user attempts workaround):
   - If any error dialog appears: Document message
   - Expected: System prevents addition without allowing user to attempt entry
9. Navigate back to **CAS configuration** and verify still shows only 4 CAS (1 internal + 3 external)
10. Verify stream still active: **Gateway VOD Status** should show stream as Active
11. Connect MPEG Tracker and verify:
    - Still detecting 4 ECM streams (no new 4th ECM attempted to be added)
    - Original 4 ECMs still present and valid
    - No interruption or stream discontinuity
12. Document UI behavior preventing 4th CAS configuration


13. Verify **PASS CRITERIA:** UI enforces maximum limit by preventing 4th external SuperCAS configuration, Add button disabled or no 4th row available when limit reached, CAS configuration remains at 4 systems (max), Stream stability maintained without any error attempts, No ECM insertion failures or stream discontinuities
#### 3.0.7.4 Expected Results
- UI properly enforces maximum CAS limit (3 external SuperCAS)
- System prevents 4th external CAS addition at UI level
- Add button disabled or no 4th configuration row visible when max reached
- Configuration remains at 4 CAS systems (1 internal + 3 external)
- Stream continues uninterrupted
- Original 4 ECM streams remain active and valid
- No system errors or warnings when attempting to exceed limit

### 3.0.8 Test Case: ECM Insertion After CAS Configuration Change
**Test ID:** TC_REL1.2.15-030_008
**Severity:** HIGH
#### 3.0.8.2 Objectives
**Objective:** Verify ECMs updated to include new CAS when 3rd SuperCAS added while stream active

#### 3.0.8.1 Initial Condition
- Test Case 3.0.5 passed (SuperCAS1 and SuperCAS2 active with 3 ECMs)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active and transmitting with 3 ECMs
- 3 ECM PIDs documented from Test Case 3.0.5
- 3rd SuperCAS available but not yet configured

#### 3.0.8.3 Procedure
1. Verify current state:
   - Stream active: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** shows stream as Active
   - MPEG Tracker monitoring output with 3 ECMs present (MediaCipher + SuperCAS1 + SuperCAS2)
   - Document baseline 3 ECM PIDs
2. Monitor continuous MPEG Tracker output (do not stop monitoring):
   - Continue monitoring TS packets from output
   - Note timestamp when starting monitoring
3. Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
4. While stream is still active and flowing, add 3rd SuperCAS:
   - Click **Add** or **Configure CAS**
   - Enter 3rd SuperCAS details (0x5601 or configured ID)
   - Click **Save** or **Apply**
5. Note timestamp when configuration saved
6. Wait 2-5 seconds for APEX3K-NE to process configuration change
7. Observe stream status: **Gateway VOD Status** should show stream as Active (no interruption)
8. Continue MPEG Tracker capture for another 10 seconds
9. Stop MPEG Tracker capture
10. Analyze captured packets:
    - Identify point where configuration change occurred (based on timestamp)
    - Look for ECM changes after timestamp
    - Identify when 4th ECM (SuperCAS3) first appears
11. Search for new/additional ECM PID:
    - Should identify new ECM PID appearing after configuration change
    - New ECM should have CAS system ID 0x5601 (SuperCAS3)
12. Verify ECM insertion timeline:
    - ECMs 1-3 (MediaCipher + SuperCAS1 + SuperCAS2) appear throughout capture
    - New ECM 4 (SuperCAS3) appears within 2-5 seconds after configuration change
    - All 4 ECMs continue after insertion of 3rd ECM
13. Verify stream continuity:
    - No gaps in TS packet sequence
    - No CRC errors or discontinuities
    - PCR (Program Clock Reference) remains continuous
14. Compare PMT before/after:
    - Capture PMT packets before and after configuration change
    - Verify PMT version incremented
    - Verify 4th CA descriptor added for SuperCAS3


15. Verify **PASS CRITERIA:** CAS configuration updated successfully, New ECM appears in transport stream within 5 seconds, All ECM PIDs unique and distinct, Stream continues without interruption, PMT properly updated, No packet loss or stream corruption
#### 3.0.8.4 Expected Results
- Configuration change accepted without stream interruption
- 4th ECM (SuperCAS3) begins appearing within 2-5 seconds of configuration change
- All 4 ECMs present simultaneously after 3rd SuperCAS insertion
- Stream packet continuity maintained (no gaps or discontinuities)
- PMT updated with 4th CA descriptor
- No ECM insertion failures or errors

### 3.0.9 Test Case: ECM Insertion After CAS Configuration Removal
**Test ID:** TC_REL1.2.15-030_009
**Severity:** HIGH
#### 3.0.9.2 Objectives
**Objective:** Verify ECMs updated when external CAS removed from configuration while stream active

#### 3.0.9.1 Initial Condition
- Test Case 3.0.6 passed (all 4 CAS systems operational with 4 ECMs)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active with all 4 ECMs flowing continuously
- All 4 ECM PIDs documented
- All 4 CAS listed in configuration

#### 3.0.9.3 Procedure
1. Verify current state:
   - Stream active: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** shows stream Active
   - MPEG Tracker capturing with all 4 ECMs present
   - Document baseline 4 ECM PIDs and CAS system IDs
2. Start continuous MPEG Tracker capture:
   - Begin recording TS packets
   - Note timestamp
3. Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
4. Identify which SuperCAS to remove:
   - Example: Remove SuperCAS2 (0x4BB8) - middle one
5. Select SuperCAS2 from the configuration list
6. Click **Delete** or **Remove** button
7. Confirm deletion when prompted
8. Note timestamp when deletion confirmed
9. Click **Save** or **Apply** to persist change
10. Wait 2-5 seconds for APEX3K-NE to process removal
11. Verify stream status: **Gateway VOD Status** should still show stream as Active
12. Continue MPEG Tracker capture for another 10 seconds after removal
13. Stop MPEG Tracker capture
14. Analyze captured packets:
    - Identify when SuperCAS2 ECM stops appearing (after configuration removal)
    - Should see ECMs 1, 2, 4 (MediaCipher, SuperCAS1, SuperCAS3) continuing
    - Should NOT see ECM 3 (SuperCAS2) in post-removal packets
15. Verify timing:
    - SuperCAS2 ECM should disappear within 2-5 seconds of configuration removal
    - Remaining 3 ECMs continue with consistent frequency
16. Verify stream continuity:
    - No gaps or discontinuities around ECM removal point
    - PCR remains continuous
    - No CRC errors or stream artifacts
17. Capture PMT after removal:
    - Should have 3 CA descriptors (down from 4)
    - SuperCAS2 descriptor should be removed
    - MediaCipher, SuperCAS1, and SuperCAS3 descriptors remain


18. Verify **PASS CRITERIA:** CAS successfully removed from configuration, Removed CAS ECM stops appearing in stream, Removal occurs within acceptable timeframe (2-5 seconds), Stream continuity preserved, Remaining ECMs unaffected, PMT descriptor count decremented correctly
#### 3.0.9.4 Expected Results
- CAS removal accepted without stream interruption
- Removed CAS ECM disappears within 2-5 seconds of configuration change
- Remaining 3 ECMs continue appearing normally
- Stream packet continuity maintained (no gaps)
- PMT updated with removal of corresponding CA descriptor
- ECM insertion continues for remaining 3 CAS systems

### 3.0.10 Test Case: PMT Descriptor for All CAS Systems
**Test ID:** TC_REL1.2.15-030_010
**Severity:** HIGH
#### 3.0.10.2 Objectives
**Objective:** Verify PMT contains CA descriptors for all 4 CAS systems with correct CAS system IDs and ECM PID references

#### 3.0.10.1 Initial Condition
- Test Case 3.0.6 passed (all 4 CAS configured)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active with all 4 CAS systems
- All 4 ECM PIDs identified and documented
- MPEG Tracker connected

#### 3.0.10.3 Procedure
1. Verify configuration:
   - Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
   - Confirm all 4 CAS listed:
     - MediaCipher (Internal)
     - SuperCAS1 (0x4B46)
     - SuperCAS2 (0x4BB8)
     - SuperCAS3 (0x5601)
2. Verify stream active: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** shows stream Active
3. Connect MPEG Tracker to output and begin capture
4. Capture 300-500 TS packets
5. Locate PMT table (table ID 0x02) from captured packets
6. Extract PMT and analyze:
   - Program number: [documented value]
   - PMT version: [value]
   - PCR PID: [value]
7. Scan PMT descriptors for CA descriptors (descriptor tag 0x09):
   - Should find 4 CA descriptors total (one for each CAS)
8. For each CA descriptor, extract and verify:
   - **CA Descriptor 1 (MediaCipher):**
     - Descriptor tag: 0x09 (CA)
     - CAS system ID: 0x4AD0
     - ECM PID: [value] (should match known MediaCipher ECM PID)
     - CA data: [present and valid]
   - **CA Descriptor 2 (SuperCAS1):**
     - Descriptor tag: 0x09 (CA)
     - CAS system ID: 0x4B46
     - ECM PID: [value] (should match SuperCAS1 ECM PID)
     - CA data: [present and valid]
   - **CA Descriptor 3 (SuperCAS2):**
     - Descriptor tag: 0x09 (CA)
     - CAS system ID: 0x4BB8
     - ECM PID: [value] (should match SuperCAS2 ECM PID)
     - CA data: [present and valid]
   - **CA Descriptor 4 (SuperCAS3):**
     - Descriptor tag: 0x09 (CA)
     - CAS system ID: 0x5601
     - ECM PID: [value] (should match SuperCAS3 ECM PID)
     - CA data: [present and valid]
9. Verify descriptor ordering:
   - Note order of CA descriptors in PMT
   - Verify consistency across multiple PMT instances
10. Verify ECM PID mapping:
    - Cross-reference each CA descriptor ECM PID with captured ECM streams
    - Confirm each referenced PID has active ECM packets
11. Verify CA data content:
    - Extract CA data fields
    - Verify they match expected format for each CAS system
12. Check for any missing or malformed descriptors
13. Capture and compare 3 different PMT instances to verify consistency
14. Document PMT descriptor table with all 4 descriptors


15. Verify **PASS CRITERIA:** All 4 CA descriptors present in PMT, Each descriptor has correct CAS system ID, ECM PID references match actual ECM streams, Descriptor structure valid per DVB specification, Descriptor content consistent across PMT instances
#### 3.0.10.4 Expected Results
- PMT contains exactly 4 CA descriptors
- Each descriptor correctly identifies its CAS system ID
- Each descriptor ECM PID matches actual ECM stream PID
- All descriptors have valid structure per DVB-SI
- Descriptor ordering consistent across multiple PMTs
- All CA data fields present and properly formatted
- No missing or corrupted descriptors

### 3.0.11 Test Case: PMT Version Increment on CAS Change
**Test ID:** TC_REL1.2.15-030_011
**Severity:** MEDIUM
#### 3.0.11.2 Objectives
**Objective:** Verify PMT version increments correctly when CAS configuration changes

#### 3.0.11.1 Initial Condition
- Test Case 3.0.6 passed (4 CAS systems operational)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active with known PMT version
- MPEG Tracker connected
- Baseline PMT version documented

#### 3.0.11.3 Procedure
1. Monitor current PMT from stream via MPEG Tracker
2. Extract and document:
   - Current PMT version (example: version 3)
   - All 4 CA descriptors with CAS system IDs
   - Timestamp of PMT monitoring
3. Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
4. Make configuration change (e.g., remove SuperCAS2)
5. Click **Save** or **Apply**
6. Note timestamp of configuration change
7. Wait 3-5 seconds for APEX3K-NE to process
8. Verify stream still active
9. Monitor new PMT from stream via MPEG Tracker (after configuration change)
10. Extract and document:
    - New PMT version (should be 4 or higher)
    - CA descriptors now present (3 instead of 4)
    - Timestamp of new PMT
11. Compare versions:
    - Verify new version > previous version
    - Verify version incremented by at least 1
12. Add 3rd SuperCAS back (or add different SuperCAS to reconfigure)
13. Click **Save** or **Apply**
14. Wait 3-5 seconds
15. Capture another new PMT
16. Verify PMT version incremented again (e.g., from 4 to 5)
17. Repeat configuration change 2-3 more times, documenting version increment each time


18. Verify **PASS CRITERIA:** PMT version increments on each configuration change, Version numbering correct per DVB specification, Descriptor updates synchronized with version changes
#### 3.0.11.4 Expected Results
- PMT version increments with each configuration change
- Version numbers sequential and correct
- Descriptor count matches CAS configuration count
- PMT version changes occur within 2-5 seconds of configuration update

### 3.0.12 Test Case: ECM Bandwidth Impact with All CAS
**Test ID:** TC_REL1.2.15-030_012
**Severity:** MEDIUM
#### 3.0.12.2 Objectives
**Objective:** Measure and verify ECM bandwidth usage with all 4 CAS systems active

#### 3.0.12.1 Initial Condition
- Test Case 3.0.6 passed (all 4 CAS operational)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active with all 4 ECMs
- MPEG Tracker connected
- All 4 ECM PIDs identified

#### 3.0.12.3 Procedure
1. Verify configuration: **APEX3K-NE EM >> Simulcrypt >> CAS configuration** shows 4 CAS systems
2. Connect MPEG Tracker to output
3. Capture 1000-2000 TS packets (continuous stream, approximately 10-20 seconds)
4. Analyze captured packets:
   - Count total TS packets: [value]
   - Count ECM packets for each PID:
     - MediaCipher ECM count: [value]
     - SuperCAS1 ECM count: [value]
     - SuperCAS2 ECM count: [value]
     - SuperCAS3 ECM count: [value]
   - Total ECM packets: [value]
5. Calculate ECM bandwidth:
   - Total TS bitrate (example: 3.75 Mbps for DVB)
   - ECM packet ratio = ECM packets / Total packets
   - ECM bandwidth = Total bitrate × ECM packet ratio
6. Document for each individual ECM:
   - ECM frequency (packets per second): Target ~8 packets/second per ECM, intervals ~120ms
   - Estimated bandwidth per CAS
   - Example: MediaCipher ECM: 10 packets/sec × 184 bytes = 18.4 kbps
7. Calculate total ECM bandwidth:
   - Sum of all 4 ECM bandwidths
   - Express as percentage of total stream bitrate
8. Verify bandwidth acceptable:
   - Compare to typical DVB ECM overhead (2-5% is typical)
   - Verify total ECM bandwidth < [acceptable threshold]
9. Verify ECM frequency consistency:
   - Measure time intervals between consecutive ECMs for each PID
   - Verify frequency within spec (120ms intervals, ~8 packets/second per DVB)
   - Calculate jitter/variance


10. Verify **PASS CRITERIA:** ECM bandwidth < 10% of total stream bitrate, Individual ECM frequencies within 120ms intervals (~8 packets/second) spec, Consistent ECM insertion rates for all 4 CAS systems
#### 3.0.12.4 Expected Results
- Total ECM bandwidth measurable and quantifiable
- ECM bandwidth typically 2-5% of total stream
- All ECM frequencies within specification
- No excessive bandwidth consumption
- Stream bitrate remains stable with 4 ECMs

### 3.0.13 Test Case: ECM Encryption and Validity
**Test ID:** TC_REL1.2.15-030_013
**Severity:** HIGH
#### 3.0.13.2 Objectives
**Objective:** Verify ECM data is properly encrypted and valid per CAS specification

#### 3.0.13.1 Initial Condition
- Test Case 3.0.6 passed
- VOD stream active with all 4 ECMs
- MPEG Tracker capture available with ECM packets
- CAS system specifications available for reference

#### 3.0.13.3 Procedure
1. Monitor ECM packets from stream via MPEG Tracker
2. Extract sample ECM packets (at least 5-10 for each CAS):
   - 5 MediaCipher ECMs
   - 5 SuperCAS1 ECMs
   - 5 SuperCAS2 ECMs
   - 5 SuperCAS3 ECMs
3. Analyze MediaCipher ECMs:
   - Verify table ID = 0x80 (ECM)
   - Verify syntax_indicator = 1
   - Extract ECM header information
   - Verify CAS system ID = 0x4AD0
   - Examine encrypted data section
   - Verify data appears random/encrypted (no obvious patterns)
   - Check CRC-32 field validity (should match calculated CRC)
4. Analyze SuperCAS1 ECMs (0x4B46):
   - Repeat checks from step 3
   - Verify CAS system ID = 0x4B46
   - Compare encryption pattern to MediaCipher (should be different format)
   - Validate CRC-32
5. Analyze SuperCAS2 and SuperCAS3 similarly
6. Verify encryption characteristics:
   - No ECM packets from same CAS have identical payload
   - Encrypted data varies between consecutive ECMs
   - No recognizable plaintext patterns
7. Verify ECM validity period:
   - Extract validity information if present
   - Verify ECMs have reasonable validity windows
8. Compare ECM structures to DVB-CSA2 specification:
   - Verify compliance with specification format
   - Check descriptor structures
   - Validate field sizes and types
9. Test ECM error detection:
   - Intentionally corrupt sample ECM CRC in analysis
   - Verify CRC check would fail


10. Verify **PASS CRITERIA:** ECM data encrypted and unreadable, CRC-32 checksums valid for all samples, Encryption proper and specification-compliant, No data integrity issues detected
#### 3.0.13.4 Expected Results
- All ECM data properly encrypted with no readable plaintext
- Encryption varies between ECM instances
- CRC validation passes for all captured ECMs
- ECM structures match CAS specifications
- No unencrypted sensitive data visible
- ECM validity periods reasonable

### 3.0.14 Test Case: ECM Insertion Frequency for Each CAS
**Test ID:** TC_REL1.2.15-030_014
**Severity:** MEDIUM
#### 3.0.14.2 Objectives
**Objective:** Verify ECM insertion frequency meets specification (120ms intervals, approximately 8 ECM packets per second) for all CAS systems

#### 3.0.14.1 Initial Condition
- Test Case 3.0.6 passed
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active with all 4 ECMs
- MPEG Tracker capturing with sufficient resolution
- All 4 ECM PIDs identified

#### 3.0.14.3 Procedure
1. Monitor 2000+ TS packets (20-30 seconds continuous) via MPEG Tracker
2. Identify all ECM packets for each CAS in monitored stream:
   - Extract MediaCipher ECM packets (ECM PID 1)
   - Extract SuperCAS1 ECM packets (ECM PID 2)
   - Extract SuperCAS2 ECM packets (ECM PID 3)
   - Extract SuperCAS3 ECM packets (ECM PID 4)
3. For MediaCipher ECMs, measure time intervals:
   - Calculate time between ECM N and ECM N+1
   - Example: if ECM 1 at packet 100, ECM 2 at packet 225, interval = 125 packets ≈ 125ms (assuming ~1000 packets/sec)
   - Calculate intervals for all consecutive MediaCipher ECM pairs
   - Determine min, max, average, and standard deviation of intervals
4. Repeat for SuperCAS1, SuperCAS2, and SuperCAS3 ECM intervals
5. Verify each CAS meets specification:
   - Minimum interval: > 100ms (minimum frequency)
   - Maximum interval: < 200ms (maximum frequency)
   - Average interval should be consistent
6. Analyze frequency distribution:
   - Plot or tabulate interval values
   - Verify no anomalies or irregular patterns
   - Verify consistency throughout capture
7. Check for synchronization:
   - Verify ECM insertion patterns for different CAS are independent
   - Confirm no unexpected synchronization between different CAS ECMs
8. Measure jitter (variance):
   - Calculate standard deviation of intervals
   - Verify jitter acceptable (target: < 10% of mean interval)


9. Verify **PASS CRITERIA:** 100% of ECM intervals within 120ms specification (~8 packets/second), Average frequency consistent for each CAS, Jitter acceptable (< 10% variance), No anomalous gaps or insertions
#### 3.0.14.4 Expected Results
- All ECM insertion intervals between 120ms per specification (~8 packets/second)
- Consistent frequency for each CAS system
- Low jitter/variance (< 10% of mean)
- No irregular gaps or burst patterns
- Each CAS maintains independent insertion schedule

### 3.0.15 Test Case: ECM Splicing and Continuity
**Test ID:** TC_REL1.2.15-030_015
**Severity:** HIGH
#### 3.0.15.2 Objectives
**Objective:** Verify ECM continuity across stream samples with no gaps or duplicates

#### 3.0.15.1 Initial Condition
- Test Case 3.0.6 passed
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active with all 4 ECMs
- MPEG Tracker capturing full stream
- All 4 ECM PIDs identified

#### 3.0.15.3 Procedure
1. Monitor 3000+ TS packets (30+ seconds) via MPEG Tracker
2. Extract all ECM packets (all 4 ECMs combined) in chronological order
3. For each ECM PID, verify continuity:
   - Extract ECM counter or sequence indicator if present in ECM data
   - Verify counter increments sequentially for each CAS
   - Check for gaps in sequence
4. Verify no duplicate ECMs:
   - Compare consecutive ECMs from same PID
   - Verify each ECM unique (not duplicated)
   - Verify payload differs between consecutive ECMs
5. Verify no missing ECMs:
   - Measure time gaps between consecutive ECMs of same PID
   - Gaps should never exceed 250ms (approximately 2x the normal 120ms interval)
   - Document any gaps approaching 150ms or larger
6. Verify splicing points (if stream spliced/edited):
   - If captured across multiple splice events, verify ECM continuity maintained
   - Verify no loss of ECM at splice boundaries
7. Check for ECM ordering:
   - Verify TS packet sequence numbers continuous and sequential
   - No skipped or out-of-order packets
   - PCR (Program Clock Reference) continuous
8. Analyze across multiple capture sessions:
   - Capture stream in 3 separate sessions (30 seconds each)
   - Verify continuity consistent across all sessions
9. Simulate real-world stream conditions:
   - If possible, capture during network jitter or load changes
   - Verify ECM continuity maintained under stress


10. Verify **PASS CRITERIA:** No ECM gaps > 250ms detected, Zero duplicate ECMs, 100% sequence continuity for all 4 ECM streams, No packet loss or reordering
#### 3.0.15.4 Expected Results
- No gaps in ECM insertion (except normal max intervals)
- No duplicate ECM packets detected
- ECM sequence continuous and sequential
- TS packet sequence unbroken
- PCR continuous and monotonically increasing
- Stream remains synchronous and valid

### 3.0.16 Test Case: ECM PIDs Allocation and Management (1,300+ mappings)
**Test ID:** TC_REL1.2.15-030_016
**Severity:** HIGH
#### 3.0.16.2 Objectives
**Objective:** Create 1,300 simultaneous streams and verify each receives unique ECM PID(s) with no collisions

#### 3.0.16.1 Initial Condition
- Single blade or isolated test blade (APEX3K-NE EM >> Blades >> Select Blade<1>)
- Gateway VOD enabled on blade
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- M3-Server capable of generating 1,300 simultaneous unicast streams
- Sufficient system resources (CPU, memory, bandwidth)
- MPEG Tracker connected to output
- Configuration with 4 CAS systems (maximum)

#### 3.0.16.3 Procedure
1. Verify configuration:
   - Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Config**
   - Confirm Gateway VOD = **Enable**
   - Confirm Virtual IP (Ingress) configured (e.g., 192.168.1.100)
   - Confirm Output IP (Egress) configured (e.g., 192.168.1.101)
2. Verify CAS configuration: **APEX3K-NE EM >> Simulcrypt >> CAS configuration** shows 4 CAS systems
3. Launch M3-Server and configure 1,300 different unicast streams:
   - Program numbers: 1000-2299 (or appropriate range for 1,300 streams)
   - Each stream unique source IP/port
   - All streams target Virtual IP (192.168.1.100)
4. Start all 1,300 streams from M3-Server:
   - Begin streaming all 1,300 simultaneously (or in waves if necessary)
   - Verify streams are ingested into APEX3K-NE
5. Monitor ingestion: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status**:
   - Observe TS and Mappings table populates
   - Wait for all 1,300 to complete ingestion (may take 30-60 seconds)
   - Verify table shows 1,300 active mappings
6. Start MPEG Tracker capture after all streams stabilized
7. Capture 10,000+ TS packets (or 1-2 minutes of stream)
8. Analyze captured packets:
   - Extract all ECM PIDs present in stream
   - Calculate expected number of unique ECM PIDs:
     - 1,300 streams × 4 CAS per stream = 5,200 potential ECM PIDs
     - However, CAS may share ECM PIDs across streams (if same encryption key)
     - Or each stream may have unique ECMs (if different encryption keys)
   - Document actual number of unique ECM PIDs found: [value]
9. Verify PID allocation:
   - Check for PID collisions:
     - Two different CAS systems should NOT share ECM PID
     - Same CAS across different streams should have consistent PID or unique PIDs per stream
   - Verify all ECM PIDs within valid DVB range (13-bit values: 0-8191)
   - No PIDs in reserved ranges (0-31)
10. Verify stream-specific PID mapping:
    - Select 10 random streams from the 1,300
    - For each, identify its ECM PIDs (should be 4 if each CAS has unique PID per stream)
    - Verify no two streams share identical ECM PID set
11. Verify ECM insertion:
    - For random sample of streams (at least 100), verify:
    - ECM packets present for each stream
    - ECM frequency within spec (120ms intervals, ~8 packets/second)
    - No ECM packet loss
12. Monitor system performance:
    - Check APEX3K-NE stability: **APEX-NE EM** interface responsive, no warnings/errors
    - Verify CPU, memory, temperature levels reasonable
    - Check output throughput stable


13. Verify **PASS CRITERIA:** 1,300 streams successfully active simultaneously, Zero PID collisions detected, All ECM PIDs unique and valid, 100% ECM insertion rate for all 1,300 streams, System stability maintained under load
#### 3.0.16.4 Expected Results
- All 1,300 streams ingested and active in Gateway VOD Status
- Unique ECM PIDs allocated for each stream-CAS combination
- No PID collisions detected
- All ECM PIDs valid (within 13-bit range, outside reserved)
- ECMs present for all streams with correct frequency
- System remains stable with 1,300 active streams
- APEX-NE EM responsive and no errors

### 3.0.17 Test Case: CAT Table Update for ECM PIDs
**Test ID:** TC_REL1.2.15-030_017
**Severity:** MEDIUM
#### 3.0.17.2 Objectives
**Objective:** Verify CAT (Conditional Access Table) includes all ECM PIDs and updates when CAS configuration changes

#### 3.0.17.1 Initial Condition
- Test Case 3.0.6 passed (4 CAS systems operational)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active
- MPEG Tracker connected

#### 3.0.17.3 Procedure
1. Monitor TS packets from stream via MPEG Tracker (100+ packets minimum)
2. Locate CAT (Conditional Access Table):
   - Search for table ID 0x01 (CAT)
   - CAT has PID 0x0001
   - Extract first CAT instance
3. Extract CAT descriptor section:
   - Look for CA descriptors (descriptor tag 0x09)
   - Should have descriptor for each ECM PID in system
4. Document each CA descriptor in CAT:
   - **Descriptor 1:** CA_system_ID = [value], ECM_PID = [value]
   - **Descriptor 2:** CA_system_ID = [value], ECM_PID = [value]
   - **Descriptor 3:** CA_system_ID = [value], ECM_PID = [value]
   - **Descriptor 4:** CA_system_ID = [value], ECM_PID = [value]
5. Verify ECM PIDs in CAT match actual ECM PIDs in stream:
   - Cross-reference CAT ECM PIDs with ECM packets captured
   - Verify each ECM PID in CAT has actual packets in stream
   - Verify no extra PIDs listed
6. Record baseline CAT version: [value]
7. Make CAS configuration change:
   - Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
   - Add, remove, or reconfigure SuperCAS
   - Click **Save** or **Apply**
8. Wait 3-5 seconds for APEX3K-NE to process
9. Capture new TS packets including new CAT
10. Locate new CAT and extract:
    - Verify CAT version incremented (should be different from baseline)
    - Extract updated descriptor list
11. Compare CAT descriptor updates:
    - If SuperCAS added: Verify new CA descriptor present for new CAS
    - If SuperCAS removed: Verify removed CA descriptor absent
    - If SuperCAS reconfigured: Verify CAS system ID and/or ECM PID updated
12. Verify ECM PID mapping consistency:
    - Cross-reference updated CAT with new ECM packets in stream
    - All CAT descriptors should have corresponding ECM packets
    - All ECM PIDs in stream should be in CAT
13. Check CAT update timing:
    - Measure time from configuration change to new CAT appearance
    - Should appear within 2-5 seconds


14. Verify **PASS CRITERIA:** CAT descriptors match configured CAS systems, All ECM PIDs in CAT have corresponding packets, CAT updates correctly with configuration changes, No missing or extra descriptors in CAT
#### 3.0.17.4 Expected Results
- CAT contains CA descriptors for all ECM systems
- Each descriptor has correct CAS system ID and ECM PID
- ECM PIDs in CAT match actual ECM packets in stream
- CAT updates correctly when configuration changes
- CAT version increments appropriately
- Update occurs within 2-5 seconds

### 3.0.18 Test Case: Service-Specific ECM Configuration Uniformity
**Test ID:** TC_REL1.2.15-030_018
**Severity:** MEDIUM
#### 3.0.18.2 Objectives
**Objective:** Verify multiple streams with different services receive correct ECM configuration consistently

#### 3.0.18.1 Initial Condition
- Test Case 3.0.6 passed
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- Multiple services configured (if available)
- 5-10 streams active, possibly with different services
- MPEG Tracker connected

#### 3.0.18.3 Procedure
1. Verify multiple services configured:
   - Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1>**
   - Check service configuration (if service-level configuration available)
2. Start 5 streams with different service configurations (if supported):
   - Stream 1-5 configured to different services/programs
   - All streams share same CAS configuration (4 CAS systems)
3. Monitor: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status**
4. Verify all 5 streams show as Active
5. Connect MPEG Tracker and capture packets
6. For each stream, extract:
   - PMT (program-specific information)
   - All CA descriptors in PMT
   - All ECM PIDs for that program
7. Verify uniformity:
   - All 5 streams have ECMs for same 4 CAS systems
   - CA descriptor ordering consistent
   - CAS system IDs identical across all services
   - ECM PID scheme consistent
8. Compare ECM delivery:
   - Verify each stream receives regular ECMs (120ms intervals, ~8 packets/second)
   - Verify no service-specific ECM gaps
9. Document comparison table:
   - Service/Stream | CAS1 | CAS2 | CAS3 | CAS4 | ECM Frequency | Status
10. Verify consistency across all services


11. Verify **PASS CRITERIA:** All services uniformly configured with 4 CAS systems, 100% ECM delivery consistency, No service-specific anomalies
#### 3.0.18.4 Expected Results
- All services/streams receive identical CAS configuration
- All 4 ECMs present for each service
- No service-specific variations
- ECM frequency consistent across services
- Uniform delivery regardless of service

### 3.0.19 Test Case: ECM Handling During Stream Pause/Resume
**Test ID:** TC_REL1.2.15-030_019
**Severity:** MEDIUM
#### 3.0.19.2 Objectives
**Objective:** Verify ECM insertion continues or handles gracefully during stream pause/resume on M3-Server

#### 3.0.19.1 Initial Condition
- VOD stream active with all 4 ECMs flowing
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- M3-Server pause/resume capability available
- MPEG Tracker capturing

#### 3.0.19.3 Procedure
1. Verify stream active:
   - Monitor: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** shows stream Active
   - MPEG Tracker showing regular TS packets and ECMs
2. Document baseline ECM pattern:
   - Count ECM packets over 10-second window before pause
   - Verify normal frequency (120ms intervals, ~8 packets/second)
3. Issue pause command on M3-Server:
   - Using M3-Server interface, pause the VOD playback
   - Stream input halts but connection remains open
4. Note timestamp of pause command
5. Continue MPEG Tracker capture during pause (10-20 seconds)
6. Monitor APEX3K-NE status during pause:
   - Verify stream status in Gateway VOD Status (may show Paused or Active depending on implementation)
   - Check for any error messages or warnings
7. Analyze captured packets during pause:
   - Determine if APEX3K-NE continues generating ECMs (likely yes, with no new content)
   - Or if ECM generation pauses (acceptable alternative)
   - Document observed behavior
8. Issue resume command on M3-Server:
   - Resume playback on M3-Server
   - Stream content flow resumes
9. Note timestamp of resume command
10. Continue MPEG Tracker capture after resume (10-20 seconds)
11. Analyze post-resume packets:
    - Verify TS packet sequence resumes
    - Verify ECM generation resumes/continues
    - Verify PCR (Program Clock Reference) properly handles resume transition
    - Check for any packet loss or gaps
12. Verify stream stability:
    - No CRC errors after resume
    - No discontinuities or corruption
    - Stream playback normal
13. Test pause/resume cycle multiple times (3-5 cycles)


14. Verify **PASS CRITERIA:** Pause/resume transitions handled without errors, Stream remains active or appropriately paused during pause, Resume successful with no data loss, ECM continuity maintained across pause/resume
#### 3.0.19.4 Expected Results
- Stream pause handled gracefully
- ECM behavior consistent (either continues or pauses with stream)
- Stream resumes successfully
- No packet loss or corruption during pause/resume
- PCR and stream timing maintained
- No errors or warnings generated

### 3.0.20 Test Case: Dynamic CAS Addition with Active ECMs
**Test ID:** TC_REL1.2.15-030_020
**Severity:** HIGH
#### 3.0.20.2 Objectives
**Objective:** Add 3rd SuperCAS to running stream with existing ECMs and verify new ECM inserted without stream interruption

#### 3.0.20.1 Initial Condition
- 2 SuperCAS + 1 MediaCipher (3 CAS total) operational with 3 ECMs flowing
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active and stable
- MPEG Tracker capturing continuous stream
- 3rd SuperCAS available but not configured

#### 3.0.20.3 Procedure
1. Verify baseline state:
   - Stream active: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** shows Active
   - MPEG Tracker capturing with 3 ECMs present
   - Document baseline 3 ECM PIDs and CAS system IDs
2. Begin continuous MPEG Tracker capture:
   - Record TS stream continuously
   - Note timestamp at start
3. Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
4. Add 3rd SuperCAS while stream is flowing:
   - Click **Add** or **Configure CAS**
   - Enter 3rd SuperCAS (0x5601) details
   - Click **Save** or **Apply**
   - Note timestamp of configuration save
5. Observe APEX3K-NE response (target: < 5 seconds for ECM update):
   - Monitor Gateway VOD Status for stream status
   - Should remain Active (no interruption)
   - Check for any error messages (should be none)
6. Continue MPEG Tracker capture for 15 additional seconds after configuration change
7. Stop MPEG Tracker capture
8. Analyze captured stream:
   - Identify exact point when configuration changed (based on timestamp)
   - Before configuration change: Should see 3 ECMs (MediaCipher, SuperCAS1, SuperCAS2)
   - After configuration change: Should see 4 ECMs (+ SuperCAS3)
   - Measure time from configuration change to first new ECM (SuperCAS3) appearance
9. Verify ECM insertion characteristics for new SuperCAS3:
   - ECM PID is unique (not collision with existing 3)
   - CAS system ID = 0x5601
   - Insertion frequency within spec (120ms intervals, ~8 packets/second)
10. Verify stream continuity:
    - No packet loss around configuration change point
    - TS packet sequence continuous
    - PCR continuous
    - No CRC errors
11. Verify original 3 ECMs unaffected:
    - Original ECM PIDs unchanged
    - Original ECM frequencies maintained
    - No interruption in original ECM streams


12. Verify **PASS CRITERIA:** Configuration accepted without stream restart, New ECM inserted within 5 seconds, All 4 ECMs operational post-addition, Zero packet loss or corruption, Original ECM service uninterrupted
#### 3.0.20.4 Expected Results
- 3rd SuperCAS added without stream interruption
- New ECM (SuperCAS3) appears within 5 seconds of configuration change
- Original 3 ECMs continue unaffected
- All 4 ECMs present and functioning after addition
- Stream packet continuity maintained
- No errors or warnings
- Stream quality unaffected

### 3.0.21 Test Case: ECM Update Propagation Time
**Test ID:** TC_REL1.2.15-030_021
**Severity:** MEDIUM
#### 3.0.21.2 Objectives
**Objective:** Measure time from CAS configuration change to ECM update in transport stream

#### 3.0.21.1 Initial Condition
- VOD stream active with baseline CAS configuration
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- MPEG Tracker with precise timing capabilities
- CAS configuration ready to change (add, remove, or modify)

#### 3.0.21.3 Procedure
1. Establish baseline configuration:
   - Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
   - Document current CAS systems
2. Synchronize timing:
   - Set up precise timing reference (MPEG Tracker clock or system clock)
   - Start continuous MPEG Tracker capture
3. Prepare configuration change:
   - Identify which CAS to add/remove/modify
   - Have configuration ready
4. Perform configuration change:
   - Click **Add** or **Remove** CAS button
   - Enter configuration details or select to delete
   - Click **Save** or **Apply**
   - **Note exact timestamp of configuration save action** (T0)
5. Immediately continue MPEG Tracker capture with precise timing
6. Scan captured stream packets:
   - Starting from time T0, search for ECM changes
   - If adding CAS: Look for new ECM PID appearance
   - If removing CAS: Look for ECM PID disappearance
   - Note timestamp when ECM change first appears (T1)
7. Calculate propagation time: T1 - T0 = Propagation delay
8. Repeat configuration change 4 more times to establish average:
   - Change 1: Add SuperCAS, measure propagation time
   - Change 2: Remove SuperCAS, measure propagation time
   - Change 3: Add different SuperCAS, measure propagation time
   - Change 4: Remove SuperCAS, measure propagation time
   - Change 5: Modify CAS configuration, measure propagation time
9. Calculate statistics:
   - Minimum propagation time: [value]
   - Maximum propagation time: [value]
   - Average propagation time: [value]
   - Standard deviation: [value]
10. Document target requirement:
    - Target propagation time: < 2 seconds


11. Verify **PASS CRITERIA:** Average propagation time < 2 seconds, 100% of changes propagate within 2 seconds, Variance < 500ms
#### 3.0.21.4 Expected Results
- Configuration changes reflected in ECM stream within 2 seconds
- Consistent propagation time across multiple changes
- Acceptable variance (< 500ms)
- No excessive delays

### 3.0.22 Test Case: ECM Error Recovery
**Test ID:** TC_REL1.2.15-030_022
**Severity:** HIGH
#### 3.0.22.2 Objectives
**Objective:** Verify ECM error handling and recovery

#### 3.0.22.1 Initial Condition
- VOD stream active with all 4 ECMs
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- APEX-NE EM accessible
- System logging accessible
- MPEG Tracker connected

#### 3.0.22.3 Procedure
1. Monitor current state:
   - Verify stream active: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** shows Active
   - MPEG Tracker showing regular ECMs for all 4 CAS
2. Test Scenario A: ECM Server Connectivity Loss (if testable):
   - If ECMG server connectivity can be interrupted:
   - Stop or disconnect ECMG server
   - Monitor APEX3K-NE response (may see degraded service or error messages)
   - Document error message and system behavior
   - Restore ECMG server connectivity
   - Verify ECM recovery (resume within 30 seconds target)
3. Test Scenario B: CAS Configuration Error (if testable):
   - Attempt to configure invalid CAS system ID
   - Verify system rejects or handles gracefully
   - Verify existing ECMs unaffected
4. Observe ECM error logging:
   - Navigate to: **APEX-NE EM >> Logs** (or appropriate logging interface)
   - Search for ECM-related errors or warnings
   - Document any ECM error entries: [list]
5. Verify error recovery mechanisms:
   - Verify system detects and reports errors
   - Verify error messages clear and actionable
   - Verify system attempts recovery (if applicable)
6. Stream stability during error:
   - Verify stream continues or gracefully stops (no corruption)
   - Verify no cascading failures
   - Verify other services unaffected
7. Document all error conditions observed and recovery actions


8. Verify **PASS CRITERIA:** Errors detected and logged appropriately, System recovery successful, Stream quality unaffected or degrades gracefully, No system instability or crashes
#### 3.0.22.4 Expected Results
- System handles ECM errors gracefully
- Error messages clear and logged
- Stream continues or safely stops (no corruption)
- ECMs recover automatically when error condition resolves
- No cascading failures to other systems
- Recovery within 30 seconds of error resolution

### 3.0.23 Test Case: ECM Validation Against CAS System IDs
**Test ID:** TC_REL1.2.15-030_023
**Severity:** MEDIUM
#### 3.0.23.2 Objectives
**Objective:** Verify ECM contains correct CAS system ID matching configured CAS systems

#### 3.0.23.1 Initial Condition
- All 4 CAS systems configured (Test Case 3.0.6 completed)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- VOD stream active with all 4 ECMs
- MPEG Tracker capturing

#### 3.0.23.3 Procedure
1. Query configured CAS systems:
   - Navigate to: **APEX3K-NE EM >> Simulcrypt >> CAS configuration**
   - Document all configured CAS system IDs:
     - MediaCipher: 0x4AD0 (or actual)
     - SuperCAS1: [actual CAS ID] (example: 0x4B46)
     - SuperCAS2: [actual CAS ID] (example: 0x4BB8)
     - SuperCAS3: [actual CAS ID] (example: 0x5601)
2. Monitor TS packets via MPEG Tracker
3. Extract all ECM packets from monitored stream
4. For each ECM, validate CAS system ID:
   - Parse ECM header to extract CAS system ID field
   - Cross-reference extracted ID with configured ID list
   - Verify match: Each ECM CAS ID matches one of configured CAS IDs
5. Verify all configured CAS have ECMs:
   - Count unique CAS system IDs found in monitored ECMs
   - Should equal number of configured CAS (4 in this test)
   - All configured IDs should be present
6. Verify no unexpected CAS IDs:
   - Verify no ECM with CAS system ID not in configured list
   - All ECM CAS IDs must match configuration
7. Sample validation (extract 10-20 ECMs for each CAS):
   - MediaCipher: Extract 10 ECMs, verify all have CAS ID 0x4AD0
   - SuperCAS1: Extract 10 ECMs, verify all have correct ID
   - SuperCAS2: Extract 10 ECMs, verify all have correct ID
   - SuperCAS3: Extract 10 ECMs, verify all have correct ID
8. Cross-reference with PMT:
   - Extract PMT CA descriptors
   - Verify CAS system IDs in PMT descriptors match ECM CAS IDs
   - Verify one-to-one mapping


9. Verify **PASS CRITERIA:** 100% of ECMs have valid CAS system ID, All CAS IDs match configuration, No unexpected CAS IDs found
#### 3.0.23.4 Expected Results
- All ECM CAS system IDs match configured CAS systems
- No ECMs with unrecognized CAS IDs
- All configured CAS have corresponding ECMs
- PMT descriptors match ECM CAS IDs
- Complete consistency verified

### 3.0.24 Test Case: PMT Consistency Across Multiple Captures
**Test ID:** TC_REL1.2.15-030_024
**Severity:** MEDIUM
#### 3.0.24.2 Objectives
**Objective:** Verify PMT content consistent across multiple stream captures

#### 3.0.24.1 Initial Condition
- VOD stream active with stable configuration
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- MPEG Tracker capable of multiple captures
- All 4 CAS systems configured

#### 3.0.24.3 Procedure
1. Perform PMT Monitoring Session 1:
   - Monitor 500 TS packets via MPEG Tracker
   - Extract PMT (table ID 0x02) from monitored stream
   - Document:
     - PMT version
     - Program number
     - PCR PID
     - All CA descriptor details (4 descriptors)
     - All ES information
2. Wait 5 minutes with stream active
3. Perform PMT Capture Session 2:
   - Capture new 500 TS packets
   - Extract PMT from new capture
   - Document same information as Session 1
4. Wait 5 minutes
5. Perform PMT Capture Session 3:
   - Repeat capture and documentation
6. Compare captured PMTs:
   - PMT structure should be identical across captures (except version if changed)
   - Program number should be same
   - PCR PID should be same
   - CA descriptor count should be same (4)
   - CA descriptor ordering should be same
   - Each CA descriptor CAS ID should match exactly
   - Each CA descriptor ECM PID should match exactly (or be consistent)
   - All ES information should match
7. Document differences (if any):
   - PMT version may increment if configuration changed
   - Note any other differences: [list]
8. Verify descriptor consistency:
   - Extract CA descriptors from each capture
   - Create side-by-side comparison table
   - Verify all descriptors identical (except version)


9. Verify **PASS CRITERIA:** 100% structural consistency across captures, All descriptors match exactly (except version), No anomalies or unexpected changes
#### 3.0.24.4 Expected Results
- PMT structure consistent across all captures
- PMT descriptors and ES information unchanged
- CAS system IDs and ECM PIDs consistent
- Only PMT version may change if configuration updated
- No unexpected variations

### 3.0.25 Test Case: ECM Performance Under Load (1,300+ mappings per blade)
**Test ID:** TC_REL1.2.15-030_025
**Severity:** CRITICAL
#### 3.0.25.2 Objectives
**Objective:** Verify ECM insertion operational and without delays for 1,300 simultaneous streams on single blade

#### 3.0.25.1 Initial Condition
- Test Case 3.0.16 completed (1,300 streams active)
- Gateway VOD configured and ENABLED on Blade<1>
  - When GVOD is enabled, other TS types are NOT available for configuration on this blade
- All 4 CAS systems configured
- MPEG Tracker connected
- System monitoring tools available

#### 3.0.25.3 Procedure
1. Verify baseline state from Test Case 3.0.16:
   - 1,300 VOD streams active and ingested
   - All streams appear in: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status**
   - All streams showing as Active
2. Connect MPEG Tracker to output
3. Monitor system performance metrics:
   - CPU utilization: [monitor via APEX-NE EM System Dashboard]
   - Memory utilization: [monitor]
   - ECM processing rate: [calculate from packet monitoring]
   - Total output bitrate: [monitor]
4. Monitor 20,000+ TS packets (2-5 minutes continuous) via MPEG Tracker
5. Analyze ECM insertion across all 1,300 streams:
   - Extract all ECM packets from monitoring
   - Count total ECM packets: [value]
   - Calculate ECM packets per second: [value]
6. Verify ECM coverage for active streams:
   - Sample 100 random streams from the 1,300
   - For each sample stream, verify:
     - ECM packets present for all 4 CAS (or appropriate CAS for that stream)
     - ECM frequency within spec (120ms intervals, ~8 packets/second)
     - No missing ECMs or gaps
   - Calculate: Number of streams with valid ECMs / 100 sample streams
   - Target: 100% of sampled streams have valid ECMs
7. Verify insertion delay:
   - Measure latency from configuration/stream initialization to ECM appearance
   - Verify delays acceptable (< 500ms typical, < 2 seconds max)
8. Monitor for ECM insertion errors:
   - Check APEX-NE EM logs: **APEX-NE EM >> Logs** for ECM-related errors
   - Document any error entries: [list]
   - Count error rate: Errors / 1,300 streams
   - Target: Error rate < 0.1%
9. Verify stream stability:
   - Monitor stream status throughout capture
   - Check for any streams dropping to Inactive or Error status
   - Count stability: Streams remaining Active / 1,300 total
   - Target: 100% of streams remain Active
10. Analyze resource consumption:
    - Measure peak CPU utilization during 1,300-stream ECM insertion: [value]%
    - Measure peak memory utilization: [value]%
    - Measure peak temperature (if available): [value]°C
    - Verify all metrics within acceptable ranges
11. Monitor output quality:
    - Verify output bitrate consistent
    - Verify no packet loss on output
    - Verify PCR continuity
    - Verify CRC error rate acceptable
12. Document performance summary:
    - ECM insertion success rate: [%]
    - Average ECM frequency: [packets/sec]
    - Average processing latency: [ms]
    - Peak CPU utilization: [%]
    - Stream stability: [%]


13. Verify **PASS CRITERIA:** ECM insertion success rate ≥ 99.9%, Average ECM frequency within 120ms spec (~8 packets/second), Error rate < 0.1%, 100% stream stability, Peak CPU < 85% utilization, Peak memory < 85% utilization, Output CRC error rate < 0.01%
#### 3.0.25.4 Expected Results
- ECMs successfully inserted for all 1,300 streams
- Insertion frequency within specification
- < 0.1% error rate
- 100% of streams remain active
- System resources (CPU, memory, temperature) within acceptable ranges
- Output stream quality maintained
- No performance degradation observed


---

## 4.0 REL1.2.15-040: Transport Stream Capacity

### 4.0.1 Test Case: Maximum 1,300 Mappings per Blade (APEX3K-NE)
**Test ID:** TC_REL1.2.15-040_001  
**Severity:** HIGH  
#### 4.0.1.2 Objectives
**Objective:** Verify APEX3K-NE Gateway VOD can handle 1,300 simultaneous unicast streams from M3 server and display all mappings with correct input/output IPs and program numbers in GVOD Status

#### 4.0.1.1 Initial Condition
- Single blade or isolated test blade
- Gateway VOD enabled: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Config >> Enable Gateway VOD**
- Virtual IP (Ingress) configured: example 192.168.1.100 (where M3-Server sends streams)
- Output IP (Egress) configured: example 192.168.1.101 (where APEX3K-NE sends TS output)
- M3-Server VOD streamer available and operational with capability to send 1,300 simultaneous unicast streams
- Sufficient system resources for 1,300 concurrent streams
- MPEG Tracker connected after APEX3K RF output for monitoring

**Test Steps:**
1. Verify Gateway VOD configuration in APEX-NE EM:
   - Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Config**
   - Confirm Gateway VOD = **Enable**
   - Confirm Virtual IP (Ingress) = **192.168.1.100** (or configured value)
   - Confirm Output IP (Egress) = **192.168.1.101** (or configured value)

2. Start M3-Server unicast stream generation:
   - Launch M3-Server application
   - Configure to send **1,300 different unicast streams** to the Virtual IP (192.168.1.100)
   - Each stream should have a unique program number (e.g., PN 1000-2299)
   - Start streaming from M3-Server (streams will be sent to APEX3K-NE Virtual IP)

3. Monitor stream ingestion in APEX3K-NE:
   - Wait 5-10 seconds for streams to reach APEX3K-NE
   - Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status**
   - Observe TS and Mappings table for incoming streams

4. Verify all 1,300 TS mappings are displayed:
   - Confirm table shows all 1,300 transport stream mappings
   - Scroll through the table to verify complete list
   - Each row should display:
     - **TS ID/Index** (1-1300)
     - **Input IP** = 192.168.1.100 (Virtual IP - source)
     - **Input Port** (port used by M3-Server)
     - **Program Number** (unique for each stream: 1000-2299 or configured range)
     - **Output IP** = 192.168.1.101 (Output IP - destination)
     - **Output Port** (APEX3K-NE assigned)
     - **Status** = Active/Online
     - **Encryption Status** (if applicable)

5. Verify mapping accuracy:
   - Select 5 random mappings from different sections (first 10, middle 650, last 10):
     - Click on each mapping to verify detailed information
     - Confirm Input IP, Output IP, and Program Number match expectations
   - Document sample mappings (e.g., TS #1, #650, #1300)

6. Monitor device stability and stream throughput:
   - Verify APEX3K-NE device remains operational (no alarms/warnings in APEX-NE EM)
   - Check device temperature: Monitor via APEX-NE EM System Dashboard (if available)
   - Verify output throughput: Confirm device is processing and forwarding all 1,300 streams
   - Confirm device responsiveness: APEX-NE EM interface remains responsive (no hangs/timeouts)
   - Check for any error messages or warnings in system logs

7. Test stream quality and playback:
   - Select 3 random streams from the 1,300 (e.g., TS #100, #650, #1250)
   - Verify each stream can be decoded/monitored
   - Confirm video/audio output is active
   - Monitor via MPEG Tracker for packet structure and integrity

8. Verify all streams remain active:
   - Monitor for minimum 2 minutes
   - Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status**
   - Confirm all 1,300 mappings still show as Active
   - Check for any dropped or offline mappings (should be zero)

9. Stress test with rapid monitoring:
   - Repeatedly refresh GVOD Status table (5-10 times in 30 seconds)
   - Verify all 1,300 mappings still display correctly
   - Confirm no UI lag or performance degradation

10. Monitor MPEG Tracker for output verification:
    - Connect MPEG Tracker to APEX3K-NE RF output
    - Verify output stream quality and integrity
    - Confirm no packet loss or errors
    - Sample 10-20 program numbers to verify correct content routing

#### 4.0.1.4 Expected Results
- All 1,300 unicast streams from M3-Server successfully ingested by APEX3K-NE
- GVOD Status displays exactly 1,300 TS mappings in the table
- Each mapping displays:
  - Correct Input IP (192.168.1.100 - Virtual IP)
  - Correct Output IP (192.168.1.101 - Output IP)
  - Unique Program Number (1000-2299 range or configured)
  - Active/Online status for all mappings
- APEX3K-NE device remains stable and operational with no alarms/errors
- Device temperature within normal operating range
- All streams remain active for continuous 2+ minute monitoring period
- MPEG Tracker confirms output stream quality and integrity
- No mapping drops, errors, or UI performance issues
- Stream playback verification successful for random sample mappings

### 4.0.2 Test Case: Reject Capacity Exceed (1,301st Mapping)
**Test ID:** TC_REL1.2.15-040_002  
**Severity:** HIGH  
#### 4.0.2.2 Objectives
**Objective:** Verify APEX3K-NE rejects mapping creation exceeding capacity limit

#### 4.0.2.1 Initial Condition
- 1,300 mappings already created and active
- Attempting to add 1,301st mapping

**Test Steps:**
1. Verify 1,300 mappings in: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** (TS and Mappings table)
2. Attempt to create 1,301st mapping (via M3-Server or manual)
3. Monitor APEX-NE EM for mapping creation
4. Verify rejection with error message
5. Document error message text
6. Verify existing 1,300 mappings remain unaffected
7. Verify no system instability

#### 4.0.2.4 Expected Results
- 1,301st mapping rejected
- Clear error message: "Maximum 1,300 mappings reached" (or similar)
- Existing 1,300 unaffected
- System remains stable

### 4.0.3 Test Case: Multi-Blade Capacity Isolation (APEX3K-NE)
**Test ID:** TC_REL1.2.15-040_003  
**Severity:** MEDIUM  
#### 4.0.3.2 Objectives
**Objective:** Verify each blade has independent 1,300 mapping capacity

#### 4.0.3.1 Initial Condition
- 3-blade APEX3K-NE system
- All blades support Gateway VOD

**Test Steps:**
1. Configure Blade<1>: **Blade >> Select Blade<1> >> Config >> Enable Gateway VOD**
   - Virtual IP: 192.168.1.100
   - Output IP: 192.168.1.101
2. Create 1,300 mappings on Blade<1>
3. Configure Blade<2>: **Blade >> Select Blade<2> >> Config >> Enable Gateway VOD**
   - Virtual IP: 192.168.2.100
   - Output IP: 192.168.2.101
4. Create 1,300 mappings on Blade<2>
5. Configure Blade<3>: **Blade >> Select Blade<3> >> Config >> Enable Gateway VOD**
   - Virtual IP: 192.168.3.100
   - Output IP: 192.168.3.101
6. Create 1,300 mappings on Blade<3>
7. Verify total 3,900 mappings across system
8. Attempt 1,301st on Blade<2> (should fail)
9. Verify Blade<1> and <3> unaffected

#### 4.0.3.4 Expected Results
- Each blade supports full 1,300 independent
- Total 3,900 mappings across 3 blades
- Capacity isolation maintained
- No cross-blade interference

### 4.0.4 Test Case: Capacity Maintained During Dynamic Addition
**Test ID:** TC_REL1.2.15-040_004  
**Severity:** MEDIUM  
#### 4.0.4.2 Objectives
**Objective:** Verify capacity handling during dynamic stream addition

#### 4.0.4.1 Initial Condition
- Starting with 1,000 active mappings
- Adding 300 more to reach 1,300 capacity

**Test Steps:**
1. Monitor 1,000 active mappings baseline
2. Monitor performance metrics (CPU, memory, throughput)
3. Start adding 300 new streams (may use script)
4. Monitor during addition (watch for issues)
5. Verify all 1,300 active after completion
6. Verify existing 1,000 remain uninterrupted
7. Monitor performance after reaching capacity

#### 4.0.4.4 Expected Results
- 300 added successfully
- All 1,300 active and stable
- No disruption to existing 1,000
- Performance acceptable at capacity

**DTCP Configuration Location:** APEX-NE EM >> Chassis >> VOD >> Follow DTCP Descriptor

**Key DTCP Differences in Gateway VOD Mode vs APEX 3000:**
- UDP Routes are dynamically created based on input UDP port streams
- Outputted streams are NOT QAM outputs (UDP Port mapped instead)
- When input DTCP descriptor is LOST: output PRKM RMD settings revert to CTE settings within **10 seconds** (vs 15 seconds in APEX 3000)
- Tier level information available on: **GVOD Status GUI >> APEX-NE EM >> Blade >> Config >> GVOD Status**
- No ERM commands in Gateway VOD mode, thus never any XML blobs

**Follow DTCP Session Control Parameter (APEX3K-NE):**
- Configuration Path: **APEX-NE EM >> Chassis >> VOD >> Follow DTCP Session Control**
- Default: Disabled
- When **Enabled:** Follow DTCP descriptor if present. If no descriptor, use CTE settings. Tier type for CTE based on APS setting
- When **Disabled:** Use CTE settings exclusively (results in CTE encryption)

**DTCP Descriptor Syntax:**
- descriptor_tag: 0x88
- descriptor_length: 0x4
- CA_System_ID: 0x0FFF
- Contains: Retention_Move_Mode, Retention_State, EPN, DTCP_CCI, AST, Image_Constraint_Token, APS


---

## 5.0 REL1.2.15-050: Pre-encrypted & DTCP

### 5.0.1 Test Case: Enable DTCP Follow Capability in Gateway VOD Mode
**Test ID:** TC_REL1.2.15-050_001  
**Severity:** CRITICAL  
#### 5.0.1.2 Objectives
**Objective:** Verify VOD_X6_022 - Blade in Gateway VOD Mode supports "Follow DTCP" capability via "Follow DTCP Session Control" parameter

#### 5.0.1.1 Initial Condition
- APEX3K-NE with multiple blades operational
- APEX-NE EM accessible with administrator access
- M3-Server VOD streamer configured
- DTCP test streams available from source device (SEM or FuzzStreamer)
- Blade configured in Gateway VOD Mode per REL1.2.15-010

**Initial Conditions (Per Reference):**
- Reuse APEX NE configuration where M3 Server streams equally divided among Blades
- Some routes removed from M3 Server to accommodate inputs from source device
- Source device unicasting DTCP test streams to be routed by APEX NE
- Each blade in Gateway VOD Mode

#### 5.0.1.3 Procedure
1. Access APEX-NE EM >> Chassis >> VOD
2. Locate parameter: **"Follow DTCP Session Control"**
3. Verify parameter displays options: Enabled / Disabled (default = Disabled)
4. Set "Follow DTCP Session Control" to **Enabled**
5. Click **Save** or **Apply**
6. Verify confirmation message (< 3 seconds)
7. Configure M3-Server to send equal load across Blades
8. Configure source device to unicast DTCP test streams to each Blade's Virtual IP
9. Start DTCP stream input to Blade<1>
10. Verify stream routing in: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** (TS and Mappings table)
11. Monitor output via: **UDP output streams to CTE authorized set-top**
12. Verify DTCP descriptor present in output stream
13. Verify CCI/APS values in output match input (if Follow DTCP enabled)
14. Repeat steps 9-13 for Blade<2> through Blade<8>
15. Verify tier level info displayed on: **APEX-NE EM >> Blade >> Config >> GVOD Status GUI**

**Expected Results (Per PFS):**
- Parameter "Follow DTCP Session Control" accessible and functional
- When Enabled: Follow DTCP descriptor if present
- When descriptor absent: Use CTE settings
- Tier type for CTE based on APS setting of DTCP
- Output streams match input DTCP requirements
- Tier level info visible in GVOD Status GUI
- **Monitoring Points:** DTCP descriptor presence/absence in output, CCI/APS values preservation, Tier level information accuracy, Per-blade stream routing

---


1. Verify **PASS CRITERIA:** Follow DTCP parameter enabled successfully, DTCP descriptors followed on all 8 blades, Tier level info available on GVOD Status GUI, Output streams properly formatted
1. Access APEX-NE EM >> Chassis >> VOD
2. Locate parameter: **"Follow DTCP Session Control"**
3. Verify parameter displays options: Enabled / Disabled (default = Disabled)
4. Set "Follow DTCP Session Control" to **Enabled**
5. Click **Save** or **Apply**
6. Verify confirmation message (< 3 seconds)
7. Configure M3-Server to send equal load across Blades
8. Configure source device to unicast DTCP test streams to each Blade's Virtual IP
9. Start DTCP stream input to Blade<1>
10. Verify stream routing in: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** (TS and Mappings table)
11. Monitor output via: **UDP output streams to CTE authorized set-top**
12. Verify DTCP descriptor present in output stream
13. Verify CCI/APS values in output match input (if Follow DTCP enabled)
14. Repeat steps 9-13 for Blade<2> through Blade<8>
15. Verify tier level info displayed on: **APEX-NE EM >> Blade >> Config >> GVOD Status GUI**

**Expected Results (Per PFS):**
- Parameter "Follow DTCP Session Control" accessible and functional
- When Enabled: Follow DTCP descriptor if present
- When descriptor absent: Use CTE settings
- Tier type for CTE based on APS setting of DTCP
- Output streams match input DTCP requirements
- Tier level info visible in GVOD Status GUI
- **Monitoring Points:** DTCP descriptor presence/absence in output, CCI/APS values preservation, Tier level information accuracy, Per-blade stream routing

---

### 5.0.2 Test Case: DTCP Descriptor Modified on Source Device
**Test ID:** TC_REL1.2.15-050_002  
**Severity:** HIGH  
#### 5.0.2.2 Objectives
**Objective:** Verify APEX3K-NE handles DTCP descriptor modifications from source device

#### 5.0.2.1 Initial Condition
- DTCP Follow enabled as per TC_REL1.2.15-050_001
- DTCP test streams flowing to Blade<1>
- Source device capable of modifying DTCP descriptors on the fly
- MPEG Tracker connected after APEX3K RF output for packet analysis

**Test Steps:**
1. Start DTCP stream to Blade<1> with known DTCP descriptor values
2. Capture baseline descriptor: APS, CCI, Image_Constraint_Token values
3. Verify output stream descriptor via MPEG Tracker
4. On source device: Modify DTCP descriptor (e.g., change APS value)
5. Send modified descriptor to APEX NE (Blade<1>)
6. Wait for output update (should be immediate or within 1-2 seconds)
7. Monitor new descriptor from output via MPEG Tracker
8. Verify modified APS value reflected in output
9. Repeat modification: Change Image_Constraint_Token on source
10. Verify output reflects new Image_Constraint_Token
11. Repeat for multiple CCI values (Full, FWK, FPK, Clear, Unencrypted)
12. Monitor no disruption to stream delivery during modifications

#### 5.0.2.4 Expected Results
- DTCP descriptor modifications followed immediately
- Output descriptor values match source modifications
- CCI/APS values updated correctly
- Stream continuity maintained
- No service interruption during changes
- **Monitoring Points:** DTCP descriptor field changes, APS/CCI value updates, Output stream quality/continuity, Descriptor update latency (should be < 2 seconds)

---

### 5.0.3 Test Case: DTCP Descriptor Loss and CTE Settings Reversion
**Test ID:** TC_REL1.2.15-050_003  
**Severity:** CRITICAL  
#### 5.0.3.2 Objectives
**Objective:** Verify VOD_X6_022 - When input DTCP descriptor lost, output PRKM RMD settings revert to CTE settings within **10 seconds** (APEX NE specific)

#### 5.0.3.1 Initial Condition
- DTCP Follow enabled
- DTCP stream flowing to Blade<1>
- CTE Configuration settings known: **APEX-NE EM >> Chassis >> VOD >> CTE Configuration**
- MPEG Tracker monitoring output
- Stopwatch/timer available to measure reversion time

**Test Steps:**
1. Establish DTCP stream with valid descriptor to Blade<1>
2. Verify output descriptor shows DTCP values (APS, CCI, etc.)
3. Record CTE Configuration settings from: **Chassis >> VOD >> CTE Configuration**
4. On source device: Stop sending DTCP descriptor (input descriptor loss)
5. Immediately start timer at T=0
6. Monitor output stream via MPEG Tracker
7. At T=5 seconds: Check output descriptor (should still show DTCP values)
8. At T=8 seconds: Check output descriptor (should still show DTCP values)
9. At T=10 seconds: Check output descriptor (should NOW show CTE settings)
10. Verify PRKM RMD settings in output match recorded CTE settings
11. Verify no stream interruption during transition
12. Verify tier level info on: **APEX-NE EM >> Blade >> Config >> GVOD Status GUI** reflects CTE tier

**Expected Results (Per APEX NE PFS):**
- Reversion to CTE settings completes within **10 seconds**
- Output PRKM RMD settings match CTE configuration
- No stream interruption
- Tier level updated on GVOD Status GUI
- Tier type based on CTE settings
- **Monitoring Points:** Exact reversion time measurement, PRKM RMD value changes, Stream delivery during transition, Tier level info updates

**Key APEX NE Specific Difference:**
APEX 3000 reverts within 15 seconds; APEX NE reverts within **10 seconds** (5-second improvement)

---

### 5.0.4 Test Case: DTCP Follow Disabled - CTE Settings Enforcement
**Test ID:** TC_REL1.2.15-050_004  
**Severity:** HIGH  
#### 5.0.4.2 Objectives
**Objective:** Verify when "Follow DTCP Session Control" is Disabled, CTE settings are used exclusively

#### 5.0.4.1 Initial Condition
- APEX3K-NE configured for Gateway VOD
- DTCP test streams available
- CTE Configuration settings known

**Test Steps:**
1. Access: **APEX-NE EM >> Chassis >> VOD**
2. Set "Follow DTCP Session Control" to **Disabled** (default)
3. Click Save/Apply
4. Input DTCP stream with specific APS value (e.g., APS=Copy Freely)
5. Input DTCP stream with different CCI value (e.g., CCI=Copy Once)
6. Verify output streams via MPEG Tracker
7. Check output descriptor: Should show CTE tier/settings, NOT DTCP values
8. Modify source DTCP descriptor (change APS/CCI values)
9. Verify output does NOT follow modifications (still uses CTE settings)
10. Monitor output stream quality/encryption

#### 5.0.4.4 Expected Results
- Follow DTCP disabled → CTE settings applied to all streams
- Output descriptor shows CTE values only
- Source DTCP modifications ignored
- All streams encrypted per CTE configuration
- No DTCP descriptor influence on output

**Pre-encrypted Configuration Location:** APEX-NE EM >> VOD >> Session control configurations

**Pre-encrypted Stream Types Tested:**
- Broadcast Encrypted (Full)
- FWK (Forward Working Key)
- FPK (Fast Pre-encrypted Key) - Optional per DAC support
- Clear
- Unencrypted CCI

**Configuration Options:**
1. **Follow DTCP Descriptor:** Enable / Disable
2. **Pre-encrypted Checking:** Enable / Disable

**Key Behavior (Per APEX NE PFS - CRITICAL):**
- When **Pre-encrypted Checking = ENABLED:** 
  - Input WITH CA_descriptor → Detected as pre-encrypted → PASS-THROUGH with SAME CA_descriptor (no re-encryption)
  - Input WITHOUT CA_descriptor → Detected as clear → ENCRYPT normally and INSERT CTE CA_descriptor
- When **Pre-encrypted Checking = DISABLED:**
  - Any input → STRIP CA_descriptor (if present) → ENCRYPT with CTE → INSERT new CTE CA_descriptor (re-encryption)

### 5.0.5 Test Case: Pre-encrypted Service Detection - Full Encryption Input (ENABLED = PASS-THROUGH)
**Test ID:** TC_REL1.2.15-050_005  
**Severity:** CRITICAL  
#### 5.0.5.2 Objectives
**Objective:** Verify VOD_X6_023 - When Pre-encrypted Checking ENABLED: Input with CA_descriptor → Pass-through with same CA_descriptor (no re-encryption)

#### 5.0.5.1 Initial Condition
- Pre-encrypted content source available (Source APEX NE, NE2000/2500, or capable device)
- Source capable of generating Broadcast Encrypted (Full) streams WITH CA_descriptor
- APEX3K-NE configured for Gateway VOD Mode
- M3-Server routes equally divided among 8 Blades
- Some routes disabled to accommodate pre-encrypted inputs

**Initial Conditions (Per Reference):**
- 1536 routes of M3 Server equally divided across 8 Blades
- Pre-encrypted streams with CA_descriptor from source device
- CTE Encryption setting = FULL
- Pre-encrypted Checking = **ENABLED** ⭐ KEY SETTING

#### 5.0.5.3 Procedure
1. Access: **APEX-NE EM >> VOD >> Session control configurations**
2. Verify settings:
   - Pre-encrypted Checking: **ENABLE** (mandatory for this test)
   - CTE Encryption: FULL
3. Configure source device to generate Broadcast Encrypted (Full) stream WITH CA_descriptor
4. Record source CA_descriptor details: CA_System_ID, ECM PID, other parameters
5. Unicast encrypted stream to Blade<1> Virtual IP
6. Verify stream routing in: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** (TS and Mappings table)
7. Monitor output via MPEG Tracker
8. **VERIFY CRITICAL BEHAVIOR:** Capture output CA_descriptor from PMT
9. Compare: Input CA_descriptor vs Output CA_descriptor (should be IDENTICAL)
10. Verify output ECM PID matches source ECM PID (same ECM stream)
11. Verify NO CTE CA_descriptor inserted (no re-encryption)
12. **STB Test 1:** Broadcast Authorized STB (has source CAS key)
    - Should be ABLE to decrypt and view stream
    - Uses source CA_descriptor to decrypt
13. **STB Test 2:** CTE Authorized STB (does NOT have source CAS key)
    - Should NOT be able to decrypt
    - Stream uses source's CA_descriptor, not CTE's
    - Result: Unable to view (NOT because of double encryption, but different CAS)
14. Verify stream quality/continuity unaffected
15. Move to Blade<2>; repeat steps 3-14
16. Continue for all 8 Blades

**Expected Results (Per Spec - PRE-ENCRYPTED CHECKING ENABLED):**
- Input with CA_descriptor detected as pre-encrypted
- **APEX-NE DOES NOT RE-ENCRYPT** the stream
- **SAME CA_descriptor copied to output PMT** (pass-through behavior)
- Source ECM PID preserved in output
- Broadcast Authorized STB can view (has source's CAS key)
- CTE Authorized STB cannot view (does not have source's CAS key, uses different CA_descriptor)
- No additional encryption layers added
- No CTE ECM inserted
- **Monitoring Points:** Input vs Output CA_descriptor comparison (MUST BE IDENTICAL), ECM PID preservation, CTE CA_descriptor absence verification, PMT structure analysis, STB authorization verification (different CAS systems)

**Critical Behavior Documented:**
When Pre-encrypted Checking = ENABLED:
- Input HAS CA_descriptor → Treated as pre-encrypted → PASS-THROUGH with SAME CA_descriptor
- Input NO CA_descriptor → Treated as clear → Encrypt normally and insert CTE CA_descriptor

---


1. Verify **PASS CRITERIA:** Pre-encrypted detection confirmed, **CA_descriptor IDENTICAL in output vs input**, No CTE CA_descriptor present, ECM PID preserved, Broadcast Auth viewing successful, CTE Auth viewing unsuccessful (due to different CAS, not double encryption), No re-encryption confirmed
1. Access: **APEX-NE EM >> VOD >> Session control configurations**
2. Verify settings:
   - Pre-encrypted Checking: **ENABLE** (mandatory for this test)
   - CTE Encryption: FULL
3. Configure source device to generate Broadcast Encrypted (Full) stream WITH CA_descriptor
4. Record source CA_descriptor details: CA_System_ID, ECM PID, other parameters
5. Unicast encrypted stream to Blade<1> Virtual IP
6. Verify stream routing in: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** (TS and Mappings table)
7. Monitor output via MPEG Tracker
8. **VERIFY CRITICAL BEHAVIOR:** Capture output CA_descriptor from PMT
9. Compare: Input CA_descriptor vs Output CA_descriptor (should be IDENTICAL)
10. Verify output ECM PID matches source ECM PID (same ECM stream)
11. Verify NO CTE CA_descriptor inserted (no re-encryption)
12. **STB Test 1:** Broadcast Authorized STB (has source CAS key)
    - Should be ABLE to decrypt and view stream
    - Uses source CA_descriptor to decrypt
13. **STB Test 2:** CTE Authorized STB (does NOT have source CAS key)
    - Should NOT be able to decrypt
    - Stream uses source's CA_descriptor, not CTE's
    - Result: Unable to view (NOT because of double encryption, but different CAS)
14. Verify stream quality/continuity unaffected
15. Move to Blade<2>; repeat steps 3-14
16. Continue for all 8 Blades

**Expected Results (Per Spec - PRE-ENCRYPTED CHECKING ENABLED):**
- Input with CA_descriptor detected as pre-encrypted
- **APEX-NE DOES NOT RE-ENCRYPT** the stream
- **SAME CA_descriptor copied to output PMT** (pass-through behavior)
- Source ECM PID preserved in output
- Broadcast Authorized STB can view (has source's CAS key)
- CTE Authorized STB cannot view (does not have source's CAS key, uses different CA_descriptor)
- No additional encryption layers added
- No CTE ECM inserted
- **Monitoring Points:** Input vs Output CA_descriptor comparison (MUST BE IDENTICAL), ECM PID preservation, CTE CA_descriptor absence verification, PMT structure analysis, STB authorization verification (different CAS systems)

**Critical Behavior Documented:**
When Pre-encrypted Checking = ENABLED:
- Input HAS CA_descriptor → Treated as pre-encrypted → PASS-THROUGH with SAME CA_descriptor
- Input NO CA_descriptor → Treated as clear → Encrypt normally and insert CTE CA_descriptor

---

### 5.0.6 Test Case: Pre-encrypted Stream Detection - FWK Input (ENABLED = PASS-THROUGH)
**Test ID:** TC_REL1.2.15-050_006  
**Severity:** HIGH  
#### 5.0.6.2 Objectives
**Objective:** Verify when Pre-encrypted Checking ENABLED: FWK input with CA_descriptor → Pass-through with same CA_descriptor

#### 5.0.6.1 Initial Condition
- Source device capable of generating FWK encrypted stream WITH CA_descriptor
- Pre-encrypted Checking = **ENABLED**
- CTE Encryption setting = FULL
- Input must have CA_descriptor to be treated as pre-encrypted

**Test Steps:**
1. Configure source device: Generate FWK encrypted stream WITH CA_descriptor
2. Record source CA_descriptor: CA_System_ID, ECM PID, parameters
3. Unicast FWK stream to Blade<1> Virtual IP
4. Verify stream detection: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** (TS and Mappings table - check pre-encrypted status)
5. Monitor output via MPEG Tracker
6. Capture output CA_descriptor from PMT
7. Verify output CA_descriptor = input CA_descriptor (IDENTICAL, not replaced)
8. Verify output ECM PID = source ECM PID
9. Verify NO CTE CA_descriptor inserted
10. **STB Test:** Broadcast Authorized STB (has source's CAS key)
    - Should be ABLE to view FWK stream
11. **STB Test:** CTE Authorized STB (does not have source's CAS key)
    - Should NOT be able to view (different CA_descriptor, different CAS)

#### 5.0.6.4 Expected Results
- FWK with CA_descriptor detected and passed through
- **Same CA_descriptor copied to output**
- Source ECM PID preserved
- No re-encryption applied
- Broadcast Auth working (source's CAS)
- CTE Auth not working (different CAS)
- Stream format preserved

**Key Difference vs TC_050_005:**
Only difference is stream type (FWK vs Full), behavior should be identical for pre-encrypted streams WITH CA_descriptor

---

### 5.0.7 Test Case: Pre-encrypted Checking DISABLED - CTE Re-encryption Applied
**Test ID:** TC_REL1.2.15-050_007  
**Severity:** CRITICAL  
#### 5.0.7.2 Objectives
**Objective:** Verify when Pre-encrypted Checking DISABLED: APEX-NE strips CA_descriptor, re-encrypts, and inserts CTE CA_descriptor

#### 5.0.7.1 Initial Condition
- Pre-encrypted stream available WITH CA_descriptor (Broadcast Encrypted Full)
- Pre-encrypted Checking = **DISABLED** ⭐ KEY SETTING
- CTE Encryption = FULL
- MPEG Tracker monitoring output

**Critical Behavior (Per Spec - PRE-ENCRYPTED CHECKING DISABLED):**
- APEX-NE SHALL STRIP OUT input CA_descriptor
- APEX-NE SHALL ENCRYPT NORMALLY (CTE encryption)
- APEX-NE SHALL INSERT NEW CA_descriptor (CTE's CA_descriptor)

**Test Steps:**
1. Access: **APEX-NE EM >> VOD >> Session control configurations**
2. Set Pre-encrypted Checking = **DISABLED**
3. Record source CA_descriptor (source's CA_System_ID, source's ECM PID)
4. Send Broadcast Encrypted (Full) stream WITH CA_descriptor to Blade<1> Virtual IP
5. Monitor output via MPEG Tracker
6. Capture output CA_descriptor and ECM PID
7. **VERIFY CRITICAL CHANGES:**
   - Input CA_descriptor: Source's CA_System_ID (e.g., 0x0FFF if Broadcast)
   - Output CA_descriptor: CTE's CA_System_ID (different value)
   - Input ECM PID: Source's ECM PID
   - Output ECM PID: CTE's ECM PID (different value)
8. Verify input CA_descriptor is **STRIPPED** (not in output)
9. Verify new CTE CA_descriptor is **INSERTED** in output
10. Verify CTE ECM stream present in output
11. Monitor stream encryption: Should be CTE encrypted (re-encrypted)
12. **STB Test 1:** Broadcast Authorized STB (has source's CAS key)
    - Should NOT be able to view (source's CA_descriptor removed, using CTE instead)
13. **STB Test 2:** CTE Authorized STB (has CTE's CAS key)
    - Should be ABLE to view (stream now encrypted with CTE CA_descriptor)

#### 5.0.7.4 Expected Results
- Input CA_descriptor STRIPPED (removed from output)
- New CTE CA_descriptor INSERTED
- ECM PID changed (source's ECM replaced with CTE's ECM)
- Stream re-encrypted with CTE encryption
- Broadcast Auth cannot view (source descriptor removed)
- CTE Auth can view (CTE descriptor applied)
- No source descriptor influence on output
- **Monitoring Points:** Input vs Output CA_descriptor comparison (MUST BE DIFFERENT), Input vs Output ECM PID comparison (MUST BE DIFFERENT), CA_descriptor replacement (not addition), ECM stream change, STB authorization outcome

**Critical Difference vs TC_050_005:**
- TC_050_005 (ENABLED): Input CA_descriptor → Output CA_descriptor (SAME, pass-through)
- TC_050_007 (DISABLED): Input CA_descriptor → Stripped → Output CTE CA_descriptor (DIFFERENT, re-encrypted)

---

### 5.0.8 Test Case: Clear Input with Pre-encrypted Checking ENABLED
**Test ID:** TC_REL1.2.15-050_008  
**Severity:** HIGH  
#### 5.0.8.2 Objectives
**Objective:** Verify when Pre-encrypted Checking ENABLED: Clear input (NO CA_descriptor) → Encrypt normally and insert CTE CA_descriptor

#### 5.0.8.1 Initial Condition
- Clear (unencrypted) VOD stream input
- Input has NO CA_descriptor
- Pre-encrypted Checking = **ENABLED**
- CTE Encryption = FULL

**Key Behavior (Per Spec - PRE-ENCRYPTED CHECKING ENABLED, INPUT = CLEAR):**
- Input without CA_descriptor → Treated as CLEAR content
- APEX-NE SHALL ENCRYPT NORMALLY
- APEX-NE SHALL INSERT CTE CA_descriptor

**Test Steps:**
1. Access: **APEX-NE EM >> VOD >> Session control configurations**
2. Verify: Pre-encrypted Checking = ENABLED
3. Send CLEAR (unencrypted) stream to Blade<1> Virtual IP
4. Verify stream has NO CA_descriptor in input
5. Monitor output via MPEG Tracker
6. Verify output has CTE CA_descriptor
7. Verify output has CTE ECM PID (new ECM inserted)
8. Verify output is CTE encrypted
9. **STB Test:** Broadcast Authorized STB
    - Should NOT be able to view (stream encrypted with CTE, not Broadcast's CA)
10. **STB Test:** CTE Authorized STB
    - Should be ABLE to view (encrypted with CTE's CA_descriptor)

#### 5.0.8.4 Expected Results
- Clear input (no CA_descriptor) encrypted with CTE
- CTE CA_descriptor inserted in output
- CTE ECM stream present
- Broadcast Auth cannot view
- CTE Auth can view
- Stream encrypted normally (per CTE settings)

### 5.0.9 Test Case: Mixed Inputs - Pre-encrypted (CA) + Clear (No CA)
**Test ID:** TC_REL1.2.15-050_009  
**Severity:** MEDIUM  
#### 5.0.9.2 Objectives
**Objective:** Verify Pre-encrypted Checking ENABLED handles mixed inputs correctly on same Blade

#### 5.0.9.1 Initial Condition
- Pre-encrypted Checking = **ENABLED**
- Multiple stream inputs to same Blade
- Stream 1: Pre-encrypted WITH CA_descriptor (Broadcast Encrypted Full)
- Stream 2: Clear WITHOUT CA_descriptor
- CTE Encryption = FULL

**Test Steps:**
1. Configure Blade<1> with Pre-encrypted Checking = ENABLED
2. **Stream 1:** Send pre-encrypted WITH CA_descriptor to Virtual IP
3. **Stream 2:** Send clear WITHOUT CA_descriptor to Virtual IP
4. Verify both streams routing: **APEX3K-NE EM >> Blades >> Select Blade<1> >> Gateway VOD Status** (TS and Mappings table)
5. Monitor output via MPEG Tracker for Stream 1
   - Verify: Source CA_descriptor preserved (SAME CA_descriptor in output)
   - Verify: Source ECM PID preserved
6. Monitor output via MPEG Tracker for Stream 2
   - Verify: CTE CA_descriptor inserted (new CA_descriptor)
   - Verify: CTE ECM PID inserted (new ECM)
7. **STB Tests for Stream 1:**
   - Broadcast Auth: Can view (source's CA_descriptor)
   - CTE Auth: Cannot view (using source's CA_descriptor, not CTE's)
8. **STB Tests for Stream 2:**
   - Broadcast Auth: Cannot view (encrypted with CTE)
   - CTE Auth: Can view (CTE encrypted)
9. Verify no cross-stream interference

#### 5.0.9.4 Expected Results
- Stream 1 (pre-encrypted with CA): Passed through with SAME CA_descriptor
- Stream 2 (clear, no CA): Encrypted with CTE, NEW CA_descriptor inserted
- Each handled per its content type
- No interference between streams
- Authorization correct for each type

**Key Behavior Verified:**
- Input WITH CA_descriptor → Pre-encrypted → Pass-through (SAME CA_descriptor)
- Input WITHOUT CA_descriptor → Clear → Encrypt and insert (NEW CTE CA_descriptor)

---

### 5.0.10 Test Case: Configuration Precedence - Pre-encrypted Checking Effects
**Test ID:** TC_REL1.2.15-050_010  
**Severity:** CRITICAL  
#### 5.0.10.2 Objectives
**Objective:** Verify Pre-encrypted Checking setting determines stream handling (CA_descriptor preservation vs replacement)

#### 5.0.10.1 Initial Condition
- Pre-encrypted stream WITH CA_descriptor available
- MPEG Tracker monitoring output
- Ability to change Pre-encrypted Checking setting

**Key Specification:**
| Setting | Input with CA_descriptor | Result |
| --- | --- | --- |
| ENABLED | Pre-encrypted (has CA_descriptor) | PASS-THROUGH: Same CA_descriptor to output |
| DISABLED | Any input | RE-ENCRYPT: Strip CA_descriptor, insert CTE CA_descriptor |

**Test Steps:**
1. Access: **APEX-NE EM >> VOD >> Session control configurations**
2. Set Pre-encrypted Checking = **ENABLED**
3. Send pre-encrypted stream WITH CA_descriptor to Blade<1>
4. Capture output CA_descriptor: Should match input (pass-through)
5. Capture output ECM PID: Should match input ECM
6. Now change: Pre-encrypted Checking = **DISABLED**
7. Send SAME pre-encrypted stream to Blade<2>
8. Capture output CA_descriptor: Should NOT match input (replaced with CTE)
9. Capture output ECM PID: Should NOT match input ECM (new CTE ECM)
10. Compare Blade<1> vs Blade<2> outputs
11. Verify different CA_descriptor handling based on setting

#### 5.0.10.4 Expected Results
- Blade<1> (ENABLED): Input CA_descriptor preserved in output
- Blade<2> (DISABLED): Input CA_descriptor stripped, replaced with CTE CA_descriptor
- Same input stream handled differently based on configuration
- Setting directly controls CA_descriptor preservation behavior

**Critical Documentation:**
Per APEX NE Specification:
- **Pre-encrypted Checking ENABLED:** Input with CA_descriptor → PASS-THROUGH same CA_descriptor
- **Pre-encrypted Checking DISABLED:** Input → STRIP CA_descriptor → INSERT CTE CA_descriptor


---

## 6.0 REL1.2.15-060: Encryption Status Display

### 6.0.1 Test Case: Element Manager Encryption Status Display - GVOD Status Table (APEX3K-NE)
**Test ID:** TC_REL1.2.15-060_001  
**Severity:** HIGH  
#### 6.0.1.2 Objectives
**Objective:** Verify encryption status and mapping details displayed in GVOD Status table

#### 6.0.1.1 Initial Condition
- APEX-NE EM interface accessible
- Multiple GVOD mappings with encryption active
- Gateway VOD configured on Blade<1>
- MediaCipher SimulCrypt enabled

**Test Steps:**
1. Navigate to: **APEX3K-NE EM >> Blades >> Select Blade<1> >> GVOD status**
2. Verify GVOD status table displays all GVOD TS entries
3. Verify table columns include mapping details
4. Check for "Encryption Status" column or property in table
5. Verify each GVOD TS mapping shows encryption status
6. Status options should include:
   - Encrypted (MediaCipher)
   - Pre-encrypted
   - Not Encrypted
   - Error
7. Review all table entries for accuracy
8. Create new GVOD mapping and verify status updates in table in real-time
9. Disable MediaCipher Simulcrypt at blade level and verify status changes
10. Verify MPEG Tracker analysis matches displayed encryption status

#### 6.0.1.4 Expected Results
- GVOD status table displays all GVOD TS entries
- Encryption status shown for each mapping
- Table includes complete mapping details
- Status accurately reflects actual encryption state
- Updates in real-time as configuration changes
- All GVOD TS consolidated in single table view

### 6.0.2 Test Case: Encryption Status Detail - CAS Systems
**Test ID:** TC_REL1.2.15-060_002  
**Severity:** MEDIUM  
#### 6.0.2.2 Objectives
**Objective:** Verify detailed status showing which CAS systems active

#### 6.0.2.1 Initial Condition
- Mapping with multiple CAS configured (MediaCipher + SuperCAS)
- APEX-NE EM Mappings view accessible

**Test Steps:**
1. Display mapping details in APEX-NE EM
2. Verify encryption status shown
3. Click for detailed status/information
4. Verify detailed view shows:
   - MediaCipher ✓ (active)
   - SuperCAS 1 ✓ (if configured)
   - SuperCAS 2 ✓ (if configured)
   - SuperCAS 3 ✓ (if configured)
5. Test with different CAS configurations
6. Verify detail level comprehensive

#### 6.0.2.4 Expected Results
- Detailed status accessible
- CAS systems listed individually
- Detailed information comprehensive
- Matches actual configuration

### 6.0.3 Test Case: Bulk Status Display and Filtering
**Test ID:** TC_REL1.2.15-060_003  
**Severity:** MEDIUM  
#### 6.0.3.2 Objectives
**Objective:** Verify Element Manager handles large mapping sets efficiently

#### 6.0.3.1 Initial Condition
- 1,000+ mappings configured
- Various encryption states

**Test Steps:**
1. Navigate to: **Blade >> Select Blade<1> >> Gateway VOD >> Mappings**
2. Load full list of 1,000+ mappings
3. Verify performance (target: < 5 sec load time)
4. Test filtering options:
   - Filter by: Encrypted
   - Filter by: Not Encrypted
   - Filter by: Pre-encrypted
5. Verify filter results accurate
6. Test bulk status operations
7. Verify pagination if applicable

#### 6.0.3.4 Expected Results
- All mappings displayed
- Performance acceptable (< 5 sec)
- Filtering functional and accurate
- Bulk operations work


---

## 7.0 REL1.2.15-070: SDM Plug-in & MIB

### 7.0.1 Test Case: SDM Plug-in Configuration Support
**Test ID:** TC_REL1.2.15-070_001  
**Severity:** HIGH  
#### 7.0.1.2 Objectives
**Objective:** Verify SDM plug-in supports MediaCipher SimulCrypt configuration

#### 7.0.1.1 Initial Condition
- SDM (Service Delivery Manager) environment available
- SDM plug-in for APEX3K-NE installed
- SDM interface functional

**Test Steps:**
1. Access SDM interface
2. Navigate to Gateway VOD configuration module
3. Verify MediaCipher SimulCrypt option present
4. Configure SimulCrypt globally
5. Configure at blade level
6. Configure external SuperCAS (up to 3)
7. Verify configuration persists

#### 7.0.1.4 Expected Results
- SDM displays all configuration options
- All options functional through SDM
- Configuration saved and persistent
- Changes propagate to APEX3K-NE

### 7.0.2 Test Case: MIB File Updates - Gateway VOD MC Simulcrypt Parameter
**Test ID:** TC_REL1.2.15-070_002  
**Severity:** HIGH  
#### 7.0.2.2 Objectives
**Objective:** Verify MIB files contain Gateway VOD MC Simulcrypt parameter with per-blade configuration

#### 7.0.2.1 Initial Condition
- Build package with updated MIB files
- config.ini file accessible
- SNMP monitoring tools available (optional for full verification)
- MIB files installed on APEX3K-NE

**Test Steps:**
1. Locate build package files
2. Find and open **config.ini** file
3. Search for parameter: **"Gateway VOD MC simulcrypt"**
4. Verify parameter exists in MIB
5. Verify parameter definition includes:
   - Name: Gateway VOD MC simulcrypt
   - Scope: Per-blade configuration
   - Values: ENABLE (1) / DISABLE (0)
6. Verify MIB structure supports per-blade:
   - Blade<1> MC Simulcrypt value
   - Blade<2> MC Simulcrypt value
   - Up to 8 blades (if applicable)
7. Load MIB in SNMP browser tool (optional)
8. Query SNMP for Gateway VOD MC simulcrypt parameter
9. Verify SNMP OID resolves correctly
10. Test SNMP set operation (if writable):
    - Set Gateway VOD MC simulcrypt = ENABLE
    - Verify reflected in APEX3K-NE EM
    - Set Gateway VOD MC simulcrypt = DISABLE
    - Verify reflected in APEX3K-NE EM

#### 7.0.2.4 Expected Results
- Gateway VOD MC simulcrypt parameter found in MIB
- Parameter documented with correct name
- Per-blade configuration supported in MIB
- ENABLE/DISABLE values defined
- config.ini file contains parameter definition
- SNMP queries functional (if applicable)
- SNMP set operations reflect correctly in EM

### 7.0.3 Test Case: SDM Upgrade - Release 1.2.14-00 to 1.2.15-00
**Test ID:** TC_REL1.2.15-070_003  
**Severity:** CRITICAL  
#### 7.0.3.2 Objectives
**Objective:** Verify APEX3K-NE upgrade from 1.2.14-00 to 1.2.15-00 via SDM includes all new features

#### 7.0.3.1 Initial Condition
- APEX3K-NE running release 1.2.14-00
- SDM device available for upgrade
- Current configuration backed up
- Scheduled maintenance window
- No active traffic (or traffic transferred to backup)

**Test Steps - Pre-Upgrade:**
1. Document current APEX3K-NE version: Should show **1.2.14-00**
2. Navigate to: **APEX3K-NE EM >> About >> System Info**
3. Document current configuration details
4. Back up all configuration files
5. Verify Gateway VOD MC Simulcrypt NOT present in current version

**Test Steps - Upgrade Process:**
1. Access SDM device
2. Initiate APEX3K-NE upgrade process
3. Select target version: **1.2.15-00**
4. Confirm source version: **1.2.14-00**
5. Accept license terms (if applicable)
6. Start upgrade (typically via TFTP or USB)
7. Monitor upgrade progress:
   - Download phase
   - Installation phase
   - Configuration migration phase
   - Reboot phase
8. Expected duration: 15-45 minutes
9. Wait for APEX3K-NE to reboot and stabilize

**Test Steps - Post-Upgrade Verification:**
1. Wait for APEX3K-NE fully operational (5-10 min)
2. Access APEX3K-NE EM
3. Navigate to: **APEX3K-NE EM >> About >> System Info**
4. Verify version shows: **1.2.15-00**
5. Verify configuration persisted after upgrade

**Test Steps - New Feature Verification:**
1. Verify Gateway VOD MC Simulcrypt parameter present:
   - Navigate to: **APEX3K-NE >> Blade >> Select Blade<1>**
   - Verify **Gateway VOD MC Simulcrypt** option visible
2. Verify Simulcrypt configuration options work:
   - Enable Simulcrypt at blade level
   - Configure ECMG server
   - Configure CAS systems
   - Create test GVOD mapping
3. Verify CTE configuration functional:
   - Navigate to: **Chassis >> VOD >> CTE configuration**
   - Verify CTE settings accessible
4. Verify GVOD Status display:
   - Navigate to: **Blades >> Select Blade<1> >> GVOD status**
   - Verify status table displays correctly
5. Verify Pre-encrypted Checking functionality:
   - Navigate to: **VOD >> Session control configurations**
   - Verify Follow DTCP Descriptor option
   - Verify Pre-encrypted Checking option
6. Verify MIB files updated:
   - Check for Gateway VOD MC simulcrypt in config.ini
   - Verify SNMP OID available (if applicable)

**Test Steps - Functionality Testing:**
1. Create test Gateway VOD stream:
   - Configure Virtual IP on Blade<1>
   - Enable Gateway VOD
   - Enable MediaCipher Simulcrypt
   - Configure ECMG server
2. Send test stream via M3-Server to Virtual IP
3. Verify output on MPEG Tracker:
   - ECM insertion correct
   - PMT updated with CA descriptors
   - Encryption applied per CTE configuration
4. Test with pre-encrypted input:
   - Enable Pre-encrypted Checking
   - Send pre-encrypted stream
   - Verify pass-through behavior
5. Test CAS configuration:
   - Configure external SuperCAS
   - Verify ECM insertion for all CAS
6. Monitor system stability:
   - No error logs after upgrade
   - Performance nominal
   - Resource utilization normal

#### 7.0.3.4 Expected Results
- Upgrade completes successfully
- Version shows 1.2.15-00 after upgrade
- All configuration persisted
- Gateway VOD MC Simulcrypt parameter present
- All new features (Simulcrypt, CTE, Pre-encrypted) functional
- MPEG Tracker analysis shows correct encryption
- MIB files updated with new parameter
- System stable with nominal performance
- No functionality regression from 1.2.14-00

#### 7.0.3.4 Expected Results
- MIB file properly loaded
- All new objects accessible
- SNMP queries return valid data
- Data matches system state


---

## 8.0 REL1.2.15-080: Aurora Networks Branding

### 8.0.1 Test Case: Aurora Networks Logo Consistency - Persistent Display Across Screens
**Test ID:** TC_REL1.2.15-080_001  
**Severity:** MEDIUM  
#### 8.0.1.2 Objectives
**Objective:** Verify Aurora Networks logo displays consistently and persistently across all APEX-NE EM screens

#### 8.0.1.1 Initial Condition
- APEX-NE EM interface accessible
- Administrator authenticated
- Aurora Networks branding guidelines available (if applicable)

**Test Steps:**
1. Access APEX-NE EM main home screen
2. Locate Aurora Networks logo on screen
3. Document logo position, size, and appearance
4. Verify logo clearly visible and professional
5. Navigate to: **Simulcrypt >> General**
6. Verify Aurora Networks logo still present on screen
7. Verify logo position/appearance UNCHANGED (consistent)
8. Navigate to: **Blades >> Select Blade<1>**
9. Verify Aurora Networks logo still present
10. Verify logo position/appearance UNCHANGED
11. Navigate to: **Chassis >> VOD >> CTE configuration**
12. Verify Aurora Networks logo still present
13. Verify logo position/appearance UNCHANGED
14. Navigate to: **VOD >> Session control configurations**
15. Verify Aurora Networks logo still present
16. Verify logo position/appearance UNCHANGED
17. Navigate to: **Blades >> Select Blade<1> >> GVOD status**
18. Verify Aurora Networks logo still present
19. Verify logo position/appearance UNCHANGED
20. Navigate to: **About** section
21. Verify Aurora Networks logo present
22. Verify logo position/appearance UNCHANGED
23. Verify no legacy company logos visible
24. Document all screens with logo verification

#### 8.0.1.4 Expected Results
- Aurora Networks logo visible on every screen
- Logo appearance consistent across all navigation
- Logo position unchanged while navigating
- Professional presentation maintained
- No legacy branding visible
- Logo clearly associated with product
- Branding consistent throughout application

### 8.0.2 Test Case: Patent URL Verification - www.an-pat.com in About Section
**Test ID:** TC_REL1.2.15-080_002  
**Severity:** MEDIUM  
#### 8.0.2.2 Objectives
**Objective:** Verify Aurora Networks patent URL (www.an-pat.com) correctly displayed in About section and functional

#### 8.0.2.1 Initial Condition
- APEX-NE EM About section accessible
- Web browser available for URL testing
- Network connectivity to external websites available
- Patient URL: www.an-pat.com should be live

**Test Steps:**
1. Access APEX-NE EM main interface
2. Navigate to: **APEX3K-NE EM >> About** (typically in top menu or help section)
3. Locate patent information section
4. Verify patent link/reference visible
5. Document exact URL text displayed: Should show **www.an-pat.com**
6. Verify URL is formatted as hyperlink or clearly marked as clickable
7. Click on patent URL/link
8. Verify browser window/tab opens
9. Verify URL address bar shows: **www.an-pat.com** (or https://www.an-pat.com)
10. Wait for page to load completely (target: < 5 seconds)
11. Verify Aurora Networks patent website loads successfully
12. Verify page contains patent information related to Aurora Networks
13. Verify page displays correctly (no 404 errors, broken links, etc.)
14. Document patent page content/title
15. Verify professional presentation
16. Close browser window and return to APEX-NE EM
17. Verify About section still displays correctly
18. Test URL multiple times to ensure consistency

#### 8.0.2.4 Expected Results
- Patent URL clearly displayed in About section
- URL text shows: www.an-pat.com
- Patent link is functional and clickable
- Browser opens and loads page correctly
- Aurora Networks patent website accessible
- Page content loads completely
- No 404 errors or broken links
- Professional presentation
- URL consistent on multiple tests
- No redirects to incorrect pages

**Document Version:** 2.0 (APEX3K-NE Updated)  
**Platform:** APEX3K-NE Network Element  
**Total Test Cases:** 50+  
**Created:** 2026-11-04  
**Reference:** Inputs_to_github-copilot.docx




