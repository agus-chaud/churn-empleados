---
description: Skill para diseño de interfaces — dashboards, paneles de administración, apps, herramientas e interfaces interactivas. NO para diseño de marketing (landing pages, sitios de marketing, campañas).
alwaysApply: false
---

# Interface Design

Construye diseño de interfaces con artesanía y consistencia.

## Alcance

**Usar para:** Dashboards, paneles de administración, apps SaaS, herramientas, páginas de configuración, interfaces de datos.

**No usar para:** Landing pages, sitios de marketing, campañas. Redirigir esos a `/frontend-design`.

---

# El Problema

Generarás output genérico. Tu entrenamiento ha visto miles de dashboards. Los patrones son fuertes.

Puedes seguir todo el proceso — explorar el dominio, nombrar una firma, declarar tu intención — y aún así producir una plantilla. Colores cálidos en estructuras frías. Fuentes amigables en layouts genéricos. "Sensación de cocina" que se ve como cualquier otra app.

Esto sucede porque la intención vive en prosa, pero la generación de código extrae de patrones. La brecha entre ellos es donde ganan los defaults.

El proceso a continuación ayuda. Pero el proceso solo no garantiza artesanía. Tienes que atraparlo.

---

# Dónde se Esconden los Defaults

Los defaults no se anuncian. Se disfrazan como infraestructura — las partes que se sienten como que solo necesitan funcionar, no ser diseñadas.

**La tipografía se siente como un contenedor.** Elige algo legible, continúa. Pero la tipografía no está sosteniendo tu diseño — ES tu diseño. El peso de un encabezado, la personalidad de una etiqueta, la textura de un párrafo. Estos moldean cómo se siente el producto antes de que alguien lea una palabra. Una herramienta de gestión de panadería y una terminal de trading pueden necesitar "tipo limpio y legible" — pero el tipo que es cálido y hecho a mano no es el tipo que es frío y preciso. Si estás alcanzando tu fuente usual, no estás diseñando.

**La navegación se siente como andamiaje.** Construye la barra lateral, agrega los enlaces, llega al trabajo real. Pero la navegación no está alrededor de tu producto — ES tu producto. Dónde estás, a dónde puedes ir, qué importa más. Una página flotando en el espacio es una demo de componente, no software. La navegación enseña a las personas cómo pensar sobre el espacio en el que están.

**Los datos se sienten como presentación.** Tienes números, muestra números. Pero un número en pantalla no es diseño. La pregunta es: ¿qué significa este número para la persona que lo mira? ¿Qué harán con él? Un anillo de progreso y una etiqueta apilada ambos muestran "3 de 10" — uno cuenta una historia, uno llena espacio. Si estás alcanzando número-sobre-etiqueta, no estás diseñando.

**Los nombres de tokens se sienten como detalle de implementación.** Pero tus variables CSS son decisiones de diseño. `--ink` y `--parchment` evocan un mundo. `--gray-700` y `--surface-2` evocan una plantilla. Alguien leyendo solo tus tokens debería poder adivinar qué producto es este.

La trampa es pensar que algunas decisiones son creativas y otras son estructurales. No hay decisiones estructurales. Todo es diseño. El momento en que dejas de preguntar "¿por qué esto?" es el momento en que los defaults toman el control.

---

# Intención Primero

Antes de tocar código, responde esto. No en tu cabeza — en voz alta, a ti mismo o al usuario.

**¿Quién es este humano?**
No "usuarios." La persona real. ¿Dónde están cuando abren esto? ¿Qué tienen en mente? ¿Qué hicieron hace 5 minutos, qué harán 5 minutos después? Un maestro a las 7am con café no es un desarrollador depurando a medianoche no es un fundador entre reuniones con inversores. Su mundo moldea la interfaz.

**¿Qué deben lograr?**
No "usar el dashboard." El verbo. Calificar estas presentaciones. Encontrar el deployment roto. Aprobar el pago. La respuesta determina qué lidera, qué sigue, qué se oculta.

**¿Cómo debería sentirse esto?**
Dilo en palabras que signifiquen algo. "Limpio y moderno" no significa nada — cada IA dice eso. ¿Cálido como un cuaderno? ¿Frío como una terminal? ¿Denso como un piso de trading? ¿Calmado como una app de lectura? La respuesta moldea color, tipo, espaciado, densidad — todo.

Si no puedes responder esto con especificidades, detente. Pregunta al usuario. No adivines. No defaults.

## Cada Elección Debe Ser Una Elección

Para cada decisión, debes poder explicar POR QUÉ.

- ¿Por qué este layout y no otro?
- ¿Por qué esta temperatura de color?
- ¿Por qué este tipo de letra?
- ¿Por qué esta escala de espaciado?
- ¿Por qué esta jerarquía de información?

Si tu respuesta es "es común" o "es limpio" o "funciona" — no has elegido. Has usado defaults. Los defaults son invisibles. Las elecciones invisibles se combinan en output genérico.

**La prueba:** Si intercambiaras tus elecciones por las alternativas más comunes y el diseño no se sintiera significativamente diferente, nunca hiciste elecciones reales.

## La Igualdad Es Fracaso

Si otra IA, dado un prompt similar, produciría sustancialmente el mismo output — has fallado.

Esto no se trata de ser diferente por sí mismo. Se trata de que la interfaz emerja del problema específico, el usuario específico, el contexto específico. Cuando diseñas desde la intención, la igualdad se vuelve imposible porque no hay dos intenciones idénticas.

Cuando diseñas desde defaults, todo se ve igual porque los defaults son compartidos.

## La Intención Debe Ser Sistémica

Decir "cálido" y usar colores fríos no es seguir adelante. La intención no es una etiqueta — es una restricción que moldea cada decisión.

Si la intención es cálida: superficies, texto, bordes, acentos, colores semánticos, tipografía — todo cálido. Si la intención es densa: espaciado, tamaño de tipo, arquitectura de información — todo denso. Si la intención es calmada: movimiento, contraste, saturación de color — todo calmado.

Verifica tu output contra tu intención declarada. ¿Cada token la refuerza? ¿O declaraste una intención y luego usaste defaults de todos modos?

---

# Exploración del Dominio del Producto

Aquí es donde se atrapan los defaults — o no.

Output genérico: Tipo de tarea → Plantilla visual → Tema
Output artesanal: Tipo de tarea → Dominio del producto → Firma → Estructura + Expresión

La diferencia: tiempo en el mundo del producto antes de cualquier pensamiento visual o estructural.

## Outputs Requeridos

**No propongas ninguna dirección hasta que produzcas los cuatro:**

**Dominio:** Conceptos, metáforas, vocabulario del mundo de este producto. No características — territorio. Mínimo 5.

**Mundo de color:** ¿Qué colores existen naturalmente en el dominio de este producto? No "cálido" o "frío" — ve al mundo real. Si este producto fuera un espacio físico, ¿qué verías? ¿Qué colores pertenecen allí que no pertenecen en otro lugar? Lista 5+.

**Firma:** Un elemento — visual, estructural o de interacción — que solo podría existir para ESTE producto. Si no puedes nombrar uno, sigue explorando.

**Defaults:** 3 elecciones obvias para este tipo de interfaz — visuales Y estructurales. No puedes evitar patrones que no has nombrado.

## Requisitos de Propuesta

Tu dirección debe referenciar explícitamente:
- Conceptos de dominio que exploraste
- Colores de tu exploración del mundo de color
- Tu elemento de firma
- Qué reemplaza cada default

**La prueba:** Lee tu propuesta. Elimina el nombre del producto. ¿Alguien podría identificar para qué es esto? Si no, es genérico. Explora más profundo.

---

# El Mandato

**Antes de mostrar al usuario, mira lo que hiciste.**

Pregúntate: "Si dijeran que esto carece de artesanía, ¿qué querrían decir?"

Esa cosa en la que acabas de pensar — arréglala primero.

Tu primer output probablemente es genérico. Eso es normal. El trabajo es atraparlo antes de que el usuario tenga que hacerlo.

## Las Verificaciones

Ejecuta esto contra tu output antes de presentar:

- **La prueba de intercambio:** Si intercambiaras el tipo de letra por tu usual, ¿alguien lo notaría? Si intercambiaras el layout por una plantilla de dashboard estándar, ¿se sentiría diferente? Los lugares donde el intercambio no importaría son los lugares donde usaste defaults.

- **La prueba de entrecerrar ojos:** Desenfoca tus ojos. ¿Aún puedes percibir jerarquía? ¿Algo salta agresivamente? La artesanía susurra.

- **La prueba de firma:** ¿Puedes señalar cinco elementos específicos donde aparece tu firma? No "la sensación general" — componentes reales. Una firma que no puedes localizar no existe.

- **La prueba de tokens:** Lee tus variables CSS en voz alta. ¿Suenan como si pertenecieran al mundo de este producto, o podrían pertenecer a cualquier proyecto?

Si alguna verificación falla, itera antes de mostrar.

---

# Fundamentos de Artesanía

## Capas Sutiles

Este es el respaldo de la artesanía. Independientemente de la dirección, tipo de producto o estilo visual — este principio se aplica a todo. Apenas deberías notar el sistema funcionando. Cuando miras el dashboard de Vercel, no piensas "bonitos bordes." Solo entiendes la estructura. La artesanía es invisible — así es como sabes que está funcionando.

### Elevación de Superficie

Las superficies se apilan. Un dropdown se sienta sobre una tarjeta que se sienta sobre la página. Construye un sistema numerado — base, luego niveles crecientes de elevación. En modo oscuro, mayor elevación = ligeramente más claro. En modo claro, mayor elevación = ligeramente más claro o usa sombra.

Cada salto debe ser solo unos pocos puntos porcentuales de luminosidad. Apenas puedes ver la diferencia en aislamiento. Pero cuando las superficies se apilan, la jerarquía emerge. Cambios susurro-silenciosos que sientes en lugar de ver.

**Decisiones clave:**
- **Barras laterales:** Mismo fondo que el canvas, no diferente. Diferentes colores fragmentan el espacio visual en "mundo de barra lateral" y "mundo de contenido." Un borde sutil es suficiente separación.
- **Dropdowns:** Un nivel por encima de su superficie padre. Si ambos comparten el mismo nivel, el dropdown se mezcla con la tarjeta y se pierde el capas.
- **Inputs:** Ligeramente más oscuros que sus alrededores, no más claros. Los inputs son "inset" — reciben contenido. Un fondo más oscuro señala "escribe aquí" sin bordes pesados.

### Bordes

Los bordes deberían desaparecer cuando no los estás buscando, pero ser encontrables cuando necesitas estructura. Baja opacidad rgba se mezcla con el fondo — define bordes sin demandar atención. Los bordes hex sólidos se ven duros en comparación.

Construye una progresión — no todos los bordes son iguales. Bordes estándar, separación más suave, bordes de énfasis, máximo énfasis para anillos de enfoque. Coincide la intensidad con la importancia del límite.

**La prueba de entrecerrar ojos:** Desenfoca tus ojos en la interfaz. Deberías poder percibir jerarquía — qué está sobre qué, dónde se dividen las secciones. Pero nada debería saltar. Sin líneas duras. Sin cambios de color discordantes. Solo estructura silenciosa.

Esto separa interfaces profesionales de las amateur. Si te equivocas en esto, nada más importa.

## Expresión Infinita

Cada patrón tiene expresiones infinitas. **Ninguna interfaz debería verse igual.**

Una visualización de métrica podría ser un número hero, estadística inline, sparkline, medidor, barra de progreso, delta de comparación, badge de tendencia, o algo nuevo. Un dashboard podría enfatizar densidad, espacio en blanco, jerarquía o flujo de maneras completamente diferentes. Incluso barra lateral + tarjetas tiene variaciones infinitas en proporción, espaciado y énfasis.

**Antes de construir, pregunta:**
- ¿Cuál es la ÚNICA cosa que los usuarios hacen más aquí?
- ¿Qué productos resuelven problemas similares brillantemente? Estúdialos.
- ¿Por qué esta interfaz se sentiría diseñada para su propósito, no templada?

**NUNCA produzcas output idéntico.** Mismo ancho de barra lateral, misma cuadrícula de tarjetas, mismas cajas de métricas con icono-izquierda-número-grande-etiqueta-pequeña cada vez — esto señala generado por IA inmediatamente. Es olvidable.

La arquitectura y los componentes deberían emerger de la tarea y los datos, ejecutados de una manera que se sienta fresca. Las tarjetas de Linear no se ven como las de Notion. Las métricas de Vercel no se ven como las de Stripe. Mismos conceptos, expresiones infinitas.

## El Color Vive en Algún Lugar

Cada producto existe en un mundo. Ese mundo tiene colores.

Antes de alcanzar una paleta, pasa tiempo en el mundo del producto. ¿Qué verías si caminaras a la versión física de este espacio? ¿Qué materiales? ¿Qué luz? ¿Qué objetos?

Tu paleta debería sentirse como si viniera DE algún lugar — no como si fuera aplicada A algo.

**Más Allá de Cálido y Frío:** La temperatura es un eje. ¿Esto es silencioso o ruidoso? ¿Denso o espacioso? ¿Serio o juguetón? ¿Geométrico u orgánico? Una terminal de trading y una app de meditación son ambos "enfocados" — tipos completamente diferentes de enfoque. Encuentra la cualidad específica, no la etiqueta genérica.

**El Color Lleva Significado:** El gris construye estructura. El color comunica — estado, acción, énfasis, identidad. Color sin motivo es ruido. Un color de acento, usado con intención, vence a cinco colores usados sin pensamiento.

---

# Antes de Escribir Cada Componente

**Cada vez** que escribas código de UI — incluso adiciones pequeñas — declara:

```
Intención: [quién es este humano, qué deben hacer, cómo debería sentirse]
Paleta: [colores de tu exploración — y POR QUÉ encajan en el mundo de este producto]
Profundidad: [bordes / sombras / capas — y POR QUÉ esto encaja con la intención]
Superficies: [tu escala de elevación — y POR QUÉ esta temperatura de color]
Tipografía: [tu tipo de letra — y POR QUÉ encaja con la intención]
Espaciado: [tu unidad base]
```

Este checkpoint es obligatorio. Te obliga a conectar cada elección técnica de vuelta a la intención.

Si no puedes explicar POR QUÉ para cada elección, estás usando defaults. Detente y piensa.

---

# Principios de Diseño

## Arquitectura de Tokens

Cada color en tu interfaz debería rastrearse hasta un pequeño conjunto de primitivos: foreground (jerarquía de texto), background (elevación de superficie), border (jerarquía de separación), brand, y semántico (destructivo, advertencia, éxito). Sin valores hex aleatorios — todo mapea a primitivos.

### Jerarquía de Texto

No solo tengas "texto" y "texto gris." Construye cuatro niveles — primario, secundario, terciario, atenuado. Cada uno sirve un rol diferente: texto por defecto, texto de apoyo, metadatos, y deshabilitado/placeholder. Usa los cuatro consistentemente. Si solo estás usando dos, tu jerarquía es demasiado plana.

### Progresión de Bordes

Los bordes no son binarios. Construye una escala que coincida la intensidad con la importancia — separación estándar, separación más suave, énfasis, máximo énfasis. No cada límite merece el mismo peso.

### Tokens de Control

Los controles de formulario tienen necesidades específicas. No reutilices tokens de superficie — crea dedicados para fondos de control, bordes de control y estados de enfoque. Esto te permite afinar elementos interactivos independientemente de superficies de layout.

## Espaciado

Elige una unidad base y mantén múltiplos. Construye una escala para diferentes contextos — espaciado micro para brechas de iconos, espaciado de componente dentro de botones y tarjetas, espaciado de sección entre grupos, separación mayor entre áreas distintas. Valores aleatorios señalan sin sistema.

## Padding

Manténlo simétrico. Si un lado tiene un valor, otros deberían coincidir a menos que el contenido requiera naturalmente asimetría.

## Profundidad

Elige UN enfoque y comprométete:
- **Solo bordes** — Limpio, técnico. Para herramientas densas.
- **Sombras sutiles** — Elevación suave. Para productos accesibles.
- **Sombras en capas** — Premium, dimensional. Para tarjetas que necesitan presencia.
- **Cambios de color de superficie** — Tintes de fondo establecen jerarquía sin sombras.

No mezcles enfoques.

## Radio de Borde

Más agudo se siente técnico. Más redondeado se siente amigable. Construye una escala — pequeño para inputs y botones, medio para tarjetas, grande para modales. No mezcles agudo y suave aleatoriamente.

## Tipografía

Construye niveles distintos distinguibles de un vistazo. Los encabezados necesitan peso y tracking ajustado para presencia. El cuerpo necesita peso cómodo para legibilidad. Las etiquetas necesitan peso medio que funcione en tamaños más pequeños. Los datos necesitan monospace con espaciado de números tabulares para alineación. No confíes solo en tamaño — combina tamaño, peso y letter-spacing.

## Layouts de Tarjetas

Una tarjeta de métrica no tiene que verse como una tarjeta de plan no tiene que verse como una tarjeta de configuración. Diseña la estructura interna de cada tarjeta para su contenido específico — pero mantén el tratamiento de superficie consistente: mismo peso de borde, profundidad de sombra, radio de esquina, escala de padding.

## Controles

Los ` ` y ` ` nativos renderizan elementos nativos del OS que no pueden ser estilizados. Construye componentes personalizados — botones trigger con dropdowns posicionados, popovers de calendario, gestión de estado estilizada.

## Iconografía

Los iconos aclaran, no decoran — si eliminar un icono pierde ningún significado, elimínalo. Elige un conjunto de iconos y mantente con él. Dale presencia a iconos independientes con contenedores de fondo sutiles.

## Animación

Micro-interacciones rápidas, easing suave. Transiciones más grandes pueden ser ligeramente más largas. Usa easing de desaceleración. Evita spring/bounce en interfaces profesionales.

## Estados

Cada elemento interactivo necesita estados: por defecto, hover, active, focus, disabled. Los datos también necesitan estados: loading, vacío, error. Estados faltantes se sienten rotos.

## Contexto de Navegación

Las pantallas necesitan fundamento. Una tabla de datos flotando en el espacio se siente como una demo de componente, no un producto. Incluye navegación mostrando dónde estás en la app, indicadores de ubicación y contexto de usuario. Al construir barras laterales, considera mismo fondo que contenido principal con separación de borde en lugar de colores diferentes.

## Modo Oscuro

Las interfaces oscuras tienen necesidades diferentes. Las sombras son menos visibles en fondos oscuros — apóyate en bordes para definición. Los colores semánticos (éxito, advertencia, error) a menudo necesitan ligera desaturación. El sistema de jerarquía aún se aplica, solo con valores invertidos.

---

# Evitar

- **Bordes duros** — si los bordes son lo primero que ves, son demasiado fuertes
- **Saltos dramáticos de superficie** — los cambios de elevación deberían ser susurro-silenciosos
- **Espaciado inconsistente** — la señal más clara de sin sistema
- **Estrategias de profundidad mezcladas** — elige un enfoque y comprométete
- **Estados de interacción faltantes** — hover, focus, disabled, loading, error
- **Sombras de caída dramáticas** — las sombras deberían ser sutiles, no llamativas
- **Radio grande en elementos pequeños**
- **Tarjetas blancas puras en fondos coloreados**
- **Bordes decorativos gruesos**
- **Gradientes y color para decoración** — el color debería significar algo
- **Múltiples colores de acento** — diluye el enfoque
- **Diferentes matices para diferentes superficies** — mantén el mismo matiz, cambia solo luminosidad

---

# Flujo de Trabajo

## Comunicación
Sé invisible. No anuncies modos o narres proceso.

**Nunca digas:** "Estoy en MODO ESTABLECER", "Déjame verificar system.md..."

**En su lugar:** Salta al trabajo. Declara sugerencias con razonamiento.

## Sugerir + Preguntar
Lidera con tu exploración y recomendación, luego confirma:
```
"Dominio: [5+ conceptos del mundo del producto]
Mundo de color: [5+ colores que existen en este dominio]
Firma: [un elemento único para este producto]
Rechazando: [default 1] → [alternativa], [default 2] → [alternativa], [default 3] → [alternativa]

Dirección: [enfoque que conecta con lo anterior]"

[Pregunta: "¿Esa dirección se siente bien?"]
```

## Si el Proyecto Tiene system.md
Lee `.interface-design/system.md` y aplica. Las decisiones están hechas.

## Si No Hay system.md
1. Explora dominio — Produce los cuatro outputs requeridos
2. Propone — La dirección debe referenciar los cuatro
3. Confirma — Obtén aceptación del usuario
4. Construye — Aplica principios
5. **Evalúa** — Ejecuta las verificaciones del mandato antes de mostrar
6. Ofrece guardar

---

# Después de Completar una Tarea

Cuando termines de construir algo, **siempre ofrece guardar**:

```
"¿Quieres que guarde estos patrones para sesiones futuras?"
```

Si sí, escribe en `.interface-design/system.md`:
- Dirección y sensación
- Estrategia de profundidad (bordes/sombras/capas)
- Unidad base de espaciado
- Patrones clave de componentes

### Qué Guardar

Agrega patrones cuando un componente se usa 2+ veces, es reutilizable en el proyecto, o tiene mediciones específicas que vale la pena recordar. No guardes componentes únicos, experimentos temporales o variaciones mejor manejadas con props.

### Verificaciones de Consistencia

Si system.md define valores, verifica contra ellos: espaciado en la cuadrícula definida, profundidad usando la estrategia declarada en todas partes, colores de la paleta definida, patrones documentados reutilizados en lugar de reinventados.

Esto se compone — cada guardado hace el trabajo futuro más rápido y consistente.
