# 🛡️ FakeShield: System Architecture & DFD Documentation

This document provides a comprehensive analysis of the **FakeShield AI Forensic Laboratory** architecture. It details the **Level 1 Data Flow Diagram (DFD)** and zooms in on the **Level 2 Data Flow Diagram (DFD)** for the **AI Image Forensic Lab (Process 3.0)**.

---

## 📂 Overview of Data Flow Diagrams (DFDs)

A **Data Flow Diagram (DFD)** maps out the flow of information for any process or system. It uses standardized symbols to represent:
*   **External Entities (Square / Rectangle):** Sources or destinations of data outside the system's boundary.
*   **Processes (Circle / Rounded Rectangle):** Processing units that transform input data flows into output data flows.
*   **Data Stores (Open-ended Rectangle / Parallel Lines):** Locations where data is stored.
*   **Data Flows (Arrows):** Directed paths showing the movement of data.

---

## 🔄 Core Architectural & Access Control Rules

The DFD is designed to enforce the two main technical characteristics of your platform:

### 1. Unified Database Store (MongoDB)
All persistent data in FakeShield is stored within a single logical **MongoDB Database**. It is segmented into the following collection stores:
*   `users`: Stores usernames, password hashes, and subscription status (`free` or `paid`).
*   `text_forensics`: Stores text scan logs and detailed model outputs.
*   `image_forensics`: Stores image metadata audits, Grad-CAM overlays, and ELA records.
*   `audio_forensics`: Stores voice cloning results, spectrograms, and pitch metrics.
*   `video_forensics`: Stores frame-by-frame landmark tracking and consistency telemetry.

### 2. Tiered Access Permissions
*   **AI Text Lab (Process 2.0):** Open to **both Free and Paid/Subscription tiers**. Users only need to register and log in to scan text.
*   **AI Image Lab (Process 3.0), AI Audio Lab (Process 4.0), and AI Video Lab (Process 5.0):** Restricted to **Paid/Subscription tier accounts**. Free users are blocked with a `403 Forbidden` error. They must use the Upgrade Handler (Process 8.0) to gain access.

---

## 🎨 Level 1 DFD: System Overview

The Level 1 DFD displays the macro-level subsystems of FakeShield, showing how data streams between user inputs, the security routers, the background status tracker, and the backend MongoDB database.

```mermaid
graph TD
    %% Define Styles and Shapes for DFD Standards
    classDef entity fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#fff;
    classDef process fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef datastore fill:#18181b,stroke:#a1a1aa,stroke-width:2px,color:#fff;

    %% External Entities (Rectangles)
    User["👤 External Entity: User / Client (React UI)"]:::entity
    SMTP["📨 External Entity: SMTP Mail Server"]:::entity
    OAuth["🔑 External Entity: OAuth Provider (Google/GitHub)"]:::entity

    %% Process Nodes (Rounded Rectangles / Circles)
    P1["⚙️ Process 1.0:<br/>Authentication & Profile Manager"]:::process
    P2["⚙️ Process 2.0:<br/>AI Text Lab (Free Tier Access)"]:::process
    P3["⚙️ Process 3.0:<br/>AI Image Lab (Subscription Plan Only)"]:::process
    P4["⚙️ Process 4.0:<br/>AI Audio Lab (Subscription Plan Only)"]:::process
    P5["⚙️ Process 5.0:<br/>AI Video Lab (Subscription Plan Only)"]:::process
    P6["⚙️ Process 6.0:<br/>Forensic PDF Report Builder"]:::process
    P7["⚙️ Process 7.0:<br/>Dashboard & Analytics Aggregator"]:::process
    P8["⚙️ Process 8.0:<br/>Subscription & Payment Upgrade Handler"]:::process

    %% Unified MongoDB Data Store (Parallel Lines / Cylinders)
    subgraph D1["💾 Data Store 1.0: Unified MongoDB Database"]
        D1a["D1.1: Users Collection"]:::datastore
        D1b["D1.2: Text Forensics Collection"]:::datastore
        D1c["D1.3: Image Forensics Collection"]:::datastore
        D1d["D1.4: Audio Forensics Collection"]:::datastore
        D1e["D1.5: Video Forensics Collection"]:::datastore
    end
    
    %% In-Memory Cache for Status Tracking
    D6["💾 Data Store 2.0:<br/>In-Memory Job Cache (RAM)"]:::datastore

    %% -------------------------------------------------------------
    %% Data Flows
    %% -------------------------------------------------------------

    %% Authentication flows
    User -->|Local credentials / Signup info| P1
    User -->|OAuth Sign In Trigger| P1
    P1 <-->|OAuth Verification token exchange| OAuth
    P1 -->|Issue JWT session token & profile details| User
    P1 <-->|Read / Write user profile parameters| D1a

    %% Billing & Upgrade flows
    User -->|QR payment code & Upgrade request| P8
    P8 -->|Upgrade status / tier confirmation| User
    P8 -->|Update user status to subscription_tier=paid| D1a

    %% Text Lab (Free Tier Flow)
    User -->|Submit Text & JWT token (Free or Paid)| P2
    P2 -->|Acknowledge request & return Job ID| User
    P2 -->|Initialize job status| D6
    P2 -->|Background Worker runs models| P2
    P2 -->|Update job status to complete & write results| D6
    User -->|Poll status (Job ID, JWT)| P2
    D6 -->|Read current job status & outputs| P2
    P2 -->|Return Text Analysis details| User
    P2 -->|Persist text scan outputs| D1b
    P2 -->|Dispatch warning email when threat=CRITICAL| SMTP

    %% Image Lab (Subscription Plan Flow)
    User -->|Submit Base64 Image, Grad-CAM request, JWT token| P3
    P3 -->|Validate Subscription Status| P3
    D1a -->|Verify tier is paid| P3
    P3 -->|Synchronous ELA, spectral analysis & DINOv2 metrics| P3
    P3 -->|Persist image scan metrics| D1c
    P3 -->|Return Image forensics split maps & scores (if paid)| User

    %% Audio Lab (Subscription Plan Flow)
    User -->|Submit Audio WAV/MP3 file, JWT token| P4
    P4 -->|Validate Subscription Status| P4
    D1a -->|Verify tier is paid| P4
    P4 -->|Acknowledge request & return Job ID (if paid)| User
    P4 -->|Initialize job status| D6
    P4 -->|Background Worker runs WavLM & AST| P4
    P4 -->|Update job status to complete & write results| D6
    User -->|Poll status (Job ID, JWT)| P4
    D6 -->|Read current job status & outputs| P4
    P4 -->|Return Audio analysis metrics| User
    P4 -->|Persist audio scan metrics| D1d

    %% Video Lab (Subscription Plan Flow)
    User -->|Submit Video MP4 file, JWT token| P5
    P5 -->|Validate Subscription Status| P5
    D1a -->|Verify tier is paid| P5
    P5 -->|Acknowledge request & return Job ID (if paid)| User
    P5 -->|Initialize job status| D6
    P5 -->|Background Worker checks landmark consistency| P5
    P5 -->|Update job status to complete & write results| D6
    User -->|Poll status (Job ID, JWT)| P5
    D6 -->|Read current job status & outputs| P5
    P5 -->|Return Video consistency metrics| User
    P5 -->|Persist video scan metrics| D1e

    %% PDF Report Builder flows
    User -->|Request report download (Scan ID + JWT)| P6
    P6 -->|Downloadable PDF binary stream| User
    D1b -->|Fetch text results| P6
    D1c -->|Fetch image results| P6
    D1d -->|Fetch audio results| P6
    D1e -->|Fetch video results| P6

    %% Dashboard and Stats flows
    User -->|Request dashboard overview & statistics| P7
    P7 -->|Aggregated scan counts, history logs| User
    D1a -->|Verify user's billing/tier metadata| P7
    D1b -->|Query text scans list| P7
    D1c -->|Query image scans list| P7
    D1d -->|Query audio scans list| P7
    D1e -->|Query video scans list| P7
```

---

## 🔬 Level 2 DFD: AI Image Forensic Lab (Process 3.0)

A **Level 2 DFD** zooms in on a specific Level 1 Process to map out its internal steps. The diagram below details the inner workings of the **AI Image Forensic Lab (Process 3.0)**, demonstrating how base64 inputs are sanitized, evaluated for quick-veto watermarks, processed through a thread pool, and combined into a final confidence-weighted decision.

```mermaid
graph TD
    %% Define Styles
    classDef entity fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#fff;
    classDef process fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef datastore fill:#18181b,stroke:#a1a1aa,stroke-width:2px,color:#fff;

    %% External Entity
    User["👤 External Entity: User / Client (React UI)"]:::entity

    %% Sub-processes of Process 3.0
    P31["⚙️ Process 3.1:<br/>Base64 Decoder & Format Sanitizer"]:::process
    P32["⚙️ Process 3.2:<br/>Watermark & C2PA Metadata Auditor<br/>(Fast Short-Circuit Checks)"]:::process
    P33["⚙️ Process 3.3:<br/>Forensic Signal Extraction Pipeline<br/>(Parallel Thread Pool)"]:::process
    P34["⚙️ Process 3.4:<br/>Confidence-Weighted Fusion Engine<br/>(Veto Rules & Decision Logic)"]:::process
    P35["⚙️ Process 3.5:<br/>MongoDB Image Scan Logger"]:::process

    %% Data Stores
    D1a["💾 D1.1: Users Collection (MongoDB)"]:::datastore
    D1c["💾 D1.3: Image Forensics (MongoDB)"]:::datastore

    %% -------------------------------------------------------------
    %% Data Flows (Process 3.0 Breakdown)
    %% -------------------------------------------------------------
    
    %% Input and Authorization
    User -->|1. Base64 Image string + JWT token| P31
    D1a -->|2. Verify user has paid/subscription status| P31
    
    %% Decoding & Magic number check
    P31 -->|3. Cleaned Image Byte Stream (WAV/PNG/JPG checks)| P32
    
    %% Short circuit evaluation (Gemini Watermark / C2PA metadata)
    P32 -->|4a. Watermark/C2PA Detected: AI Veto (1.0 Prob, 100% Conf)| P34
    P32 -->|4b. No Short-circuit: Pass bytes to ML extractors| P33
    
    %% Deep Extraction Pipeline
    subgraph P33Sub["Forensic Extraction Modules"]
        P33 -->|FFT Spectrum| FFT["FFT Anomaly Extractor"]
        P33 -->|DINOv2 ViT CLS| DINO["RIGID Perturbation Evaluator"]
        P33 -->|umm-maybe & dima806| Neural["Neural Classifier Ensemble"]
        P33 -->|Error Level Analysis| ELA["ELA Compressor"]
        P33 -->|Wiener Filter Residual| PRNU["PRNU Noise Auditor"]
        P33 -->|EXIF Auditor| EXIF["EXIF Metadata Inspector"]
        P33 -->|CLIP Prompt Align| CLIP["CLIP Semantic Evaluator"]
    end
    
    %% Outputs from extraction to decision engine
    FFT -->|5. Radial average slope & colormap| P34
    DINO -->|5. Cosine similarity shifts| P34
    Neural -->|5. Combined classifier weights| P34
    ELA -->|5. Recompression error variance map| P34
    PRNU -->|5. Isotropy residual metrics| P34
    EXIF -->|5. Software tagging blacklist results| P34
    CLIP -->|5. Prompt similarity vectors| P34

    %% Decision, Logging and Return
    P34 -->|6. Unified Diagnostics payload (Verdicts, Heatmaps)| P35
    P35 -->|7. Persist document to image_forensics collection| D1c
    P34 -->|8. Final Analysis report (JSON response)| User
```

---

## 📊 Detailed Level 2 Data Flow Specifications (Process 3.0)

| Step ID | Source | Destination | Data Elements Transmitted | Purpose / Code Reference |
| :--- | :--- | :--- | :--- | :--- |
| **3.0.1** | User | Process 3.1 | Base64 Image String, Grad-CAM Flag, JWT | User triggers image audit. Check authorization from `users` collection. |
| **3.0.2** | Process 3.1 | Process 3.2 | Sanitized Binary Bytes | Decodes Base64, strips padding, validates magic headers (JPEG `FF D8 FF`, PNG `89 50 4E 47`, etc.). |
| **3.0.3** | Process 3.2 | Process 3.4 | AI Veto (1.00 Prob, 100% Conf) | **Short-Circuit Route**: Bypasses heavy processing if Google Gemini watermark astroid or C2PA `c2pa.genai` is found. |
| **3.0.4** | Process 3.2 | Process 3.3 | Verified Byte Stream | **Standard Route**: If no watermark is found, routes bytes to thread pool for feature extraction. |
| **3.0.5** | Process 3.3 (Modules) | Process 3.4 | Individual Scores, spectral graphs, ELA images | Extracts 7 signals (FFT, DINOv2, ELA, PRNU, Neural, EXIF, CLIP) in parallel. |
| **3.0.6** | Process 3.4 | Process 3.5 | Final Verdict, Threat Level, Heatmaps | Merges signals using confidence weights. If CLIP Semantic > 0.92, triggers digital art veto. |
| **3.0.7** | Process 3.5 | D1.3 Store | Scan document schema | Logs scan results to MongoDB `image_forensics` collection. |
| **3.0.8** | Process 3.4 | User | Final JSON analytical results | Delivers ELA diff overlay, Spectral power plots, and gauges back to the frontend. |

---

## 🖌️ Step-by-Step Drawing Guide for Project Presentation

To explain the Level 2 DFD in your project slides or viva:
1.  **Emphasize the Short-Circuit (Process 3.2):** Standard ML models are computationally heavy. Explain that Process 3.2 checks for **Gemini astroid watermarks** and **C2PA credentials** to immediately output a verdict of `AI-Generated` without consuming ML thread time.
2.  **Describe the Parallelism (Process 3.3):** Explain that the system spawns a `ThreadPoolExecutor` to extract seven separate forensic signals (FFT, RIGID/DINOv2, Neural Ensemble, ELA, PRNU, EXIF, CLIP) concurrently, preventing CPU execution block.
3.  **Explain the Weighted Fusion (Process 3.4):** Highlight how the engine resolves conflicts. If deep classifiers report "human" due to texture smoothing, the **CLIP Semantic veto** overrides the neural model to correctly classify AI-generated illustrations.
