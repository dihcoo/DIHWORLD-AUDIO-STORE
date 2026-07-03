#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    FrameBreak,
    HRFlowable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "DIHWORLD_IDEAL_SHORT_DEMOS_HANDOFF_20260703.md"
OUTPUT = ROOT / "output" / "pdf" / "DIHWorld_Ideal_Short_Demos_Handoff_20260703.pdf"


def clean_inline(text: str) -> str:
    text = text.strip()
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    return text


def make_styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=31,
            textColor=colors.HexColor("#151515"),
            spaceAfter=18,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            parent=base["BodyText"],
            alignment=TA_CENTER,
            fontName="Helvetica",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#4e5a52"),
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=21,
            textColor=colors.HexColor("#151515"),
            spaceBefore=12,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13.5,
            leading=17,
            textColor=colors.HexColor("#73263c"),
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=14,
            textColor=colors.HexColor("#13766f"),
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.3,
            leading=12.8,
            textColor=colors.HexColor("#222622"),
            spaceAfter=5,
        ),
        "label": ParagraphStyle(
            "Label",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.8,
            leading=11,
            textColor=colors.HexColor("#151515"),
            spaceBefore=5,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.0,
            leading=12,
            leftIndent=12,
            firstLineIndent=0,
            textColor=colors.HexColor("#222622"),
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.3,
            leading=9.2,
            textColor=colors.HexColor("#222622"),
            backColor=colors.HexColor("#eef1ee"),
            borderPadding=5,
            spaceBefore=4,
            spaceAfter=6,
        ),
    }


def footer(canvas, doc):
    canvas.saveState()
    width, height = letter
    canvas.setStrokeColor(colors.HexColor("#d7ded6"))
    canvas.line(0.65 * inch, 0.52 * inch, width - 0.65 * inch, 0.52 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#687169"))
    canvas.drawString(0.65 * inch, 0.34 * inch, "DIHWorld Audio Ideal Short Demos Handoff")
    canvas.drawRightString(width - 0.65 * inch, 0.34 * inch, f"Page {doc.page}")
    canvas.restoreState()


def flush_list(story, pending, styles, ordered=False):
    if not pending:
        return
    for idx, item in enumerate(pending, start=1):
        marker = f"{idx}." if ordered else "-"
        story.append(Paragraph(f"<font color='#13766f'>{marker}</font> {clean_inline(item)}", styles["bullet"]))
    story.append(Spacer(1, 4))
    pending.clear()


def add_cover(story, styles):
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph("DIHWorld Audio", styles["cover_title"]))
    story.append(Paragraph("Ideal Short Demos Handoff", styles["cover_title"]))
    story.append(Spacer(1, 0.12 * inch))
    story.append(HRFlowable(width="42%", thickness=1.6, color=colors.HexColor("#c9a348"), spaceAfter=18))
    story.append(Paragraph("Family-based short demo slate, special functions, and combo chains", styles["cover_sub"]))
    story.append(Paragraph("Prepared for the current 42-plugin, 13-family DIHWorld Audio release", styles["cover_sub"]))
    story.append(Spacer(1, 0.35 * inch))
    label_style = ParagraphStyle(
        "CoverLabel",
        parent=styles["cover_sub"],
        alignment=TA_LEFT,
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#73263c"),
    )
    path_style = ParagraphStyle(
        "CoverPath",
        parent=styles["cover_sub"],
        alignment=TA_LEFT,
        fontName="Courier",
        fontSize=6.6,
        leading=8.4,
        textColor=colors.HexColor("#151515"),
    )
    data = [
        [Paragraph("Source page", label_style), Paragraph(clean_inline("/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/index.html"), path_style)],
        [Paragraph("Family authority", label_style), Paragraph(clean_inline("/Users/hakeemsalaam/Development/DIH_BUILDS/DIH_FAMILIES/CURRENT_FAMILY_AUTHORITY.md"), path_style)],
        [Paragraph("Release index", label_style), Paragraph(clean_inline("/Users/hakeemsalaam/Development/DIH_BUILDS/DIH_FAMILIES/CURRENT_RELEASE_INDEX.md"), path_style)],
        [Paragraph("Copy references", label_style), Paragraph(clean_inline("/Users/hakeemsalaam/Desktop/DIHWorld_Audio_Welcome_Package"), path_style)],
        [Paragraph("Date", label_style), Paragraph("2026-07-03", path_style)],
    ]
    table = Table(data, colWidths=[1.35 * inch, 4.85 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef1ee")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#73263c")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d7ded6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(table)
    story.append(PageBreak())


def build_story(markdown: str):
    styles = make_styles()
    story = []
    add_cover(story, styles)

    lines = markdown.splitlines()
    bullets = []
    numbers = []
    in_code = False
    code_lines = []
    seen_first_section = False

    for raw in lines:
        line = raw.rstrip()

        if line.startswith("# DIHWorld Audio Demo Storefront Copy Handoff"):
            continue

        if not seen_first_section:
            if line.startswith("## "):
                seen_first_section = True
            else:
                continue

        if line.startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code_lines), styles["code"]))
                code_lines = []
                in_code = False
            else:
                flush_list(story, bullets, styles, ordered=False)
                flush_list(story, numbers, styles, ordered=True)
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            flush_list(story, bullets, styles, ordered=False)
            flush_list(story, numbers, styles, ordered=True)
            story.append(Spacer(1, 2))
            continue

        bullet_match = re.match(r"^- (.+)$", stripped)
        number_match = re.match(r"^\d+\. (.+)$", stripped)

        if bullet_match:
            flush_list(story, numbers, styles, ordered=True)
            bullets.append(bullet_match.group(1))
            continue

        if number_match:
            flush_list(story, bullets, styles, ordered=False)
            numbers.append(number_match.group(1))
            continue

        flush_list(story, bullets, styles, ordered=False)
        flush_list(story, numbers, styles, ordered=True)

        if stripped.startswith("## "):
            if stripped.startswith("## Step ") and len(story) > 8:
                story.append(Spacer(1, 6))
            story.append(Paragraph(clean_inline(stripped[3:]), styles["h1"]))
            story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#d7ded6"), spaceAfter=6))
        elif stripped.startswith("### "):
            story.append(Paragraph(clean_inline(stripped[4:]), styles["h2"]))
        elif stripped.endswith(":") and len(stripped) < 72:
            story.append(Paragraph(clean_inline(stripped), styles["label"]))
        else:
            style = styles["body"]
            story.append(Paragraph(clean_inline(stripped), style))

    flush_list(story, bullets, styles, ordered=False)
    flush_list(story, numbers, styles, ordered=True)
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    markdown = SOURCE.read_text(encoding="utf-8")
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.7 * inch,
        title="DIHWorld Audio Ideal Short Demos Handoff",
        author="DIHWorld Audio",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    template = PageTemplate(id="handoff", frames=[frame], onPage=footer)
    doc.addPageTemplates([template])
    doc.build(build_story(markdown))
    print(OUTPUT)


if __name__ == "__main__":
    main()
