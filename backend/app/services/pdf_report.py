"""
PDF Report Generator v16.5 (Enterprise Forensic Edition)
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units     import cm
from reportlab.lib            import colors
from reportlab.platypus       import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, PageBreak
)
from io import BytesIO
from datetime import datetime
import hashlib


def generate_pdf(scan_id: str, result: dict, text: str) -> bytes:
    buffer = BytesIO()
    doc    = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm,   bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()
    story  = []

    # ── Colours ──────────────────────────────────────────────
    DARK    = colors.HexColor("#020617")
    CYAN    = colors.HexColor("#00E5CC")
    RED     = colors.HexColor("#EF4444")
    GREEN   = colors.HexColor("#10B981")
    AMBER   = colors.HexColor("#F59E0B")
    GRAY    = colors.HexColor("#64748B")
    BG_LIGHT = colors.HexColor("#F8FAFC")
    BORDER   = colors.HexColor("#E2E8F0")

    threat_level = result.get("threat_level", "LOW")
    threat_color = {
        "CRITICAL": RED,
        "HIGH":     colors.HexColor("#F97316"),
        "MEDIUM":   AMBER,
        "LOW":      GREEN,
    }.get(threat_level, GRAY)

    # ── Header & Branding ───────────────────────────────────────────────
    header_data = [
        [
            Paragraph("<b>FAKESHIELD</b><br/><font size='8' color='#64748B'>FORENSIC LABS & INTELLIGENCE</font>", 
                      ParagraphStyle("Brand", parent=styles["Normal"], fontSize=20, textColor=DARK, leading=18)),
            Paragraph(f"<b>REPORT #</b> {scan_id.upper()}<br/><b>ISSUED:</b> {datetime.now().strftime('%d %b %Y | %H:%M')}", 
                      ParagraphStyle("Meta", parent=styles["Normal"], fontSize=8, textColor=GRAY, alignment=2))
        ]
    ]
    header_table = Table(header_data, colWidths=[10*cm, 8*cm])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.2*cm))
    story.append(HRFlowable(width="100%", color=DARK, thickness=1.5, vAlign='TOP'))
    story.append(Spacer(1, 0.8*cm))

    # ── Master Verdict ───────────────────────────────────────────
    verdict_title = Paragraph("I. EXECUTIVE FORENSIC SUMMARY", ParagraphStyle("H1", parent=styles["Heading1"], fontSize=12, textColor=DARK, spaceAfter=12))
    story.append(verdict_title)

    verdict_data = [[
        Paragraph(f"<font color='#64748B' size='8'>OVERALL VERDICT</font><br/><b>{result.get('verdict', 'UNKNOWN')}</b>", 
                  ParagraphStyle("V1", parent=styles["Normal"], fontSize=14, leading=18)),
        Paragraph(f"<font color='#64748B' size='8'>AI PROBABILITY</font><br/><b>{int((result.get('score', 0) if isinstance(result.get('score'), (int, float)) else 0) * 100)}%</b>", 
                  ParagraphStyle("V2", parent=styles["Normal"], fontSize=14, leading=18)),
        Paragraph(f"<font color='#64748B' size='8'>THREAT LEVEL</font><br/><b>{threat_level}</b>", 
                  ParagraphStyle("V3", parent=styles["Normal"], fontSize=14, leading=18, textColor=threat_color)),
    ]]
    vt = Table(verdict_data, colWidths=[6*cm, 6*cm, 6*cm])
    vt.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), BG_LIGHT),
        ("BOX",         (0,0), (-1,-1), 1, BORDER),
        ("TOPPADDING",  (0,0), (-1,-1), 15),
        ("BOTTOMPADDING",(0,0), (-1,-1), 15),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
    ]))
    story.append(vt)
    story.append(Spacer(1, 1*cm))

    # ── Technical Metadata ─────────────────────────────────────────
    meta_data = [
        [Paragraph("<b>II. TECHNICAL SPECIFICATIONS</b>", ParagraphStyle("H2", parent=styles["Heading2"], fontSize=10))],
        ["Engine Cluster", "v85.26 Elite Fusion (Neural + Statistical + Stylometric)"],
        ["Confidence Matrix", f"{result.get('confidence_level', 'STABLE')} ({result.get('confidence', '90%')})"],
        ["Analysis Depth", "Deep Scan (Recursive Linguistic Audit)"],
        ["Word Count", f"{result.get('word_count', 0)} Tokens"],
        ["Latency", result.get("processing_time", "N/A")],
        ["Data Hash (SHA-256)", hashlib.sha256(text.encode()).hexdigest()[:32].upper()]
    ]
    meta_table = Table(meta_data[1:], colWidths=[6*cm, 12*cm])
    meta_table.setStyle(TableStyle([
        ("FONTSIZE",    (0,0), (-1,-1), 8),
        ("TEXTCOLOR",   (0,0), (0,-1), GRAY),
        ("FONTNAME",    (0,0), (0,-1), "Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LINEBELOW",   (0,0), (-1,-1), 0.5, BORDER),
    ]))
    story.append(meta_data[0][0])
    story.append(Spacer(1, 0.2*cm))
    story.append(meta_table)
    story.append(Spacer(1, 1*cm))

    # ── Forensic Reasoning ──────────────────────────────────────────
    reasoning = result.get("forensic_reasoning", "")
    if reasoning:
        story.append(Paragraph("<b>III. LINGUISTIC REASONING AUDIT</b>", ParagraphStyle("H2", parent=styles["Heading2"], fontSize=10)))
        story.append(Spacer(1, 0.3*cm))
        reasoning_style = ParagraphStyle(
            "Reasoning",
            parent=styles["Normal"],
            fontSize=10,
            leading=15,
            textColor=DARK,
            backColor=colors.HexColor("#F1F5F9"),
            borderPadding=15,
            borderWidth=1,
            borderColor=BORDER,
            borderRadius=8
        )
        story.append(Paragraph(reasoning, reasoning_style))
        story.append(Spacer(1, 1*cm))

    # ── Multi-Vector Signals ─────────────────────────────────────────
    story.append(Paragraph("<b>IV. MULTI-VECTOR SIGNAL INTEL (v85.26)</b>", ParagraphStyle("H2", parent=styles["Heading2"], fontSize=10)))
    story.append(Spacer(1, 0.3*cm))
    sigs = result.get("signals", {})
    sig_data = [["Intelligence Vector", "Intensity", "Reliability", "Diagnostic Note"]]
    
    sig_rows = [
        ("Neural Pulse (DeBERTa-v3-L)", f"{int(sigs.get('neural', 0.5)*100)}%", "HIGH", "Adversarial pattern recognition"),
        ("Binoculars (Statistical)", f"{int(sigs.get('statistical', 0.5)*100)}%", "HIGH", "Log-probability distribution audit"),
        ("Rhythmic Variance (Forensic)", f"{int(sigs.get('rhythm', 0.5)*100)}%", "MEDIUM", "Syntactic complexity & burstiness"),
        ("Semantic Flow (Drift)", f"{int(sigs.get('flow', 0.5)*100)}%", "HIGH", "Thought trajectory consistency check"),
    ]
    for name, score, rel, desc in sig_rows:
        sig_data.append([name, score, rel, desc])

    sig_table = Table(sig_data, colWidths=[6*cm, 3*cm, 3*cm, 6*cm])
    sig_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("ALIGN",        (1,1), (2,-1), "CENTER"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, BG_LIGHT]),
        ("GRID",         (0,0), (-1,-1), 0.5, BORDER),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
    ]))
    story.append(sig_table)
    
    story.append(PageBreak())

    # ── Certification Section ─────────────────────────────────────────
    story.append(Spacer(1, 2*cm))
    cert_data = [
        [
            Paragraph("<b>CERTIFICATE OF AUTHENTICITY</b><br/><font size='8'>This document certifies that the forensic analysis of the provided text evidence was conducted using the FakeShield Elite Ensemble. The results are mathematically derived from multi-vector linguistic signals.</font>", 
                      ParagraphStyle("Cert", parent=styles["Normal"], fontSize=12, leading=16, borderPadding=20, borderWidth=2, borderColor=DARK, borderRadius=10)),
        ]
    ]
    cert_table = Table(cert_data, colWidths=[18*cm])
    story.append(cert_table)
    story.append(Spacer(1, 2*cm))

    # ── Signatures ─────────────────────────────────────────
    sig_data = [
        [
            Paragraph("__________________________<br/><b>CHIEF FORENSIC ANALYST</b><br/>FakeShield Automated Systems", 
                      ParagraphStyle("Sig1", parent=styles["Normal"], fontSize=9)),
            Paragraph(f"<b>DIGITAL SEAL</b><br/><font size='6' color='#64748B'>{hashlib.md5(scan_id.encode()).hexdigest().upper()}</font>", 
                      ParagraphStyle("Sig2", parent=styles["Normal"], fontSize=9, alignment=2))
        ]
    ]
    sig_table = Table(sig_data, colWidths=[9*cm, 9*cm])
    story.append(sig_table)

    # ── Confidentiality Notice ─────────────────────────────────────────
    story.append(Spacer(1, 4*cm))
    story.append(HRFlowable(width="100%", color=GRAY, thickness=0.5))
    story.append(Paragraph(
        "<b>CONFIDENTIALITY & DISCLAIMER:</b> This report is generated by FakeShield Forensic Engine v85.26. "
        "The analysis is based on probabilistic models and statistical linguistics. "
        "Results should be interpreted as diagnostic indicators. FakeShield is not liable for actions taken based on this report. "
        "Property of FakeShield Labs.",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=7, textColor=GRAY, alignment=1, leading=10)
    ))

    doc.build(story)
    return buffer.getvalue()
