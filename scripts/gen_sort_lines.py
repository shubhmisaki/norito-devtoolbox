#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m3 16 4 4 4-4"/><path d="M7 20V4"/><path d="M11 4h10"/><path d="M11 8h7"/><path d="M11 12h4"/></svg>'
ICON_CLASS = "c-purple"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field">
          <label for="textInput">{t['input_label']}</label>
          <textarea id="textInput" class="mono-output" rows="12" placeholder="{t['placeholder']}"></textarea>
        </div>
        <div class="field-row">
          <div class="field">
            <label for="sortBy">{t['sort_by']}</label>
            <select id="sortBy">
              <option value="alpha">{t['opt_alpha']}</option>
              <option value="alphaCI" selected>{t['opt_alpha_ci']}</option>
              <option value="numeric">{t['opt_numeric']}</option>
              <option value="length">{t['opt_length']}</option>
              <option value="shuffle">{t['opt_shuffle']}</option>
            </select>
          </div>
          <div class="field">
            <label for="direction">{t['direction']}</label>
            <select id="direction">
              <option value="asc" selected>{t['asc']}</option>
              <option value="desc">{t['desc']}</option>
            </select>
          </div>
        </div>
        <div class="option-row">
          <span class="option-label">{t['dedupe']}</span>
          <label class="switch"><input type="checkbox" id="optDedupe" /><span class="track"></span></label>
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
          <p class="note" id="statInfo" style="margin-top:0;">{t['zero_lines']}</p>
          <button id="sortNowBtn" class="secondary" style="margin-right:8px;">{t['sort_now']}</button>
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
    title="Ordenar líneas online: alfabético, numérico, aleatorio | norito",
    meta_desc="Ordena una lista de líneas alfabética o numéricamente, por longitud, o mézclala aleatoriamente, directamente en tu navegador. No se sube nada.",
    app_name="Ordenar líneas", h1="Ordenar líneas", breadcrumb_label="Ordenar líneas",
    lede="Ordena una lista alfabética o numéricamente, por longitud, o mézclala aleatoriamente. Ascendente o descendente, con eliminación de duplicados opcional.",
    t=dict(
        input_label="Entrada (un elemento por línea)", placeholder="plátano\nmanzana\ncereza",
        sort_by="Ordenar por", opt_alpha="Alfabético (sensible a mayúsculas)", opt_alpha_ci="Alfabético (ignorar mayúsculas)",
        opt_numeric="Numérico", opt_length="Longitud de línea", opt_shuffle="Mezclar aleatoriamente",
        direction="Dirección", asc="Ascendente", desc="Descendente",
        dedupe="Eliminar líneas duplicadas", remove_blank="Eliminar líneas en blanco",
        result="Resultado", zero_lines="0 líneas.", sort_now="Ordenar ahora", copy_result="Copiar resultado",
        how_h2="Cómo funciona",
        how_p1='Tu texto se divide por saltos de línea y se ordena con un comparador elegido según el menú desplegable. El orden alfabético usa <code>localeCompare</code>, la comparación consciente del idioma del navegador, en lugar de códigos de carácter en bruto. La diferencia se nota de inmediato: un ordenamiento ingenuo por punto de código pone toda letra mayúscula antes que cualquier minúscula (así que "Zebra" se ordena antes que "manzana"), y desordena los caracteres acentuados. La comparación consciente del idioma ordena las palabras como lo haría un diccionario.',
        how_p2='El orden numérico analiza cada línea con <code>parseFloat</code> y compara los números, lo que corrige el clásico error del ordenamiento de cadenas donde "10" va antes que "9" porque "1" es un carácter menor. Las líneas que no empiezan con un número se tratan como 0 y se agrupan juntas. El orden por longitud compara el número de caracteres, y la mezcla usa el algoritmo Fisher-Yates, que da a cada ordenación la misma probabilidad. Vale la pena aclararlo: el popular truco <code>sort(() =&gt; Math.random() - 0.5)</code> produce mezclas sesgadas porque los algoritmos de ordenamiento asumen un comparador consistente, mientras que Fisher-Yates recorre el array una sola vez, intercambiando cada elemento con una posición anterior elegida uniformemente al azar.',
        how_p3="El orden descendente ordena de forma ascendente y luego invierte, la eliminación de duplicados se ejecuta después de ordenar usando un <code>Set</code> para que solo se eliminen las repeticiones exactas, y las líneas en blanco pueden filtrarse antes de todo esto. Todo el proceso son operaciones de array sobre una cadena en tu pestaña: no se dispara ninguna petición al pegar u ordenar (verifícalo en el panel Red de las herramientas de desarrollador), así que ordenar una lista de nombres, correos o claves nunca involucra a un servidor.",
    ),
    related_tools=[
        ("remove-duplicate-lines.html", "Eliminar líneas duplicadas", "Elimina duplicados antes o después de ordenar."),
        ("/case-converter.html", "Conversor de mayúsculas/minúsculas", "Convierte texto entre mayúsculas, minúsculas, camelCase y más."),
        ("json-formatter.html", "Formateador JSON", "Formatea y valida JSON."),
    ],
)

PAGES["zh"] = dict(
    title="在线排序行：字母、数字、随机打乱 | norito",
    meta_desc="直接在浏览器中按字母、数字、长度排序一列文本行，或随机打乱。不会上传任何内容。",
    app_name="行排序", h1="行排序", breadcrumb_label="行排序",
    lede="按字母、数字或长度排序一个列表，或随机打乱它。支持升序或降序，以及可选的去重。",
    t=dict(
        input_label="输入内容（每行一项）", placeholder="香蕉\n苹果\n樱桃",
        sort_by="排序方式", opt_alpha="按字母（区分大小写）", opt_alpha_ci="按字母（忽略大小写）",
        opt_numeric="按数字", opt_length="按行长度", opt_shuffle="随机打乱",
        direction="方向", asc="升序", desc="降序",
        dedupe="删除重复行", remove_blank="删除空行",
        result="结果", zero_lines="0 行。", sort_now="立即排序", copy_result="复制结果",
        how_h2="工作原理",
        how_p1='你的文本会按换行符拆分，并用下拉菜单选择的比较器进行排序。字母排序使用 <code>localeCompare</code>，即浏览器提供的语言感知比较方式，而不是原始字符编码。这个区别立刻就能看出来：简单粗暴的按码位排序会把所有大写字母排在所有小写字母之前（所以 "Zebra" 会排在 "apple" 之前），并且会打乱带重音符号的字符顺序。语言感知比较会按照词典的方式排列单词。',
        how_p2='数字排序会用 <code>parseFloat</code> 解析每一行并比较数值，从而修正字符串排序中的经典问题——比如 "10" 会排在 "9" 前面，因为字符 "1" 比较小。不以数字开头的行会被当作 0 处理，并归到一起。长度排序比较字符数，随机打乱则使用 Fisher-Yates 算法，保证每种排列的概率相同。值得一提的是：流行的 <code>sort(() =&gt; Math.random() - 0.5)</code> 技巧会产生有偏差的打乱结果，因为排序算法假定比较器是一致的，而 Fisher-Yates 只遍历数组一次，每次都把当前元素与前面某个均匀随机选取的位置交换。',
        how_p3="降序是先升序排列再反转，去重是在排序之后用 <code>Set</code> 完成的，因此只会去掉完全相同的重复项，空行则可以在这一切之前就被过滤掉。整个流程都是在你的标签页里对一段字符串进行数组操作：粘贴或排序时不会触发任何请求（可在开发者工具的网络面板中验证），所以排序姓名、邮箱或密钥列表永远不会涉及服务器。",
    ),
    related_tools=[
        ("remove-duplicate-lines.html", "删除重复行", "在排序前后对列表去重。"),
        ("/case-converter.html", "大小写转换器", "在大写、小写、驼峰式等之间转换文本。"),
        ("json-formatter.html", "JSON 格式化", "格式化并校验 JSON。"),
    ],
)

PAGES["ar"] = dict(
    title="ترتيب الأسطر أونلاين: أبجديًا، رقميًا، عشوائيًا | norito",
    meta_desc="رتّب قائمة من الأسطر أبجديًا أو رقميًا أو حسب الطول، أو اخلطها عشوائيًا، مباشرةً في متصفحك. لا يُرفع أي شيء.",
    app_name="ترتيب الأسطر", h1="ترتيب الأسطر", breadcrumb_label="ترتيب الأسطر",
    lede="رتّب قائمة أبجديًا أو رقميًا أو حسب الطول، أو اخلطها عشوائيًا. تصاعديًا أو تنازليًا، مع إزالة اختيارية للتكرارات.",
    t=dict(
        input_label="الإدخال (عنصر واحد لكل سطر)", placeholder="موز\nتفاح\nكرز",
        sort_by="ترتيب حسب", opt_alpha="أبجدي (حساس لحالة الأحرف)", opt_alpha_ci="أبجدي (تجاهل حالة الأحرف)",
        opt_numeric="رقمي", opt_length="طول السطر", opt_shuffle="خلط عشوائي",
        direction="الاتجاه", asc="تصاعدي", desc="تنازلي",
        dedupe="إزالة الأسطر المكررة", remove_blank="إزالة الأسطر الفارغة",
        result="النتيجة", zero_lines="0 سطر.", sort_now="رتّب الآن", copy_result="نسخ النتيجة",
        how_h2="كيف يعمل",
        how_p1='يُقسَّم نصك عند فواصل الأسطر ويُرتَّب باستخدام دالة مقارنة تُحدَّد من القائمة المنسدلة. يستخدم الترتيب الأبجدي <code>localeCompare</code>، وهي المقارنة الواعية باللغة في المتصفح، بدلًا من رموز الأحرف الخام. هذا الفرق واضح فورًا: الترتيب الساذج حسب نقطة الرمز يضع كل حرف كبير قبل كل حرف صغير (لذا يُرتَّب "Zebra" قبل "apple")، ويشوّه ترتيب الأحرف المنقّطة. المقارنة الواعية باللغة ترتّب الكلمات بالطريقة نفسها التي يرتّبها بها القاموس.',
        how_p2='يحلّل الترتيب الرقمي كل سطر باستخدام <code>parseFloat</code> ويقارن الأرقام، ما يصحّح الخلل الكلاسيكي في ترتيب النصوص حيث يأتي "10" قبل "9" لأن "1" حرف أصغر. تُعامَل الأسطر التي لا تبدأ برقم كأنها 0 وتُجمَّع معًا. يقارن الترتيب حسب الطول عدد الأحرف، ويستخدم الخلط العشوائي خوارزمية Fisher-Yates، التي تمنح كل ترتيب احتمالية متساوية. يستحق هذا توضيحًا: الحيلة الشائعة <code>sort(() =&gt; Math.random() - 0.5)</code> تنتج خلطًا متحيّزًا لأن خوارزميات الترتيب تفترض دالة مقارنة ثابتة، بينما تمر خوارزمية Fisher-Yates على المصفوفة مرة واحدة، مبدّلة كل عنصر بموضع سابق عشوائي منتظم التوزيع.',
        how_p3="الترتيب التنازلي يرتّب تصاعديًا ثم يعكس، وتُنفَّذ إزالة التكرارات بعد الترتيب باستخدام <code>Set</code> بحيث تُحذف فقط التكرارات المطابقة تمامًا، ويمكن تصفية الأسطر الفارغة قبل كل ذلك. العملية بأكملها هي عمليات على مصفوفة نصية داخل تبويبك: لا يُطلق أي طلب عند اللصق أو الترتيب (تحقّق من ذلك في لوحة الشبكة بأدوات المطوّر)، لذا فإن ترتيب قائمة أسماء أو رسائل بريد أو مفاتيح لا يشمل خادمًا أبدًا.",
    ),
    related_tools=[
        ("remove-duplicate-lines.html", "إزالة الأسطر المكررة", "أزل التكرارات قبل الترتيب أو بعده."),
        ("/case-converter.html", "محوّل حالة الأحرف", "حوّل النص بين الأحرف الكبيرة والصغيرة وcamelCase والمزيد."),
        ("json-formatter.html", "منسّق JSON", "تنسيق والتحقق من JSON."),
    ],
)

PAGES["hi"] = dict(
    title="लाइनें सॉर्ट करें ऑनलाइन: अल्फ़ाबेटिकल, न्यूमेरिक, शफ़ल | norito",
    meta_desc="लाइनों की एक लिस्ट को अल्फ़ाबेटिकली, न्यूमेरिकली, लंबाई के हिसाब से सॉर्ट करें, या रैंडमली शफ़ल करें, अपने ब्राउज़र में ही। कुछ भी अपलोड नहीं होता।",
    app_name="लाइनें सॉर्ट करें", h1="लाइनें सॉर्ट करें", breadcrumb_label="लाइनें सॉर्ट करें",
    lede="एक लिस्ट को अल्फ़ाबेटिकली, न्यूमेरिकली, लंबाई के हिसाब से सॉर्ट करें, या रैंडमली शफ़ल करें। एसेंडिंग या डिसेंडिंग, वैकल्पिक डीडुप्लीकेशन के साथ।",
    t=dict(
        input_label="इनपुट (प्रति लाइन एक आइटम)", placeholder="केला\nसेब\nचेरी",
        sort_by="इस हिसाब से सॉर्ट करें", opt_alpha="अल्फ़ाबेटिकल (केस-सेंसिटिव)", opt_alpha_ci="अल्फ़ाबेटिकल (केस इग्नोर करें)",
        opt_numeric="न्यूमेरिक", opt_length="लाइन की लंबाई", opt_shuffle="रैंडमली शफ़ल करें",
        direction="दिशा", asc="एसेंडिंग", desc="डिसेंडिंग",
        dedupe="डुप्लीकेट लाइनें हटाएं", remove_blank="खाली लाइनें हटाएं",
        result="परिणाम", zero_lines="0 लाइनें।", sort_now="अभी सॉर्ट करें", copy_result="परिणाम कॉपी करें",
        how_h2="यह कैसे काम करता है",
        how_p1='आपका टेक्स्ट न्यूलाइन पर स्प्लिट होता है और ड्रॉपडाउन से चुने गए कंपैरेटर से सॉर्ट होता है। अल्फ़ाबेटिकल ऑर्डर रॉ कैरेक्टर कोड की बजाय <code>localeCompare</code> का उपयोग करता है, जो ब्राउज़र की भाषा-जागरूक तुलना है। यह फ़र्क तुरंत दिखता है: एक नैव कोड-पॉइंट सॉर्ट हर बड़े अक्षर को हर छोटे अक्षर से पहले रखता है (इसलिए "Zebra", "apple" से पहले सॉर्ट होगा), और यह एक्सेंट वाले कैरेक्टर को गड़बड़ कर देता है। लोकेल-अवेयर तुलना शब्दों को वैसे ही क्रम में रखती है जैसे कोई डिक्शनरी रखेगी।',
        how_p2='न्यूमेरिक सॉर्ट हर लाइन को <code>parseFloat</code> से पार्स करता है और नंबरों की तुलना करता है, जो उस क्लासिक स्ट्रिंग-सॉर्ट बग को ठीक करता है जहाँ "10", "9" से पहले आ जाता है क्योंकि "1" एक छोटा कैरेक्टर है। जो लाइनें किसी नंबर से शुरू नहीं होतीं उन्हें 0 माना जाता है और साथ में समूहित किया जाता है। लेंथ सॉर्ट कैरेक्टर काउंट की तुलना करता है, और शफ़ल Fisher-Yates एल्गोरिद्म का उपयोग करता है, जो हर ऑर्डरिंग को बराबर संभावना देता है। यह बताना ज़रूरी है: लोकप्रिय <code>sort(() =&gt; Math.random() - 0.5)</code> ट्रिक बायस्ड शफ़ल पैदा करती है क्योंकि सॉर्ट एल्गोरिद्म एक कंसिस्टेंट कंपैरेटर मान लेते हैं, जबकि Fisher-Yates एरे पर सिर्फ़ एक बार चलता है, हर आइटम को समान रूप से रैंडम पहले वाले स्लॉट से स्वैप करते हुए।',
        how_p3="डिसेंडिंग ऑर्डर पहले एसेंडिंग सॉर्ट करता है फिर उसे रिवर्स करता है, डीडुप सॉर्टिंग के बाद <code>Set</code> से चलता है ताकि सिर्फ़ बिल्कुल एक जैसी रिपीट लाइनें हटें, और खाली लाइनें इस सबसे पहले फ़िल्टर हो सकती हैं। पूरी प्रोसेस आपके टैब में एक स्ट्रिंग पर एरे ऑपरेशंस है: पेस्ट करने या सॉर्ट करने पर कोई रिक्वेस्ट फ़ायर नहीं होती (डेवलपर टूल्स के नेटवर्क पैनल में पुष्टि करें), इसलिए नामों, ईमेल या कीज़ की लिस्ट सॉर्ट करने में कभी सर्वर शामिल नहीं होता।",
    ),
    related_tools=[
        ("remove-duplicate-lines.html", "डुप्लीकेट लाइनें हटाएं", "सॉर्ट करने से पहले या बाद में लिस्ट को डीडुप्लीकेट करें।"),
        ("/case-converter.html", "केस कन्वर्टर", "टेक्स्ट को अपरकेस, लोअरकेस, camelCase और अन्य में बदलें।"),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "JSON फ़ॉर्मैट और वैलिडेट करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Сортировка строк онлайн: по алфавиту, числам, вперемешку | norito",
    meta_desc="Сортируйте список строк по алфавиту, по числам, по длине или перемешивайте случайным образом прямо в браузере. Ничего не загружается.",
    app_name="Сортировка строк", h1="Сортировка строк", breadcrumb_label="Сортировка строк",
    lede="Сортируйте список по алфавиту, по числам, по длине, или перемешайте его случайным образом. По возрастанию или убыванию, с опциональным удалением дубликатов.",
    t=dict(
        input_label="Ввод (один элемент на строку)", placeholder="банан\nяблоко\nвишня",
        sort_by="Сортировать по", opt_alpha="По алфавиту (с учётом регистра)", opt_alpha_ci="По алфавиту (без учёта регистра)",
        opt_numeric="По числам", opt_length="По длине строки", opt_shuffle="Перемешать случайно",
        direction="Направление", asc="По возрастанию", desc="По убыванию",
        dedupe="Удалить повторяющиеся строки", remove_blank="Удалить пустые строки",
        result="Результат", zero_lines="0 строк.", sort_now="Сортировать сейчас", copy_result="Скопировать результат",
        how_h2="Как это работает",
        how_p1='Ваш текст разбивается по переносам строк и сортируется компаратором, выбранным в выпадающем списке. Алфавитный порядок использует <code>localeCompare</code> — языково-зависимое сравнение браузера — вместо необработанных кодов символов. Разница видна сразу: наивная сортировка по кодовым точкам ставит каждую заглавную букву перед каждой строчной (поэтому "Zebra" сортируется перед "apple"), и она искажает порядок символов с диакритическими знаками. Языково-зависимое сравнение упорядочивает слова так, как это сделал бы словарь.',
        how_p2='Числовая сортировка разбирает каждую строку функцией <code>parseFloat</code> и сравнивает числа, что исправляет классическую ошибку строковой сортировки, при которой "10" оказывается перед "9", потому что "1" — меньший символ. Строки, не начинающиеся с числа, считаются равными 0 и группируются вместе. Сортировка по длине сравнивает количество символов, а перемешивание использует алгоритм Фишера — Йетса, который даёт каждому порядку равную вероятность. Стоит пояснить: популярный трюк <code>sort(() =&gt; Math.random() - 0.5)</code> даёт смещённое перемешивание, потому что алгоритмы сортировки предполагают согласованный компаратор, тогда как Фишер — Йетс проходит по массиву один раз, меняя каждый элемент местами с равномерно случайной более ранней позицией.',
        how_p3="Сортировка по убыванию — это сортировка по возрастанию с последующим разворотом, удаление дубликатов выполняется после сортировки с помощью <code>Set</code>, поэтому удаляются только точные повторы, а пустые строки можно отфильтровать ещё до всего этого. Весь процесс — это операции с массивом над строкой прямо в вашей вкладке: при вставке или сортировке не отправляется ни одного запроса (проверьте на панели «Сеть» в инструментах разработчика), поэтому сортировка списка имён, email-адресов или ключей никогда не затрагивает сервер.",
    ),
    related_tools=[
        ("remove-duplicate-lines.html", "Удаление дублирующихся строк", "Удаление дубликатов до или после сортировки."),
        ("/case-converter.html", "Конвертер регистра", "Преобразование текста между верхним, нижним регистром, camelCase и другими."),
        ("json-formatter.html", "Форматирование JSON", "Форматирование и проверка JSON."),
    ],
)

PAGES["ja"] = dict(
    title="行の並べ替え：アルファベット順、数値順、シャッフル | norito",
    meta_desc="行のリストをアルファベット順、数値順、長さ順に並べ替えたり、ランダムにシャッフルしたりできます。ブラウザ内で完結。アップロードは一切行われません。",
    app_name="行の並べ替え", h1="行の並べ替え", breadcrumb_label="行の並べ替え",
    lede="リストをアルファベット順、数値順、長さ順に並べ替えたり、ランダムにシャッフルしたりできます。昇順・降順、重複削除オプション付き。",
    t=dict(
        input_label="入力（1行に1項目）", placeholder="バナナ\nりんご\nさくらんぼ",
        sort_by="並べ替え基準", opt_alpha="アルファベット順（大文字小文字を区別）", opt_alpha_ci="アルファベット順（大文字小文字を無視）",
        opt_numeric="数値順", opt_length="行の長さ順", opt_shuffle="ランダムにシャッフル",
        direction="方向", asc="昇順", desc="降順",
        dedupe="重複行を削除", remove_blank="空行を削除",
        result="結果", zero_lines="0 行。", sort_now="今すぐ並べ替え", copy_result="結果をコピー",
        how_h2="仕組み",
        how_p1='入力されたテキストは改行で分割され、ドロップダウンで選んだ比較関数で並べ替えられます。アルファベット順は生の文字コードではなく、ブラウザの言語対応比較機能である <code>localeCompare</code> を使用します。この違いはすぐにわかります。素朴なコードポイント順の並べ替えでは、すべての大文字がすべての小文字より前に来てしまい（そのため "Zebra" は "apple" より前に並びます）、アクセント記号付きの文字の順序も崩れてしまいます。ロケールを考慮した比較なら、辞書と同じように単語を並べられます。',
        how_p2='数値順の並べ替えは各行を <code>parseFloat</code> で解析して数値を比較するため、"1" が小さい文字であるために "10" が "9" より前に来てしまうという文字列ソートの典型的なバグを解消します。数値で始まらない行は0として扱われ、まとめてグループ化されます。長さ順は文字数を比較し、シャッフルはFisher-Yatesアルゴリズムを使用するため、すべての並び順が等しい確率になります。ここは一言触れておく価値があります。よく使われる <code>sort(() =&gt; Math.random() - 0.5)</code> というテクニックは、ソートアルゴリズムが一貫した比較関数を前提としているため偏ったシャッフルになりますが、Fisher-Yatesは配列を1回だけ走査し、各要素を一様にランダムな前方のスロットと入れ替えます。',
        how_p3="降順は昇順に並べ替えてから反転する処理で、重複削除は並べ替え後に <code>Set</code> を使って行われるため、完全に一致するものだけが削除されます。空行はそれより前の段階でフィルタリングできます。この一連の処理はすべて、そのタブ内の文字列に対する配列操作です。貼り付けや並べ替えを行ってもリクエストは一切発生しません（開発者ツールのネットワークパネルで確認できます）。そのため、名前やメールアドレス、キーのリストを並べ替える際にサーバーが関わることは一切ありません。",
    ),
    related_tools=[
        ("remove-duplicate-lines.html", "重複行の削除", "並べ替えの前後でリストの重複を削除。"),
        ("/case-converter.html", "大文字小文字変換ツール", "大文字、小文字、camelCaseなどの間でテキストを変換。"),
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "sort-lines.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-sort-lines.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/sort-lines.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
