#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m3 8 4-4 4 4"/><path d="M7 4v16"/><path d="M21 16h-6l6-8h-6"/></svg>'
ICON_CLASS = "c-amber"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field">
          <label for="textInput">{t['your_text']}</label>
          <textarea id="textInput" class="mono-output" rows="8" placeholder="{t['ph_text']}">{t['sample_text']}</textarea>
        </div>
        <div class="case-btn-grid">
          <button type="button" class="case-btn active" data-case="upper">UPPERCASE</button>
          <button type="button" class="case-btn" data-case="lower">lowercase</button>
          <button type="button" class="case-btn" data-case="title">{t['title_case']}</button>
          <button type="button" class="case-btn" data-case="sentence">{t['sentence_case']}</button>
          <button type="button" class="case-btn" data-case="camel">camelCase</button>
          <button type="button" class="case-btn" data-case="pascal">PascalCase</button>
          <button type="button" class="case-btn" data-case="snake">snake_case</button>
          <button type="button" class="case-btn" data-case="kebab">kebab-case</button>
          <button type="button" class="case-btn" data-case="constant">CONSTANT_CASE</button>
          <button type="button" class="case-btn" data-case="alternating">aLtErNaTiNg</button>
        </div>
      </div>

      <div>
        <div class="panel">
          <div class="field">
            <label for="textOutput">{t['result']}</label>
            <textarea id="textOutput" class="mono-output" rows="8" readonly></textarea>
          </div>
          <button id="copyBtn">{t['copy_result']}</button>
        </div>
        <p class="note">
          {t['side_note']}
        </p>
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
    title="Conversor de Mayúsculas/Minúsculas: UPPERCASE, camelCase | norito",
    meta_desc="Convierte texto entre MAYÚSCULAS, minúsculas, Formato Título, Formato oración, camelCase, PascalCase, snake_case, y kebab-case, en tu navegador.",
    app_name="Conversor de Mayúsculas/Minúsculas", h1="Conversor de Mayúsculas/Minúsculas", breadcrumb_label="Conversor de Mayúsculas/Minúsculas",
    lede="Convierte texto entre MAYÚSCULAS, minúsculas, Formato Título, Formato oración, camelCase, PascalCase, snake_case, kebab-case, y más, con un clic.",
    t=dict(
        your_text="Tu texto", ph_text="Escribe o pega texto aquí...",
        sample_text="el veloz murciélago hindú comía feliz cardillo y kiwi",
        title_case="Formato Título", sentence_case="Formato oración",
        result="Resultado", copy_result="Copiar resultado",
        side_note="camelCase, PascalCase, snake_case, kebab-case, y CONSTANT_CASE dividen primero tu texto en palabras (manejando espacios, puntuación, y límites de camelCase ya existentes), y luego las vuelven a unir en el estilo objetivo, así que convertir entre cualquiera de ellos funciona limpiamente en cualquier dirección.",
        how_h2="Cómo funciona",
        how_p1="Cada botón es una simple transformación de cadena en JavaScript que se vuelve a ejecutar en cada pulsación. MAYÚSCULAS y minúsculas son de una línea, pero los formatos de programador (camelCase, snake_case, kebab-case, PascalCase, CONSTANT_CASE) comparten primero un paso de división en palabras: una expresión regular inserta un límite donde una letra minúscula o dígito va seguido de una letra mayúscula, y luego el texto se divide en cualquier secuencia de caracteres no alfanuméricos. Una vez que la entrada es una lista limpia de palabras, volver a unirla en el estilo objetivo es trivial, por eso puedes ir de kebab-case a PascalCase a snake_case en cualquier orden sin que se acumule basura.",
        how_p2='Una peculiaridad que vale la pena conocer: las mayúsculas consecutivas se tratan como una sola palabra. El divisor solo rompe entre un carácter en minúscula y uno en mayúscula, así que <code>APIKey</code> se convierte en <code>apikey</code> en snake_case, no en <code>api_key</code>. Si tus identificadores contienen siglas, revisa esos puntos después de convertir. Formato Título es más inteligente que simplemente poner mayúscula a cada palabra: mantiene palabras menores como "un", "el", "de", y "en" en minúscula a menos que empiecen el texto, y Formato oración solo pone mayúscula después de <code>.</code>, <code>!</code>, o <code>?</code>.',
        how_p3="Todo esto ocurre dentro del JavaScript de la página, sin librerías y sin servidor. Abre la pestaña Red de las DevTools mientras escribes: no se envía nada, porque no hay nada a lo que enviarlo.",
    ),
    related_tools=[
        ("word-counter.html", "Contador de palabras", "Cuenta palabras, caracteres, y tiempo de lectura."),
        ("seo-slug-generator.html", "Generador de slugs SEO", "Convierte un título en un slug de URL limpio."),
        ("remove-duplicate-lines.html", "Eliminar líneas duplicadas", "Elimina duplicados antes o después de ordenar."),
    ],
)

PAGES["zh"] = dict(
    title="大小写转换器：大写、camelCase、snake_case | norito",
    meta_desc="在浏览器中直接转换文本格式，包括大写、小写、标题格式、句子格式、camelCase、PascalCase、snake_case 和 kebab-case。",
    app_name="大小写转换器", h1="大小写转换器", breadcrumb_label="大小写转换器",
    lede="一键在大写、小写、标题格式、句子格式、camelCase、PascalCase、snake_case、kebab-case 等格式之间转换文本。",
    t=dict(
        your_text="你的文本", ph_text="在此输入或粘贴文本...",
        sample_text="敏捷的棕色狐狸跳过了懒惰的狗",
        title_case="标题格式", sentence_case="句子格式",
        result="结果", copy_result="复制结果",
        side_note="camelCase、PascalCase、snake_case、kebab-case 和 CONSTANT_CASE 都会先把你的文本拆分成单词（处理空格、标点符号以及已有的 camelCase 边界），然后按目标格式重新拼接，因此在这些格式之间互相转换在任何方向上都能干净地完成。",
        how_h2="工作原理",
        how_p1="每个按钮都是一个纯 JavaScript 字符串转换函数，在每次按键时重新运行一次。大写和小写只需一行代码，但程序员常用的格式（camelCase、snake_case、kebab-case、PascalCase、CONSTANT_CASE）都共享一个先拆词的步骤：一个正则表达式会在小写字母或数字后紧跟大写字母的位置插入边界，然后文本会在任意一段非字母数字字符处被拆分。一旦输入变成了一份干净的单词列表，按目标风格重新拼接就变得非常简单，这就是为什么你可以按任意顺序在 kebab-case、PascalCase、snake_case 之间转换，而不会积累出垃圾结果。",
        how_p2='有一个值得了解的小细节：连续的大写字母会被当作一个单词处理。拆分逻辑只会在小写字符和大写字符之间断开，所以 <code>APIKey</code> 在 snake_case 中会变成 <code>apikey</code>，而不是 <code>api_key</code>。如果你的标识符中包含缩写词，转换后请检查这些位置。标题格式比简单地把每个单词首字母大写要更智能：除非位于文本开头，否则它会让 "a"、"the"、"of"、"in" 这类小词保持小写，而句子格式只在 <code>.</code>、<code>!</code>、<code>?</code> 之后才大写。',
        how_p3="这一切都发生在页面自身的 JavaScript 中，不依赖任何库，也没有服务器参与。输入时打开开发者工具的 Network 标签页：没有任何内容被发送，因为根本没有可以发送的目标。",
    ),
    related_tools=[
        ("word-counter.html", "字数统计", "统计单词数、字符数和阅读时间。"),
        ("seo-slug-generator.html", "SEO Slug 生成器", "把标题转换成简洁的网址 slug。"),
        ("remove-duplicate-lines.html", "删除重复行", "在排序前后对列表去重。"),
    ],
)

PAGES["ar"] = dict(
    title="محول حالة الأحرف: UPPERCASE، camelCase، snake_case | norito",
    meta_desc="حوّل النص بين الأحرف الكبيرة والصغيرة، Title Case، Sentence case، camelCase، PascalCase، snake_case، وkebab-case، مباشرة في متصفحك.",
    app_name="محول حالة الأحرف", h1="محول حالة الأحرف", breadcrumb_label="محول حالة الأحرف",
    lede="حوّل النص بين الأحرف الكبيرة والصغيرة، Title Case، Sentence case، camelCase، PascalCase، snake_case، kebab-case، والمزيد، بنقرة واحدة.",
    t=dict(
        your_text="نصك", ph_text="اكتب أو الصق نصًا هنا...",
        sample_text="الثعلب البني السريع يقفز فوق الكلب الكسول",
        title_case="Title Case", sentence_case="Sentence case",
        result="النتيجة", copy_result="نسخ النتيجة",
        side_note="camelCase وPascalCase وsnake_case وkebab-case وCONSTANT_CASE، كلها تقسّم نصك إلى كلمات أولًا (متعاملةً مع المسافات وعلامات الترقيم وحدود camelCase الموجودة)، ثم تعيد ضمّها بالنمط المستهدف، لذا يعمل التحويل بين أيٍّ منها بسلاسة في أي اتجاه.",
        how_h2="كيف يعمل",
        how_p1='كل زر هو تحويل سلسلة نصية بسيط في جافاسكريبت يُعاد تشغيله مع كل ضغطة مفتاح. الأحرف الكبيرة والصغيرة سطر واحد، لكن أنماط المبرمجين (camelCase وsnake_case وkebab-case وPascalCase وCONSTANT_CASE) تشترك جميعها أولًا في خطوة تقسيم إلى كلمات: تعبير نمطي يُدرج حدًا أينما تلي حرفًا صغيرًا أو رقمًا حرفٌ كبير، ثم يُقسَّم النص عند أي تسلسل من الأحرف غير الأبجدية الرقمية. بمجرد أن يصبح الإدخال قائمة كلمات نظيفة، تصبح إعادة الضمّ بالنمط المستهدف أمرًا بسيطًا، ولهذا يمكنك الانتقال من kebab-case إلى PascalCase إلى snake_case بأي ترتيب دون تراكم فوضى.',
        how_p2='أمر غريب يستحق المعرفة: الأحرف الكبيرة المتتالية تُعامَل ككلمة واحدة. يقسّم المقسّم فقط بين حرف صغير وحرف كبير، لذا يتحول <code>APIKey</code> إلى <code>apikey</code> في snake_case، وليس <code>api_key</code>. إذا كانت معرّفاتك تحتوي على اختصارات، تحقّق من تلك النقاط بعد التحويل. Title Case أذكى من مجرد تكبير حرف كل كلمة: يبقي الكلمات الثانوية مثل "a" و"the" و"of" و"in" صغيرة ما لم تبدأ النص، وSentence case يكبّر فقط بعد <code>.</code> أو <code>!</code> أو <code>?</code>.',
        how_p3="كل هذا يحدث داخل جافاسكريبت الصفحة، دون أي مكتبة ودون خادم. افتح لسان Network في أدوات المطوّر أثناء الكتابة: لا يُرسَل شيء، لأنه لا يوجد شيء لإرساله إليه.",
    ),
    related_tools=[
        ("word-counter.html", "عدّاد الكلمات", "عدّ الكلمات والأحرف ووقت القراءة."),
        ("seo-slug-generator.html", "مولّد روابط SEO", "حوّل عنوانًا إلى رابط نظيف."),
        ("remove-duplicate-lines.html", "إزالة الأسطر المكررة", "أزل التكرارات قبل الترتيب أو بعده."),
    ],
)

PAGES["hi"] = dict(
    title="केस कन्वर्टर: UPPERCASE, camelCase, snake_case | norito",
    meta_desc="अपने ब्राउज़र में ही UPPERCASE, lowercase, Title Case, Sentence case, camelCase, PascalCase, snake_case, और kebab-case के बीच टेक्स्ट कन्वर्ट करें।",
    app_name="केस कन्वर्टर", h1="केस कन्वर्टर", breadcrumb_label="केस कन्वर्टर",
    lede="एक क्लिक में UPPERCASE, lowercase, Title Case, Sentence case, camelCase, PascalCase, snake_case, kebab-case, और अधिक के बीच टेक्स्ट कन्वर्ट करें।",
    t=dict(
        your_text="आपका टेक्स्ट", ph_text="यहां टेक्स्ट टाइप या पेस्ट करें...",
        sample_text="तेज़ भूरी लोमड़ी आलसी कुत्ते के ऊपर से कूदती है",
        title_case="Title Case", sentence_case="Sentence case",
        result="परिणाम", copy_result="परिणाम कॉपी करें",
        side_note="camelCase, PascalCase, snake_case, kebab-case, और CONSTANT_CASE सभी पहले आपके टेक्स्ट को शब्दों में बांटते हैं (स्पेस, पंक्चुएशन, और मौजूदा camelCase बाउंड्रीज़ को हैंडल करते हुए), फिर उन्हें टारगेट स्टाइल में वापस जोड़ते हैं, इसलिए इनके बीच कन्वर्ट करना किसी भी दिशा में क्लीनली काम करता है।",
        how_h2="यह कैसे काम करता है",
        how_p1="हर बटन एक सादा JavaScript स्ट्रिंग ट्रांसफ़ॉर्म है जो हर कीस्ट्रोक पर दोबारा चलता है। UPPERCASE और lowercase वन-लाइनर हैं, लेकिन प्रोग्रामर केसेज़ (camelCase, snake_case, kebab-case, PascalCase, CONSTANT_CASE) सभी पहले एक वर्ड-स्प्लिटिंग स्टेप शेयर करते हैं: एक रेगेक्स हर जगह एक बाउंड्री डालता है जहां कोई लोअरकेस लेटर या डिजिट किसी अपरकेस लेटर के बाद आता है, फिर टेक्स्ट को किसी भी नॉन-अल्फ़ान्यूमेरिक कैरेक्टर्स की सीक्वेंस पर स्प्लिट किया जाता है। एक बार जब इनपुट एक क्लीन वर्ड लिस्ट बन जाता है, तो उसे टारगेट स्टाइल में वापस जोड़ना ट्रिवियल हो जाता है, इसीलिए आप बिना कोई कचरा जमा किए किसी भी क्रम में kebab-case से PascalCase से snake_case तक जा सकते हैं।",
        how_p2='एक बात जो जानने लायक है: लगातार आने वाले कैपिटल्स को एक ही शब्द माना जाता है। स्प्लिटर सिर्फ़ एक लोअरकेस कैरेक्टर और एक अपरकेस के बीच ब्रेक करता है, इसलिए <code>APIKey</code> snake_case में <code>apikey</code> बन जाता है, <code>api_key</code> नहीं। अगर आपके आइडेंटिफ़ायर्स में एक्रोनिम्स हैं, तो कन्वर्ट करने के बाद उन जगहों को चेक करें। Title Case एक सादे हर-शब्द-को-कैपिटलाइज़ करने से ज़्यादा स्मार्ट है: यह "a", "the", "of", और "in" जैसे माइनर शब्दों को लोअरकेस में रखता है जब तक कि वे टेक्स्ट शुरू न करें, और Sentence case सिर्फ़ <code>.</code>, <code>!</code>, या <code>?</code> के बाद कैपिटलाइज़ करता है।',
        how_p3="यह सब पेज के JavaScript के अंदर होता है, बिना किसी लाइब्रेरी और बिना किसी सर्वर के। टाइप करते समय डेवटूल्स का Network टैब खोलें: कुछ भी नहीं भेजा जाता, क्योंकि भेजने के लिए कुछ है ही नहीं।",
    ),
    related_tools=[
        ("word-counter.html", "वर्ड काउंटर", "वर्ड, कैरेक्टर, और पढ़ने का समय गिनें।"),
        ("seo-slug-generator.html", "SEO स्लग जनरेटर", "टाइटल को साफ़-सुथरे URL स्लग में बदलें."),
        ("remove-duplicate-lines.html", "डुप्लीकेट लाइनें हटाएं", "सॉर्ट करने से पहले या बाद में लिस्ट को डीडुप्लीकेट करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Конвертер регистра: UPPERCASE, camelCase, snake_case | norito",
    meta_desc="Конвертируйте текст между ВЕРХНИМ регистром, нижним регистром, Title Case, Sentence case, camelCase, PascalCase, snake_case и kebab-case прямо в браузере.",
    app_name="Конвертер регистра", h1="Конвертер регистра", breadcrumb_label="Конвертер регистра",
    lede="Конвертируйте текст между ВЕРХНИМ регистром, нижним регистром, Title Case, Sentence case, camelCase, PascalCase, snake_case, kebab-case и другими в один клик.",
    t=dict(
        your_text="Ваш текст", ph_text="Введите или вставьте текст здесь...",
        sample_text="быстрая бурая лиса перепрыгивает через ленивую собаку",
        title_case="Title Case", sentence_case="Sentence case",
        result="Результат", copy_result="Скопировать результат",
        side_note="camelCase, PascalCase, snake_case, kebab-case и CONSTANT_CASE сначала разбивают ваш текст на слова (обрабатывая пробелы, пунктуацию и существующие границы camelCase), а затем собирают их заново в целевом стиле, поэтому конвертация между любыми из них работает корректно в любом направлении.",
        how_h2="Как это работает",
        how_p1="Каждая кнопка — это простое преобразование строки в JavaScript, которое заново запускается при каждом нажатии клавиши. ВЕРХНИЙ и нижний регистр — это однострочники, но программистские регистры (camelCase, snake_case, kebab-case, PascalCase, CONSTANT_CASE) сначала проходят общий этап разбивки на слова: регулярное выражение вставляет границу везде, где за строчной буквой или цифрой следует заглавная буква, а затем текст разбивается по любой последовательности небуквенно-цифровых символов. Как только ввод превращается в чистый список слов, повторная сборка в целевом стиле становится тривиальной задачей, поэтому вы можете переходить от kebab-case к PascalCase к snake_case в любом порядке без накопления мусора.",
        how_p2='Одна особенность, которую стоит знать: последовательные заглавные буквы считаются одним словом. Разделитель разрывает только между строчным и заглавным символом, поэтому <code>APIKey</code> становится <code>apikey</code> в snake_case, а не <code>api_key</code>. Если ваши идентификаторы содержат аббревиатуры, проверьте эти места после конвертации. Title Case умнее простого капитализации каждого слова: он оставляет второстепенные слова вроде "a", "the", "of" и "in" в нижнем регистре, если только они не начинают текст, а Sentence case делает заглавной букву только после <code>.</code>, <code>!</code> или <code>?</code>.',
        how_p3="Всё это происходит внутри JavaScript страницы, без каких-либо библиотек и без сервера. Откройте вкладку Network в DevTools во время ввода: ничего не отправляется, потому что отправлять просто некуда.",
    ),
    related_tools=[
        ("word-counter.html", "Счётчик слов", "Подсчёт слов, символов и времени чтения."),
        ("seo-slug-generator.html", "Генератор SEO-слагов", "Превратите заголовок в чистый URL-слаг."),
        ("remove-duplicate-lines.html", "Удаление дублирующихся строк", "Удаление дубликатов до или после сортировки."),
    ],
)

PAGES["ja"] = dict(
    title="大文字小文字変換ツール：UPPERCASE、camelCase、snake_case | norito",
    meta_desc="ブラウザ内でUPPERCASE、lowercase、Title Case、Sentence case、camelCase、PascalCase、snake_case、kebab-caseの間でテキストを変換します。",
    app_name="大文字小文字変換ツール", h1="大文字小文字変換ツール", breadcrumb_label="大文字小文字変換ツール",
    lede="ワンクリックでUPPERCASE、lowercase、Title Case、Sentence case、camelCase、PascalCase、snake_case、kebab-caseなどの間でテキストを変換します。",
    t=dict(
        your_text="あなたのテキスト", ph_text="ここにテキストを入力または貼り付け...",
        sample_text="素早い茶色のキツネが怠け者の犬を飛び越える",
        title_case="Title Case", sentence_case="Sentence case",
        result="結果", copy_result="結果をコピー",
        side_note="camelCase、PascalCase、snake_case、kebab-case、CONSTANT_CASEはすべて、まずテキストを単語に分割し（スペース、句読点、既存のcamelCase境界を処理）、次にターゲットのスタイルで再結合します。そのため、これらの形式間の変換はどの方向でもきれいに機能します。",
        how_h2="仕組み",
        how_p1="各ボタンは、キー入力のたびに再実行される単純なJavaScriptの文字列変換です。UPPERCASEとlowercaseは1行で済みますが、プログラマー向けの形式（camelCase、snake_case、kebab-case、PascalCase、CONSTANT_CASE）はすべて、まず単語分割のステップを共有します。正規表現が小文字または数字の後に大文字が続く箇所に境界を挿入し、次にテキストが英数字以外の文字の連続部分で分割されます。入力がきれいな単語リストになれば、ターゲットのスタイルで再結合するのは簡単な作業です。だからこそ、kebab-caseからPascalCase、snake_caseへとどの順序でもゴミが蓄積することなく変換できます。",
        how_p2='知っておく価値のある癖が一つあります。連続する大文字は1つの単語として扱われます。分割処理は小文字と大文字の間でのみ区切るため、<code>APIKey</code>はsnake_caseで<code>api_key</code>ではなく<code>apikey</code>になります。識別子に略語が含まれる場合は、変換後にその部分を確認してください。Title Caseは単純にすべての単語の先頭を大文字にするより賢く、テキストの先頭でない限り"a"、"the"、"of"、"in"のような小さな単語は小文字のままにします。Sentence caseは<code>.</code>、<code>!</code>、<code>?</code>の後にのみ大文字にします。',
        how_p3="これらはすべてページのJavaScript内で行われ、ライブラリもサーバーも使いません。入力中にDevToolsのNetworkタブを開いてみてください。何も送信されません。送信先が何もないからです。",
    ),
    related_tools=[
        ("word-counter.html", "単語数カウンター", "単語数、文字数、読了時間をカウント。"),
        ("seo-slug-generator.html", "SEOスラッグジェネレーター", "タイトルをクリーンなURLスラッグに変換します。"),
        ("remove-duplicate-lines.html", "重複行の削除", "並べ替えの前後でリストの重複を削除。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "case-converter.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-case-converter.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/case-converter.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
