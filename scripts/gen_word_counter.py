#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg>'
ICON_CLASS = "c-rose"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field">
          <label for="textInput">{t['your_text']}</label>
          <textarea id="textInput" class="mono-output" rows="14" placeholder="{t['placeholder']}"></textarea>
        </div>
      </div>
      <div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['stats']}</h3>
          <div class="meta-list">
            <div class="meta-row"><span class="meta-label">{t['words']}</span><span class="meta-value" id="statWords">0</span></div>
            <div class="meta-row"><span class="meta-label">{t['characters']}</span><span class="meta-value" id="statChars">0</span></div>
            <div class="meta-row"><span class="meta-label">{t['sentences']}</span><span class="meta-value" id="statSentences">0</span></div>
            <div class="meta-row"><span class="meta-label">{t['paragraphs']}</span><span class="meta-value" id="statParagraphs">0</span></div>
            <div class="meta-row"><span class="meta-label">{t['reading_time']}</span><span class="meta-value" id="statReadingTime">0 sec</span></div>
            <div class="meta-row"><span class="meta-label">{t['speaking_time']}</span><span class="meta-value" id="statSpeakingTime">0 sec</span></div>
          </div>
        </div>
        <p class="note">
          {t['note']}
        </p>
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
    title="Contador de palabras: palabras, caracteres, tiempo de lectura | norito",
    meta_desc="Cuenta palabras, caracteres, frases y párrafos en vivo mientras escribes, con tiempo estimado de lectura y de habla. No se sube nada.",
    app_name="Contador de palabras", h1="Contador de palabras", breadcrumb_label="Contador de palabras",
    lede="Recuento en vivo de palabras, caracteres, frases y párrafos mientras escribes, más el tiempo estimado de lectura y de habla.",
    t=dict(
        your_text="Tu texto", placeholder="Pega o escribe tu texto aquí...",
        stats="Estadísticas", words="Palabras", characters="Caracteres", sentences="Frases",
        paragraphs="Párrafos", reading_time="Tiempo de lectura", speaking_time="Tiempo de habla",
        note="El tiempo de lectura asume 225 palabras por minuto (velocidad media de lectura silenciosa de un adulto). El tiempo de habla asume 130 palabras por minuto (ritmo medio de una presentación oral).",
        how_h2="Cómo funciona",
        how_p1='En cada pulsación, el contador vuelve a derivar las seis estadísticas a partir del texto sin procesar. Las palabras son secuencias sin espacios en blanco, contadas dividiendo con la expresión regular <code>\\s+</code>; las frases son secuencias de texto que terminan en <code>.</code>, <code>!</code> o <code>?</code> seguidas de un espacio o del final del texto; los párrafos son bloques separados por líneas en blanco. El tiempo de lectura asume 225 palabras por minuto (un ritmo típico de lectura silenciosa) y el tiempo de habla asume 130, aproximadamente la velocidad de una charla de conferencia, ambos redondeados al segundo más cercano.',
        how_p2='Son aproximaciones honestas, y vale la pena saber dónde fallan. El recuento de frases no puede distinguir una abreviatura de un punto final, así que "El Sr. García llegó." cuenta como dos frases. El recuento de palabras también difiere legítimamente entre herramientas: esta cuenta "estado del arte" como tres palabras (sin espacios internos que las junten), mientras que algunos procesadores de texto cuentan los compuestos con guion de forma distinta, por eso tu redacción puede tener 998 palabras aquí y 1002 en otro sitio. Ninguna está equivocada; simplemente no coinciden en qué es un límite de palabra.',
        how_p3="El recuento de caracteres es la longitud sin procesar del texto, que incluye espacios y saltos de línea. Un matiz: las cadenas de JavaScript cuentan unidades UTF-16, así que la mayoría de los emojis cuentan como 2 caracteres y algunos (como los de familia o bandera) cuentan como más. Esto coincide con cómo se suelen aplicar los límites de plataformas al estilo Twitter, así que es el número útil de ver.",
        how_p4="Contar es un puñado de operaciones de expresiones regulares en tu pestaña. Nada de lo que escribes se transmite a ningún sitio: el panel Red de las herramientas de desarrollador permanece vacío mientras escribes, y el contador sigue funcionando con la conexión desactivada.",
    ),
    related_tools=[
        ("character-counter.html", "Contador de caracteres", "Compáralo con los límites de tuits, SMS y meta descripciones."),
        ("limited-text-generator.html", "Generador de texto limitado", "Genera texto de relleno con una longitud exacta."),
        ("/case-converter.html", "Conversor de mayúsculas/minúsculas", "Convierte texto entre mayúsculas, minúsculas, camelCase y más."),
    ],
)

PAGES["zh"] = dict(
    title="字数统计：单词、字符、阅读时间 | norito",
    meta_desc="输入即时统计单词数、字符数、句子数和段落数，并估算阅读和朗读所需时间。不会上传任何内容。",
    app_name="字数统计", h1="字数统计", breadcrumb_label="字数统计",
    lede="输入时实时统计单词数、字符数、句子数和段落数，并给出预计阅读和朗读时间。",
    t=dict(
        your_text="你的文本", placeholder="在此粘贴或输入文本…",
        stats="统计数据", words="单词数", characters="字符数", sentences="句子数",
        paragraphs="段落数", reading_time="阅读时间", speaking_time="朗读时间",
        note="阅读时间按每分钟 225 词计算（成年人默读的平均速度）。朗读时间按每分钟 130 词计算（口头演讲的平均语速）。",
        how_h2="工作原理",
        how_p1='每次按键时，计数器都会从原始文本重新推导全部六项统计数据。单词是由非空白字符组成的连续片段，通过正则表达式 <code>\\s+</code> 分割来统计；句子是以 <code>.</code>、<code>!</code> 或 <code>?</code> 结尾、后接空格或文本结束的连续片段；段落是由空行分隔的文本块。阅读时间按每分钟 225 词计算（典型的默读速度），朗读时间按每分钟 130 词计算（大致是会议演讲的语速），两者都四舍五入到最近的一秒。',
        how_p2='这些都是合理的近似值，了解它们在哪些地方会出现偏差也很有意义。句子统计无法区分缩写和句号，所以"Mr. Smith arrived."会被算作两个句子。不同工具的单词统计也存在合理的差异：本工具把"state-of-the-art"算作一个单词（内部没有空格），而有些文字处理软件对连字符复合词的处理方式不同，这就是为什么你的文章在这里是 998 词，在别处却是 1002 词。两者都没有错，只是对"单词边界"的定义不同。',
        how_p3="字符数是文本的原始长度，包含空格和换行符。有一点需要注意：JavaScript 字符串统计的是 UTF-16 单元，因此大多数表情符号会被算作 2 个字符，有些（如家庭或旗帜表情）会被算作更多。这与 Twitter 风格的平台限制通常的计算方式一致，因此这是一个很有参考价值的数字。",
        how_p4="统计工作只是在你的标签页里进行的几次正则表达式运算。你输入的任何内容都不会被发送到任何地方：书写时开发者工具的网络面板始终为空，即使断网，计数器依然可以正常工作。",
    ),
    related_tools=[
        ("character-counter.html", "字符计数器", "对照推文、短信和 meta 描述的限制。"),
        ("limited-text-generator.html", "限长文本生成器", "生成精确长度的占位文本。"),
        ("/case-converter.html", "大小写转换器", "在大写、小写、驼峰式等之间转换文本。"),
    ],
)

PAGES["ar"] = dict(
    title="عدّاد الكلمات: الكلمات والأحرف ووقت القراءة | norito",
    meta_desc="عُدّ الكلمات والأحرف والجمل والفقرات مباشرةً أثناء الكتابة، مع تقدير وقت القراءة والتحدث. لا يُرفع أي شيء.",
    app_name="عدّاد الكلمات", h1="عدّاد الكلمات", breadcrumb_label="عدّاد الكلمات",
    lede="عدّ فوري للكلمات والأحرف والجمل والفقرات أثناء الكتابة، بالإضافة إلى تقدير وقت القراءة والتحدث.",
    t=dict(
        your_text="نصّك", placeholder="الصق أو اكتب نصّك هنا...",
        stats="الإحصاءات", words="الكلمات", characters="الأحرف", sentences="الجمل",
        paragraphs="الفقرات", reading_time="وقت القراءة", speaking_time="وقت التحدث",
        note="يفترض وقت القراءة 225 كلمة في الدقيقة (متوسط شائع لسرعة القراءة الصامتة لدى البالغين). ويفترض وقت التحدث 130 كلمة في الدقيقة (متوسط سرعة العرض الشفهي).",
        how_h2="كيف يعمل",
        how_p1='مع كل ضغطة مفتاح، يعيد العدّاد اشتقاق الإحصاءات الست من النص الخام. الكلمات هي سلاسل خالية من المسافات البيضاء، تُحسب بالتقسيم باستخدام التعبير النمطي <code>\\s+</code>؛ والجمل هي سلاسل نصية تنتهي بـ <code>.</code> أو <code>!</code> أو <code>؟</code> تليها مسافة أو نهاية النص؛ والفقرات هي كتل مفصولة بأسطر فارغة. يفترض وقت القراءة 225 كلمة في الدقيقة (وتيرة قراءة صامتة نموذجية) ويفترض وقت التحدث 130، أي تقريبًا سرعة إلقاء محاضرة، وكلاهما مقرَّب لأقرب ثانية.',
        how_p2='هذه تقديرات صادقة، ويستحق الأمر معرفة أين تنحرف. لا يستطيع عدّ الجمل التمييز بين اختصار ونقطة نهاية، لذا فإن "وصل السيد. أحمد." يُحسب كجملتين. كذلك يختلف عدّ الكلمات بشكل مشروع بين الأدوات: هذه الأداة تعدّ "أحدث ما توصلت إليه" كسلسلة واحدة إذا لم تفصلها مسافات، بينما تتعامل بعض معالجات النصوص مع الكلمات المركّبة بشرطة بشكل مختلف، ولهذا يمكن أن يكون مقالك 998 كلمة هنا و1002 كلمة في مكان آخر. لا أحد منهما مخطئ؛ إنهما ببساطة يختلفان حول ما يُعدّ حدًّا للكلمة.',
        how_p3="عدّ الأحرف هو الطول الخام للنص، ويشمل المسافات وفواصل الأسطر. ملاحظة دقيقة: تعدّ سلاسل جافاسكريبت وحدات UTF-16، لذا تُحسب معظم الإيموجي كحرفين، بينما تُحسب بعضها (مثل إيموجي العائلة أو العلم) كأكثر من ذلك. يتطابق هذا مع الطريقة المعتادة لفرض حدود المنصات على غرار تويتر، لذا فهو رقم مفيد للمتابعة.",
        how_p4="العدّ هو مجرد مجموعة من عمليات التعبيرات النمطية داخل تبويبك. لا يُرسل أي شيء تكتبه إلى أي مكان: تبقى لوحة الشبكة في أدوات المطوّر فارغة أثناء الكتابة، ويستمر العدّاد في العمل حتى مع قطع الاتصال.",
    ),
    related_tools=[
        ("character-counter.html", "عدّاد الأحرف", "قارن مع حدود التغريدات والرسائل النصية وأوصاف الميتا."),
        ("limited-text-generator.html", "مولّد نص محدود الطول", "أنشئ نصًا نائبًا بطول دقيق."),
        ("/case-converter.html", "محوّل حالة الأحرف", "حوّل النص بين الأحرف الكبيرة والصغيرة وcamelCase والمزيد."),
    ],
)

PAGES["hi"] = dict(
    title="वर्ड काउंटर: शब्द, कैरेक्टर, पढ़ने का समय | norito",
    meta_desc="टाइप करते ही लाइव शब्द, कैरेक्टर, वाक्य और पैराग्राफ गिनें, अनुमानित पढ़ने और बोलने के समय के साथ। कुछ भी अपलोड नहीं होता।",
    app_name="वर्ड काउंटर", h1="वर्ड काउंटर", breadcrumb_label="वर्ड काउंटर",
    lede="टाइप करते समय लाइव शब्द, कैरेक्टर, वाक्य और पैराग्राफ काउंट, साथ ही अनुमानित पढ़ने और बोलने का समय।",
    t=dict(
        your_text="आपका टेक्स्ट", placeholder="यहाँ अपना टेक्स्ट पेस्ट या टाइप करें...",
        stats="आँकड़े", words="शब्द", characters="कैरेक्टर", sentences="वाक्य",
        paragraphs="पैराग्राफ", reading_time="पढ़ने का समय", speaking_time="बोलने का समय",
        note="पढ़ने का समय 225 शब्द प्रति मिनट (वयस्कों की औसत मौन पठन गति) मानकर निकाला जाता है। बोलने का समय 130 शब्द प्रति मिनट (औसत बोलचाल प्रेजेंटेशन गति) मानकर निकाला जाता है।",
        how_h2="यह कैसे काम करता है",
        how_p1='हर कीस्ट्रोक पर काउंटर रॉ टेक्स्ट से सभी छह आँकड़े फिर से निकालता है। शब्द व्हाइटस्पेस-रहित सीक्वेंस होते हैं, जिन्हें <code>\\s+</code> रेगेक्स पर स्प्लिट करके गिना जाता है; वाक्य वे टेक्स्ट सीक्वेंस हैं जो <code>.</code>, <code>!</code>, या <code>?</code> पर खत्म होते हैं और उसके बाद स्पेस या टेक्स्ट का अंत आता है; पैराग्राफ खाली लाइनों से अलग हुए हिस्से होते हैं। पढ़ने के समय में 225 शब्द प्रति मिनट (आम मौन पठन गति) माना जाता है और बोलने के समय में 130, यानी लगभग कॉन्फ़्रेंस-टॉक जैसी गति, दोनों को नज़दीकी सेकंड तक राउंड किया जाता है।',
        how_p2='ये ईमानदार अनुमान हैं, और यह जानना अच्छा है कि ये कहाँ चूक सकते हैं। वाक्य गिनती किसी संक्षिप्त रूप और पूर्ण विराम में फ़र्क नहीं कर सकती, इसलिए "श्री शर्मा आए।" को दो वाक्य गिना जाता है। टूल्स के बीच शब्द गिनती भी वाजिब तौर पर अलग होती है: यह टूल "state-of-the-art" को एक शब्द गिनता है (अंदर कोई स्पेस नहीं), जबकि कुछ वर्ड प्रोसेसर हाइफ़न वाले शब्दों को अलग तरह से गिनते हैं, इसलिए आपका निबंध यहाँ 998 शब्द का हो सकता है और कहीं और 1002 शब्द का। कोई भी गलत नहीं है; वे बस इस बात पर असहमत हैं कि शब्द की सीमा क्या है।',
        how_p3="कैरेक्टर काउंट टेक्स्ट की रॉ लंबाई है, जिसमें स्पेस और लाइन ब्रेक शामिल हैं। एक बारीकी: जावास्क्रिप्ट स्ट्रिंग्स UTF-16 यूनिट गिनती हैं, इसलिए ज़्यादातर इमोजी 2 कैरेक्टर गिने जाते हैं और कुछ (फ़ैमिली या फ़्लैग इमोजी) ज़्यादा गिने जाते हैं। यह इस बात से मेल खाता है कि ट्विटर-स्टाइल प्लेटफ़ॉर्म लिमिट आमतौर पर कैसे लागू होती हैं, इसलिए यह देखने लायक उपयोगी नंबर है।",
        how_p4="गिनती आपके टैब में चंद रेगेक्स ऑपरेशन भर है। आपका टाइप किया कुछ भी कहीं नहीं भेजा जाता: लिखते समय डेवलपर टूल्स का नेटवर्क पैनल खाली रहता है, और कनेक्शन बंद होने पर भी काउंटर काम करता रहता है।",
    ),
    related_tools=[
        ("character-counter.html", "कैरेक्टर काउंटर", "ट्वीट, SMS और मेटा डिस्क्रिप्शन लिमिट के हिसाब से जांचें।"),
        ("limited-text-generator.html", "लिमिटेड टेक्स्ट जनरेटर", "सटीक लंबाई का प्लेसहोल्डर टेक्स्ट जनरेट करें।"),
        ("/case-converter.html", "केस कन्वर्टर", "टेक्स्ट को अपरकेस, लोअरकेस, camelCase और अन्य में बदलें।"),
    ],
)

PAGES["ru"] = dict(
    title="Счётчик слов: слова, символы, время чтения | norito",
    meta_desc="Считайте слова, символы, предложения и абзацы в реальном времени по мере набора текста, с оценкой времени чтения и произнесения вслух. Ничего не загружается.",
    app_name="Счётчик слов", h1="Счётчик слов", breadcrumb_label="Счётчик слов",
    lede="Подсчёт слов, символов, предложений и абзацев в реальном времени по мере набора текста, плюс оценка времени чтения и произнесения вслух.",
    t=dict(
        your_text="Ваш текст", placeholder="Вставьте или введите текст здесь...",
        stats="Статистика", words="Слова", characters="Символы", sentences="Предложения",
        paragraphs="Абзацы", reading_time="Время чтения", speaking_time="Время произнесения",
        note="Время чтения рассчитывается исходя из 225 слов в минуту (часто упоминаемая средняя скорость молчаливого чтения у взрослых). Время произнесения рассчитывается исходя из 130 слов в минуту (средний темп устного выступления).",
        how_h2="Как это работает",
        how_p1='При каждом нажатии клавиши счётчик заново выводит все шесть показателей из исходного текста. Слова — это последовательности без пробельных символов, подсчитываемые разбиением по регулярному выражению <code>\\s+</code>; предложения — это фрагменты текста, заканчивающиеся на <code>.</code>, <code>!</code> или <code>?</code> и за которыми следует пробел или конец текста; абзацы — это блоки, разделённые пустыми строками. Время чтения рассчитывается исходя из 225 слов в минуту (типичный темп молчаливого чтения), а время произнесения — из 130, что примерно соответствует темпу доклада на конференции; оба значения округляются до ближайшей секунды.',
        how_p2='Это честные приближения, и стоит знать, где они дают сбой. Подсчёт предложений не может отличить сокращение от точки в конце предложения, поэтому "Г-н Смирнов пришёл." считается за два предложения. Подсчёт слов также законно различается между инструментами: этот инструмент считает "состояние-искусства" одним словом (внутри нет пробелов), в то время как некоторые текстовые редакторы считают составные слова через дефис иначе, поэтому ваше эссе может быть 998 слов здесь и 1002 слова в другом месте. Ни один из вариантов не ошибочен — они просто по-разному определяют границу слова.',
        how_p3="Количество символов — это необработанная длина текста, включающая пробелы и переносы строк. Один нюанс: строки JavaScript считают единицы UTF-16, поэтому большинство эмодзи считаются за 2 символа, а некоторые (например, семейные эмодзи или флаги) — за больше. Это соответствует тому, как обычно применяются лимиты платформ в стиле Twitter, поэтому это полезное число для отслеживания.",
        how_p4="Подсчёт — это всего лишь несколько операций с регулярными выражениями прямо в вашей вкладке. Ничто из набранного вами никуда не передаётся: панель «Сеть» в инструментах разработчика остаётся пустой во время письма, и счётчик продолжает работать даже при отключённом соединении.",
    ),
    related_tools=[
        ("character-counter.html", "Счётчик символов", "Сравните с лимитами твитов, SMS и мета-описаний."),
        ("limited-text-generator.html", "Генератор текста заданной длины", "Генерация текста-заполнителя точной длины."),
        ("/case-converter.html", "Конвертер регистра", "Преобразование текста между верхним, нижним регистром, camelCase и другими."),
    ],
)

PAGES["ja"] = dict(
    title="単語数カウンター：単語数・文字数・読了時間 | norito",
    meta_desc="入力と同時に単語数、文字数、文の数、段落数をカウントし、読了時間と話す時間の目安も表示。アップロードは一切行われません。",
    app_name="単語数カウンター", h1="単語数カウンター", breadcrumb_label="単語数カウンター",
    lede="入力中にリアルタイムで単語数、文字数、文数、段落数をカウントし、読了時間と話す時間の目安も表示します。",
    t=dict(
        your_text="テキスト", placeholder="ここにテキストを貼り付けるか入力...",
        stats="統計", words="単語数", characters="文字数", sentences="文数",
        paragraphs="段落数", reading_time="読了時間", speaking_time="話す時間",
        note="読了時間は毎分225語（成人の黙読の平均速度としてよく引用される値）を想定しています。話す時間は毎分130語（口頭発表の平均的なペース）を想定しています。",
        how_h2="仕組み",
        how_p1='キー入力のたびに、カウンターは元のテキストから6つの統計値をすべて再計算します。単語は空白を含まない連続文字列で、正規表現 <code>\\s+</code> で分割してカウントします。文は <code>.</code>、<code>!</code>、<code>?</code> のいずれかで終わり、その後にスペースまたはテキストの終端が続く連続文字列です。段落は空行で区切られたまとまりです。読了時間は毎分225語（典型的な黙読ペース）、話す時間は毎分130語（おおよそ講演のペース）を想定し、どちらも最も近い秒数に丸められます。',
        how_p2='これらは正直な近似値であり、どこで実態とずれるかを知っておく価値があります。文のカウントは略語と句点の区別ができないため、「Mr. Smith arrived.」は2文としてカウントされます。単語数も、ツールによって正当に異なります。このツールは「state-of-the-art」を（内部にスペースがないため）1語としてカウントしますが、ワープロソフトの中にはハイフン付きの複合語を別の方法で数えるものもあり、そのため同じ文章がここでは998語、別の場所では1002語になることがあります。どちらも間違いではなく、単に単語の境界の定義が異なるだけです。',
        how_p3="文字数はテキストの生の長さで、スペースや改行も含まれます。一つ注意点があります。JavaScriptの文字列はUTF-16単位でカウントするため、ほとんどの絵文字は2文字としてカウントされ、一部（家族や国旗の絵文字など）はさらに多くカウントされます。これはTwitterのようなプラットフォームの文字数制限が通常適用される方法と一致するため、確認する価値のある数値です。",
        how_p4="カウント処理はタブ内で行われるわずかな正規表現の演算にすぎません。入力した内容がどこかに送信されることはありません。書いている間、開発者ツールのネットワークパネルは空のままで、接続を切ってもカウンターは動作し続けます。",
    ),
    related_tools=[
        ("character-counter.html", "文字数カウンター", "ツイート、SMS、meta descriptionの上限と比較。"),
        ("limited-text-generator.html", "文字数制限テキストジェネレーター", "指定した長さぴったりのダミーテキストを生成。"),
        ("/case-converter.html", "大文字小文字変換ツール", "大文字、小文字、camelCaseなどの間でテキストを変換。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "word-counter.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-word-counter.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/word-counter.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
