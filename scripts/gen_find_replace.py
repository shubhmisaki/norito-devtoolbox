#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>'
ICON_CLASS = "c-teal"

def body(t):
    return f'''
    <div class="panel">
      <div class="field" style="margin-bottom:16px;">
        <label for="input">{t['text']}</label>
        <textarea id="input" class="mono-area" rows="10" placeholder="{t['ph_text']}"></textarea>
      </div>

      <div class="two-col" style="margin-bottom:16px;">
        <div class="field">
          <label for="findText">{t['find']}</label>
          <input type="text" id="findText" class="mono-area" placeholder="{t['ph_find']}" />
        </div>
        <div class="field">
          <label for="replaceText">{t['replace_with']}</label>
          <input type="text" id="replaceText" class="mono-area" placeholder="{t['ph_replace']}" />
        </div>
      </div>

      <div style="display:flex; gap:16px; flex-wrap:wrap; margin-bottom:16px;">
        <label class="option-row" style="flex:0 0 auto;">
          <input type="checkbox" id="useRegex" />
          <span>{t['use_regex']}</span>
        </label>
        <label class="option-row" style="flex:0 0 auto;">
          <input type="checkbox" id="caseSensitive" />
          <span>{t['case_sensitive']}</span>
        </label>
        <label class="option-row" style="flex:0 0 auto;">
          <input type="checkbox" id="wholeWord" />
          <span>{t['whole_word']}</span>
        </label>
        <label class="option-row" style="flex:0 0 auto;">
          <input type="checkbox" id="replaceAll" checked />
          <span>{t['replace_all']}</span>
        </label>
      </div>

      <div class="result-box error" id="errorBox" style="display:none; margin-bottom:16px;">
        <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
        <div class="r-body"></div>
      </div>

      <div class="field" style="margin-bottom:8px;">
        <label for="output">{t['result']} <span id="matchCount" class="note" style="display:inline; margin-left:8px;"></span></label>
        <textarea id="output" class="mono-area" rows="10" readonly></textarea>
      </div>

      <div style="margin-top:16px;">
        <button id="copyBtn">{t['copy_result']}</button>
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
    title="Buscar y Reemplazar Texto Online (con Regex) | norito",
    meta_desc="Busca y reemplaza texto con regex opcional, sensibilidad a mayúsculas, y coincidencia de palabra completa, en vivo en tu navegador. No se sube nada.",
    app_name="Buscar y Reemplazar", h1="Buscar y Reemplazar", breadcrumb_label="Buscar y Reemplazar",
    lede="Busca y reemplaza texto en un documento, con regex opcional, sensibilidad a mayúsculas, y coincidencia de palabra completa, en vivo mientras escribes.",
    t=dict(
        text="Texto", ph_text="Pega o escribe tu texto...",
        find="Buscar", ph_find="texto o patrón a buscar",
        replace_with="Reemplazar con", ph_replace="texto de reemplazo",
        use_regex="Usar regex", case_sensitive="Sensible a mayúsculas", whole_word="Solo palabra completa",
        replace_all="Reemplazar todas las coincidencias",
        result="Resultado", copy_result="Copiar resultado",
        how_h2="Cómo funciona",
        how_p1='Cada búsqueda, ya sea de texto plano o regex, se compila internamente en un único <code>RegExp</code> de JavaScript. En modo texto plano tu término de búsqueda se escapa primero (para que <code>.</code>, <code>(</code>, <code>$</code> y similares coincidan literalmente), "palabra completa" envuelve el patrón en límites de palabra <code>\\b</code>, y el interruptor de mayúsculas simplemente añade o quita la bandera <code>i</code>. El resultado se vuelve a renderizar en cada pulsación, y el conteo de coincidencias viene de ejecutar el mismo patrón con la bandera global antes de reemplazar. Una entrada regex inválida no borra tu texto, solo muestra el error del motor y deja la salida intacta.',
        how_p2='Aquí está la función que casi ninguna página de buscar y reemplazar menciona: como el reemplazo usa el <code>String.replace</code> nativo de JavaScript, las referencias inversas funcionan en modo regex. Usa <code>$1</code>, <code>$2</code> para grupos de captura y <code>$&amp;</code> para toda la coincidencia. Así, buscar <code>(\\w+), (\\w+)</code> y reemplazar con <code>$2 $1</code> convierte "Doe, Jane" en "Jane Doe" en todo un archivo, y <code>$$</code> te da un signo de dólar literal cuando lo necesitas.',
        how_p3='Todo esto se ejecuta en el JavaScript de esta página, en tu máquina. Abre la pestaña Red de las DevTools mientras trabajas: ninguna petición transporta tu texto, por eso es seguro pegar logs, archivos de configuración, o cualquier otra cosa que prefieras no subir a un sitio web al azar.',
    ),
    related_tools=[
        ("regex-tester.html", "Probador de Regex", "Prueba una expresión regular con resaltado de coincidencias en vivo."),
        ("remove-duplicate-lines.html", "Eliminar líneas duplicadas", "Elimina duplicados antes o después de ordenar."),
        ("case-converter.html", "Conversor de mayúsculas/minúsculas", "MAYÚSCULAS, camelCase, snake_case, y más."),
    ],
)

PAGES["zh"] = dict(
    title="在线查找和替换文本（支持正则表达式）| norito",
    meta_desc="在浏览器中实时查找和替换文本，支持可选的正则表达式、区分大小写和全字匹配。不上传任何内容。",
    app_name="查找和替换", h1="查找和替换", breadcrumb_label="查找和替换",
    lede="在文档中查找和替换文本，支持可选的正则表达式、区分大小写和全字匹配，输入时实时更新。",
    t=dict(
        text="文本", ph_text="粘贴或输入你的文本...",
        find="查找", ph_find="要查找的文本或模式",
        replace_with="替换为", ph_replace="替换文本",
        use_regex="使用正则表达式", case_sensitive="区分大小写", whole_word="仅全字匹配",
        replace_all="替换所有匹配项",
        result="结果", copy_result="复制结果",
        how_h2="工作原理",
        how_p1='无论是纯文本查找还是正则表达式查找，每次搜索在底层都会被编译成一个 JavaScript <code>RegExp</code> 对象。在纯文本模式下，你的搜索词会先被转义（这样 <code>.</code>、<code>(</code>、<code>$</code> 等字符会按字面意思匹配），「仅全字匹配」会用 <code>\\b</code> 单词边界包裹该模式，大小写开关只是简单地添加或移除 <code>i</code> 标志。结果会在每次按键后重新渲染，匹配计数则来自在替换之前使用全局标志运行同一模式。无效的正则表达式输入不会清空你的文本，只会显示引擎的错误信息，并保持输出不变。',
        how_p2='这里有一个大多数查找替换页面从未提及的功能：由于替换使用了 JavaScript 原生的 <code>String.replace</code>，反向引用在正则模式下是可用的。使用 <code>$1</code>、<code>$2</code> 表示捕获组，<code>$&amp;</code> 表示整个匹配项。因此，查找 <code>(\\w+), (\\w+)</code> 并替换为 <code>$2 $1</code>，会在整个文件中把「Doe, Jane」变成「Jane Doe」，而 <code>$$</code> 则可以在你需要时给出一个字面上的美元符号。',
        how_p3='整个过程都在你机器上这个页面的 JavaScript 中运行。工作时打开开发者工具的 Network 标签页：没有任何请求携带你的文本，这正是为什么粘贴日志、配置文件，或任何你不想上传到随机网站的内容是安全的。',
    ),
    related_tools=[
        ("regex-tester.html", "正则表达式测试工具", "测试正则表达式，实时高亮匹配结果。"),
        ("remove-duplicate-lines.html", "删除重复行", "在排序前后对列表去重。"),
        ("case-converter.html", "大小写转换器", "大写、camelCase、snake_case 等多种格式。"),
    ],
)

PAGES["ar"] = dict(
    title="بحث واستبدال النص أونلاين (يدعم Regex) | norito",
    meta_desc="ابحث واستبدل النص مع دعم اختياري للتعبيرات النمطية، حساسية حالة الأحرف، ومطابقة الكلمة الكاملة، مباشرة في متصفحك. لا شيء يُرفَع.",
    app_name="بحث واستبدال", h1="بحث واستبدال", breadcrumb_label="بحث واستبدال",
    lede="ابحث واستبدل النص في مستند، مع تعبيرات نمطية اختيارية، وحساسية لحالة الأحرف، ومطابقة الكلمة الكاملة، مباشرة أثناء الكتابة.",
    t=dict(
        text="النص", ph_text="الصق أو اكتب نصك...",
        find="بحث", ph_find="نص أو نمط للبحث عنه",
        replace_with="استبدال بـ", ph_replace="نص الاستبدال",
        use_regex="استخدام Regex", case_sensitive="حساس لحالة الأحرف", whole_word="كلمة كاملة فقط",
        replace_all="استبدال كل التكرارات",
        result="النتيجة", copy_result="نسخ النتيجة",
        how_h2="كيف يعمل",
        how_p1='يُجمَّع كل بحث، سواء كان نصًا عاديًا أو تعبيرًا نمطيًا، داخليًا إلى <code>RegExp</code> واحد في جافاسكريبت. في وضع النص العادي، يُهرَّب مصطلح البحث أولًا (بحيث تتطابق <code>.</code> و<code>(</code> و<code>$</code> وما شابهها حرفيًا)، و«كلمة كاملة» تُغلِّف النمط بحدود كلمة <code>\\b</code>، ومفتاح حالة الأحرف يضيف أو يزيل ببساطة العلامة <code>i</code>. تُعاد عرض النتيجة مع كل ضغطة مفتاح، ويأتي عدد التطابقات من تشغيل نفس النمط بالعلامة الشاملة قبل الاستبدال. الإدخال غير الصالح للتعبير النمطي لا يمسح نصك، بل يعرض فقط خطأ المحرك ويترك الإخراج دون تغيير.',
        how_p2='إليك الميزة التي لا تذكرها تقريبًا أي صفحة بحث واستبدال أخرى: بما أن الاستبدال يستخدم <code>String.replace</code> الأصلي في جافاسكريبت، تعمل المراجع الخلفية في وضع Regex. استخدم <code>$1</code> و<code>$2</code> لمجموعات الالتقاط و<code>$&amp;</code> للتطابق الكامل. فالبحث عن <code>(\\w+), (\\w+)</code> والاستبدال بـ <code>$2 $1</code> يقلب «Doe, Jane» إلى «Jane Doe» عبر ملف كامل، ويمنحك <code>$$</code> علامة دولار حرفية عندما تحتاج إليها.',
        how_p3='كل هذا يعمل في جافاسكريبت هذه الصفحة على جهازك. افتح لسان Network في أدوات المطوّر أثناء العمل: لا يحمل أي طلب نصك، ولهذا بالضبط من الآمن لصق السجلات أو ملفات الإعدادات أو أي شيء آخر تفضّل عدم رفعه إلى موقع عشوائي.',
    ),
    related_tools=[
        ("regex-tester.html", "أداة اختبار Regex", "اختبر تعبيرًا نمطيًا مع تمييز مباشر للتطابقات."),
        ("remove-duplicate-lines.html", "إزالة الأسطر المكررة", "أزل التكرارات قبل الترتيب أو بعده."),
        ("case-converter.html", "محول حالة الأحرف", "أحرف كبيرة، camelCase، snake_case، والمزيد."),
    ],
)

PAGES["hi"] = dict(
    title="टेक्स्ट फ़ाइंड एंड रिप्लेस ऑनलाइन (Regex सपोर्टेड) | norito",
    meta_desc="अपने ब्राउज़र में लाइव, ऑप्शनल regex, केस सेंसिटिविटी, और होल-वर्ड मैचिंग के साथ टेक्स्ट फ़ाइंड और रिप्लेस करें। कुछ भी अपलोड नहीं होता।",
    app_name="फ़ाइंड एंड रिप्लेस", h1="फ़ाइंड एंड रिप्लेस", breadcrumb_label="फ़ाइंड एंड रिप्लेस",
    lede="किसी डॉक्यूमेंट में टेक्स्ट फ़ाइंड और रिप्लेस करें, ऑप्शनल regex, केस सेंसिटिविटी, और होल-वर्ड मैचिंग के साथ, टाइप करते ही लाइव।",
    t=dict(
        text="टेक्स्ट", ph_text="अपना टेक्स्ट पेस्ट या टाइप करें...",
        find="ढूंढें", ph_find="ढूंढने के लिए टेक्स्ट या पैटर्न",
        replace_with="इससे बदलें", ph_replace="रिप्लेसमेंट टेक्स्ट",
        use_regex="Regex इस्तेमाल करें", case_sensitive="केस सेंसिटिव", whole_word="सिर्फ़ पूरा शब्द",
        replace_all="सभी मैच रिप्लेस करें",
        result="परिणाम", copy_result="परिणाम कॉपी करें",
        how_h2="यह कैसे काम करता है",
        how_p1='हर सर्च, चाहे प्लेन टेक्स्ट हो या regex, अंदर ही अंदर एक सिंगल JavaScript <code>RegExp</code> में कंपाइल हो जाती है। प्लेन-टेक्स्ट मोड में आपका सर्च टर्म पहले एस्केप किया जाता है (ताकि <code>.</code>, <code>(</code>, <code>$</code> जैसे कैरेक्टर लिटरली मैच हों), "होल वर्ड" पैटर्न को <code>\\b</code> वर्ड बाउंड्रीज़ में रैप कर देता है, और केस टॉगल बस <code>i</code> फ़्लैग को जोड़ या हटा देता है। रिज़ल्ट हर कीस्ट्रोक पर दोबारा रेंडर होता है, और मैच काउंट रिप्लेस करने से पहले उसी पैटर्न को ग्लोबल फ़्लैग के साथ चलाकर मिलता है। इनवैलिड regex इनपुट आपका टेक्स्ट नहीं मिटाता, यह सिर्फ़ इंजन का एरर दिखाता है और आउटपुट को अनछुआ छोड़ देता है।',
        how_p2='यहां वह फ़ीचर है जिसका ज़्यादातर फ़ाइंड-एंड-रिप्लेस पेज कभी ज़िक्र नहीं करते: क्योंकि रिप्लेसमेंट JavaScript के नेटिव <code>String.replace</code> का इस्तेमाल करता है, बैकरेफ़रेंस regex मोड में काम करते हैं। कैप्चर ग्रुप्स के लिए <code>$1</code>, <code>$2</code> और पूरे मैच के लिए <code>$&amp;</code> इस्तेमाल करें। तो <code>(\\w+), (\\w+)</code> ढूंढकर <code>$2 $1</code> से रिप्लेस करने पर पूरी फ़ाइल में "Doe, Jane" "Jane Doe" में बदल जाता है, और <code>$$</code> ज़रूरत पड़ने पर आपको एक लिटरल डॉलर साइन देता है।',
        how_p3='यह सब आपकी मशीन पर इस पेज के JavaScript में चलता है। काम करते समय डेवटूल्स का Network टैब खोलें: कोई रिक्वेस्ट आपका टेक्स्ट नहीं ले जाती, इसीलिए लॉग्स, कॉन्फ़िग फ़ाइलें, या कुछ भी जो आप किसी रैंडम वेबसाइट पर अपलोड नहीं करना चाहते, यहां पेस्ट करना सेफ़ है।',
    ),
    related_tools=[
        ("regex-tester.html", "Regex टेस्टर", "लाइव मैच हाइलाइटिंग के साथ एक regex टेस्ट करें।"),
        ("remove-duplicate-lines.html", "डुप्लीकेट लाइनें हटाएं", "सॉर्ट करने से पहले या बाद में लिस्ट को डीडुप्लीकेट करें।"),
        ("case-converter.html", "केस कन्वर्टर", "UPPERCASE, camelCase, snake_case, और अधिक।"),
    ],
)

PAGES["ru"] = dict(
    title="Поиск и замена текста онлайн (с поддержкой Regex) | norito",
    meta_desc="Ищите и заменяйте текст с опциональной поддержкой regex, учётом регистра и совпадением по целому слову, прямо в браузере. Ничего не загружается.",
    app_name="Поиск и замена", h1="Поиск и замена", breadcrumb_label="Поиск и замена",
    lede="Ищите и заменяйте текст в документе с опциональной поддержкой regex, учётом регистра и совпадением по целому слову, прямо во время ввода.",
    t=dict(
        text="Текст", ph_text="Вставьте или введите ваш текст...",
        find="Найти", ph_find="текст или шаблон для поиска",
        replace_with="Заменить на", ph_replace="текст замены",
        use_regex="Использовать regex", case_sensitive="Учитывать регистр", whole_word="Только целое слово",
        replace_all="Заменить все совпадения",
        result="Результат", copy_result="Скопировать результат",
        how_h2="Как это работает",
        how_p1='Каждый поиск, обычный или regex, внутренне компилируется в единый JavaScript <code>RegExp</code>. В режиме обычного текста ваш поисковый запрос сначала экранируется (чтобы <code>.</code>, <code>(</code>, <code>$</code> и подобные символы совпадали буквально), «целое слово» оборачивает шаблон в границы слова <code>\\b</code>, а переключатель регистра просто добавляет или убирает флаг <code>i</code>. Результат перерисовывается при каждом нажатии клавиши, а счётчик совпадений получается запуском того же шаблона с глобальным флагом перед заменой. Некорректный regex-ввод не стирает ваш текст, а просто показывает ошибку движка и оставляет вывод нетронутым.',
        how_p2='Вот функция, которую почти ни одна страница поиска и замены не упоминает: поскольку замена использует нативный <code>String.replace</code> JavaScript, обратные ссылки работают в режиме regex. Используйте <code>$1</code>, <code>$2</code> для групп захвата и <code>$&amp;</code> для всего совпадения. Так, поиск <code>(\\w+), (\\w+)</code> и замена на <code>$2 $1</code> превращает «Doe, Jane» в «Jane Doe» по всему файлу, а <code>$$</code> даёт буквальный знак доллара, когда он вам нужен.',
        how_p3='Всё это выполняется в JavaScript этой страницы на вашем компьютере. Откройте вкладку Network в DevTools во время работы: ни один запрос не передаёт ваш текст, именно поэтому безопасно вставлять сюда логи, конфигурационные файлы или что угодно ещё, что вы предпочли бы не загружать на случайный сайт.',
    ),
    related_tools=[
        ("regex-tester.html", "Тестер регулярных выражений", "Проверьте regex с подсветкой совпадений в реальном времени."),
        ("remove-duplicate-lines.html", "Удаление дублирующихся строк", "Удаление дубликатов до или после сортировки."),
        ("case-converter.html", "Конвертер регистра", "ВЕРХНИЙ РЕГИСТР, camelCase, snake_case и другие."),
    ],
)

PAGES["ja"] = dict(
    title="テキストの検索と置換をオンラインで（正規表現対応）| norito",
    meta_desc="正規表現、大文字小文字の区別、単語単位の一致をオプションで指定し、ブラウザ内でリアルタイムにテキストを検索・置換。アップロードなし。",
    app_name="検索と置換", h1="検索と置換", breadcrumb_label="検索と置換",
    lede="正規表現、大文字小文字の区別、単語単位の一致をオプションで指定し、ドキュメント内のテキストを検索・置換します。入力するとリアルタイムに反映されます。",
    t=dict(
        text="テキスト", ph_text="テキストを貼り付けまたは入力...",
        find="検索", ph_find="検索するテキストまたはパターン",
        replace_with="置換後", ph_replace="置換テキスト",
        use_regex="正規表現を使用", case_sensitive="大文字小文字を区別", whole_word="単語単位のみ",
        replace_all="すべての一致を置換",
        result="結果", copy_result="結果をコピー",
        how_h2="仕組み",
        how_p1='プレーンテキストであれ正規表現であれ、すべての検索は内部で単一のJavaScript <code>RegExp</code>にコンパイルされます。プレーンテキストモードでは、検索語がまずエスケープされ（<code>.</code>、<code>(</code>、<code>$</code>などがそのまま文字として一致するように）、「単語単位」はパターンを<code>\\b</code>の単語境界で囲みます。大文字小文字の切り替えは単に<code>i</code>フラグを付け外しするだけです。結果はキー入力のたびに再描画され、一致件数は置換前に同じパターンをグローバルフラグ付きで実行することで得られます。無効な正規表現を入力してもテキストは消去されず、エンジンのエラーが表示されるだけで出力はそのまま保持されます。',
        how_p2='ほとんどの検索・置換ページが触れない機能をご紹介します。置換にはJavaScriptネイティブの<code>String.replace</code>が使われているため、正規表現モードで後方参照が使えます。キャプチャグループには<code>$1</code>、<code>$2</code>を、一致全体には<code>$&amp;</code>を使用します。つまり<code>(\\w+), (\\w+)</code>を検索し<code>$2 $1</code>で置換すれば、ファイル全体で「Doe, Jane」が「Jane Doe」に反転し、<code>$$</code>を使えば文字通りのドル記号が必要な時に得られます。',
        how_p3='この処理はすべて、あなたのマシン上でこのページのJavaScriptとして実行されます。作業中にDevToolsのNetworkタブを開いてみてください。あなたのテキストを運ぶリクエストは一切なく、だからこそログや設定ファイル、あるいはランダムなウェブサイトにアップロードしたくないものを貼り付けても安全なのです。',
    ),
    related_tools=[
        ("regex-tester.html", "正規表現テストツール", "正規表現をリアルタイムのハイライト付きでテスト。"),
        ("remove-duplicate-lines.html", "重複行の削除", "並べ替えの前後でリストの重複を削除。"),
        ("case-converter.html", "大文字小文字変換ツール", "大文字、camelCase、snake_caseなど。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "find-and-replace.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-find-replace.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/find-and-replace.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
