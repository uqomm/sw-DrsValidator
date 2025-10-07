# Technical Questions: Digital Cards Connectivity VHF, P25 and LC500

## System Context

### Architecture
```mermaid
flowchart TD
    A["Validation Software<br/>(Ours)"]

    subgraph "Independent Systems per Band"
        B1["Master Digital Board<br/>(VHF)"]
        B2["Master Digital Board<br/>(P25)"]
        B3["Master Digital Board<br/>(LC500)"]

        C1["Remote Digital Board<br/>(VHF)"]
        C2["Remote Digital Board<br/>(P25)"]
        C3["Remote Digital Board<br/>(LC500)"]

        D1["LNA / PA<br/>(VHF)"]
        D2["LNA / PA<br/>(P25)"]
        D3["LNA / PA<br/>(LC500)"]
    end

    A -.->|"TCP/IP Port 65050"| B1
    A -.->|"TCP/IP Port 65050"| B2
    A -.->|"TCP/IP Port 65050"| B3

    B1 -.->|"Optical Fiber"| C1
    B2 -.->|"Optical Fiber"| C2
    B3 -.->|"Optical Fiber"| C3

    C1 -.->|"DB9↔IDC-10pin JP1"| D1
    C2 -.->|"DB9↔IDC-10pin JP1"| D2
    C3 -.->|"DB9↔IDC-10pin JP1"| D3

    style A fill:#e1f5fe,color:#000
    style B1 fill:#e8f5e8,color:#000
    style B2 fill:#e8f5e8,color:#000
    style B3 fill:#ffebee,color:#000
    style C1 fill:#e8f5e8,color:#000
    style C2 fill:#e8f5e8,color:#000
    style C3 fill:#ffebee,color:#000
    style D1 fill:#fff3e0,color:#000
    style D2 fill:#fff3e0,color:#000
    style D3 fill:#ffebee,color:#000

    classDef working stroke:#4caf50,stroke-width:2px,color:#000
    classDef problem stroke:#f44336,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    class B1,C1 working
    class B2,C2 working
    class B3,C3,D3 problem
```

**NOTE**: Each band (VHF, P25, LC500) has its own Master Digital Board and operates as an independent system

### Software Versions
- **VHF**: 231016-BB1-145-15M-16C-OP8 ✅ TCP Compatible
- **P25**: 231115-BB1-806D851M-18M-16C-OP8 ✅ TCP Compatible
- **LC500**: FPGA:250529-16A, Software:250530-05, Kernel:210909 ❌ TCP Not Compatible

### LNA/PA Components
- **Connection**: JP1 port pins 5,7 via DB9↔IDC-10pin cable
- **Problem**: Remote native software does NOT read LNA/PA parameters
- **Objective**: Integrated monitoring via TCP/IP

---

## Technical Questions

### 1. LNA/PA Monitoring

**Problem Architecture:**
```mermaid
flowchart TD
    A["Validation Software<br/>(Ours)"]
    B["Master Digital Board<br/>(VHF/P25)"]
    C["Remote Digital Board<br/>(VHF/P25)"]
    D["LNA / PA"]

    A -.->|"TCP/IP<br/>Port 65050"| B
    B -.->|"Optical Fiber"| C
    C -.->|"DB9↔IDC-10pin Cable<br/>JP1 Port (pins 5,7)"| D

    style A fill:#e1f5fe,color:#000
    style B fill:#f3e5f5,color:#000
    style C fill:#fff3e0,color:#000
    style D fill:#ffebee,color:#000

    classDef problem stroke:#f44336,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    class D problem
```

**PROBLEM**: Remote native software does NOT read LNA/PA parameters
**OBJECTIVE**: Integrated monitoring via TCP/IP

**Questions:**
- Are there specific commands in "Protocol _TT_2023_8_30.pdf" for LNA and PA?
- Can port 65050 be used to monitor LNA/PA?
- Why doesn't the remote native software read LNA parameters via DB9-IDC 10pin?
- Is it possible to transport LNA/PA commands through: Master → Fiber → Remote → TCP/IP?
- Is special configuration required in master/remote to enable LNA/PA communication?
- Do the VHF/P25 .rar files include monitoring commands for LNA/PA?

### 2. LC500 Compatibility

**Problem Architecture:**
```mermaid
flowchart TD
    A["Validation Software<br/>(Ours)"]
    B["Master Digital Board<br/>(LC500)"]
    C["Remote Digital Board<br/>(LC500)"]

    A -.->|"TCP/IP Port 65050<br/>❌ Not Compatible"| B
    B -.->|"Optical Fiber"| C

    style A fill:#e1f5fe,color:#000
    style B fill:#ffebee,color:#000
    style C fill:#ffebee,color:#000

    classDef incompatible stroke:#f44336,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    class B,C incompatible
```

**PROBLEM**: LC500 does not support TCP protocol Port 65050
**OBJECTIVE**: Make LC500 compatible with monitoring system

**Questions:**
- Does LC500 support the same TCP commands as VHF/P25 via optical fiber?
- Is it compatible with port 65050 in master digital board?
- What modifications does LC500 require for TCP compatibility?
- Does LC500 need to be updated to versions compatible with VHF/P25?

### 3. Standardization

**Versions Architecture:**
```mermaid
flowchart TD
    A["Validation Software<br/>(Unified System)"]

    subgraph "Current Versions"
        V1["VHF<br/>231016-BB1-145-15M-16C-OP8<br/>✅ Working"]
        V2["P25<br/>231115-BB1-806D851M-18M-16C-OP8<br/>✅ Working"]
        V3["LC500<br/>FPGA: 250529-16A<br/>Software: 250530-05<br/>Kernel: 210909<br/>❌ Not Compatible"]
    end

    subgraph "Objective: Unified Versions"
        U1["VHF Standardized<br/>Compatible Version"]
        U2["P25 Standardized<br/>Compatible Version"]
        U3["LC500 Updated<br/>Compatible Version"]
    end

    A -.-> V1
    A -.-> V2
    A -.-> V3

    V1 --> U1
    V2 --> U2
    V3 --> U3

    style A fill:#e1f5fe,color:#000
    style V1 fill:#e8f5e8,color:#000
    style V2 fill:#e8f5e8,color:#000
    style V3 fill:#ffebee,color:#000
    style U1 fill:#f0f4c3,color:#000
    style U2 fill:#f0f4c3,color:#000
    style U3 fill:#f0f4c3,color:#000

    classDef working stroke:#4caf50,stroke-width:2px,color:#000
    classDef broken stroke:#f44336,stroke-width:2px,color:#000
    classDef target stroke:#ff9800,stroke-width:2px,stroke-dasharray: 3 3,color:#000
    class V1,V2 working
    class V3 broken
    class U1,U2,U3 target
```

**PROBLEM**: Different versions complicate maintenance and compatibility
**OBJECTIVE**: Standardize versions for unified monitoring

**Questions:**
- Is it possible to use the same VHF/P25 versions on all cards?
- Would this improve TCP monitoring compatibility?
- Are there technical implications in standardizing versions?

## Required Monitoring Commands (13 TCP commands)
- `temperature` (0x02), `device_id` (0x97), `datt` (0x09)
- `input_and_output_power` (0xF3), `channel_switch` (0x42)
- `channel_frequency_configuration` (0x36), `central_frequency_point` (0xEB)
- `subband_bandwidth` (0xED), `broadband_switching` (0x81)
- `optical_port_switch` (0x91), `optical_port_status` (0x9A)
- `optical_port_devices_connected_1` (0xF8), `optical_port_devices_connected_2` (0xF9)

## Reference Files
- `Protocol _TT_2023_8_30.pdf` ✅ Main protocol (works)
- `Santone module monitor protocol_2023_8_15.pdf` ❌ Doesn't work
- `VHF - 231016-BB1-145-15M-16C-OP8.rar`, `P25 - 231115-BB1-806D851M-18M-16C-OP8.rar`
- `LNA_VHF_Technical Specification (1).pdf`

---
*Version: 2.2 - Mermaid diagrams per question*</content>
<parameter name="filePath">/home/arturo/sw-drsmonitoring/validation-framework/docs/preguntas_conectividad_tarjetas_digitales.md