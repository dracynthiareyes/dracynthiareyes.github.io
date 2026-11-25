# AGENTS.md — Proyecto Dra. Cynthia Reyes López

Instrucciones y contexto operativo para agentes de IA que trabajen en este repositorio (sitio web + generación automatizada de contenido **OncoUpdates** para Instagram).

---

## 1. Contexto del proyecto

- **Especialista:** Dra. Cynthia Reyes López — Ginecología, Obstetricia y Ginecología Oncológica (certificada por CONACEM).
- **Consultorio:** World Trade Center Ciudad de México (Piso 34, Consultorio 28) y modalidad de Consulta Virtual.
- **Instagram:** `@dracynthiareyes`
- **Sitio web:** `index.html` (publicado en GitHub Pages: `https://dracynthiareyes.github.io/`).
- **Archivos clave del repositorio:**
  - `index.html` — Sitio web oficial y fuente de verdad de colores, credenciales y datos de contacto.
  - `data/tarjetas.json` — Resumen curado de temas oncológicos ginecológicos con sus fuentes clínicas exactas (sí está en GitHub).
  - `assets/logo-cr.png` — Monograma oficial (usado en las infografías).
  - `onco-updates/` — Motor (`motor/`), `historial.json`, pilotos (`piloto-01-*`, `piloto-02-*`) y entregas (`entregas/`) de la serie **OncoUpdates**.
  - `.github/workflows/oncoupdates-publish.yml` — Workflow de GitHub Actions para publicación automática en Instagram (`IG_USER_ID` e `IG_ACCESS_TOKEN` en GitHub Secrets).
  - `docs/` y `manuales/` — **Carpetas locales excluidas en `.gitignore`** (NO subir a GitHub). Contienen constancias/CV (`docs/`) y guías clínicas PDF como NCCN 2025–2027, ESMO 2024, OMS y Atlas UNAM (`manuales/`).

---

## 2. Reglas de la serie **OncoUpdates** (Instagram)

### Nombre oficial
- Usar siempre **`OncoUpdates`** (con esa capitalización exacta) y el hashtag **`#OncoUpdates`**.
- **No** usar "Onco Tips" ni variantes.

### Frecuencia y rotación
- **Cadencia:** 3 publicaciones por semana (**lunes, miércoles y viernes a las 09:17 AM hora CDMX**, `America/Mexico_City`, ejecutado vía GitHub Actions en `17 15 * * 1,3,5`).
- **Rotación de temas:** Llevar control en `onco-updates/historial.json` (ya activo; usar `onco-updates/motor/generar.py` para nuevas entregas) para rotar sin repetir entre:
  1. Patología mamaria (NCCN Mama / OMS)
  2. Cérvix, VPH y colposcopia (ESMO 2024 / Atlas UNAM)
  3. Cáncer de ovario y señales de alerta (NCCN Ovario / ESMO 2024)
  4. Endometrio / neoplasias uterinas (NCCN Útero / ESMO 2024)
  5. Vulva y vagina (NCCN Vulva y Vagina)
  6. Prevención, tamizaje y genética (BRCA, Síndrome de Lynch)
  7. Confianza, segunda opinión y credenciales de la Dra.

### Rotación de paletas de color y diseño
Nunca repetir la misma paleta en dos publicaciones consecutivas. Rotar entre estas paletas armoniosas con la marca:
1. **Rosa & Guinda:** fondo `#FDF4F7`, acento `#C83E72`, oscuro `#6B1737`, detalles dorados `#C99A3B`.
2. **Azul Clínico (paleta `clinical` de `index.html`):** fondo `#EFFAFC`, acento `#0E7C8B` / `#1499AB`, oscuro `#0A3944`, detalles dorados `#C99A3B`.
3. **Blanco Editorial & Rosa Suave:** fondo `#FFFFFF`, acento `#FDE4EE` / `#C83E72`, oscuro `#4D0F2B`.
4. **Lila & Ciruela:** fondo `#F8F4FC`, acento `#7C4D9E`, oscuro `#4A2566`, detalles dorados `#C99A3B`.
5. **Marfil / Crema & Guinda Dorado:** fondo `#FCF9F4`, acento `#A87B32`, oscuro `#6B1737`.

Alternar también las estructuras visuales (cuadrícula 2×2, lista vertical de 3 pasos, mito vs. realidad, checklist) para dar dinamismo al feed.

### Requisitos obligatorios en cada infografía
- **Formato:** PNG `1080×1350 px` (relación 4:5 ideal para feed de Instagram).
- **Elementos fijos:**
  - Etiqueta `OncoUpdates · XX` + categoría del tema.
  - Logo circular `assets/logo-cr.png`.
  - Usuario `@dracynthiareyes` y subtítulo profesional (`Dra. Cynthia Reyes López · Ginecología Oncológica · WTC CDMX y Consulta Virtual`).
  - Llamado a la acción visible: **Agenda tu consulta · Datos de contacto en la bio**.
  - **Fuente clínica exacta** al pie (ej. *Guías NCCN...*, *ESMO Essentials 2024*, *Atlas UNAM*) + nota breve (*Contenido educativo · No sustituye consulta médica*).
- **Renderizado recomendado:** Generar HTML/CSS autocontenido y renderizar con Chrome headless para garantizar cero errores tipográficos en términos médicos:
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless=new --disable-gpu --no-sandbox \
    --user-data-dir=/tmp/chrome-infografia --hide-scrollbars \
    --window-size=1080,1350 --force-device-scale-factor=1 \
    --screenshot="ruta/salida.png" "file:///ruta/absoluta/infografia.html"
  ```
  *(Verificar siempre la imagen renderizada para asegurar que no haya texto cortado ni desbordes).*

### Requisitos obligatorios en cada texto (caption)
- Tono empático, claro, riguroso y accesible para pacientes (sin alarmismo).
- Aclarar cuando aplique que tener síntomas no equivale automáticamente a cáncer, pero amerita valoración oportuna.
- Invitar siempre a **agendar consulta** (presencial en WTC CDMX o virtual) mencionando que los **datos de contacto están en la bio** (`@dracynthiareyes`).
- Incluir la **fuente clínica exacta** y breve aviso informativo.
- Hashtags relevantes empezando por `#OncoUpdates` `#DraCynthiaReyes` `#GinecologiaOncologica`.

---

## 3. Reglas de seguridad y privacidad
- **Nunca** agregar `docs/` ni `manuales/` al control de versiones ni quitarlos de `.gitignore`.
- No exponer credenciales, tokens de Meta/WhatsApp/Instagram ni archivos `.env` en el repositorio.
