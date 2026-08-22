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
    HRFlowable,
    Image,
    LongTable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "DIHWORLD_PRICING_TEAM_HANDOFF_20260822.md"
OUTPUT = ROOT / "output" / "pdf" / "DIHWorld_Pricing_Team_Handoff_20260822.pdf"
LOGO = ROOT / "assets" / "images" / "dihworld-audio-logo.jpg"

INK = colors.HexColor("#151515")
CREAM = colors.HexColor("#FBFAF7")
GOLD = colors.HexColor("#C9A348")
WINE = colors.HexColor("#73263C")
TEAL = colors.HexColor("#13766F")
MUTED = colors.HexColor("#62625E")
LINE = colors.HexColor("#DEDed8")
PALE_GOLD = colors.HexColor("#F4EBD4")
PALE_GREEN = colors.HexColor("#EDF4F1")


def esc(text: str) -> str:
    return (
        text.strip()
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover_brand": ParagraphStyle(
            "CoverBrand",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            alignment=TA_CENTER,
            textColor=GOLD,
            spaceAfter=12,
        ),
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=29,
            leading=32,
            alignment=TA_CENTER,
            textColor=INK,
            spaceAfter=14,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            textColor=MUTED,
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=INK,
            spaceBefore=12,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=WINE,
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=13.1,
            textColor=colors.HexColor("#292925"),
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=12.7,
            leftIndent=14,
            firstLineIndent=-9,
            textColor=colors.HexColor("#292925"),
            spaceAfter=4,
        ),
        "table_head": ParagraphStyle(
            "TableHead",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.7,
            leading=9.5,
            textColor=colors.white,
        ),
        "table_body": ParagraphStyle(
            "TableBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=INK,
        ),
        "table_body_bold": ParagraphStyle(
            "TableBodyBold",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9.5,
            textColor=INK,
        ),
        "status": ParagraphStyle(
            "Status",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=WINE,
        ),
    }


def footer(canvas, doc):
    canvas.saveState()
    width, height = letter
    if doc.page > 1:
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.setFillColor(GOLD)
        canvas.drawString(0.65 * inch, height - 0.38 * inch, "DIHWORLD AUDIO")
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(width - 0.65 * inch, height - 0.38 * inch, "PRICING TEAM HANDOFF")
    canvas.setStrokeColor(LINE)
    canvas.line(0.65 * inch, 0.52 * inch, width - 0.65 * inch, 0.52 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.65 * inch, 0.34 * inch, "Proposed - team review required")
    canvas.drawRightString(width - 0.65 * inch, 0.34 * inch, f"Page {doc.page}")
    canvas.restoreState()


def cover(story, st):
    story.append(Spacer(1, 0.7 * inch))
    if LOGO.exists():
        logo = Image(str(LOGO), width=0.92 * inch, height=0.92 * inch)
        logo.hAlign = "CENTER"
        story.append(logo)
        story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph("DIHWORLD AUDIO", st["cover_brand"]))
    story.append(Paragraph("Pricing Team Handoff", st["cover_title"]))
    story.append(HRFlowable(width="34%", thickness=2, color=GOLD, spaceBefore=4, spaceAfter=18))
    story.append(Paragraph("Proposed price ladder, processor-tier logic, Lifetime benefits, and approval checklist", st["cover_sub"]))
    story.append(Spacer(1, 0.34 * inch))

    status = Table(
        [[Paragraph("PROPOSED - TEAM REVIEW REQUIRED", st["status"])],
         [Paragraph("No price or Lifetime term in this handoff is final until the team approves it.", st["cover_sub"])]],
        colWidths=[5.65 * inch],
    )
    status.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_GOLD),
        ("BOX", (0, 0), (-1, -1), 0.8, GOLD),
        ("TOPPADDING", (0, 0), (-1, 0), 11),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("TOPPADDING", (0, 1), (-1, 1), 3),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 11),
    ]))
    status.hAlign = "CENTER"
    story.append(status)
    story.append(Spacer(1, 0.45 * inch))

    meta_style = ParagraphStyle(
        "Meta",
        parent=st["body"],
        fontSize=9,
        leading=12,
        spaceAfter=0,
    )
    meta = Table([
        [Paragraph("Prepared", st["table_body_bold"]), Paragraph("August 22, 2026", meta_style)],
        [Paragraph("Decision owner", st["table_body_bold"]), Paragraph("____________________________", meta_style)],
        [Paragraph("Target approval", st["table_body_bold"]), Paragraph("____________________________", meta_style)],
        [Paragraph("Final decision", st["table_body_bold"]), Paragraph("APPROVE / REVISE / HOLD", meta_style)],
    ], colWidths=[1.45 * inch, 4.2 * inch])
    meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    meta.hAlign = "CENTER"
    story.append(meta)
    story.append(PageBreak())


def widths_for(headers: list[str]) -> list[float]:
    key = headers[0].lower()
    if key == "offer":
        return [2.55 * inch, 0.9 * inch, 0.9 * inch, 2.15 * inch]
    if key == "family":
        return [2.95 * inch, 0.75 * inch, 1.05 * inch, 1.05 * inch]
    if key == "bundle":
        return [1.38 * inch, 0.72 * inch, 0.72 * inch, 3.68 * inch]
    if key == "decision":
        return [2.7 * inch, 0.7 * inch, 0.7 * inch, 2.4 * inch]
    return [6.5 * inch / len(headers)] * len(headers)


def make_table(rows: list[list[str]], st):
    wrapped = []
    for row_index, row in enumerate(rows):
        current = []
        for col_index, value in enumerate(row):
            style = st["table_head"] if row_index == 0 else (
                st["table_body_bold"] if col_index == 0 else st["table_body"]
            )
            current.append(Paragraph(esc(value), style))
        wrapped.append(current)
    table = LongTable(wrapped, colWidths=widths_for(rows[0]), repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for idx in range(1, len(rows)):
        commands.append(("BACKGROUND", (0, idx), (-1, idx), CREAM if idx % 2 else PALE_GREEN))
    table.setStyle(TableStyle(commands))
    return table


def body_story(markdown: str, st):
    story = []
    lines = markdown.splitlines()
    idx = 0
    page_break_before = {
        "Proposed Public Price Ladder",
        "Proposed Family Prices",
        "Proposed Workflow Bundles",
        "Lifetime Membership - Confirmed Benefits",
        "Competitive Presentation Direction",
        "Team Decision Checklist",
    }
    seen_content = False

    while idx < len(lines):
        stripped = lines[idx].strip()
        if not stripped or stripped.startswith("# DIHWorld Audio Pricing Team Handoff"):
            idx += 1
            continue
        if re.match(r"^(Date|Status|Decision owner|Target approval date):", stripped):
            idx += 1
            continue

        if stripped.startswith("## "):
            title = stripped[3:]
            if seen_content and title in page_break_before:
                story.append(PageBreak())
            story.append(Paragraph(esc(title), st["h1"]))
            story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=8))
            seen_content = True
            idx += 1
            continue

        if stripped.startswith("### "):
            story.append(Paragraph(esc(stripped[4:]), st["h2"]))
            idx += 1
            continue

        if stripped.startswith("| "):
            table_lines = []
            while idx < len(lines) and lines[idx].strip().startswith("|"):
                table_lines.append(lines[idx].strip())
                idx += 1
            rows = []
            for table_index, line in enumerate(table_lines):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                if table_index == 1 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    continue
                rows.append(cells)
            story.append(make_table(rows, st))
            story.append(Spacer(1, 8))
            continue

        if stripped.startswith("- "):
            story.append(Paragraph(f"<font color='#13766F'>&#8226;</font> {esc(stripped[2:])}", st["bullet"]))
            idx += 1
            continue

        if stripped.startswith("Final decision:") or stripped.startswith("Approved by:") or stripped.startswith("Notes:"):
            story.append(Paragraph(f"<b>{esc(stripped)}</b>", st["body"]))
            idx += 1
            continue

        story.append(Paragraph(esc(stripped), st["body"]))
        idx += 1

    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    markdown = SOURCE.read_text(encoding="utf-8")
    st = styles()
    story = []
    cover(story, st)
    story.extend(body_story(markdown, st))

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.7 * inch,
        title="DIHWorld Audio Pricing Team Handoff",
        author="DIHWorld Audio",
        subject="Proposed pricing and Lifetime membership decisions",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="handoff", frames=[frame], onPage=footer)])
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    main()
