# Resumen de conversación y estado del proyecto — OncoUpdates

**Fecha:** 23 de noviembre de 2026  
**Objetivo:** Crear y automatizar la generación de publicaciones educativas (**OncoUpdates**) para el Instagram de la Dra. Cynthia Reyes López (`@dracynthiareyes`), 3 veces por semana, basadas en sus manuales médicos y documentos.

---

## 1. Decisiones tomadas
1. **Nombre de la serie:** Se cambió de "Onco Tips" a **`OncoUpdates`** por indicación de la Dra. Cynthia para diferenciarse de otras cuentas en redes.
2. **Formato aprobado:** Infografía vertical `1080×1350 px` (4:5) renderizada desde plantillas HTML/CSS (para garantizar ortografía médica perfecta y consistencia visual) + texto (`caption.md`) listo para publicar.
3. **Elementos obligatorios definidos:**
   - Identidad visual alineada con el sitio web (`index.html`) y el monograma `assets/logo-cr.png`.
   - Badge `OncoUpdates · XX`.
   - Handle `@dracynthiareyes` visible.
   - Llamado a la acción invitando a agendar consulta con **datos de contacto en la bio**.
   - **Fuente clínica exacta** al pie de la infografía y al final del caption.
4. **Variación visual aprobada:** Rotar paletas de colores y estructuras entre publicaciones para que el feed sea dinámico (Rosa & Guinda, Azul Clínico del sitio web, Blanco & Rosa, Lila & Ciruela, Marfil & Guinda Dorado).

---

## 2. Trabajo completado (pilotos listos)
Se generaron y validaron visualmente 2 pilotos completos en `onco-updates/`:

1. **OncoUpdates 01 — Rosa & Guinda (cuadrícula 2×2):**
   - Tema: *Síntomas abdominales que no debes ignorar* (Salud Ovárica).
   - Fuente: Guías NCCN de Cáncer de Ovario (2027) y ESMO Essentials in Gynaecological Tumours (2024).
   - Archivos: `onco-updates/piloto-01-ovario-sintomas/` (`infografia.html`, `oncoupdates-01-ovario-sintomas.png`, `caption.md`).

2. **OncoUpdates 02 — Azul Clínico (lista vertical de 3 pasos):**
   - Tema: *¿Qué hacer ante un Papanicolaou anormal?* (Prevención Cervical).
   - Fuente: Atlas de Oncología Ginecológica (UNAM) y ESMO Essentials in Gynaecological Tumours (2024).
   - Archivos: `onco-updates/piloto-02-papanicolaou-azul/` (`infografia.html`, `oncoupdates-02-papanicolaou-azul.png`, `caption.md`).

---

## 3. Pendiente para la siguiente sesión
1. **Confirmar con la Dra. el canal de entrega / publicación:**
   - **Opción A:** Envío automático al WhatsApp de la Dra. (imagen + texto listo para revisar y publicar) vía WhatsApp Cloud API de Meta, Twilio o Zapier.
   - **Opción B:** Publicación directa en Instagram vía Instagram Graph API o Zapier (requiere cuenta Business/Creator vinculada a Página de Facebook).
   - **Opción C:** Subida automática a carpeta compartida de Google Drive (opción más rápida sin configurar Meta).
2. **Definir días y horario** de las 3 publicaciones semanales (ej. Lunes, Miércoles y Viernes a las 9:00 AM hora CDMX).
3. **Construir el motor reutilizable y la automatización:**
   - Script/plantilla parametrizada con las 5 paletas de color y rotación de layouts.
   - Archivo `onco-updates/historial.json` para registrar temas, fuentes y paletas ya usadas.
   - Automatización programada en Antigravity (`America/Mexico_City`) conectada al canal elegido.

---

## 4. Nota sobre trabajar en otra computadora (carpetas no subidas a GitHub)
En `.gitignore` están excluidas **`docs/`** y **`manuales/`** para no subir documentos personales ni PDFs pesados a GitHub Pages:
- **Sin `docs/`:** No hay problema para continuar; las credenciales y datos públicos de la Dra. ya están en `index.html`.
- **Con/sin `manuales/`:** Para arrancar y cubrir los primeros ~15 temas alcanza con `data/tarjetas.json` (sí está en GitHub). Para generar decenas de temas nuevos directamente desde los PDFs originales (NCCN, ESMO, OMS, Atlas UNAM) en la otra computadora, conviene copiar `manuales/` por fuera de GitHub (ej. Google Drive o USB).
