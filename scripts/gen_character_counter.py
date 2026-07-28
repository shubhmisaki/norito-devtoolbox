#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 7A5 5 0 0 0 7 7"/><path d="M7 7v10a5 5 0 0 0 10 0V7"/></svg>'
ICON_CLASS = "c-coral"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field">
          <label for="textInput">{t['your_text']}</label>
          <textarea id="textInput" class="mono-output" rows="10" placeholder="{t['placeholder']}"></textarea>
        </div>
        <div class="meta-list">
          <div class="meta-row"><span class="meta-label">{t['with_spaces']}</span><span class="meta-value" id="statWithSpaces">0</span></div>
          <div class="meta-row"><span class="meta-label">{t['no_spaces']}</span><span class="meta-value" id="statNoSpaces">0</span></div>
          <div class="meta-row"><span class="meta-label">{t['bytes']}</span><span class="meta-value" id="statBytes">0</span></div>
        </div>
      </div>
      <div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['common_limits']}</h3>
          <div class="meta-list" id="limitList"></div>
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
    title="Contador de caracteres: comprueba límites de plataformas | norito",
    meta_desc="Cuenta caracteres con y sin espacios, más el tamaño en bytes, y compáralo en vivo con los límites de tuits, SMS y meta descripciones. No se sube nada.",
    app_name="Contador de caracteres", h1="Contador de caracteres", breadcrumb_label="Contador de caracteres",
    lede="Recuento de caracteres en vivo, con y sin espacios, tamaño en bytes, y qué tan cerca estás de los límites habituales de plataformas como tuits y meta descripciones.",
    t=dict(
        your_text="Tu texto", placeholder="Pega o escribe tu texto aquí...",
        with_spaces="Caracteres (con espacios)", no_spaces="Caracteres (sin espacios)", bytes="Tamaño en bytes (UTF-8)",
        common_limits="Límites habituales",
        how_h2="Cómo funciona",
        how_p1='En cada pulsación la página recalcula tres números. El recuento de caracteres es <code>.length</code> de JavaScript, que cuenta unidades de código UTF-16. El recuento sin espacios elimina primero todos los espacios en blanco (espacios, tabulaciones, saltos de línea) con una expresión regular. El tamaño en bytes pasa tu texto por la API <code>TextEncoder</code> del navegador, que produce los bytes UTF-8 reales que el texto ocuparía en un archivo, una columna de base de datos o el cuerpo de una petición HTTP. La lista de límites de plataformas es entonces solo una resta contra cada límite, cambiando al estilo "excedido" en cuanto lo superas.',
        how_p2='La diferencia entre esos números es donde la gente se sorprende. Un emoji como una carita sonriente es un símbolo visible pero dos unidades de código UTF-16 (por lo que cuenta como 2 caracteres aquí, y en muchas plataformas) y cuatro bytes de UTF-8. Para SMS en concreto, el límite de 160 caracteres asume que el mensaje se mantiene dentro del antiguo alfabeto GSM-7: incluye un solo emoji o una comilla tipográfica y el operador cambia silenciosamente todo el mensaje a codificación UCS-2, reduciendo el límite por segmento a 70 caracteres. Si al editar un solo carácter tu texto de repente se divide en dos segmentos de SMS, esa es la razón.',
        how_p3="El recuento ocurre por completo en el JavaScript de esta página. Abre la pestaña Red de las herramientas de desarrollador mientras escribes: verás cero peticiones, porque tu texto nunca sale del navegador.",
    ),
    related_tools=[
        ("/word-counter.html", "Contador de palabras", "Recuento de palabras, frases y párrafos, más tiempo de lectura."),
        ("limited-text-generator.html", "Generador de texto limitado", "Genera texto de relleno con una longitud exacta."),
        ("seo-slug-generator.html", "Generador de slugs SEO", "Slugs de URL limpios a partir de títulos."),
    ],
)

PAGES["zh"] = dict(
    title="字符计数器：检查平台限制 | norito",
    meta_desc="统计含空格和不含空格的字符数以及字节大小，并实时对照推文、短信和 meta 描述的限制。不会上传任何内容。",
    app_name="字符计数器", h1="字符计数器", breadcrumb_label="字符计数器",
    lede="实时统计含空格和不含空格的字符数、字节大小，以及与推文、meta 描述等常见平台限制的接近程度。",
    t=dict(
        your_text="你的文本", placeholder="在此粘贴或输入文本…",
        with_spaces="字符数（含空格）", no_spaces="字符数（不含空格）", bytes="字节大小（UTF-8）",
        common_limits="常见限制",
        how_h2="工作原理",
        how_p1='每次按键时，页面都会重新计算三个数值。字符数是 JavaScript 的 <code>.length</code>，统计的是 UTF-16 代码单元数。不含空格的计数会先用正则表达式去除所有空白（空格、制表符、换行符）。字节大小则将你的文本传入浏览器的 <code>TextEncoder</code> API，得到该文本在文件、数据库列或 HTTP 请求体中实际占用的 UTF-8 字节数。平台限制列表只是用每个限制值做减法，一旦超出就切换为"超限"样式。',
        how_p2="这些数值之间的差异正是容易踩坑的地方。一个笑脸表情符号在视觉上是一个符号，但在这里（以及许多平台上）算作 2 个 UTF-16 代码单元，也就是 2 个字符，并占用 4 个 UTF-8 字节。就短信而言，160 字符的限制是假设消息始终使用旧的 GSM-7 字符集：只要包含一个表情符号或弯引号，运营商就会悄悄把整条消息切换为 UCS-2 编码，把单段限制降到 70 个字符。如果修改了一个字符，短信突然被拆成两段，原因就在这里。",
        how_p3="统计完全在本页面的 JavaScript 中完成。打字时打开开发者工具的网络面板：你会看到零请求，因为你的文本从未离开浏览器。",
    ),
    related_tools=[
        ("/word-counter.html", "字数统计", "统计单词数、句子数、段落数及预计阅读时间。"),
        ("limited-text-generator.html", "限长文本生成器", "生成精确长度的占位文本。"),
        ("seo-slug-generator.html", "SEO Slug 生成器", "从标题生成简洁的 URL slug。"),
    ],
)

PAGES["ar"] = dict(
    title="عدّاد الأحرف: تحقّق من حدود المنصات | norito",
    meta_desc="عُدّ الأحرف مع المسافات وبدونها، بالإضافة إلى الحجم بالبايت، وتحقّق مباشرةً من حدود التغريدات والرسائل النصية وأوصاف الميتا. لا يُرفع أي شيء.",
    app_name="عدّاد الأحرف", h1="عدّاد الأحرف", breadcrumb_label="عدّاد الأحرف",
    lede="عدّ فوري للأحرف، مع المسافات وبدونها، والحجم بالبايت، ومدى قربك من الحدود الشائعة للمنصات مثل التغريدات وأوصاف الميتا.",
    t=dict(
        your_text="نصّك", placeholder="الصق أو اكتب نصّك هنا...",
        with_spaces="الأحرف (مع المسافات)", no_spaces="الأحرف (بدون مسافات)", bytes="الحجم بالبايت (UTF-8)",
        common_limits="الحدود الشائعة",
        how_h2="كيف يعمل",
        how_p1='مع كل ضغطة مفتاح، تُعيد الصفحة حساب ثلاثة أرقام. عدّ الأحرف هو خاصية <code>.length</code> في جافاسكريبت، التي تحسب وحدات ترميز UTF-16. أما العدّ بدون مسافات فيزيل أولًا كل المسافات البيضاء (المسافات وعلامات التبويب وفواصل الأسطر) باستخدام تعبير نمطي. يُمرَّر نصك عبر واجهة <code>TextEncoder</code> الخاصة بالمتصفح لحساب الحجم بالبايت، والتي تُنتج بايتات UTF-8 الفعلية التي سيشغلها النص في ملف أو عمود قاعدة بيانات أو نص طلب HTTP. أما قائمة حدود المنصات فهي مجرد عملية طرح مقابل كل حد، وتتحول إلى تنسيق "تجاوز الحد" بمجرد تخطّيه.',
        how_p2='الفجوة بين هذه الأرقام هي ما يُوقع الناس في المفاجآت. الإيموجي مثل الوجه المبتسم هو رمز واحد مرئي لكنه وحدتا ترميز UTF-16 (لذا يُحسب كحرفين هنا، وعلى العديد من المنصات) وأربعة بايتات من UTF-8. بالنسبة للرسائل النصية تحديدًا، يفترض حدّ الـ160 حرفًا أن الرسالة تبقى ضمن أبجدية GSM-7 القديمة: أضف إيموجي واحدًا أو علامة اقتباس "ذكية" منحنية وسيحوّل مشغّل الشبكة الرسالة بأكملها بصمت إلى ترميز UCS-2، مما يخفض حد الجزء الواحد إلى 70 حرفًا. إذا أدى تعديل حرف واحد فجأة إلى تقسيم نصك إلى جزأين من الرسائل النصية، فهذا هو السبب.',
        how_p3="يتم العدّ بالكامل داخل جافاسكريبت هذه الصفحة. افتح تبويب الشبكة في أدوات المطوّر أثناء الكتابة: لن ترى أي طلبات، لأن نصك لا يغادر المتصفح أبدًا.",
    ),
    related_tools=[
        ("/word-counter.html", "عدّاد الكلمات", "عدّ الكلمات والجمل والفقرات بالإضافة إلى وقت القراءة."),
        ("limited-text-generator.html", "مولّد نص محدود الطول", "أنشئ نصًا نائبًا بطول دقيق."),
        ("seo-slug-generator.html", "مولّد سلاجات SEO", "سلاجات URL نظيفة من العناوين."),
    ],
)

PAGES["hi"] = dict(
    title="कैरेक्टर काउंटर: प्लेटफ़ॉर्म लिमिट चेक करें | norito",
    meta_desc="स्पेस के साथ और बिना स्पेस कैरेक्टर गिनें, साथ ही बाइट साइज़, और लाइव ट्वीट, SMS और मेटा डिस्क्रिप्शन लिमिट के हिसाब से जांचें। कुछ भी अपलोड नहीं होता।",
    app_name="कैरेक्टर काउंटर", h1="कैरेक्टर काउंटर", breadcrumb_label="कैरेक्टर काउंटर",
    lede="लाइव कैरेक्टर काउंट, स्पेस के साथ और बिना स्पेस, बाइट साइज़, और आप ट्वीट व मेटा डिस्क्रिप्शन जैसी आम प्लेटफ़ॉर्म लिमिट के कितने करीब हैं।",
    t=dict(
        your_text="आपका टेक्स्ट", placeholder="यहाँ अपना टेक्स्ट पेस्ट या टाइप करें...",
        with_spaces="कैरेक्टर (स्पेस सहित)", no_spaces="कैरेक्टर (बिना स्पेस)", bytes="बाइट साइज़ (UTF-8)",
        common_limits="सामान्य लिमिट",
        how_h2="यह कैसे काम करता है",
        how_p1='हर कीस्ट्रोक पर पेज तीन नंबर फिर से कैलकुलेट करता है। कैरेक्टर काउंट जावास्क्रिप्ट का <code>.length</code> है, जो UTF-16 कोड यूनिट गिनता है। बिना-स्पेस वाला काउंट पहले एक रेगेक्स से सभी व्हाइटस्पेस (स्पेस, टैब, लाइन ब्रेक) हटा देता है। बाइट साइज़ आपके टेक्स्ट को ब्राउज़र के <code>TextEncoder</code> API से गुज़ारता है, जो असली UTF-8 बाइट्स बताता है कि वह टेक्स्ट किसी फ़ाइल, डेटाबेस कॉलम, या HTTP रिक्वेस्ट बॉडी में कितनी जगह लेगा। प्लेटफ़ॉर्म लिमिट लिस्ट फिर बस हर लिमिट के मुकाबले घटाव है, और जैसे ही आप उसे पार करते हैं "over" स्टाइल में बदल जाती है।',
        how_p2='इन नंबरों के बीच का फ़र्क वहीं है जहाँ लोग चौंक जाते हैं। स्माइली जैसा इमोजी एक दिखने वाला सिंबल है लेकिन दो UTF-16 कोड यूनिट (इसलिए यहाँ, और कई प्लेटफ़ॉर्म पर, 2 कैरेक्टर गिना जाता है) और UTF-8 के चार बाइट्स। खासकर SMS के लिए, 160-कैरेक्टर की लिमिट मानती है कि मैसेज पुरानी GSM-7 वर्णमाला के अंदर ही रहे: एक इमोजी या घुमावदार "स्मार्ट कोट" शामिल करें और कैरियर चुपचाप पूरे मैसेज को UCS-2 एन्कोडिंग में बदल देता है, जिससे प्रति-सेगमेंट लिमिट घटकर 70 कैरेक्टर रह जाती है। अगर एक कैरेक्टर के एडिट से आपका टेक्स्ट अचानक दो SMS सेगमेंट में बंट जाए, तो यही वजह है।',
        how_p3="गिनती पूरी तरह इस पेज के जावास्क्रिप्ट में होती है। टाइप करते समय डेवलपर टूल्स का नेटवर्क टैब खोलें: आपको शून्य रिक्वेस्ट दिखेंगी, क्योंकि आपका टेक्स्ट कभी ब्राउज़र से बाहर नहीं जाता।",
    ),
    related_tools=[
        ("/word-counter.html", "वर्ड काउंटर", "वर्ड, वाक्य और पैराग्राफ़ काउंट, साथ ही पढ़ने का समय।"),
        ("limited-text-generator.html", "लिमिटेड टेक्स्ट जनरेटर", "सटीक लंबाई का प्लेसहोल्डर टेक्स्ट जनरेट करें।"),
        ("seo-slug-generator.html", "SEO स्लग जनरेटर", "टाइटल से क्लीन URL स्लग।"),
    ],
)

PAGES["ru"] = dict(
    title="Счётчик символов: проверка лимитов платформ | norito",
    meta_desc="Считайте символы с пробелами и без, а также размер в байтах, и сверяйтесь в реальном времени с лимитами твитов, SMS и мета-описаний. Ничего не загружается.",
    app_name="Счётчик символов", h1="Счётчик символов", breadcrumb_label="Счётчик символов",
    lede="Подсчёт символов в реальном времени, с пробелами и без, размер в байтах, и насколько вы близки к типичным лимитам платформ вроде твитов и мета-описаний.",
    t=dict(
        your_text="Ваш текст", placeholder="Вставьте или введите текст здесь...",
        with_spaces="Символы (с пробелами)", no_spaces="Символы (без пробелов)", bytes="Размер в байтах (UTF-8)",
        common_limits="Типичные лимиты",
        how_h2="Как это работает",
        how_p1='При каждом нажатии клавиши страница пересчитывает три значения. Количество символов — это <code>.length</code> в JavaScript, которое считает единицы кода UTF-16. Подсчёт без пробелов сначала удаляет все пробельные символы (пробелы, табуляции, переносы строк) с помощью регулярного выражения. Размер в байтах пропускает ваш текст через API <code>TextEncoder</code> браузера, который выдаёт реальные байты UTF-8, которые текст займёт в файле, столбце базы данных или теле HTTP-запроса. Список лимитов платформ — это просто вычитание относительно каждого лимита, переключающееся на стиль «превышено» в момент, когда вы его пересекаете.',
        how_p2='Разрыв между этими числами — вот где люди попадают впросак. Эмодзи вроде улыбающегося лица — это один видимый символ, но две единицы кода UTF-16 (поэтому здесь, как и на многих платформах, он считается за 2 символа) и четыре байта UTF-8. Что касается SMS, лимит в 160 символов предполагает, что сообщение остаётся в рамках старого алфавита GSM-7: добавьте один эмодзи или изогнутую "умную" кавычку — и оператор незаметно переключает всё сообщение на кодировку UCS-2, снижая лимит на сегмент до 70 символов. Если правка одного символа вдруг разбила ваш текст на два SMS-сегмента, вот почему.',
        how_p3="Подсчёт происходит полностью в JavaScript этой страницы. Откройте вкладку «Сеть» в инструментах разработчика во время набора текста: вы увидите ноль запросов, потому что ваш текст никогда не покидает браузер.",
    ),
    related_tools=[
        ("/word-counter.html", "Счётчик слов", "Подсчёт слов, предложений и абзацев плюс время чтения."),
        ("limited-text-generator.html", "Генератор текста заданной длины", "Генерация текста-заполнителя точной длины."),
        ("seo-slug-generator.html", "Генератор SEO-слагов", "Чистые URL-слаги из заголовков."),
    ],
)

PAGES["ja"] = dict(
    title="文字数カウンター：プラットフォームの上限をチェック | norito",
    meta_desc="スペースあり・なしの文字数とバイトサイズをカウントし、ツイート、SMS、meta descriptionの上限とリアルタイムで比較。アップロードは一切行われません。",
    app_name="文字数カウンター", h1="文字数カウンター", breadcrumb_label="文字数カウンター",
    lede="スペースあり・なしのリアルタイム文字数、バイトサイズ、そしてツイートやmeta descriptionなど一般的なプラットフォームの上限にどれだけ近いかを表示します。",
    t=dict(
        your_text="テキスト", placeholder="ここにテキストを貼り付けるか入力...",
        with_spaces="文字数（スペースあり）", no_spaces="文字数（スペースなし）", bytes="バイトサイズ（UTF-8）",
        common_limits="よくある上限",
        how_h2="仕組み",
        how_p1='キー入力のたびに、ページは3つの数値を再計算します。文字数は JavaScript の <code>.length</code> で、UTF-16 コードユニット数をカウントします。スペースなしのカウントは、まず正規表現ですべての空白（スペース、タブ、改行）を取り除きます。バイトサイズはブラウザの <code>TextEncoder</code> API にテキストを通し、そのテキストがファイルやデータベースの列、HTTPリクエストボディで実際に占める UTF-8 バイト数を算出します。プラットフォームの上限リストは、各上限との単純な引き算で、上限を超えた瞬間に「超過」スタイルに切り替わります。',
        how_p2='これらの数値の差こそが落とし穴です。スマイリーのような絵文字は見た目には1つの記号ですが、UTF-16 では2コードユニット（そのためここでも多くのプラットフォームでも2文字としてカウントされます）、UTF-8では4バイトになります。特にSMSでは、160文字という上限は、メッセージが従来のGSM-7文字セット内に収まることを前提としています。絵文字1つやカーブした「スマート引用符」を1つ含めるだけで、キャリアはメッセージ全体を黙ってUCS-2エンコーディングに切り替え、セグメントあたりの上限が70文字まで下がります。1文字編集しただけで突然SMSが2セグメントに分かれてしまうのは、これが理由です。',
        how_p3="カウントはすべてこのページのJavaScript内で行われます。入力中に開発者ツールのネットワークタブを開いてみてください。リクエストは一切発生しません。テキストがブラウザの外に出ることはないからです。",
    ),
    related_tools=[
        ("/word-counter.html", "単語数カウンター", "単語数、文数、段落数と読了時間の目安。"),
        ("limited-text-generator.html", "文字数制限テキストジェネレーター", "指定した長さぴったりのダミーテキストを生成。"),
        ("seo-slug-generator.html", "SEOスラグジェネレーター", "タイトルからきれいなURLスラグを生成。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "character-counter.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-character-counter.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/character-counter.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
