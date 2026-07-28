#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/outputs")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="9" y2="9"/><line x1="4" x2="20" y1="15" y2="15"/><line x1="10" x2="8" y1="3" y2="21"/><line x1="16" x2="14" y1="3" y2="21"/></svg>'
ICON_CLASS = "c-coral"

def body(labels):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field" style="margin-bottom:20px;">
          <label for="input">{labels['text_label']}</label>
          <textarea id="input" class="mono-area" rows="6" placeholder="{labels['placeholder']}"></textarea>
        </div>
        <div id="hashList"></div>
      </div>

      <div>
        <div class="panel">
          <div class="panel-header">
            <div class="icon-chip c-coral" style="width:36px;height:36px;">
              {ICON_SVG}
            </div>
            <div>
              <h3>{labels['which_h3']}</h3>
              <p>{labels['which_p']}</p>
            </div>
          </div>
          <p class="note" style="margin-top:0;">
            {labels['which_note']}
          </p>
        </div>
        <div class="panel">
          <h3 style="margin-top:0;">{labels['not_pw_h3']}</h3>
          <p class="note" style="margin-top:0;">
            {labels['not_pw_note']}
          </p>
        </div>
      </div>
    </div>

    <div class="explain-panel">
      <h2>{labels['how_h2']}</h2>
      <p>
        {labels['how_p1']}
      </p>
      <p>
        {labels['how_p2']}
      </p>
      <p>
        {labels['how_p3']}
      </p>
    </div>
'''

PAGES = {}

PAGES["es"] = dict(
    title="Generador de hashes: MD5, SHA-1, SHA-256, SHA-512 | norito",
    meta_desc="Genera hashes MD5, SHA-1, SHA-256 y SHA-512 de cualquier texto, en vivo mientras escribes, completamente en tu navegador. No se sube nada.",
    app_name="Generador de hashes",
    breadcrumb_label="Generador de hashes",
    h1="Generador de hashes",
    lede="MD5, SHA-1, SHA-256 y SHA-512 de cualquier texto, calculados en vivo en tu navegador con la API Web Crypto. Nada de lo que escribes se envía a ningún sitio.",
    labels=dict(
        text_label="Texto",
        placeholder="Escribe o pega texto para calcular su hash...",
        which_h3="¿Cuál debería usar?",
        which_p="Depende de para qué estés calculando el hash.",
        which_note="SHA-256 es la opción segura por defecto para sumas de verificación e integridad. MD5 y SHA-1 están criptográficamente rotos (es posible construir colisiones); sirven para comprobar que un archivo no se corrompió en la transferencia, pero no para nada sensible como el almacenamiento de contraseñas.",
        not_pw_h3="No sirve para contraseñas",
        not_pw_note="Ninguno de estos algoritmos debe usarse para almacenar contraseñas: son deliberadamente rápidos, justo lo contrario de lo que hace falta para esa tarea. El almacenamiento de contraseñas necesita un algoritmo lento y diseñado para ello, como bcrypt, scrypt o Argon2.",
        how_h2="Cómo funciona",
        how_p1='SHA-1, SHA-256 y SHA-512 se calculan con la API nativa <code>crypto.subtle.digest</code> de tu navegador: tu texto se convierte a bytes UTF-8 con <code>TextEncoder</code>, se procesa de forma nativa y el resultado se formatea como hexadecimal en minúsculas. MD5 es la excepción: Web Crypto se niega deliberadamente a implementarlo (está criptográficamente roto), así que esta herramienta incluye una pequeña implementación en JavaScript de RFC 1321 solo para MD5. Los cuatro se recalculan en cada pulsación, con una protección que descarta resultados obsoletos si escribes más rápido de lo que tardan los cálculos.',
        how_p2='Un problema práctico al comparar con una terminal: esta herramienta calcula el hash exactamente de los bytes que escribiste, sin salto de línea final. <code>echo "hello" | sha256sum</code> nunca coincidirá, porque <code>echo</code> añade un salto de línea y en realidad estás calculando el hash de "hello\\n". Usa <code>printf \'%s\' "hello" | sha256sum</code> en su lugar y los hashes coincidirán exactamente. Esta misma trampa explica la mayoría de los casos de "por qué mi hash no coincide" entre lenguajes y herramientas.',
        how_p3="Como <code>crypto.subtle</code> vive dentro del navegador, no hace falta enviar nada a ningún sitio para calcular un hash. Puedes comprobarlo: abre la pestaña Red de las herramientas de desarrollador y escribe una contraseña o clave de API en el campo. No aparece ninguna petición, tu texto se queda en la pestaña.",
    ),
    related_tools=[
        ("base64-encoder.html", "Codificar / Decodificar Base64", "Convierte texto a y desde Base64, seguro para UTF-8."),
        ("/uuid-generator.html", "Generador de UUID", "Identificadores UUID v4 aleatorios en lote."),
        ("password-generator.html", "Generador de contraseñas", "Contraseñas aleatorias seguras o frases fáciles de recordar."),
    ],
)

PAGES["zh"] = dict(
    title="哈希生成器：MD5、SHA-1、SHA-256、SHA-512 | norito",
    meta_desc="即时生成任意文本的 MD5、SHA-1、SHA-256 和 SHA-512 哈希值，输入即算，完全在浏览器本地完成，不会上传任何内容。",
    app_name="哈希生成器",
    breadcrumb_label="哈希生成器",
    h1="哈希生成器",
    lede="任意文本的 MD5、SHA-1、SHA-256 和 SHA-512 哈希值，使用 Web Crypto API 在浏览器中实时计算。你输入的内容不会发送到任何地方。",
    labels=dict(
        text_label="文本",
        placeholder="输入或粘贴要计算哈希的文本…",
        which_h3="应该用哪一种？",
        which_p="取决于你计算哈希的用途。",
        which_note="SHA-256 是校验和与完整性检查的安全默认选择。MD5 和 SHA-1 在密码学上都已被攻破（可以构造出碰撞），适合用来检查文件在传输中是否损坏，但不适合任何安全敏感的场景，比如存储密码。",
        not_pw_h3="不能用于密码",
        not_pw_note="这些算法都不应该用来存储密码——它们被特意设计得很快，而这恰恰是密码存储最不需要的特性。密码存储需要专门设计的慢速算法，比如 bcrypt、scrypt 或 Argon2。",
        how_h2="工作原理",
        how_p1='SHA-1、SHA-256 和 SHA-512 由浏览器内置的 <code>crypto.subtle.digest</code> API 计算：你的文本先用 <code>TextEncoder</code> 转换为 UTF-8 字节，原生计算摘要，结果格式化为小写十六进制。MD5 是个例外：Web Crypto 特意拒绝实现它（因为它在密码学上已被攻破），所以这个工具内置了一个小型的 RFC 1321 JavaScript 实现专门用于 MD5。四种算法在每次按键时都会重新计算，并有防护机制：如果你打字速度快于计算完成速度，会丢弃过时的结果。',
        how_p2='和终端比对时的一个实际陷阱：这个工具计算的哈希严格对应你输入的字节，末尾没有换行符。<code>echo "hello" | sha256sum</code> 永远不会匹配，因为 <code>echo</code> 会追加一个换行符，你实际计算的是 "hello\\n" 的哈希。换成 <code>printf \'%s\' "hello" | sha256sum</code>，结果就能完全一致。这个陷阱也解释了不同语言和工具之间"为什么我的哈希对不上"的大多数情况。',
        how_p3="由于 <code>crypto.subtle</code> 运行在浏览器内部，计算摘要不需要把任何东西发送出去。你可以自己验证：打开开发者工具的网络面板，在输入框中输入密码或 API 密钥。不会出现任何请求，你的文本始终留在这个标签页里。",
    ),
    related_tools=[
        ("/base64-encoder.html", "Base64 编码 / 解码", "文本与 Base64 互转，UTF-8 安全。"),
        ("/uuid-generator.html", "UUID 生成器", "批量生成随机 UUID v4 标识符。"),
        ("password-generator.html", "密码生成器", "生成安全的随机密码或易记的密码短语。"),
    ],
)

PAGES["ar"] = dict(
    title="مولّد التجزئة: MD5، SHA-1، SHA-256، SHA-512 | norito",
    meta_desc="أنشئ قيم تجزئة MD5 وSHA-1 وSHA-256 وSHA-512 لأي نص، مباشرةً أثناء الكتابة، بالكامل داخل متصفحك. لا يُرفع أي شيء.",
    app_name="مولّد التجزئة",
    breadcrumb_label="مولّد التجزئة",
    h1="مولّد التجزئة",
    lede="قيم تجزئة MD5 وSHA-1 وSHA-256 وSHA-512 لأي نص، تُحسب مباشرةً في متصفحك باستخدام واجهة Web Crypto. لا يُرسل أي شيء تكتبه إلى أي مكان.",
    labels=dict(
        text_label="النص",
        placeholder="اكتب أو الصق نصًا لحساب تجزئته...",
        which_h3="أيّها يجب أن أستخدم؟",
        which_p="يعتمد على الغرض من حساب التجزئة.",
        which_note="خوارزمية SHA-256 هي الخيار الآمن الافتراضي لعمليات التحقق من السلامة ومجاميع التحقق. أما MD5 وSHA-1 فمكسورتان تشفيريًا (يمكن إنشاء تصادمات عمليًا)، وتصلحان للتحقق من أن ملفًا لم يتلف أثناء النقل، لكن لا تصلحان لأي شيء حسّاس أمنيًا مثل تخزين كلمات المرور.",
        not_pw_h3="لا تصلح لكلمات المرور",
        not_pw_note="لا ينبغي استخدام أي من هذه الخوارزميات لتخزين كلمات المرور؛ فهي سريعة عمدًا، وهو ما يتعارض تمامًا مع متطلبات تلك المهمة. يحتاج تخزين كلمات المرور إلى خوارزمية بطيئة مصمّمة خصيصًا لذلك، مثل bcrypt أو scrypt أو Argon2.",
        how_h2="كيف يعمل",
        how_p1='تُحسب SHA-1 وSHA-256 وSHA-512 عبر واجهة <code>crypto.subtle.digest</code> المدمجة في متصفحك: يُحوَّل نصك إلى بايتات UTF-8 باستخدام <code>TextEncoder</code>، ثم تُحسب التجزئة بشكل أصلي، وتُنسَّق النتيجة كسداسي عشري بأحرف صغيرة. أما MD5 فهي الاستثناء: ترفض Web Crypto عمدًا تنفيذها (لأنها مكسورة تشفيريًا)، لذا تتضمن هذه الأداة تنفيذًا صغيرًا بلغة JavaScript لمعيار RFC 1321 خاصًا بـ MD5 فقط. تُعاد حسابات الخوارزميات الأربع مع كل ضغطة مفتاح، مع حماية تتجاهل النتائج القديمة إذا كتبت أسرع من انتهاء الحسابات.',
        how_p2='مشكلة عملية شائعة عند المقارنة مع الطرفية: تحسب هذه الأداة تجزئة البايتات التي كتبتها بالضبط، دون سطر جديد في النهاية. لن يتطابق أمر <code>echo "hello" | sha256sum</code> أبدًا، لأن <code>echo</code> يضيف سطرًا جديدًا وأنت فعليًا تحسب تجزئة "hello\\n". استخدم بدلاً من ذلك <code>printf \'%s\' "hello" | sha256sum</code> لتتطابق القيم تمامًا. هذا الفخ نفسه يفسّر معظم حالات "لماذا لا تتطابق تجزئتي" بين اللغات والأدوات.',
        how_p3="بما أن <code>crypto.subtle</code> يعمل داخل المتصفح، فلا حاجة لإرسال أي شيء إلى أي مكان لحساب التجزئة. يمكنك التحقق بنفسك: افتح تبويب الشبكة في أدوات المطوّر واكتب كلمة مرور أو مفتاح API في الحقل. لن يظهر أي طلب، ويبقى نصك داخل التبويب.",
    ),
    related_tools=[
        ("/base64-encoder.html", "ترميز / فك ترميز Base64", "حوّل النص من وإلى Base64، آمن مع UTF-8."),
        ("/uuid-generator.html", "مولّد UUID", "معرّفات UUID v4 عشوائية بالجملة."),
        ("password-generator.html", "مولّد كلمات المرور", "كلمات مرور عشوائية قوية أو عبارات مرور يسهل تذكرها."),
    ],
)

PAGES["hi"] = dict(
    title="हैश जनरेटर: MD5, SHA-1, SHA-256, SHA-512 | norito",
    meta_desc="किसी भी टेक्स्ट के MD5, SHA-1, SHA-256 और SHA-512 हैश टाइप करते ही, पूरी तरह आपके ब्राउज़र में जनरेट करें। कुछ भी अपलोड नहीं होता।",
    app_name="हैश जनरेटर",
    breadcrumb_label="हैश जनरेटर",
    h1="हैश जनरेटर",
    lede="किसी भी टेक्स्ट के MD5, SHA-1, SHA-256 और SHA-512 हैश, Web Crypto API का उपयोग करके आपके ब्राउज़र में लाइव कैलकुलेट किए जाते हैं। आपके टाइप किए गए टेक्स्ट को कहीं नहीं भेजा जाता।",
    labels=dict(
        text_label="टेक्स्ट",
        placeholder="हैश करने के लिए टेक्स्ट टाइप या पेस्ट करें...",
        which_h3="कौन-सा इस्तेमाल करें?",
        which_p="यह इस बात पर निर्भर करता है कि आप हैश किसलिए बना रहे हैं।",
        which_note="चेकसम और इंटीग्रिटी जांच के लिए SHA-256 सुरक्षित डिफ़ॉल्ट विकल्प है। MD5 और SHA-1 दोनों क्रिप्टोग्राफ़िक रूप से टूट चुके हैं (कोलिज़न बनाना व्यावहारिक रूप से संभव है), ये यह जांचने के लिए ठीक हैं कि ट्रांसफ़र के दौरान फ़ाइल करप्ट तो नहीं हुई, लेकिन पासवर्ड स्टोरेज जैसे किसी भी सुरक्षा-संवेदनशील काम के लिए उपयुक्त नहीं हैं।",
        not_pw_h3="पासवर्ड के लिए नहीं",
        not_pw_note="इनमें से किसी भी एल्गोरिद्म का उपयोग पासवर्ड स्टोर करने के लिए नहीं करना चाहिए—ये जानबूझकर तेज़ बनाए गए हैं, जो इस काम के लिए बिल्कुल गलत है। पासवर्ड स्टोरेज के लिए bcrypt, scrypt या Argon2 जैसे धीमे, खास तौर पर इसी काम के लिए बनाए गए एल्गोरिद्म चाहिए।",
        how_h2="यह कैसे काम करता है",
        how_p1='SHA-1, SHA-256 और SHA-512 आपके ब्राउज़र की बिल्ट-इन <code>crypto.subtle.digest</code> API से कैलकुलेट होते हैं: आपका टेक्स्ट <code>TextEncoder</code> से UTF-8 बाइट्स में बदला जाता है, नेटिव रूप से डाइजेस्ट किया जाता है, और नतीजे को लोअरकेस हेक्स में फ़ॉर्मेट किया जाता है। MD5 अपवाद है: Web Crypto जानबूझकर इसे लागू नहीं करता (क्योंकि यह क्रिप्टोग्राफ़िक रूप से टूट चुका है), इसलिए यह टूल सिर्फ़ MD5 के लिए RFC 1321 का एक छोटा जावास्क्रिप्ट इम्प्लीमेंटेशन शामिल करता है। चारों हर कीस्ट्रोक पर फिर से कैलकुलेट होते हैं, और अगर आप डाइजेस्ट पूरा होने से तेज़ टाइप करें तो पुराने नतीजों को हटाने वाला एक गार्ड भी है।',
        how_p2='टर्मिनल से मिलान करते समय एक व्यावहारिक झोल: यह टूल ठीक उन्हीं बाइट्स को हैश करता है जो आपने टाइप कीं, बिना किसी ट्रेलिंग न्यूलाइन के। <code>echo "hello" | sha256sum</code> कभी मैच नहीं करेगा, क्योंकि <code>echo</code> एक न्यूलाइन जोड़ देता है और आप असल में "hello\\n" हैश कर रहे होते हैं। इसकी जगह <code>printf \'%s\' "hello" | sha256sum</code> इस्तेमाल करें और डाइजेस्ट बिल्कुल मैच करेंगे। यही झोल भाषाओं और टूल्स के बीच ज़्यादातर "मेरा हैश क्यों नहीं मिल रहा" वाले मामलों की वजह है।',
        how_p3="चूँकि <code>crypto.subtle</code> ब्राउज़र के अंदर ही चलता है, इसलिए डाइजेस्ट कैलकुलेट करने के लिए कहीं कुछ भेजने की ज़रूरत नहीं। आप खुद पुष्टि कर सकते हैं: डेवलपर टूल्स का नेटवर्क टैब खोलें और इनपुट में कोई पासवर्ड या API की टाइप करें। कोई रिक्वेस्ट नहीं दिखेगी, आपका टेक्स्ट टैब में ही रहता है।",
    ),
    related_tools=[
        ("/base64-encoder.html", "Base64 एनकोड / डिकोड", "टेक्स्ट को Base64 में और वापस बदलें, UTF-8 सेफ़।"),
        ("/uuid-generator.html", "UUID जनरेटर", "बल्क रैंडम UUID v4 आइडेंटिफ़ायर।"),
        ("password-generator.html", "पासवर्ड जनरेटर", "रैंडम, मज़बूत पासवर्ड या याद रखने में आसान पासफ़्रेज़."),
    ],
)

PAGES["ru"] = dict(
    title="Генератор хешей: MD5, SHA-1, SHA-256, SHA-512 | norito",
    meta_desc="Создавайте хеши MD5, SHA-1, SHA-256 и SHA-512 любого текста прямо во время набора, полностью в вашем браузере. Ничего не загружается на сервер.",
    app_name="Генератор хешей",
    breadcrumb_label="Генератор хешей",
    h1="Генератор хешей",
    lede="Хеши MD5, SHA-1, SHA-256 и SHA-512 любого текста, вычисляемые в реальном времени в вашем браузере с помощью Web Crypto API. Всё, что вы вводите, никуда не отправляется.",
    labels=dict(
        text_label="Текст",
        placeholder="Введите или вставьте текст для хеширования...",
        which_h3="Какой алгоритм выбрать?",
        which_p="Зависит от того, для чего вам нужен хеш.",
        which_note="SHA-256 — безопасный вариант по умолчанию для контрольных сумм и проверки целостности. MD5 и SHA-1 криптографически скомпрометированы (для них практически возможно построить коллизии): они подходят, чтобы проверить, что файл не повредился при передаче, но не годятся ни для чего, связанного с безопасностью, например для хранения паролей.",
        not_pw_h3="Не подходит для паролей",
        not_pw_note="Ни один из этих алгоритмов нельзя использовать для хранения паролей — они намеренно быстрые, а это как раз то, что не нужно для такой задачи. Для хранения паролей нужен медленный, специально созданный для этого алгоритм, например bcrypt, scrypt или Argon2.",
        how_h2="Как это работает",
        how_p1='SHA-1, SHA-256 и SHA-512 вычисляются встроенным в браузер API <code>crypto.subtle.digest</code>: ваш текст преобразуется в байты UTF-8 через <code>TextEncoder</code>, хешируется нативно, а результат форматируется как шестнадцатеричная строка в нижнем регистре. MD5 — исключение: Web Crypto намеренно отказывается его реализовывать (поскольку он криптографически скомпрометирован), поэтому этот инструмент включает небольшую JavaScript-реализацию RFC 1321 специально для MD5. Все четыре хеша пересчитываются при каждом нажатии клавиши, с защитой, которая отбрасывает устаревшие результаты, если вы печатаете быстрее, чем завершаются вычисления.',
        how_p2='Практическая ловушка при сверке с терминалом: этот инструмент хеширует ровно те байты, которые вы ввели, без завершающего перевода строки. <code>echo "hello" | sha256sum</code> никогда не совпадёт, потому что <code>echo</code> добавляет перевод строки, и вы фактически хешируете "hello\\n". Вместо этого используйте <code>printf \'%s\' "hello" | sha256sum</code> — и хеши совпадут точно. Та же самая ловушка объясняет большинство случаев «почему мой хеш не совпадает» между разными языками и инструментами.',
        how_p3="Поскольку <code>crypto.subtle</code> работает внутри браузера, для вычисления хеша ничего никуда отправлять не нужно. Вы можете убедиться в этом сами: откройте вкладку «Сеть» в инструментах разработчика и введите пароль или API-ключ в поле. Ни один запрос не появится — текст остаётся во вкладке.",
    ),
    related_tools=[
        ("/base64-encoder.html", "Кодировщик / декодировщик Base64", "Преобразование текста в Base64 и обратно, безопасно для UTF-8."),
        ("/uuid-generator.html", "Генератор UUID", "Массовая генерация случайных идентификаторов UUID v4."),
        ("password-generator.html", "Генератор паролей", "Надёжные случайные пароли или легко запоминающиеся фразы."),
    ],
)

PAGES["ja"] = dict(
    title="ハッシュジェネレーター: MD5, SHA-1, SHA-256, SHA-512 | norito",
    meta_desc="任意のテキストの MD5、SHA-1、SHA-256、SHA-512 ハッシュを、入力と同時にブラウザ内だけで生成します。アップロードは一切行われません。",
    app_name="ハッシュジェネレーター",
    breadcrumb_label="ハッシュジェネレーター",
    h1="ハッシュジェネレーター",
    lede="任意のテキストの MD5、SHA-1、SHA-256、SHA-512 ハッシュを、Web Crypto API を使ってブラウザ内でリアルタイムに計算します。入力した内容はどこにも送信されません。",
    labels=dict(
        text_label="テキスト",
        placeholder="ハッシュ化するテキストを入力または貼り付け...",
        which_h3="どれを使えばいい？",
        which_p="何のためにハッシュを計算するかによります。",
        which_note="SHA-256 はチェックサムや整合性確認における安全なデフォルトです。MD5 と SHA-1 はどちらも暗号学的に破られており（衝突の作成が現実的に可能）、転送中にファイルが壊れていないかの確認には使えますが、パスワード保存のようなセキュリティ上重要な用途には適していません。",
        not_pw_h3="パスワードには使えません",
        not_pw_note="これらのアルゴリズムはいずれもパスワードの保存に使うべきではありません。意図的に高速に作られており、それはこの用途にとってまさに逆効果だからです。パスワードの保存には、bcrypt、scrypt、Argon2 のような、あえて低速に設計された専用アルゴリズムが必要です。",
        how_h2="仕組み",
        how_p1='SHA-1、SHA-256、SHA-512 はブラウザ組み込みの <code>crypto.subtle.digest</code> API で計算されます。テキストは <code>TextEncoder</code> で UTF-8 バイト列に変換され、ネイティブにダイジェストされ、結果は小文字の16進数としてフォーマットされます。MD5 だけは例外です。Web Crypto は（暗号学的に破られているため）意図的に MD5 を実装していないので、このツールは MD5 専用に RFC 1321 の小さな JavaScript 実装を同梱しています。4つとも入力のたびに再計算され、計算が終わるより速くタイプした場合は古い結果を破棄するガードが働きます。',
        how_p2='ターミナルと突き合わせるときによくある落とし穴があります。このツールは入力したバイト列そのものをハッシュ化し、末尾に改行は付きません。<code>echo "hello" | sha256sum</code> は決して一致しません。<code>echo</code> は改行を付加するため、実際には "hello\\n" をハッシュ化していることになるからです。代わりに <code>printf \'%s\' "hello" | sha256sum</code> を使えば、ダイジェストは正確に一致します。同じ落とし穴が、言語やツール間で「ハッシュが一致しない」問題の大半の原因になっています。',
        how_p3="<code>crypto.subtle</code> はブラウザ内部で動作するため、ダイジェストの計算に何かをどこかへ送信する必要はありません。実際に確認できます。開発者ツールのネットワークタブを開き、入力欄にパスワードや API キーを入力してみてください。リクエストは一切発生せず、テキストはそのタブの中にとどまります。",
    ),
    related_tools=[
        ("/base64-encoder.html", "Base64 エンコード / デコード", "テキストを Base64 との間で変換、UTF-8 セーフ。"),
        ("/uuid-generator.html", "UUID ジェネレーター", "ランダムな UUID v4 識別子を一括生成。"),
        ("password-generator.html", "パスワードジェネレーター", "安全なランダムパスワード、または覚えやすいフレーズ。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "hash-generator.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["labels"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-hash.js"],
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/hash-generator.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
