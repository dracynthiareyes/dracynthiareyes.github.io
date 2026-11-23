/**
 * Sitio web — Dra. Cynthia Reyes López
 * Ginecología, Obstetricia y Ginecología Oncológica
 *
 * Lógica ligera en JavaScript puro:
 * - Menú móvil accesible y barra superior fija
 * - Rotación automática quincenal de tarjetas preventivas (data/tarjetas.json)
 * - Botón "Ver otros temas" con transición suave
 * - Generación de enlaces directos a WhatsApp con mensajes por contexto
 */

const CONFIG = {
  whatsappPhone: "525580065948",
  tarjetasPorBloque: 3,
  tarjetasUrl: "data/tarjetas.json",
  // Opcional: si activas "Citas de Google Calendar" (Appointment Schedule),
  // pega aquí el enlace (ej. "https://calendar.app.google/...") para mostrar
  // automáticamente un botón discreto de "Ver disponibilidad".
  googleCalendarUrl: ""
};

/**
 * Construye un enlace wa.me seguro con mensaje prellenado.
 */
function buildWhatsAppUrl(mensaje) {
  const texto = encodeURIComponent(mensaje.trim());
  return `https://wa.me/${CONFIG.whatsappPhone}?text=${texto}`;
}

/**
 * Calcula la quincena actual del año (cada 14 días).
 */
function obtenerQuincenaActual(fecha = new Date()) {
  const inicioAnio = new Date(fecha.getFullYear(), 0, 1);
  const msPorDia = 1000 * 60 * 60 * 24;
  const diasTranscurridos = Math.floor((fecha - inicioAnio) / msPorDia);
  return Math.floor(diasTranscurridos / 14);
}

/**
 * Escapa texto para evitar inyección HTML accidental desde JSON.
 */
function escaparHtml(texto) {
  const div = document.createElement("div");
  div.textContent = texto ?? "";
  return div.innerHTML;
}

/**
 * Renderiza el grupo actual de 3 tarjetas informativas.
 */
function crearTarjetaHtml(tarjeta) {
  const urlWhatsapp = buildWhatsAppUrl(
    tarjeta.mensaje_whatsapp ||
      `Hola Dra. Cynthia, me gustaría agendar una consulta sobre: ${tarjeta.titulo}.`
  );

  return `
    <article class="group flex flex-col justify-between bg-white border border-slate-200/80 hover:border-clinical-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-200">
      <div>
        <div class="flex items-center justify-between gap-2 mb-4">
          <span class="inline-flex items-center gap-1.5 text-xs font-semibold text-brand-700 bg-blush-100 border border-blush-200 px-3 py-1 rounded-full">
            <i data-lucide="shield-check" class="w-3.5 h-3.5 text-brand-600"></i>
            ${escaparHtml(tarjeta.categoria)}
          </span>
        </div>

        <h3 class="font-display text-lg font-bold text-slate-900 leading-snug mb-3 group-hover:text-clinical-700 transition-colors duration-200">
          ${escaparHtml(tarjeta.titulo)}
        </h3>

        <p class="text-sm text-slate-600 leading-relaxed mb-4">
          ${escaparHtml(tarjeta.resumen_paciente)}
        </p>

        <div class="bg-clinical-50/80 border border-clinical-100 rounded-xl p-3.5 mb-5">
          <p class="text-xs text-slate-700 leading-relaxed">
            <span class="font-semibold text-clinical-800">Recomendación:</span>
            ${escaparHtml(tarjeta.accion_sugerida)}
          </p>
        </div>
      </div>

      <div class="pt-4 border-t border-slate-100 space-y-3">
        <p class="text-[11px] text-slate-500 flex items-start gap-1.5 leading-snug">
          <i data-lucide="book-open" class="w-3.5 h-3.5 text-clinical-600 shrink-0 mt-0.5"></i>
          <span>${escaparHtml(tarjeta.fuente_guia)}</span>
        </p>

        <a
          href="${urlWhatsapp}"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center justify-center gap-2 w-full px-5 py-2.5 text-sm font-medium text-clinical-700 bg-clinical-50 hover:bg-clinical-600 hover:text-white border border-clinical-200/70 rounded-full transition-all duration-200"
        >
          <i data-lucide="message-circle" class="w-4 h-4"></i>
          <span>Consultar sobre este tema</span>
        </a>
      </div>
    </article>
  `;
}

/**
 * Inicializa la sección de tarjetas preventivas con rotación quincenal.
 */
async function initTarjetasPreventivas() {
  const contenedor = document.getElementById("tarjetas-grid");
  const botonOtros = document.getElementById("btn-otros-temas");
  const indicador = document.getElementById("tarjetas-indicador");

  if (!contenedor) return;

  let tarjetas = [];
  let offsetManual = 0;

  const renderGrupo = (conAnimacion = false) => {
    if (!tarjetas.length) return;

    const totalGrupos = Math.max(
      1,
      Math.ceil(tarjetas.length / CONFIG.tarjetasPorBloque)
    );
    const quincena = obtenerQuincenaActual();
    const grupoActual = (quincena + offsetManual) % totalGrupos;
    const inicio = (grupoActual * CONFIG.tarjetasPorBloque) % tarjetas.length;

    const seleccion = [];
    for (let i = 0; i < Math.min(CONFIG.tarjetasPorBloque, tarjetas.length); i++) {
      seleccion.push(tarjetas[(inicio + i) % tarjetas.length]);
    }

    const aplicarHtml = () => {
      contenedor.innerHTML = seleccion.map(crearTarjetaHtml).join("");
      if (indicador) {
        indicador.textContent = `Mostrando ${seleccion.length} de ${tarjetas.length} temas`;
      }
      if (window.lucide) {
        window.lucide.createIcons();
      }
    };

    if (conAnimacion) {
      contenedor.classList.add("opacity-0", "translate-y-1");
      window.setTimeout(() => {
        aplicarHtml();
        contenedor.classList.remove("opacity-0", "translate-y-1");
      }, 160);
    } else {
      aplicarHtml();
    }
  };

  try {
    const respuesta = await fetch(CONFIG.tarjetasUrl, { cache: "no-cache" });
    if (!respuesta.ok) {
      throw new Error(`HTTP ${respuesta.status}`);
    }
    tarjetas = await respuesta.json();
    renderGrupo(false);

    if (botonOtros) {
      botonOtros.addEventListener("click", () => {
        offsetManual += 1;
        renderGrupo(true);
      });
    }
  } catch (error) {
    console.error("No se pudieron cargar las tarjetas preventivas:", error);
    contenedor.innerHTML = `
      <div class="md:col-span-3 bg-slate-50 border border-slate-200/80 rounded-2xl p-8 text-center">
        <p class="text-sm text-slate-600 mb-3">
          No fue posible cargar la información preventiva en este momento.
        </p>
        <p class="text-xs text-slate-500">
          Si estás viendo el sitio de forma local, ábrelo mediante un servidor web o en GitHub Pages.
        </p>
      </div>
    `;
    if (botonOtros) {
      botonOtros.classList.add("hidden");
    }
  }
}

/**
 * Menú hamburguesa para dispositivos móviles.
 */
function initMenuMovil() {
  const btnMenu = document.getElementById("mobile-menu-btn");
  const menu = document.getElementById("mobile-menu");
  const iconOpen = document.getElementById("menu-icon-open");
  const iconClose = document.getElementById("menu-icon-close");

  if (!btnMenu || !menu) return;

  const setEstado = (abierto) => {
    btnMenu.setAttribute("aria-expanded", String(abierto));
    menu.classList.toggle("hidden", !abierto);
    if (iconOpen && iconClose) {
      iconOpen.classList.toggle("hidden", abierto);
      iconClose.classList.toggle("hidden", !abierto);
    }
  };

  btnMenu.addEventListener("click", () => {
    const estaAbierto = btnMenu.getAttribute("aria-expanded") === "true";
    setEstado(!estaAbierto);
  });

  menu.querySelectorAll("a").forEach((enlace) => {
    enlace.addEventListener("click", () => setEstado(false));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setEstado(false);
    }
  });
}

/**
 * Efecto sutil en la barra de navegación fija al hacer scroll.
 */
function initNavbarScroll() {
  const header = document.getElementById("site-header");
  if (!header) return;

  const actualizar = () => {
    if (window.scrollY > 12) {
      header.classList.add("shadow-sm", "border-slate-200/90");
    } else {
      header.classList.remove("shadow-sm", "border-slate-200/90");
    }
  };

  window.addEventListener("scroll", actualizar, { passive: true });
  actualizar();
}

/**
 * Muestra el botón opcional de Google Calendar si se configura una URL.
 */
function initAgendaOpcional() {
  const btnCalendar = document.getElementById("btn-google-calendar");
  if (btnCalendar && CONFIG.googleCalendarUrl) {
    btnCalendar.href = CONFIG.googleCalendarUrl;
    btnCalendar.classList.remove("hidden");
    btnCalendar.classList.add("inline-flex");
  }
}

/**
 * Formulario de valoración inicial en el Hero → WhatsApp estructurado.
 */
function initHeroBookingForm() {
  const form = document.getElementById("hero-booking-form");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const nombre = (document.getElementById("booking-name")?.value || "").trim();
    const telefono = (document.getElementById("booking-phone")?.value || "").trim();
    const modalidad = (document.getElementById("booking-modality")?.value || "").trim();
    const motivo = (document.getElementById("booking-reason")?.value || "").trim();
    const notas = (document.getElementById("booking-notes")?.value || "").trim();

    if (!nombre || !telefono || !motivo) return;

    const lineas = [
      "Hola Dra. Cynthia, me gustaría agendar una consulta:",
      `• Nombre: ${nombre}`,
      `• Teléfono: ${telefono}`,
      `• Modalidad: ${modalidad}`,
      `• Motivo: ${motivo}`
    ];

    if (notas) {
      lineas.push(`• Comentarios: ${notas}`);
    }

    const url = buildWhatsAppUrl(lineas.join("\n"));
    window.open(url, "_blank", "noopener,noreferrer");
  });
}

/**
 * Actualiza el año en el pie de página.
 */
function initAnioActual() {
  const el = document.getElementById("current-year");
  if (el) {
    el.textContent = String(new Date().getFullYear());
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }
  initMenuMovil();
  initNavbarScroll();
  initHeroBookingForm();
  initTarjetasPreventivas();
  initAgendaOpcional();
  initAnioActual();
});
