"""
PDF Report Generator v10.1 (Linguistic Forensic Edition)
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units     import cm
from reportlab.lib            import colors
from reportlab.platypus       import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)
from io import BytesIO
from datetime import datetime


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
    DARK    = colors.HexColor("#0A0E1A")
    CYAN    = colors.HexColor("#00F0FF")
    RED     = colors.HexColor("#EF4444")
    GREEN   = colors.HexColor("#10B981")
    AMBER   = colors.HexColor("#F59E0B")
    GRAY    = colors.HexColor("#6B7280")
    BG_LIGHT = colors.HexColor("#F9FAFB")

    threat_level = result.get("threat_level", "LOW")
    threat_color = {
        "CRITICAL": RED,
        "HIGH":     colors.HexColor("#F97316"),
        "MEDIUM":   AMBER,
        "LOW":      GREEN,
    }.get(threat_level, GRAY)

    # ── Header ───────────────────────────────────────────────
    story.append(Paragraph(
        "<b>FAKESHIELD</b> — Forensic AI Detection Report",
        ParagraphStyle("H", parent=styles["Title"], fontSize=22, textColor=DARK)
    ))
    story.append(Paragraph(
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC | v10.1.0-PRO-FORENSIC",
        ParagraphStyle("Sub", parent=styles["Normal"], fontSize=8, textColor=GRAY)
    ))
    story.append(HRFlowable(width="100%", color=CYAN, thickness=2, vAlign='TOP'))
    story.append(Spacer(1, 0.5*cm))

    # ── Scan metadata ─────────────────────────────────────────
    meta = [
        ["Scan ID",    scan_id],
        ["Engine",     result.get("engine_version", "v10.1.0-PRO-FORENSIC")],
        ["Signals",    "Structural + Semantic + Reasoning + Statistical"],
        ["Word Count", f"{result.get('word_count', 0)} words"],
        ["Proc. Time", result.get("processing_time", "N/A")],
        ["Confidence", f"<b>{result.get('confidence', 'MEDIUM')}</b>"],
    ]
    meta_table = Table(meta, colWidths=[4*cm, 13*cm])
    meta_table.setStyle(TableStyle([
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("TEXTCOLOR",   (0,0), (0,-1), GRAY),
        ("FONTNAME",    (0,0), (0,-1), "Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.4*cm))

    # ── Verdict box ───────────────────────────────────────────
    verdict_data = [[
        f"CRITICAL VERDICT: {result.get('verdict', 'UNKNOWN')}",
        f"AI SCORE: {int((result.get('score', 0) if isinstance(result.get('score'), (int, float)) else 0) * 100)}%",
        f"THREAT: {threat_level}",
    ]]
    vt = Table(verdict_data, colWidths=[7*cm, 5*cm, 5*cm])
    vt.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), DARK),
        ("TEXTCOLOR",   (0,0), (-1,-1), threat_color),
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 12),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("BOX",         (0,0), (-1,-1), 2, threat_color),
        ("TOPPADDING",  (0,0), (-1,-1), 14),
        ("BOTTOMPADDING",(0,0), (-1,-1), 14),
    ]))
    story.append(vt)
    story.append(Spacer(1, 0.8*cm))

    # ── Forensic Reasoning Box (v10.1 HIGHLIGHT) ──────────────
    reasoning = result.get("forensic_reasoning", "")
    if reasoning:
        story.append(Paragraph(
            "Forensic Expert Reasoning (Gemini v1.5 Flash Audit)",
            ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11, textColor=DARK)
        ))
        reasoning_style = ParagraphStyle(
            "Reasoning",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            italic=True,
            leftIndent=15,
            rightIndent=15,
            textColor=colors.HexColor("#1F2937")
        )
        # Styled box for reasoning
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(f'"{reasoning}"', reasoning_style))
        story.append(Spacer(1, 0.6*cm))

    # ── v10.1 Signal Audit Table ─────────────────────────────
    story.append(Paragraph(
        "Forensic Signal Audit (v10.1 Logic Weights)",
        ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11)
    ))
    sigs = result.get("signals", {})
    # Weights dynamic based on engine
    sig_data = [["Forensic Signal", "Score", "Weight", "Significance"]]
    
    # We use actual v14 signals
    sig_rows = [
        ("Structural Entropy",   f"{int(sigs.get('structural_strength', 0.5)*100)}%", "20%", "Dependency Tree Regularity"),
        ("Semantic Flow Drift",  f"{int(sigs.get('semantic_irregularity', 0.5)*100)}%",   "20%", "Thought Evolution Consistency"),
        ("GPT-2 PPL Entropy",    f"{int(sigs.get('ppl_signal', 0.5)*100)}%",  "10%", "Neural Predictability"),
        ("Statistical Burstiness",f"{int(sigs.get('burstiness_signal', 0.5)*100)}%","10%", "Token Probability Variance"),
        ("HC3 ChatGPT Classifier",f"{int(sigs.get('classifier_signal', 0.5)*100)}%",    "40%", "Neural Fingerprinting"),
    ]
    for name, score, weight, desc in sig_rows:
        sig_data.append([name, score, weight, desc])

    sig_table = Table(sig_data, colWidths=[6*cm, 3*cm, 3*cm, 5*cm])
    sig_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK),
        ("TEXTCOLOR",    (0,0), (-1,0), CYAN),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ALIGN",        (1,0), (2,-1), "CENTER"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [BG_LIGHT, colors.white]),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 0.6*cm))

    # ── Structural & Semantic Details ──────────────────────────
    sd = result.get("structural_details", {})
    sem = result.get("semantic_details", {})
    
    story.append(Paragraph(
        "Advanced Linguistic Diagnostics",
        ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11)
    ))
    
    diag_data = [
        ["Diagnostic Metric", "Value", "Forensic Interpretation"],
        ["Tree Depth Variance", str(sd.get('depth_variance', 'N/A')), "Structural irregularity (High = Human)"],
        ["Semantic Consistency", f"{round(sem.get('semantic_consistency', 0)*100, 1)}%", "Topic stability (Extreme = AI-like)"],
        ["Drift Trajectory", str(sem.get('trajectory_smoothness', 'N/A')), "Logic flow path (Linear = AI-like)"],
        ["Sentence Cadence CV", str(sd.get('sentence_cadence_cv', 'N/A')), "Rhythmic variation across text"],
    ]
    diag_table = Table(diag_data, colWidths=[5*cm, 4*cm, 8*cm])
    diag_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#1F2937")),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("FONTNAME",     (0,0), (-1,-1), "Helvetica"),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 0.8*cm))

    # ── Key Indicators (v10.1 Bullets) ────────────────────────
    indicators = result.get("indicators", [])
    if indicators:
        story.append(Paragraph(
            "Suspicious Forensic Indicators",
            ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11)
        ))
        for ind in indicators:
            story.append(Paragraph(
                f"• {ind}",
                ParagraphStyle("Indicator", parent=styles["Normal"], fontSize=9, leftIndent=10)
            ))
        story.append(Spacer(1, 0.5*cm))

    # ── Sentence Level Sample ─────────────────────────────────
    hls = result.get("sentence_highlights", [])
    if hls:
        story.append(Paragraph(
            "Sentence-Level Micro-Audit (Partial Sample)",
            ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11)
        ))
        hl_data = [["Sentence", "Verdict", "AI Score"]]
        for hl in hls[:6]:
            hl_data.append([
                hl["sentence"][:100] + ("..." if len(hl["sentence"]) > 100 else ""),
                hl["label"],
                f"{int(hl['ai_score']*100)}%" if hl.get('ai_score') else "N/A"
            ])
        
        hl_table = Table(hl_data, colWidths=[12*cm, 3*cm, 2*cm])
        hl_table.setStyle(TableStyle([
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.2, GRAY),
            ("BACKGROUND", (0,0), (-1,0), BG_LIGHT),
        ]))
        story.append(hl_table)

    # ── Footer ────────────────────────────────────────────────
    story.append(Spacer(1, 1.5*cm))
    story.append(HRFlowable(width="100%", color=GRAY, thickness=0.5))
    story.append(Paragraph(
        "FakeShield Forensic Engine v10.1-PRO. This report is data-driven and for audit purposes only. "
        "Intended for professional verification of text integrity.",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=7, textColor=GRAY, alignment=1)
    ))

    doc.build(story)
    return buffer.getvalue()
