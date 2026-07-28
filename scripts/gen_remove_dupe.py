#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2h8c1.1 0 2 .9 2 2"/></svg>'
ICON_CLASS = "c-teal"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field">
          <label for="textInput">{t['input_label']}</label>
          <textarea id="textInput" class="mono-output" rows="12" placeholder="{t['placeholder']}"></textarea>
        </div>
        <div class="option-row">
          <span class="option-label">{t['case_sensitive']}</span>
          <label class="switch"><input type="checkbox" id="optCaseSensitive" /><span class="track"></span></label>
        </div>
        <div class="option-row">
          <span class="option-label">{t['trim']}</span>
          <label class="switch"><input type="checkbox" id="optTrimLines" checked /><span class="track"></span></label>
        </div>
        <div class="option-row" style="margin-bottom:20px;">
          <span class="option-label">{t['remove_blank']}</span>
          <label class="switch"><input type="checkbox" id="optRemoveBlank" checked /><span class="track"></span></label>
        </div>
      </div>

      <div>
        <div class="panel">
          <div class="field">
            <label for="textOutput">{t['result']}</label>
            <textarea id="textOutput" class="mono-output" rows="12" readonly></textarea>
          </div>
          <p class="note" id="statRemoved" style="margin-top:0;">{t['zero_removed']}</p>
          <button id="copyBtn">{t['copy_result']}</button>
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
    title="Eliminar líneas duplicadas online | norito",
    meta_desc="Elimina líneas duplicadas de una lista, directamente en tu navegador. Alternar sensibilidad a mayúsculas, recortar espacios, eliminar líneas en blanco. No se sube nada.",
    app_name="Eliminar líneas duplicadas", h1="Eliminar líneas duplicadas", breadcrumb_label="Eliminar líneas duplicadas",
    lede="Pega una lista y elimina las líneas duplicadas, conservando la primera aparición de cada una. Incluye alternar sensibilidad a mayúsculas y limpieza de líneas en blanco.",
    t=dict(
        input_label="Entrada (un elemento por línea)", placeholder="manzana\nplátano\nmanzana\ncereza",
        case_sensitive="Sensible a mayúsculas", trim="Recortar espacios en cada línea", remove_blank="Eliminar líneas en blanco",
        result="Resultado", zero_removed="0 líneas duplicadas eliminadas.", copy_result="Copiar resultado",
        how_h2="Cómo funciona",
        how_p1='La herramienta divide tu texto por saltos de línea y luego recorre las líneas una vez con un <code>Set</code> de JavaScript que va registrando lo que ya ha visto. La primera aparición de cada línea se conserva en su posición original; las repeticiones posteriores se descartan. Como es un único recorrido con búsquedas de tiempo constante, incluso decenas de miles de líneas se deduplican al instante, y a diferencia del clásico truco de shell <code>sort | uniq</code>, tu orden de líneas se conserva: nada se ordena alfabéticamente como efecto secundario.',
        how_p2='Las opciones cambian qué cuenta como "la misma línea". Con la sensibilidad a mayúsculas desactivada, cada línea se convierte a minúsculas antes de la comparación (la línea conservada sigue mostrando su capitalización original). "Recortar espacios" elimina primero los espacios y tabulaciones al principio y al final, algo que importa más de lo que parece: dos líneas pueden verse idénticas en pantalla pero diferir por un espacio o una tabulación al final, y una comparación byte a byte las trata como distintas. Si tus duplicados no se detectan, casi siempre es por espacios invisibles, y recortarlos lo soluciona. La eliminación de líneas en blanco se ejecuta antes de deduplicar, así que una línea vacía suelta no sobrevive como "la primera en blanco".',
        how_p3="El procesamiento son unas pocas líneas de JavaScript que operan sobre el texto que ya está en tu pestaña. No se sube nada: abre las herramientas de desarrollador, cambia a la pestaña Red, y pega o edita todo lo que quieras. Nunca se dispara ninguna petición, y la herramienta funciona sin conexión una vez que la página se ha cargado, algo que importa si estás limpiando listas que contienen correos, URLs, o cualquier otra cosa que prefieras no enviar a un servidor cualquiera.",
    ),
    related_tools=[
        ("sort-lines.html", "Ordenar líneas", "Ordena alfabéticamente, invierte o mezcla una lista de líneas."),
        ("/case-converter.html", "Conversor de mayúsculas/minúsculas", "Convierte texto entre mayúsculas, minúsculas, camelCase y más."),
        ("word-counter.html", "Contador de palabras", "Cuenta palabras, caracteres y tiempo de lectura."),
    ],
)

PAGES["zh"] = dict(
    title="在线删除重复行 | norito",
    meta_desc="直接在浏览器中从列表中删除重复行。支持区分大小写开关、去除空白、删除空行。不会上传任何内容。",
    app_name="删除重复行", h1="删除重复行", breadcrumb_label="删除重复行",
    lede="粘贴一个列表并删除重复行，保留每一项的首次出现。内置区分大小写开关和空行清理功能。",
    t=dict(
        input_label="输入内容（每行一项）", placeholder="苹果\n香蕉\n苹果\n樱桃",
        case_sensitive="区分大小写", trim="去除每行首尾空白", remove_blank="删除空行",
        result="结果", zero_removed="已删除 0 行重复内容。", copy_result="复制结果",
        how_h2="工作原理",
        how_p1='这个工具会按换行符拆分你的文本，然后用一个 JavaScript <code>Set</code> 遍历所有行一次，记录已经出现过的内容。每一行的首次出现会保留在其原始位置；之后的重复项会被删除。由于只需一次遍历并且查找是常数时间，即使是数万行也能瞬间完成去重；而且与经典的 shell 命令 <code>sort | uniq</code> 不同，你的行顺序会被保留下来：不会作为副作用而被按字母排序。',
        how_p2='这些选项决定了什么算作"相同的行"。关闭区分大小写后，比较前每一行都会先转为小写（保留的那一行仍然显示原始大小写）。"去除空白"会先去掉每行开头和结尾的空格与制表符，这一点比你想象的更重要：两行在屏幕上看起来完全一样，却可能因为结尾多了一个空格或制表符而不同，逐字节比较会把它们当作不同的行。如果你的重复项没有被检测到，几乎总是因为看不见的空白字符，而去除空白正好能解决这个问题。空行删除是在去重之前进行的，所以单独一个空行不会作为"第一个空行"被保留下来。',
        how_p3="整个处理过程只是对你标签页里已有文本运行的几行 JavaScript 代码。不会上传任何内容：打开开发者工具，切换到网络面板，随意粘贴或编辑。永远不会触发任何请求，页面加载完成后这个工具甚至可以离线使用——如果你要清理的列表包含邮箱、网址，或任何你不想发送给陌生服务器的内容，这一点就很重要。",
    ),
    related_tools=[
        ("sort-lines.html", "行排序", "按字母排序、反转或随机打乱一列文本行。"),
        ("/case-converter.html", "大小写转换器", "在大写、小写、驼峰式等之间转换文本。"),
        ("word-counter.html", "字数统计", "统计单词数、字符数和阅读时间。"),
    ],
)

PAGES["ar"] = dict(
    title="إزالة الأسطر المكررة أونلاين | norito",
    meta_desc="أزل الأسطر المكررة من قائمة، مباشرةً في متصفحك. مفتاح حساسية حالة الأحرف، إزالة المسافات، إزالة الأسطر الفارغة. لا يُرفع أي شيء.",
    app_name="إزالة الأسطر المكررة", h1="إزالة الأسطر المكررة", breadcrumb_label="إزالة الأسطر المكررة",
    lede="الصق قائمة وأزل الأسطر المكررة، مع الاحتفاظ بأول ظهور لكل سطر. يتضمن مفتاح حساسية حالة الأحرف وتنظيف الأسطر الفارغة.",
    t=dict(
        input_label="الإدخال (عنصر واحد لكل سطر)", placeholder="تفاح\nموز\nتفاح\nكرز",
        case_sensitive="حساس لحالة الأحرف", trim="إزالة المسافات من كل سطر", remove_blank="إزالة الأسطر الفارغة",
        result="النتيجة", zero_removed="تمت إزالة 0 سطر مكرر.", copy_result="نسخ النتيجة",
        how_h2="كيف يعمل",
        how_p1='تقسّم الأداة نصك عند فواصل الأسطر، ثم تمرّ على الأسطر مرة واحدة باستخدام <code>Set</code> في جافاسكريبت يتتبّع ما رأته بالفعل. يُحتفَظ بأول ظهور لكل سطر في موضعه الأصلي؛ وتُحذف التكرارات اللاحقة. ولأنها عملية مرور واحدة بعمليات بحث ثابتة الزمن، حتى عشرات الآلاف من الأسطر تُزال تكراراتها فورًا، وعلى عكس حيلة الطرفية الكلاسيكية <code>sort | uniq</code>، يُحافَظ على ترتيب أسطرك: لا يُرتَّب شيء أبجديًا كأثر جانبي.',
        how_p2='تُغيّر الخيارات ما يُعتبر "السطر نفسه". عند إيقاف حساسية حالة الأحرف، يُحوَّل كل سطر إلى أحرف صغيرة قبل المقارنة (يظل السطر المحتفَظ به معروضًا بحالة أحرفه الأصلية). "إزالة المسافات" تحذف المسافات وعلامات التبويب البادئة واللاحقة أولًا، وهذا أهم مما قد تتوقع: يمكن أن يبدو سطران متطابقين تمامًا على الشاشة لكنهما يختلفان بمسافة أو تبويب لاحق، وتعاملهما المقارنة الدقيقة بايتًا ببايت كسطرين مختلفين. إذا لم تُكتشف التكرارات لديك، فالسبب غالبًا هو مسافات غير مرئية، وإزالة المسافات تحلّ المشكلة. تُنفَّذ إزالة الأسطر الفارغة قبل إزالة التكرار، لذا لا يبقى سطر فارغ منفرد باعتباره "الفارغ الأول".',
        how_p3="المعالجة هي بضعة أسطر من جافاسكريبت تعمل على النص الموجود بالفعل في تبويبك. لا يُرفع أي شيء: افتح أدوات المطوّر، انتقل إلى تبويب الشبكة، والصق أو عدّل كما تشاء. لن يُطلق أي طلب مطلقًا، وتعمل الأداة دون اتصال بمجرد تحميل الصفحة، وهذا مهم إذا كنت تنظّف قوائم تحتوي على رسائل بريد إلكتروني أو روابط أو أي شيء آخر تفضّل عدم إرساله إلى خادم عشوائي.",
    ),
    related_tools=[
        ("sort-lines.html", "ترتيب الأسطر", "رتّب أبجديًا، أو اعكس، أو اخلط قائمة من الأسطر."),
        ("/case-converter.html", "محوّل حالة الأحرف", "حوّل النص بين الأحرف الكبيرة والصغيرة وcamelCase والمزيد."),
        ("word-counter.html", "عدّاد الكلمات", "عدّ الكلمات والأحرف ووقت القراءة."),
    ],
)

PAGES["hi"] = dict(
    title="डुप्लीकेट लाइनें हटाएं ऑनलाइन | norito",
    meta_desc="किसी लिस्ट से डुप्लीकेट लाइनें हटाएं, अपने ब्राउज़र में ही। केस-सेंसिटिव टॉगल, व्हाइटस्पेस ट्रिम, खाली लाइनें हटाएं। कुछ भी अपलोड नहीं होता।",
    app_name="डुप्लीकेट लाइनें हटाएं", h1="डुप्लीकेट लाइनें हटाएं", breadcrumb_label="डुप्लीकेट लाइनें हटाएं",
    lede="एक लिस्ट पेस्ट करें और डुप्लीकेट लाइनें हटाएं, हर एक की पहली मौजूदगी रखते हुए। केस-सेंसिटिव टॉगल और खाली-लाइन क्लीनअप शामिल है।",
    t=dict(
        input_label="इनपुट (प्रति लाइन एक आइटम)", placeholder="सेब\nकेला\nसेब\nचेरी",
        case_sensitive="केस-सेंसिटिव", trim="हर लाइन पर व्हाइटस्पेस ट्रिम करें", remove_blank="खाली लाइनें हटाएं",
        result="परिणाम", zero_removed="0 डुप्लीकेट लाइनें हटाई गईं।", copy_result="परिणाम कॉपी करें",
        how_h2="यह कैसे काम करता है",
        how_p1='यह टूल आपके टेक्स्ट को न्यूलाइन पर स्प्लिट करता है, फिर एक जावास्क्रिप्ट <code>Set</code> के साथ लाइनों पर एक बार चलता है जो ट्रैक रखता है कि वह पहले क्या देख चुका है। हर लाइन की पहली मौजूदगी उसकी मूल जगह पर रखी जाती है; बाद की रिपीट हटा दी जाती हैं। चूंकि यह कॉन्स्टेंट-टाइम लुकअप के साथ एक ही पास है, हज़ारों लाइनें भी तुरंत डीडुप्लीकेट हो जाती हैं, और क्लासिक शेल ट्रिक <code>sort | uniq</code> के उलट, आपकी लाइन का क्रम बना रहता है: साइड इफ़ेक्ट के तौर पर कुछ भी अल्फ़ाबेटिकली सॉर्ट नहीं होता।',
        how_p2='ऑप्शंस बदलते हैं कि "एक जैसी लाइन" क्या मानी जाए। केस सेंसिटिविटी बंद होने पर, तुलना से पहले हर लाइन को लोअरकेस कर दिया जाता है (रखी गई लाइन फिर भी अपना ओरिजिनल केस दिखाती है)। "व्हाइटस्पेस ट्रिम करें" पहले शुरुआती और आखिरी स्पेस और टैब हटाता है, जो आपकी सोच से कहीं ज़्यादा मायने रखता है: दो लाइनें स्क्रीन पर बिल्कुल एक जैसी दिख सकती हैं लेकिन आखिर में एक स्पेस या टैब की वजह से अलग हो सकती हैं, और बाइट-दर-बाइट तुलना उन्हें अलग मानती है। अगर आपके डुप्लीकेट पकड़ में नहीं आ रहे, तो लगभग हमेशा इनविज़िबल व्हाइटस्पेस ही वजह होती है, और ट्रिम करने से यह ठीक हो जाता है। खाली-लाइन हटाना डीडुप करने से पहले चलता है, इसलिए कोई अकेली खाली लाइन "पहली खाली" के तौर पर नहीं बचती।',
        how_p3="प्रोसेसिंग आपके टैब में पहले से मौजूद टेक्स्ट पर चलने वाली जावास्क्रिप्ट की कुछ लाइनें भर हैं। कुछ भी अपलोड नहीं होता: डेवलपर टूल्स खोलें, नेटवर्क टैब पर जाएं, और जितना चाहें पेस्ट या एडिट करें। कोई रिक्वेस्ट कभी फ़ायर नहीं होती, और पेज लोड होने के बाद यह टूल ऑफ़लाइन भी काम करता है, जो तब मायने रखता है जब आप ऐसी लिस्ट साफ़ कर रहे हों जिनमें ईमेल, URL, या कुछ भी ऐसा हो जिसे आप किसी रैंडम सर्वर पर नहीं भेजना चाहते।",
    ),
    related_tools=[
        ("sort-lines.html", "लाइनें सॉर्ट करें", "लाइनों की लिस्ट को अल्फ़ाबेटाइज़, रिवर्स, या शफ़ल करें।"),
        ("/case-converter.html", "केस कन्वर्टर", "टेक्स्ट को अपरकेस, लोअरकेस, camelCase और अन्य में बदलें।"),
        ("word-counter.html", "वर्ड काउंटर", "शब्द, कैरेक्टर, और पढ़ने का समय गिनें।"),
    ],
)

PAGES["ru"] = dict(
    title="Удаление дублирующихся строк онлайн | norito",
    meta_desc="Удаляйте дублирующиеся строки из списка прямо в браузере. Переключатель регистра, обрезка пробелов, удаление пустых строк. Ничего не загружается.",
    app_name="Удаление дублирующихся строк", h1="Удаление дублирующихся строк", breadcrumb_label="Удаление дублирующихся строк",
    lede="Вставьте список и удалите дублирующиеся строки, сохранив первое вхождение каждой. Включены переключатель учёта регистра и очистка пустых строк.",
    t=dict(
        input_label="Ввод (один элемент на строку)", placeholder="яблоко\nбанан\nяблоко\nвишня",
        case_sensitive="С учётом регистра", trim="Обрезать пробелы в каждой строке", remove_blank="Удалить пустые строки",
        result="Результат", zero_removed="Удалено 0 дублирующихся строк.", copy_result="Скопировать результат",
        how_h2="Как это работает",
        how_p1='Инструмент разбивает ваш текст по переносам строк, а затем проходит по строкам один раз с помощью <code>Set</code> в JavaScript, отслеживая, что уже встречалось. Первое вхождение каждой строки сохраняется в исходной позиции; последующие повторы удаляются. Поскольку это единственный проход с поиском за константное время, даже десятки тысяч строк дедуплицируются мгновенно, и, в отличие от классического приёма командной строки <code>sort | uniq</code>, порядок ваших строк сохраняется: ничего не сортируется по алфавиту в качестве побочного эффекта.',
        how_p2='Опции меняют то, что считается «одной и той же строкой». При отключённом учёте регистра каждая строка перед сравнением переводится в нижний регистр (сохранённая строка всё равно отображается с исходным регистром). «Обрезать пробелы» сначала убирает пробелы и табуляции в начале и конце — это важнее, чем кажется: две строки могут выглядеть на экране абсолютно одинаково, но отличаться завершающим пробелом или табуляцией, а побайтовое сравнение сочтёт их разными. Если ваши дубликаты не обнаруживаются, почти всегда причина — невидимые пробельные символы, и обрезка это исправляет. Удаление пустых строк выполняется до дедупликации, поэтому одна пустая строка не сохранится как «первая пустая».',
        how_p3="Обработка — это несколько строк JavaScript, работающих с текстом, уже находящимся в вашей вкладке. Ничего не загружается: откройте инструменты разработчика, переключитесь на вкладку «Сеть» и вставляйте или редактируйте сколько угодно. Ни один запрос никогда не отправляется, а инструмент работает офлайн после загрузки страницы — это важно, если вы очищаете списки, содержащие email-адреса, URL или что-то ещё, что вы предпочли бы не отправлять на случайный сервер.",
    ),
    related_tools=[
        ("sort-lines.html", "Сортировка строк", "Сортировка по алфавиту, разворот или перемешивание списка строк."),
        ("/case-converter.html", "Конвертер регистра", "Преобразование текста между верхним, нижним регистром, camelCase и другими."),
        ("word-counter.html", "Счётчик слов", "Подсчёт слов, символов и времени чтения."),
    ],
)

PAGES["ja"] = dict(
    title="重複行の削除オンライン | norito",
    meta_desc="リストから重複行をブラウザ内で削除。大文字小文字区別の切り替え、空白のトリム、空行の削除に対応。アップロードは一切行われません。",
    app_name="重複行の削除", h1="重複行の削除", breadcrumb_label="重複行の削除",
    lede="リストを貼り付けて重複行を削除し、それぞれ最初に出現したものを残します。大文字小文字区別の切り替えと空行のクリーンアップも含まれます。",
    t=dict(
        input_label="入力（1行に1項目）", placeholder="りんご\nバナナ\nりんご\nさくらんぼ",
        case_sensitive="大文字小文字を区別", trim="各行の空白をトリム", remove_blank="空行を削除",
        result="結果", zero_removed="0行の重複を削除しました。", copy_result="結果をコピー",
        how_h2="仕組み",
        how_p1='このツールはテキストを改行で分割し、その後JavaScriptの <code>Set</code> を使って一度だけ各行を走査し、すでに見た内容を記録します。各行の最初の出現は元の位置に保持され、それ以降の重複は削除されます。1回の走査で定数時間のルックアップを行うため、数万行でも即座に重複削除でき、古典的なシェルのテクニック <code>sort | uniq</code> とは異なり、行の順序も保持されます。副作用としてアルファベット順に並べ替えられることもありません。',
        how_p2='オプションによって「同じ行」とみなす基準が変わります。大文字小文字の区別をオフにすると、比較の前に各行が小文字に変換されます（保持される行は元の大文字小文字表記のまま表示されます）。「空白をトリム」は先頭と末尾のスペースやタブを最初に取り除きます。これは思っている以上に重要です。画面上ではピクセル単位で同じに見える2行でも、末尾のスペースやタブが原因で実際には異なることがあり、バイト単位の比較ではそれらは別の行として扱われます。重複が検出されない場合、ほとんどの場合は目に見えない空白が原因であり、トリムすることで解決します。空行の削除は重複削除の前に行われるため、単独の空行が「最初の空行」として残ることはありません。',
        how_p3="処理はタブ内にすでにあるテキストに対して実行される、ほんの数行のJavaScriptです。何もアップロードされません。開発者ツールを開き、ネットワークタブに切り替えて、好きなだけ貼り付けたり編集したりしてみてください。リクエストは一切発生せず、ページの読み込みが完了すればこのツールはオフラインでも動作します。これは、メールアドレスやURL、あるいは見知らぬサーバーには送りたくない情報を含むリストを整理する際に重要なポイントです。",
    ),
    related_tools=[
        ("sort-lines.html", "行の並べ替え", "行のリストをアルファベット順に並べ替え、反転、またはシャッフル。"),
        ("/case-converter.html", "大文字小文字変換ツール", "大文字、小文字、camelCaseなどの間でテキストを変換。"),
        ("word-counter.html", "単語数カウンター", "単語数、文字数、読了時間をカウント。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "remove-duplicate-lines.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-remove-duplicate-lines.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/remove-duplicate-lines.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
