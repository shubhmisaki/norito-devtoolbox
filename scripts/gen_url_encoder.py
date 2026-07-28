#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>'
ICON_CLASS = "c-amber"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="tabs" id="mode-tabs" role="tablist" style="margin-bottom:20px;">
          <button type="button" class="tab active" data-value="encode">{t['encode']}</button>
          <button type="button" class="tab" data-value="decode">{t['decode']}</button>
        </div>
        <select id="mode" style="display:none;">
          <option value="encode">encode</option>
          <option value="decode">decode</option>
        </select>

        <div class="field" style="margin-bottom:16px;">
          <label for="encodeType">{t['encoding_type']}</label>
          <select id="encodeType">
            <option value="component" selected>{t['component_opt']}</option>
            <option value="full">{t['full_opt']}</option>
          </select>
        </div>

        <div class="field" style="margin-bottom:16px;">
          <label for="input">{t['input']}</label>
          <textarea id="input" class="mono-area" rows="6" placeholder="{t['ph_input']}"></textarea>
        </div>

        <div class="result-box error" id="errorBox" style="display:none; margin-bottom:16px;">
          <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
          <div class="r-body"></div>
        </div>

        <div class="field" style="margin-top:16px;">
          <label for="output">{t['output']}</label>
          <textarea id="output" class="mono-area" rows="6" readonly></textarea>
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
            <div class="icon-chip c-amber" style="width:36px;height:36px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>
            </div>
            <div>
              <h3>{t['side1_h']}</h3>
              <p>{t['side1_sub']}</p>
            </div>
          </div>
          <p class="note" style="margin-top:0;">
            {t['side1_body']}
          </p>
        </div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['side2_h']}</h3>
          <p class="note" style="margin-top:0;">
            {t['side2_body']}
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
    title="Codificador / Decodificador de URL Online | norito",
    meta_desc="Codifica o decodifica una URL o un componente de URL (percent-encoding), en vivo en tu navegador. Modos de componente y URI completa. No se sube nada.",
    app_name="Codificador / Decodificador de URL", h1="Codificador / Decodificador de URL", breadcrumb_label="Codificador / Decodificador de URL",
    lede="Codifica o decodifica en porcentaje una URL o un solo componente de URL, en vivo mientras escribes. Nada de lo que escribes se envía a ningún sitio.",
    t=dict(
        encode="Codificar", decode="Decodificar", encoding_type="Tipo de codificación",
        component_opt="Componente (encodeURIComponent), recomendado", full_opt="URI completa (encodeURI)",
        input="Entrada", ph_input="Escribe o pega texto o una URL...", output="Salida",
        swap="Intercambiar", copy_output="Copiar salida",
        side1_h="Componente vs. URI completa", side1_sub="Codifican caracteres diferentes.",
        side1_body='<strong>Componente</strong> escapa todo lo que no es seguro dentro de un solo segmento de URL, incluyendo <code>&amp;</code>, <code>=</code>, y <code>?</code>, úsalo para el valor de un parámetro de consulta. <strong>URI completa</strong> deja esos caracteres intactos porque tienen significado estructural en una URL completa, úsalo al codificar una dirección entera en vez de una sola parte.',
        side2_h="Por qué codificar una URL",
        side2_body='Las URL solo pueden contener un conjunto limitado de caracteres ASCII. Espacios, letras acentuadas, emoji, y símbolos reservados como <code>&amp;</code> o <code>#</code> necesitan codificarse en porcentaje (como <code>%20</code> para un espacio) para sobrevivir al pasar como parte de un enlace sin romperlo.',
        how_h2="Cómo funciona",
        how_p1='La codificación llama a las funciones propias del navegador <code>encodeURIComponent</code> o <code>encodeURI</code>, las mismas que usa el código JavaScript, así que la salida es exactamente lo que produciría un navegador o una librería HTTP. Cada byte inseguro se convierte en un signo de porcentaje más dos dígitos hexadecimales de su codificación UTF-8: un espacio se convierte en <code>%20</code>, y los caracteres multi-byte se expanden en varios escapes (é es <code>%C3%A9</code>).',
        how_p2='Los dos modos de codificación existen porque "codificar una URL" significa dos cosas distintas. El modo componente escapa todo lo que no sea una letra, un dígito o un puñado de símbolos seguros, incluyendo <code>/ ? &amp; = :</code>. Eso es lo que quieres para un único valor que va dentro de una cadena de consulta, de lo contrario un ampersand dentro del valor parte tu parámetro en dos. El modo URI completa deja los caracteres estructurales intactos para que una URL completa siga funcionando, y solo escapa caracteres que no pueden aparecer en crudo en absoluto. Usar codificación de componente en una URL entera la rompe; usar codificación de URI completa en el valor de un parámetro es un bug de inyección esperando a ocurrir. Elige según lo que estás codificando, no por costumbre.',
        how_p3='El modo de decodificación ejecuta <code>decodeURIComponent</code>, con un extra práctico: los signos más se convierten primero en espacios, porque la codificación de formularios HTML (el formato <code>application/x-www-form-urlencoded</code> que ves en las cadenas de consulta) históricamente escribe los espacios como <code>+</code>. Una entrada malformada, como un <code>%</code> suelto no seguido de dos dígitos hexadecimales, lanza un <code>URIError</code> que la herramienta captura y reporta en vez de mostrar texto medio decodificado. Si al decodificar una vez todavía quedan secuencias <code>%25xx</code>, tu cadena estaba codificada dos veces; pásala por decodificar de nuevo.',
        how_p4='Ambas direcciones son llamadas a una sola función incorporada en tu pestaña. El panel Red de las DevTools no muestra tráfico mientras escribes, así que los tokens y URLs con secretos se quedan en tu máquina.',
    ),
    related_tools=[
        ("base64-encoder.html", "Codificar / Decodificar Base64", "Convierte texto a y desde Base64, seguro para UTF-8."),
        ("html-entity-encoder.html", "Codificador de entidades HTML", "Escapa o desescapa entidades HTML."),
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica JSON."),
    ],
)

PAGES["zh"] = dict(
    title="URL 编码 / 解码工具：在线百分号编码 | norito",
    meta_desc="在浏览器中实时编码或解码 URL 或 URL 组件（百分号编码）。支持组件和完整 URI 两种模式。不上传任何内容。",
    app_name="URL 编码 / 解码工具", h1="URL 编码 / 解码工具", breadcrumb_label="URL 编码 / 解码工具",
    lede="对 URL 或单个 URL 组件进行百分号编码或解码，输入时实时更新。你输入的任何内容都不会被发送到任何地方。",
    t=dict(
        encode="编码", decode="解码", encoding_type="编码类型",
        component_opt="组件（encodeURIComponent），推荐", full_opt="完整 URI（encodeURI）",
        input="输入", ph_input="输入或粘贴文本或 URL...", output="输出",
        swap="交换", copy_output="复制输出",
        side1_h="组件 vs 完整 URI", side1_sub="两者编码的字符不同。",
        side1_body='<strong>组件</strong>编码会转义在单个 URL 片段中不安全的所有字符，包括 <code>&amp;</code>、<code>=</code> 和 <code>?</code>，适用于查询参数值。<strong>完整 URI</strong> 编码会保留这些字符不变，因为它们在完整 URL 中具有结构性意义，适用于编码整个地址而非其中一部分。',
        side2_h="为什么要编码 URL",
        side2_body='URL 只能包含一组有限的 ASCII 字符。空格、带重音的字母、表情符号，以及像 <code>&amp;</code> 或 <code>#</code> 这样的保留符号需要进行百分号编码（例如空格编码为 <code>%20</code>），这样它们才能作为链接的一部分被传递而不破坏链接。',
        how_h2="工作原理",
        how_p1='编码调用的是浏览器自身的 <code>encodeURIComponent</code> 或 <code>encodeURI</code> 函数，与 JavaScript 代码使用的是同一函数，因此输出结果与浏览器或 HTTP 库产生的结果完全一致。每个不安全的字节会变成一个百分号加上其 UTF-8 编码的两位十六进制数字：空格变成 <code>%20</code>，多字节字符会展开成多个转义序列（é 是 <code>%C3%A9</code>）。',
        how_p2='存在两种编码模式，是因为「编码一个 URL」实际上有两种不同的含义。组件模式会转义除字母、数字和少数几个安全符号之外的所有字符，包括 <code>/ ? &amp; = :</code>。这正是你放入查询字符串中的单个值所需要的，否则值中的 & 符号会把你的参数一分为二。完整 URL 模式会保留结构性字符不变，让完整的 URL 继续正常工作，只转义那些完全不能以原始形式出现的字符。对整个 URL 使用组件编码会破坏它；对参数值使用完整 URL 编码则是一个潜在的注入漏洞。应根据你编码的对象来选择，而不是凭习惯。',
        how_p3='解码模式运行 <code>decodeURIComponent</code>，并附加一个实用步骤：加号会先被转换为空格，因为 HTML 表单编码（也就是查询字符串中常见的 <code>application/x-www-form-urlencoded</code> 格式）历来用 <code>+</code> 表示空格。格式错误的输入，比如一个孤立的 <code>%</code> 后面没有跟两位十六进制数字，会抛出 <code>URIError</code>，工具会捕获并报告这个错误，而不是显示部分解码的文本。如果解码一次后仍然留有 <code>%25xx</code> 这样的序列，说明你的字符串被编码了两次；再解码一次即可。',
        how_p4='两个方向都只是标签页里对内置函数的单次调用。开发者工具的 Network 面板在你输入时不会显示任何流量，因此包含密钥的令牌和 URL 都只留在你的电脑上。',
    ),
    related_tools=[
        ("base64-encoder.html", "Base64 编码 / 解码", "文本与 Base64 互转，UTF-8 安全。"),
        ("html-entity-encoder.html", "HTML 实体编码器", "转义或反转义 HTML 实体。"),
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩 JSON。"),
    ],
)

PAGES["ar"] = dict(
    title="أداة ترميز / فك ترميز URL أونلاين | norito",
    meta_desc="رمّز أو فكّ ترميز رابط URL أو جزء منه (ترميز النسبة المئوية)، مباشرة في متصفحك. وضعا الجزء وURI الكامل. لا شيء يُرفَع.",
    app_name="ترميز / فك ترميز URL", h1="ترميز / فك ترميز URL", breadcrumb_label="ترميز / فك ترميز URL",
    lede="رمّز بالنسبة المئوية أو فكّ ترميز رابط URL أو جزء واحد منه، مباشرة أثناء الكتابة. لا شيء تكتبه يُرسَل إلى أي مكان.",
    t=dict(
        encode="ترميز", decode="فك الترميز", encoding_type="نوع الترميز",
        component_opt="جزء (encodeURIComponent)، موصى به", full_opt="URI كامل (encodeURI)",
        input="الإدخال", ph_input="اكتب أو الصق نصًا أو رابطًا...", output="الإخراج",
        swap="تبديل", copy_output="نسخ الإخراج",
        side1_h="الجزء مقابل URI الكامل", side1_sub="كل منهما يرمّز أحرفًا مختلفة.",
        side1_body='ترميز <strong>الجزء</strong> يهرب من كل ما هو غير آمن داخل مقطع واحد من الرابط، بما في ذلك <code>&amp;</code> و<code>=</code> و<code>?</code>، استخدمه لقيمة معامل استعلام. ترميز <strong>URI الكامل</strong> يترك هذه الأحرف كما هي لأن لها معنى بنيويًا في عنوان كامل، استخدمه عند ترميز عنوان كامل بدلاً من جزء واحد منه.',
        side2_h="لماذا نرمّز رابطًا أصلًا",
        side2_body='لا يمكن أن تحتوي الروابط إلا على مجموعة محدودة من أحرف ASCII. المسافات، الأحرف المشكّلة، الرموز التعبيرية، والرموز المحجوزة مثل <code>&amp;</code> أو <code>#</code> تحتاج إلى ترميز بالنسبة المئوية (مثل <code>%20</code> للمسافة) حتى تنجو عند تمريرها كجزء من رابط دون كسره.',
        how_h2="كيف يعمل",
        how_p1='يستدعي الترميز دالتي المتصفح نفسه <code>encodeURIComponent</code> أو <code>encodeURI</code>، وهما نفس الدالتين اللتين يستخدمهما كود جافاسكريبت، لذا يكون الإخراج تمامًا كما ينتجه المتصفح أو مكتبة HTTP. كل بايت غير آمن يتحول إلى علامة نسبة مئوية بالإضافة إلى رقمين سداسيَّي عشريَّين من ترميز UTF-8 الخاص به: تتحول المسافة إلى <code>%20</code>، وتتوسّع الأحرف متعددة البايتات إلى عدة رموز هروب (é هي <code>%C3%A9</code>).',
        how_p2='يوجد وضعا الترميز لأن «ترميز رابط» يعني شيئين مختلفين. وضع الجزء يهرب من كل شيء ليس حرفًا أو رقمًا أو حفنة من الرموز الآمنة، بما في ذلك <code>/ ? &amp; = :</code>. هذا ما تحتاجه لقيمة واحدة تدخل في سلسلة استعلام، وإلا فإن علامة العطف داخل القيمة تقسّم معاملك إلى قسمين. يترك وضع URI الكامل الأحرف البنيوية كما هي حتى يستمر عمل رابط كامل، ولا يهرب إلا من الأحرف التي لا يمكن أن تظهر خامًا على الإطلاق. استخدام ترميز الجزء على رابط كامل يكسره؛ واستخدام ترميز URI الكامل على قيمة معامل هو ثغرة حقن تنتظر أن تحدث. اختر بناءً على ما ترمّزه، لا بناءً على العادة.',
        how_p3='يشغّل وضع فك الترميز <code>decodeURIComponent</code>، مع إضافة عملية واحدة: تُحوَّل علامات الزائد إلى مسافات أولًا، لأن ترميز نماذج HTML (تنسيق <code>application/x-www-form-urlencoded</code> الذي تراه في سلاسل الاستعلام) يكتب المسافات تاريخيًا كـ <code>+</code>. الإدخال المُشوَّه، مثل علامة <code>%</code> منفردة غير متبوعة برقمين سداسيَّي عشريَّين، يُطلِق <code>URIError</code> تلتقطه الأداة وتُبلِغ عنه بدلاً من عرض نص نصف مفكوك الترميز. إذا بقيت تسلسلات <code>%25xx</code> بعد فك الترميز مرة واحدة، فسلسلتك مُرمَّزة مرتين؛ مرّرها عبر فك الترميز مرة أخرى.',
        how_p4='كلا الاتجاهين هما مجرد استدعاء دالة واحدة مدمجة في تبويبك. لوحة Network في أدوات المطوّر لا تُظهر أي حركة أثناء الكتابة، لذا تبقى الرموز والروابط التي تحتوي أسرارًا على جهازك فقط.',
    ),
    related_tools=[
        ("base64-encoder.html", "ترميز / فك ترميز Base64", "حوّل النص من وإلى Base64، آمن مع UTF-8."),
        ("html-entity-encoder.html", "مرمّز كيانات HTML", "هروب أو إلغاء هروب كيانات HTML."),
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق وضغط JSON."),
    ],
)

PAGES["hi"] = dict(
    title="URL एनकोडर / डिकोडर: पर्सेंट-एनकोडिंग ऑनलाइन | norito",
    meta_desc="अपने ब्राउज़र में लाइव URL या URL कॉम्पोनेंट को एनकोड या डिकोड करें (पर्सेंट-एनकोडिंग)। कॉम्पोनेंट और फ़ुल-URI मोड। कुछ भी अपलोड नहीं होता।",
    app_name="URL एनकोडर / डिकोडर", h1="URL एनकोडर / डिकोडर", breadcrumb_label="URL एनकोडर / डिकोडर",
    lede="एक URL या एक सिंगल URL कॉम्पोनेंट को पर्सेंट-एनकोड या डिकोड करें, टाइप करते ही लाइव। आप जो भी टाइप करते हैं वह कहीं नहीं भेजा जाता।",
    t=dict(
        encode="एनकोड करें", decode="डिकोड करें", encoding_type="एनकोडिंग टाइप",
        component_opt="कॉम्पोनेंट (encodeURIComponent), अनुशंसित", full_opt="फ़ुल URI (encodeURI)",
        input="इनपुट", ph_input="टेक्स्ट या URL टाइप या पेस्ट करें...", output="आउटपुट",
        swap="स्वैप करें", copy_output="आउटपुट कॉपी करें",
        side1_h="कॉम्पोनेंट बनाम फ़ुल URI", side1_sub="ये अलग-अलग कैरेक्टर एनकोड करते हैं।",
        side1_body='<strong>कॉम्पोनेंट</strong> एनकोडिंग हर उस चीज़ को एस्केप करती है जो किसी एक URL सेगमेंट के अंदर सेफ़ नहीं है, जिसमें <code>&amp;</code>, <code>=</code>, और <code>?</code> शामिल हैं—इसे किसी क्वेरी पैरामीटर वैल्यू के लिए इस्तेमाल करें। <strong>फ़ुल URI</strong> एनकोडिंग उन कैरेक्टर्स को छोड़ देती है क्योंकि उनका पूरे एड्रेस में स्ट्रक्चरल मतलब होता है—इसे तब इस्तेमाल करें जब आप एक हिस्से की बजाय पूरा URL एनकोड कर रहे हों।',
        side2_h="URL को एनकोड क्यों करें",
        side2_body='URL में सिर्फ़ एक सीमित सेट के ASCII कैरेक्टर्स ही हो सकते हैं। स्पेस, एक्सेंटेड लेटर, इमोजी, और <code>&amp;</code> या <code>#</code> जैसे रिज़र्व्ड सिंबल को पर्सेंट-एनकोड करना ज़रूरी है (जैसे स्पेस के लिए <code>%20</code>) ताकि वे लिंक के हिस्से के रूप में पास होने पर उसे तोड़े बिना बचे रहें।',
        how_h2="यह कैसे काम करता है",
        how_p1='एनकोडिंग ब्राउज़र के अपने <code>encodeURIComponent</code> या <code>encodeURI</code> को कॉल करती है, वही फ़ंक्शन जो JavaScript कोड इस्तेमाल करता है, इसलिए आउटपुट बिल्कुल वही होता है जो एक ब्राउज़र या HTTP लाइब्रेरी प्रोड्यूस करती। हर अनसेफ़ बाइट एक पर्सेंट साइन प्लस उसकी UTF-8 एनकोडिंग के दो हेक्स डिजिट बन जाती है: स्पेस <code>%20</code> बन जाता है, और मल्टी-बाइट कैरेक्टर कई एस्केप में एक्सपैंड होते हैं (é है <code>%C3%A9</code>)।',
        how_p2='दो एनकोड मोड इसलिए हैं क्योंकि "URL एनकोड करना" दो अलग-अलग चीज़ों का मतलब रखता है। कॉम्पोनेंट मोड हर उस चीज़ को एस्केप करता है जो लेटर, डिजिट, या मुट्ठी भर सेफ़ मार्क्स नहीं है, जिसमें <code>/ ? &amp; = :</code> शामिल हैं। क्वेरी स्ट्रिंग में जाने वाली एक सिंगल वैल्यू के लिए आपको यही चाहिए होता है, वरना वैल्यू के अंदर का एम्परसैंड आपके पैरामीटर को दो हिस्सों में बांट देगा। फ़ुल-URL मोड स्ट्रक्चरल कैरेक्टर्स को छोड़ देता है ताकि पूरा URL काम करता रहे, और सिर्फ़ उन कैरेक्टर्स को एस्केप करता है जो बिल्कुल रॉ फ़ॉर्म में नहीं आ सकते। पूरे URL पर कॉम्पोनेंट एनकोडिंग इस्तेमाल करना उसे तोड़ देता है; किसी पैरामीटर वैल्यू पर फ़ुल-URL एनकोडिंग इस्तेमाल करना एक इंजेक्शन बग का इंतज़ार है। आप क्या एनकोड कर रहे हैं उसके हिसाब से चुनें, आदत के हिसाब से नहीं।',
        how_p3='डिकोड मोड <code>decodeURIComponent</code> चलाता है, एक प्रैक्टिकल एक्स्ट्रा के साथ: प्लस साइन को पहले स्पेस में बदला जाता है, क्योंकि HTML फ़ॉर्म एनकोडिंग (वह <code>application/x-www-form-urlencoded</code> फ़ॉर्मैट जो आप क्वेरी स्ट्रिंग्स में देखते हैं) ऐतिहासिक रूप से स्पेस को <code>+</code> के रूप में लिखती है। मैलफ़ॉर्म्ड इनपुट, जैसे कोई अकेला <code>%</code> जिसके बाद दो हेक्स डिजिट नहीं हों, एक <code>URIError</code> थ्रो करता है जिसे टूल कैच करके रिपोर्ट करता है, बजाय आधा-डिकोडेड टेक्स्ट दिखाने के। अगर एक बार डिकोड करने के बाद भी <code>%25xx</code> सीक्वेंस बचे रहते हैं, तो आपकी स्ट्रिंग दो बार एनकोड हुई थी; इसे दोबारा डिकोड से गुज़ारें।',
        how_p4='दोनों दिशाएं आपके टैब में सिंगल बिल्ट-इन फ़ंक्शन कॉल हैं। डेवटूल्स का Network पैनल टाइप करते समय कोई ट्रैफ़िक नहीं दिखाता, इसलिए सीक्रेट्स वाले टोकन और URL आपकी मशीन पर ही रहते हैं।',
    ),
    related_tools=[
        ("base64-encoder.html", "Base64 एनकोड / डिकोड", "टेक्स्ट को Base64 में और वापस बदलें, UTF-8 सेफ़।"),
        ("html-entity-encoder.html", "HTML एंटिटी एनकोडर", "HTML एंटिटीज़ को एस्केप या अनएस्केप करें।"),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "JSON फ़ॉर्मैट, वैलिडेट और मिनिफ़ाई करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Кодировщик / декодировщик URL онлайн | norito",
    meta_desc="Кодируйте или декодируйте URL или компонент URL (percent-encoding), прямо в браузере. Режимы компонента и полного URI. Ничего не загружается.",
    app_name="Кодировщик / декодировщик URL", h1="Кодировщик / декодировщик URL", breadcrumb_label="Кодировщик / декодировщик URL",
    lede="Кодируйте в процентном формате или декодируйте URL или один компонент URL прямо во время ввода. Ничего из введённого никуда не отправляется.",
    t=dict(
        encode="Кодировать", decode="Декодировать", encoding_type="Тип кодирования",
        component_opt="Компонент (encodeURIComponent), рекомендуется", full_opt="Полный URI (encodeURI)",
        input="Ввод", ph_input="Введите или вставьте текст или URL...", output="Вывод",
        swap="Поменять местами", copy_output="Скопировать вывод",
        side1_h="Компонент vs полный URI", side1_sub="Они кодируют разные символы.",
        side1_body='Кодирование <strong>компонента</strong> экранирует всё, что небезопасно внутри одного сегмента URL, включая <code>&amp;</code>, <code>=</code> и <code>?</code>, используйте его для значения параметра запроса. Кодирование <strong>полного URI</strong> оставляет эти символы нетронутыми, поскольку они структурно значимы в полном URL, используйте его при кодировании целого адреса, а не одной его части.',
        side2_h="Зачем вообще кодировать URL",
        side2_body='URL может содержать лишь ограниченный набор ASCII-символов. Пробелы, буквы с диакритикой, эмодзи и зарезервированные символы вроде <code>&amp;</code> или <code>#</code> нужно кодировать в процентном формате (например, <code>%20</code> для пробела), чтобы они уцелели при передаче в составе ссылки, не сломав её.',
        how_h2="Как это работает",
        how_p1='Кодирование вызывает собственные функции браузера <code>encodeURIComponent</code> или <code>encodeURI</code>, те же самые, что использует JavaScript-код, поэтому вывод в точности совпадает с тем, что произвёл бы браузер или HTTP-библиотека. Каждый небезопасный байт превращается в знак процента плюс два шестнадцатеричных символа его UTF-8-кодировки: пробел становится <code>%20</code>, а многобайтовые символы разворачиваются в несколько escape-последовательностей (é это <code>%C3%A9</code>).',
        how_p2='Два режима кодирования существуют потому, что «закодировать URL» означает две разные вещи. Режим компонента экранирует всё, что не является буквой, цифрой или горсткой безопасных символов, включая <code>/ ? &amp; = :</code>. Это то, что нужно для одного значения, попадающего в строку запроса, иначе амперсанд внутри значения разобьёт ваш параметр надвое. Режим полного URL оставляет структурные символы нетронутыми, чтобы полный URL продолжал работать, и экранирует только те символы, которые вообще не могут появляться в необработанном виде. Использование кодирования компонента для целого URL ломает его; использование кодирования полного URL для значения параметра — это готовая уязвимость для инъекции. Выбирайте исходя из того, что кодируете, а не по привычке.',
        how_p3='Режим декодирования запускает <code>decodeURIComponent</code> с одним практичным дополнением: плюсы сначала преобразуются в пробелы, потому что кодирование HTML-форм (формат <code>application/x-www-form-urlencoded</code>, который вы видите в строках запроса) исторически записывает пробелы как <code>+</code>. Некорректный ввод, например одинокий <code>%</code>, за которым не следуют два шестнадцатеричных символа, вызывает <code>URIError</code>, который инструмент перехватывает и сообщает вместо показа наполовину декодированного текста. Если после одного декодирования всё ещё остаются последовательности <code>%25xx</code>, значит строка была закодирована дважды; пропустите её через декодирование ещё раз.',
        how_p4='Оба направления — это единичный вызов встроенной функции в вашей вкладке. Панель Network в DevTools не показывает никакого трафика во время ввода, так что токены и URL с секретами остаются только на вашем компьютере.',
    ),
    related_tools=[
        ("base64-encoder.html", "Кодировщик / декодировщик Base64", "Преобразование текста в Base64 и обратно, безопасно для UTF-8."),
        ("html-entity-encoder.html", "Кодировщик HTML-сущностей", "Экранирование и раскодирование HTML-сущностей."),
        ("json-formatter.html", "Форматирование JSON", "Форматирует, проверяет и минифицирует JSON."),
    ],
)

PAGES["ja"] = dict(
    title="URLエンコード/デコードツール：パーセントエンコーディング | norito",
    meta_desc="URLまたはURLコンポーネントをブラウザ内でリアルタイムにエンコード・デコード（パーセントエンコーディング）。コンポーネントモードと完全URIモード対応。アップロードなし。",
    app_name="URLエンコード/デコードツール", h1="URLエンコード/デコードツール", breadcrumb_label="URLエンコード/デコードツール",
    lede="URLまたは単一のURLコンポーネントをパーセントエンコードまたはデコードします。入力するとリアルタイムに反映され、入力内容はどこにも送信されません。",
    t=dict(
        encode="エンコード", decode="デコード", encoding_type="エンコーディングの種類",
        component_opt="コンポーネント（encodeURIComponent）、推奨", full_opt="完全URI（encodeURI）",
        input="入力", ph_input="テキストまたはURLを入力または貼り付け...", output="出力",
        swap="入れ替え", copy_output="出力をコピー",
        side1_h="コンポーネント vs 完全URI", side1_sub="エンコードする文字が異なります。",
        side1_body='<strong>コンポーネント</strong>エンコードは、URLの1つのセグメント内で安全でないすべての文字をエスケープします。<code>&amp;</code>、<code>=</code>、<code>?</code>を含みます。クエリパラメータの値に使用してください。<strong>完全URI</strong>エンコードは、完全なURL内で構造的な意味を持つため、これらの文字をそのまま残します。一部分ではなくアドレス全体をエンコードする場合に使用してください。',
        side2_h="そもそもなぜURLをエンコードするのか",
        side2_body='URLに使用できるASCII文字は限られています。スペース、アクセント付き文字、絵文字、<code>&amp;</code>や<code>#</code>のような予約記号は、リンクの一部として渡される際にリンクを壊さずに済むよう、パーセントエンコード（スペースなら<code>%20</code>など）する必要があります。',
        how_h2="仕組み",
        how_p1='エンコードはブラウザ自体の<code>encodeURIComponent</code>または<code>encodeURI</code>関数を呼び出します。これはJavaScriptコードが使用するのと同じ関数なので、出力はブラウザやHTTPライブラリが生成するものと完全に一致します。安全でない各バイトは、そのUTF-8エンコーディングのパーセント記号と16進数2桁に変換されます。スペースは<code>%20</code>になり、マルチバイト文字は複数のエスケープシーケンスに展開されます（éは<code>%C3%A9</code>）。',
        how_p2='2つのエンコードモードが存在するのは、「URLをエンコードする」ということが2つの異なる意味を持つためです。コンポーネントモードは、文字、数字、少数の安全な記号を除くすべてをエスケープします。<code>/ ? &amp; = :</code>を含みます。これはクエリ文字列に入る単一の値に必要なもので、そうしないと値の中のアンパサンドがパラメータを2つに分割してしまいます。完全URLモードは構造的な文字をそのまま残し、完全なURLが機能し続けるようにし、生の形で全く出現できない文字だけをエスケープします。URL全体にコンポーネントエンコードを使うと壊れます。パラメータ値に完全URLエンコードを使うとインジェクションのバグにつながります。習慣ではなく、何をエンコードしているかで選んでください。',
        how_p3='デコードモードは<code>decodeURIComponent</code>を実行しますが、1つ実用的な処理が追加されています。プラス記号が先にスペースに変換されます。これは、HTMLフォームエンコーディング（クエリ文字列でよく見る<code>application/x-www-form-urlencoded</code>形式）が歴史的にスペースを<code>+</code>として書いてきたためです。不正な入力、例えば16進数2桁が続かない孤立した<code>%</code>があると<code>URIError</code>が発生しますが、ツールはこれを捕捉して報告し、中途半端にデコードされたテキストを表示することはありません。一度デコードしてもまだ<code>%25xx</code>のようなシーケンスが残っている場合、その文字列は二重にエンコードされています。もう一度デコードにかけてください。',
        how_p4='どちらの方向も、タブ内での組み込み関数の単純な呼び出しです。入力中、DevToolsのNetworkパネルには一切通信が表示されないため、機密情報を含むトークンやURLはあなたのマシン内にとどまります。',
    ),
    related_tools=[
        ("base64-encoder.html", "Base64 エンコード / デコード", "テキストを Base64 との間で変換、UTF-8 セーフ。"),
        ("html-entity-encoder.html", "HTMLエンティティエンコーダー", "HTMLエンティティのエスケープ・アンエスケープ。"),
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証・圧縮。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "url-encoder-decoder.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-url-encoder.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/url-encoder-decoder.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
