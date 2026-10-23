import sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import pymupdf

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

PAGE_W, PAGE_H = A4
M_H = 13 * mm
M_V = 11 * mm
CW = PAGE_W - 2 * M_H

class CustomNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        self.setFont('DejaVu-Bold', 7)
        self.setFillColor(getattr(self, 'primary_color', colors.HexColor('#0f766e')))
        self.drawString(M_H, PAGE_H - 8 * mm, getattr(self, 'series_title', 'ПСИХОТЕРАПЕВТИЧЕСКИЙ ЖУРНАЛ'))
        self.setFont('DejaVu', 7)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawRightString(PAGE_W - M_H, PAGE_H - 8 * mm, "ПРАКТИКУМ САМОСТОЯТЕЛЬНОЙ ТЕРАПИИ")
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.5)
        self.line(M_H, PAGE_H - 9.5 * mm, PAGE_W - M_H, PAGE_H - 9.5 * mm)

        self.setFont('DejaVu', 6.8)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawString(M_H, 6.5 * mm, "Терапевтический протокол • Персональная психологическая практика • Ресурс")
        page_str = f"Страница {self._pageNumber} из {total_pages}"
        self.drawRightString(PAGE_W - M_H, 6.5 * mm, page_str)
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.5)
        self.line(M_H, 8.2 * mm, PAGE_W - M_H, 8.2 * mm)
        self.restoreState()

def make_canvas(title_str, primary_hex):
    class CanvasSubclass(CustomNumberedCanvas):
        def __init__(self, *args, **kwargs):
            self.series_title = title_str
            self.primary_color = colors.HexColor(primary_hex)
            super().__init__(*args, **kwargs)
    return CanvasSubclass

class PaletteBuilder:
    def __init__(self, p_hex, bg_hex, dark_hex):
        self.primary = colors.HexColor(p_hex)
        self.bg = colors.HexColor(bg_hex)
        self.dark = colors.HexColor(dark_hex)
        self.text = colors.HexColor('#0f172a')
        self.muted = colors.HexColor('#475569')
        self.line_c = colors.HexColor('#cbd5e1')
        self.warn_bg = colors.HexColor('#fff7ed')
        self.warn_border = colors.HexColor('#ea580c')
        
        self.s_title = ParagraphStyle('T1', fontName='DejaVu-Bold', fontSize=10, leading=13, textColor=self.dark, alignment=1)
        self.s_sub = ParagraphStyle('TSub', fontName='DejaVu', fontSize=7, leading=9, textColor=self.muted, alignment=1)
        self.s_head = ParagraphStyle('TH_H', fontName='DejaVu-Bold', fontSize=8, leading=10.5, textColor=self.dark)
        self.s_badge = ParagraphStyle('TH_B', fontName='DejaVu-Bold', fontSize=6.8, leading=8.8, textColor=self.primary, alignment=2)
        self.s_bsub = ParagraphStyle('TH_BS', fontName='DejaVu', fontSize=5.8, leading=7.5, textColor=self.muted, alignment=2)
        self.s_body = ParagraphStyle('Body', fontName='DejaVu', fontSize=6.7, leading=9, textColor=self.text)
        self.s_body_b = ParagraphStyle('BodyB', fontName='DejaVu-Bold', fontSize=6.7, leading=9, textColor=self.text)
        self.s_muted = ParagraphStyle('Muted', fontName='DejaVu', fontSize=6.2, leading=8, textColor=self.muted)
        self.s_line = ParagraphStyle('Line', fontName='DejaVu', fontSize=6.2, leading=8, textColor=colors.HexColor('#94a3b8'))

    def timing_header(self, step_title, minutes, theory_min, practice_min):
        col1 = [Paragraph(f"📌 {step_title}", self.s_head)]
        col2 = [
            Paragraph(f"⏱ <b>Время: ~{minutes} мин</b>", self.s_badge),
            Paragraph(f"({theory_min} мин чтение • {practice_min} мин практика)", self.s_bsub)
        ]
        t = Table([[col1, col2]], colWidths=[122 * mm, 62 * mm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('TOPPADDING', (0,0), (-1,-1), 0.5),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('LINEBELOW', (0,0), (-1,-1), 0.6, self.primary),
        ]))
        return t

    def card(self, items, bg=None, border=None, padding=1.8):
        bg = bg or self.bg
        border = border or self.primary
        flow = []
        for x in items:
            flow.append(Paragraph(x, self.s_body) if isinstance(x, str) else x)
        t = Table([[flow]], colWidths=[CW])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('BOX', (0,0), (-1,-1), 0.5, border),
            ('TOPPADDING', (0,0), (-1,-1), padding),
            ('BOTTOMPADDING', (0,0), (-1,-1), padding),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))
        return t

    def invivo(self, title, context, instruction, success_metric, lines=2):
        head_s = ParagraphStyle('IV_H', fontName='DejaVu-Bold', fontSize=7, leading=8.8, textColor=colors.HexColor('#b45309'))
        txt_s = ParagraphStyle('IV_T', fontName='DejaVu', fontSize=6.4, leading=8.2, textColor=self.text)
        b_s = ParagraphStyle('IV_B', fontName='DejaVu-Bold', fontSize=6.4, leading=8.2, textColor=self.text)
        
        flow = [
            Paragraph(f"🎯 <b>ПОВЕДЕНЧЕСКИЙ ЭКСПЕРИМЕНТ В РЕАЛЬНОЙ ЖИЗНИ (IN VIVO): {title}</b>", head_s),
            Spacer(1, 0.5*mm),
            Paragraph(f"• <b>Где и когда провести:</b> {context}", txt_s),
            Paragraph(f"• <b>Что именно сделать:</b> {instruction}", txt_s),
            Paragraph(f"• <b>Критерий успеха:</b> {success_metric}", txt_s),
            Spacer(1, 0.4*mm),
            Paragraph("<b>Полевой отчёт (зафиксируйте реакцию тела и результат):</b>", b_s)
        ]
        for _ in range(lines):
            flow.append(Paragraph("____________________________________________________________________________________________________", self.s_line))
        t = Table([[flow]], colWidths=[CW])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), self.warn_bg),
            ('BOX', (0,0), (-1,-1), 0.6, self.warn_border),
            ('TOPPADDING', (0,0), (-1,-1), 1.8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))
        return t

    def table(self, data, widths, bg=None):
        bg = bg or self.bg
        t_rows = []
        for r_i, r in enumerate(data):
            row_flow = []
            for c in r:
                st = self.s_body_b if r_i == 0 else self.s_body
                row_flow.append(Paragraph(c, st) if isinstance(c, str) else c)
            t_rows.append(row_flow)
        t = Table(t_rows, colWidths=widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), bg),
            ('GRID', (0,0), (-1,-1), 0.5, self.line_c),
            ('TOPPADDING', (0,0), (-1,-1), 1.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ]))
        return t

    def lines(self, count=2, label="Моя рефлексия и записи:"):
        flow = [Paragraph(f"<b>{label}</b>", self.s_body_b)]
        for _ in range(count):
            flow.append(Paragraph("____________________________________________________________________________________________________", self.s_line))
        return flow

print("PaletteBuilder setup complete.")
