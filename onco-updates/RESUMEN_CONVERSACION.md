# Resumen de conversación y estado del proyecto — OncoUpdates

**Última actualización:** 25 de noviembre de 2026  
**Objetivo:** Crear y automatizar la generación y publicación de infografías educativas (**OncoUpdates**) en el Instagram de la Dra. Cynthia Reyes López (`@dracynthiareyes`), 3 veces por semana, basadas en sus manuales médicos y documentos.

---

## 1. Decisiones tomadas
1. **Nombre de la serie:** Se usa **`OncoUpdates`** (y `#OncoUpdates`) por indicación de la Dra. Cynthia.
2. **Formato aprobado:** Infografía vertical `1080×1350 px` (4:5) renderizada desde HTML/CSS con Chrome headless y convertida a **`.jpg`** para compatibilidad directa con Instagram Graph API + texto (`caption.md`) listo para publicar.
3. **Elementos obligatorios definidos:**
   - Identidad visual alineada con `index.html` y monograma `assets/logo-cr.png`.
   - Badge `OncoUpdates · XX`, handle `@dracynthiareyes`, CTA **Agenda tu consulta · Datos de contacto en la bio**.
   - **Fuente clínica exacta** al pie de la infografía y al final del caption.
4. **Variación visual aprobada:** Rotar 5 paletas (`rosa_guinda`, `azul_clinico`, `blanco_rosa`, `lila_ciruela`, `marfil_dorado`) y 4 layouts (`grid_2x2`, `steps_3`, `myth_reality`, `checklist`).
5. **Canal y horario confirmados:** Publicación directa en Instagram (`@dracynthiareyes`) vía **Meta Instagram Graph API (`v21.0`)** y **GitHub Actions** los **lunes, miércoles y viernes a las 09:17 AM hora CDMX (`America/Mexico_City`)**.

---

## 2. Trabajo completado
1. **Motor reutilizable (`onco-updates/motor/`):**
   - `paletas.py` — 5 paletas oficiales y 7 categorías temáticas.
   - `plantillas.py` — Generador HTML/CSS (`1080×1350`) para los 4 layouts + generador de `caption.md`.
   - `generar.py` — CLI para generar entregas/lotes desde JSON, renderizar con Chrome headless (actualizado a `.jpg` en `8167491`) y actualizar `onco-updates/historial.json`.
   - `publicar_ig.py` — Publicador automático en Instagram Graph API que lee `historial.json`, verifica la imagen pública en GitHub Pages, publica y registra `ig_media_id` y estado `"publicada"`.
   - `.github/workflows/oncoupdates-publish.yml` — Cron `17 15 * * 1,3,5` + `workflow_dispatch` (con soporte de `--fecha` y `--dry-run`).

2. **Configuración de Meta e Instagram (validada en producción):**
   - `@dracynthiareyes` en modo Cuenta Profesional (Empresa) vinculada a la Página de Facebook de la Dra. Reyes dentro del Portafolio comercial.
   - App `OncoUpdates Publisher` creada en Meta for Developers con permisos `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`.
   - Secretos configurados en GitHub Actions (`Settings → Secrets and variables → Actions`): **`IG_USER_ID`** e **`IG_ACCESS_TOKEN`** (token de larga duración de **60 días** generado el **24 de noviembre de 2026**).
   - **Primera publicación real exitosa:** El miércoles **25 de noviembre de 2026** (~16:41 CDMX) se ejecutó manualmente `Run workflow` (`workflow_dispatch`) y se publicó **`OncoUpdates · 01`** en `@dracynthiareyes` sin errores, actualizando `historial.json` automáticamente (commit `d2d4c88`).

3. **Estado de entregas en `onco-updates/historial.json`:**
   - **01 — Miércoles 25 nov 2026 (`publicada`):** *Síntomas abdominales que no debes ignorar* (Salud Ovárica · `rosa_guinda` · `grid_2x2`) — `onco-updates/piloto-01-ovario-sintomas/`.
   - **02 — Viernes 27 nov 2026 (`programada`):** *¿Qué hacer ante un Papanicolaou anormal?* (Prevención Cervical · `azul_clinico` · `steps_3`) — `onco-updates/piloto-02-papanicolaou-azul/`.
   - **03 — Lunes 30 nov 2026 (`programada`):** *¿Notaste un bulto o cambio en tu mama?* (Patología Mamaria · `blanco_rosa` · `myth_reality`) — `onco-updates/entregas/03-mama-evaluacion-nodulo/`.

---

## 3. Incidencia detectada y próximos pasos (para retomar en cualquier computadora)
1. **Incidencia con el `cron` de GitHub Actions (25 nov 2026):**
   - El disparo automático `cron: "17 15 * * 1,3,5"` (09:17 AM CDMX) **no se ejecutó** el miércoles 25 nov (suele ocurrir en la primera ventana tras crear/editar un `cron` en GitHub Actions).
   - Se publicó manualmente con **Actions → Publicar OncoUpdates en Instagram → Run workflow** y funcionó al 100%.
2. **Qué revisar el viernes 27 nov 2026 (~09:50–10:00 AM CDMX):**
   - Verificar en `@dracynthiareyes` y en GitHub **Actions** si **`OncoUpdates · 02`** salió de forma automática (considerando que el `cron` de GitHub puede retrasarse 5–30 min).
   - **Si NO sale automáticamente el viernes:**
     1. Publicar `02` manualmente con **Run workflow**.
     2. Conectar un disparador externo gratuito (ej. **cron-job.org**) para que llame de forma puntual a la API `workflow_dispatch` de GitHub (`POST https://api.github.com/repos/dracynthiareyes/dracynthiareyes.github.io/actions/workflows/oncoupdates-publish.yml/dispatches` con `{"ref":"main"}` usando un Fine-grained PAT con permiso `Actions: Read and write` en este repositorio).
3. **Generar el siguiente lote semanal (a partir del miércoles 2 dic 2026):**
   - Continuar rotación de categorías (ej. `4` Salud Endometrial, `5` Salud Vulvar y Vaginal, `6` Prevención y Genética, `7` Atención Especializada), paletas (`lila_ciruela`, `marfil_dorado`) y layout (`checklist`).
   - Usar `python3 onco-updates/motor/generar.py generar <lote.json>`, verificar visualmente los `.jpg` y hacer `git push`.
4. **Renovación del token (antes del ~23 de enero de 2027):**
   - El token actual de 60 días debe renovarse antes de vencer, o bien sustituirse en GitHub Secrets por un **token permanente de Usuario del Sistema** desde `business.facebook.com/settings/system-users`.

---

## 4. Nota sobre trabajar en otra computadora (carpetas no subidas a GitHub)
En `.gitignore` están excluidas **`docs/`** y **`manuales/`** para no subir documentos personales ni PDFs pesados a GitHub Pages:
- **Sin `docs/`:** No hay problema para continuar; las credenciales y datos públicos de la Dra. ya están en `index.html`.
- **Con/sin `manuales/`:** Para cubrir los primeros ~15 temas alcanza con `data/tarjetas.json` (sí está en GitHub). Para generar temas nuevos directamente desde los PDFs originales (NCCN, ESMO, OMS, Atlas UNAM) en otra computadora, conviene copiar `manuales/` por fuera de GitHub (ej. Google Drive o USB).
- **Nota sobre GitHub:** Los secretos `IG_USER_ID` e `IG_ACCESS_TOKEN` ya viven en GitHub Actions, así que no hace falta reconfigurarlos en otra computadora salvo para pruebas locales con `.env`.
