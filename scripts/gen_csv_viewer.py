#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>'
DZ_ICON = '<svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>'
ICON_CLASS = "c-teal"

def body(t):
    return f'''
    <div class="panel">
      <div class="dropzone" id="drop">
        {DZ_ICON}
        <p><strong>{t['dz_click']}</strong>{t['dz_or']}</p>
        <p class="note" style="margin-top:2px;">{t['dz_note']}</p>
        <input type="file" id="fileInput" accept=".csv,text/csv" />
      </div>
      <div class="result-box" id="result" style="display:none;"></div>
      <div class="csv-table-wrap" id="tableWrap" style="display:none;"></div>
      <div class="csv-table-actions">
        <button type="button" class="secondary" id="addRowBtn">{t['add_row']}</button>
        <button type="button" class="secondary" id="addColBtn">{t['add_col']}</button>
        <button type="button" id="downloadBtn">{t['download']}</button>
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
    title="Visor y editor de CSV | norito",
    meta_desc="Visualiza un archivo CSV como una tabla editable directamente en tu navegador. Edita celdas, añade filas o columnas y exporta de vuelta a CSV.",
    app_name="Visor de CSV",
    h1="Visor de CSV", breadcrumb_label="Visor de CSV",
    lede="Abre un archivo CSV como una tabla realmente editable, corrige un valor, añade una fila o columna, y expórtalo de nuevo. No necesitas ninguna hoja de cálculo.",
    t=dict(
        dz_click="Haz clic para elegir un archivo .csv",
        dz_or=", o arrástralo y suéltalo aquí",
        dz_note="Edita cualquier celda directamente en la tabla de abajo y luego exporta.",
        add_row="Añadir fila", add_col="Añadir columna", download="Descargar .csv",
        how_h2="Cómo funciona",
        how_p1='Tu archivo se lee como texto con la API <code>FileReader</code> del navegador, el delimitador se detecta automáticamente contando comas, puntos y coma y tabulaciones en la primera línea, y un analizador consciente de las comillas (estilo RFC 4180: los campos entre comillas pueden contener comas y saltos de línea, <code>""</code> significa una comilla literal) lo convierte en una cuadrícula en memoria. La tabla que ves es HTML real: cada celda es un elemento <code>&lt;input&gt;</code> conectado para escribir los cambios directamente en esa cuadrícula, por eso editar se siente instantáneo y por eso deshacer funciona celda por celda como cualquier campo de formulario.',
        how_p2="La exportación es donde esta herramienta es más cuidadosa que la mayoría. El serializador solo pone entre comillas los campos que realmente lo necesitan (los que contienen una coma, comilla o salto de línea), duplica las comillas incrustadas, y une las filas con saltos de línea CRLF (<code>\\r\\n</code>), exactamente lo que especifica RFC 4180 y lo que espera Excel. Una consecuencia: un archivo puede ir y volver con datos idénticos pero bytes ligeramente distintos, porque el uso inconsistente de comillas en el original se normaliza. Eso es cosmético, no pérdida de datos.",
        how_p3="Nada de esto toca un servidor. Abre la pestaña Red de las herramientas de desarrollador, carga un CSV, edita algunas celdas, descarga el resultado: verás cero peticiones relacionadas con tus datos. La descarga en sí es un <code>Blob</code> ensamblado en memoria y guardado por tu navegador.",
    ),
    related_tools=[
        ("/csv-to-json.html", "CSV a JSON", "Convierte un archivo CSV a JSON."),
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica JSON con una vista de árbol."),
        ("/sort-lines.html", "Ordenar líneas", "Ordena líneas de texto alfabética o numéricamente."),
    ],
)

PAGES["zh"] = dict(
    title="CSV 查看器与编辑器 | norito",
    meta_desc="直接在浏览器中把 CSV 文件当作可编辑表格查看。编辑单元格、添加行或列，再导出回 CSV。",
    app_name="CSV 查看器",
    h1="CSV 查看器", breadcrumb_label="CSV 查看器",
    lede="把 CSV 文件当作真正可编辑的表格打开，修正一个值、添加一行或一列，然后再导出。不需要任何电子表格软件。",
    t=dict(
        dz_click="点击选择一个 .csv 文件",
        dz_or="，或拖放到此处",
        dz_note="直接在下方表格中编辑任意单元格，然后导出。",
        add_row="添加行", add_col="添加列", download="下载 .csv",
        how_h2="工作原理",
        how_p1='你的文件通过浏览器内置的 <code>FileReader</code> API 读取为文本，分隔符会通过统计第一行中逗号、分号和制表符的数量自动检测，一个支持引号的解析器（RFC 4180 风格：带引号的字段可以包含逗号和换行符，<code>""</code> 表示字面意义上的引号）将其转换为内存中的网格。你看到的表格是真正的 HTML：每个单元格都是一个 <code>&lt;input&gt;</code> 元素，绑定后会把改动直接写回那个网格，这就是为什么编辑感觉是即时的，也是为什么撤销像任何表单字段一样按单元格生效。',
        how_p2="导出是这个工具比大多数同类工具更用心的地方。序列化器只会为真正需要的字段加引号（包含逗号、引号或换行符的字段），对内嵌的引号做双写处理，并用 CRLF（<code>\\r\\n</code>）换行符连接各行，这正是 RFC 4180 规定、也是 Excel 所期望的格式。一个后果是：文件往返导出后数据可能完全一致，但字节略有不同，因为原文件中不一致的加引号方式会被规范化。这只是表面差异，不是数据丢失。",
        how_p3="这一切都不会碰到服务器。打开开发者工具的网络面板，加载一个 CSV，编辑几个单元格，下载结果：你会看到零个涉及你数据的请求。下载本身是在内存中组装的 <code>Blob</code>，由浏览器保存。",
    ),
    related_tools=[
        ("/csv-to-json.html", "CSV 转 JSON", "将 CSV 文件转换为 JSON。"),
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩 JSON，附带树状视图。"),
        ("/sort-lines.html", "行排序", "按字母或数字顺序对文本行排序。"),
    ],
)

PAGES["ar"] = dict(
    title="عارض ومحرّر CSV | norito",
    meta_desc="اعرض ملف CSV كجدول قابل للتحرير مباشرةً في متصفحك. عدّل الخلايا، أضف صفوفًا أو أعمدة، وصدّره مرة أخرى كملف CSV.",
    app_name="عارض CSV",
    h1="عارض CSV", breadcrumb_label="عارض CSV",
    lede="افتح ملف CSV كجدول قابل للتحرير فعليًا، صحّح قيمة، أضف صفًا أو عمودًا، ثم صدّره مجددًا. لا حاجة لأي برنامج جداول بيانات.",
    t=dict(
        dz_click="انقر لاختيار ملف .csv",
        dz_or="، أو اسحبه وأفلته هنا",
        dz_note="عدّل أي خلية مباشرةً في الجدول أدناه، ثم صدّر.",
        add_row="إضافة صف", add_col="إضافة عمود", download="تنزيل .csv",
        how_h2="كيف يعمل",
        how_p1='يُقرأ ملفك كنص باستخدام واجهة <code>FileReader</code> المدمجة في المتصفح، ويُكتشف الفاصل تلقائيًا بعدّ الفواصل والفواصل المنقوطة وعلامات التبويب في السطر الأول، ثم يحوّله محلّل واعٍ بعلامات الاقتباس (بأسلوب RFC 4180: يمكن للحقول المقتبسة أن تحتوي على فواصل وأسطر جديدة، و<code>""</code> تعني علامة اقتباس حرفية) إلى شبكة في الذاكرة. الجدول الذي تراه هو HTML حقيقي: كل خلية عنصر <code>&lt;input&gt;</code> موصول لكتابة التغييرات مباشرةً في تلك الشبكة، ولهذا يبدو التحرير فوريًا ولهذا يعمل التراجع لكل خلية على حدة كأي حقل نموذج.',
        how_p2="التصدير هو حيث تكون هذه الأداة أكثر دقة من معظم الأدوات المشابهة. لا يضع المُسلسِل علامات اقتباس إلا حول الحقول التي تحتاجها فعلًا (التي تحتوي على فاصلة أو علامة اقتباس أو سطر جديد)، ويضاعف أي علامات اقتباس مضمّنة، ويصل الصفوف بنهايات أسطر CRLF (<code>\\r\\n</code>)، وهو بالضبط ما يحدده معيار RFC 4180 وما يتوقعه Excel. من النتائج المترتبة على ذلك: يمكن أن يُصدَّر الملف ويُستورد ببيانات متطابقة لكن بايتات مختلفة قليلًا، لأن وضع علامات الاقتباس غير المتسق في الملف الأصلي يُطبَّع. هذا أمر شكلي، وليس فقدانًا للبيانات.",
        how_p3="لا شيء هنا يلمس أي خادم. افتح تبويب الشبكة في أدوات المطوّر، حمّل ملف CSV، عدّل بعض الخلايا، نزّل النتيجة: لن ترى أي طلبات تتعلق ببياناتك. التنزيل نفسه عبارة عن <code>Blob</code> يُجمَّع في الذاكرة ويحفظه متصفحك.",
    ),
    related_tools=[
        ("/csv-to-json.html", "CSV إلى JSON", "حوّل ملف CSV إلى JSON."),
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق وضغط JSON مع عرض شجري."),
        ("/sort-lines.html", "ترتيب الأسطر", "رتّب أسطر النص أبجديًا أو رقميًا."),
    ],
)

PAGES["hi"] = dict(
    title="CSV व्यूअर और एडिटर | norito",
    meta_desc="अपने ब्राउज़र में ही CSV फ़ाइल को एडिटेबल टेबल के रूप में देखें। सेल एडिट करें, रो या कॉलम जोड़ें, और वापस CSV में एक्सपोर्ट करें।",
    app_name="CSV व्यूअर",
    h1="CSV व्यूअर", breadcrumb_label="CSV व्यूअर",
    lede="CSV फ़ाइल को असली एडिटेबल टेबल की तरह खोलें, कोई वैल्यू ठीक करें, रो या कॉलम जोड़ें, फिर वापस एक्सपोर्ट करें। किसी स्प्रेडशीट सॉफ़्टवेयर की ज़रूरत नहीं।",
    t=dict(
        dz_click="एक .csv फ़ाइल चुनने के लिए क्लिक करें",
        dz_or=", या इसे यहाँ ड्रैग करके छोड़ें",
        dz_note="नीचे टेबल में सीधे किसी भी सेल को एडिट करें, फिर एक्सपोर्ट करें।",
        add_row="रो जोड़ें", add_col="कॉलम जोड़ें", download="CSV डाउनलोड करें",
        how_h2="यह कैसे काम करता है",
        how_p1='आपकी फ़ाइल ब्राउज़र के बिल्ट-इन <code>FileReader</code> API से टेक्स्ट के रूप में पढ़ी जाती है, पहली लाइन में कॉमा, सेमीकोलन और टैब गिनकर डीलिमिटर अपने-आप पहचाना जाता है, और एक कोट-अवेयर पार्सर (RFC 4180 स्टाइल: कोट किए गए फ़ील्ड में कॉमा और लाइन ब्रेक हो सकते हैं, <code>""</code> का मतलब है एक लिटरल कोट) इसे मेमोरी में मौजूद ग्रिड में बदल देता है। जो टेबल आप देखते हैं वह असली HTML है: हर सेल एक <code>&lt;input&gt;</code> एलिमेंट है जो बदलावों को सीधे उस ग्रिड में वापस लिखने के लिए जुड़ा है, यही वजह है कि एडिटिंग तुरंत महसूस होती है और अनडू किसी भी फ़ॉर्म फ़ील्ड की तरह हर सेल पर अलग से काम करता है।',
        how_p2="एक्सपोर्ट वह जगह है जहाँ यह टूल ज़्यादातर टूल्स से ज़्यादा सावधान है। सीरियलाइज़र सिर्फ़ उन्हीं फ़ील्ड्स को कोट करता है जिन्हें वाकई इसकी ज़रूरत है (जिनमें कॉमा, कोट या लाइन ब्रेक हो), किसी भी एम्बेडेड कोट को डबल कर देता है, और रो को CRLF (<code>\\r\\n</code>) लाइन एंडिंग से जोड़ता है—बिल्कुल वही जो RFC 4180 बताता है और जो Excel उम्मीद करता है। एक नतीजा यह है कि फ़ाइल एक जैसे डेटा के साथ लेकिन थोड़े अलग बाइट्स के साथ राउंड-ट्रिप कर सकती है, क्योंकि ओरिजिनल में असंगत कोटिंग को नॉर्मलाइज़ कर दिया जाता है। यह सिर्फ़ कॉस्मेटिक है, डेटा लॉस नहीं।",
        how_p3="यहाँ कुछ भी सर्वर तक नहीं पहुँचता। डेवलपर टूल्स का नेटवर्क टैब खोलें, एक CSV लोड करें, कुछ सेल एडिट करें, नतीजा डाउनलोड करें: आपको अपने डेटा से जुड़ी शून्य रिक्वेस्ट दिखेंगी। डाउनलोड खुद मेमोरी में असेंबल किया गया एक <code>Blob</code> है जिसे आपका ब्राउज़र सेव करता है।",
    ),
    related_tools=[
        ("/csv-to-json.html", "CSV से JSON", "एक CSV फ़ाइल को JSON में बदलें।"),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "ट्री व्यू के साथ JSON फ़ॉर्मैट, वैलिडेट और मिनिफ़ाई करें."),
        ("/sort-lines.html", "लाइनें सॉर्ट करें", "टेक्स्ट लाइनों को अल्फ़ाबेटिकली या न्यूमेरिकली सॉर्ट करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Просмотр и редактирование CSV | norito",
    meta_desc="Просматривайте файл CSV как редактируемую таблицу прямо в браузере. Редактируйте ячейки, добавляйте строки или столбцы и экспортируйте обратно в CSV.",
    app_name="Просмотр CSV",
    h1="Просмотр CSV", breadcrumb_label="Просмотр CSV",
    lede="Откройте файл CSV как настоящую редактируемую таблицу, исправьте значение, добавьте строку или столбец, а затем экспортируйте обратно. Программа для работы с таблицами не нужна.",
    t=dict(
        dz_click="Нажмите, чтобы выбрать файл .csv",
        dz_or=", или перетащите его сюда",
        dz_note="Редактируйте любую ячейку прямо в таблице ниже, затем экспортируйте.",
        add_row="Добавить строку", add_col="Добавить столбец", download="Скачать .csv",
        how_h2="Как это работает",
        how_p1='Ваш файл читается как текст через встроенный в браузер API <code>FileReader</code>, разделитель определяется автоматически подсчётом запятых, точек с запятой и табуляций в первой строке, а парсер, учитывающий кавычки (в стиле RFC 4180: поля в кавычках могут содержать запятые и переносы строк, <code>""</code> означает буквальную кавычку), превращает его в сетку в памяти. Таблица, которую вы видите, — это настоящий HTML: каждая ячейка представляет собой элемент <code>&lt;input&gt;</code>, подключённый для записи изменений прямо в эту сетку, поэтому редактирование ощущается мгновенным, а отмена работает для каждой ячейки отдельно, как в любом поле формы.',
        how_p2="Экспорт — это то, в чём инструмент внимательнее большинства аналогов. Сериализатор заключает в кавычки только те поля, которым это действительно нужно (содержащие запятую, кавычку или перенос строки), удваивает встроенные кавычки и соединяет строки окончаниями CRLF (<code>\\r\\n</code>) — именно так, как предписывает RFC 4180 и как ожидает Excel. Следствие: файл может пройти полный цикл экспорта-импорта с идентичными данными, но чуть иными байтами, поскольку непоследовательное расставление кавычек в оригинале нормализуется. Это косметическая разница, а не потеря данных.",
        how_p3="Ничто из этого не обращается к серверу. Откройте вкладку «Сеть» в инструментах разработчика, загрузите CSV, отредактируйте несколько ячеек, скачайте результат — вы не увидите ни одного запроса, связанного с вашими данными. Сама загрузка — это <code>Blob</code>, собранный в памяти и сохранённый вашим браузером.",
    ),
    related_tools=[
        ("/csv-to-json.html", "CSV в JSON", "Преобразование файла CSV в JSON."),
        ("json-formatter.html", "Форматирование JSON", "Форматирует, проверяет и минифицирует JSON с древовидным представлением."),
        ("/sort-lines.html", "Сортировка строк", "Сортировка строк текста по алфавиту или по числам."),
    ],
)

PAGES["ja"] = dict(
    title="CSVビューア＆エディター | norito",
    meta_desc="CSVファイルをブラウザ内で編集可能な表としてそのまま表示。セルを編集し、行や列を追加して、CSVとして書き出せます。",
    app_name="CSVビューア",
    h1="CSVビューア", breadcrumb_label="CSVビューア",
    lede="CSVファイルを実際に編集できる表として開き、値を修正したり、行や列を追加したりして、そのままエクスポートできます。表計算ソフトは不要です。",
    t=dict(
        dz_click="クリックして .csv ファイルを選択",
        dz_or="、またはここにドラッグ＆ドロップ",
        dz_note="下の表で任意のセルを直接編集し、エクスポートしてください。",
        add_row="行を追加", add_col="列を追加", download=".csv をダウンロード",
        how_h2="仕組み",
        how_p1='ファイルはブラウザ組み込みの <code>FileReader</code> API でテキストとして読み込まれ、1行目のカンマ・セミコロン・タブの数を数えることで区切り文字が自動判定されます。引用符を考慮したパーサー（RFC 4180方式：引用符で囲まれたフィールドにはカンマや改行を含められ、<code>""</code> はリテラルな引用符を意味します）がこれをメモリ上のグリッドに変換します。表示されている表は本物のHTMLです。各セルは <code>&lt;input&gt;</code> 要素として実装され、変更を直接そのグリッドに書き戻すよう結び付けられているため、編集が即座に反映され、通常のフォーム項目と同じようにセル単位で元に戻せます。',
        how_p2="このツールが他の多くのツールより丁寧なのがエクスポート部分です。シリアライザーは実際に必要なフィールド（カンマ、引用符、改行を含むもの）だけを引用符で囲み、内部の引用符は二重化し、行は CRLF（<code>\\r\\n</code>）の改行コードで連結します。これはまさに RFC 4180 の仕様であり、Excel が期待する形式です。その結果、元のファイルで引用符の付け方が一貫していなかった場合、往復させたファイルはデータは同一でもバイト列が若干異なることがあります。これは見た目上の違いであり、データの欠落ではありません。",
        how_p3="この処理はサーバーに一切触れません。開発者ツールのネットワークタブを開き、CSVを読み込み、セルをいくつか編集し、結果をダウンロードしてみてください。データに関するリクエストは一つも発生しません。ダウンロード自体はメモリ内で組み立てられた <code>Blob</code> をブラウザが保存するものです。",
    ),
    related_tools=[
        ("/csv-to-json.html", "CSVからJSONへ", "CSVファイルをJSONに変換。"),
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証・圧縮し、ツリー表示できます。"),
        ("/sort-lines.html", "行の並べ替え", "テキストの行をアルファベット順または数値順に並べ替え。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "csv-viewer.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-csv-viewer.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/csv-viewer.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
