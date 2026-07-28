#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m18 14 4 4-4 4"/><path d="m18 2 4 4-4 4"/><path d="M2 18h1.973a4 4 0 0 0 3.3-1.7l5.454-8.6a4 4 0 0 1 3.3-1.7H22"/><path d="M2 6h1.972a4 4 0 0 1 3.6 2.2"/><path d="M22 18h-6.041a4 4 0 0 1-3.3-1.8l-.36-.54"/></svg>'
ICON_CLASS = "c-indigo"
GEN_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 12a9 9 0 1 1-2.64-6.36"/><path d="M21 3v6h-6"/></svg>'

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field-row">
          <div class="field">
            <label for="count">{t['count']}</label>
            <input type="number" id="count" min="1" max="100" value="5" style="width:100px;" />
          </div>
          <button id="genBtn" style="align-self:flex-end;">
            {GEN_ICON}
            {t['generate']}
          </button>
          <button id="copyAllBtn" class="secondary" style="align-self:flex-end;">{t['copy_all']}</button>
        </div>

        <div class="option-row">
          <span class="option-label">{t['uppercase']}</span>
          <label class="switch"><input type="checkbox" id="optUppercase" /><span class="track"></span></label>
        </div>
        <div class="option-row">
          <span class="option-label">{t['remove_hyphens']}</span>
          <label class="switch"><input type="checkbox" id="optNoHyphens" /><span class="track"></span></label>
        </div>

        <div id="uuidList" style="margin-top:20px;"></div>
      </div>

      <div>
        <div class="panel">
          <div class="panel-header">
            <div class="icon-chip c-indigo" style="width:36px;height:36px;">
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
          <h3 style="margin-top:0;">{t['uses_h3']}</h3>
          <p class="note" style="margin-top:0;">
            {t['uses_note']}
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
    title="Generador de UUID: generador masivo de UUID v4 | norito",
    meta_desc="Genera identificadores UUID v4 aleatorios en lote, directamente en tu navegador. Opciones de mayúsculas y sin guiones, copia uno o todos. No se envía nada a ningún sitio.",
    app_name="Generador de UUID", h1="Generador de UUID", breadcrumb_label="Generador de UUID",
    lede="Genera identificadores UUID v4 aleatorios usando el generador de números aleatorios criptográfico de tu navegador. Crea uno o cien a la vez, no se envía nada a ningún sitio.",
    t=dict(
        count="Cantidad", generate="Generar", copy_all="Copiar todos",
        uppercase="Mayúsculas", remove_hyphens="Quitar guiones",
        what_h3="¿Qué es un UUID v4?", what_p="128 bits de aleatoriedad, formateados como un identificador estándar.",
        what_note="Un UUID v4 son 122 bits aleatorios (los otros 6 están fijos para marcar la versión y la variante), lo que da aproximadamente 5,3 undecillones de valores posibles. Las colisiones son tan improbables que no son una preocupación práctica para claves primarias de bases de datos, IDs de peticiones o nombres de archivo.",
        uses_h3="Usos comunes",
        uses_note="Claves primarias de bases de datos que no revelan el número de filas, claves de idempotencia para peticiones de API, IDs de correlación para rastrear registros entre servicios, y nombres únicos de archivos o sesiones que no colisionarán aunque se generen en máquinas distintas al mismo tiempo.",
        how_h2="Cómo funciona",
        how_p1='Cada ID proviene de <code>crypto.randomUUID()</code>, el generador integrado del navegador. Por debajo, extrae 128 bits de la fuente aleatoria criptográficamente segura del sistema operativo (la misma que genera las claves TLS), y luego fija 6 de esos bits con valores concretos: el nibble de versión se convierte en 4 y los bits de variante en 10. Por eso todo UUID aquí tiene un 4 al inicio del tercer grupo y un 8, 9, a o b al inicio del cuarto. Los 122 bits restantes son puramente aleatorios, lo que hace que las colisiones no sean un problema en la práctica.',
        how_p2="¿Cuán poco problema? Hay 2^122 UUID v4 posibles, unos 5,3 undecillones. Las matemáticas del problema del cumpleaños dicen que necesitarías generar aproximadamente 103 billones de UUID antes de que la probabilidad de una sola colisión llegue a uno entre un millón. Cada ID que tus sistemas lleguen a generar es un error de redondeo frente a esa cifra, por lo que los UUID v4 son seguros de generar en cualquier máquina sin coordinación.",
        how_p3="La generación es una única llamada a la API del navegador, así que no se solicita nada a un servidor ni se envía nada a uno: abre la pestaña Red de las herramientas de desarrollador, haz clic en Generar, y observa que no pasa nada. Los interruptores de mayúsculas y sin guiones solo reformatean los IDs ya generados; los valores subyacentes no cambian.",
        how_p4="Una nota práctica: los UUID v4 son deliberadamente desordenados, así que como claves primarias de bases de datos dispersan las inserciones por todo el índice. Si necesitas IDs que se ordenen por tiempo de creación, mira el UUID v7, que coloca una marca de tiempo en los bits altos. Para todo lo demás (IDs de peticiones, nombres de archivo, tokens de correlación), el v4 aleatorio es exactamente lo adecuado.",
    ),
    related_tools=[
        ("hash-generator.html", "Generador de hashes", "MD5, SHA-1, SHA-256 y SHA-512 de cualquier texto."),
        ("base64-encoder.html", "Codificar / Decodificar Base64", "Convierte texto a y desde Base64, seguro para UTF-8."),
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica JSON con una vista de árbol."),
    ],
)

PAGES["zh"] = dict(
    title="UUID 生成器：批量生成 UUID v4 | norito",
    meta_desc="直接在浏览器中批量生成随机 UUID v4 标识符。支持大写和去连字符选项，可复制单个或全部。不会向任何地方发送任何内容。",
    app_name="UUID 生成器", h1="UUID 生成器", breadcrumb_label="UUID 生成器",
    lede="使用浏览器内置的加密随机数生成器生成随机 UUID v4 标识符。一次生成一个或上百个，不会向任何地方发送任何内容。",
    t=dict(
        count="数量", generate="生成", copy_all="复制全部",
        uppercase="大写", remove_hyphens="去除连字符",
        what_h3="什么是 UUID v4？", what_p="128 位随机数，格式化为标准标识符。",
        what_note="UUID v4 由 122 个随机比特组成（另外 6 位固定用于标记版本和变体），能产生约 5.3 万亿的万亿的万亿种可能值。冲突的概率极低，对于数据库主键、请求 ID 或文件名来说，实际上不构成问题。",
        uses_h3="常见用途",
        uses_note="不泄露行数的数据库主键、API 请求的幂等键、用于跨服务追踪日志的关联 ID，以及即使在不同机器上同时生成也不会冲突的唯一文件名或会话名。",
        how_h2="工作原理",
        how_p1='每个 ID 都来自浏览器内置的生成器 <code>crypto.randomUUID()</code>。其底层从操作系统的加密安全随机源（与生成 TLS 密钥的来源相同）中提取 128 位，然后将其中 6 位固定为特定值：版本半字节被设为 4，变体位被设为 10。这就是为什么这里的每个 UUID 第三组开头都是 4，第四组开头都是 8、9、a 或 b。剩下的 122 位是纯随机的，这正是冲突在实践中几乎不成问题的原因。',
        how_p2="到底有多不成问题？一共有 2^122 种可能的 v4 UUID，约 5.3 万亿的万亿的万亿种。根据生日问题的数学原理，大约需要生成 103 万亿个 UUID，出现哪怕一次冲突的概率才会达到百万分之一。你的系统所生成的每一个 ID，相对这个数字而言都只是舍入误差，这也是为什么 v4 UUID 可以在任何机器上无需协调地安全生成。",
        how_p3="生成过程只是一次浏览器 API 调用，因此不会向服务器请求任何内容，也不会发送任何内容：打开开发者工具的网络面板，点击「生成」，你会看到什么都没发生。大写和去连字符开关只是对已生成的 ID 重新格式化；底层的值并不会改变。",
        how_p4="一个实用提示：v4 UUID 是刻意无序的，因此作为数据库主键时会使插入操作分散到索引各处。如果你需要按创建时间排序的 ID，可以了解一下 UUID v7，它把时间戳放在高位比特中。至于其他场景（请求 ID、文件名、关联令牌），随机的 v4 正合适。",
    ),
    related_tools=[
        ("hash-generator.html", "哈希生成器", "任意文本的 MD5、SHA-1、SHA-256 和 SHA-512。"),
        ("base64-encoder.html", "Base64 编码 / 解码", "文本与 Base64 互转，UTF-8 安全。"),
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩 JSON，附带树状视图。"),
    ],
)

PAGES["ar"] = dict(
    title="مولّد UUID: مولّد UUID v4 بالجملة | norito",
    meta_desc="أنشئ معرّفات UUID v4 عشوائية بالجملة، مباشرةً في متصفحك. خيارات الأحرف الكبيرة وإزالة الشرطات، انسخ واحدًا أو الكل. لا يُرسل أي شيء إلى أي مكان.",
    app_name="مولّد UUID", h1="مولّد UUID", breadcrumb_label="مولّد UUID",
    lede="أنشئ معرّفات UUID v4 عشوائية باستخدام مولّد الأرقام العشوائية التشفيري في متصفحك. أنشئ واحدًا أو مئة دفعة واحدة، لا يُرسل أي شيء إلى أي مكان.",
    t=dict(
        count="العدد", generate="إنشاء", copy_all="نسخ الكل",
        uppercase="أحرف كبيرة", remove_hyphens="إزالة الشرطات",
        what_h3="ما هو UUID v4؟", what_p="128 بت من العشوائية، منسّقة كمعرّف قياسي.",
        what_note="يتكوّن UUID v4 من 122 بت عشوائيًا (البتات الست الأخرى ثابتة لتمييز الإصدار والمتغيّر)، ما يعطي حوالي 5.3 أنديسيليون قيمة ممكنة. التصادمات نادرة الحدوث لدرجة أنها ليست مصدر قلق عملي لمفاتيح قواعد البيانات الأساسية، أو معرّفات الطلبات، أو أسماء الملفات.",
        uses_h3="الاستخدامات الشائعة",
        uses_note="مفاتيح قواعد بيانات أساسية لا تكشف عدد الصفوف، ومفاتيح idempotency لطلبات API، ومعرّفات ربط لتتبّع السجلات عبر الخدمات، وأسماء ملفات أو جلسات فريدة لن تتصادم حتى لو أُنشئت على أجهزة مختلفة في الوقت نفسه.",
        how_h2="كيف يعمل",
        how_p1='يأتي كل معرّف من <code>crypto.randomUUID()</code>، المولّد المدمج في المتصفح. تحت الغطاء، يسحب 128 بت من مصدر التشفير الآمن العشوائي لنظام التشغيل (نفس المصدر الذي يولّد مفاتيح TLS)، ثم يثبّت 6 من هذه البتات بقيم محددة: تصبح خانة الإصدار 4 وتصبح بتات المتغيّر 10. لهذا السبب يبدأ كل UUID هنا بالرقم 4 في بداية المجموعة الثالثة وبالرقم 8 أو 9 أو a أو b في بداية المجموعة الرابعة. أما البتات الـ122 المتبقية فهي عشوائية بحتة، وهذا ما يجعل التصادمات غير ذات أهمية عمليًا.',
        how_p2="إلى أي مدى غير ذات أهمية؟ يوجد 2^122 معرّف UUID v4 ممكن، أي حوالي 5.3 أنديسيليون. تقول رياضيات «مسألة أعياد الميلاد» إنك ستحتاج إلى إنشاء نحو 103 تريليون UUID قبل أن تصل احتمالية حدوث تصادم واحد فقط إلى واحد من كل مليون. كل معرّف قد تنشئه أنظمتك على الإطلاق هو خطأ تقريب لا يُذكر أمام هذا الرقم، ولهذا يُعدّ إنشاء UUID v4 آمنًا على أي جهاز دون أي تنسيق.",
        how_p3="الإنشاء هو مجرد استدعاء واحد لواجهة برمجة المتصفح، لذا لا يُطلب أي شيء من خادم ولا يُرسل أي شيء إليه: افتح تبويب الشبكة في أدوات المطوّر، انقر على «إنشاء»، وشاهد أنه لا يحدث شيء. تُعيد مفاتيح الأحرف الكبيرة وإزالة الشرطات تنسيق المعرّفات المُنشأة بالفعل فقط؛ القيم الأساسية لا تتغيّر.",
        how_p4="ملاحظة عملية: معرّفات UUID v4 غير مرتّبة عمدًا، لذا فهي كمفاتيح أساسية لقاعدة بيانات تُوزّع عمليات الإدراج عبر الفهرس. إذا كنت بحاجة إلى معرّفات تُرتَّب حسب وقت الإنشاء، فانظر إلى UUID v7 الذي يضع طابعًا زمنيًا في البتات العليا. أما في كل الحالات الأخرى (معرّفات الطلبات، أسماء الملفات، رموز الربط)، فإن UUID v4 العشوائي هو الخيار الصحيح تمامًا.",
    ),
    related_tools=[
        ("hash-generator.html", "مولّد التجزئة", "MD5 وSHA-1 وSHA-256 وSHA-512 لأي نص."),
        ("base64-encoder.html", "ترميز / فك ترميز Base64", "حوّل النص من وإلى Base64، آمن مع UTF-8."),
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق وضغط JSON مع عرض شجري."),
    ],
)

PAGES["hi"] = dict(
    title="UUID जनरेटर: बल्क UUID v4 जनरेटर | norito",
    meta_desc="अपने ब्राउज़र में ही रैंडम UUID v4 आइडेंटिफ़ायर बल्क में जनरेट करें। अपरकेस और बिना-हाइफ़न विकल्प, एक या सभी कॉपी करें। कहीं कुछ नहीं भेजा जाता।",
    app_name="UUID जनरेटर", h1="UUID जनरेटर", breadcrumb_label="UUID जनरेटर",
    lede="अपने ब्राउज़र के क्रिप्टोग्राफ़िक रैंडम नंबर जनरेटर से रैंडम UUID v4 आइडेंटिफ़ायर जनरेट करें। एक बार में एक या सौ बनाएं, कहीं कुछ नहीं भेजा जाता।",
    t=dict(
        count="काउंट", generate="जनरेट करें", copy_all="सभी कॉपी करें",
        uppercase="अपरकेस", remove_hyphens="हाइफ़न हटाएं",
        what_h3="UUID v4 क्या है?", what_p="128 बिट रैंडमनेस, एक स्टैंडर्ड आइडेंटिफ़ायर के रूप में फ़ॉर्मैट की गई।",
        what_note="एक UUID v4 122 रैंडम बिट्स होते हैं (बाकी 6 वर्शन और वेरिएंट दिखाने के लिए फ़िक्स्ड होते हैं), जो लगभग 5.3 अनडेसिलियन संभावित वैल्यू देते हैं। कोलिज़न इतने असंभव हैं कि डेटाबेस प्राइमरी की, रिक्वेस्ट आईडी, या फ़ाइल नामों के लिए ये कोई व्यावहारिक चिंता नहीं हैं।",
        uses_h3="सामान्य उपयोग",
        uses_note="डेटाबेस प्राइमरी की जो रो काउंट लीक नहीं करतीं, API रिक्वेस्ट के लिए आइडेंपोटेंसी कीज़, सेवाओं के बीच लॉग ट्रेस करने के लिए कोरिलेशन आईडी, और यूनीक फ़ाइल या सेशन नाम जो अलग-अलग मशीनों पर एक ही समय में जनरेट होने पर भी नहीं टकराएंगे।",
        how_h2="यह कैसे काम करता है",
        how_p1='हर ID ब्राउज़र के बिल्ट-इन जनरेटर <code>crypto.randomUUID()</code> से आती है। इसके अंदर, यह ऑपरेटिंग सिस्टम के क्रिप्टोग्राफ़िकली सिक्योर रैंडम सोर्स (वही जो TLS कीज़ जनरेट करता है) से 128 बिट्स लेता है, फिर उनमें से 6 बिट्स को फ़िक्स्ड वैल्यू से स्टैंप करता है: वर्शन निबल 4 बन जाता है और वेरिएंट बिट्स 10 बन जाते हैं। इसी वजह से यहाँ हर UUID के तीसरे ग्रुप की शुरुआत में 4 होता है और चौथे ग्रुप की शुरुआत में 8, 9, a, या b होता है। बाकी बचे 122 बिट्स शुद्ध रैंडमनेस हैं, जिसकी वजह से प्रैक्टिस में कोलिज़न कोई मुद्दा नहीं रह जाता।',
        how_p2="कितना गैर-मुद्दा? 2^122 संभावित v4 UUID हैं, लगभग 5.3 अनडेसिलियन। बर्थडे-प्रॉब्लम का गणित कहता है कि आपको एक कोलिज़न की संभावना दस लाख में एक तक पहुँचने से पहले लगभग 103 ट्रिलियन UUID जनरेट करने होंगे। आपके सिस्टम कभी भी जितनी भी ID बनाएंगे, वह इस संख्या के सामने बस एक राउंडिंग एरर है, इसी वजह से v4 UUID किसी भी मशीन पर बिना किसी कोऑर्डिनेशन के जनरेट करना सुरक्षित है।",
        how_p3="जनरेशन बस एक ब्राउज़र API कॉल है, इसलिए न तो सर्वर से कुछ रिक्वेस्ट किया जाता है और न ही उसे कुछ भेजा जाता है: डेवलपर टूल्स का नेटवर्क टैब खोलें, Generate पर क्लिक करें, और देखें कि कुछ नहीं होता। अपरकेस और बिना-हाइफ़न टॉगल केवल पहले से जनरेट हुई ID को दोबारा फ़ॉर्मैट करते हैं; अंदरूनी वैल्यू नहीं बदलतीं।",
        how_p4="एक व्यावहारिक बात: v4 UUID जानबूझकर अनऑर्डर्ड होते हैं, इसलिए डेटाबेस प्राइमरी की के रूप में ये इंसर्ट को पूरे इंडेक्स में बिखेर देते हैं। अगर आपको क्रिएशन टाइम के हिसाब से सॉर्ट होने वाली ID चाहिए, तो UUID v7 देखें, जो ऊँचे बिट्स में एक टाइमस्टैम्प डालता है। बाकी हर चीज़ के लिए (रिक्वेस्ट ID, फ़ाइल नाम, कोरिलेशन टोकन), रैंडम v4 बिल्कुल सही है।",
    ),
    related_tools=[
        ("hash-generator.html", "हैश जनरेटर", "किसी भी टेक्स्ट के MD5, SHA-1, SHA-256, और SHA-512."),
        ("base64-encoder.html", "Base64 एनकोड / डिकोड", "टेक्स्ट को Base64 में और वापस बदलें, UTF-8 सेफ़।"),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "ट्री व्यू के साथ JSON फ़ॉर्मैट, वैलिडेट और मिनिफ़ाई करें."),
    ],
)

PAGES["ru"] = dict(
    title="Генератор UUID: массовый генератор UUID v4 | norito",
    meta_desc="Создавайте случайные идентификаторы UUID v4 массово прямо в браузере. Опции верхнего регистра и без дефисов, копирование одного или всех. Ничего никуда не отправляется.",
    app_name="Генератор UUID", h1="Генератор UUID", breadcrumb_label="Генератор UUID",
    lede="Создавайте случайные идентификаторы UUID v4 с помощью криптографического генератора случайных чисел вашего браузера. Создайте один или сто сразу, ничего никуда не отправляется.",
    t=dict(
        count="Количество", generate="Сгенерировать", copy_all="Копировать все",
        uppercase="Верхний регистр", remove_hyphens="Убрать дефисы",
        what_h3="Что такое UUID v4?", what_p="128 бит случайности, отформатированные как стандартный идентификатор.",
        what_note="UUID v4 — это 122 случайных бита (остальные 6 фиксированы для обозначения версии и варианта), что даёт примерно 5,3 андециллиона возможных значений. Коллизии настолько маловероятны, что не представляют практической проблемы для первичных ключей баз данных, идентификаторов запросов или имён файлов.",
        uses_h3="Распространённые случаи использования",
        uses_note="Первичные ключи баз данных, не раскрывающие количество строк, ключи идемпотентности для API-запросов, идентификаторы корреляции для трассировки логов между сервисами, а также уникальные имена файлов или сессий, которые не столкнутся, даже если сгенерированы одновременно на разных машинах.",
        how_h2="Как это работает",
        how_p1='Каждый ID создаётся функцией <code>crypto.randomUUID()</code> — встроенным генератором браузера. Внутри он берёт 128 бит из криптографически безопасного источника случайности операционной системы (того же, что генерирует ключи TLS), а затем фиксирует 6 из этих бит определёнными значениями: полубайт версии становится 4, а биты варианта — 10. Именно поэтому у каждого UUID здесь третья группа начинается с 4, а четвёртая — с 8, 9, a или b. Остальные 122 бита — чистая случайность, из-за чего коллизии на практике не представляют проблемы.',
        how_p2="Насколько не проблема? Существует 2^122 возможных UUID v4 — около 5,3 андециллиона. Математика «задачи о днях рождения» показывает, что потребуется сгенерировать примерно 103 триллиона UUID, прежде чем вероятность хотя бы одной коллизии достигнет одного к миллиону. Любое количество ID, которое когда-либо создадут ваши системы, — это статистическая погрешность на фоне этого числа, поэтому UUID v4 безопасно генерировать на любой машине без какой-либо координации.",
        how_p3="Генерация — это единственный вызов API браузера, поэтому от сервера ничего не запрашивается и на него ничего не отправляется: откройте вкладку «Сеть» в инструментах разработчика, нажмите «Сгенерировать» и убедитесь, что ничего не происходит. Переключатели верхнего регистра и без дефисов лишь переформатируют уже сгенерированные ID; сами значения не меняются.",
        how_p4="Практическое замечание: UUID v4 намеренно неупорядочены, поэтому в качестве первичных ключей базы данных они разбрасывают вставки по всему индексу. Если вам нужны ID, сортируемые по времени создания, обратите внимание на UUID v7, который помещает временную метку в старшие биты. Для всего остального (ID запросов, имена файлов, токены корреляции) случайный v4 подходит идеально.",
    ),
    related_tools=[
        ("hash-generator.html", "Генератор хешей", "MD5, SHA-1, SHA-256 и SHA-512 любого текста."),
        ("base64-encoder.html", "Кодировщик / декодировщик Base64", "Преобразование текста в Base64 и обратно, безопасно для UTF-8."),
        ("json-formatter.html", "Форматирование JSON", "Форматирует, проверяет и минифицирует JSON с древовидным представлением."),
    ],
)

PAGES["ja"] = dict(
    title="UUIDジェネレーター：UUID v4 一括生成 | norito",
    meta_desc="ランダムなUUID v4識別子をブラウザ内で一括生成。大文字化・ハイフンなしオプション、1件または全件をコピー。どこにも送信されません。",
    app_name="UUIDジェネレーター", h1="UUIDジェネレーター", breadcrumb_label="UUIDジェネレーター",
    lede="ブラウザ組み込みの暗号論的乱数生成器を使ってランダムなUUID v4識別子を生成します。1個でも100個でも一度に生成でき、どこにも送信されません。",
    t=dict(
        count="件数", generate="生成", copy_all="すべてコピー",
        uppercase="大文字", remove_hyphens="ハイフンを削除",
        what_h3="UUID v4とは？", what_p="128ビットのランダム性を、標準的な識別子として整形したもの。",
        what_note="UUID v4は122ビットのランダムな値です（残り6ビットはバージョンとバリアントを示すために固定）。可能な値はおよそ5.3 undecillion（10の36乗のオーダー）通りです。衝突の確率は極めて低く、データベースの主キー、リクエストID、ファイル名として実用上問題になりません。",
        uses_h3="よくある用途",
        uses_note="行数が漏れないデータベース主キー、APIリクエスト用の冪等性キー、サービス間でログを追跡するための相関ID、そして異なるマシンで同時に生成しても衝突しないユニークなファイル名やセッション名。",
        how_h2="仕組み",
        how_p1='各IDはブラウザ組み込みのジェネレーターである <code>crypto.randomUUID()</code> から生成されます。内部ではOSの暗号論的に安全な乱数源（TLS鍵を生成するのと同じ源）から128ビットを取得し、そのうち6ビットに固定値を刻印します。バージョンのニブルは4に、バリアントビットは10になります。そのため、ここで生成されるすべてのUUIDは3番目のグループの先頭が4になり、4番目のグループの先頭が8、9、a、bのいずれかになります。残りの122ビットは純粋にランダムであり、これが実質的に衝突を問題にしない理由です。',
        how_p2="どれくらい問題にならないか？ 可能なv4 UUIDは2^122通り、約5.3 undecillion通りです。誕生日問題の数学によれば、たった1回の衝突確率が100万分の1に達するまでには、およそ103兆個のUUIDを生成する必要があります。システムが生成するあらゆるIDは、この数字に対しては誤差の範囲でしかなく、これがv4 UUIDをどのマシンでも協調なしに安全に生成できる理由です。",
        how_p3="生成はブラウザAPIの1回の呼び出しにすぎないため、サーバーへの要求も送信も一切発生しません。開発者ツールのネットワークタブを開いて「生成」をクリックしても、何も起きないことを確認できます。大文字化とハイフンなしのトグルは、すでに生成されたIDを整形し直すだけで、内部の値自体は変わりません。",
        how_p4="実用上の注意点として、v4 UUIDは意図的に順序を持たないため、データベースの主キーとして使うと挿入がインデックス全体に分散します。作成日時順に並べ替えたいIDが必要な場合は、上位ビットにタイムスタンプを持つUUID v7を検討してください。それ以外の用途（リクエストID、ファイル名、相関トークンなど）には、ランダムなv4がまさに最適です。",
    ),
    related_tools=[
        ("hash-generator.html", "ハッシュジェネレーター", "任意のテキストのMD5、SHA-1、SHA-256、SHA-512。"),
        ("base64-encoder.html", "Base64 エンコード / デコード", "テキストを Base64 との間で変換、UTF-8 セーフ。"),
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証・圧縮し、ツリー表示できます。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "uuid-generator.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-uuid.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/uuid-generator.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
