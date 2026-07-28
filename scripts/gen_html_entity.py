#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>'
ICON_CLASS = "c-teal"

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

        <div class="option-row" style="margin-bottom:16px;">
          <div>
            <div class="option-label">{t['opt_label']}</div>
            <div class="option-hint">{t['opt_hint']}</div>
          </div>
          <label class="switch"><input type="checkbox" id="optAllNonAscii" /><span class="track"></span></label>
        </div>

        <div class="field" style="margin-bottom:16px;">
          <label for="input">{t['input']}</label>
          <textarea id="input" class="mono-area" rows="6" placeholder="{t['ph_input']}"></textarea>
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
            <div class="icon-chip c-teal" style="width:36px;height:36px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
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
    </div>
'''

PAGES = {}

PAGES["es"] = dict(
    title="Codificador / Decodificador de Entidades HTML | norito",
    meta_desc="Escapa o desescapa entidades HTML (&lt; &gt; &amp; y más), en vivo en tu navegador. Maneja entidades con nombre y numéricas. No se sube nada.",
    app_name="Codificador / Decodificador de Entidades HTML", h1="Codificador / Decodificador de Entidades HTML", breadcrumb_label="Codificador de Entidades HTML",
    lede="Escapa caracteres especiales a entidades HTML, o decodifica entidades de vuelta a texto plano, en vivo mientras escribes.",
    t=dict(
        encode="Codificar", decode="Decodificar",
        opt_label="Codificar todos los caracteres no ASCII",
        opt_hint='También escapa letras acentuadas y emoji, no solo &lt; &gt; &amp; " \'.',
        input="Entrada", ph_input="Escribe o pega HTML o texto...", output="Salida",
        swap="Intercambiar", copy_output="Copiar salida",
        side1_h="Por qué existen las entidades HTML", side1_sub="Algunos caracteres están reservados por el propio HTML.",
        side1_body='Caracteres como <code>&lt;</code>, <code>&gt;</code>, y <code>&amp;</code> tienen un significado especial en el marcado HTML; escribirlos literalmente dentro del contenido de una página puede romperla o, peor aún, permitir que la entrada del usuario se interprete como marcado ejecutable. Codificarlos como entidades como <code>&amp;lt;</code> muestra el carácter de forma segura como texto plano.',
        side2_h="Entidades con nombre vs. numéricas",
        side2_body='<code>&amp;amp;</code> y <code>&amp;#38;</code> se decodifican ambas al mismo ampersand; las entidades con nombre existen para caracteres comunes, las entidades numéricas (decimales o hex) pueden representar cualquier carácter Unicode. Esta herramienta decodifica ambas formas.',
        how_h2="Cómo funciona",
        how_p1='La codificación es una sustitución sencilla: una expresión regular reemplaza los cinco caracteres reservados de HTML (<code>&amp;</code>, <code>&lt;</code>, <code>&gt;</code>, <code>"</code>, <code>\'</code>) por sus entidades. La opción "codificar todos los no ASCII" va más allá y convierte cada carácter por encima del rango ASCII en una referencia numérica usando <code>codePointAt</code>, útil cuando la salida debe sobrevivir a un flujo solo-ASCII como un sistema de plantillas de correo antiguo o un archivo de configuración que corrompe UTF-8.',
        how_p2='La decodificación usa un truco que vale la pena conocer: la cadena se asigna al <code>innerHTML</code> de un <code>&lt;textarea&gt;</code> desconectado, y luego se lee de vuelta desde su <code>.value</code>. Eso delega el trabajo al propio parser HTML del navegador, que ya conoce las más de 2000 entidades con nombre además de toda forma numérica decimal y hex, así que la herramienta no incluye una tabla de consulta que pueda quedar obsoleta. También por eso es seguro decodificar entrada no confiable aquí: el contenido de un textarea siempre se trata como texto plano, así que un <code>&amp;lt;script&amp;gt;</code> decodificado se convierte en el texto de una etiqueta script, y nada llega a ejecutarse.',
        how_p3='Ambas direcciones se ejecutan en cada pulsación dentro del JavaScript de esta página. Abre la pestaña Red de las DevTools mientras escribes: no hay peticiones, tu marcado nunca sale del navegador.',
    ),
    related_tools=[
        ("url-encoder-decoder.html", "Codificador / Decodificador de URL", "Codifica o decodifica en porcentaje una URL."),
        ("base64-encoder.html", "Codificar / Decodificar Base64", "Convierte texto a y desde Base64, seguro para UTF-8."),
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica JSON."),
    ],
)

PAGES["zh"] = dict(
    title="HTML 实体编码 / 解码工具在线使用 | norito",
    meta_desc="在浏览器中实时转义或反转义 HTML 实体（&lt; &gt; &amp; 等）。支持命名实体和数字实体。不上传任何内容。",
    app_name="HTML 实体编码 / 解码工具", h1="HTML 实体编码 / 解码工具", breadcrumb_label="HTML 实体编码工具",
    lede="将特殊字符转义为 HTML 实体，或将实体解码回纯文本，输入时实时更新。",
    t=dict(
        encode="编码", decode="解码",
        opt_label="编码所有非 ASCII 字符",
        opt_hint='同时转义带重音的字母和表情符号，而不仅仅是 &lt; &gt; &amp; " \'。',
        input="输入", ph_input="输入或粘贴 HTML 或文本...", output="输出",
        swap="交换", copy_output="复制输出",
        side1_h="为什么会有 HTML 实体", side1_sub="有些字符被 HTML 本身保留。",
        side1_body='像 <code>&lt;</code>、<code>&gt;</code> 和 <code>&amp;</code> 这样的字符在 HTML 标记中具有特殊含义，直接在页面内容中输入它们可能会破坏页面，更糟糕的是，可能让用户输入被解释为可执行的标记。将它们编码为像 <code>&amp;lt;</code> 这样的实体，可以安全地将该字符显示为纯文本。',
        side2_h="命名实体 vs 数字实体",
        side2_body='<code>&amp;amp;</code> 和 <code>&amp;#38;</code> 都会解码为同一个 & 符号；命名实体是为常见字符设置的，数字实体（十进制或十六进制）则可以表示任意 Unicode 字符。此工具可以解码这两种形式。',
        how_h2="工作原理",
        how_p1='编码是一种简单的替换操作：正则表达式将五个 HTML 保留字符（<code>&amp;</code>、<code>&lt;</code>、<code>&gt;</code>、<code>"</code>、<code>\'</code>）替换为对应的实体。「编码所有非 ASCII 字符」选项则更进一步，使用 <code>codePointAt</code> 将 ASCII 范围以外的每个字符都转换为数字引用，这在输出需要通过仅支持 ASCII 的旧邮件模板系统或会破坏 UTF-8 的配置文件时非常有用。',
        how_p2='解码使用了一个值得了解的小技巧：将字符串赋值给一个未挂载的 <code>&lt;textarea&gt;</code> 的 <code>innerHTML</code>，然后再从其 <code>.value</code> 读回结果。这把工作交给了浏览器自身的 HTML 解析器，它已经掌握了 2000 多个命名实体以及所有十进制和十六进制数字形式，因此该工具不需要内置一张可能过时的查找表。这也是为什么在这里解码不受信任的输入是安全的：textarea 的内容始终被当作纯文本处理，因此解码后的 <code>&amp;lt;script&amp;gt;</code> 只会变成一个 script 标签的文本内容，不会被执行。',
        how_p3='两个方向都在这个页面的 JavaScript 中随每次按键实时运行。输入时打开开发者工具的 Network 标签页：不会有任何请求，你的标记内容永远不会离开浏览器。',
    ),
    related_tools=[
        ("url-encoder-decoder.html", "URL 编码 / 解码工具", "对 URL 进行百分号编码或解码。"),
        ("base64-encoder.html", "Base64 编码 / 解码", "文本与 Base64 互转，UTF-8 安全。"),
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩 JSON。"),
    ],
)

PAGES["ar"] = dict(
    title="أداة ترميز / فك ترميز كيانات HTML أونلاين | norito",
    meta_desc="هروب أو إلغاء هروب كيانات HTML (&lt; &gt; &amp; والمزيد)، مباشرة في متصفحك. يتعامل مع الكيانات المسمّاة والرقمية. لا شيء يُرفَع.",
    app_name="ترميز / فك ترميز كيانات HTML", h1="ترميز / فك ترميز كيانات HTML", breadcrumb_label="مرمّز كيانات HTML",
    lede="اهرب الأحرف الخاصة إلى كيانات HTML، أو فُكّ ترميز الكيانات إلى نص عادي، مباشرة أثناء الكتابة.",
    t=dict(
        encode="ترميز", decode="فك الترميز",
        opt_label="ترميز جميع الأحرف غير ASCII",
        opt_hint='يهرب أيضًا الأحرف المشكّلة والرموز التعبيرية، وليس فقط &lt; &gt; &amp; " \'.',
        input="الإدخال", ph_input="اكتب أو الصق HTML أو نصًا...", output="الإخراج",
        swap="تبديل", copy_output="نسخ الإخراج",
        side1_h="لماذا توجد كيانات HTML", side1_sub="بعض الأحرف محجوزة من قِبل HTML نفسه.",
        side1_body='أحرف مثل <code>&lt;</code> و<code>&gt;</code> و<code>&amp;</code> لها معنى خاص في ترميز HTML، كتابتها حرفيًا داخل محتوى الصفحة يمكن أن يكسر الصفحة، أو الأسوأ، يسمح بتفسير إدخال المستخدم كترميز قابل للتنفيذ. ترميزها ككيانات مثل <code>&amp;lt;</code> يعرض الحرف بأمان كنص عادي.',
        side2_h="الكيانات المسمّاة مقابل الرقمية",
        side2_body='كل من <code>&amp;amp;</code> و<code>&amp;#38;</code> يُفكّان إلى نفس علامة العطف؛ الكيانات المسمّاة موجودة للأحرف الشائعة، والكيانات الرقمية (عشرية أو سداسية عشرية) يمكن أن تمثّل أي حرف يونيكود على الإطلاق. تفكّ هذه الأداة كلا الشكلين.',
        how_h2="كيف يعمل",
        how_p1='الترميز هو استبدال مباشر: تستبدل عبارة نمطية الأحرف الخمسة المحجوزة في HTML (<code>&amp;</code> و<code>&lt;</code> و<code>&gt;</code> و<code>"</code> و<code>\'</code>) بكياناتها. يذهب خيار «ترميز جميع الأحرف غير ASCII» إلى أبعد من ذلك ويحوّل كل حرف فوق نطاق ASCII إلى مرجع رقمي باستخدام <code>codePointAt</code>، وهو مفيد عندما يجب أن ينجو الإخراج عبر مسار يتعامل فقط مع ASCII، مثل نظام قوالب بريد إلكتروني قديم أو ملف إعدادات يُفسد UTF-8.',
        how_p2='يستخدم فك الترميز حيلة تستحق المعرفة: تُسنَد السلسلة إلى <code>innerHTML</code> الخاص بعنصر <code>&lt;textarea&gt;</code> منفصل، ثم تُقرأ مجددًا من <code>.value</code> الخاص به. هذا يسلّم المهمة لمحلل HTML الخاص بالمتصفح نفسه، الذي يعرف بالفعل أكثر من 2000 كيان مسمّى بالإضافة إلى كل شكل رقمي عشري وسداسي عشري، لذا لا تحتاج الأداة لشحن جدول بحث قد يصبح قديمًا. وهذا أيضًا سبب أمان فك ترميز إدخال غير موثوق هنا: محتويات عنصر textarea تُعامَل دائمًا كنص عادي، لذا يتحول <code>&amp;lt;script&amp;gt;</code> بعد فك الترميز إلى نص وسم script، ولا يُنفَّذ أي شيء أبدًا.',
        how_p3='يعمل كلا الاتجاهين مع كل ضغطة مفتاح داخل جافاسكريبت هذه الصفحة. افتح لسان Network في أدوات المطوّر أثناء الكتابة: لا توجد طلبات، وترميزك لا يغادر المتصفح أبدًا.',
    ),
    related_tools=[
        ("url-encoder-decoder.html", "ترميز / فك ترميز URL", "رمّز بالنسبة المئوية أو فكّ ترميز رابط."),
        ("base64-encoder.html", "ترميز / فك ترميز Base64", "حوّل النص من وإلى Base64، آمن مع UTF-8."),
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق وضغط JSON."),
    ],
)

PAGES["hi"] = dict(
    title="HTML एंटिटी एनकोडर / डिकोडर ऑनलाइन | norito",
    meta_desc="अपने ब्राउज़र में लाइव HTML एंटिटीज़ (&lt; &gt; &amp; और अन्य) को एस्केप या अनएस्केप करें। नेम्ड और न्यूमेरिक दोनों एंटिटीज़ हैंडल करता है। कुछ भी अपलोड नहीं होता।",
    app_name="HTML एंटिटी एनकोडर / डिकोडर", h1="HTML एंटिटी एनकोडर / डिकोडर", breadcrumb_label="HTML एंटिटी एनकोडर",
    lede="स्पेशल कैरेक्टर्स को HTML एंटिटीज़ में एस्केप करें, या एंटिटीज़ को वापस प्लेन टेक्स्ट में डिकोड करें, टाइप करते ही लाइव।",
    t=dict(
        encode="एनकोड करें", decode="डिकोड करें",
        opt_label="सभी नॉन-ASCII कैरेक्टर एनकोड करें",
        opt_hint='सिर्फ़ &lt; &gt; &amp; " \' ही नहीं, एक्सेंटेड लेटर और इमोजी को भी एस्केप करता है।',
        input="इनपुट", ph_input="HTML या टेक्स्ट टाइप या पेस्ट करें...", output="आउटपुट",
        swap="स्वैप करें", copy_output="आउटपुट कॉपी करें",
        side1_h="HTML एंटिटीज़ क्यों मौजूद हैं", side1_sub="कुछ कैरेक्टर्स ख़ुद HTML द्वारा रिज़र्व्ड हैं।",
        side1_body='<code>&lt;</code>, <code>&gt;</code>, और <code>&amp;</code> जैसे कैरेक्टर्स का HTML मार्कअप में ख़ास मतलब होता है, पेज कंटेंट के अंदर इन्हें लिटरली टाइप करने से पेज टूट सकता है, या इससे भी बुरा, यूज़र इनपुट को एक्ज़ीक्यूटेबल मार्कअप के रूप में इंटरप्रेट किया जा सकता है। इन्हें <code>&amp;lt;</code> जैसी एंटिटीज़ के रूप में एनकोड करने से कैरेक्टर सेफ़ली प्लेन टेक्स्ट के रूप में दिखता है।',
        side2_h="नेम्ड बनाम न्यूमेरिक एंटिटीज़",
        side2_body='<code>&amp;amp;</code> और <code>&amp;#38;</code> दोनों एक ही एम्परसैंड में डिकोड होते हैं, नेम्ड एंटिटीज़ आम कैरेक्टर्स के लिए होती हैं, न्यूमेरिक एंटिटीज़ (डेसिमल या हेक्स) किसी भी यूनिकोड कैरेक्टर को रिप्रज़ेंट कर सकती हैं। यह टूल दोनों फ़ॉर्म को डिकोड करता है।',
        how_h2="यह कैसे काम करता है",
        how_p1='एनकोडिंग एक सीधा सा सब्स्टिट्यूशन है: एक रेगेक्स पांच HTML-रिज़र्व्ड कैरेक्टर्स (<code>&amp;</code>, <code>&lt;</code>, <code>&gt;</code>, <code>"</code>, <code>\'</code>) को उनकी एंटिटीज़ से बदल देता है। "सभी नॉन-ASCII कैरेक्टर एनकोड करें" ऑप्शन आगे जाकर <code>codePointAt</code> का इस्तेमाल करते हुए ASCII रेंज से ऊपर के हर कैरेक्टर को एक न्यूमेरिक रेफ़रेंस में बदल देता है, यह तब काम आता है जब आउटपुट को किसी पुराने ईमेल टेम्पलेट सिस्टम या UTF-8 को ख़राब कर देने वाली कॉन्फ़िग फ़ाइल जैसे ASCII-ओनली पाइपलाइन से गुज़रना हो।',
        how_p2='डिकोडिंग एक ऐसी ट्रिक इस्तेमाल करती है जो जानने लायक है: स्ट्रिंग को एक डिटैच्ड <code>&lt;textarea&gt;</code> के <code>innerHTML</code> में असाइन किया जाता है, फिर उसके <code>.value</code> से वापस पढ़ा जाता है। इससे काम ब्राउज़र के अपने HTML पार्सर को सौंप दिया जाता है, जो पहले से ही 2,000 से ज़्यादा नेम्ड एंटिटीज़ के साथ-साथ हर डेसिमल और हेक्स न्यूमेरिक फ़ॉर्म को जानता है, इसलिए टूल कोई लुकअप टेबल शिप नहीं करता जो पुरानी पड़ सकती है। यही वजह है कि यहां अनट्रस्टेड इनपुट को डिकोड करना सेफ़ है: टेक्स्टएरिया का कंटेंट हमेशा प्लेन टेक्स्ट के रूप में ट्रीट होता है, इसलिए डिकोड किया गया <code>&amp;lt;script&amp;gt;</code> एक स्क्रिप्ट टैग के टेक्स्ट में बदल जाता है, और कुछ भी एक्ज़ीक्यूट नहीं होता।',
        how_p3='दोनों दिशाएं इस पेज के JavaScript के अंदर हर कीस्ट्रोक पर चलती हैं। टाइप करते समय डेवटूल्स का Network टैब खोलें: कोई रिक्वेस्ट नहीं होती, आपका मार्कअप कभी ब्राउज़र से बाहर नहीं जाता।',
    ),
    related_tools=[
        ("url-encoder-decoder.html", "URL एनकोडर / डिकोडर", "किसी URL को पर्सेंट-एनकोड या डिकोड करें।"),
        ("base64-encoder.html", "Base64 एनकोड / डिकोड", "टेक्स्ट को Base64 में और वापस बदलें, UTF-8 सेफ़।"),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "JSON फ़ॉर्मैट, वैलिडेट और मिनिफ़ाई करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Кодировщик / декодировщик HTML-сущностей онлайн | norito",
    meta_desc="Экранируйте или раскодируйте HTML-сущности (&lt; &gt; &amp; и другие) прямо в браузере. Поддерживает именованные и числовые сущности. Ничего не загружается.",
    app_name="Кодировщик / декодировщик HTML-сущностей", h1="Кодировщик / декодировщик HTML-сущностей", breadcrumb_label="Кодировщик HTML-сущностей",
    lede="Экранируйте специальные символы в HTML-сущности или раскодируйте сущности обратно в обычный текст прямо во время ввода.",
    t=dict(
        encode="Кодировать", decode="Декодировать",
        opt_label="Кодировать все не-ASCII символы",
        opt_hint='Также экранирует буквы с диакритикой и эмодзи, а не только &lt; &gt; &amp; " \'.',
        input="Ввод", ph_input="Введите или вставьте HTML или текст...", output="Вывод",
        swap="Поменять местами", copy_output="Скопировать вывод",
        side1_h="Зачем нужны HTML-сущности", side1_sub="Некоторые символы зарезервированы самим HTML.",
        side1_body='Символы вроде <code>&lt;</code>, <code>&gt;</code> и <code>&amp;</code> имеют особое значение в HTML-разметке; ввод их напрямую в содержимом страницы может сломать страницу или, что хуже, позволить интерпретировать пользовательский ввод как исполняемую разметку. Кодирование их в сущности вроде <code>&amp;lt;</code> безопасно отображает символ как обычный текст.',
        side2_h="Именованные vs числовые сущности",
        side2_body='<code>&amp;amp;</code> и <code>&amp;#38;</code> оба декодируются в один и тот же амперсанд; именованные сущности существуют для распространённых символов, а числовые сущности (десятичные или шестнадцатеричные) могут представлять любой символ Юникода. Этот инструмент декодирует обе формы.',
        how_h2="Как это работает",
        how_p1='Кодирование — это простая замена: регулярное выражение заменяет пять зарезервированных в HTML символов (<code>&amp;</code>, <code>&lt;</code>, <code>&gt;</code>, <code>"</code>, <code>\'</code>) на их сущности. Опция «кодировать все не-ASCII символы» идёт дальше и преобразует каждый символ за пределами диапазона ASCII в числовую ссылку с помощью <code>codePointAt</code>, что полезно, когда вывод должен пройти через ASCII-only канал, например старую систему email-шаблонов или конфигурационный файл, портящий UTF-8.',
        how_p2='Декодирование использует приём, который стоит знать: строка присваивается свойству <code>innerHTML</code> отсоединённого элемента <code>&lt;textarea&gt;</code>, а затем считывается обратно из его <code>.value</code>. Это перекладывает работу на собственный HTML-парсер браузера, который уже знает более 2000 именованных сущностей, а также все десятичные и шестнадцатеричные числовые формы, поэтому инструменту не нужна таблица соответствий, которая может устареть. Именно поэтому здесь безопасно декодировать недоверенный ввод: содержимое textarea всегда обрабатывается как обычный текст, поэтому декодированный <code>&amp;lt;script&amp;gt;</code> становится текстом внутри тега script, и ничего никогда не выполняется.',
        how_p3='Оба направления выполняются при каждом нажатии клавиши в JavaScript этой страницы. Откройте вкладку Network в DevTools во время ввода: запросов нет, ваша разметка никогда не покидает браузер.',
    ),
    related_tools=[
        ("url-encoder-decoder.html", "Кодировщик / декодировщик URL", "Кодируйте в процентном формате или декодируйте URL."),
        ("base64-encoder.html", "Кодировщик / декодировщик Base64", "Преобразование текста в Base64 и обратно, безопасно для UTF-8."),
        ("json-formatter.html", "Форматирование JSON", "Форматирует, проверяет и минифицирует JSON."),
    ],
)

PAGES["ja"] = dict(
    title="HTMLエンティティエンコーダー/デコーダー | norito",
    meta_desc="HTMLエンティティ（&lt; &gt; &amp; など）をブラウザ内でリアルタイムにエスケープ・アンエスケープ。名前付きエンティティと数値エンティティに対応。アップロードなし。",
    app_name="HTMLエンティティエンコーダー/デコーダー", h1="HTMLエンティティエンコーダー/デコーダー", breadcrumb_label="HTMLエンティティエンコーダー",
    lede="特殊文字をHTMLエンティティにエスケープ、またはエンティティをプレーンテキストにデコードします。入力するとリアルタイムに反映されます。",
    t=dict(
        encode="エンコード", decode="デコード",
        opt_label="すべての非ASCII文字をエンコード",
        opt_hint='&lt; &gt; &amp; " \' だけでなく、アクセント付き文字や絵文字もエスケープします。',
        input="入力", ph_input="HTMLまたはテキストを入力または貼り付け...", output="出力",
        swap="入れ替え", copy_output="出力をコピー",
        side1_h="HTMLエンティティが存在する理由", side1_sub="一部の文字はHTML自体によって予約されています。",
        side1_body='<code>&lt;</code>、<code>&gt;</code>、<code>&amp;</code>のような文字はHTMLマークアップにおいて特別な意味を持ちます。ページコンテンツ内にそのまま入力するとページが壊れたり、さらに悪い場合はユーザー入力が実行可能なマークアップとして解釈されてしまうことがあります。<code>&amp;lt;</code>のようなエンティティとしてエンコードすることで、その文字を安全にプレーンテキストとして表示できます。',
        side2_h="名前付きエンティティ vs 数値エンティティ",
        side2_body='<code>&amp;amp;</code>と<code>&amp;#38;</code>はどちらも同じアンパサンドにデコードされます。名前付きエンティティは一般的な文字向けに存在し、数値エンティティ（10進または16進）はあらゆるUnicode文字を表現できます。このツールは両方の形式をデコードします。',
        how_h2="仕組み",
        how_p1='エンコードは単純な置換処理です。正規表現がHTMLで予約された5つの文字（<code>&amp;</code>、<code>&lt;</code>、<code>&gt;</code>、<code>"</code>、<code>\'</code>）をそれぞれのエンティティに置き換えます。「すべての非ASCII文字をエンコード」オプションはさらに進んで、<code>codePointAt</code>を使ってASCII範囲を超えるすべての文字を数値参照に変換します。これは、古いメールテンプレートシステムやUTF-8を壊してしまう設定ファイルのようなASCII専用の処理経路を出力が通過する必要がある場合に便利です。',
        how_p2='デコードには知っておく価値のあるテクニックが使われています。文字列を切り離された<code>&lt;textarea&gt;</code>要素の<code>innerHTML</code>に代入し、その<code>.value</code>から読み戻すという方法です。これによりブラウザ自身のHTMLパーサーに処理を委ねることができ、パーサーはすでに2000以上の名前付きエンティティに加え、あらゆる10進・16進の数値形式を把握しているため、このツールは古くなる可能性のあるルックアップテーブルを持つ必要がありません。これはまた、信頼できない入力をここでデコードしても安全な理由でもあります。textareaの内容は常にプレーンテキストとして扱われるため、デコードされた<code>&amp;lt;script&amp;gt;</code>はscriptタグのテキストになるだけで、何も実行されません。',
        how_p3='どちらの方向も、このページのJavaScript内でキー入力のたびに実行されます。入力中にDevToolsのNetworkタブを開いてみてください。リクエストは一切発生せず、あなたのマークアップがブラウザの外に出ることはありません。',
    ),
    related_tools=[
        ("url-encoder-decoder.html", "URLエンコード/デコードツール", "URLをパーセントエンコードまたはデコード。"),
        ("base64-encoder.html", "Base64 エンコード / デコード", "テキストを Base64 との間で変換、UTF-8 セーフ。"),
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証・圧縮。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "html-entity-encoder.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-html-entity.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/html-entity-encoder.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
