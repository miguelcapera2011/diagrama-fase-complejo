import html
import re

import streamlit as st
import streamlit.components.v1 as components

# ----------------------------------------------------------------------
# CONFIGURACIÓN: edita aquí tus datos
# ----------------------------------------------------------------------
NOMBRE = "Miguel Angel garatejo Capera"  # Escribe tu nombre entre comillas. Si lo dejas vacío, no se muestra.
PROFESORA = "Gisou Díaz Rojo"
UNIVERSIDAD = "Universidad del Tolima"
SEMINARIO = "Seminario 1"
PERSONAJE = "Agente de Investigacion MG"

# Lo que entendí, lo que no y mi reflexión: cámbialo por tus propias palabras.
ENTENDI = [
    "Investigar y enseñar deben ir juntas: si solo se transmite información, se olvida rápido.",
    "Sin ciencia propia, un país depende de otros en lo cultural y lo tecnológico.",
    "Los obstáculos son de tres tipos: dinero, organización y mentalidad.",
]
DUDAS = [
    "Los datos son de 1977 y 1984: ¿cuánto habrá cambiado la situación hoy?",
    "¿Cómo se logra una libertad absoluta de pensamiento si la investigación depende de fondos externos?",
    "El texto se enfoca en ciencias exactas y naturales: ¿y las ciencias sociales y humanas?",
]
REFLEXION = [
    "Quiero ver la investigación como una forma de pensar y de resolver problemas de mi entorno.",
    "Mi formación tiene un compromiso social: lo que aprendo debe servir a otros.",
    "Conocer lo que tenemos (nuestra región, nuestra gente) es el primer paso para cuidarlo.",
]

# Imágenes de internet por palabra clave (loremflickr.com). Puedes cambiar cualquier
# enlace por una foto tuya: solo pega la URL completa en lugar de la que está aquí.
def foto(palabras, n):
    return f"https://loremflickr.com/720/360/{palabras}?lock={n}"

# ----------------------------------------------------------------------
# IMÁGENES
# ----------------------------------------------------------------------

IMAGENES = {
    "lab": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=720&h=360",
    
    "universidad": "https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=720&h=360",
    
    "selva": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=720&h=360",
    
    "biblioteca": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=720&h=360",
    
    "estudiantes": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=720&h=360",
    
    "microscopio": "https://images.unsplash.com/photo-1576086213369-97a306d36557?auto=format&fit=crop&w=720&h=360",
}

# ----------------------------------------------------------------------
# CONTENIDO (basado solo en el artículo de Gabriel Roldán P., 1984)
# Tipos de mensaje: ("t", texto) · ("img", clave, pie) · ("q", cita, página)
#                   ("stats", [(cifra, etiqueta), ...]) · ("ul", título, [items])
# ----------------------------------------------------------------------
INTRO = [
    ("t", f"¡Hola! Soy  tu **{ "Agente MG"}** 👋 Hoy te cuento el artículo **La investigación científica en la universidad colombiana**, de Gabriel Roldán P. (Revista de la Facultad de Ingeniería, Vol. 1, No. 1, 1984, pp. 139-148)."),
    ("img", "lab", "Investigar es buscar respuestas con método."),
]

ESCENAS = [
    {
        "msgs": INTRO,
        "replies": [("¡Empecemos!", None)],
    },
    {
        "msgs": [
            ("t", "Primero, la **idea general**: para el autor, la investigación científica es una **necesidad** para los países en desarrollo, no un lujo."),
            ("ul", "¿Qué es investigar?", [
                "Una búsqueda sistemática de nuevos conocimientos, con pasos ordenados y planeados, no un proceso al azar.",
                "No consiste en repetir experimentos o recopilar datos, sino en **plantear problemas y buscar soluciones**.",
                "Tener un instrumento sofisticado o un laboratorio no hace científico a nadie.",
            ]),
        ],
        "replies": [("¿Y qué tipos hay?", None)],
    },
    {
        "msgs": [
            ("ul", "Tres tipos de investigación", [
                "**Básica:** busca un conocimiento más completo del tema, no una aplicación práctica.",
                "**Aplicada:** está orientada a la aplicación práctica del conocimiento, con objetivos específicos sobre productos y procesos.",
                "**Desarrollo tecnológico:** uso sistemático del conocimiento científico para producir materiales, dispositivos, sistemas o métodos útiles.",
            ]),
            ("t", "Ojo: la investigación y el desarrollo tecnológico son parte de la investigación científica, y uno es el soporte del otro."),
            ("t", "🧠 **Pregunta rápida:** una investigación que busca conocer más a fondo un tema, sin buscar una aplicación práctica, es…"),
        ],
        "replies": [("Básica", None), ("Aplicada", None), ("Desarrollo tecnológico", None)],
        "quiz": {"correcto": 0, "explica": "La investigación básica busca conocer mejor la materia de estudio, no aplicarla de inmediato."},
    },
    {
        "msgs": [
            ("t", "El autor se pregunta si investigar es una **necesidad** o más bien un **lujo** en los países en vías de desarrollo. ¿Tú qué piensas?"),
        ],
        "replies": [
            ("Es un lujo", "Es una respuesta común: el autor recuerda expresiones como «qué vamos a inventar lo que ya se ha inventado». Según él, solo reflejan que no se conoce la historia de la ciencia ni el desarrollo cultural de la humanidad."),
            ("Es una necesidad", "¡Coincides con el autor! Para él la investigación científica es una actividad irrenunciable de un país, entre otras razones por su valor cultural."),
        ],
    },
    {
        "msgs": [
            ("t", "Ahora las **ideas nuevas** que plantea el texto 💡"),
            ("ul", "Lo que más llama la atención", [
                "**La ciencia es cultura.** Un país culto es un país preparado para el desarrollo.",
                "**Mide la dependencia.** La ciencia es una medida de la dependencia económica de otros países.",
                "**Independencia intelectual.** Comprar una máquina no es comprar tecnología: a menudo significa más dependencia extranjera, por el manejo y los repuestos.",
                "**Investigación propia.** Aleja el peligro de interpretar nuestras realidades con moldes foráneos.",
                "**La básica también sirve.** Es base de la ciencia aplicada y culturiza al pueblo: quien conoce lo que tiene lo aprecia, lo conserva y lo mejora.",
            ]),
        ],
        "replies": [("Cuéntame un ejemplo", None)],
    },
    {
        "msgs": [
            ("t", "El autor da un ejemplo: aún hay inmensas **selvas tropicales** en cuyos árboles es probable que existan miles de sustancias químicas cuyas propiedades no se conocen, con posibilidades para la medicina, la alimentación y la tecnología."),
            ("img", "selva", "Las selvas guardan sustancias que aún no conocemos."),
            ("t", "Y termina con una pregunta abierta: **¿quién apoyará su estudio?** ¿Qué respondes?"),
        ],
        "replies": [
            ("El gobierno", "El autor dice que conocer los elementos químicos requirió un apoyo económico de valor incalculable a instituciones y personas dedicadas a buscar lo desconocido."),
            ("Las universidades", "Para el autor la universidad es el lugar donde debe darse la libertad de pensamiento y de generación de ideas, y debe buscar también fuentes nacionales e internacionales de financiación."),
            ("Las empresas", "Aquí el texto es crítico: el sector productivo ignora a la universidad y prefiere importar tecnología. En 1977 aportó solo el 2,5 % de los recursos."),
        ],
    },
    {
        "msgs": [
            ("t", "Hablemos del **compromiso del investigador** 🎓"),
            ("ul", "Según el texto", [
                "Formar al investigador es un esfuerzo social considerable, mientras existen necesidades apremiantes como la desnutrición, el desempleo y la falta de educación.",
                "Por eso el investigador debe ser consciente de su **compromiso social**.",
                "Su responsabilidad es generar conocimientos que culturicen al pueblo y contribuyan a elevar su nivel de vida, física y mental.",
                "Si no se toma conciencia de esa labor, el país dependerá cada vez más de los países más desarrollados.",
            ]),
        ],
        "replies": [("¿Qué se necesita para investigar?", None)],
    },
    {
        "msgs": [
            ("ul", "Condiciones necesarias en la universidad", [
                "**Programa a largo plazo:** continuidad garantizada y profesores estables.",
                "**Sistema internacional:** la ciencia no tiene fronteras y sus resultados se miden con patrones internacionales.",
                "**Libertad:** un ambiente universitario crítico y de diálogo abierto, con criterios de prioridad claros.",
                "**Manejo adecuado:** que dependa de una Vicerrectoría o Director Académico, con un equipo técnico que apoye lo administrativo.",
                "**Financiación:** las universidades deben buscar también otras fuentes nacionales e internacionales.",
                "**Independencia intelectual:** el futuro de un país depende de que sus gentes aprendan a pensar y a producir.",
            ]),
            ("t", "🧠 **Pregunta rápida:** ¿qué porcentaje de su presupuesto deberían dedicar las universidades a la investigación?"),
        ],
        "replies": [("2 %", None), ("10 %", None), ("25 %", None)],
        "quiz": {"correcto": 0, "explica": "Es el 2 % del presupuesto, pero el autor lo llama «letra muerta» en la mayoría de las universidades colombianas."},
    },
    {
        "msgs": [
            ("t", "Ahora, ¿cómo estaba la investigación en la **universidad colombiana**?"),
            ("img", "universidad", "Docencia e investigación, separadas."),
            ("ul", "El diagnóstico del autor", [
                "Investigación y docencia están **separadas**: la docencia, como transmisión de conocimientos, ha sido la actividad fundamental.",
                "Se hace énfasis en información que se olvida rápido y se descuida la formación del espíritu científico.",
                "La universidad aporta muy poco al análisis y solución de los problemas del país, y el sector productivo la ignora.",
                "La investigación universitaria sumaba apenas un 25 o 30 % del total del país.",
                "Para el autor, esto revela un concepto distorsionado de la educación superior.",
            ]),
        ],
        "replies": [("Muéstrame los datos", None)],
    },
    {
        "msgs": [
            ("t", "Estos son los datos del **estudio de Colciencias (1977)** que cita el autor "),
            ("stats", [("28", "universidades investigaban (19 públicas, 9 privadas)"), ("606", "proyectos en ejecución"), ("1.055", "investigadores"), ("23 %", "de tiempo completo"), ("51 %", "con estudios de posgrado"), ("2,5 %", "aporte del sector productivo")]),
            ("ul", "Más datos", [
                "El 80 % de la investigación universitaria se hacía en universidades públicas (488 proyectos de 606).",
                "Las universidades aportaron el 46 % de los gastos; el 54 % vino de otras fuentes.",
                "El 82,9 % de los recursos fue a investigación aplicada.",
                "Las ciencias básicas concentraban el 40 % de proyectos e investigadores y el 33 % de los recursos.",
            ]),
            ("t", "🧠 **Pregunta rápida:** ¿qué parte de la investigación universitaria se hacía en universidades públicas?"),
        ],
        "replies": [("20 %", None), ("50 %", None), ("80 %", None)],
        "quiz": {"correcto": 2, "explica": "El 80 % se hacía en públicas, sobre todo en la Nacional, del Valle, de Antioquia e Industrial de Santander."},
    },
    {
        "msgs": [
            ("t", "¿Y qué frena la investigación? El autor resume **tres tipos de obstáculos** 🚧"),
            ("ul", "Obstáculos", [
                "**Financieros:** los más sobresalientes. Los incentivos salariales al investigador son mínimos.",
                "**Institucionales:** la docencia pesa más que la investigación, hay pocos docentes investigadores de tiempo completo, laboratorios y bibliotecas deficientes, y poca difusión de los trabajos.",
                "**Socioculturales:** falta de reconocimiento al investigador por parte de la sociedad y poca vinculación de la universidad con la comunidad.",
            ]),
        ],
        "replies": [("¿Y qué propone?", None)],
    },
    {
        "msgs": [
            ("ul", "Recomendaciones del autor", [
                "Crear **Comités de Investigación** en cada facultad.",
                "Hacer una **reforma curricular**: menos asignaturas de información y más cursos prácticos y electivos.",
                "Fortalecer la **carrera profesoral** con estabilidad, promoción y descarga académica.",
                "Mejorar bibliotecas y laboratorios, y ampliar préstamos y becas para estudiantes.",
                "Conseguir fondos que no comprometan la autonomía de la labor investigativa.",
                "Mejorar la imagen de la universidad ante el país y el sector empresarial.",
                "Crear fondos permanentes para la investigación y discutir los trabajos con otros investigadores.",
            ]),
        ],
        "replies": [("¿Hay algún ejemplo?", None)],
    },
    {
        "msgs": [
            ("t", "Sí: el autor cuenta el caso de la **Facultad de Ciencias Exactas y Naturales** de la Universidad de Antioquia, donde el Centro de Investigaciones empezó en enero de 1981 🔬"),
            ("img", "microscopio", "Un ejemplo de investigación en la universidad."),
            ("stats", [("25", "proyectos inscritos"), ("57", "profesores en proyectos"), ("25 %", "de los profesores investigaban"), ("12", "publicaciones"), ("14", "presentaciones nacionales"), ("4", "presentaciones internacionales")]),
            ("ul", "Dificultades que encontraron", [
                "Falta de tiempo de algunos investigadores por exceso de cargas administrativas y docentes.",
                "Lentitud en las compras por parte de la universidad.",
                "Falta de mantenimiento de equipos.",
                "Dificultades económicas de la universidad.",
            ]),
        ],
        "replies": [("¿Cuáles son las conclusiones?", None)],
    },
    {
        "msgs": [
            ("ul", "Conclusiones del autor", [
                "La investigación científica es una **necesidad** para los países en desarrollo: genera las bases de la investigación aplicada y crea cultura.",
                "Debe ser una actividad **propia del profesor universitario**, no independiente de la docencia.",
                "La universidad tiene la obligación moral y material de aportar el 2 % de su presupuesto.",
                "En la Universidad de Antioquia la actividad creció mucho por el Sistema Universitario de Investigación.",
                "Hace falta una **mayor relación entre la universidad y la comunidad**.",
            ]),
        ],
        "replies": [("¿Con qué frase me quedo?", None)],
    },
    {
        "msgs": [
            ("t", "Una frase para llevarte 📌"),
            ("q", "La ciencia no debe tener ni puede tener fronteras geográficas ni políticas.", "Roldán (1984), p. 142"),
            ("ul", "Otras ideas para citar (con su página)", [
                "Investigar es plantear problemas y buscar soluciones, no repetir experimentos (p. 139).",
                "Conocer lo que se tiene hace que el pueblo lo aprecie, lo conserve y lo mejore (p. 141).",
                "Comprar una máquina no es comprar tecnología (p. 143).",
            ]),
        ],
        "replies": [("¿Qué entendí y qué no?", None)],
    },
    {
        "msgs": [
            ("ul", "✅ Lo que entendí", ENTENDI),
            ("ul", "❓ Lo que me generó dudas", DUDAS),
            ("ul", "🌱 Lo que me llevo para mi vida y mi trabajo", REFLEXION),
        ],
        "replies": [("Terminar", None)],
    },
]


# ----------------------------------------------------------------------
# DISEÑO
# ----------------------------------------------------------------------
CSS = """
<style>
.stApp { background: #ECE5DD; }
header[data-testid="stHeader"], footer { display: none; }
.block-container { max-width: 720px; padding-top: 0.5rem; padding-bottom: 6rem; }
.top { background:#075E54; color:#fff; padding:12px 16px; border-radius:0 0 14px 14px;
       display:flex; align-items:center; gap:12px; margin-bottom:8px; }
.avatar { width:42px; height:42px; border-radius:50%; background:#FAC775; display:flex;
          align-items:center; justify-content:center; font-size:22px; }
.top .n { font-weight:600; font-size:16px; line-height:1.2; }
.top .s { font-size:12px; color:#CDEBE4; }
.row { display:flex; margin:6px 0; }
.row.me { justify-content:flex-end; }
.bubble { max-width:88%; padding:9px 12px; border-radius:12px; font-size:15px; line-height:1.5;
          box-shadow:0 1px 1px rgba(0,0,0,.12); color:#1f2a2e; }
.bot { background:#fff; border-top-left-radius:2px; }
.me .bubble { background:#DCF8C6; border-top-right-radius:2px; }
.bubble ul { margin:6px 0 0 0; padding-left:18px; }
.bubble li { margin-bottom:5px; }
.bubble h4 { margin:0 0 2px 0; font-size:15px; color:#075E54; }
.bubble img { width:100%; border-radius:8px; margin-top:6px; display:block; background:#D9E8E4; min-height:90px; }
.cap { font-size:12px; color:#667781; margin-top:3px; }
.quote { border-left:4px solid #F2A541; padding-left:10px; font-style:italic; font-size:16px; }
.pg { font-size:12px; color:#667781; margin-top:4px; }
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:8px; margin-top:4px; }
.stat { background:#E7F3F1; border-radius:10px; padding:8px; text-align:center; }
.stat b { display:block; font-size:22px; color:#075E54; }
.stat span { font-size:12px; color:#3b4a50; }
div.stButton > button { border-radius:18px; border:1.5px solid #1D9E75; background:#fff; color:#075E54; font-weight:500; }
div.stButton > button:hover { background:#E1F5EE; border-color:#075E54; color:#075E54; }
</style>
"""


def fmt(texto):
    t = html.escape(texto)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def mensaje_html(m):
    tipo = m[0]
    if tipo == "t":
        return fmt(m[1])
    if tipo == "img":
        url = IMAGENES.get(m[1], m[1])
        return f'<img src="{html.escape(url)}" alt="{html.escape(m[2])}"><div class="cap">{fmt(m[2])}</div>'
    if tipo == "q":
        return f'<div class="quote">“{fmt(m[1])}”</div><div class="pg">{fmt(m[2])}</div>'
    if tipo == "stats":
        celdas = "".join(f'<div class="stat"><b>{fmt(a)}</b><span>{fmt(b)}</span></div>' for a, b in m[1])
        return f'<div class="stats">{celdas}</div>'
    if tipo == "ul":
        items = "".join(f"<li>{fmt(i)}</li>" for i in m[2])
        return f"<h4>{fmt(m[1])}</h4><ul>{items}</ul>"
    return ""


def burbuja(contenido, lado="bot"):
    clase = "row me" if lado == "me" else "row"
    caja = "bubble" if lado == "me" else "bubble bot"
    st.markdown(f'<div class="{clase}"><div class="{caja}">{contenido}</div></div>', unsafe_allow_html=True)


def respuesta_bot(escena, j):
    quiz = escena.get("quiz")
    if quiz:
        ok = j == quiz["correcto"]
        return ("✅ ¡Correcto! " if ok else "🤔 Casi. ") + quiz["explica"]
    return escena["replies"][j][1]


def elegir(i, j):
    st.session_state.elegidas[i] = j
    st.session_state.paso = i + 1


def reiniciar():
    st.session_state.paso = 0
    st.session_state.elegidas = {}


# ----------------------------------------------------------------------
# APP
# ----------------------------------------------------------------------
st.set_page_config(page_title=f"{PERSONAJE} · Investigación científica", page_icon="🔬", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)

if "paso" not in st.session_state:
    reiniciar()

paso = st.session_state.paso
total = len(ESCENAS)

subtitulo = f"{UNIVERSIDAD} · {SEMINARIO}"
st.markdown(
    f'<div class="top"><div class="avatar">🧑‍🏫</div><div><div class="n">{PERSONAJE}</div>'
    f'<div class="s">en línea · {html.escape(subtitulo)}</div></div></div>',
    unsafe_allow_html=True,
)
st.progress(min(paso / total, 1.0), text=f"Avance: {min(paso, total)} de {total}")

with st.sidebar:
    st.markdown(f"**{"MATESTAD"}**")
    if NOMBRE:
        st.write(f"Presenta: {NOMBRE}")
    st.write(f"Profesora: {PROFESORA}")
    st.write(f"{UNIVERSIDAD} · {SEMINARIO}")
    st.button("Volver a empezar", on_click=reiniciar)

for i, escena in enumerate(ESCENAS):
    if i > paso:
        break
    for m in escena["msgs"]:
        burbuja(mensaje_html(m))
    if i < paso:
        j = st.session_state.elegidas.get(i, 0)
        burbuja(fmt(escena["replies"][j][0]), "me")
        texto = respuesta_bot(escena, j)
        if texto:
            burbuja(fmt(texto))
    else:
        for j, (etiqueta, _) in enumerate(escena["replies"]):
            st.button(etiqueta, key=f"r{i}_{j}", on_click=elegir, args=(i, j), use_container_width=True)

if paso >= total:
    burbuja("¡Eso es todo! 🎉 Gracias por leer conmigo. Si quieres repasar, toca **Volver a empezar**.")
    st.button("Volver a empezar", key="fin", on_click=reiniciar, use_container_width=True)
    if NOMBRE:
        burbuja(fmt(f"Presenta: **{NOMBRE}** · Profesora: {PROFESORA}"))

components.html(
    """<script>
    const d = window.parent.document;
    [d.querySelector('[data-testid="stMain"]'), d.querySelector('section.main'), d.documentElement]
      .forEach(e => { if (e) e.scrollTo({top: e.scrollHeight, behavior: 'smooth'}); });
    </script>""",
    height=0,
)
