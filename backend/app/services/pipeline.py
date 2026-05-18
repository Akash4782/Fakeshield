"""
FakeShield — Text Detection Pipeline
Replaces n8n entirely. Pure Python.
Handles: validation → detection → DB save → alerts → PDF → response
"""

import uuid
import smtplib
import asyncio
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models.new_forensic_engine import analyze_forensic as analyze
from app.services.database    import save_scan
from app.services.pdf_report  import generate_pdf
from app.config               import settings


# ─────────────────────────────────────────────────────────────
# RETRY WRAPPER
# Retries any function up to max_retries times on failure
# Replaces n8n's built-in retry logic
# ─────────────────────────────────────────────────────────────
async def with_retry(fn, *args, max_retries=3, delay=2, **kwargs):
    last_error = None
    for attempt in range(max_retries):
        try:
            return await fn(*args, **kwargs)
        except Exception as e:
            last_error = e
            print(f"[Retry] Attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay * (attempt + 1))
    raise last_error


# ─────────────────────────────────────────────────────────────
# STEP 1 — VALIDATE
# Pydantic handles this in the router, but we double-check here
# ─────────────────────────────────────────────────────────────
def validate_input(text: str, mode: str) -> dict:
    text = text.strip()
    if len(text) < 20:
        raise ValueError("Text too short. Minimum 20 characters.")
    if len(text) > 15000:
        raise ValueError("Text too long. Maximum 15000 characters.")
    if mode not in ("fast", "deep"):
        mode = "deep"

    return {
        "text":         text,
        "mode":         mode,
        "scan_id":      "fs_" + str(uuid.uuid4()).replace("-", "")[:16],
        "submitted_at": datetime.utcnow().isoformat() + "Z",
    }


# ─────────────────────────────────────────────────────────────
# STEP 2 — RUN DETECTION
# Calls the 5-signal engine directly (no HTTP call needed)
# ─────────────────────────────────────────────────────────────
def run_detection(text: str, mode: str, include_highlights: bool) -> dict:
    return analyze(
        text=text,
        mode=mode
    )


# ─────────────────────────────────────────────────────────────
# STEP 3 — SAVE TO POSTGRESQL
# Replaces n8n's Postgres node
# ─────────────────────────────────────────────────────────────
async def save_to_database(user_email: str, scan_id: str, result: dict, text: str):
    try:
        await save_scan(
            user_email=user_email,
            scan_id=scan_id,
            verdict=result["verdict"],
            threat_level=result["threat_level"],
            confidence=result["confidence"],
            confidence_level=result["confidence_level"],
            agreement_score=result["agreement_score"],
            stability_score=result["stability_score"],
            signals=result["signals"],
            linguistic_profile=result["linguistic_profile"],
            stylometric_details=result.get("stylometric_details", {}),
            word_count=result["word_count"],
            processing_time=result["processing_time"],
            text_preview=text[:200],
        )
        print(f"[DB] Scan {scan_id} saved.")
    except Exception as e:
        # Non-critical — don't fail the whole request if DB is down
        print(f"[DB] Save failed (non-critical): {e}")


# ─────────────────────────────────────────────────────────────
# STEP 4 — SEND CRITICAL ALERT
# Replaces n8n's email/Telegram node
# Sends email alert when confidence >= 80%
# ─────────────────────────────────────────────────────────────
def send_critical_alert(scan_id: str, result: dict, text_preview: str):
    try:
        if not settings.ALERT_EMAIL_ENABLED:
            print(f"[Alert] CRITICAL scan {scan_id} — email disabled in config")
            return

        subject = f"🚨 FakeShield CRITICAL — AI Text Detected ({int(result.get('score', 0)*100)}%)"

        body = f"""
FakeShield Forensic Alert (Engine v10.1-PRO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scan ID:     {scan_id}
Verdict:     {result['verdict']}
Confidence:  {result.get('confidence', 'N/A')}
Threat:      {result['threat_level']}
Words:       {result.get('word_count', 0)}
Time:        {result.get('processing_time', 'N/A')}

Forensic Intelligence (v16.5-RESEARCH):
  - Reasoning:   {int(result['signals'].get('lexical_signal', 0.5)*100)}%
  - Structural:  {int(result['signals'].get('structural_strength', 0.5)*100)}%
  - Semantic:    {int(result['signals'].get('semantic_irregularity', 0.5)*100)}%
  - Binoculars:  {int(result['signals'].get('binoculars_signal', 0.5)*100)}%
  - Neural:      {int(result['signals'].get('classifier_signal', 0.5)*100)}%

Forensic Expert Reasoning:
"{result.get('forensic_reasoning', 'Analysis complete.')}"

Key Indicators:
{chr(10).join(['  - ' + i for i in result.get('indicators', [])])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FakeShield v16.5 — Research Forensic Suite
        """

        msg = MIMEMultipart()
        msg["From"]    = settings.SMTP_FROM
        msg["To"]      = settings.ALERT_EMAIL_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        print(f"[Alert] Critical alert sent for scan {scan_id}")

    except Exception as e:
        print(f"[Alert] Email failed (non-critical): {e}")


# ─────────────────────────────────────────────────────────────
# STEP 5 — GENERATE PDF REPORT
# Replaces n8n's PDF generation + file node
# ─────────────────────────────────────────────────────────────
def create_pdf_report(scan_id: str, result: dict, text: str) -> bytes:
    try:
        pdf_bytes = generate_pdf(
            scan_id=scan_id,
            result=result,
            text=text
        )
        print(f"[PDF] Report generated for scan {scan_id}")
        return pdf_bytes
    except Exception as e:
        print(f"[PDF] Generation failed: {e}")
        return b""


# ─────────────────────────────────────────────────────────────
# MASTER PIPELINE — called by the router
# This IS the n8n workflow, written in Python
# ─────────────────────────────────────────────────────────────
async def run_text_pipeline(
    user_email: str,
    text: str,
    mode: str = "deep",
    include_highlights: bool = True,
    generate_report: bool = False,
) -> dict:

    pipeline_start = time.time()

    # ── Step 1: Validate ─────────────────────────────────────
    validated = validate_input(text, mode)
    scan_id   = validated["scan_id"]
    clean_text = validated["text"]

    print(f"[Pipeline] Starting scan {scan_id} | mode={mode}")

    # ── Step 2: Detect (with retry) ──────────────────────────
    try:
        # run_detection is synchronous and heavy, run it in a thread to keep the event loop alive
        result = await asyncio.to_thread(run_detection, clean_text, mode, include_highlights)
    except Exception as e:
        # Retry detection once on failure
        print(f"[Pipeline] Detection failed, retrying: {e}")
        await asyncio.sleep(1)
        result = await asyncio.to_thread(run_detection, clean_text, mode, include_highlights)

    # ── Step 3: Enrich result ────────────────────────────────
    result["scan_id"]      = scan_id
    result["submitted_at"] = validated["submitted_at"]
    result["completed_at"] = datetime.utcnow().isoformat() + "Z"
    result["text_preview"] = clean_text[:150] + "..."

    # ── Step 4: Save to DB (background — non-blocking) ───────
    asyncio.create_task(
        save_to_database(user_email, scan_id, result, clean_text)
    )

    # ── Step 5: CRITICAL alert (background — non-blocking) ───
    if result.get("threat_level") == "CRITICAL":
        asyncio.create_task(
            asyncio.to_thread(
                send_critical_alert,
                scan_id, result, clean_text[:300]
            )
        )

    # ── Step 6: PDF report (optional) ────────────────────────
    pdf_bytes = b""
    if generate_report:
        pdf_bytes = await asyncio.to_thread(
            create_pdf_report, scan_id, result, clean_text
        )
        result["report_available"] = True
        result["report_size_kb"]   = round(len(pdf_bytes) / 1024, 1)
    else:
        result["report_available"] = False

    # ── Final timing ─────────────────────────────────────────
    result["pipeline_time"] = f"{round(time.time()-pipeline_start, 2)}s"

    print(f"[Pipeline] Scan {scan_id} complete | "
          f"verdict={result['verdict']} | "
          f"confidence={result['confidence']}% ({result['confidence_level']})")

    return result, pdf_bytes
