from fpdf import FPDF
from unidecode import unidecode
from fpdf.enums import XPos, YPos


def text_to_pdf(text: str) -> bytes:
    if not text:
        text = "Bo'sh matn"

    replacements = {
        '•': '-', '·': '-', '◦': '-', '▪': '-', '▸': '-',
        '→': '->', '←': '<-', '↑': '^', '↓': 'v',
        '©': '(c)', '®': '(r)', '™': '(tm)',
        '…': '...', '—': '-', '–': '-',
        '\u02bc': "'", '\u02bb': "'",
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\t': '  ',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    text = unidecode(text)
    text = ''.join(c if 32 <= ord(c) <= 126 or c == '\n' else ' ' for c in text)

    lines = text.split('\n')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_font("helvetica", size=10)
    effective_width = pdf.w - pdf.l_margin - pdf.r_margin

    for line in lines:
        try:
            cleaned = line.lstrip()
            if cleaned:
                pdf.multi_cell(
                    effective_width,
                    6,
                    txt=cleaned,
                    align='L',
                    new_x=XPos.LMARGIN,  # har qatordan keyin chap marginga qayt
                    new_y=YPos.NEXT,     # pastga tush
                )
            else:
                pdf.ln(4)
        except Exception:
            try:
                words = line.lstrip().split()
                if words:
                    pdf.multi_cell(
                        effective_width, 6,
                        txt=' '.join(words),
                        align='L',
                        new_x=XPos.LMARGIN,
                        new_y=YPos.NEXT,
                    )
            except Exception:
                continue

    return bytes(pdf.output())