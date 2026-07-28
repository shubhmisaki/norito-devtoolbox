#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg>'
ICON_CLASS = "c-pink"
REGEN_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 12a9 9 0 1 1-2.64-6.36"/><path d="M21 3v6h-6"/></svg>'

def body(t):
    return f'''
    <div class="panel">
      <div class="two-col" style="margin-bottom:16px;">
        <div class="field">
          <label for="unit">{t['generate']}</label>
          <select id="unit">
            <option value="paragraphs" selected>{t['paragraphs']}</option>
            <option value="sentences">{t['sentences']}</option>
            <option value="words">{t['words']}</option>
          </select>
        </div>
        <div class="field">
          <label for="count">{t['how_many']}</label>
          <input type="number" id="count" min="1" max="500" value="3" />
        </div>
      </div>

      <div style="display:flex; gap:16px; flex-wrap:wrap; margin-bottom:16px;">
        <label class="option-row" style="flex:0 0 auto;">
          <input type="checkbox" id="startClassic" checked />
          <span>{t['start_classic']}</span>
        </label>
        <label class="option-row" style="flex:0 0 auto;">
          <input type="checkbox" id="asHtml" />
          <span>{t['wrap_p']}</span>
        </label>
      </div>

      <div class="field" style="margin-bottom:16px;">
        <label for="output">{t['output']}</label>
        <textarea id="output" class="mono-area" rows="14" readonly></textarea>
      </div>

      <div style="display:flex; gap:10px;">
        <button id="regenBtn" class="secondary">
          {REGEN_ICON}
          {t['regenerate']}
        </button>
        <button id="copyBtn">{t['copy_text']}</button>
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
    title="Generador de Lorem Ipsum: texto de relleno online | norito",
    meta_desc="Genera texto de relleno lorem ipsum por palabras, frases o párrafos, con etiquetas HTML opcionales. Gratis, instantáneo, funciona en tu navegador.",
    app_name="Generador de Lorem Ipsum", h1="Generador de Lorem Ipsum", breadcrumb_label="Generador de Lorem Ipsum",
    lede="Genera el clásico texto de relleno lorem ipsum por palabras, frases o párrafos, listo para pegar en un diseño o maqueta.",
    t=dict(
        generate="Generar", paragraphs="Párrafos", sentences="Frases", words="Palabras", how_many="Cuántos",
        start_classic='Empezar con "Lorem ipsum dolor sit amet..."', wrap_p="Envolver párrafos en etiquetas &lt;p&gt;",
        output="Salida", regenerate="Regenerar", copy_text="Copiar texto",
        how_h2="Cómo funciona",
        how_p1='El generador mantiene un conjunto de unas 110 palabras latinas clásicas de relleno y las combina con <code>Math.random()</code>: cada frase recibe una longitud aleatoria de entre 6 y 14 palabras, las frases de más de 6 palabras reciben una coma colocada en algún punto intermedio, y cada párrafo se construye con 4 a 7 frases. Ese truco de la coma importa más de lo que parece: un texto sin ninguna variación de puntuación se ve claramente falso en un diseño, mientras que un poco de ritmo hace que el bloque se lea como prosa real a primera vista. Si mantienes activada la opción "Empezar con Lorem ipsum dolor sit amet", la primera frase queda fijada a la apertura tradicional, de modo que la salida se reconoce al instante como texto de relleno.',
        how_p2="Todo es concatenación de cadenas en JavaScript, ejecutándose en tu pestaña. No se obtiene nada ni se envía nada: abre las herramientas de desarrollador, observa el panel Red, y haz clic en Regenerar tantas veces como quieras. No se dispara ninguna petición, y la herramienta sigue funcionando con el Wi-Fi apagado.",
        how_p3='Algo que la mayoría de los generadores no te cuenta: como las longitudes de las palabras son aleatorias, dos ejecuciones de "3 párrafos" pueden diferir en docenas de caracteres. Eso está bien para calcular a ojo un diseño, pero es inútil para probar un límite estricto de caracteres (una columna de base de datos, una meta descripción, un tuit). Para eso, genera aquí por cantidad exacta de palabras, o usa en su lugar una herramienta de relleno de longitud fija. Y si estás pegando en plantillas HTML, la opción "Envolver párrafos en etiquetas &lt;p&gt;" te ahorra envolver cada bloque a mano.',
    ),
    related_tools=[
        ("limited-text-generator.html", "Generador de texto limitado", "Texto de relleno, longitud exacta."),
        ("word-counter.html", "Contador de palabras", "Recuento en vivo de palabras, frases y párrafos."),
        ("character-counter.html", "Contador de caracteres", "Recuento de caracteres, con límites de plataformas."),
    ],
)

PAGES["zh"] = dict(
    title="Lorem Ipsum 生成器：在线占位文本 | norito",
    meta_desc="按单词、句子或段落生成 Lorem Ipsum 占位文本，可选包裹 HTML 标签。免费、即时，运行在你的浏览器中。",
    app_name="Lorem Ipsum 生成器", h1="Lorem Ipsum 生成器", breadcrumb_label="Lorem Ipsum 生成器",
    lede="按单词、句子或段落生成经典的 Lorem Ipsum 占位文本，可直接粘贴到设计稿或原型中使用。",
    t=dict(
        generate="生成", paragraphs="段落", sentences="句子", words="单词", how_many="数量",
        start_classic='以 "Lorem ipsum dolor sit amet..." 开头', wrap_p="用 &lt;p&gt; 标签包裹段落",
        output="输出", regenerate="重新生成", copy_text="复制文本",
        how_h2="工作原理",
        how_p1='生成器维护着一个约 110 个经典拉丁占位单词的词库，并用 <code>Math.random()</code> 组合它们：每个句子随机取 6 到 14 个单词的长度，超过 6 个单词的句子会在中间某处随机插入一个逗号，每个段落由 4 到 7 个句子构成。这个逗号技巧比听起来更重要：完全没有标点变化的文本在排版中会显得明显不真实，而适度的节奏感能让这段文字乍看之下更像真实的文章。如果保持"以 Lorem ipsum dolor sit amet 开头"选项开启，第一句会固定为传统的开场白，让输出内容一眼就能被认出是占位文本。',
        how_p2="整个过程只是运行在你标签页里的 JavaScript 字符串拼接。不会获取任何内容，也不会发送任何内容：打开开发者工具，观察网络面板，随意点击「重新生成」多少次都可以。不会触发任何请求，即使关掉 Wi-Fi，这个工具依然能正常工作。",
        how_p3='多数生成器不会告诉你的一点是：由于单词长度是随机的，两次生成"3 段"的结果可能相差数十个字符。这对目测排版效果没问题，但对测试严格的字符限制（数据库列、meta 描述、推文）就没什么用了。对于这种需求，可以在这里按精确单词数生成，或改用固定长度的占位文本工具。如果你要粘贴到 HTML 模板里，"用 &lt;p&gt; 标签包裹段落"这个选项能省去你手动包裹每一段的麻烦。',
    ),
    related_tools=[
        ("limited-text-generator.html", "限长文本生成器", "精确长度的占位文本。"),
        ("word-counter.html", "字数统计", "实时统计单词数、句子数和段落数。"),
        ("character-counter.html", "字符计数器", "字符统计，附平台限制对照。"),
    ],
)

PAGES["ar"] = dict(
    title="مولّد Lorem Ipsum: نص نائب أونلاين | norito",
    meta_desc="أنشئ نص Lorem Ipsum النائب حسب الكلمات أو الجمل أو الفقرات، مع وسوم HTML اختيارية. مجاني وفوري ويعمل في متصفحك.",
    app_name="مولّد Lorem Ipsum", h1="مولّد Lorem Ipsum", breadcrumb_label="مولّد Lorem Ipsum",
    lede="أنشئ نص Lorem Ipsum النائب الكلاسيكي حسب الكلمات أو الجمل أو الفقرات، جاهزًا للصق في تصميم أو نموذج أولي.",
    t=dict(
        generate="إنشاء", paragraphs="فقرات", sentences="جمل", words="كلمات", how_many="العدد",
        start_classic='ابدأ بـ "Lorem ipsum dolor sit amet..."', wrap_p="لفّ الفقرات بوسوم &lt;p&gt;",
        output="الإخراج", regenerate="إعادة الإنشاء", copy_text="نسخ النص",
        how_h2="كيف يعمل",
        how_p1='يحتفظ المولّد بمجموعة من حوالي 110 كلمة لاتينية نائبة كلاسيكية ويجمعها باستخدام <code>Math.random()</code>: تحصل كل جملة على طول عشوائي بين 6 و14 كلمة، والجمل الأطول من 6 كلمات تحصل على فاصلة تُوضع في مكان ما في المنتصف، وتُبنى كل فقرة من 4 إلى 7 جمل. حيلة الفاصلة هذه أهم مما تبدو عليه: النص الخالي تمامًا من أي تنوع في علامات الترقيم يبدو مزيفًا بوضوح في التخطيط، بينما القليل من الإيقاع يجعل الكتلة تُقرأ كنثر حقيقي للوهلة الأولى. إذا أبقيت خيار "ابدأ بـ Lorem ipsum dolor sit amet" مفعّلًا، تُثبَّت الجملة الأولى على الافتتاحية التقليدية بحيث يُتعرَّف على الناتج فورًا كنص نائب.',
        how_p2="كل شيء هنا هو مجرد ضم سلاسل نصية في جافاسكريبت، يعمل داخل تبويبك. لا يُجلب شيء ولا يُرسل شيء: افتح أدوات المطوّر، راقب لوحة الشبكة، وانقر على «إعادة الإنشاء» بقدر ما تشاء. لا تُطلق أي طلبات، وتستمر الأداة في العمل حتى مع إيقاف تشغيل Wi-Fi.",
        how_p3='أمر لا تخبرك به معظم المولّدات: نظرًا لأن أطوال الكلمات عشوائية، يمكن أن يختلف تشغيلان لـ"3 فقرات" بعشرات الأحرف. هذا جيد لتقدير التخطيط بالعين، لكنه عديم الفائدة لاختبار حد أحرف صارم (عمود قاعدة بيانات، وصف ميتا، تغريدة). لذلك، أنشئ هنا حسب عدد كلمات دقيق، أو استخدم أداة نص نائب بطول ثابت بدلًا من ذلك. وإذا كنت تلصق في قوالب HTML، فإن خيار "لفّ الفقرات بوسوم &lt;p&gt;" يوفّر عليك لفّ كل كتلة يدويًا.',
    ),
    related_tools=[
        ("limited-text-generator.html", "مولّد نص محدود الطول", "نص نائب، طول دقيق."),
        ("word-counter.html", "عدّاد الكلمات", "عدّ فوري للكلمات والجمل والفقرات."),
        ("character-counter.html", "عدّاد الأحرف", "عدّ الأحرف، مع حدود المنصات."),
    ],
)

PAGES["hi"] = dict(
    title="Lorem Ipsum जनरेटर: प्लेसहोल्डर टेक्स्ट ऑनलाइन | norito",
    meta_desc="वर्ड, वाक्य, या पैराग्राफ के हिसाब से Lorem Ipsum प्लेसहोल्डर टेक्स्ट जनरेट करें, वैकल्पिक HTML टैग के साथ। मुफ़्त, तुरंत, आपके ब्राउज़र में चलता है।",
    app_name="Lorem Ipsum जनरेटर", h1="Lorem Ipsum जनरेटर", breadcrumb_label="Lorem Ipsum जनरेटर",
    lede="वर्ड, वाक्य, या पैराग्राफ के हिसाब से क्लासिक Lorem Ipsum प्लेसहोल्डर टेक्स्ट जनरेट करें, किसी डिज़ाइन या मॉकअप में पेस्ट करने के लिए तैयार।",
    t=dict(
        generate="जनरेट करें", paragraphs="पैराग्राफ", sentences="वाक्य", words="वर्ड", how_many="कितने",
        start_classic='"Lorem ipsum dolor sit amet..." से शुरू करें', wrap_p="पैराग्राफ को &lt;p&gt; टैग में रैप करें",
        output="आउटपुट", regenerate="फिर से जनरेट करें", copy_text="टेक्स्ट कॉपी करें",
        how_h2="यह कैसे काम करता है",
        how_p1='जनरेटर लगभग 110 क्लासिक लैटिन प्लेसहोल्डर शब्दों का एक पूल रखता है और उन्हें <code>Math.random()</code> से जोड़ता है: हर वाक्य को 6 से 14 शब्दों के बीच रैंडम लंबाई मिलती है, 6 शब्दों से लंबे वाक्यों के बीच कहीं एक कॉमा डाल दिया जाता है, और हर पैराग्राफ 4 से 7 वाक्यों से बनता है। यह कॉमा वाली तरकीब उससे ज़्यादा मायने रखती है जितनी लगती है: जीरो पंक्चुएशन वैरिएशन वाला टेक्स्ट किसी लेआउट में साफ़ नकली दिखता है, जबकि थोड़ी सी रिदम ब्लॉक को एक नज़र में असली गद्य जैसा बना देती है। अगर आप "Lorem ipsum dolor sit amet से शुरू करें" ऑप्शन ऑन रखते हैं, तो पहला वाक्य पारंपरिक ओपनर पर फ़िक्स रहता है ताकि आउटपुट तुरंत प्लेसहोल्डर टेक्स्ट के रूप में पहचाना जा सके।',
        how_p2="सब कुछ आपके टैब में चलने वाली जावास्क्रिप्ट में सिंपल स्ट्रिंग कॉन्कैटिनेशन है। कुछ भी फ़ेच नहीं होता और कुछ भी नहीं भेजा जाता: डेवलपर टूल्स खोलें, नेटवर्क पैनल देखें, और जितनी बार चाहें Regenerate पर क्लिक करें। कोई रिक्वेस्ट फ़ायर नहीं होती, और Wi-Fi बंद होने पर भी टूल काम करता रहता है।",
        how_p3='एक बात जो ज़्यादातर जनरेटर आपको नहीं बताते: चूंकि वर्ड की लंबाई रैंडम होती है, "3 पैराग्राफ" के दो रन दर्जनों कैरेक्टर से अलग हो सकते हैं। यह लेआउट को आंख से जांचने के लिए ठीक है, लेकिन किसी सख़्त कैरेक्टर लिमिट (डेटाबेस कॉलम, मेटा डिस्क्रिप्शन, ट्वीट) को टेस्ट करने के लिए बेकार है। इसके लिए, यहाँ सटीक वर्ड काउंट के हिसाब से जनरेट करें, या इसकी बजाय एक फ़िक्स्ड-लेंथ प्लेसहोल्डर टूल इस्तेमाल करें। और अगर आप HTML टेम्पलेट्स में पेस्ट कर रहे हैं, तो "पैराग्राफ को &lt;p&gt; टैग में रैप करें" ऑप्शन आपको हर ब्लॉक हाथ से रैप करने से बचाता है।',
    ),
    related_tools=[
        ("limited-text-generator.html", "लिमिटेड टेक्स्ट जनरेटर", "प्लेसहोल्डर टेक्स्ट, सटीक लंबाई।"),
        ("word-counter.html", "वर्ड काउंटर", "लाइव वर्ड, वाक्य, और पैराग्राफ काउंट।"),
        ("character-counter.html", "कैरेक्टर काउंटर", "कैरेक्टर काउंट, प्लेटफ़ॉर्म लिमिट के साथ।"),
    ],
)

PAGES["ru"] = dict(
    title="Генератор Lorem Ipsum: текст-заполнитель онлайн | norito",
    meta_desc="Генерируйте текст-заполнитель lorem ipsum по словам, предложениям или абзацам, с опциональными HTML-тегами. Бесплатно, мгновенно, работает в браузере.",
    app_name="Генератор Lorem Ipsum", h1="Генератор Lorem Ipsum", breadcrumb_label="Генератор Lorem Ipsum",
    lede="Генерируйте классический текст-заполнитель lorem ipsum по словам, предложениям или абзацам, готовый для вставки в дизайн или макет.",
    t=dict(
        generate="Сгенерировать", paragraphs="Абзацы", sentences="Предложения", words="Слова", how_many="Сколько",
        start_classic='Начинать с «Lorem ipsum dolor sit amet...»', wrap_p="Оборачивать абзацы в теги &lt;p&gt;",
        output="Вывод", regenerate="Сгенерировать заново", copy_text="Скопировать текст",
        how_h2="Как это работает",
        how_p1='Генератор хранит пул примерно из 110 классических латинских слов-заполнителей и собирает их с помощью <code>Math.random()</code>: каждому предложению присваивается случайная длина от 6 до 14 слов, в предложения длиннее 6 слов где-то в середине добавляется запятая, а каждый абзац строится из 4–7 предложений. Этот приём с запятой важнее, чем кажется: текст без вариаций пунктуации выглядит явно ненастоящим в макете, а лёгкий ритм заставляет блок читаться как настоящая проза на первый взгляд. Если оставить опцию «Начинать с Lorem ipsum dolor sit amet» включённой, первое предложение закрепляется за традиционным зачином, поэтому вывод сразу узнаётся как текст-заполнитель.',
        how_p2="Всё сводится к обычной конкатинации строк в JavaScript, выполняемой в вашей вкладке. Ничего не запрашивается и ничего не отправляется: откройте инструменты разработчика, следите за панелью «Сеть» и нажимайте «Сгенерировать заново» сколько угодно раз. Ни один запрос не отправляется, и инструмент продолжает работать при выключенном Wi-Fi.",
        how_p3='Вот что не рассказывает большинство генераторов: поскольку длина слов случайна, два запуска «3 абзацев» могут отличаться на десятки символов. Это нормально для визуальной оценки макета, но бесполезно для проверки строгого ограничения по символам (столбец базы данных, мета-описание, твит). Для этого генерируйте здесь по точному количеству слов или используйте вместо этого инструмент заполнителя фиксированной длины. А если вы вставляете текст в HTML-шаблоны, опция «Оборачивать абзацы в теги &lt;p&gt;» избавит вас от необходимости оборачивать каждый блок вручную.',
    ),
    related_tools=[
        ("limited-text-generator.html", "Генератор текста заданной длины", "Текст-заполнитель точной длины."),
        ("word-counter.html", "Счётчик слов", "Подсчёт слов, предложений и абзацев в реальном времени."),
        ("character-counter.html", "Счётчик символов", "Подсчёт символов с учётом лимитов платформ."),
    ],
)

PAGES["ja"] = dict(
    title="Lorem Ipsumジェネレーター：ダミーテキストをオンライン生成 | norito",
    meta_desc="単語数、文数、段落数を指定してLorem Ipsumダミーテキストを生成。HTMLタグの付与も選択可。無料、即座に、ブラウザ内で動作します。",
    app_name="Lorem Ipsumジェネレーター", h1="Lorem Ipsumジェネレーター", breadcrumb_label="Lorem Ipsumジェネレーター",
    lede="単語、文、段落単位で定番のLorem Ipsumダミーテキストを生成し、デザインやモックアップにそのまま貼り付けられます。",
    t=dict(
        generate="生成", paragraphs="段落", sentences="文", words="単語", how_many="件数",
        start_classic='「Lorem ipsum dolor sit amet...」で始める', wrap_p="段落を &lt;p&gt; タグで囲む",
        output="出力", regenerate="再生成", copy_text="テキストをコピー",
        how_h2="仕組み",
        how_p1='ジェネレーターは約110語の古典的なラテン語のダミー単語プールを保持し、<code>Math.random()</code> でそれらを組み合わせます。各文は6〜14語のランダムな長さになり、6語を超える文には中間のどこかにカンマが挿入され、各段落は4〜7文で構成されます。このカンマの工夫は見た目以上に重要です。句読点にまったく変化がないテキストはレイアウト上で明らかに偽物っぽく見えますが、少しリズムを加えるだけで、ひと目で本物の文章のように読めるようになります。「Lorem ipsum dolor sit ametで始める」オプションをオンにしておくと、最初の文が伝統的な書き出しに固定されるため、出力が即座にダミーテキストだとわかります。',
        how_p2="処理はすべてタブ内で実行される単純なJavaScriptの文字列結合です。何も取得されず、何も送信されません。開発者ツールを開いてネットワークパネルを監視しながら、「再生成」を好きなだけクリックしてみてください。リクエストは一切発生せず、Wi-Fiをオフにしてもツールは動作し続けます。",
        how_p3='多くのジェネレーターが教えてくれないことがあります。単語の長さがランダムなので、「3段落」を2回実行しても、文字数が数十文字違うことがあります。レイアウトを目視で確認する分には問題ありませんが、厳密な文字数制限（データベースの列、meta description、ツイートなど）をテストするには使えません。そのような用途には、正確な単語数を指定してここで生成するか、固定長のダミーテキストツールを使ってください。HTMLテンプレートに貼り付ける場合は、「段落を&lt;p&gt;タグで囲む」オプションを使えば、各ブロックを手動で囲む手間が省けます。',
    ),
    related_tools=[
        ("limited-text-generator.html", "文字数制限テキストジェネレーター", "ダミーテキスト、正確な長さ。"),
        ("word-counter.html", "単語数カウンター", "単語数、文数、段落数をリアルタイムでカウント。"),
        ("character-counter.html", "文字数カウンター", "文字数カウント、プラットフォームの上限付き。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "lorem-ipsum-generator.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-lorem-ipsum.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/lorem-ipsum-generator.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
