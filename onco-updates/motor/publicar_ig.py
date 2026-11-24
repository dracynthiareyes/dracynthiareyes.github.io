#!/usr/bin/env python3
"""Publica en Instagram (@dracynthiareyes) la entrega programada de OncoUpdates para hoy."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

MOTOR_DIR = Path(__file__).resolve().parent
ONCO_DIR = MOTOR_DIR.parent
REPO_ROOT = ONCO_DIR.parent
HISTORIAL_PATH = ONCO_DIR / "historial.json"
GRAPH_BASE = "https://graph.facebook.com/v21.0"
CDMX_TZ = ZoneInfo("America/Mexico_City")


def cargar_env_local() -> None:
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for linea in env_path.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        k, v = linea.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def http_json(url: str, data: dict | None = None) -> dict:
    encoded = urllib.parse.urlencode(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=encoded, method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Error HTTP {e.code} en Meta Graph API: {detalle}") from e


def verificar_url_publica(url: str) -> None:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "OncoUpdates-Publisher/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status >= 400:
                raise RuntimeError(f"La imagen devolvió HTTP {resp.status}: {url}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"La imagen aún no está disponible en GitHub Pages ({e.code}): {url}") from e


def seleccionar_entrega(historial: dict, fecha_obj: str, numero: int | None) -> dict | None:
    for item in historial["entregas"]:
        if numero is not None:
            if item["numero"] == numero:
                return item
        elif item.get("estado") == "programada" and item.get("fecha_programada") == fecha_obj:
            return item
    return None


def publicar_en_instagram(ig_user_id: str, token: str, image_url: str, caption: str) -> str:
    # 1. Crear contenedor de medios
    creacion = http_json(
        f"{GRAPH_BASE}/{ig_user_id}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": token,
        },
    )
    creation_id = creacion["id"]

    # 2. Esperar a que Meta procese la imagen
    for _ in range(12):
        estado = http_json(
            f"{GRAPH_BASE}/{creation_id}?"
            + urllib.parse.urlencode({"fields": "status_code", "access_token": token})
        )
        code = estado.get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise RuntimeError(f"Meta reportó error procesando el contenedor {creation_id}: {estado}")
        time.sleep(3)
    else:
        raise TimeoutError(f"Tiempo agotado esperando procesamiento de {creation_id}")

    # 3. Publicar contenedor
    publicado = http_json(
        f"{GRAPH_BASE}/{ig_user_id}/media_publish",
        data={
            "creation_id": creation_id,
            "access_token": token,
        },
    )
    return publicado["id"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Publicador Instagram Graph API para OncoUpdates")
    parser.add_argument("--fecha", help="Fecha YYYY-MM-DD (por defecto hoy en America/Mexico_City)")
    parser.add_argument("--numero", type=int, help="Forzar publicación de un número específico")
    parser.add_argument("--dry-run", action="store_true", help="Valida todo sin llamar a Meta")
    args = parser.parse_args()

    cargar_env_local()
    fecha_obj = args.fecha or datetime.now(CDMX_TZ).date().isoformat()
    historial = json.loads(HISTORIAL_PATH.read_text(encoding="utf-8"))

    entrega = seleccionar_entrega(historial, fecha_obj, args.numero)
    if not entrega:
        print(f"No hay entregas programadas para {fecha_obj}. Nada que publicar.")
        return

    base_url = historial["configuracion"]["base_url_pages"].rstrip("/")
    image_url = f"{base_url}/{entrega['imagen_relativa']}"
    caption_path = REPO_ROOT / entrega["caption_relativa"]
    caption = caption_path.read_text(encoding="utf-8").strip()

    print(f"Entrega seleccionada: OncoUpdates {entrega['numero']:02d} — {entrega['titulo']}")
    print(f"Imagen pública: {image_url}")

    if args.dry_run:
        print("[DRY-RUN] Caption listo:")
        print("-" * 40)
        print(caption)
        print("-" * 40)
        return

    ig_user_id = os.environ.get("IG_USER_ID", "").strip()
    token = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    if not ig_user_id or not token:
        print("Faltan variables de entorno IG_USER_ID o IG_ACCESS_TOKEN.", file=sys.stderr)
        sys.exit(1)

    verificar_url_publica(image_url)
    media_id = publicar_en_instagram(ig_user_id, token, image_url, caption)

    entrega["estado"] = "publicada"
    entrega["ig_media_id"] = media_id
    entrega["publicada_en"] = datetime.now(CDMX_TZ).isoformat()

    HISTORIAL_PATH.write_text(
        json.dumps(historial, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"[OK] Publicado en Instagram. media_id={media_id}")


if __name__ == "__main__":
    main()
