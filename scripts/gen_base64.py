#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="14" y="14" width="4" height="6" rx="1"/><rect x="6" y="4" width="4" height="6" rx="1"/><path d="M6 20h4"/><path d="M14 10h4"/><path d="M6 14h2v6"/><path d="M14 4h2v6"/></svg>'
ICON_CLASS = "c-purple"
SWAP_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg>'

TAB_SCRIPT = '''<script>
  document.querySelectorAll("#mode-tabs .tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#mode-tabs .tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const modeSelect = document.getElementById("mode");
      modeSelect.value = btn.dataset.value;
      modeSelect.dispatchEvent(new Event("change"));
    });
  });
</script>
'''

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
          <label for="input">{t['input']}</label>
          <textarea id="input" class="mono-area" rows="6" placeholder="{t['placeholder']}"></textarea>
        </div>

        <div class="option-row">
          <span class="option-label">{t['url_safe']}</span>
          <label class="switch"><input type="checkbox" id="optUrlSafe" /><span class="track"></span></label>
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
            {SWAP_ICON}
            {t['swap']}
          </button>
          <button id="copyBtn">{t['copy_output']}</button>
        </div>
      </div>

      <div>
        <div class="panel">
          <div class="panel-header">
            <div class="icon-chip c-purple" style="width:36px;height:36px;">
              {ICON_SVG}
            </div>
            <div>
              <h3>{t['what_h3']}</h3>
              <p>{t['what_p']}</p>
            </div>
          </div>
          <p class="note" style="margin-top:0;">
            {t['what_note']}
          </p>
        </div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['urlsafe_h3']}</h3>
          <p class="note" style="margin-top:0;">
            {t['urlsafe_note']}
          </p>
        </div>
      </div>
    </div>

    <div class="explain-panel">
      <h2>{t['how_h2']}</h2>
      <p>
        {t['how_p1']}
      </p>
      <p>
        {t['how_p2']}
      </p>
      <p>
        {t['how_p3']}
      </p>
    </div>
'''

PAGES = {}

PAGES["es"] = dict(
    title="Codificar / Decodificar Base64 online, gratis | norito",
    meta_desc="Codifica texto a Base64 o decodifica de vuelta, directamente en tu navegador. Maneja UTF-8 completo, con opción de variante segura para URL.",
    app_name="Codificar / Decodificar Base64", h1="Codificar / Decodificar Base64", breadcrumb_label="Codificar / Decodificar Base64",
    lede="Convierte texto a Base64 o decodifícalo de vuelta, en vivo mientras escribes. Compatibilidad total con UTF-8, así que las letras acentuadas, los emoji y los alfabetos no latinos se conservan correctamente en ambos sentidos.",
    t=dict(
        encode="Codificar", decode="Decodificar", input="Entrada", placeholder="Escribe o pega texto para codificar...",
        url_safe="Variante segura para URL", output="Salida", swap="Intercambiar", copy_output="Copiar salida",
        what_h3="Para qué sirve Base64", what_p="Texto binario seguro, no cifrado.",
        what_note='Base64 convierte bytes arbitrarios en una cadena que usa solo letras, dígitos, <code>+</code> y <code>/</code>, segura para incrustar en JSON, URLs o correos donde el binario crudo se rompería. No es cifrado: cualquiera puede decodificarlo al instante, así que por sí solo no oculta ni protege nada.',
        urlsafe_h3="Variante segura para URL",
        urlsafe_note='Los caracteres <code>+</code> y <code>/</code> del Base64 estándar tienen significado especial en las URLs. La variante segura para URL los cambia por <code>-</code> y <code>_</code> y elimina el relleno <code>=</code> final, así el resultado puede ir directo a una cadena de consulta o a un nombre de archivo.',
        how_h2="Cómo funciona",
        how_p1='Al codificar, tu texto se convierte primero en bytes UTF-8 sin procesar con la API <code>TextEncoder</code> del navegador, y esos bytes se pasan a la función integrada <code>btoa()</code>. Ese primer paso importa: <code>btoa()</code> por sí sola solo maneja caracteres Latin-1 y falla con cualquier otra cosa, así que las herramientas que se saltan ese paso se rompen silenciosamente con emojis, acentos o cualquier alfabeto no latino. Decodificar ejecuta el mismo proceso a la inversa: <code>atob()</code> convierte el Base64 de nuevo en bytes, y <code>TextDecoder</code> los reensambla en texto. El decodificador también es deliberadamente permisivo: recorta espacios en blanco, acepta tanto el alfabeto estándar como el seguro para URL, y vuelve a añadir cualquier relleno <code>=</code> que falte, así que un fragmento copiado directamente de un JWT o una cadena de consulta se decodifica sin necesidad de arreglarlo a mano.',
        how_p2="Espera que la salida sea aproximadamente un 33% más grande que la entrada. Base64 usa 64 símbolos, y 64 símbolos solo pueden transportar 6 bits cada uno, así que cada 3 bytes de entrada se convierten en 4 caracteres de salida. Por eso incrustar una imagen de 1 MB como URI de datos Base64 te cuesta aproximadamente 1,37 MB de HTML, y por eso Base64 es un formato de transporte, no de compresión.",
        how_p3="Ambas direcciones se ejecutan en el propio JavaScript de esta página en cada pulsación, usando solo <code>btoa</code>, <code>atob</code>, y las APIs de codificación de texto que tu navegador ya incluye. Puedes comprobarlo: abre las herramientas de desarrollador, cambia a la pestaña Red, y escribe lo que quieras. Ninguna petición lleva tu texto a ningún sitio.",
    ),
    related_tools=[
        ("/hash-generator.html", "Generador de hashes", "MD5, SHA-1, SHA-256 y SHA-512 de cualquier texto."),
        ("/uuid-generator.html", "Generador de UUID", "Identificadores UUID v4 aleatorios en lote."),
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica JSON con una vista de árbol."),
    ],
)

PAGES["zh"] = dict(
    title="Base64 编码 / 解码，免费在线工具 | norito",
    meta_desc="直接在浏览器中将文本编码为 Base64 或解码回来。完整支持 UTF-8，并可选 URL 安全变体。",
    app_name="Base64 编码 / 解码", h1="Base64 编码 / 解码", breadcrumb_label="Base64 编码 / 解码",
    lede="输入即时将文本转换为 Base64 或解码回来。完整支持 UTF-8，因此带重音符号的字母、表情符号和非拉丁字母都能正确地双向转换。",
    t=dict(
        encode="编码", decode="解码", input="输入", placeholder="输入或粘贴要编码的文本…",
        url_safe="URL 安全变体", output="输出", swap="交换", copy_output="复制输出",
        what_h3="Base64 的用途", what_p="二进制安全文本，不是加密。",
        what_note='Base64 把任意字节转换成一串只由字母、数字、<code>+</code> 和 <code>/</code> 组成的字符串，可以安全地嵌入到原始二进制会出问题的 JSON、URL 或邮件中。它不是加密：任何人都能立即将其解码回来，所以它本身不隐藏也不保护任何东西。',
        urlsafe_h3="URL 安全变体",
        urlsafe_note='标准 Base64 中的 <code>+</code> 和 <code>/</code> 字符在 URL 中具有特殊含义。URL 安全变体会把它们替换为 <code>-</code> 和 <code>_</code>，并去掉末尾的 <code>=</code> 填充符，因此结果可以直接用在查询字符串或文件名中。',
        how_h2="工作原理",
        how_p1='编码时，你的文本首先通过浏览器的 <code>TextEncoder</code> API 转换为原始 UTF-8 字节，然后这些字节被送入内置的 <code>btoa()</code> 函数。这一步很关键：单独使用 <code>btoa()</code> 只能处理 Latin-1 字符，遇到其他字符就会报错，因此跳过这一步的工具在处理表情符号、重音字符或任何非拉丁文字时会悄悄出错。解码则以相反顺序执行同样的流程：<code>atob()</code> 把 Base64 转回字节，<code>TextDecoder</code> 再把这些字节重新组装成文本。解码器还特意做得很宽容：会去除空白，同时接受标准和 URL 安全两种字母表，并自动补回被去掉的 <code>=</code> 填充符，因此直接从 JWT 或查询字符串中复制出来的片段无需手动修正就能正确解码。',
        how_p2="预计输出会比输入大约大 33%。Base64 使用 64 个符号，每个符号只能携带 6 位信息，所以每 3 字节的输入会变成 4 个字符的输出。这就是为什么把一张 1 MB 的图片内联为 Base64 数据 URI 会耗费大约 1.37 MB 的 HTML，也是为什么 Base64 是一种传输格式，而不是压缩格式。",
        how_p3="两个方向的转换都在这个页面自身的 JavaScript 中随每次按键实时运行，只使用 <code>btoa</code>、<code>atob</code> 以及浏览器自带的文本编码 API。你可以自己验证：打开开发者工具，切换到网络面板，随意输入。不会有任何请求把你的文本发送到任何地方。",
    ),
    related_tools=[
        ("/hash-generator.html", "哈希生成器", "任意文本的 MD5、SHA-1、SHA-256 和 SHA-512。"),
        ("/uuid-generator.html", "UUID 生成器", "批量生成随机 UUID v4 标识符。"),
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩 JSON，附带树状视图。"),
    ],
)

PAGES["ar"] = dict(
    title="ترميز / فك ترميز Base64 أونلاين، مجانًا | norito",
    meta_desc="رمّز النص إلى Base64 أو فكّ ترميزه، مباشرةً في متصفحك. دعم كامل لـ UTF-8، مع خيار نسخة آمنة لعناوين URL.",
    app_name="ترميز / فك ترميز Base64", h1="ترميز / فك ترميز Base64", breadcrumb_label="ترميز / فك ترميز Base64",
    lede="حوّل النص إلى Base64 أو فكّ ترميزه، مباشرةً أثناء الكتابة. دعم كامل لـ UTF-8، بحيث تُحفظ الأحرف المنقّطة والإيموجي والأبجديات غير اللاتينية بشكل صحيح في الاتجاهين.",
    t=dict(
        encode="ترميز", decode="فك الترميز", input="الإدخال", placeholder="اكتب أو الصق نصًا للترميز...",
        url_safe="نسخة آمنة لعناوين URL", output="الإخراج", swap="تبديل", copy_output="نسخ الإخراج",
        what_h3="ما فائدة Base64", what_p="نص آمن للبيانات الثنائية، وليس تشفيرًا.",
        what_note='يحوّل Base64 بايتات عشوائية إلى سلسلة تستخدم فقط الأحرف والأرقام و<code>+</code> و<code>/</code>، وهي آمنة للتضمين في JSON أو عناوين URL أو رسائل البريد الإلكتروني حيث قد تتعطل البيانات الثنائية الخام. إنه ليس تشفيرًا: يمكن لأي شخص فك ترميزه فورًا، لذا فهو لا يخفي أو يحمي أي شيء بمفرده.',
        urlsafe_h3="النسخة الآمنة لعناوين URL",
        urlsafe_note='لحرفَي <code>+</code> و<code>/</code> في Base64 القياسي معنى خاص في عناوين URL. تستبدلهما النسخة الآمنة لعناوين URL بـ <code>-</code> و<code>_</code> وتحذف حشو <code>=</code> النهائي، بحيث يمكن استخدام النتيجة مباشرةً في سلسلة استعلام أو اسم ملف.',
        how_h2="كيف يعمل",
        how_p1='عند الترميز، يُحوَّل نصك أولًا إلى بايتات UTF-8 خام باستخدام واجهة <code>TextEncoder</code> الخاصة بالمتصفح، وتُمرَّر تلك البايتات إلى دالة <code>btoa()</code> المدمجة. هذه الخطوة الأولى مهمة: تتعامل <code>btoa()</code> وحدها فقط مع أحرف Latin-1 وتفشل مع أي شيء آخر، لذا فإن الأدوات التي تتخطى هذه الخطوة تتعطل بصمت مع الإيموجي أو الأحرف المنقّطة أو أي أبجدية غير لاتينية. يعمل فك الترميز بنفس الخط بالاتجاه المعاكس: تحوّل <code>atob()</code> Base64 مرة أخرى إلى بايتات، ويعيد <code>TextDecoder</code> تجميعها في نص. كما أن فك الترميز متساهل عمدًا: يزيل المسافات البيضاء، ويقبل كلًا من الأبجدية القياسية والآمنة لعناوين URL، ويعيد إضافة أي حشو <code>=</code> محذوف، بحيث يمكن فك ترميز مقطع منسوخ مباشرةً من JWT أو سلسلة استعلام دون إصلاح يدوي.',
        how_p2="تَوقَّع أن يكون الإخراج أكبر بحوالي 33% من الإدخال. يستخدم Base64 64 رمزًا، ولا يمكن لـ 64 رمزًا أن يحمل سوى 6 بتات لكل منها، لذا فإن كل 3 بايتات من الإدخال تصبح 4 أحرف من الإخراج. لهذا السبب يكلّفك تضمين صورة بحجم 1 ميغابايت كـ URI بيانات Base64 حوالي 1.37 ميغابايت من HTML، ولهذا السبب Base64 هو تنسيق نقل، وليس تنسيق ضغط.",
        how_p3="يعمل كلا الاتجاهين ضمن جافاسكريبت هذه الصفحة نفسها مع كل ضغطة مفتاح، باستخدام <code>btoa</code> و<code>atob</code> فقط وواجهات ترميز النصوص التي يوفّرها متصفحك بالفعل. يمكنك التحقق من ذلك: افتح أدوات المطوّر، انتقل إلى تبويب الشبكة، واكتب كما تشاء. لا يحمل أي طلب نصك إلى أي مكان أبدًا.",
    ),
    related_tools=[
        ("/hash-generator.html", "مولّد التجزئة", "MD5 وSHA-1 وSHA-256 وSHA-512 لأي نص."),
        ("/uuid-generator.html", "مولّد UUID", "معرّفات UUID v4 عشوائية بالجملة."),
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق وضغط JSON مع عرض شجري."),
    ],
)

PAGES["hi"] = dict(
    title="Base64 एनकोड / डिकोड ऑनलाइन, मुफ़्त | norito",
    meta_desc="टेक्स्ट को Base64 में एनकोड करें या वापस डिकोड करें, अपने ब्राउज़र में ही। पूरा UTF-8 सपोर्ट, URL-सेफ़ वेरिएंट विकल्प के साथ।",
    app_name="Base64 एनकोड / डिकोड", h1="Base64 एनकोड / डिकोड", breadcrumb_label="Base64 एनकोड / डिकोड",
    lede="टेक्स्ट को Base64 में बदलें या वापस डिकोड करें, टाइप करते ही लाइव। पूरा UTF-8 सपोर्ट, इसलिए एक्सेंट वाले अक्षर, इमोजी, और नॉन-लैटिन स्क्रिप्ट दोनों दिशाओं में सही तरीके से बरकरार रहती हैं।",
    t=dict(
        encode="एनकोड करें", decode="डिकोड करें", input="इनपुट", placeholder="एनकोड करने के लिए टेक्स्ट टाइप या पेस्ट करें...",
        url_safe="URL-सेफ़ वेरिएंट", output="आउटपुट", swap="स्वैप करें", copy_output="आउटपुट कॉपी करें",
        what_h3="Base64 किसलिए है", what_p="बाइनरी-सेफ़ टेक्स्ट, एन्क्रिप्शन नहीं।",
        what_note='Base64 किसी भी बाइट को केवल अक्षरों, अंकों, <code>+</code>, और <code>/</code> का उपयोग करने वाली एक स्ट्रिंग में बदल देता है, जो JSON, URL, या ईमेल में एम्बेड करने के लिए सुरक्षित है जहाँ रॉ बाइनरी टूट जाती। यह एन्क्रिप्शन नहीं है: कोई भी इसे तुरंत डिकोड कर सकता है, इसलिए यह अपने आप में कुछ भी छिपाता या सुरक्षित नहीं करता।',
        urlsafe_h3="URL-सेफ़ वेरिएंट",
        urlsafe_note='स्टैंडर्ड Base64 के <code>+</code> और <code>/</code> कैरेक्टर का URL में खास मतलब होता है। URL-सेफ़ वेरिएंट इन्हें <code>-</code> और <code>_</code> से बदल देता है और आखिरी <code>=</code> पैडिंग हटा देता है, इसलिए नतीजा सीधे किसी क्वेरी स्ट्रिंग या फ़ाइल नाम में जा सकता है।',
        how_h2="यह कैसे काम करता है",
        how_p1='एनकोड करते समय, आपका टेक्स्ट पहले ब्राउज़र के <code>TextEncoder</code> API से रॉ UTF-8 बाइट्स में बदला जाता है, और वे बाइट्स बिल्ट-इन <code>btoa()</code> फ़ंक्शन को दिए जाते हैं। यह पहला स्टेप मायने रखता है: अकेले <code>btoa()</code> सिर्फ़ Latin-1 कैरेक्टर हैंडल करता है और बाकी सब पर एरर देता है, इसलिए जो टूल इसे स्किप करते हैं वे इमोजी, एक्सेंट, या किसी भी नॉन-लैटिन स्क्रिप्ट पर चुपचाप टूट जाते हैं। डिकोडिंग उल्टे क्रम में वही पाइपलाइन चलाती है: <code>atob()</code> Base64 को वापस बाइट्स में बदलता है, और <code>TextDecoder</code> उन्हें वापस टेक्स्ट में जोड़ता है। डिकोडर जानबूझकर सहनशील भी है: यह व्हाइटस्पेस ट्रिम करता है, स्टैंडर्ड और URL-सेफ़ दोनों अल्फ़ाबेट स्वीकार करता है, और किसी भी हटाई गई <code>=</code> पैडिंग को वापस जोड़ देता है, इसलिए किसी JWT या क्वेरी स्ट्रिंग से सीधे कॉपी किया गया हिस्सा बिना हाथ से ठीक किए डिकोड हो जाता है।',
        how_p2="उम्मीद करें कि आउटपुट इनपुट से लगभग 33% बड़ा होगा। Base64, 64 सिंबल का उपयोग करता है, और 64 सिंबल हर एक में सिर्फ़ 6 बिट्स ही ले जा सकते हैं, इसलिए इनपुट के हर 3 बाइट्स आउटपुट के 4 कैरेक्टर बन जाते हैं। इसी वजह से 1 MB की इमेज को Base64 डेटा URI के रूप में इनलाइन करने पर आपको लगभग 1.37 MB का HTML खर्च होता है, और इसी वजह से Base64 एक ट्रांसपोर्ट फ़ॉर्मैट है, कंप्रेशन फ़ॉर्मैट नहीं।",
        how_p3="दोनों दिशाएं इस पेज के अपने जावास्क्रिप्ट में हर कीस्ट्रोक पर चलती हैं, सिर्फ़ <code>btoa</code>, <code>atob</code>, और आपके ब्राउज़र के पहले से मौजूद टेक्स्ट एन्कोडिंग API का उपयोग करते हुए। आप इसकी पुष्टि कर सकते हैं: डेवलपर टूल्स खोलें, नेटवर्क टैब पर जाएं, और जो चाहें टाइप करें। कोई भी रिक्वेस्ट कभी आपका टेक्स्ट कहीं नहीं ले जाती।",
    ),
    related_tools=[
        ("/hash-generator.html", "हैश जनरेटर", "किसी भी टेक्स्ट के MD5, SHA-1, SHA-256, और SHA-512."),
        ("/uuid-generator.html", "UUID जनरेटर", "बल्क रैंडम UUID v4 आइडेंटिफ़ायर।"),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "ट्री व्यू के साथ JSON फ़ॉर्मैट, वैलिडेट और मिनिफ़ाई करें."),
    ],
)

PAGES["ru"] = dict(
    title="Кодирование / декодирование Base64 онлайн, бесплатно | norito",
    meta_desc="Кодируйте текст в Base64 или декодируйте обратно прямо в браузере. Полная поддержка UTF-8, с опцией URL-безопасного варианта.",
    app_name="Кодирование / декодирование Base64", h1="Кодирование / декодирование Base64", breadcrumb_label="Кодирование / декодирование Base64",
    lede="Преобразуйте текст в Base64 или декодируйте обратно в реальном времени по мере набора. Полная поддержка UTF-8, поэтому буквы с диакритикой, эмодзи и нелатинские алфавиты корректно сохраняются в обоих направлениях.",
    t=dict(
        encode="Кодировать", decode="Декодировать", input="Ввод", placeholder="Введите или вставьте текст для кодирования...",
        url_safe="URL-безопасный вариант", output="Вывод", swap="Поменять местами", copy_output="Скопировать вывод",
        what_h3="Для чего нужен Base64", what_p="Двоично-безопасный текст, не шифрование.",
        what_note='Base64 превращает произвольные байты в строку, использующую только буквы, цифры, <code>+</code> и <code>/</code>, безопасную для встраивания в JSON, URL или email, где необработанные бинарные данные привели бы к ошибкам. Это не шифрование: любой может мгновенно декодировать его обратно, поэтому само по себе оно ничего не скрывает и не защищает.',
        urlsafe_h3="URL-безопасный вариант",
        urlsafe_note='Символы <code>+</code> и <code>/</code> стандартного Base64 имеют особое значение в URL. URL-безопасный вариант заменяет их на <code>-</code> и <code>_</code> и убирает завершающее заполнение <code>=</code>, поэтому результат можно сразу использовать в строке запроса или имени файла.',
        how_h2="Как это работает",
        how_p1='При кодировании ваш текст сначала преобразуется в необработанные байты UTF-8 с помощью API <code>TextEncoder</code> браузера, и эти байты передаются встроенной функции <code>btoa()</code>. Этот первый шаг важен: сама по себе <code>btoa()</code> обрабатывает только символы Latin-1 и выдаёт ошибку на всём остальном, поэтому инструменты, пропускающие этот шаг, незаметно ломаются на эмодзи, диакритических знаках или любом нелатинском алфавите. Декодирование выполняет тот же процесс в обратном порядке: <code>atob()</code> превращает Base64 обратно в байты, а <code>TextDecoder</code> собирает их обратно в текст. Декодер также намеренно снисходителен: он обрезает пробелы, принимает как стандартный, так и URL-безопасный алфавит, и заново добавляет любое удалённое заполнение <code>=</code>, поэтому фрагмент, скопированный прямо из JWT или строки запроса, декодируется без ручных исправлений.',
        how_p2="Ожидайте, что вывод будет примерно на 33% больше ввода. Base64 использует 64 символа, а 64 символа могут нести только по 6 бит каждый, поэтому каждые 3 байта ввода превращаются в 4 символа вывода. Именно поэтому встраивание изображения размером 1 МБ в виде Base64 data URI обходится примерно в 1,37 МБ HTML, и именно поэтому Base64 — это формат передачи, а не формат сжатия.",
        how_p3="Оба направления выполняются в собственном JavaScript этой страницы при каждом нажатии клавиши, используя только <code>btoa</code>, <code>atob</code> и API кодирования текста, уже встроенные в ваш браузер. Вы можете это проверить: откройте инструменты разработчика, переключитесь на вкладку «Сеть» и печатайте что угодно. Ни один запрос никогда не передаёт ваш текст никуда.",
    ),
    related_tools=[
        ("/hash-generator.html", "Генератор хешей", "MD5, SHA-1, SHA-256 и SHA-512 любого текста."),
        ("/uuid-generator.html", "Генератор UUID", "Массовая генерация случайных идентификаторов UUID v4."),
        ("json-formatter.html", "Форматирование JSON", "Форматирует, проверяет и минифицирует JSON с древовидным представлением."),
    ],
)

PAGES["ja"] = dict(
    title="Base64 エンコード／デコード、無料オンラインツール | norito",
    meta_desc="ブラウザ内でテキストをBase64にエンコードしたり、デコードして戻したりできます。UTF-8完全対応、URLセーフ版オプション付き。",
    app_name="Base64 エンコード／デコード", h1="Base64 エンコード／デコード", breadcrumb_label="Base64 エンコード／デコード",
    lede="テキストをBase64に変換したり、入力と同時にリアルタイムでデコードして戻したりできます。UTF-8に完全対応しているため、アクセント付き文字、絵文字、非ラテン文字も両方向で正しく変換されます。",
    t=dict(
        encode="エンコード", decode="デコード", input="入力", placeholder="エンコードするテキストを入力または貼り付け...",
        url_safe="URLセーフ版", output="出力", swap="入れ替え", copy_output="出力をコピー",
        what_h3="Base64の用途", what_p="バイナリセーフなテキストであり、暗号化ではありません。",
        what_note='Base64は任意のバイト列を、文字・数字・<code>+</code>・<code>/</code> のみを使う文字列に変換します。生のバイナリデータでは問題が起きるJSON、URL、メールなどに安全に埋め込めます。これは暗号化ではありません。誰でも即座に元に戻せるため、それ自体では何も隠したり保護したりしません。',
        urlsafe_h3="URLセーフ版",
        urlsafe_note='標準のBase64にある <code>+</code> と <code>/</code> の文字はURLの中で特別な意味を持ちます。URLセーフ版ではこれらを <code>-</code> と <code>_</code> に置き換え、末尾の <code>=</code> パディングを取り除くため、結果をそのままクエリ文字列やファイル名に使用できます。',
        how_h2="仕組み",
        how_p1='エンコード時には、まずブラウザの <code>TextEncoder</code> APIによってテキストが生のUTF-8バイト列に変換され、そのバイト列が組み込みの <code>btoa()</code> 関数に渡されます。この最初のステップが重要です。<code>btoa()</code> 単体ではLatin-1文字しか扱えず、それ以外の文字ではエラーになるため、このステップを省略するツールは絵文字やアクセント文字、非ラテン文字で静かに壊れてしまいます。デコードは同じ処理を逆順に実行します。<code>atob()</code> がBase64をバイト列に戻し、<code>TextDecoder</code> がそれをテキストに再構成します。デコーダーは意図的に寛容に作られており、空白をトリムし、標準版とURLセーフ版の両方の文字セットを受け入れ、削除された <code>=</code> パディングを自動的に補完します。そのためJWTやクエリ文字列からそのままコピーした断片も、手動修正なしにデコードできます。',
        how_p2="出力は入力よりおよそ33%大きくなると考えてください。Base64は64種類の記号を使い、64種類の記号はそれぞれ6ビットしか運べないため、入力の3バイトごとに出力の4文字になります。これが、1MBの画像をBase64データURIとしてインライン化すると約1.37MBのHTMLになる理由であり、Base64が圧縮形式ではなく転送形式である理由です。",
        how_p3="どちらの方向の変換も、このページ自身のJavaScriptの中でキー入力のたびに実行され、使用するのはブラウザに標準搭載されている <code>btoa</code>、<code>atob</code>、およびテキストエンコーディングAPIだけです。実際に確認できます。開発者ツールを開き、ネットワークタブに切り替えて自由に入力してみてください。あなたのテキストをどこかに運ぶリクエストは一切発生しません。",
    ),
    related_tools=[
        ("/hash-generator.html", "ハッシュジェネレーター", "任意のテキストのMD5、SHA-1、SHA-256、SHA-512。"),
        ("/uuid-generator.html", "UUIDジェネレーター", "ランダムなUUID v4識別子を一括生成。"),
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証・圧縮し、ツリー表示できます。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "base64-encoder.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-base64.js"],
        use_foot_scripts_head=False,
        extra_mid_script=TAB_SCRIPT,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/base64-encoder.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
