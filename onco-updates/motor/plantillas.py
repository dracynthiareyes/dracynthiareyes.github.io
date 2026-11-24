"""Generador de HTML/CSS (1080x1350) y caption.md para OncoUpdates."""

from __future__ import annotations

from html import escape
from paletas import PALETAS

ICONOS_SVG = {
    "alerta": '<circle cx="12" cy="12" r="9"/><path d="M12 8v5"/><path d="M12 16h.01"/>',
    "reloj": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "corazon": '<path d="M12 21s-7-4.5-7-10.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 7 3.5C19 16.5 12 21 12 21z"/>',
    "escudo": '<path d="M12 2l7 4v6c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6l7-4z"/><path d="M9.5 12.5l1.8 1.8 3.7-3.8"/>',
    "lupa": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/>',
    "calendario": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
    "estetoscopio": '<path d="M6 4v6a4 4 0 0 0 8 0V4"/><path d="M10 14v3a4 4 0 0 0 8 0v-3"/><circle cx="18" cy="12" r="2"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/>',
}


def _svg(nombre: str, color: str, size: int = 28) -> str:
    path = ICONOS_SVG.get(nombre, ICONOS_SVG["check"])
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f"{path}</svg>"
    )


def _render_titulo(titulo: str, highlight: str | None) -> str:
    if highlight and highlight in titulo:
        partes = titulo.split(highlight, 1)
        return (
            f"{escape(partes[0])}"
            f'<span class="highlight">{escape(highlight)}</span>'
            f"{escape(partes[1])}"
        )
    return escape(titulo)


def _render_body_grid_2x2(items: list[dict], p: dict) -> str:
    cards = []
    for idx, item in enumerate(items[:4], start=1):
        icono = _svg(item.get("icono", "check"), p["accent"], 28)
        cards.append(
            f"""      <article class="card">
        <div class="card-top">
          <div class="icon-box">{icono}</div>
          <span class="card-num">{idx:02d}</span>
        </div>
        <h2>{escape(item["titulo"])}</h2>
        <p>{escape(item["texto"])}</p>
      </article>"""
        )
    return '<section class="grid-2x2">\n' + "\n".join(cards) + "\n    </section>"


def _render_body_steps_3(items: list[dict], p: dict) -> str:
    steps = []
    for idx, item in enumerate(items[:3], start=1):
        steps.append(
            f"""      <article class="step-card">
        <div class="step-badge">{idx:02d}</div>
        <div class="step-content">
          <h2>{escape(item["titulo"])}</h2>
          <p>{escape(item["texto"])}</p>
        </div>
      </article>"""
        )
    return '<section class="steps-3">\n' + "\n".join(steps) + "\n    </section>"


def _render_body_myth_reality(items: list[dict], p: dict) -> str:
    rows = []
    for item in items[:3]:
        rows.append(
            f"""      <article class="mr-row">
        <div class="mr-box mr-myth">
          <span class="mr-tag">Mito</span>
          <p>{escape(item["mito"])}</p>
        </div>
        <div class="mr-box mr-fact">
          <span class="mr-tag">Realidad médica</span>
          <p>{escape(item["realidad"])}</p>
        </div>
      </article>"""
        )
    return '<section class="myth-reality">\n' + "\n".join(rows) + "\n    </section>"


def _render_body_checklist(items: list[dict], p: dict) -> str:
    checks = []
    for item in items[:4]:
        icono = _svg("check", p["accent"], 26)
        checks.append(
            f"""      <article class="check-item">
        <div class="check-icon">{icono}</div>
        <div class="check-text">
          <h2>{escape(item["titulo"])}</h2>
          <p>{escape(item["texto"])}</p>
        </div>
      </article>"""
        )
    return '<section class="checklist">\n' + "\n".join(checks) + "\n    </section>"


def generar_html(data: dict, logo_rel_path: str = "../../../assets/logo-cr.png") -> str:
    """Genera un HTML autocontenido de 1080x1350 para renderizar con Chrome headless."""
    paleta_id = data["paleta"]
    layout = data["layout"]
    p = PALETAS[paleta_id]
    num_str = f"{int(data['numero']):02d}"

    renderers = {
        "grid_2x2": _render_body_grid_2x2,
        "steps_3": _render_body_steps_3,
        "myth_reality": _render_body_myth_reality,
        "checklist": _render_body_checklist,
    }
    if layout not in renderers:
        raise ValueError(f"Layout no soportado: {layout}")

    body_html = renderers[layout](data["items"], p)
    titulo_html = _render_titulo(data["titulo"], data.get("titulo_destacado"))

    callout = data.get("callout") or {}
    callout_html = ""
    if callout:
        callout_html = f"""
    <section class="callout">
      <div class="callout-badge">
        <span class="big">{escape(callout.get("badge_grande", "Clave"))}</span>
        <span class="small">{escape(callout.get("badge_chico", "Médica"))}</span>
      </div>
      <div class="callout-text">
        <h3>{escape(callout["titulo"])}</h3>
        <p>{escape(callout["texto"])}</p>
      </div>
    </section>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>OncoUpdates {num_str} — {escape(data["titulo"])}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 1080px;
      height: 1350px;
      overflow: hidden;
      font-family: "Avenir Next", -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
      background: {p["bg"]};
      color: {p["text"]};
      -webkit-font-smoothing: antialiased;
    }}
    .canvas {{
      position: relative;
      width: 1080px;
      height: 1350px;
      padding: 46px 58px 42px 58px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: {p["canvas_bg"]};
    }}
    .frame-accent {{
      position: absolute;
      inset: 22px;
      border: 1.5px solid {p["frame_border"]};
      border-radius: 28px;
      pointer-events: none;
    }}
    .header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 2;
    }}
    .badges {{ display: flex; align-items: center; gap: 14px; }}
    .badge-onco {{
      background: {p["badge_grad"]};
      color: #FFFFFF;
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0.05em;
      padding: 11px 24px;
      border-radius: 999px;
      box-shadow: 0 6px 18px {p["badge_shadow"]};
    }}
    .badge-cat {{
      background: {p["cat_bg"]};
      border: 1.5px solid {p["cat_border"]};
      color: {p["cat_text"]};
      font-size: 18px;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 10px 20px;
      border-radius: 999px;
    }}
    .logo-wrap {{
      width: 88px;
      height: 88px;
      border-radius: 50%;
      background: #FFFFFF;
      padding: 4px;
      box-shadow: 0 8px 24px {p["card_shadow"]};
      border: 1.5px solid {p["gold"]};
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .logo-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 50%;
    }}
    .hero {{ z-index: 2; }}
    .hero h1 {{
      font-family: "Georgia", "Palatino", serif;
      font-size: 52px;
      line-height: 1.12;
      font-weight: 700;
      color: {p["title"]};
      letter-spacing: -0.01em;
    }}
    .hero h1 .highlight {{ color: {p["accent"]}; font-style: italic; }}
    .hero-divider {{
      width: 88px;
      height: 4px;
      background: {p["divider_grad"]};
      border-radius: 4px;
      margin: 14px 0 12px 0;
    }}
    .hero p {{
      font-size: 23px;
      line-height: 1.38;
      color: {p["text_muted"]};
      font-weight: 500;
      max-width: 940px;
    }}

    /* Layout 1: Grid 2x2 */
    .grid-2x2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      z-index: 2;
    }}
    .card {{
      background: {p["card_bg"]};
      border: 1.5px solid {p["card_border"]};
      border-radius: 24px;
      padding: 24px 26px;
      box-shadow: 0 12px 30px {p["card_shadow"]};
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .card-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .icon-box {{
      width: 52px;
      height: 52px;
      border-radius: 15px;
      background: {p["icon_bg"]};
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .card-num {{
      font-family: "Georgia", serif;
      font-size: 26px;
      font-weight: 700;
      color: {p["num_color"]};
    }}
    .card h2 {{ font-size: 24px; font-weight: 700; color: {p["title"]}; line-height: 1.22; }}
    .card p {{ font-size: 19px; line-height: 1.42; color: {p["text_muted"]}; }}

    /* Layout 2: 3 Steps */
    .steps-3 {{
      display: flex;
      flex-direction: column;
      gap: 18px;
      z-index: 2;
    }}
    .step-card {{
      background: {p["card_bg"]};
      border: 1.5px solid {p["card_border"]};
      border-left: 6px solid {p["accent"]};
      border-radius: 22px;
      padding: 22px 28px;
      box-shadow: 0 10px 26px {p["card_shadow"]};
      display: flex;
      align-items: center;
      gap: 24px;
    }}
    .step-badge {{
      flex-shrink: 0;
      width: 66px;
      height: 66px;
      border-radius: 18px;
      background: {p["badge_grad"]};
      color: #FFFFFF;
      font-family: "Georgia", serif;
      font-size: 28px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .step-content h2 {{ font-size: 25px; font-weight: 700; color: {p["title"]}; margin-bottom: 6px; }}
    .step-content p {{ font-size: 19.5px; line-height: 1.42; color: {p["text_muted"]}; }}

    /* Layout 3: Myth vs Reality */
    .myth-reality {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      z-index: 2;
    }}
    .mr-row {{
      display: grid;
      grid-template-columns: 1fr 1.25fr;
      gap: 16px;
    }}
    .mr-box {{
      border-radius: 20px;
      padding: 18px 22px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      box-shadow: 0 8px 22px {p["card_shadow"]};
    }}
    .mr-myth {{
      background: rgba(255, 255, 255, 0.72);
      border: 1.5px dashed {p["card_border"]};
    }}
    .mr-fact {{
      background: {p["card_bg"]};
      border: 1.5px solid {p["accent"]};
    }}
    .mr-tag {{
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: {p["accent"]};
    }}
    .mr-myth .mr-tag {{ color: {p["text_muted"]}; }}
    .mr-box p {{ font-size: 18.5px; line-height: 1.38; color: {p["text"]}; font-weight: 500; }}

    /* Layout 4: Checklist */
    .checklist {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      z-index: 2;
    }}
    .check-item {{
      background: {p["card_bg"]};
      border: 1.5px solid {p["card_border"]};
      border-radius: 20px;
      padding: 18px 24px;
      box-shadow: 0 8px 22px {p["card_shadow"]};
      display: flex;
      align-items: flex-start;
      gap: 18px;
    }}
    .check-icon {{
      flex-shrink: 0;
      width: 46px;
      height: 46px;
      border-radius: 14px;
      background: {p["icon_bg"]};
      display: flex;
      align-items: center;
      justify-content: center;
      margin-top: 2px;
    }}
    .check-text h2 {{ font-size: 22px; font-weight: 700; color: {p["title"]}; margin-bottom: 4px; }}
    .check-text p {{ font-size: 18.5px; line-height: 1.38; color: {p["text_muted"]}; }}

    /* Callout */
    .callout {{
      background: {p["callout_bg"]};
      border-radius: 22px;
      padding: 20px 28px;
      display: flex;
      align-items: center;
      gap: 22px;
      z-index: 2;
      box-shadow: 0 12px 28px {p["badge_shadow"]};
    }}
    .callout-badge {{
      flex-shrink: 0;
      background: {p["callout_badge_bg"]};
      border: 1.5px solid {p["gold"]};
      border-radius: 16px;
      padding: 12px 18px;
      text-align: center;
      min-width: 112px;
    }}
    .callout-badge .big {{
      display: block;
      font-family: "Georgia", serif;
      font-size: 26px;
      font-weight: 700;
      color: #FFFFFF;
      line-height: 1.1;
    }}
    .callout-badge .small {{
      display: block;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: {p["callout_sub"]};
      margin-top: 3px;
    }}
    .callout-text h3 {{ font-size: 21px; font-weight: 700; color: {p["callout_text"]}; margin-bottom: 4px; }}
    .callout-text p {{ font-size: 18px; line-height: 1.38; color: {p["callout_sub"]}; }}

    /* Footer */
    .footer {{
      z-index: 2;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .footer-main {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 4px;
    }}
    .brand-info {{ display: flex; flex-direction: column; gap: 3px; }}
    .handle {{ font-size: 27px; font-weight: 700; color: {p["dark"]}; letter-spacing: -0.01em; }}
    .credentials {{ font-size: 17px; font-weight: 500; color: {p["text_muted"]}; }}
    .cta-pill {{
      background: {p["cta_bg"]};
      border: 2px solid {p["cta_border"]};
      border-radius: 999px;
      padding: 12px 24px;
      text-align: right;
      box-shadow: 0 6px 16px {p["card_shadow"]};
    }}
    .cta-pill .cta-title {{ font-size: 18px; font-weight: 700; color: {p["cta_title"]}; display: block; }}
    .cta-pill .cta-sub {{ font-size: 15px; font-weight: 600; color: {p["cta_sub"]}; display: block; margin-top: 2px; }}
    .source-bar {{
      border-top: 1px solid {p["footer_border"]};
      padding-top: 10px;
      font-size: 14.5px;
      line-height: 1.35;
      color: {p["text_muted"]};
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
    }}
    .source-bar strong {{ color: {p["dark"]}; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="canvas">
    <div class="frame-accent"></div>

    <header class="header">
      <div class="badges">
        <span class="badge-onco">OncoUpdates · {num_str}</span>
        <span class="badge-cat">{escape(data["categoria_nombre"])}</span>
      </div>
      <div class="logo-wrap">
        <img src="{escape(logo_rel_path)}" alt="Logo Dra. Cynthia Reyes" />
      </div>
    </header>

    <section class="hero">
      <h1>{titulo_html}</h1>
      <div class="hero-divider"></div>
      <p>{escape(data["subtitulo"])}</p>
    </section>

    {body_html}
    {callout_html}

    <footer class="footer">
      <div class="footer-main">
        <div class="brand-info">
          <span class="handle">@dracynthiareyes</span>
          <span class="credentials">Dra. Cynthia Reyes López · Ginecología Oncológica · WTC CDMX y Consulta Virtual</span>
        </div>
        <div class="cta-pill">
          <span class="cta-title">Agenda tu consulta</span>
          <span class="cta-sub">Datos de contacto en la bio</span>
        </div>
      </div>
      <div class="source-bar">
        <span><strong>Fuente:</strong> {escape(data["fuente"])}</span>
        <span>Contenido educativo · No sustituye consulta médica</span>
      </div>
    </footer>
  </div>
</body>
</html>
"""


def generar_caption(data: dict) -> str:
    """Genera el texto (caption.md) siguiendo las reglas de AGENTS.md."""
    hashtags_base = ["#OncoUpdates", "#DraCynthiaReyes", "#GinecologiaOncologica"]
    extras = [h if h.startswith("#") else f"#{h}" for h in data.get("hashtags", [])]
    todos_hashtags = " ".join(dict.fromkeys(hashtags_base + extras))

    aclaracion = data.get(
        "aclaracion",
        "Recuerda que presentar dudas o síntomas no equivale automáticamente a un diagnóstico de cáncer, pero sí amerita una valoración oportuna y especializada.",
    )
    return (
        f"{data['caption_intro'].strip()}\n\n"
        f"{data['caption_cuerpo'].strip()}\n\n"
        f"{aclaracion.strip()}\n\n"
        f"Agenda tu consulta presencial en WTC Ciudad de México o en modalidad virtual — "
        f"encuentra todos los datos de contacto en la bio de @dracynthiareyes.\n\n"
        f"Fuente clínica: {data['fuente'].strip()}\n"
        f"Contenido educativo · No sustituye una consulta médica.\n\n"
        f"{todos_hashtags}\n"
    )
