# Sitio web — Dra. Cynthia Reyes López

Sitio web estático, ligero y responsivo para la consulta privada de la **Dra. Cynthia Reyes López** (Ginecología, Obstetricia y Ginecología Oncológica) en el World Trade Center Ciudad de México, listo para desplegarse en **GitHub Pages**.

## Estructura del proyecto

```text
├── index.html          # Página principal (HTML5 semántico + Tailwind CSS + Lucide Icons)
├── js/
│   └── app.js          # Menú móvil, enlaces WhatsApp y rotación quincenal de tarjetas
├── data/
│   └── tarjetas.json   # Banco de 15 tarjetas informativas basadas en guías clínicas
├── assets/
│   └── 387254.png      # Fotografía profesional
├── .gitignore          # Excluye carpetas locales privadas (docs/, manuales/, .DS_Store)
└── README.md
```

> **Privacidad:** Las carpetas locales `docs/` y `manuales/` están ignoradas en `.gitignore` para no subir documentos personales ni PDFs pesados al repositorio público.

---

## Cómo actualizar las tarjetas preventivas (`data/tarjetas.json`)

El sitio calcula automáticamente la quincena actual del año (`Math.floor(diasTranscurridos / 14)`) y muestra **3 tarjetas distintas cada 14 días** sin necesidad de modificar `index.html`.

Cuando agregues nuevos manuales o guías clínicas en tu carpeta local `manuales/`, puedes añadir o editar entradas en `data/tarjetas.json` siguiendo esta estructura:

```json
{
  "id": "identificador-unico-sin-espacios",
  "categoria": "Categoría médica breve",
  "titulo": "Título claro para pacientes",
  "resumen_paciente": "Explicación empática y sin jerga innecesaria (2 a 3 líneas).",
  "fuente_guia": "Basado en Guías NCCN (año) / ESMO / etc.",
  "accion_sugerida": "Paso concreto y claro recomendado para la paciente.",
  "mensaje_whatsapp": "Hola Dra. Cynthia, me gustaría agendar una consulta sobre..."
}
```

**Recomendaciones al editar el JSON:**
- Mantén un múltiplo de 3 tarjetas (por ejemplo, 12, 15 o 18) para que cada quincena muestre bloques equilibrados.
- Verifica que no falten comas entre objetos ni haya una coma sobrante después del último objeto.

---

## Opcional: Conectar agenda de Google Calendar

El sitio prioriza el agendamiento por **WhatsApp** (`55 8006 5948`), ya que permite coordinar horarios entre semana y fechas mensuales de fin de semana sin mostrar una agenda vacía.

Si en el futuro deseas habilitar un botón complementario con **Citas de Google Calendar (Appointment Schedules)** —que muestra únicamente los bloques disponibles sin exponer tu calendario personal—:
1. Crea un horario de citas en Google Calendar y copia su enlace (`https://calendar.app.google/...`).
2. Abre `js/app.js` y pega el enlace en `CONFIG.googleCalendarUrl`.
3. El botón **"Ver agenda disponible"** aparecerá automáticamente en la sección de Ubicación y Contacto.

---

## Cómo publicar cambios desde GitHub Desktop a GitHub Pages

1. **Abre GitHub Desktop** y selecciona el repositorio `sitio-dra-cynthia`.
2. Revisa en la columna izquierda (**Changes**) los archivos modificados (por ejemplo, `data/tarjetas.json` o `index.html`). Verifica que nunca aparezcan archivos de `docs/` o `manuales/`.
3. Escribe un resumen breve en el campo **Summary** (ej. `Actualización de tarjetas preventivas`) y haz clic en **Commit to main**.
4. Haz clic en **Push origin** en la barra superior para subir los cambios a GitHub.
5. *(Solo la primera vez)* En GitHub.com entra a **Settings → Pages**, selecciona **Deploy from a branch**, elige la rama `main` y carpeta `/ (root)`, y guarda. En 1 a 2 minutos el sitio quedará publicado y se actualizará automáticamente en cada `Push`.

---

## Pendientes posteriores a la publicación

- [ ] **Google Business Profile (Google Maps):** Dar de alta y verificar el consultorio en WTC CDMX (Montecito 38, Piso 34, Consultorio 28) enlazando el sitio web y WhatsApp (`55 8006 5948`).
- [ ] **Dominio propio:** Adquirir un dominio (ej. `dracynthiareyes.com` o `.mx`) y conectarlo a GitHub Pages (*Settings → Pages → Custom domain*).
- [ ] **Google Search Console:** Registrar el sitio y enviar `sitemap.xml` para acelerar la indexación en Google.
- [ ] **Google Calendar (opcional):** Pegar la URL de *Appointment Schedules* en `CONFIG.googleCalendarUrl` dentro de `js/app.js`.
- [ ] **Aseguradoras (futuro):** Agregar bloque de seguros/reembolso cuando se defina.

