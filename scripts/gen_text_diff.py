#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/></svg>'
ICON_CLASS = "c-rose"

def body(t):
    return f'''
    <div class="panel">
      <div style="display:flex; gap:16px; flex-wrap:wrap; margin-bottom:16px;">
        <label class="option-row" style="flex:0 0 auto;">
          <input type="checkbox" id="ignoreWhitespace" />
          <span>{t['ignore_ws']}</span>
        </label>
        <label class="option-row" style="flex:0 0 auto;">
          <input type="checkbox" id="ignoreCase" />
          <span>{t['ignore_case']}</span>
        </label>
      </div>

      <div class="two-col" style="margin-bottom:16px;">
        <div class="field">
          <label for="inputA">{t['original']}</label>
          <textarea id="inputA" class="mono-area" rows="10" placeholder="{t['ph_a']}"></textarea>
        </div>
        <div class="field">
          <label for="inputB">{t['changed']}</label>
          <textarea id="inputB" class="mono-area" rows="10" placeholder="{t['ph_b']}"></textarea>
        </div>
      </div>

      <div id="tooLarge" class="result-box error" style="display:none; margin-bottom:16px;">
        <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
        <div class="r-body">{t['too_large']}</div>
      </div>

      <div id="emptyState" class="note" style="display:block;">{t['empty_state']}</div>

      <div id="diffStatsRow" style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
        <div class="diff-stats" id="statsBox" style="display:none;"></div>
      </div>
      <div class="diff-view" id="diffOutput" style="display:none;"></div>

      <div style="margin-top:16px;">
        <button id="copyBtn" class="secondary">{t['copy_diff']}</button>
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
    title="Comparador de Texto: Compara Dos Textos Online | norito",
    meta_desc="Compara dos bloques de texto línea por línea y ve exactamente qué cambió. Ignora espacios o mayúsculas, copia el diff. Funciona por completo en tu navegador.",
    app_name="Comparador de Texto", h1="Comparador de Texto", breadcrumb_label="Comparador de Texto",
    lede="Compara dos bloques de texto línea por línea y ve exactamente qué se añadió, se eliminó o quedó sin cambios.",
    t=dict(
        ignore_ws="Ignorar espacios", ignore_case="Ignorar mayúsculas/minúsculas",
        original="Original", changed="Modificado",
        ph_a="Pega el texto original...", ph_b="Pega el texto modificado...",
        too_large="Uno de estos textos supera las 4000 líneas. Prueba a comparar una sección más pequeña.",
        empty_state="Pega texto en ambos cuadros para ver una comparación línea por línea.",
        copy_diff="Copiar diff como texto",
        how_h2="Cómo funciona",
        how_p1='La comparación es un diff a nivel de línea basado en el algoritmo de la subsecuencia común más larga (LCS), la misma familia de lógica detrás de <code>git diff</code>. Ambos textos se dividen en líneas y luego una tabla de programación dinámica calcula el mayor conjunto de líneas que comparten las dos versiones en orden. Recorrer esa tabla hacia atrás produce las operaciones que ves: las líneas que solo están en el texto izquierdo se marcan en rojo como eliminadas, las que solo están en el derecho se marcan en verde como añadidas, y las líneas compartidas permanecen neutras, cada una con su número de línea original.',
        how_p2='El diff a nivel de línea es una decisión deliberada. Los diffs a nivel de carácter pueden mostrar que una sola palabra cambió dentro de una línea, pero en documentos reales degeneran en confeti: cientos de fragmentos diminutos más difíciles de leer que simplemente ver la línea antigua eliminada y la nueva añadida. La salida a nivel de línea se mantiene legible y encaja directamente con cómo la revisión de código y el control de versiones presentan los cambios. Las dos casillas ajustan qué significa "igual": ignorar espacios colapsa las secuencias de espacios y recorta los finales de línea antes de comparar (ideal para código reformateado), e ignorar mayúsculas/minúsculas pone ambos lados en minúsculas. Las líneas mostradas conservan su formato original en cualquier caso.',
        how_p3="Como la tabla de programación dinámica cuesta memoria y tiempo proporcional a (líneas en A) x (líneas en B), la herramienta limita la entrada a 4000 líneas por lado; más allá de eso, la tabla por sí sola tendría decenas de millones de celdas y la pestaña se trabaría. Dentro del límite, todo se ejecuta de forma síncrona en tu navegador: ambos textos viven solo en tu pestaña, no se dispara ninguna petición al escribir (comprueba el panel Red de las DevTools), y los borradores o configuraciones confidenciales nunca tocan un servidor.",
    ),
    related_tools=[
        ("json-diff.html", "Comparador de JSON", "Compara dos documentos JSON."),
        ("remove-duplicate-lines.html", "Eliminar líneas duplicadas", "Elimina duplicados antes o después de ordenar."),
        ("sort-lines.html", "Ordenar líneas", "Ordena líneas de texto alfabética o numéricamente."),
    ],
)

PAGES["zh"] = dict(
    title="文本对比工具：在线比较两段文本 | norito",
    meta_desc="逐行比较两段文本，精确显示发生的更改。可忽略空格或大小写，复制差异结果。完全在浏览器中运行。",
    app_name="文本对比工具", h1="文本对比工具", breadcrumb_label="文本对比工具",
    lede="逐行比较两段文本，精确查看哪些内容被添加、删除或保持不变。",
    t=dict(
        ignore_ws="忽略空格", ignore_case="忽略大小写",
        original="原始文本", changed="修改后",
        ph_a="粘贴原始文本...", ph_b="粘贴修改后的文本...",
        too_large="其中一段文本超过 4000 行。请尝试比较更小的部分。",
        empty_state="在两个文本框中粘贴内容，即可查看逐行对比结果。",
        copy_diff="复制差异为文本",
        how_h2="工作原理",
        how_p1='该对比功能是基于最长公共子序列（LCS）算法实现的逐行差异比较，与 <code>git diff</code> 背后的逻辑属于同一类。两段文本先被拆分成行，然后通过一张动态规划表计算出两个版本按顺序共有的最大行集合。反向遍历这张表就能得出你看到的操作结果：只存在于左侧文本的行被标记为红色删除，只存在于右侧的行被标记为绿色添加，共有的行保持中性显示，并各自附带原始行号。',
        how_p2='采用逐行对比是一个刻意的权衡。逐字符对比可以显示某一行中某个词发生了变化，但在真实文档中，这种方式往往会退化成满屏碎片：数百个细小片段，比直接看到旧行被删除、新行被添加更难阅读。逐行输出保持易读性，也直接对应代码审查和版本控制展示更改的方式。两个复选框可以调整"相等"的定义：忽略空格会在比较前折叠连续空格并去除行末空白（非常适合重新格式化过的代码），忽略大小写会将两侧统一转为小写。无论如何设置，显示的行都会保留其原始格式。',
        how_p3="由于动态规划表所需的内存和时间与（A 的行数）x（B 的行数）成正比，该工具将每侧输入限制在 4000 行以内；超过这个限制，仅这张表就会有数千万个单元格，标签页会卡顿。在限制范围内，一切都在你的浏览器中同步运行：两段文本只存在于你的标签页中，输入时不会发出任何请求（可在开发者工具的 Network 面板中查看），机密草稿或配置内容永远不会接触服务器。",
    ),
    related_tools=[
        ("json-diff.html", "JSON 对比工具", "比较两个 JSON 文档。"),
        ("remove-duplicate-lines.html", "删除重复行", "在排序前后对列表去重。"),
        ("sort-lines.html", "行排序", "按字母或数字顺序对文本行排序。"),
    ],
)

PAGES["ar"] = dict(
    title="أداة مقارنة النصوص: قارن نصين أونلاين | norito",
    meta_desc="قارن كتلتين من النص سطرًا بسطر وشاهد بالضبط ما تغيّر. تجاهل المسافات أو حالة الأحرف، وانسخ الفروقات. يعمل بالكامل في متصفحك.",
    app_name="أداة مقارنة النصوص", h1="أداة مقارنة النصوص", breadcrumb_label="أداة مقارنة النصوص",
    lede="قارن كتلتين من النص سطرًا بسطر وشاهد بالضبط ما أُضيف أو حُذف أو بقي دون تغيير.",
    t=dict(
        ignore_ws="تجاهل المسافات", ignore_case="تجاهل حالة الأحرف",
        original="النص الأصلي", changed="النص المعدَّل",
        ph_a="الصق النص الأصلي...", ph_b="الصق النص المعدَّل...",
        too_large="أحد هذين النصين يتجاوز 4000 سطر. جرّب مقارنة قسم أصغر.",
        empty_state="الصق نصًا في كلا المربعين لرؤية مقارنة سطرًا بسطر.",
        copy_diff="نسخ الفروقات كنص",
        how_h2="كيف يعمل",
        how_p1='المقارنة هي مقارنة على مستوى الأسطر مبنية على خوارزمية أطول تتابع مشترك (LCS)، وهي نفس عائلة المنطق وراء <code>git diff</code>. يُقسَّم كلا النصين إلى أسطر، ثم تحسب جدول برمجة ديناميكية أكبر مجموعة من الأسطر التي تتشاركها النسختان بالترتيب. يؤدي تتبّع هذا الجدول رجوعًا إلى إنتاج العمليات التي تراها: الأسطر الموجودة فقط في النص الأيسر تُوسَم باللون الأحمر كمحذوفة، والأسطر الموجودة فقط في اليمين تُوسَم باللون الأخضر كمضافة، وتبقى الأسطر المشتركة محايدة، ولكل منها رقم سطرها الأصلي.',
        how_p2='المقارنة على مستوى الأسطر هي مفاضلة متعمّدة. يمكن للمقارنات على مستوى الأحرف أن تُظهر أن كلمة واحدة تغيّرت داخل سطر ما، لكنها في المستندات الحقيقية تتحول إلى فوضى من الشظايا: مئات القطع الصغيرة الأصعب في القراءة من مجرد رؤية السطر القديم محذوفًا والجديد مضافًا. تبقى المخرجات على مستوى السطر سهلة القراءة وتتوافق مباشرة مع كيفية عرض مراجعة الكود والتحكم في الإصدارات للتغييرات. يضبط المربعان معنى «التساوي»: تجاهل المسافات يطوي سلاسل المسافات ويقصّ نهايات الأسطر قبل المقارنة (ممتاز للكود المعاد تنسيقه)، وتجاهل حالة الأحرف يحوّل الجانبين إلى أحرف صغيرة. تحتفظ الأسطر المعروضة بتنسيقها الأصلي في كلتا الحالتين.',
        how_p3='بما أن جدول البرمجة الديناميكية يكلّف ذاكرة ووقتًا يتناسبان مع (أسطر A) × (أسطر B)، تحدّ الأداة الإدخال بـ 4000 سطر لكل جانب؛ وبعد ذلك الحد، سيحتوي الجدول وحده على عشرات الملايين من الخلايا وسيتلعثم التبويب. ضمن الحد، يعمل كل شيء بشكل متزامن في متصفحك: يعيش كلا النصين فقط في تبويبك، ولا يُطلَق أي طلب عند الكتابة (تحقق من لوحة الشبكة في أدوات المطوّر)، ولا تلمس المسودات أو الإعدادات السرّية خادمًا أبدًا.',
    ),
    related_tools=[
        ("json-diff.html", "أداة مقارنة JSON", "قارن مستندي JSON."),
        ("remove-duplicate-lines.html", "إزالة الأسطر المكررة", "أزل التكرارات قبل الترتيب أو بعده."),
        ("sort-lines.html", "ترتيب الأسطر", "رتّب أسطر النص أبجديًا أو رقميًا."),
    ],
)

PAGES["hi"] = dict(
    title="टेक्स्ट डिफ चेकर: दो टेक्स्ट ऑनलाइन कंपेयर करें | norito",
    meta_desc="दो टेक्स्ट ब्लॉक की लाइन-दर-लाइन तुलना करें और देखें कि क्या बदला। व्हाइटस्पेस या केस इग्नोर करें, डिफ कॉपी करें। पूरी तरह आपके ब्राउज़र में चलता है।",
    app_name="टेक्स्ट डिफ चेकर", h1="टेक्स्ट डिफ चेकर", breadcrumb_label="टेक्स्ट डिफ चेकर",
    lede="दो टेक्स्ट ब्लॉक की लाइन-दर-लाइन तुलना करें और देखें कि क्या जोड़ा गया, हटाया गया, या बिना बदलाव के छोड़ा गया।",
    t=dict(
        ignore_ws="व्हाइटस्पेस इग्नोर करें", ignore_case="केस इग्नोर करें",
        original="ओरिजिनल", changed="बदला हुआ",
        ph_a="ओरिजिनल टेक्स्ट पेस्ट करें...", ph_b="बदला हुआ टेक्स्ट पेस्ट करें...",
        too_large="इनमें से एक टेक्स्ट 4,000 लाइनों से ज़्यादा है। कोई छोटा सेक्शन कंपेयर करके देखें।",
        empty_state="लाइन-दर-लाइन तुलना देखने के लिए दोनों बॉक्स में टेक्स्ट पेस्ट करें।",
        copy_diff="डिफ को टेक्स्ट के रूप में कॉपी करें",
        how_h2="यह कैसे काम करता है",
        how_p1='यह तुलना लॉन्गेस्ट कॉमन सबसीक्वेंस (LCS) एल्गोरिद्म पर बना एक लाइन-लेवल डिफ है, जो <code>git diff</code> के पीछे वाले लॉजिक के उसी परिवार का है। दोनों टेक्स्ट को लाइनों में बांटा जाता है, फिर एक डायनामिक-प्रोग्रामिंग टेबल यह पता लगाती है कि दोनों वर्ज़न किस क्रम में सबसे ज़्यादा लाइनें शेयर करते हैं। उस टेबल को पीछे की ओर ट्रेस करने पर वे ऑपरेशन मिलते हैं जो आप देखते हैं: सिर्फ़ बाईं तरफ़ की लाइनें लाल रंग में रिमूवल के रूप में मार्क होती हैं, सिर्फ़ दाईं तरफ़ की लाइनें हरे रंग में एडिशन के रूप में, और शेयर की गई लाइनें न्यूट्रल रहती हैं, हर एक अपनी ओरिजिनल लाइन नंबर के साथ।',
        how_p2='लाइन-लेवल डिफिंग एक जानबूझकर लिया गया ट्रेडऑफ़ है। कैरेक्टर-लेवल डिफ यह दिखा सकते हैं कि किसी लाइन के अंदर एक शब्द बदला, लेकिन असली डॉक्यूमेंट्स पर वे कन्फ़ेटी में बदल जाते हैं: सैकड़ों छोटे-छोटे टुकड़े जो सिर्फ़ पुरानी लाइन हटी और नई लाइन जुड़ी देखने से ज़्यादा पढ़ने में मुश्किल होते हैं। लाइन-लेवल आउटपुट पढ़ने लायक बना रहता है और सीधे उस तरीक़े से मेल खाता है जैसे कोड रिव्यू और वर्ज़न कंट्रोल बदलावों को दिखाते हैं। दोनों चेकबॉक्स यह ट्यून करते हैं कि "बराबर" का मतलब क्या है: व्हाइटस्पेस इग्नोर करें, तुलना से पहले लगातार स्पेस को समेट देता है और लाइन के आख़िर को ट्रिम कर देता है (रीफ़ॉर्मैट किए गए कोड के लिए बढ़िया), और केस इग्नोर करें दोनों तरफ़ को लोअरकेस कर देता है। दिखाई गई लाइनें दोनों ही स्थिति में अपना ओरिजिनल फ़ॉर्मैटिंग बनाए रखती हैं।',
        how_p3="चूंकि DP टेबल की मेमोरी और समय की लागत (A में लाइनें) x (B में लाइनें) के अनुपात में होती है, टूल इनपुट को हर तरफ़ 4,000 लाइनों तक सीमित रखता है; इस लिमिट के बाद, अकेले टेबल में करोड़ों सेल हो जातीं और टैब अटकने लगता। लिमिट के अंदर, सब कुछ आपके ब्राउज़र में सिंक्रोनसली चलता है: दोनों टेक्स्ट सिर्फ़ आपके टैब में रहते हैं, टाइप करते समय कोई रिक्वेस्ट फ़ायर नहीं होती (डेवटूल्स के Network पैनल में चेक करें), और गोपनीय ड्राफ़्ट या कॉन्फ़िग कभी सर्वर को नहीं छूते।",
    ),
    related_tools=[
        ("json-diff.html", "JSON डिफ", "दो JSON डॉक्यूमेंट कंपेयर करें।"),
        ("remove-duplicate-lines.html", "डुप्लीकेट लाइनें हटाएं", "सॉर्ट करने से पहले या बाद में लिस्ट को डीडुप्लीकेट करें।"),
        ("sort-lines.html", "लाइनें सॉर्ट करें", "टेक्स्ट लाइनों को अल्फ़ाबेटिकली या न्यूमेरिकली सॉर्ट करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Сравнение текста: сравнить два текста онлайн | norito",
    meta_desc="Сравните два блока текста построчно и увидьте, что именно изменилось. Игнорируйте пробелы или регистр, копируйте различия. Работает полностью в браузере.",
    app_name="Сравнение текста", h1="Сравнение текста", breadcrumb_label="Сравнение текста",
    lede="Сравните два блока текста построчно и увидьте, что именно было добавлено, удалено или осталось без изменений.",
    t=dict(
        ignore_ws="Игнорировать пробелы", ignore_case="Игнорировать регистр",
        original="Исходный текст", changed="Изменённый текст",
        ph_a="Вставьте исходный текст...", ph_b="Вставьте изменённый текст...",
        too_large="Один из текстов превышает 4000 строк. Попробуйте сравнить меньший фрагмент.",
        empty_state="Вставьте текст в оба поля, чтобы увидеть построчное сравнение.",
        copy_diff="Скопировать различия как текст",
        how_h2="Как это работает",
        how_p1='Сравнение выполняется на уровне строк на основе алгоритма наибольшей общей подпоследовательности (LCS) — той же логики, что лежит в основе <code>git diff</code>. Оба текста разбиваются на строки, а затем таблица динамического программирования вычисляет наибольший набор строк, которые обе версии разделяют по порядку. Обратный проход по этой таблице даёт те операции, которые вы видите: строки, существующие только в левом тексте, помечаются красным как удалённые, строки только в правом — зелёным как добавленные, а общие строки остаются нейтральными, каждая со своим исходным номером строки.',
        how_p2='Сравнение на уровне строк — это осознанный компромисс. Посимвольные диффы могут показать, что внутри строки изменилось одно слово, но на реальных документах они вырождаются в конфетти: сотни крошечных фрагментов, которые читать сложнее, чем просто увидеть удалённую старую строку и добавленную новую. Построчный вывод остаётся читаемым и напрямую соответствует тому, как код-ревью и системы контроля версий представляют изменения. Два флажка настраивают, что значит «равно»: игнорировать пробелы схлопывает последовательности пробелов и обрезает концы строк перед сравнением (отлично для переформатированного кода), а игнорировать регистр приводит обе стороны к нижнему регистру. Отображаемые строки в любом случае сохраняют исходное форматирование.',
        how_p3="Поскольку таблица динамического программирования требует памяти и времени, пропорциональных (строки в A) x (строки в B), инструмент ограничивает ввод 4000 строками на сторону; свыше этого одна только таблица содержала бы десятки миллионов ячеек, и вкладка бы зависала. В пределах лимита всё выполняется синхронно в вашем браузере: оба текста существуют только в вашей вкладке, при наборе не отправляется ни одного запроса (проверьте панель Network в DevTools), а конфиденциальные черновики или конфигурации никогда не касаются сервера.",
    ),
    related_tools=[
        ("json-diff.html", "Сравнение JSON", "Сравните два JSON-документа."),
        ("remove-duplicate-lines.html", "Удаление дублирующихся строк", "Удаление дубликатов до или после сортировки."),
        ("sort-lines.html", "Сортировка строк", "Сортировка строк текста по алфавиту или по числам."),
    ],
)

PAGES["ja"] = dict(
    title="テキスト差分チェッカー：2つのテキストをオンライン比較 | norito",
    meta_desc="2つのテキストブロックを行単位で比較し、変更点を正確に表示。空白や大文字小文字を無視、差分をコピー。すべてブラウザ内で完結します。",
    app_name="テキスト差分チェッカー", h1="テキスト差分チェッカー", breadcrumb_label="テキスト差分チェッカー",
    lede="2つのテキストブロックを行単位で比較し、追加、削除、変更なしの箇所を正確に確認できます。",
    t=dict(
        ignore_ws="空白を無視", ignore_case="大文字小文字を無視",
        original="変更前", changed="変更後",
        ph_a="変更前のテキストを貼り付け...", ph_b="変更後のテキストを貼り付け...",
        too_large="どちらかのテキストが4,000行を超えています。より小さいセクションで比較してください。",
        empty_state="両方のボックスにテキストを貼り付けると、行単位の比較が表示されます。",
        copy_diff="差分をテキストとしてコピー",
        how_h2="仕組み",
        how_p1='この比較は最長共通部分列（LCS）アルゴリズムに基づく行レベルの差分計算で、<code>git diff</code>の背後にあるロジックと同じ系統のものです。両方のテキストは行に分割され、動的計画法のテーブルによって両バージョンが順序を保って共有する最大の行の集合が求められます。このテーブルを逆にたどることで、表示される操作が得られます。左側のテキストにしか存在しない行は削除として赤で、右側にしか存在しない行は追加として緑でマークされ、共通の行はニュートラルなまま、それぞれ元の行番号を保持します。',
        how_p2='行レベルでの差分表示は意図的なトレードオフです。文字レベルの差分は行内の1単語の変更を示せますが、実際のドキュメントでは無数の小さな断片に分解されてしまい、単に旧行の削除と新行の追加を見るよりもかえって読みづらくなります。行レベルの出力は読みやすさを保ち、コードレビューやバージョン管理が変更を提示する方法にそのまま対応します。2つのチェックボックスは「等しい」の意味を調整します。空白を無視は比較前に連続する空白をまとめ行末をトリムします（再フォーマットされたコードに最適）。大文字小文字を無視は両側を小文字に変換します。表示される行はいずれの場合も元の書式を保持します。',
        how_p3="動的計画法テーブルは（Aの行数）×（Bの行数）に比例したメモリと時間を要するため、このツールは各側の入力を4,000行に制限しています。それを超えるとテーブルだけで数千万セルになり、タブがフリーズしてしまいます。制限内であれば、すべての処理はブラウザ内で同期的に実行されます。両方のテキストはタブ内にのみ存在し、入力してもリクエストは一切発生しません（DevToolsのNetworkパネルで確認できます）。機密性の高い下書きや設定がサーバーに触れることは一切ありません。",
    ),
    related_tools=[
        ("json-diff.html", "JSON差分ツール", "2つのJSONドキュメントを比較。"),
        ("remove-duplicate-lines.html", "重複行の削除", "並べ替えの前後でリストの重複を削除。"),
        ("sort-lines.html", "行の並べ替え", "テキストの行をアルファベット順または数値順に並べ替え。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "text-diff.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-text-diff.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/text-diff.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
