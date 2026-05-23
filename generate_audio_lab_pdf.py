import os
import re
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Paths
DOCS_DIR = r"C:\Users\office\Documents\Final_year_project\fakeshield\docs"
MD_FILE = os.path.join(DOCS_DIR, "audio_lab_documentation.md")
PDF_FILE = os.path.join(DOCS_DIR, "AI_Audio_Lab_Technical_Specs.pdf")
MMDC_PATH = r"C:\Users\office\AppData\Roaming\npm\mmdc.ps1"

# Extract and compile Mermaid diagrams
print("Extracting Mermaid blocks from markdown...")
with open(MD_FILE, "r", encoding="utf-8") as f:
    md_content = f.read()

mermaid_pattern = r"```mermaid\n(.*?)\n```"
mermaid_blocks = re.findall(mermaid_pattern, md_content, re.DOTALL)

png_diagrams = []
for idx, mmd_code in enumerate(mermaid_blocks):
    temp_mmd = os.path.join(DOCS_DIR, f"temp_diag_{idx}.mmd")
    out_png = os.path.join(DOCS_DIR, f"audio_lab_diagram_{idx}.png")
    
    with open(temp_mmd, "w", encoding="utf-8") as f:
        f.write(mmd_code)
        
    print(f"Compiling Mermaid diagram {idx} to PNG...")
    try:
        # Run mmdc using powershell
        cmd = ["powershell", "-File", MMDC_PATH, "-i", temp_mmd, "-o", out_png, "-t", "dark", "-b", "#0f172a"]
        subprocess.run(cmd, check=True)
        png_diagrams.append(out_png)
    except Exception as e:
        print(f"Error compiling diagram {idx}: {e}")
        # If compilation fails, check if we can fall back to standard styling or keep going
        png_diagrams.append(None)
    finally:
        if os.path.exists(temp_mmd):
            os.remove(temp_mmd)

# Set up ReportLab Document
doc = SimpleDocTemplate(
    PDF_FILE, pagesize=A4,
    rightMargin=1.5*cm, leftMargin=1.5*cm,
    topMargin=2.0*cm, bottomMargin=2.0*cm
)

# Color Scheme
DARK = colors.HexColor("#0F172A")       # Primary slate
CYAN = colors.HexColor("#00E5CC")       # Accent cyan
INDIGO = colors.HexColor("#6366F1")     # Accent indigo
GRAY = colors.HexColor("#64748B")       # Muted text
LIGHT_BG = colors.HexColor("#F8FAFC")   # Page backgrounds
BORDER = colors.HexColor("#E2E8F0")     # Light border
ALERT_BG = colors.HexColor("#EFF6FF")   # Alert callout bg
ALERT_BORDER = colors.HexColor("#3B82F6") # Alert callout border

styles = getSampleStyleSheet()

# Custom Paragraph Styles
styles.add(ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=26,
    textColor=DARK,
    spaceAfter=15,
    alignment=TA_LEFT
))

styles.add(ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=10,
    leading=14,
    textColor=GRAY,
    spaceAfter=30,
    alignment=TA_LEFT
))

styles.add(ParagraphStyle(
    "CustomH1",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=17,
    textColor=DARK,
    spaceBefore=22,
    spaceAfter=10,
    keepWithNext=True
))

styles.add(ParagraphStyle(
    "CustomH2",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=15,
    textColor=DARK,
    spaceBefore=16,
    spaceAfter=8,
    keepWithNext=True
))

styles.add(ParagraphStyle(
    "CustomH3",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=13,
    textColor=DARK,
    spaceBefore=12,
    spaceAfter=6,
    keepWithNext=True
))

styles.add(ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12.5,
    textColor=colors.HexColor("#334155"),
    spaceAfter=8
))

styles.add(ParagraphStyle(
    "ListItem",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12.5,
    textColor=colors.HexColor("#334155"),
    leftIndent=15,
    firstLineIndent=-10,
    spaceAfter=4
))

styles.add(ParagraphStyle(
    "CodeBlock",
    parent=styles["Normal"],
    fontName="Courier",
    fontSize=7.5,
    leading=10.5,
    textColor=colors.HexColor("#0F172A"),
    backColor=colors.HexColor("#F1F5F9"),
    borderColor=BORDER,
    borderWidth=0.5,
    borderPadding=8,
    spaceAfter=8,
    borderRadius=4
))

styles.add(ParagraphStyle(
    "AlertText",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12.5,
    textColor=colors.HexColor("#1E3A8A")
))

styles.add(ParagraphStyle(
    "TableText",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#334155")
))

styles.add(ParagraphStyle(
    "TableHeaderText",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=11,
    textColor=colors.white
))

def clean_markdown_formatting(text):
    # Bold: **text** -> <b>text</b>
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    # Italic: *text* -> <i>text</i>
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    # Inline code: `code` -> <font face="Courier" size="8" color="#0F172A">code</font>
    text = re.sub(r"`(.*?)`", r'<font face="Courier" size="7.5" color="#0F172A"><b>\1</b></font>', text)
    # Math notation: $$Formula$$ or $Formula$ -> simplified html
    text = text.replace("$$\\text{Stability} = 1.0 - \\text{min}\\left(1.0, \\frac{|\\text{Score}_{\\text{original}} - \\text{Score}_{\\text{telephony}}|}{0.40}\\right)$$".replace("\\", "\\\\"), "<b>Stability = 1.0 - min(1.0, |Score_original - Score_telephony| / 0.40)</b>")
    text = text.replace("$$\\text{Stability} = 1.0 - \\text{min}\\left(1.0, \\frac{|\\text{Score}_{\\text{original}} - \\text{Score}_{\\text{telephony}}|}{0.40}\\right)$$".replace("\\", "\\"), "<b>Stability = 1.0 - min(1.0, |Score_original - Score_telephony| / 0.40)</b>")
    text = text.replace("$$\\text{Stability} = 1.0 - \\text{min}\\left(1.0, \\frac{|\\text{Score}_{\\text{original}} - \\text{Score}_{\\text{telephony}}|}{0.40}\\right)$$", "<b>Stability = 1.0 - min(1.0, |Score_original - Score_telephony| / 0.40)</b>")
    text = text.replace("$$\\Delta_{\\text{mel}} = \\frac{1}{T-1} \\sum_{t=1}^{T-1} |M_{t+1} - M_t|$$".replace("\\", "\\\\"), "<b>Delta_mel = (1 / (T-1)) * Sum(|M_t+1 - M_t|)</b>")
    text = text.replace("$$\\Delta_{\\text{mel}} = \\frac{1}{T-1} \\sum_{t=1}^{T-1} |M_{t+1} - M_t|$$", "<b>Delta_mel = (1 / (T-1)) * Sum(|M_t+1 - M_t|)</b>")
    text = text.replace("$$\\text{DC Offset} = \\left| \\frac{1}{N} \\sum_{i=1}^N x[i] \\right|$$".replace("\\", "\\\\"), "<b>DC Offset = | (1/N) * Sum(x[i]) |</b>")
    text = text.replace("$$\\text{DC Offset} = \\left| \\frac{1}{N} \\sum_{i=1}^N x[i] \\right|$$", "<b>DC Offset = | (1/N) * Sum(x[i]) |</b>")
    text = text.replace("$$\\text{Std}(F_0)$$".replace("\\", "\\\\"), "<b>Std(F0)</b>")
    text = text.replace("$$\\text{Std}(F_0)$$", "<b>Std(F0)</b>")
    text = text.replace("$$\\text{semitones}$$", "<b>semitones</b>")
    text = text.replace("$$\\text{dB}$$", "<b>dB</b>")
    text = text.replace("$", "")
    return text

# Build Story Flow
story = []

# Title Banner
header_table = Table([
    [
        Paragraph("<b>FAKESHIELD FORENSIC LABORATORIES</b>", ParagraphStyle("HeaderL", parent=styles["Normal"], fontSize=9, textColor=GRAY, fontName="Helvetica-Bold")),
        Paragraph("TECHNICAL SPECIFICATION REPORT", ParagraphStyle("HeaderR", parent=styles["Normal"], fontSize=9, textColor=GRAY, fontName="Helvetica-Bold", alignment=2))
    ]
], colWidths=[9*cm, 9*cm])
header_table.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 4),
]))

story.append(header_table)
story.append(HRFlowable(width="100%", color=DARK, thickness=1.5, spaceAfter=15))

# Document Title
story.append(Paragraph("🎙️ AI Audio Forensic Lab (Process 4.0)", styles["DocTitle"]))
story.append(Paragraph("System Architecture, Forensic Models, Multi-Phase Fusion, and Integration Specifications", styles["DocSubtitle"]))

# Parse markdown sections manually to create flows
lines = md_content.split("\n")
i = 0
in_list = False
in_table = False
table_headers = []
table_rows = []
in_code = False
code_text = []

# Tracker for mermaid diagrams (since we stripped them out and compiled them)
diag_idx = 0

while i < len(lines):
    line = lines[i].strip()
    
    # Handle Code Blocks
    if line.startswith("```"):
        if line.startswith("```mermaid"):
            # Skip mermaid block since we render it separately as an Image flowable
            # Just advance until the closing block
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            
            # Place Compiled Diagram Image
            if diag_idx < len(png_diagrams) and png_diagrams[diag_idx]:
                story.append(Spacer(1, 0.4*cm))
                img_path = png_diagrams[diag_idx]
                # Scale image to fit A4 width nicely (max ~17cm width)
                # Keep aspect ratio
                story.append(KeepTogether([
                    Paragraph(f"<b>Figure {diag_idx + 1}: {'Audio Lab Processing Workflow' if diag_idx == 0 else 'Hierarchical Fusion Decision Tree'}</b>", 
                              ParagraphStyle("FigCap", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, textColor=DARK, spaceAfter=8, alignment=TA_CENTER)),
                    Image(img_path, width=17*cm, height=9.5*cm),
                    Spacer(1, 0.5*cm)
                ]))
                diag_idx += 1
            i += 1
            continue
        
        elif in_code:
            in_code = False
            # Render Code block
            code_content = "\n".join(code_text)
            story.append(Paragraph(code_content.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["CodeBlock"]))
            code_text = []
        else:
            in_code = True
        i += 1
        continue

    if in_code:
        code_text.append(line)
        i += 1
        continue

    # Skip empty lines
    if not line:
        i += 1
        continue
        
    # Handle Headers
    if line.startswith("# "):
        # Document title is handled separately, skip main H1
        i += 1
        continue
    elif line.startswith("## "):
        story.append(Spacer(1, 0.3*cm))
        header_text = clean_markdown_formatting(line[3:])
        story.append(Paragraph(header_text, styles["CustomH1"]))
        story.append(HRFlowable(width="100%", color=BORDER, thickness=0.8, spaceAfter=8))
        i += 1
        continue
    elif line.startswith("### "):
        header_text = clean_markdown_formatting(line[4:])
        story.append(Paragraph(header_text, styles["CustomH2"]))
        i += 1
        continue
    elif line.startswith("#### "):
        header_text = clean_markdown_formatting(line[5:])
        story.append(Paragraph(header_text, styles["CustomH3"]))
        i += 1
        continue

    # Handle Bullet Lists
    if line.startswith("* ") or line.startswith("- "):
        list_text = clean_markdown_formatting(line[2:])
        story.append(Paragraph(f"• {list_text}", styles["ListItem"]))
        i += 1
        continue

    # Handle Numbered Lists
    if re.match(r"^\d+\.\s+", line):
        parts = line.split(".", 1)
        num = parts[0].strip()
        list_text = clean_markdown_formatting(parts[1].strip())
        story.append(Paragraph(f"{num}. {list_text}", styles["ListItem"]))
        i += 1
        continue

    # Handle Alert Blocks (GitHub style blockquotes)
    if line.startswith("> [!"):
        alert_type = re.search(r"\[!(.*?)\]", line).group(1)
        alert_body_lines = []
        i += 1
        while i < len(lines) and lines[i].strip().startswith(">"):
            alert_body_lines.append(lines[i].strip().lstrip(">").strip())
            i += 1
        alert_body = clean_markdown_formatting(" ".join(alert_body_lines))
        
        # Render beautiful Callout Table
        alert_para = Paragraph(f"<b>{alert_type.upper()}:</b> {alert_body}", styles["AlertText"])
        alert_table = Table([[alert_para]], colWidths=[18*cm])
        alert_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), ALERT_BG),
            ("BOX", (0,0), (-1,-1), 0.5, ALERT_BORDER),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 10),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ]))
        story.append(Spacer(1, 0.2*cm))
        story.append(alert_table)
        story.append(Spacer(1, 0.2*cm))
        continue

    # Handle Markdown Tables
    if line.startswith("|"):
        # We parse the table headers and lines
        table_lines = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            table_lines.append(lines[i].strip())
            i += 1
            
        # Parse headers
        headers_raw = [h.strip() for h in table_lines[0].split("|")[1:-1]]
        headers_p = [Paragraph(f"<b>{clean_markdown_formatting(h)}</b>", styles["TableHeaderText"]) for h in headers_raw]
        
        rows_p = []
        # Skip table divider (index 1)
        for row_line in table_lines[2:]:
            cells_raw = [c.strip() for c in row_line.split("|")[1:-1]]
            cells_p = [Paragraph(clean_markdown_formatting(c), styles["TableText"]) for c in cells_raw]
            rows_p.append(cells_p)
            
        # Table layout
        all_table_data = [headers_p] + rows_p
        
        # Dynamic col widths based on column count
        col_count = len(headers_raw)
        if col_count == 3:
            col_widths = [4.5*cm, 3.5*cm, 10.0*cm]
        elif col_count == 4:
            col_widths = [6.0*cm, 3.0*cm, 3.0*cm, 6.0*cm]
        else:
            col_widths = [18.0 / col_count * cm] * col_count
            
        p_table = Table(all_table_data, colWidths=col_widths)
        p_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), DARK),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT_BG]),
            ("GRID", (0,0), (-1,-1), 0.5, BORDER),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(Spacer(1, 0.2*cm))
        story.append(p_table)
        story.append(Spacer(1, 0.3*cm))
        continue

    # Regular Paragraph
    p_text = clean_markdown_formatting(line)
    story.append(Paragraph(p_text, styles["Body"]))
    i += 1

# Page Numbering & Footer Callback
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(1.5*cm, 1.5*cm, 19.5*cm, 1.5*cm)
    
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(1.5*cm, 1.1*cm, "FakeShield Automated Intelligence Systems — AI Audio Lab v3.2.1-PRO")
    canvas.drawRightString(19.5*cm, 1.1*cm, f"Page {doc.page}")
    canvas.restoreState()

# Build PDF
print(f"Building document to {PDF_FILE}...")
doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
print("PDF compilation complete!")

# Cleanup diagram PNGs (if desired)
# for path in png_diagrams:
#     if path and os.path.exists(path):
#         os.remove(path)
