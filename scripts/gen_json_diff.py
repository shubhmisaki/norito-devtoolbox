#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/></svg>'
ICON_CLASS = "c-indigo"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field-row">
          <div class="field" style="flex:1;">
            <label for="leftInput">{t['left_json']}</label>
            <textarea id="leftInput" class="mono-output" rows="12" spellcheck="false">{t['left_sample']}</textarea>
          </div>
          <div class="field" style="flex:1;">
            <label for="rightInput">{t['right_json']}</label>
            <textarea id="rightInput" class="mono-output" rows="12" spellcheck="false">{t['right_sample']}</textarea>
          </div>
        </div>
        <button id="diffBtn" style="margin-top:8px;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/></svg>
          {t['compare']}
        </button>
        <div class="result-box" id="result" style="display:none;"></div>
        <div id="diffOutput" style="margin-top:12px;"></div>
      </div>

      <div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['side_h']}</h3>
          <p class="note" style="margin-top:0;">
            {t['side_body']}
          </p>
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
    title="JSON Diff: Compara Dos Archivos JSON Online | norito",
    meta_desc="Compara dos documentos JSON y ve exactamente qué se añadió, eliminó, y cambió, en tu navegador. No se sube nada.",
    app_name="JSON Diff", h1="JSON Diff", breadcrumb_label="JSON Diff",
    lede="Pega dos documentos JSON y ve exactamente qué claves se añadieron, eliminaron, o cambiaron entre ellos.",
    t=dict(
        left_json="JSON izquierdo", right_json="JSON derecho",
        left_sample='{\n  "name": "norito",\n  "version": 1,\n  "tools": ["compress", "resize"]\n}',
        right_sample='{\n  "name": "norito",\n  "version": 2,\n  "tools": ["compress", "resize", "crop"]\n}',
        compare="Comparar",
        side_h="Cómo funciona esto",
        side_body="Ambos lados se analizan como JSON, luego se comparan clave por clave e índice por índice. Las claves que solo están a la derecha son adiciones, las que solo están a la izquierda son eliminaciones, y las claves presentes en ambos lados con valores diferentes son cambios. El orden de las claves del objeto no importa, solo los valores.",
        how_h2="Cómo funciona",
        how_p1='Ambos lados pasan primero por <code>JSON.parse</code>, así que si uno no es JSON válido obtienes el propio mensaje de error del parser señalando el problema en vez de un diff inservible. La comparación recorre entonces las dos estructuras analizadas recursivamente: para objetos toma la unión de ambos conjuntos de claves y recurre en cada clave, para arrays compara índice por índice, y los valores hoja se consideran iguales solo si se serializan de forma idéntica. Cada diferencia se emite como una ruta tipo <code>user.address[1].zip</code> etiquetada como añadida, eliminada, o cambiada, y luego se resume en conteos.',
        how_p2='Como el diff se ejecuta sobre valores analizados en vez de texto, el formato es invisible: la indentación, el orden de claves, y las diferencias de espacios en blanco no producen ruido alguno, que es el punto entero frente a un diff de texto basado en líneas. El compromiso a entender es la alineación de arrays. Es posicional, así que insertar un elemento al principio de un array largo reporta cada índice siguiente como "cambiado" más una adición al final. Cuando veas una pared de entradas cambiadas que parecen todas desplazadas por uno, léelo como "algo se insertó o eliminó al principio de este array", no como docenas de ediciones independientes.',
        how_p3='El análisis y la comparación ocurren por completo en el JavaScript de esta página. Abre la pestaña Red de las DevTools y pulsa Comparar: ninguna petición transporta tu JSON, así que las respuestas de API y archivos de configuración con secretos se quedan en tu máquina.',
    ),
    related_tools=[
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica un único documento JSON."),
        ("base64-encoder.html", "Codificar / Decodificar Base64", "Convierte texto a y desde Base64."),
        ("regex-tester.html", "Probador de Regex", "Prueba una expresión regular contra un texto de muestra en vivo."),
    ],
)

PAGES["zh"] = dict(
    title="JSON Diff：在线比较两个 JSON 文件 | norito",
    meta_desc="比较两个 JSON 文档，精确查看新增、删除和修改的内容，全部在浏览器中完成。不上传任何内容。",
    app_name="JSON Diff", h1="JSON Diff", breadcrumb_label="JSON Diff",
    lede="粘贴两个 JSON 文档，精确查看它们之间哪些键被添加、删除或更改。",
    t=dict(
        left_json="左侧 JSON", right_json="右侧 JSON",
        left_sample='{\n  "name": "norito",\n  "version": 1,\n  "tools": ["compress", "resize"]\n}',
        right_sample='{\n  "name": "norito",\n  "version": 2,\n  "tools": ["compress", "resize", "crop"]\n}',
        compare="比较",
        side_h="工作方式",
        side_body="两侧都会被解析为 JSON，然后逐键、逐索引进行比较。只出现在右侧的键为新增，只出现在左侧的键为删除，两侧都存在但值不同的键为修改。对象键的顺序不重要，重要的只是值。",
        how_h2="工作原理",
        how_p1='两侧都会先经过 <code>JSON.parse</code>，因此如果其中一方不是有效的 JSON，你会得到解析器自身指出问题所在的错误消息，而不是一份毫无意义的差异结果。然后，比较过程会递归遍历两个解析后的结构：对于对象，会取两个键集合的并集并对每个键递归比较；对于数组，会逐个索引进行比较；叶子值只有在序列化结果完全一致时才被视为相等。每一处差异都会以类似 <code>user.address[1].zip</code> 的路径形式输出，并标记为新增、删除或修改，最后汇总成计数。',
        how_p2='由于差异比较是针对解析后的值而非文本进行的，格式差异是不可见的：缩进、键的顺序以及空白字符的差异都不会产生任何噪音，这正是相较于基于行的文本差异工具的核心优势所在。需要理解的一个权衡是数组的对齐方式。它是按位置比较的，因此在一个较长的数组开头插入一个元素，会导致后面每个索引都被报告为「已修改」，外加末尾一处新增。当你看到一大片看起来整体错位了一位的修改条目时，应把它理解为「这个数组早期插入或删除了某个元素」，而不是数十处独立的编辑。',
        how_p3='解析和比较都完全在这个页面的 JavaScript 中进行。打开开发者工具的 Network 标签页并点击「比较」：不会有任何请求携带你的 JSON，因此包含密钥的 API 响应和配置文件都只留在你的电脑上。',
    ),
    related_tools=[
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩单个 JSON 文档。"),
        ("base64-encoder.html", "Base64 编码 / 解码", "文本与 Base64 互转。"),
        ("regex-tester.html", "正则表达式测试工具", "针对示例文本实时测试正则表达式。"),
    ],
)

PAGES["ar"] = dict(
    title="أداة مقارنة JSON: قارن ملفي JSON أونلاين | norito",
    meta_desc="قارن مستندي JSON وشاهد بالضبط ما أُضيف وحُذف وتغيّر، مباشرة في متصفحك. لا شيء يُرفَع.",
    app_name="أداة مقارنة JSON", h1="أداة مقارنة JSON", breadcrumb_label="أداة مقارنة JSON",
    lede="الصق مستندي JSON وشاهد بالضبط أي مفاتيح أُضيفت أو حُذفت أو تغيّرت بينهما.",
    t=dict(
        left_json="JSON الأيسر", right_json="JSON الأيمن",
        left_sample='{\n  "name": "norito",\n  "version": 1,\n  "tools": ["compress", "resize"]\n}',
        right_sample='{\n  "name": "norito",\n  "version": 2,\n  "tools": ["compress", "resize", "crop"]\n}',
        compare="مقارنة",
        side_h="كيف يعمل هذا",
        side_body="يُحلَّل الجانبان كـ JSON، ثم يُقارَنان مفتاحًا بمفتاح وفهرسًا بفهرس. المفاتيح الموجودة في اليمين فقط هي إضافات، والموجودة في اليسار فقط هي حذوفات، والمفاتيح الموجودة في كلا الجانبين بقيم مختلفة هي تغييرات. ترتيب مفاتيح الكائن لا يهم، القيم فقط هي المهمة.",
        how_h2="كيف يعمل",
        how_p1='يمرّ كلا الجانبين أولًا عبر <code>JSON.parse</code>، لذا إذا لم يكن أحدهما JSON صالحًا، تحصل على رسالة خطأ المحلِّل نفسها تشير إلى المشكلة بدلًا من فرق عديم الفائدة. تمرّ المقارنة بعدها عبر البنيتين المحلَّلتين بشكل تكراري: بالنسبة للكائنات، تأخذ اتحاد مجموعتي المفاتيح وتتكرر في كل مفتاح، وبالنسبة للمصفوفات، تقارن فهرسًا بفهرس، وتُعتبَر القيم الطرفية متساوية فقط إذا تسلسلت بشكل متطابق. يُصدَر كل فرق كمسار مثل <code>user.address[1].zip</code> موسومًا بأنه مُضاف أو محذوف أو مُغيَّر، ثم يُلخَّص في أعداد.',
        how_p2='بما أن الفرق يعمل على قيم محلَّلة وليس نصًا، فإن التنسيق غير مرئي: المسافات البادئة، وترتيب المفاتيح، واختلافات المسافات البيضاء لا تُنتِج أي ضجيج، وهذا هو بيت القصيد مقارنة بفرق نصي قائم على الأسطر. المفاضلة التي يجب فهمها هي محاذاة المصفوفات. إنها موضعية، لذا فإن إدراج عنصر واحد في مقدمة مصفوفة طويلة يُبلِغ عن كل فهرس تالٍ بأنه «مُغيَّر» بالإضافة إلى إضافة واحدة في النهاية. عندما ترى جدارًا من الإدخالات المُغيَّرة التي تبدو جميعها منزاحة بواحد، اقرأها على أنها «شيء أُدرِج أو حُذِف مبكرًا في هذه المصفوفة»، وليس كعشرات التعديلات المستقلة.',
        how_p3='يحدث التحليل والمقارنة بالكامل في جافاسكريبت هذه الصفحة. افتح لسان Network في أدوات المطوّر واضغط مقارنة: لا يحمل أي طلب JSON الخاص بك، لذا تبقى استجابات API وملفات الإعدادات التي تحتوي أسرارًا على جهازك.',
    ),
    related_tools=[
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق وضغط مستند JSON واحد."),
        ("base64-encoder.html", "ترميز / فك ترميز Base64", "حوّل النص من وإلى Base64."),
        ("regex-tester.html", "أداة اختبار Regex", "اختبر تعبيرًا نمطيًا مقابل نص عينة مباشرة."),
    ],
)

PAGES["hi"] = dict(
    title="JSON डिफ: दो JSON फ़ाइलों को ऑनलाइन कंपेयर करें | norito",
    meta_desc="दो JSON डॉक्यूमेंट्स को कंपेयर करें और देखें कि क्या जोड़ा गया, हटाया गया, और बदला गया, आपके ब्राउज़र में ही। कुछ भी अपलोड नहीं होता।",
    app_name="JSON डिफ", h1="JSON डिफ", breadcrumb_label="JSON डिफ",
    lede="दो JSON डॉक्यूमेंट्स पेस्ट करें और देखें कि उनके बीच कौन-सी कीज़ जोड़ी गईं, हटाई गईं, या बदली गईं।",
    t=dict(
        left_json="बायां JSON", right_json="दायां JSON",
        left_sample='{\n  "name": "norito",\n  "version": 1,\n  "tools": ["compress", "resize"]\n}',
        right_sample='{\n  "name": "norito",\n  "version": 2,\n  "tools": ["compress", "resize", "crop"]\n}',
        compare="कंपेयर करें",
        side_h="यह कैसे काम करता है",
        side_body="दोनों तरफ़ को JSON के रूप में पार्स किया जाता है, फिर की-बाय-की और इंडेक्स-बाय-इंडेक्स कंपेयर किया जाता है। सिर्फ़ दाईं तरफ़ मौजूद कीज़ एडिशन हैं, सिर्फ़ बाईं तरफ़ मौजूद कीज़ रिमूवल हैं, और दोनों तरफ़ अलग-अलग वैल्यूज़ के साथ मौजूद कीज़ चेंजेज़ हैं। ऑब्जेक्ट कीज़ का ऑर्डर मायने नहीं रखता, सिर्फ़ वैल्यूज़ मायने रखती हैं।",
        how_h2="यह कैसे काम करता है",
        how_p1='दोनों तरफ़ पहले <code>JSON.parse</code> से गुज़रती हैं, इसलिए अगर कोई एक वैलिड JSON नहीं है, तो आपको एक कचरा डिफ़ के बजाय पार्सर का अपना एरर मैसेज मिलता है जो समस्या की ओर इशारा करता है। कंपैरिज़न फिर दोनों पार्स की गई स्ट्रक्चर्स को रिकर्सिवली चलता है: ऑब्जेक्ट्स के लिए यह दोनों की सेट्स का यूनियन लेता है और हर की में रिकर्स करता है, ऐरेज़ के लिए यह इंडेक्स-बाय-इंडेक्स कंपेयर करता है, और लीफ़ वैल्यूज़ को बराबर तभी माना जाता है जब वे बिल्कुल एक जैसी सीरियलाइज़ हों। हर अंतर को <code>user.address[1].zip</code> जैसे पाथ के रूप में एडेड, रिमूव्ड, या चेंज्ड टैग के साथ जारी किया जाता है, फिर काउंट्स में समराइज़ किया जाता है।',
        how_p2='क्योंकि डिफ़ टेक्स्ट के बजाय पार्स की गई वैल्यूज़ पर चलता है, फ़ॉर्मैटिंग इनविज़िबल होती है: इंडेंटेशन, की ऑर्डर, और व्हाइटस्पेस के अंतर से बिल्कुल भी शोर पैदा नहीं होता, जो लाइन-बेस्ड टेक्स्ट डिफ़ के मुक़ाबले पूरा मक़सद है। समझने लायक ट्रेडऑफ़ है ऐरे अलाइनमेंट। यह पोज़िशनल है, इसलिए एक लंबे ऐरे के आगे एक एलिमेंट इंसर्ट करने पर हर आगे वाला इंडेक्स "changed" के रूप में रिपोर्ट होता है, साथ ही आख़िर में एक एडिशन। जब आप ऐसी बहुत सारी चेंज्ड एंट्रीज़ की दीवार देखें जो सभी एक से शिफ़्ट हुई लगें, तो इसे "इस ऐरे में शुरुआत में कुछ इंसर्ट या रिमूव हुआ" के रूप में पढ़ें, दर्जनों इंडिपेंडेंट एडिट्स के रूप में नहीं।',
        how_p3='पार्सिंग और कंपैरिज़न पूरी तरह इस पेज के JavaScript में होते हैं। डेवटूल्स का Network टैब खोलें और Compare दबाएं: कोई रिक्वेस्ट आपका JSON नहीं ले जाती, इसलिए सीक्रेट्स वाले API रिस्पॉन्सेज़ और कॉन्फ़िग फ़ाइलें आपकी मशीन पर ही रहती हैं।',
    ),
    related_tools=[
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "एक सिंगल JSON डॉक्यूमेंट को फ़ॉर्मैट, वैलिडेट और मिनिफ़ाई करें।"),
        ("base64-encoder.html", "Base64 एनकोड / डिकोड", "टेक्स्ट को Base64 में और वापस बदलें।"),
        ("regex-tester.html", "Regex टेस्टर", "सैंपल टेक्स्ट के खिलाफ़ एक रेगुलर एक्सप्रेशन लाइव टेस्ट करें।"),
    ],
)

PAGES["ru"] = dict(
    title="JSON Diff: сравните два JSON-файла онлайн | norito",
    meta_desc="Сравните два JSON-документа и увидьте точно, что было добавлено, удалено и изменено, прямо в браузере. Ничего не загружается.",
    app_name="JSON Diff", h1="JSON Diff", breadcrumb_label="JSON Diff",
    lede="Вставьте два JSON-документа и точно увидьте, какие ключи были добавлены, удалены или изменены между ними.",
    t=dict(
        left_json="Левый JSON", right_json="Правый JSON",
        left_sample='{\n  "name": "norito",\n  "version": 1,\n  "tools": ["compress", "resize"]\n}',
        right_sample='{\n  "name": "norito",\n  "version": 2,\n  "tools": ["compress", "resize", "crop"]\n}',
        compare="Сравнить",
        side_h="Как это работает",
        side_body="Обе стороны разбираются как JSON, затем сравниваются ключ за ключом и индекс за индексом. Ключи только справа — это добавления, ключи только слева — удаления, а ключи, присутствующие с обеих сторон с разными значениями, — изменения. Порядок ключей объекта не важен, важны только значения.",
        how_h2="Как это работает",
        how_p1='Обе стороны сначала проходят через <code>JSON.parse</code>, поэтому если одна из них не является допустимым JSON, вы получаете собственное сообщение об ошибке парсера, указывающее на проблему, а не бессмысленный diff. Затем сравнение рекурсивно обходит две разобранные структуры: для объектов берётся объединение обоих наборов ключей и рекурсия по каждому ключу, для массивов сравнение идёт индекс за индексом, а листовые значения считаются равными только при полностью идентичной сериализации. Каждое различие выводится в виде пути вроде <code>user.address[1].zip</code>, помеченного как добавленное, удалённое или изменённое, а затем суммируется в счётчики.',
        how_p2='Поскольку сравнение выполняется по разобранным значениям, а не по тексту, форматирование становится невидимым: отступы, порядок ключей и различия в пробелах не создают никакого шума, что и есть весь смысл по сравнению с построчным текстовым diff. Компромисс, который стоит понимать, — это позиционное выравнивание массивов. Вставка одного элемента в начало длинного массива приводит к тому, что каждый последующий индекс сообщается как «изменённый», плюс одно добавление в конце. Когда вы видите стену изменённых записей, которые все выглядят сдвинутыми на единицу, читайте это как «что-то было вставлено или удалено в начале этого массива», а не как десятки независимых правок.',
        how_p3='Разбор и сравнение полностью выполняются в JavaScript этой страницы. Откройте вкладку Network в DevTools и нажмите «Сравнить»: ни один запрос не передаёт ваш JSON, поэтому ответы API и конфигурационные файлы с секретами остаются на вашем компьютере.',
    ),
    related_tools=[
        ("json-formatter.html", "Форматирование JSON", "Форматирует, проверяет и минифицирует один JSON-документ."),
        ("base64-encoder.html", "Кодировщик / декодировщик Base64", "Преобразование текста в Base64 и обратно."),
        ("regex-tester.html", "Тестер регулярных выражений", "Проверьте регулярное выражение на образце текста в реальном времени."),
    ],
)

PAGES["ja"] = dict(
    title="JSON Diff：2つのJSONファイルをオンラインで比較 | norito",
    meta_desc="2つのJSONドキュメントを比較し、追加・削除・変更された内容を正確に確認。すべてブラウザ内で完結します。アップロードなし。",
    app_name="JSON Diff", h1="JSON Diff", breadcrumb_label="JSON Diff",
    lede="2つのJSONドキュメントを貼り付けると、その間でどのキーが追加、削除、変更されたかを正確に確認できます。",
    t=dict(
        left_json="左側のJSON", right_json="右側のJSON",
        left_sample='{\n  "name": "norito",\n  "version": 1,\n  "tools": ["compress", "resize"]\n}',
        right_sample='{\n  "name": "norito",\n  "version": 2,\n  "tools": ["compress", "resize", "crop"]\n}',
        compare="比較する",
        side_h="仕組み",
        side_body="両方の入力はJSONとして解析され、その後キーごと、インデックスごとに比較されます。右側にのみ存在するキーは追加、左側にのみ存在するキーは削除、両側に存在するが値が異なるキーは変更として扱われます。オブジェクトのキーの順序は関係なく、値だけが問題になります。",
        how_h2="仕組み",
        how_p1='両方の入力はまず<code>JSON.parse</code>を通ります。そのため、どちらかが有効なJSONでない場合、意味のないdiffの代わりに、パーサー自身が問題を指し示すエラーメッセージが表示されます。比較処理は、解析された2つの構造を再帰的にたどります。オブジェクトの場合は両方のキー集合の和集合を取り各キーに再帰し、配列の場合はインデックスごとに比較し、末端の値は完全に同一にシリアライズされる場合にのみ等しいとみなされます。すべての差異は<code>user.address[1].zip</code>のようなパスとして出力され、追加・削除・変更のいずれかにタグ付けされ、最後に件数として集計されます。',
        how_p2='diffはテキストではなく解析された値に対して実行されるため、フォーマットの違いは見えません。インデント、キーの順序、空白の違いはノイズを一切生みません。これこそが行ベースのテキストdiffに対する最大の利点です。理解しておくべきトレードオフは配列の位置合わせです。これは位置ベースであるため、長い配列の先頭に1つの要素を挿入すると、それ以降のすべてのインデックスが「変更」として報告され、末尾に1つの追加が加わります。すべてが1つずつずれているように見える大量の変更エントリを目にしたら、それを数十件の独立した編集としてではなく、「この配列の早い段階で何かが挿入または削除された」と読み取ってください。',
        how_p3='解析と比較は、すべてこのページのJavaScript内で行われます。DevToolsのNetworkタブを開いて「比較する」をクリックしてみてください。あなたのJSONを運ぶリクエストは一切発生しないため、秘密情報を含むAPIレスポンスや設定ファイルはあなたのマシン内にとどまります。',
    ),
    related_tools=[
        ("json-formatter.html", "JSONフォーマッタ", "単一のJSONドキュメントを整形・検証・圧縮。"),
        ("base64-encoder.html", "Base64 エンコード / デコード", "テキストを Base64 との間で変換。"),
        ("regex-tester.html", "正規表現テストツール", "サンプルテキストに対して正規表現をリアルタイムでテスト。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "json-diff.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-json-diff.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/json-diff.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
