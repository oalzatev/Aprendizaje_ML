#!/usr/bin/env python3
"""
Generate professional PDF report for ML Project - Entrega 1
Predicción del Precio de Bolsa de Energía Eléctrica en Colombia
"""

import os
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ──────────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────────
BASE = Path("/home/user/workspace/ml-proyecto")
FIGURES = BASE / "figures"
OUTPUT = BASE / "report" / "reporte_entrega1.pdf"
FONT_DIR = Path("/tmp/fonts")

# ──────────────────────────────────────────────────
# COLORS
# ──────────────────────────────────────────────────
TEAL = HexColor("#01696F")
TEAL_DARK = HexColor("#0C4E54")
TEXT_COLOR = HexColor("#28251D")
TEXT_MUTED = HexColor("#7A7974")
BG_WHITE = HexColor("#FFFFFF")
BG_LIGHT = HexColor("#F7F6F2")
BG_ALT = HexColor("#EDF7F7")  # light teal for alternating rows
BORDER_COLOR = HexColor("#D4D1CA")

# ──────────────────────────────────────────────────
# FONTS
# ──────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("DMSans", str(FONT_DIR / "DMSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Bold", str(FONT_DIR / "DMSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Medium", str(FONT_DIR / "DMSans-Medium.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Italic", str(FONT_DIR / "DMSans-Italic.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-BoldItalic", str(FONT_DIR / "DMSans-BoldItalic.ttf")))
registerFontFamily(
    "DMSans",
    normal="DMSans",
    bold="DMSans-Bold",
    italic="DMSans-Italic",
    boldItalic="DMSans-BoldItalic",
)

# ──────────────────────────────────────────────────
# PAGE SIZE AND MARGINS
# ──────────────────────────────────────────────────
PAGE_W, PAGE_H = A4  # 595.27, 841.89 points
MARGIN = 2.5 * cm

# ──────────────────────────────────────────────────
# STYLES
# ──────────────────────────────────────────────────
styles = getSampleStyleSheet()

# Body text
body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["Normal"],
    fontName="DMSans",
    fontSize=10,
    leading=15,
    spaceAfter=8,
    spaceBefore=2,
    textColor=TEXT_COLOR,
    alignment=TA_JUSTIFY,
)

# Section heading (14pt)
heading1_style = ParagraphStyle(
    "Heading1Custom",
    parent=styles["Heading1"],
    fontName="DMSans-Bold",
    fontSize=14,
    leading=18,
    spaceBefore=20,
    spaceAfter=10,
    textColor=TEAL,
    alignment=TA_LEFT,
)

# Subsection heading
heading2_style = ParagraphStyle(
    "Heading2Custom",
    parent=styles["Heading2"],
    fontName="DMSans-Bold",
    fontSize=12,
    leading=15,
    spaceBefore=14,
    spaceAfter=8,
    textColor=TEAL_DARK,
    alignment=TA_LEFT,
)

# Sub-subsection heading
heading3_style = ParagraphStyle(
    "Heading3Custom",
    parent=styles["Heading3"],
    fontName="DMSans-Medium",
    fontSize=11,
    leading=14,
    spaceBefore=10,
    spaceAfter=6,
    textColor=TEXT_COLOR,
    alignment=TA_LEFT,
)

# Bold body
bold_style = ParagraphStyle(
    "BoldBody",
    parent=body_style,
    fontName="DMSans-Bold",
)

# Italic body
italic_style = ParagraphStyle(
    "ItalicBody",
    parent=body_style,
    fontName="DMSans-Italic",
    textColor=TEXT_MUTED,
)

# Bullet
bullet_style = ParagraphStyle(
    "BulletCustom",
    parent=body_style,
    leftIndent=20,
    bulletIndent=8,
    spaceAfter=4,
    spaceBefore=2,
)

# Caption for figures
caption_style = ParagraphStyle(
    "CaptionCustom",
    parent=body_style,
    fontName="DMSans-Italic",
    fontSize=9,
    leading=12,
    alignment=TA_CENTER,
    textColor=TEXT_MUTED,
    spaceBefore=4,
    spaceAfter=12,
)

# Table cell text
cell_style = ParagraphStyle(
    "CellText",
    parent=body_style,
    fontSize=9,
    leading=12,
    spaceAfter=0,
    spaceBefore=0,
    alignment=TA_LEFT,
)

cell_center_style = ParagraphStyle(
    "CellCenter",
    parent=cell_style,
    alignment=TA_CENTER,
)

# Table header text
header_cell_style = ParagraphStyle(
    "HeaderCell",
    parent=cell_style,
    fontName="DMSans-Bold",
    textColor=white,
    fontSize=9,
    leading=12,
)

header_cell_center_style = ParagraphStyle(
    "HeaderCellCenter",
    parent=header_cell_style,
    alignment=TA_CENTER,
)

# Footnote style
footnote_style = ParagraphStyle(
    "FootnoteCustom",
    parent=body_style,
    fontSize=8,
    leading=10,
    textColor=TEXT_MUTED,
    spaceAfter=3,
)

# Cover styles
cover_title = ParagraphStyle(
    "CoverTitle",
    fontName="DMSans-Bold",
    fontSize=26,
    leading=32,
    textColor=TEAL,
    alignment=TA_CENTER,
    spaceAfter=12,
)

cover_subtitle = ParagraphStyle(
    "CoverSubtitle",
    fontName="DMSans-Medium",
    fontSize=14,
    leading=18,
    textColor=TEXT_COLOR,
    alignment=TA_CENTER,
    spaceAfter=8,
)

cover_info = ParagraphStyle(
    "CoverInfo",
    fontName="DMSans",
    fontSize=12,
    leading=16,
    textColor=TEXT_MUTED,
    alignment=TA_CENTER,
    spaceAfter=6,
)


# ──────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────
def make_table(headers, rows, col_widths=None, center_cols=None):
    """Create a styled table with teal header."""
    center_cols = center_cols or []
    
    # Build header row
    header_data = []
    for i, h in enumerate(headers):
        style = header_cell_center_style if i in center_cols else header_cell_style
        header_data.append(Paragraph(h, style))
    
    # Build data rows
    table_data = [header_data]
    for row in rows:
        row_data = []
        for i, cell in enumerate(row):
            style = cell_center_style if i in center_cols else cell_style
            row_data.append(Paragraph(str(cell), style))
        table_data.append(row_data)
    
    available_width = PAGE_W - 2 * MARGIN
    if col_widths is None:
        n = len(headers)
        col_widths = [available_width / n] * n
    
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "DMSans-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, 0), 0.5, TEAL),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("LINEAFTER", (0, 0), (-1, -1), 0.3, BORDER_COLOR),
        ("LINEBEFORE", (0, 0), (0, -1), 0.3, BORDER_COLOR),
        ("LINEAFTER", (-1, 0), (-1, -1), 0.3, BORDER_COLOR),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BG_WHITE, BG_ALT]),
    ]
    
    t.setStyle(TableStyle(style_cmds))
    return t


def add_figure(story, fig_path, caption_text, fig_num, max_width=None, max_height=None):
    """Add a figure with caption."""
    if max_width is None:
        max_width = PAGE_W - 2 * MARGIN
    if max_height is None:
        max_height = 14 * cm
    
    if os.path.exists(fig_path):
        img = Image(str(fig_path))
        iw, ih = img.imageWidth, img.imageHeight
        
        # Scale to fit
        scale = min(max_width / iw, max_height / ih, 1.0)
        img.drawWidth = iw * scale
        img.drawHeight = ih * scale
        img.hAlign = "CENTER"
        
        story.append(Spacer(1, 6))
        story.append(img)
        story.append(Paragraph(
            f"<b>Figura {fig_num}.</b> {caption_text}",
            caption_style
        ))
    else:
        story.append(Paragraph(
            f"<i>[Figura {fig_num} no encontrada: {fig_path}]</i>",
            italic_style
        ))


def bullet_list(items, story):
    """Add a bullet list to the story."""
    for item in items:
        story.append(Paragraph(
            f"<bullet>&bull;</bullet> {item}",
            bullet_style
        ))


# ──────────────────────────────────────────────────
# HEADER / FOOTER
# ──────────────────────────────────────────────────
def on_first_page(canvas, doc):
    """Cover page - no header/footer."""
    canvas.saveState()
    canvas.restoreState()


def on_later_pages(canvas, doc):
    """Header with course name, footer with page number."""
    canvas.saveState()
    
    # Header line
    y_header = PAGE_H - 1.5 * cm
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, y_header, PAGE_W - MARGIN, y_header)
    
    canvas.setFont("DMSans", 8)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, y_header + 4, "Aprendizaje de Máquina Aplicado — EAFIT")
    canvas.drawRightString(PAGE_W - MARGIN, y_header + 4, "Entrega 1")
    
    # Footer
    y_footer = 1.2 * cm
    canvas.setStrokeColor(BORDER_COLOR)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, y_footer + 6, PAGE_W - MARGIN, y_footer + 6)
    
    canvas.setFont("DMSans", 8)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawCentredString(PAGE_W / 2, y_footer - 2, f"Página {doc.page}")
    
    canvas.restoreState()


# ──────────────────────────────────────────────────
# BUILD DOCUMENT
# ──────────────────────────────────────────────────
doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    title="Predicción del Precio de Bolsa de Energía Eléctrica en Colombia — Entrega 1",
    author="Perplexity Computer",
    leftMargin=MARGIN,
    rightMargin=MARGIN,
    topMargin=3 * cm,  # Space for header
    bottomMargin=2.5 * cm,
)

story = []

# ══════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════
story.append(Spacer(1, 4 * cm))

# Decorative teal line
story.append(HRFlowable(
    width="60%", thickness=3, color=TEAL,
    spaceAfter=20, spaceBefore=0
))

story.append(Paragraph(
    "Predicción del Precio de Bolsa<br/>de Energía Eléctrica en Colombia",
    cover_title
))

story.append(Spacer(1, 0.5 * cm))

story.append(HRFlowable(
    width="40%", thickness=1.5, color=BORDER_COLOR,
    spaceAfter=16, spaceBefore=0
))

story.append(Paragraph(
    "Entrega 1: Comprensión del Problema, EDA y Baseline",
    cover_subtitle
))

story.append(Spacer(1, 1.5 * cm))

story.append(Paragraph(
    "Aprendizaje de Máquina Aplicado — EAFIT",
    cover_info
))
story.append(Paragraph(
    "Profesor: Marco Teran",
    cover_info
))
story.append(Paragraph(
    "Abril 2026",
    cover_info
))

story.append(Spacer(1, 3 * cm))

# Decorative bottom line
story.append(HRFlowable(
    width="80%", thickness=2, color=TEAL,
    spaceAfter=0, spaceBefore=0
))

story.append(PageBreak())

# ══════════════════════════════════════════════════
# SECTION 1: PLANTEAMIENTO DEL PROBLEMA
# ══════════════════════════════════════════════════
story.append(Paragraph("1. Planteamiento del Problema", heading1_style))

story.append(Paragraph(
    "El mercado eléctrico colombiano opera mediante un mecanismo de despacho por mérito de precios, "
    "en el cual XM (el operador del sistema) ordena las ofertas de los generadores de menor a mayor costo "
    "y despacha hasta cubrir la demanda. El precio de bolsa corresponde al precio de la última planta "
    "despachada (precio marginal del sistema). Este proceso se repite cada hora del día, y los generadores "
    "deben presentar sus ofertas con un día de anticipación (<i>day-ahead</i>).",
    body_style
))

story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>Pregunta de investigación:</b> ¿Es posible predecir con suficiente precisión el precio de bolsa "
    "ponderado nacional del día siguiente usando variables del mercado energético colombiano disponibles "
    'públicamente en la API XM/SIMEM?',
    body_style
))

story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>Justificación:</b> La incertidumbre en el precio de bolsa representa un riesgo financiero significativo. "
    "Según literatura colombiana, la variación diaria equivale aproximadamente a $10M COP por GWh/día para "
    "agentes medianos. Un modelo de predicción confiable permite optimizar estrategias de oferta, planificar "
    "despachos y gestionar contratos.",
    body_style
))

story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>Tipo de tarea ML:</b> Regresión supervisada — variable objetivo continua (COP/kWh).",
    body_style
))

# ══════════════════════════════════════════════════
# SECTION 2: DESCRIPCIÓN DE LOS DATOS
# ══════════════════════════════════════════════════
story.append(Paragraph("2. Descripción de los Datos", heading1_style))

story.append(Paragraph(
    'Fuente: API pública XM/SIMEM (<a href="https://www.simem.co" color="#01696F">simem.co</a>). '
    "Los datos son de acceso público y corresponden al Operador del Sistema Interconectado Nacional de Colombia.",
    body_style
))

story.append(Spacer(1, 8))

# Variables table
avail_w = PAGE_W - 2 * MARGIN
var_headers = ["Variable", "Dataset ID", "Descripción", "Tipo"]
var_rows = [
    ["Precio de Bolsa Ponderado", "96D56E", "Variable objetivo — precio PPBO nacional diario", "Target"],
    ["Máximo Precio Ofertado", "03ba47", "MPO Nacional — señal de estrategia de oferta", "Feature"],
    ["Precio de Escasez", "43D616", "Techo regulatorio del mercado", "Feature"],
    ["Demanda Comercial", "d55202", "Demanda total del sistema (promedio, máx, pico 18-21h)", "Feature"],
    ["Generación Real por Tipo", "E17D25", "Generación hidro, térmica, solar, eólica, ratio hidro", "Feature"],
    ["Aportes Hídricos en Energía", "BA1C55", "Aportes hídricos total nacional", "Feature"],
    ["Reservas Hidráulicas en %", "843497", "Nivel de embalses como % de capacidad útil", "Feature"],
]
var_widths = [avail_w * 0.22, avail_w * 0.10, avail_w * 0.55, avail_w * 0.13]
story.append(Paragraph("<b>Tabla 1.</b> Variables descargadas de la API XM/SIMEM.", caption_style))
story.append(make_table(var_headers, var_rows, col_widths=var_widths, center_cols=[1, 3]))

story.append(Spacer(1, 10))

bullet_list([
    "<b>Rango temporal:</b> 2023-02-01 a 2026-03-31",
    "<b>Total de observaciones:</b> 1,125 días",
    "<b>Features totales después de ingeniería:</b> 22",
], story)

# ══════════════════════════════════════════════════
# SECTION 3: HALLAZGOS DEL EDA
# ══════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph("3. Hallazgos del EDA", heading1_style))

# 3.1 Stats
story.append(Paragraph("3.1 Estadísticas del precio de bolsa", heading2_style))

bullet_list([
    "<b>Media:</b> ~471 COP/kWh  |  <b>Mediana:</b> ~350 COP/kWh  |  <b>Desv. Estándar:</b> ~400 COP/kWh",
    "<b>Mínimo:</b> ~102 COP/kWh  |  <b>Máximo:</b> ~3,683 COP/kWh",
    "<b>Coeficiente de variación:</b> &gt;100% — alta volatilidad",
    "El precio presenta asimetría positiva (cola derecha): hay días de precio extremadamente alto",
], story)

story.append(Spacer(1, 6))

# Figure 1 - mapa faltantes
add_figure(story, str(FIGURES / "fig1_mapa_faltantes.png"),
           "Mapa de valores faltantes por variable y fecha.", 1,
           max_height=9*cm)

# Figure 2 - serie precio
add_figure(story, str(FIGURES / "fig2_serie_precio_bolsa.png"),
           "Serie temporal del precio de bolsa ponderado nacional (COP/kWh).", 2,
           max_height=10*cm)

# Figure 3 - distribución
add_figure(story, str(FIGURES / "fig3_distribucion_precio.png"),
           "Distribución del precio de bolsa — histograma y boxplot.", 3,
           max_height=9*cm)

# 3.2 Correlaciones
story.append(Paragraph("3.2 Correlaciones principales con el precio de bolsa", heading2_style))

corr_headers = ["Variable", "Correlación"]
corr_rows = [
    ["MPO Promedio", "+0.998"],
    ["MPO Máximo", "+0.847"],
    ["Generación Térmica", "+0.795"],
    ["Ratio Hidro (%)", "-0.774"],
    ["Generación Hidro", "-0.701"],
    ["Demanda Máxima", "-0.462"],
    ["Aportes Hídricos", "-0.461"],
    ["Reservas Hidráulicas %", "-0.374"],
    ["Precio de Escasez", "+0.285"],
]
corr_widths = [avail_w * 0.60, avail_w * 0.40]
story.append(Paragraph("<b>Tabla 2.</b> Correlaciones con el precio de bolsa (ordenadas por magnitud).", caption_style))
story.append(make_table(corr_headers, corr_rows, col_widths=corr_widths, center_cols=[1]))

story.append(Spacer(1, 6))

# Figure 5 - correlaciones
add_figure(story, str(FIGURES / "fig5_correlaciones.png"),
           "Matriz de correlaciones entre variables principales.", 5,
           max_height=11*cm)

# 3.3 Patrones temporales
story.append(Paragraph("3.3 Patrones temporales", heading2_style))

bullet_list([
    "<b>Precios más altos en temporada seca</b> (diciembre-marzo): menor generación hidráulica disponible.",
    "El precio del día siguiente está fuertemente correlacionado con el precio actual (<b>autocorrelación alta a lag=1</b>).",
    "La media del precio en el conjunto de prueba (jul 2025 - mar 2026) es <b>208.56 COP/kWh</b>, significativamente "
    "menor que la media histórica de los 3 años (~471 COP/kWh), lo que indica un periodo de precios bajos.",
], story)

# 3.4 Calidad de datos
story.append(Paragraph("3.4 Calidad de datos", heading2_style))

bullet_list([
    "Valores faltantes tratados con <b>interpolación lineal</b> (mecanismo MAR).",
    "No se detectaron duplicados.",
    "Los outliers (picos de precio) se conservan: son información real del mercado, no errores.",
], story)

# ══════════════════════════════════════════════════
# SECTION 4: MÉTRICA DE EVALUACIÓN
# ══════════════════════════════════════════════════
story.append(Paragraph("4. Métrica de Evaluación", heading1_style))

story.append(Paragraph(
    "Se utilizan dos métricas complementarias:",
    body_style
))

story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>MAE (Error Absoluto Medio) — métrica principal:</b> Directamente interpretable en COP/kWh. "
    "Robusto a valores extremos. Responde a la pregunta: \"¿cuántos COP/kWh me equivoco en promedio?\"",
    body_style
))

story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>RMSE (Raíz del Error Cuadrático Medio) — métrica complementaria:</b> Castiga errores grandes. "
    "Útil para detectar si el modelo falla en días de alta volatilidad. Sistemáticamente mayor que el "
    "MAE dado el alto coeficiente de variación del precio.",
    body_style
))

story.append(Spacer(1, 4))

story.append(Paragraph(
    "Ambas métricas también se reportan como porcentaje de la media del conjunto de prueba para "
    "facilitar la comparación entre modelos.",
    body_style
))

# ══════════════════════════════════════════════════
# SECTION 5: BASELINES Y DIFICULTAD DEL PROBLEMA
# ══════════════════════════════════════════════════
story.append(Paragraph("5. Baselines y Dificultad del Problema", heading1_style))

story.append(Paragraph(
    "Se construyeron tres baselines para establecer el nivel de referencia mínimo:",
    body_style
))

story.append(Spacer(1, 8))

# Baselines table
bl_headers = ["Baseline", "MAE (val)", "RMSE (val)", "MAE (test)", "RMSE (test)", "MAE/Media test"]
bl_rows = [
    ["B1 — Persistencia", "33.81", "55.66", "27.65", "39.72", "13.3%"],
    ["B2 — Media Móvil 7d", "46.43", "73.56", "43.41", "57.08", "20.8%"],
    ["B3 — Reg. Lineal (lags)", "44.80", "60.62", "38.75", "49.47", "18.6%"],
]
bl_widths = [avail_w * 0.24, avail_w * 0.13, avail_w * 0.14, avail_w * 0.14, avail_w * 0.14, avail_w * 0.21]
story.append(Paragraph("<b>Tabla 3.</b> Resultados de los baselines en validación y test.", caption_style))
story.append(make_table(bl_headers, bl_rows, col_widths=bl_widths, center_cols=[1, 2, 3, 4, 5]))

story.append(Spacer(1, 10))

story.append(Paragraph("<b>Descripción de los baselines:</b>", body_style))

bullet_list([
    "<b>B1 Persistencia:</b> precio_mañana = precio_hoy. Captura la fuerte autocorrelación a lag=1.",
    "<b>B2 Media Móvil 7 días:</b> promedio de los últimos 7 días. Suaviza volatilidad.",
    "<b>B3 Regresión Lineal:</b> modelo entrenado usando solo lags del precio y variables temporales.",
], story)

story.append(Spacer(1, 6))

# Figure 7 - baselines
add_figure(story, str(FIGURES / "fig7_baselines_vs_real.png"),
           "Comparación de baselines vs. precio real en el conjunto de test.", 7,
           max_height=10*cm)

story.append(Spacer(1, 6))

story.append(Paragraph(
    "<b>Conclusión sobre la dificultad:</b> El problema es de dificultad media-alta. El baseline de persistencia "
    "(B1) logra un MAE de 27.65 COP/kWh en test (13.3% de error relativo), estableciendo un piso competitivo "
    "difícil de superar. Cualquier modelo de ML debe demostrar una mejora significativa sobre este baseline "
    "para justificar su complejidad.",
    body_style
))

# ══════════════════════════════════════════════════
# SECTION 6: SPLIT TEMPORAL
# ══════════════════════════════════════════════════
story.append(Paragraph("6. Split Temporal", heading1_style))

split_headers = ["Conjunto", "Período", "Observaciones", "Proporción"]
split_rows = [
    ["Entrenamiento", "2023-03-03 a 2024-12-31", "670", "59.6%"],
    ["Validación", "2025-01-01 a 2025-06-30", "181", "16.1%"],
    ["Test", "2025-07-01 a 2026-03-31", "274", "24.4%"],
]
split_widths = [avail_w * 0.20, avail_w * 0.35, avail_w * 0.20, avail_w * 0.25]
story.append(Paragraph("<b>Tabla 4.</b> División temporal del dataset.", caption_style))
story.append(make_table(split_headers, split_rows, col_widths=split_widths, center_cols=[2, 3]))

story.append(Spacer(1, 10))

story.append(Paragraph(
    "División cronológica estricta para evitar <i>data leakage</i>. El conjunto de test no se toca "
    "hasta la evaluación final.",
    body_style
))

# ══════════════════════════════════════════════════
# SECTION 7: CONCLUSIONES Y PRÓXIMOS PASOS
# ══════════════════════════════════════════════════
story.append(Paragraph("7. Conclusiones y Próximos Pasos", heading1_style))

story.append(Paragraph(
    "El EDA confirma que el precio de bolsa en Colombia está principalmente determinado por la dinámica "
    "hidro-térmica del sistema: cuando la generación hidráulica domina (ratio_hidro alto, embalses llenos, "
    "aportes abundantes), los precios son bajos; cuando entra la generación térmica (más costosa), los "
    "precios suben. El MPO tiene correlación de 0.998 con el precio, lo que sugiere que la estrategia de "
    "oferta de los generadores es el principal determinante inmediato del precio.",
    body_style
))

story.append(Spacer(1, 6))

story.append(Paragraph(
    "Para la <b>Entrega 2</b> se compararán al menos dos familias adicionales de modelos "
    "(XGBoost/LightGBM y SARIMAX/VAR) contra los baselines usando validación temporal walk-forward, "
    "análisis de importancia de features y métricas MAE y RMSE.",
    body_style
))

# ══════════════════════════════════════════════════
# FUENTES
# ══════════════════════════════════════════════════
story.append(Spacer(1, 16))
story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceAfter=8))
story.append(Paragraph("Fuentes", heading2_style))

story.append(Paragraph(
    '1. González Pérez, L.F. &amp; Urbano Buriticá, S.N. (2022). <i>Predicción de corto plazo del precio '
    'de bolsa de energía en el mercado colombiano.</i> Tesis de Maestría, Universidad de los Andes.',
    footnote_style
))

story.append(Paragraph(
    '2. Villarreal Marimon, Y.J. &amp; Flores San Martín, L.A. (2023). <i>Modelos de predicción del precio '
    'de la energía en bolsa en Colombia.</i> Tesis de Maestría, EAFIT.',
    footnote_style
))

story.append(Paragraph(
    '3. XM S.A. E.S.P. — API SIMEM: '
    '<a href="https://www.simem.co" color="#01696F">https://www.simem.co</a>',
    footnote_style
))

# ──────────────────────────────────────────────────
# BUILD
# ──────────────────────────────────────────────────
doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
print(f"PDF generated: {OUTPUT}")
print(f"File size: {OUTPUT.stat().st_size / 1024:.1f} KB")
