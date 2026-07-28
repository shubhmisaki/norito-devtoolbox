#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H7a2 2 0 0 0-2 2v4a2 2 0 0 1-2 2 2 2 0 0 1 2 2v4a2 2 0 0 0 2 2h1"/><path d="M16 3h1a2 2 0 0 1 2 2v4a2 2 0 0 0 2 2 2 2 0 0 0-2 2v4a2 2 0 0 1-2 2h-1"/></svg>'
ICON_CLASS = "c-indigo"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="tabs" id="mode-tabs" role="tablist" style="margin-bottom:20px;">
          <button type="button" class="tab active" data-value="yaml2json">YAML &rarr; JSON</button>
          <button type="button" class="tab" data-value="json2yaml">JSON &rarr; YAML</button>
        </div>
        <select id="mode" style="display:none;">
          <option value="yaml2json">yaml2json</option>
          <option value="json2yaml">json2yaml</option>
        </select>

        <div class="field" style="margin-bottom:16px;">
          <label for="indentSize">{t['json_indent']}</label>
          <select id="indentSize">
            <option value="2" selected>{t['spaces2']}</option>
            <option value="4">{t['spaces4']}</option>
          </select>
        </div>

        <div class="field" style="margin-bottom:16px;">
          <label for="input">{t['input']}</label>
          <textarea id="input" class="mono-area" rows="12" placeholder="{t['paste_yaml']}"></textarea>
        </div>

        <div class="result-box error" id="errorBox" style="display:none; margin-bottom:16px;">
          <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
          <div class="r-body"></div>
        </div>

        <div class="field" style="margin-top:16px;">
          <label for="output">{t['output']}</label>
          <textarea id="output" class="mono-area" rows="12" readonly></textarea>
        </div>

        <div style="display:flex; gap:10px; margin-top:16px;">
          <button id="swapBtn" class="secondary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg>
            {t['swap']}
          </button>
          <button id="copyBtn">{t['copy_output']}</button>
        </div>
      </div>

      <div>
        <div class="panel">
          <div class="panel-header">
            <div class="icon-chip c-indigo" style="width:36px;height:36px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H7a2 2 0 0 0-2 2v4a2 2 0 0 1-2 2 2 2 0 0 1 2 2v4a2 2 0 0 0 2 2h1"/><path d="M16 3h1a2 2 0 0 1 2 2v4a2 2 0 0 0 2 2 2 2 0 0 0-2 2v4a2 2 0 0 1-2 2h-1"/></svg>
            </div>
            <div>
              <h3>{t['card1_h']}</h3>
              <p>{t['card1_p']}</p>
            </div>
          </div>
          <p class="note" style="margin-top:0;">
            {t['card1_note']}
          </p>
        </div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['card2_h']}</h3>
          <p class="note" style="margin-top:0;">
            {t['card2_note']}
          </p>
        </div>
      </div>
    </div>


    <div class="explain-panel">
      <h2>{t['how_h2']}</h2>
      <p>{t['how_p1']}</p>
      <p>{t['how_p2']}</p>
      <p>{t['how_p3']}</p>
      <p>{t['how_p4']}</p>
    </div>
'''

PAGES = {}

PAGES["es"] = dict(
    title="Conversor YAML a JSON (y viceversa) | norito",
    meta_desc="Convierte YAML a JSON o JSON a YAML, en vivo en tu navegador. Soporta mapeos, secuencias, cadenas entre comillas y comentarios. No se sube nada.",
    app_name="Conversor YAML a JSON", h1="Conversor YAML a JSON", breadcrumb_label="Conversor YAML a JSON",
    lede="Convierte YAML a JSON o JSON a YAML, en vivo mientras escribes. Funciona por completo en tu navegador, nada de lo que pegues se sube.",
    t=dict(
        json_indent="Sangría JSON", spaces2="2 espacios", spaces4="4 espacios",
        input="Entrada", paste_yaml="Pega YAML...", output="Salida", swap="Intercambiar", copy_output="Copiar salida",
        card1_h="Archivos de configuración, portátiles", card1_p="YAML es común en Docker Compose, Kubernetes y configuraciones de CI.",
        card1_note="YAML es más fácil de leer y editar para las personas, pero JSON es lo que la mayoría de las APIs y lenguajes de programación esperan. Esta herramienta convierte entre ambos por completo en tu navegador, en ambas direcciones.",
        card2_h="Qué se soporta",
        card2_note='Mapeos y secuencias en bloque y en línea, escalares entre comillas y planos, números, booleanos, null, y comentarios. Anclas/alias, archivos multi-documento, y escalares de bloque multilínea (<code>|</code> / <code>&gt;</code>) no están soportados.',
        how_h2="Cómo funciona",
        how_p1='YAML a JSON ejecuta un pequeño analizador de descenso recursivo escrito para esta página. Primero elimina los comentarios (con cuidado, para que un <code>#</code> dentro de una cadena entre comillas sobreviva), registra la indentación de cada línea, luego construye la estructura tal como YAML la define: la indentación abre mapas anidados, las líneas que empiezan con <code>-</code> construyen secuencias, y todo lo demás es un escalar. Los escalares se tipan con las mismas reglas que usan los analizadores YAML reales: <code>true</code>/<code>false</code> se convierten en booleanos, <code>~</code> y <code>null</code> se convierten en null, los números sin comillas se convierten en números, las cadenas entre comillas siguen siendo cadenas, y la sintaxis de flujo en línea <code>[a, b]</code> o <code>{{k: v}}</code> también se maneja. El resultado se serializa con <code>JSON.stringify</code> en la sangría que elijas. JSON a YAML es lo inverso: <code>JSON.parse</code> valida la entrada, luego un emisor recorre el valor y escribe YAML indentado, entrecomillando cualquier cadena que de otro modo se leería mal como número, booleano, o null.',
        how_p2='Una decisión deliberada que vale la pena conocer: este analizador solo trata los literales <code>true</code> y <code>false</code> como booleanos. Los analizadores YAML 1.1 más antiguos también convierten <code>yes</code>, <code>no</code>, <code>on</code>, y <code>off</code>, que es como el código de país de Noruega <code>NO</code> se convierte famosamente en <code>false</code> en archivos de configuración (el "problema de Noruega"). Aquí se mantiene como la cadena que parece ser.',
        how_p3='Es un analizador de subconjunto, mantenido pequeño a propósito: las anclas y alias (<code>&amp;</code>/<code>*</code>), los archivos multi-documento, y los escalares de bloque (<code>|</code> y <code>&gt;</code>) no están soportados, así que un manifiesto de Kubernetes complejo que use esas características no hará un round-trip correcto. Para la conversión de configuración cotidiana, cubre lo que realmente pegas.',
        how_p4="La conversión ocurre por completo en tu pestaña con cada pulsación de tecla. No se llama a ningún servicio de análisis: el panel Red de las DevTools permanece en silencio mientras escribes, así que los archivos de configuración llenos de nombres de host y secretos nunca salen de tu máquina.",
    ),
    related_tools=[
        ("csv-to-json.html", "CSV a JSON", "Convierte un archivo CSV a JSON."),
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica JSON."),
        ("json-diff.html", "JSON Diff", "Compara dos documentos JSON."),
    ],
)

PAGES["zh"] = dict(
    title="YAML 转 JSON 转换器（双向）| norito",
    meta_desc="在浏览器中实时将 YAML 转换为 JSON，或将 JSON 转换为 YAML。支持映射、序列、引号字符串和注释。不上传任何内容。",
    app_name="YAML 转 JSON 转换器", h1="YAML 转 JSON 转换器", breadcrumb_label="YAML 转 JSON 转换器",
    lede="将 YAML 转换为 JSON，或将 JSON 转换为 YAML，边输入边实时转换。完全在浏览器中运行，粘贴的内容不会上传。",
    t=dict(
        json_indent="JSON 缩进", spaces2="2 个空格", spaces4="4 个空格",
        input="输入", paste_yaml="粘贴 YAML...", output="输出", swap="交换", copy_output="复制输出",
        card1_h="配置文件，随处可用", card1_p="YAML 常见于 Docker Compose、Kubernetes 和 CI 配置文件中。",
        card1_note="YAML 对人类来说更易读易改，但大多数 API 和编程语言需要的是 JSON。这个工具完全在浏览器中双向转换这两种格式。",
        card2_h="支持哪些内容",
        card2_note='支持块状和流式映射与序列、带引号和不带引号的标量、数字、布尔值、null，以及注释。不支持锚点/别名、多文档文件，以及多行块状标量（<code>|</code> / <code>&gt;</code>）。',
        how_h2="工作原理",
        how_p1='YAML 转 JSON 使用一个为此页面编写的小型递归下降解析器。它首先去除注释（会小心处理，确保引号字符串内的 <code>#</code> 不会被误删），记录每一行的缩进，然后按照 YAML 定义的方式构建结构：缩进用于打开嵌套的映射，以 <code>-</code> 开头的行用于构建序列，其余内容作为标量处理。标量的类型判断规则与真实的 YAML 解析器一致：<code>true</code>/<code>false</code> 转为布尔值，<code>~</code> 和 <code>null</code> 转为 null，裸数字转为数字，带引号的字符串保持为字符串，行内的 <code>[a, b]</code> 或 <code>{{k: v}}</code> 流式语法也能正确处理。结果通过 <code>JSON.stringify</code> 按你选择的缩进序列化输出。JSON 转 YAML 则是相反的过程：<code>JSON.parse</code> 校验输入，然后一个生成器遍历该值并写出带缩进的 YAML，对任何可能被误读为数字、布尔值或 null 的字符串加上引号。',
        how_p2='有一个刻意的设计选择值得了解：这个解析器只把字面量 <code>true</code> 和 <code>false</code> 当作布尔值。较旧的 YAML 1.1 解析器还会把 <code>yes</code>、<code>no</code>、<code>on</code>、<code>off</code> 转换为布尔值，这正是挪威国家代码 <code>NO</code> 在配置文件中著名地变成 <code>false</code> 的原因（「挪威问题」）。在这里，它会保持看起来的样子，仍是字符串。',
        how_p3='这是一个有意保持精简的子集解析器：不支持锚点和别名（<code>&amp;</code>/<code>*</code>）、多文档文件，以及块状标量（<code>|</code> 和 <code>&gt;</code>），因此使用这些特性的复杂 Kubernetes 清单文件无法正确来回转换。对于日常的配置转换来说，它能覆盖你实际会粘贴的内容。',
        how_p4="转换在你每次按键时完全在当前标签页内完成。不会调用任何解析服务：你在输入时开发者工具的 Network 面板始终保持静默，因此包含主机名和密钥的配置文件永远不会离开你的电脑。",
    ),
    related_tools=[
        ("csv-to-json.html", "CSV 转 JSON", "将 CSV 文件转换为 JSON。"),
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩 JSON。"),
        ("json-diff.html", "JSON 对比", "比较两份 JSON 文档。"),
    ],
)

PAGES["ar"] = dict(
    title="محوّل YAML إلى JSON (والعكس) | norito",
    meta_desc="حوّل YAML إلى JSON أو JSON إلى YAML، مباشرةً في متصفحك. يدعم الخرائط والتسلسلات والسلاسل المقتبسة والتعليقات. لا شيء يُرفَع.",
    app_name="محوّل YAML إلى JSON", h1="محوّل YAML إلى JSON", breadcrumb_label="محوّل YAML إلى JSON",
    lede="حوّل YAML إلى JSON أو JSON إلى YAML، مباشرةً أثناء الكتابة. يعمل بالكامل في متصفحك، لا شيء مما تلصقه يُرفَع.",
    t=dict(
        json_indent="مسافة بادئة JSON", spaces2="مسافتان", spaces4="4 مسافات",
        input="الإدخال", paste_yaml="الصق YAML...", output="الإخراج", swap="تبديل", copy_output="نسخ الإخراج",
        card1_h="ملفات إعدادات قابلة للنقل", card1_p="YAML شائع في Docker Compose وKubernetes وإعدادات CI.",
        card1_note="YAML أسهل للبشر في القراءة والتحرير، لكن JSON هو ما تتوقعه معظم واجهات API ولغات البرمجة. تُحوِّل هذه الأداة بين الاثنين بالكامل داخل متصفحك، في كلا الاتجاهين.",
        card2_h="ما المدعوم",
        card2_note='الخرائط والتسلسلات الكتلية والانسيابية، السلاسل المقتبسة والعادية، الأرقام، القيم المنطقية، null، والتعليقات. المراسي والأسماء المستعارة، والملفات متعددة المستندات، وسلاسل الكتل متعددة الأسطر (<code>|</code> / <code>&gt;</code>) غير مدعومة.',
        how_h2="كيف تعمل",
        how_p1='يعمل محوّل YAML إلى JSON عبر محلل تنازلي تكراري صغير مكتوب خصيصًا لهذه الصفحة. يزيل أولاً التعليقات (بعناية، بحيث تنجو علامة <code>#</code> داخل سلسلة مقتبسة)، ويسجّل مسافة الإزاحة لكل سطر، ثم يبني البنية بالطريقة التي يعرّفها YAML: الإزاحة تفتح خرائط متداخلة، والأسطر التي تبدأ بـ <code>-</code> تبني تسلسلات، وكل ما عدا ذلك هو قيمة عددية (scalar). تُصنَّف القيم العددية وفق نفس القواعد التي تستخدمها محلّلات YAML الحقيقية: تصبح <code>true</code>/<code>false</code> قيمًا منطقية، وتصبح <code>~</code> و<code>null</code> قيمة null، وتصبح الأرقام المجردة أرقامًا، وتبقى السلاسل المقتبسة سلاسل، وتُعالَج أيضًا صياغة التدفق المضمّنة مثل <code>[a, b]</code> أو <code>{{k: v}}</code>. تُسلسَل النتيجة باستخدام <code>JSON.stringify</code> بمسافة الإزاحة التي تختارها. أما JSON إلى YAML فهو العكس: يتحقق <code>JSON.parse</code> من صحة الإدخال، ثم يمر مُصدِر عبر القيمة ويكتب YAML بإزاحة مناسبة، مع وضع أي سلسلة قد تُقرأ خطأً كرقم أو قيمة منطقية أو null بين علامتي اقتباس.',
        how_p2='خيار مقصود يستحق المعرفة: يعامل هذا المحلل فقط الحرفيتين <code>true</code> و<code>false</code> كقيم منطقية. محلّلات YAML 1.1 الأقدم تحوّل أيضًا <code>yes</code> و<code>no</code> و<code>on</code> و<code>off</code>، وهذا بالضبط كيف يتحول رمز دولة النرويج <code>NO</code> بشكل شهير إلى <code>false</code> في ملفات الإعداد ("مشكلة النرويج"). هنا يبقى كما يبدو: سلسلة نصية.',
        how_p3='إنه محلل مجموعة جزئية، مُبقًى صغيرًا عمدًا: المراسي والأسماء المستعارة (<code>&amp;</code>/<code>*</code>)، والملفات متعددة المستندات، وسلاسل الكتل (<code>|</code> و<code>&gt;</code>) غير مدعومة، لذا فإن بيان Kubernetes معقدًا يستخدم هذه الميزات لن يُحوَّل ذهابًا وإيابًا بشكل صحيح. بالنسبة لتحويل الإعدادات اليومية، فهو يغطي ما تلصقه فعليًا.',
        how_p4="يحدث التحويل بالكامل داخل تبويبك مع كل ضغطة مفتاح. لا يُستدعى أي خادم تحليل: تبقى لوحة Network في أدوات المطوّر صامتة أثناء الكتابة، لذا فإن ملفات الإعداد المليئة بأسماء المضيفين والأسرار لا تغادر جهازك أبدًا.",
    ),
    related_tools=[
        ("csv-to-json.html", "CSV إلى JSON", "حوّل ملف CSV إلى JSON."),
        ("json-formatter.html", "منسّق JSON", "نسّق وتحقق ومصغّر JSON."),
        ("json-diff.html", "مقارنة JSON", "قارن بين مستندي JSON."),
    ],
)

PAGES["hi"] = dict(
    title="YAML से JSON कनवर्टर (और वापस) | norito",
    meta_desc="YAML को JSON में या JSON को YAML में बदलें, आपके ब्राउज़र में लाइव. मैपिंग, सीक्वेंस, कोट की गई स्ट्रिंग्स, और कमेंट्स को हैंडल करता है. कुछ भी अपलोड नहीं होता.",
    app_name="YAML से JSON कनवर्टर", h1="YAML से JSON कनवर्टर", breadcrumb_label="YAML से JSON कनवर्टर",
    lede="YAML को JSON में या JSON को YAML में बदलें, टाइप करते ही लाइव. पूरी तरह आपके ब्राउज़र में चलता है, जो भी आप पेस्ट करते हैं वह अपलोड नहीं होता.",
    t=dict(
        json_indent="JSON इंडेंट", spaces2="2 स्पेस", spaces4="4 स्पेस",
        input="इनपुट", paste_yaml="YAML पेस्ट करें...", output="आउटपुट", swap="स्वैप करें", copy_output="आउटपुट कॉपी करें",
        card1_h="कॉन्फ़िग फ़ाइलें, पोर्टेबल बनी", card1_p="YAML, Docker Compose, Kubernetes, और CI कॉन्फ़िग में आम है.",
        card1_note="YAML लोगों के पढ़ने और एडिट करने के लिए आसान है, लेकिन ज़्यादातर API और प्रोग्रामिंग भाषाओं को JSON चाहिए होता है. यह टूल दोनों के बीच पूरी तरह आपके ब्राउज़र में, दोनों दिशाओं में कन्वर्ट करता है.",
        card2_h="क्या सपोर्टेड है",
        card2_note='ब्लॉक और फ़्लो मैपिंग और सीक्वेंस, कोट की गई और प्लेन स्केलर वैल्यूज़, नंबर, बूलियन, null, और कमेंट्स. एंकर/एलियास, मल्टी-डॉक्यूमेंट फ़ाइलें, और मल्टीलाइन ब्लॉक स्केलर (<code>|</code> / <code>&gt;</code>) सपोर्टेड नहीं हैं.',
        how_h2="यह कैसे काम करता है",
        how_p1='YAML से JSON इस पेज के लिए लिखे गए एक छोटे रिकर्सिव-डिसेंट पार्सर को चलाता है. यह पहले कमेंट्स हटाता है (सावधानी से, ताकि कोट की गई स्ट्रिंग के अंदर मौजूद <code>#</code> बचा रहे), हर लाइन का इंडेंटेशन रिकॉर्ड करता है, फिर उस तरीके से स्ट्रक्चर बनाता है जैसे YAML इसे डिफ़ाइन करता है: इंडेंटेशन नेस्टेड मैप्स खोलता है, <code>-</code> से शुरू होने वाली लाइनें सीक्वेंस बनाती हैं, और बाकी सब एक स्केलर होता है. स्केलर्स को उन्हीं नियमों से टाइप किया जाता है जो असली YAML पार्सर इस्तेमाल करते हैं: <code>true</code>/<code>false</code> बूलियन बन जाते हैं, <code>~</code> और <code>null</code>, null बन जाते हैं, बिना कोट के नंबर, नंबर बन जाते हैं, कोट की गई स्ट्रिंग्स स्ट्रिंग ही रहती हैं, और इनलाइन <code>[a, b]</code> या <code>{{k: v}}</code> फ़्लो सिंटैक्स भी हैंडल होता है. रिज़ल्ट को आपके चुने इंडेंट पर <code>JSON.stringify</code> से सीरियलाइज़ किया जाता है. JSON से YAML उल्टा है: <code>JSON.parse</code> इनपुट को वैलिडेट करता है, फिर एक एमिटर वैल्यू पर चलकर इंडेंटेड YAML लिखता है, और किसी भी ऐसी स्ट्रिंग को कोट करता है जो वरना नंबर, बूलियन, या null के तौर पर गलत पढ़ी जाती.',
        how_p2='एक जान-बूझकर लिया गया फ़ैसला जानना ज़रूरी है: यह पार्सर सिर्फ़ लिटरल <code>true</code> और <code>false</code> को बूलियन मानता है. पुराने YAML 1.1 पार्सर <code>yes</code>, <code>no</code>, <code>on</code>, और <code>off</code> को भी कन्वर्ट कर देते हैं, यही वजह है कि नॉर्वे का कंट्री कोड <code>NO</code> मशहूर तरीके से कॉन्फ़िग फ़ाइलों में <code>false</code> बन जाता है ("नॉर्वे प्रॉब्लम"). यहां यह वैसी ही स्ट्रिंग बना रहता है जैसा यह दिखता है.',
        how_p3='यह एक सबसेट पार्सर है, जिसे जान-बूझकर छोटा रखा गया है: एंकर और एलियास (<code>&amp;</code>/<code>*</code>), मल्टी-डॉक्यूमेंट फ़ाइलें, और ब्लॉक स्केलर (<code>|</code> और <code>&gt;</code>) सपोर्टेड नहीं हैं, इसलिए इन फ़ीचर्स का इस्तेमाल करने वाला कोई कॉम्प्लेक्स Kubernetes मैनिफ़ेस्ट सही तरीके से राउंड-ट्रिप नहीं करेगा. रोज़मर्रा के कॉन्फ़िग कन्वर्ज़न के लिए, यह वही कवर करता है जो आप असल में पेस्ट करते हैं.',
        how_p4="कन्वर्ज़न हर कीस्ट्रोक पर पूरी तरह आपके टैब में होता है. किसी पार्सर सर्विस को कॉल नहीं किया जाता: आपके टाइप करते समय DevTools का Network पैनल खामोश रहता है, इसलिए होस्टनेम और सीक्रेट्स से भरी कॉन्फ़िग फ़ाइलें कभी आपकी मशीन से बाहर नहीं जातीं.",
    ),
    related_tools=[
        ("csv-to-json.html", "CSV से JSON", "किसी CSV फ़ाइल को JSON में बदलें."),
        ("json-formatter.html", "JSON फ़ॉर्मेटर", "JSON फ़ॉर्मेट करें, वैलिडेट करें, और मिनिफ़ाई करें."),
        ("json-diff.html", "JSON डिफ़", "दो JSON डॉक्यूमेंट्स की तुलना करें."),
    ],
)

PAGES["ru"] = dict(
    title="Конвертер YAML в JSON (и обратно) | norito",
    meta_desc="Конвертируйте YAML в JSON или JSON в YAML прямо в браузере. Поддерживает отображения, последовательности, строки в кавычках и комментарии. Ничего не загружается.",
    app_name="Конвертер YAML в JSON", h1="Конвертер YAML в JSON", breadcrumb_label="Конвертер YAML в JSON",
    lede="Конвертируйте YAML в JSON или JSON в YAML в реальном времени по мере ввода. Работает полностью в браузере, ничего из вставленного не загружается.",
    t=dict(
        json_indent="Отступ JSON", spaces2="2 пробела", spaces4="4 пробела",
        input="Ввод", paste_yaml="Вставьте YAML...", output="Вывод", swap="Поменять местами", copy_output="Скопировать вывод",
        card1_h="Конфигурационные файлы, переносимые", card1_p="YAML часто встречается в Docker Compose, Kubernetes и конфигурациях CI.",
        card1_note="YAML легче читать и редактировать людям, но большинство API и языков программирования ожидают JSON. Этот инструмент конвертирует между ними полностью в браузере, в обоих направлениях.",
        card2_h="Что поддерживается",
        card2_note='Блочные и потоковые отображения и последовательности, строки в кавычках и без них, числа, булевы значения, null и комментарии. Якоря/алиасы, многодокументные файлы и многострочные блочные скаляры (<code>|</code> / <code>&gt;</code>) не поддерживаются.',
        how_h2="Как это работает",
        how_p1='YAML в JSON запускает небольшой рекурсивный нисходящий парсер, написанный специально для этой страницы. Сначала он удаляет комментарии (аккуратно, чтобы <code>#</code> внутри строки в кавычках сохранился), фиксирует отступ каждой строки, затем строит структуру так, как это определяет YAML: отступ открывает вложенные отображения, строки, начинающиеся с <code>-</code>, формируют последовательности, а всё остальное — скаляр. Скаляры типизируются по тем же правилам, что и в настоящих парсерах YAML: <code>true</code>/<code>false</code> становятся булевыми значениями, <code>~</code> и <code>null</code> становятся null, числа без кавычек становятся числами, строки в кавычках остаются строками, а встроенный потоковый синтаксис <code>[a, b]</code> или <code>{{k: v}}</code> тоже обрабатывается. Результат сериализуется через <code>JSON.stringify</code> с выбранным вами отступом. JSON в YAML — обратный процесс: <code>JSON.parse</code> проверяет ввод, затем эмиттер проходит по значению и записывает YAML с отступами, заключая в кавычки любую строку, которая иначе была бы неверно прочитана как число, булево значение или null.',
        how_p2='Осознанное решение, о котором стоит знать: этот парсер трактует как булевы значения только буквальные <code>true</code> и <code>false</code>. Более старые парсеры YAML 1.1 также преобразуют <code>yes</code>, <code>no</code>, <code>on</code> и <code>off</code>, из-за чего код страны Норвегии <code>NO</code> печально известно превращается в <code>false</code> в конфигурационных файлах («проблема Норвегии»). Здесь он остаётся той строкой, какой и выглядит.',
        how_p3='Это парсер подмножества, намеренно сделанный небольшим: якоря и алиасы (<code>&amp;</code>/<code>*</code>), многодокументные файлы и блочные скаляры (<code>|</code> и <code>&gt;</code>) не поддерживаются, поэтому сложный манифест Kubernetes, использующий эти возможности, не пройдёт конвертацию туда и обратно корректно. Для повседневной конвертации конфигураций он покрывает именно то, что вы реально вставляете.',
        how_p4="Конвертация происходит полностью в вашей вкладке при каждом нажатии клавиши. Никакой сервис парсинга не вызывается: панель Network в DevTools остаётся безмолвной, пока вы печатаете, поэтому конфигурационные файлы, полные имён хостов и секретов, никогда не покидают ваш компьютер.",
    ),
    related_tools=[
        ("csv-to-json.html", "CSV в JSON", "Преобразуйте файл CSV в JSON."),
        ("json-formatter.html", "Форматирование JSON", "Форматирование, проверка и минификация JSON."),
        ("json-diff.html", "Сравнение JSON", "Сравните два JSON-документа."),
    ],
)

PAGES["ja"] = dict(
    title="YAML から JSON への変換ツール（相互変換）| norito",
    meta_desc="YAMLをJSONに、またはJSONをYAMLにブラウザ内でリアルタイム変換。マッピング、シーケンス、引用符付き文字列、コメントに対応。アップロードなし。",
    app_name="YAMLからJSONへの変換ツール", h1="YAMLからJSONへの変換ツール", breadcrumb_label="YAMLからJSONへの変換ツール",
    lede="YAMLをJSONに、またはJSONをYAMLに、入力しながらリアルタイムで変換します。すべてブラウザ内で動作し、貼り付けた内容がアップロードされることはありません。",
    t=dict(
        json_indent="JSONインデント", spaces2="スペース2個", spaces4="スペース4個",
        input="入力", paste_yaml="YAMLを貼り付け...", output="出力", swap="入れ替え", copy_output="出力をコピー",
        card1_h="設定ファイルを、どこでも使えるように", card1_p="YAMLはDocker Compose、Kubernetes、CI設定でよく使われます。",
        card1_note="YAMLは人間が読み書きしやすい形式ですが、ほとんどのAPIやプログラミング言語が想定しているのはJSONです。このツールはブラウザ内だけで、双方向にこの2つを変換します。",
        card2_h="対応している内容",
        card2_note='ブロック形式・フロー形式のマッピングとシーケンス、引用符付き・プレーンなスカラー値、数値、真偽値、null、コメントに対応しています。アンカー／エイリアス、複数ドキュメントファイル、複数行のブロックスカラー（<code>|</code> / <code>&gt;</code>）には対応していません。',
        how_h2="仕組み",
        how_p1='YAMLからJSONへの変換は、このページ専用に書かれた小さな再帰下降パーサーで行われます。まずコメントを除去し（引用符付き文字列内の<code>#</code>が誤って消えないよう慎重に処理します）、各行のインデントを記録した上で、YAMLの定義どおりに構造を構築します。インデントはネストしたマップを開き、<code>-</code>で始まる行はシーケンスを構築し、それ以外はすべてスカラー値になります。スカラー値は実際のYAMLパーサーと同じルールで型付けされます。<code>true</code>/<code>false</code>は真偽値に、<code>~</code>と<code>null</code>はnullに、引用符のない数字は数値に、引用符付き文字列はそのまま文字列となり、インラインの<code>[a, b]</code>や<code>{{k: v}}</code>のようなフロー構文も処理されます。結果は選択したインデントで<code>JSON.stringify</code>によりシリアライズされます。JSONからYAMLはその逆で、<code>JSON.parse</code>で入力を検証した後、エミッターが値をたどってインデント付きのYAMLを書き出し、数値・真偽値・nullと誤読されうる文字列には引用符を付けます。',
        how_p2='知っておく価値のある意図的な選択があります。このパーサーはリテラルの<code>true</code>と<code>false</code>のみを真偽値として扱います。古いYAML 1.1パーサーは<code>yes</code>、<code>no</code>、<code>on</code>、<code>off</code>も変換してしまい、これがノルウェーの国コード<code>NO</code>が設定ファイル内で有名にも<code>false</code>になってしまう原因です（いわゆる「ノルウェー問題」）。ここでは見た目どおりの文字列のまま保たれます。',
        how_p3='これは意図的に小さく保たれたサブセットパーサーです。アンカーとエイリアス（<code>&amp;</code>/<code>*</code>）、複数ドキュメントファイル、ブロックスカラー（<code>|</code>と<code>&gt;</code>）には対応していないため、これらの機能を使う複雑なKubernetesマニフェストは正しく往復変換できません。日常的な設定変換であれば、実際に貼り付ける内容はカバーされています。',
        how_p4="変換はキーストロークのたびに、すべてタブ内で完結します。パーサーサービスは一切呼び出されません。入力中はDevToolsのNetworkパネルが静かなままなので、ホスト名やシークレットが詰まった設定ファイルが端末から出ていくことはありません。",
    ),
    related_tools=[
        ("csv-to-json.html", "CSVからJSONへ", "CSVファイルをJSONに変換。"),
        ("json-formatter.html", "JSONフォーマッター", "JSONの整形、検証、圧縮。"),
        ("json-diff.html", "JSON差分比較", "2つのJSONドキュメントを比較。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "yaml-to-json-converter.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-yaml-json.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/yaml-to-json-converter.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
