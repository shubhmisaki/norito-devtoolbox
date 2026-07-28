#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="9" x2="9" y2="21"/></svg>'
ICON_CLASS = "c-indigo"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="dropzone" id="drop">
          <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="9" x2="9" y2="21"/></svg>
          <p><strong>{t['dz_click']}</strong>{t['dz_drag']}</p>
          <p class="note" style="margin-top:2px;">{t['dz_or_paste']}</p>
          <input type="file" id="fileInput" accept=".csv,text/csv" />
        </div>
        <div class="field" style="margin-top:16px;">
          <label for="csvInput">{t['csv_text']}</label>
          <textarea id="csvInput" class="mono-area" rows="8" placeholder="{t['ph_csv']}"></textarea>
        </div>
        <div class="field-row">
          <div class="field">
            <label for="delimiter">{t['delimiter']}</label>
            <select id="delimiter">
              <option value="auto" selected>{t['auto_detect']}</option>
              <option value=",">{t['comma']}</option>
              <option value=";">{t['semicolon']}</option>
              <option value="\\t">{t['tab']}</option>
            </select>
          </div>
        </div>
        <div class="option-row">
          <span class="option-label">{t['first_row_header']}</span>
          <label class="switch"><input type="checkbox" id="headerToggle" checked /><span class="track"></span></label>
        </div>
        <div class="option-row">
          <span class="option-label">{t['pretty_print']}</span>
          <label class="switch"><input type="checkbox" id="prettyToggle" checked /><span class="track"></span></label>
        </div>
        <div class="result-box" id="result" style="display:none;"></div>
      </div>
      <div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['output']}</h3>
          <pre class="code-output" id="jsonOutput"></pre>
          <div class="batch-actions">
            <button type="button" class="secondary" id="copyBtn">{t['copy_json']}</button>
            <button type="button" id="downloadBtn">{t['download_json']}</button>
          </div>
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
    title="Conversor de CSV a JSON | norito",
    meta_desc="Convierte CSV a JSON en vivo en tu navegador. Detecta automáticamente el delimitador, trata la primera fila como encabezados, y formatea la salida.",
    app_name="CSV a JSON", h1="CSV a JSON", breadcrumb_label="CSV a JSON",
    lede="Pega o sube un archivo CSV y obtén JSON limpio al instante, los encabezados se convierten en claves de objeto, números y booleanos se detectan automáticamente.",
    t=dict(
        dz_click="Haz clic para elegir un archivo .csv", dz_drag=", o arrástralo aquí",
        dz_or_paste="O pega el texto CSV directamente en el cuadro de abajo.",
        csv_text="Texto CSV", ph_csv="nombre,edad,ciudad\nAlicia,30,Boston\nRoberto,25,Denver",
        delimiter="Delimitador", auto_detect="Detectar automáticamente", comma="Coma (,)", semicolon="Punto y coma (;)", tab="Tabulación",
        first_row_header="La primera fila es un encabezado", pretty_print="Formatear JSON",
        output="Salida", copy_json="Copiar JSON", download_json="Descargar .json",
        how_h2="Cómo funciona",
        how_p1='Los archivos se leen con la API <code>FileReader</code> del navegador y se analizan con un parser de una sola pasada escrito a mano que sigue las reglas de RFC 4180: recorre el texto carácter por carácter mientras rastrea si está dentro de un campo entre comillas. Esa es la parte que los conversores ingenuos de "dividir por comas" hacen mal: dentro de las comillas, las comas e incluso los saltos de línea pertenecen a la celda, y una comilla doblada (<code>""</code>) es un carácter de comilla literal. La autodetección de delimitador es pragmática en vez de inteligente: cuenta comas, puntos y coma, y tabulaciones en la primera línea y elige la ganadora, lo que maneja los CSV delimitados por punto y coma que producen las exportaciones de Excel europeas.',
        how_p2='La coerción de tipos es donde deberías mirar dos veces la salida. Los valores que parecen enteros o decimales se convierten en números JSON, y <code>true</code>/<code>false</code> se convierten en booleanos. Eso normalmente es lo que quieres, pero significa que valores con ceros a la izquierda, como códigos postales o extensiones telefónicas, salen como números: <code>01234</code> se convierte en <code>1234</code>. Si una columna es un identificador en vez de una cantidad, verifícala después de convertir. Las celdas finales faltantes en filas cortas se convierten en cadenas vacías en vez de romper la fila.',
        how_p3='El análisis, la coerción, e incluso la descarga .json (construida a partir de un <code>Blob</code> en memoria) ocurren todos dentro del JavaScript de esta página. Abre la pestaña Red de las DevTools mientras conviertes: ninguna petición transporta tus datos, así que las listas de clientes y exportaciones nunca salen de tu máquina.',
    ),
    related_tools=[
        ("csv-viewer.html", "Visor de CSV", "Ve y edita un CSV como una tabla editable."),
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica JSON."),
        ("json-diff.html", "JSON Diff", "Compara dos documentos JSON."),
    ],
)

PAGES["zh"] = dict(
    title="CSV 转 JSON 转换器 | norito",
    meta_desc="在浏览器中实时将 CSV 转换为 JSON。自动检测分隔符，将第一行作为表头，并对输出进行格式化。",
    app_name="CSV 转 JSON", h1="CSV 转 JSON", breadcrumb_label="CSV 转 JSON",
    lede="粘贴或上传一个 CSV 文件，立即获得整洁的 JSON，表头会自动变成对象的键，数字和布尔值会被自动识别。",
    t=dict(
        dz_click="点击选择一个 .csv 文件", dz_drag="，或将其拖放到此处",
        dz_or_paste="或者直接将 CSV 文本粘贴到下面的框中。",
        csv_text="CSV 文本", ph_csv="姓名,年龄,城市\n爱丽丝,30,波士顿\n鲍勃,25,丹佛",
        delimiter="分隔符", auto_detect="自动检测", comma="逗号 (,)", semicolon="分号 (;)", tab="制表符",
        first_row_header="第一行是表头", pretty_print="格式化 JSON",
        output="输出", copy_json="复制 JSON", download_json="下载 .json",
        how_h2="工作原理",
        how_p1='文件通过浏览器的 <code>FileReader</code> API 读取，并由一个手写的单遍解析器按照 RFC 4180 规则解析：它逐字符遍历文本，同时跟踪当前是否处于带引号的字段内。这正是简单的「按逗号分割」转换器容易出错的地方：在引号内，逗号甚至换行符都属于该单元格的一部分，而双引号（<code>""</code>）会被视为一个字面意义上的引号字符。分隔符的自动检测是实用型而非智能型的：它统计第一行中逗号、分号和制表符的出现次数，并选择出现次数最多的那个，这样就能正确处理欧洲版 Excel 导出常见的以分号分隔的 CSV 文件。',
        how_p2='类型强制转换是你应该重点检查输出结果的地方。看起来像整数或小数的值会被转换成 JSON 数字，<code>true</code>/<code>false</code> 会被转换成布尔值。这通常是你想要的效果，但也意味着带前导零的值（比如邮编或分机号）会被输出为数字：<code>01234</code> 会变成 <code>1234</code>。如果某一列是标识符而不是数量，请在转换后进行核对。较短行中缺失的末尾单元格会变成空字符串，而不会导致整行出错。',
        how_p3='解析、类型转换，甚至 .json 文件的下载（基于内存中的 <code>Blob</code> 构建）都在这个页面自身的 JavaScript 中完成。转换时打开开发者工具的 Network 标签页：不会有任何请求携带你的数据，因此客户名单和导出文件永远不会离开你的电脑。',
    ),
    related_tools=[
        ("csv-viewer.html", "CSV 查看器", "以可编辑表格的形式查看和编辑 CSV。"),
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩 JSON。"),
        ("json-diff.html", "JSON Diff", "比较两个 JSON 文档。"),
    ],
)

PAGES["ar"] = dict(
    title="محول CSV إلى JSON | norito",
    meta_desc="حوّل CSV إلى JSON مباشرة في متصفحك. يكتشف الفاصل تلقائيًا، ويعامل الصف الأول كرؤوس، وينسّق الإخراج.",
    app_name="CSV إلى JSON", h1="CSV إلى JSON", breadcrumb_label="CSV إلى JSON",
    lede="الصق أو ارفع ملف CSV واحصل على JSON نظيف فورًا، تصبح الرؤوس مفاتيح كائن، وتُكتشَف الأرقام والقيم المنطقية تلقائيًا.",
    t=dict(
        dz_click="انقر لاختيار ملف .csv", dz_drag="، أو اسحبه وأفلته هنا",
        dz_or_paste="أو الصق نص CSV مباشرة في المربع أدناه.",
        csv_text="نص CSV", ph_csv="الاسم,العمر,المدينة\nعلي,30,الرياض\nسارة,25,جدة",
        delimiter="الفاصل", auto_detect="اكتشاف تلقائي", comma="فاصلة (,)", semicolon="فاصلة منقوطة (;)", tab="تبويب",
        first_row_header="الصف الأول رأس", pretty_print="تنسيق JSON",
        output="الإخراج", copy_json="نسخ JSON", download_json="تنزيل .json",
        how_h2="كيف يعمل",
        how_p1='تُقرَأ الملفات بواجهة <code>FileReader</code> الخاصة بالمتصفح، ويُحلَّلها محلِّل مكتوب يدويًا بمرور واحد يتبع قواعد RFC 4180: يمر عبر النص حرفًا بحرف بينما يتتبّع ما إذا كان داخل حقل بين علامتي اقتباس. هذا هو الجزء الذي تخطئه محولات «التقسيم على الفاصلة» الساذجة: داخل علامات الاقتباس، تنتمي الفواصل وحتى فواصل الأسطر إلى الخلية، وعلامة الاقتباس المضاعفة (<code>""</code>) هي حرف اقتباس حرفي. الاكتشاف التلقائي للفاصل عملي وليس ذكيًا: يحسب الفواصل والفواصل المنقوطة وعلامات التبويب في السطر الأول ويختار الفائز، وهو ما يتعامل بشكل صحيح مع ملفات CSV المفصولة بفاصلة منقوطة التي تنتجها صادرات Excel الأوروبية.',
        how_p2='الإكراه النوعي هو المكان الذي يجب أن تنظر فيه إلى الإخراج مرتين. القيم التي تبدو كأعداد صحيحة أو عشرية تصبح أرقام JSON، وتصبح <code>true</code>/<code>false</code> قيمًا منطقية. هذا عادة ما تريده، لكنه يعني أن القيم ذات الأصفار البادئة، مثل الرموز البريدية أو امتدادات الهاتف، تخرج كأرقام: <code>01234</code> تتحول إلى <code>1234</code>. إذا كان العمود معرّفًا وليس كمية، تحقّق منه بعد التحويل. الخلايا الأخيرة المفقودة في الصفوف القصيرة تصبح سلاسل فارغة بدلاً من تعطيل الصف.',
        how_p3='يحدث التحليل والإكراه النوعي وحتى تنزيل .json (المبني من <code>Blob</code> في الذاكرة) كل ذلك داخل جافاسكريبت هذه الصفحة. افتح لسان Network في أدوات المطوّر أثناء التحويل: لا يحمل أي طلب بياناتك، لذا قوائم العملاء والصادرات لا تغادر جهازك أبدًا.',
    ),
    related_tools=[
        ("csv-viewer.html", "عارض CSV", "اعرض وحرّر CSV كجدول قابل للتحرير."),
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق وضغط JSON."),
        ("json-diff.html", "أداة مقارنة JSON", "قارن مستندي JSON."),
    ],
)

PAGES["hi"] = dict(
    title="CSV से JSON कन्वर्टर | norito",
    meta_desc="अपने ब्राउज़र में लाइव CSV को JSON में कन्वर्ट करें। डीलिमिटर को ऑटो-डिटेक्ट करता है, पहली रो को हेडर मानता है, और आउटपुट को प्रेटी-प्रिंट करता है।",
    app_name="CSV से JSON", h1="CSV से JSON", breadcrumb_label="CSV से JSON",
    lede="एक CSV फ़ाइल पेस्ट या अपलोड करें और तुरंत क्लीन JSON पाएं, हेडर्स ऑब्जेक्ट कीज़ बन जाते हैं, नंबर्स और बूलियन्स ऑटोमैटिकली डिटेक्ट होते हैं।",
    t=dict(
        dz_click=".csv फ़ाइल चुनने के लिए क्लिक करें", dz_drag=", या इसे यहां ड्रैग करके ड्रॉप करें",
        dz_or_paste="या नीचे दिए गए बॉक्स में सीधे CSV टेक्स्ट पेस्ट करें।",
        csv_text="CSV टेक्स्ट", ph_csv="name,age,city\nAlice,30,Boston\nBob,25,Denver",
        delimiter="डीलिमिटर", auto_detect="ऑटो-डिटेक्ट", comma="कॉमा (,)", semicolon="सेमीकोलन (;)", tab="टैब",
        first_row_header="पहली रो एक हेडर है", pretty_print="JSON प्रेटी-प्रिंट करें",
        output="आउटपुट", copy_json="JSON कॉपी करें", download_json=".json डाउनलोड करें",
        how_h2="यह कैसे काम करता है",
        how_p1='फ़ाइलों को ब्राउज़र के <code>FileReader</code> API से पढ़ा जाता है और एक हाथ से लिखे गए सिंगल-पास पार्सर से पार्स किया जाता है जो RFC 4180 नियमों का पालन करता है: यह टेक्स्ट को कैरेक्टर-दर-कैरेक्टर चलता है और साथ ही ट्रैक करता है कि यह किसी कोटेड फ़ील्ड के अंदर है या नहीं। यही वह हिस्सा है जो नैव स्प्लिट-ऑन-कॉमा कन्वर्टर्स ग़लत करते हैं: कोट्स के अंदर, कॉमा और यहां तक कि लाइन ब्रेक्स भी सेल के हिस्से होते हैं, और एक डबल्ड कोट (<code>""</code>) एक लिटरल कोट कैरेक्टर होता है। डीलिमिटर ऑटो-डिटेक्शन स्मार्ट होने के बजाय प्रैगमैटिक है: यह पहली लाइन में कॉमा, सेमीकोलन, और टैब्स गिनता है और विनर चुनता है, जो यूरोपियन Excel एक्सपोर्ट्स द्वारा बनाए गए सेमीकोलन-डीलिमिटेड CSVs को सही तरीक़े से हैंडल करता है।',
        how_p2='टाइप कोअर्शन वह जगह है जहां आपको आउटपुट को दो बार देखना चाहिए। ऐसी वैल्यूज़ जो इंटिजर्स या डेसिमल्स जैसी दिखती हैं JSON नंबर्स बन जाती हैं, और <code>true</code>/<code>false</code> बूलियन्स बन जाते हैं। यह आमतौर पर वही है जो आप चाहते हैं, लेकिन इसका मतलब है कि लीडिंग ज़ीरोज़ वाली वैल्यूज़, जैसे ZIP कोड्स या फ़ोन एक्सटेंशन्स, नंबर्स के रूप में निकलती हैं: <code>01234</code> <code>1234</code> बन जाता है। अगर कोई कॉलम क्वांटिटी के बजाय एक आइडेंटिफ़ायर है, तो कन्वर्ट करने के बाद उसे वेरिफ़ाई करें। छोटी रोज़ में गायब ट्रेलिंग सेल्स रो को क्रैश करने के बजाय ख़ाली स्ट्रिंग्स बन जाती हैं।',
        how_p3='पार्सिंग, कोअर्शन, और यहां तक कि .json डाउनलोड (एक इन-मेमोरी <code>Blob</code> से बना) सब कुछ इस पेज के JavaScript के अंदर होता है। कन्वर्ट करते समय डेवटूल्स का Network टैब खोलें: कोई रिक्वेस्ट आपका डेटा नहीं ले जाती, इसलिए कस्टमर लिस्ट्स और एक्सपोर्ट्स कभी आपकी मशीन से बाहर नहीं जाते।',
    ),
    related_tools=[
        ("csv-viewer.html", "CSV व्यूअर", "CSV को एक एडिटेबल टेबल के रूप में देखें और एडिट करें।"),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "JSON फ़ॉर्मैट, वैलिडेट और मिनिफ़ाई करें।"),
        ("json-diff.html", "JSON डिफ", "दो JSON डॉक्यूमेंट कंपेयर करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Конвертер CSV в JSON | norito",
    meta_desc="Конвертируйте CSV в JSON прямо в браузере. Автоматически определяет разделитель, обрабатывает первую строку как заголовки и форматирует вывод.",
    app_name="CSV в JSON", h1="CSV в JSON", breadcrumb_label="CSV в JSON",
    lede="Вставьте или загрузите CSV-файл и мгновенно получите чистый JSON — заголовки становятся ключами объекта, числа и логические значения определяются автоматически.",
    t=dict(
        dz_click="Нажмите, чтобы выбрать файл .csv", dz_drag=", или перетащите его сюда",
        dz_or_paste="Или вставьте текст CSV прямо в поле ниже.",
        csv_text="Текст CSV", ph_csv="имя,возраст,город\nАлиса,30,Бостон\nБоб,25,Денвер",
        delimiter="Разделитель", auto_detect="Автоопределение", comma="Запятая (,)", semicolon="Точка с запятой (;)", tab="Табуляция",
        first_row_header="Первая строка — заголовок", pretty_print="Форматировать JSON",
        output="Вывод", copy_json="Скопировать JSON", download_json="Скачать .json",
        how_h2="Как это работает",
        how_p1='Файлы читаются с помощью API браузера <code>FileReader</code> и разбираются написанным вручную однопроходным парсером, следующим правилам RFC 4180: он проходит по тексту символ за символом, отслеживая, находится ли он внутри поля в кавычках. Именно в этом ошибаются наивные конвертеры, разделяющие по запятым: внутри кавычек запятые и даже переносы строк принадлежат ячейке, а удвоенная кавычка (<code>""</code>) — это буквальный символ кавычки. Автоопределение разделителя прагматично, а не «умно»: оно считает запятые, точки с запятой и табуляции в первой строке и выбирает победителя, что корректно обрабатывает CSV-файлы с разделителем точка с запятой, которые создают европейские экспорты из Excel.',
        how_p2='Приведение типов — это то место, куда стоит внимательно посмотреть в результате. Значения, похожие на целые или десятичные числа, становятся числами JSON, а <code>true</code>/<code>false</code> — логическими значениями. Обычно это именно то, что нужно, но это означает, что значения с ведущими нулями, например почтовые индексы или добавочные номера телефонов, выходят как числа: <code>01234</code> превращается в <code>1234</code>. Если столбец является идентификатором, а не количеством, проверьте его после конвертации. Отсутствующие завершающие ячейки в коротких строках становятся пустыми строками, а не приводят к сбою строки.',
        how_p3='Разбор, приведение типов и даже скачивание .json (построенное из <code>Blob</code> в памяти) — всё это происходит внутри JavaScript этой страницы. Откройте вкладку Network в DevTools во время конвертации: ни один запрос не передаёт ваши данные, поэтому списки клиентов и экспортированные файлы никогда не покидают ваш компьютер.',
    ),
    related_tools=[
        ("csv-viewer.html", "Просмотр CSV", "Просматривайте и редактируйте CSV как редактируемую таблицу."),
        ("json-formatter.html", "Форматирование JSON", "Форматирует, проверяет и минифицирует JSON."),
        ("json-diff.html", "JSON Diff", "Сравните два JSON-документа."),
    ],
)

PAGES["ja"] = dict(
    title="CSVからJSONへの変換ツール | norito",
    meta_desc="ブラウザ内でCSVをJSONにリアルタイム変換。区切り文字を自動検出し、1行目をヘッダーとして扱い、出力を整形します。",
    app_name="CSVからJSON", h1="CSVからJSON", breadcrumb_label="CSVからJSON",
    lede="CSVファイルを貼り付けまたはアップロードすると、すぐにきれいなJSONが得られます。ヘッダーはオブジェクトのキーになり、数値や真偽値は自動的に検出されます。",
    t=dict(
        dz_click="クリックして.csvファイルを選択", dz_drag="、またはここにドラッグ＆ドロップ",
        dz_or_paste="または下のボックスにCSVテキストを直接貼り付けてください。",
        csv_text="CSVテキスト", ph_csv="名前,年齢,都市\n太郎,30,東京\n花子,25,大阪",
        delimiter="区切り文字", auto_detect="自動検出", comma="カンマ (,)", semicolon="セミコロン (;)", tab="タブ",
        first_row_header="1行目はヘッダー", pretty_print="JSONを整形",
        output="出力", copy_json="JSONをコピー", download_json=".jsonをダウンロード",
        how_h2="仕組み",
        how_p1='ファイルはブラウザの<code>FileReader</code> APIで読み込まれ、RFC 4180のルールに従って書かれた手作りのシングルパスパーサーで解析されます。テキストを1文字ずつたどりながら、引用符で囲まれたフィールド内かどうかを追跡します。ここが単純な「カンマで分割」する変換ツールが間違えやすい部分です。引用符の中では、カンマや改行までもがそのセルの一部になり、二重引用符（<code>""</code>）はリテラルな引用符文字として扱われます。区切り文字の自動検出は賢さよりも実用性を重視しています。1行目のカンマ、セミコロン、タブの出現回数を数え、最も多いものを選ぶという方式で、これによりヨーロッパ版Excelのエクスポートでよく見られるセミコロン区切りのCSVも正しく処理できます。',
        how_p2='型の強制変換は、出力結果を二度見すべきポイントです。整数や小数のように見える値はJSONの数値に変換され、<code>true</code>/<code>false</code>は真偽値になります。これは通常望ましい動作ですが、郵便番号や内線番号のように先頭にゼロが付く値も数値として出力されてしまうことを意味します。<code>01234</code>は<code>1234</code>になります。ある列が数量ではなく識別子である場合は、変換後に確認してください。短い行で末尾のセルが欠けている場合、その行を壊すのではなく空文字列として扱われます。',
        how_p3='解析、型変換、さらには.jsonのダウンロード（メモリ内の<code>Blob</code>から構築）まで、すべてこのページのJavaScript内で行われます。変換中にDevToolsのNetworkタブを開いてみてください。あなたのデータを運ぶリクエストは一切発生しないため、顧客リストやエクスポートファイルがあなたのマシンから外に出ることはありません。',
    ),
    related_tools=[
        ("csv-viewer.html", "CSVビューア", "CSVを編集可能な表として表示・編集。"),
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証・圧縮。"),
        ("json-diff.html", "JSON Diff", "2つのJSONドキュメントを比較。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "csv-to-json.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-csv-to-json.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/csv-to-json.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
