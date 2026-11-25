#!/usr/bin/env python3
"""Motor reutilizable para generar entregas de OncoUpdates (HTML, PNG 1080x1350 y caption.md)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

MOTOR_DIR = Path(__file__).resolve().parent
ONCO_DIR = MOTOR_DIR.parent
REPO_ROOT = ONCO_DIR.parent
HISTORIAL_PATH = ONCO_DIR / "historial.json"
ENTREGAS_DIR = ONCO_DIR / "entregas"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

sys.path.insert(0, str(MOTOR_DIR))
from paletas import CATEGORIAS, ORDEN_LAYOUTS, ORDEN_PALETAS, PALETAS  # noqa: E402
from plantillas import generar_caption, generar_html  # noqa: E402


def cargar_historial() -> dict:
    with HISTORIAL_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def guardar_historial(historial: dict) -> None:
    with HISTORIAL_PATH.open("w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)
        f.write("\n")


def siguiente_opcion(actual: str | None, orden: list[str]) -> str:
    if actual not in orden:
        return orden[0]
    return orden[(orden.index(actual) + 1) % len(orden)]


def proximas_fechas_lmv(desde: date | None = None, cantidad: int = 3) -> list[str]:
    """Devuelve las próximas N fechas de lunes (0), miércoles (2) o viernes (4)."""
    cursor = (desde or date.today()) + timedelta(days=1)
    dias_objetivo = {0, 2, 4}
    resultado = []
    while len(resultado) < cantidad:
        if cursor.weekday() in dias_objetivo:
            resultado.append(cursor.isoformat())
        cursor += timedelta(days=1)
    return resultado


def renderizar_png(html_path: Path, png_path: Path) -> None:
    if not Path(CHROME_BIN).exists():
        raise FileNotFoundError(f"No se encontró Google Chrome en: {CHROME_BIN}")
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--user-data-dir=/tmp/chrome-infografia",
        "--hide-scrollbars",
        "--window-size=1080,1350",
        "--force-device-scale-factor=1",
        f"--screenshot={png_path}",
        html_path.resolve().as_uri(),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not png_path.exists():
        raise RuntimeError(f"Error al renderizar PNG: {res.stderr or res.stdout}")


def convertir_a_jpg(png_path: Path, jpg_path: Path) -> None:
    """Convierte el PNG renderizado a JPEG (formato requerido por Instagram Graph API)."""
    if Path("/usr/bin/sips").exists():
        cmd = [
            "/usr/bin/sips",
            "-s", "format", "jpeg",
            "-s", "formatOptions", "95",
            str(png_path),
            "--out", str(jpg_path),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 or not jpg_path.exists():
            raise RuntimeError(f"Error al convertir PNG a JPG con sips: {res.stderr or res.stdout}")
        return
    try:
        from PIL import Image  # type: ignore

        with Image.open(png_path) as img:
            img.convert("RGB").save(jpg_path, "JPEG", quality=95, optimize=True)
    except ImportError as exc:
        raise RuntimeError(
            "No se encontró sips ni Pillow para convertir PNG a JPEG (requerido por Instagram Graph API)."
        ) from exc


def procesar_entrega(spec: dict, historial: dict, sin_render: bool = False) -> dict:
    entregas = historial["entregas"]
    ultima = entregas[-1] if entregas else None

    numero = spec.get("numero") or ((ultima["numero"] + 1) if ultima else 1)
    ultima_paleta = ultima["paleta"] if ultima else None
    ultimo_layout = ultima["layout"] if ultima else None

    paleta = spec.get("paleta") or siguiente_opcion(ultima_paleta, ORDEN_PALETAS)
    if paleta == ultima_paleta:
        raise ValueError(f"La paleta '{paleta}' repite la de la entrega anterior.")
    if paleta not in PALETAS:
        raise ValueError(f"Paleta desconocida: '{paleta}'")

    layout = spec.get("layout") or siguiente_opcion(ultimo_layout, ORDEN_LAYOUTS)
    if layout not in ORDEN_LAYOUTS:
        raise ValueError(f"Layout desconocido: '{layout}'")

    categoria_id = int(spec["categoria_id"])
    categoria_nombre = spec.get("categoria_nombre") or CATEGORIAS[categoria_id]

    slug = spec["slug"]
    carpeta = ENTREGAS_DIR / f"{numero:02d}-{slug}"
    carpeta.mkdir(parents=True, exist_ok=True)

    datos_render = {
        **spec,
        "numero": numero,
        "paleta": paleta,
        "layout": layout,
        "categoria_nombre": categoria_nombre,
    }

    html_path = carpeta / "infografia.html"
    png_path = carpeta / f"oncoupdates-{numero:02d}-{slug}.png"
    jpg_path = carpeta / f"oncoupdates-{numero:02d}-{slug}.jpg"
    caption_path = carpeta / "caption.md"

    html_path.write_text(generar_html(datos_render), encoding="utf-8")
    caption_path.write_text(generar_caption(datos_render), encoding="utf-8")

    if not sin_render:
        renderizar_png(html_path, png_path)
        convertir_a_jpg(png_path, jpg_path)

    registro = {
        "numero": numero,
        "slug": slug,
        "fecha_programada": spec.get("fecha_programada"),
        "categoria_id": categoria_id,
        "categoria_nombre": categoria_nombre,
        "paleta": paleta,
        "layout": layout,
        "titulo": spec["titulo"],
        "fuente": spec["fuente"],
        "imagen_relativa": str(jpg_path.relative_to(REPO_ROOT)),
        "caption_relativa": str(caption_path.relative_to(REPO_ROOT)),
        "estado": "programada" if spec.get("fecha_programada") else "borrador",
        "ig_media_id": None,
        "publicada_en": None,
    }
    entregas.append(registro)
    return registro


def main() -> None:
    parser = argparse.ArgumentParser(description="Generador OncoUpdates")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_gen = sub.add_parser("generar", help="Genera 1 entrega o un lote desde un JSON")
    p_gen.add_argument("archivo_json", type=Path, help="Ruta al JSON (objeto o lista)")
    p_gen.add_argument("--sin-render", action="store_true", help="Solo HTML y caption.md")

    p_fechas = sub.add_parser("proximas-fechas", help="Muestra próximos lunes/miércoles/viernes")
    p_fechas.add_argument("--cantidad", type=int, default=3)

    args = parser.parse_args()

    if args.comando == "proximas-fechas":
        for f in proximas_fechas_lmv(cantidad=args.cantidad):
            print(f)
        return

    payload = json.loads(args.archivo_json.read_text(encoding="utf-8"))
    specs = payload if isinstance(payload, list) else [payload]

    historial = cargar_historial()
    generados = []
    for spec in specs:
        reg = procesar_entrega(spec, historial, sin_render=args.sin_render)
        generados.append(reg)
        print(
            f"[OK] OncoUpdates {reg['numero']:02d} ({reg['slug']}) | "
            f"paleta={reg['paleta']} | layout={reg['layout']} | fecha={reg['fecha_programada']}"
        )

    guardar_historial(historial)
    print(f"Historial actualizado ({len(generados)} entrega(s) agregada(s)).")


if __name__ == "__main__":
    main()
