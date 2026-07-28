#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-12"/><path d="M5 8h4"/><path d="M15 16h4"/><circle cx="5" cy="14" r="2"/><circle cx="19" cy="10" r="2"/></svg>'
ICON_CLASS = "c-teal"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field-row">
          <div class="field" style="flex:2;">
            <label for="pattern">{t['pattern']}</label>
            <input type="text" id="pattern" class="mono-output" spellcheck="false" value="\\b[A-Z][a-z]+\\b" />
          </div>
          <div class="field">
            <label for="flags">{t['flags']}</label>
            <input type="text" id="flags" class="mono-output" spellcheck="false" value="g" placeholder="gimsuy" />
          </div>
        </div>
        <div class="field">
          <label for="testString">{t['test_string']}</label>
          <textarea id="testString" class="mono-output" rows="6" spellcheck="false">{t['sample_text']}</textarea>
        </div>
        <div class="result-box" id="result" style="display:none;"></div>
        <div class="field" style="margin-top:16px;">
          <label>{t['highlighted']}</label>
          <div class="regex-highlighted" id="highlighted"></div>
        </div>
        <div class="meta-panel" id="matchesPanel" style="display:none; margin-top:16px;">
          <p class="meta-summary">{t['all_matches']}</p>
          <div id="matchesList"></div>
        </div>
      </div>

      <div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['flags_ref']}</h3>
          <p class="note" style="margin-top:0;">
            {t['flags_ref_body']}
          </p>
        </div>
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
    title="Probador de Regex: Prueba Expresiones Regulares en Vivo | norito",
    meta_desc="Prueba una expresión regular contra un texto de muestra con resaltado de coincidencias en vivo, en tu navegador. Ve grupos de captura y todas las coincidencias. No se sube nada.",
    app_name="Probador de Regex", h1="Probador de Regex", breadcrumb_label="Probador de Regex",
    lede="Prueba una expresión regular contra un texto de muestra, con las coincidencias resaltadas en vivo mientras escribes. Ve cada coincidencia y sus grupos de captura.",
    t=dict(
        pattern="Patrón", flags="Flags", test_string="Texto de prueba",
        sample_text="El Rápido Zorro Marrón salta sobre el Perro perezoso.",
        highlighted="Coincidencias resaltadas", all_matches="Todas las coincidencias",
        flags_ref="Referencia de flags",
        flags_ref_body='<strong>g</strong> global (encuentra todas las coincidencias, siempre aplicado internamente aquí), <strong>i</strong> insensible a mayúsculas, <strong>m</strong> multilínea (^ y $ coinciden con los límites de línea), <strong>s</strong> dotAll (. coincide con saltos de línea), <strong>u</strong> unicode, <strong>y</strong> sticky.',
        how_h2="Cómo funciona",
        how_p1='Tu patrón se compila con el motor <code>RegExp</code> nativo del navegador, exactamente el mismo motor que tu código JavaScript usará en producción. Ese es el punto de probar aquí en vez de en una herramienta basada en PCRE: la sintaxis que difiere entre variantes (soporte de lookbehind, semántica de <code>\\d</code> bajo la bandera <code>u</code>, grupos con nombre) se comporta aquí exactamente como lo hará en Node o en el navegador. El campo de flags se sanea al conjunto válido (<code>d g i m s u y</code>), y el probador añade silenciosamente <code>g</code> internamente para poder recorrer cada coincidencia, sin cambiar lo que escribiste.',
        how_p2='La coincidencia se ejecuta en cada pulsación: el probador llama a <code>exec()</code> en un bucle, recopilando el texto de la coincidencia, su posición, y los grupos de captura. Dos protecciones lo mantienen honesto: las coincidencias de longitud cero (de patrones como <code>a*</code>) reciben un avance manual de índice para que el bucle no gire para siempre, y la iteración se limita a 5000 coincidencias. El resaltado se construye recorriendo tu texto de prueba una vez y envolviendo cada tramo coincidente, con todo el texto escapado a HTML primero para que una coincidencia que contenga <code>&lt;script&gt;</code> se muestre como texto, no como marcado.',
        how_p3='Todo permanece en tu pestaña; el panel Red de las DevTools muestra cero peticiones mientras escribes, así que los textos de prueba con datos reales nunca salen de tu máquina.',
        how_p4='Un detalle que vale la pena conocer: cuantificadores anidados como <code>(a+)+$</code> pueden desencadenar un retroceso catastrófico, donde el tiempo de coincidencia explota exponencialmente en una entrada larga casi-coincidente. Si la página se congela con un patrón así, no es la herramienta, es el regex, y colgará tu código de producción de la misma manera. Reescribe el patrón para que los grupos cuantificados no puedan coincidir con los mismos caracteres de múltiples formas.',
    ),
    related_tools=[
        ("json-formatter.html", "Formateador JSON", "Formatea y valida JSON."),
        ("seo-slug-generator.html", "Generador de slugs SEO", "Slugs de URL limpios a partir de títulos."),
        ("case-converter.html", "Conversor de mayúsculas/minúsculas", "Convierte texto entre mayúsculas y minúsculas."),
    ],
)

PAGES["zh"] = dict(
    title="正则表达式测试工具：在线实时测试 | norito",
    meta_desc="在浏览器中实时高亮匹配结果，针对示例文本测试正则表达式。查看捕获组和所有匹配项。不上传任何内容。",
    app_name="正则表达式测试工具", h1="正则表达式测试工具", breadcrumb_label="正则表达式测试工具",
    lede="针对示例文本测试正则表达式，输入时实时高亮显示匹配结果。查看每个匹配项及其捕获组。",
    t=dict(
        pattern="模式", flags="标志", test_string="测试字符串",
        sample_text="敏捷的棕色狐狸跳过了懒惰的狗。",
        highlighted="高亮匹配", all_matches="所有匹配项",
        flags_ref="标志参考",
        flags_ref_body='<strong>g</strong> 全局（查找所有匹配项，此工具内部始终应用），<strong>i</strong> 不区分大小写，<strong>m</strong> 多行模式（^ 和 $ 匹配行边界），<strong>s</strong> dotAll 模式（. 匹配换行符），<strong>u</strong> Unicode 模式，<strong>y</strong> 粘性模式。',
        how_h2="工作原理",
        how_p1='你的模式使用浏览器原生的 <code>RegExp</code> 引擎编译，与你的 JavaScript 代码在生产环境中使用的引擎完全相同。这正是在此处测试而非在基于 PCRE 的工具中测试的意义所在：不同方言之间存在差异的语法（后行断言支持、<code>u</code> 标志下 <code>\\d</code> 的语义、命名组）在这里的行为与在 Node 或浏览器中完全一致。标志字段会被清理为有效集合（<code>d g i m s u y</code>），测试工具会在内部悄悄添加 <code>g</code>，以便遍历每个匹配项，而不会改变你输入的内容。',
        how_p2='匹配在每次按键时运行：测试工具在循环中调用 <code>exec()</code>，收集匹配文本、位置和捕获组。两个保护机制保证其正确性：零长度匹配（来自像 <code>a*</code> 这样的模式）会手动推进索引，以防止循环无限运行；迭代次数上限为 5000 个匹配项。高亮显示是通过遍历一次测试字符串并包裹每个匹配的片段构建的，所有文本会先进行 HTML 转义，因此包含 <code>&lt;script&gt;</code> 的匹配项会以文本形式呈现，而不会作为标记渲染。',
        how_p3='一切都保留在你的标签页中；输入时开发者工具的 Network 面板显示零请求，因此包含真实数据的测试字符串永远不会离开你的电脑。',
        how_p4='一个值得了解的陷阱：像 <code>(a+)+$</code> 这样的嵌套量词可能引发灾难性回溯，导致匹配时间在长的、几乎匹配的输入上呈指数级爆炸增长。如果页面在这样的模式下卡死，问题不在于工具，而在于正则表达式本身，它同样会以相同方式卡住你的生产代码。请重写模式，使量化的分组不能以多种方式匹配相同的字符。',
    ),
    related_tools=[
        ("json-formatter.html", "JSON 格式化", "格式化并校验 JSON。"),
        ("seo-slug-generator.html", "SEO Slug 生成器", "从标题生成干净的 URL slug。"),
        ("case-converter.html", "大小写转换器", "在不同大小写格式之间转换文本。"),
    ],
)

PAGES["ar"] = dict(
    title="أداة اختبار Regex: اختبر التعبيرات النمطية مباشرة | norito",
    meta_desc="اختبر تعبيرًا نمطيًا مقابل نص عينة مع تمييز مباشر للتطابقات، مباشرة في متصفحك. شاهد مجموعات الالتقاط وكل التطابقات. لا شيء يُرفَع.",
    app_name="أداة اختبار Regex", h1="أداة اختبار Regex", breadcrumb_label="أداة اختبار Regex",
    lede="اختبر تعبيرًا نمطيًا مقابل نص عينة، مع تمييز التطابقات مباشرة أثناء الكتابة. شاهد كل تطابق ومجموعات التقاطه.",
    t=dict(
        pattern="النمط", flags="العلامات", test_string="نص الاختبار",
        sample_text="الثعلب البني السريع يقفز فوق الكلب الكسول.",
        highlighted="التطابقات المميّزة", all_matches="كل التطابقات",
        flags_ref="مرجع العلامات",
        flags_ref_body='<strong>g</strong> شامل (يجد كل التطابقات، مُطبَّق دائمًا داخليًا هنا)، <strong>i</strong> غير حساس لحالة الأحرف، <strong>m</strong> متعدد الأسطر (^ و$ يطابقان حدود الأسطر)، <strong>s</strong> dotAll (. يطابق الأسطر الجديدة)، <strong>u</strong> يونيكود، <strong>y</strong> لاصق.',
        how_h2="كيف يعمل",
        how_p1='يُجمَّع نمطك بمحرك <code>RegExp</code> الأصلي للمتصفح، وهو نفس المحرك تمامًا الذي سيستخدمه كود جافاسكريبت في الإنتاج. هذه هي فائدة الاختبار هنا بدلًا من أداة مبنية على PCRE: الصياغة التي تختلف بين النكهات (دعم lookbehind، دلالات <code>\\d</code> تحت علامة <code>u</code>، المجموعات المسمّاة) تتصرف هنا تمامًا كما ستتصرف في Node أو المتصفح. يُنقَّى حقل العلامات إلى المجموعة الصالحة (<code>d g i m s u y</code>)، وتضيف الأداة بصمت <code>g</code> داخليًا حتى تتمكن من المرور على كل تطابق، دون تغيير ما كتبته.',
        how_p2='تعمل المطابقة مع كل ضغطة مفتاح: تستدعي الأداة <code>exec()</code> في حلقة، جامعةً نص التطابق وموضعه ومجموعات الالتقاط. حارسان يحافظان على الدقة: التطابقات صفرية الطول (من أنماط مثل <code>a*</code>) تحصل على زيادة يدوية للفهرس حتى لا تدور الحلقة إلى الأبد، ويُحدَّد التكرار بحد أقصى 5000 تطابق. يُبنى التمييز بالمرور على نص اختبارك مرة واحدة وتغليف كل نطاق مطابق، مع تهريب كل النص إلى HTML أولًا حتى يُعرَض تطابق يحتوي <code>&lt;script&gt;</code> كنص، لا كترميز.',
        how_p3='يبقى كل شيء في تبويبك؛ تُظهر لوحة Network في أدوات المطوّر صفر طلبات أثناء الكتابة، لذا نصوص الاختبار التي تحتوي بيانات حقيقية لا تغادر جهازك أبدًا.',
        how_p4='مطبّ يستحق المعرفة: المُحدِّدات الكمية المتداخلة مثل <code>(a+)+$</code> يمكن أن تُطلِق تراجعًا كارثيًا، حيث ينفجر وقت المطابقة أسّيًا على إدخال طويل شبه مطابق. إذا تجمّدت الصفحة مع نمط كهذا، فالمشكلة ليست في الأداة، بل في التعبير النمطي نفسه، وسيُعلِّق كود الإنتاج لديك بنفس الطريقة. أعد صياغة النمط حتى لا تستطيع المجموعات المُحدَّدة كميًا مطابقة نفس الأحرف بطرق متعددة.',
    ),
    related_tools=[
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق من JSON."),
        ("seo-slug-generator.html", "مولّد سلاجات SEO", "سلاجات روابط نظيفة من العناوين."),
        ("case-converter.html", "محول حالة الأحرف", "حوّل النص بين حالات الأحرف المختلفة."),
    ],
)

PAGES["hi"] = dict(
    title="Regex टेस्टर: रेगुलर एक्सप्रेशन लाइव टेस्ट करें | norito",
    meta_desc="अपने ब्राउज़र में ही, लाइव मैच हाइलाइटिंग के साथ सैंपल टेक्स्ट के खिलाफ एक रेगुलर एक्सप्रेशन टेस्ट करें। कैप्चर ग्रुप्स और सभी मैच देखें। कुछ भी अपलोड नहीं होता।",
    app_name="Regex टेस्टर", h1="Regex टेस्टर", breadcrumb_label="Regex टेस्टर",
    lede="सैंपल टेक्स्ट के खिलाफ एक रेगुलर एक्सप्रेशन टेस्ट करें, टाइप करते ही मैचेज़ लाइव हाइलाइट होते हैं। हर मैच और उसके कैप्चर ग्रुप्स देखें।",
    t=dict(
        pattern="पैटर्न", flags="फ़्लैग्स", test_string="टेस्ट स्ट्रिंग",
        sample_text="तेज़ भूरी लोमड़ी आलसी कुत्ते के ऊपर से कूदती है।",
        highlighted="हाइलाइट किए गए मैच", all_matches="सभी मैच",
        flags_ref="फ़्लैग्स रेफ़रेंस",
        flags_ref_body='<strong>g</strong> ग्लोबल (सभी मैच ढूंढता है, यहां हमेशा इंटरनली अप्लाई किया जाता है), <strong>i</strong> केस-इनसेंसिटिव, <strong>m</strong> मल्टीलाइन (^ और $ लाइन बाउंड्रीज़ से मैच करते हैं), <strong>s</strong> dotAll (. न्यूलाइन से मैच करता है), <strong>u</strong> यूनिकोड, <strong>y</strong> स्टिकी।',
        how_h2="यह कैसे काम करता है",
        how_p1='आपका पैटर्न ब्राउज़र के नेटिव <code>RegExp</code> इंजन से कंपाइल होता है, बिल्कुल वही इंजन जो आपका JavaScript कोड प्रोडक्शन में इस्तेमाल करेगा। PCRE-आधारित टूल के बजाय यहां टेस्ट करने का यही मक़सद है: सिंटैक्स जो अलग-अलग फ़्लेवर्स के बीच अलग होता है (lookbehind सपोर्ट, <code>u</code> फ़्लैग के तहत <code>\\d</code> सिमेंटिक्स, नेम्ड ग्रुप्स) यहां बिल्कुल वैसे ही बर्ताव करता है जैसे वह Node या ब्राउज़र में करेगा। फ़्लैग्स फ़ील्ड को वैलिड सेट (<code>d g i m s u y</code>) में सैनिटाइज़ किया जाता है, और टेस्टर चुपचाप इंटरनली <code>g</code> जोड़ देता है ताकि वह हर मैच पर चल सके, बिना आपके टाइप किए हुए को बदले।',
        how_p2='मैचिंग हर कीस्ट्रोक पर चलती है: टेस्टर एक लूप में <code>exec()</code> कॉल करता है, मैच टेक्स्ट, पोज़िशन, और कैप्चर ग्रुप्स इकट्ठा करते हुए। दो गार्ड्स इसे ईमानदार रखते हैं: ज़ीरो-लेंथ मैचेज़ (जैसे <code>a*</code> जैसे पैटर्न से) को मैनुअल इंडेक्स बंप मिलता है ताकि लूप हमेशा के लिए न घूमे, और इटरेशन 5,000 मैचेज़ पर कैप होता है। हाइलाइटिंग आपकी टेस्ट स्ट्रिंग को एक बार चलाकर और हर मैच किए गए स्पैन को रैप करके बनाई जाती है, सारे टेक्स्ट को पहले HTML-एस्केप्ड किया जाता है ताकि <code>&lt;script&gt;</code> वाला कोई मैच टेक्स्ट के रूप में दिखे, मार्कअप के रूप में नहीं।',
        how_p3='सब कुछ आपके टैब में रहता है; टाइप करते समय डेवटूल्स का Network पैनल ज़ीरो रिक्वेस्ट दिखाता है, इसलिए असली डेटा वाली टेस्ट स्ट्रिंग्स कभी आपकी मशीन से बाहर नहीं जातीं।',
        how_p4='एक बात जो जानने लायक है: <code>(a+)+$</code> जैसे नेस्टेड क्वांटिफ़ायर कैटास्ट्रोफ़िक बैकट्रैकिंग ट्रिगर कर सकते हैं, जहां लंबे लगभग-मैचिंग इनपुट पर मैच टाइम एक्सपोनेंशियली फट जाता है। अगर पेज ऐसे किसी पैटर्न पर फ़्रीज़ हो जाए, तो यह टूल की गलती नहीं, regex की है, और यह आपके प्रोडक्शन कोड को भी उसी तरह हैंग कर देगा। पैटर्न को इस तरह फिर से लिखें कि क्वांटिफ़ाइड ग्रुप्स एक ही कैरेक्टर्स को कई तरीक़ों से मैच न कर सकें।',
    ),
    related_tools=[
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "JSON फ़ॉर्मैट और वैलिडेट करें।"),
        ("seo-slug-generator.html", "SEO स्लग जनरेटर", "टाइटल से क्लीन URL स्लग बनाएं।"),
        ("case-converter.html", "केस कन्वर्टर", "टेक्स्ट को अलग-अलग केस के बीच कन्वर्ट करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Тестер регулярных выражений онлайн | norito",
    meta_desc="Проверьте регулярное выражение на образце текста с живой подсветкой совпадений прямо в браузере. Смотрите группы захвата и все совпадения. Ничего не загружается.",
    app_name="Тестер регулярных выражений", h1="Тестер регулярных выражений", breadcrumb_label="Тестер регулярных выражений",
    lede="Проверьте регулярное выражение на образце текста, совпадения подсвечиваются в реальном времени по мере ввода. Смотрите каждое совпадение и его группы захвата.",
    t=dict(
        pattern="Шаблон", flags="Флаги", test_string="Тестовая строка",
        sample_text="Быстрая бурая лиса перепрыгивает через ленивую собаку.",
        highlighted="Подсвеченные совпадения", all_matches="Все совпадения",
        flags_ref="Справочник флагов",
        flags_ref_body='<strong>g</strong> глобальный (находит все совпадения, здесь всегда применяется внутренне), <strong>i</strong> без учёта регистра, <strong>m</strong> многострочный (^ и $ совпадают с границами строк), <strong>s</strong> dotAll (. совпадает с переносами строк), <strong>u</strong> юникод, <strong>y</strong> липкий (sticky).',
        how_h2="Как это работает",
        how_p1='Ваш шаблон компилируется нативным движком <code>RegExp</code> браузера — тем же самым движком, который ваш JavaScript-код будет использовать в продакшене. В этом и смысл тестирования здесь, а не в инструменте на основе PCRE: синтаксис, отличающийся между диалектами (поддержка lookbehind, семантика <code>\\d</code> под флагом <code>u</code>, именованные группы), ведёт себя здесь точно так же, как в Node или браузере. Поле флагов очищается до допустимого набора (<code>d g i m s u y</code>), и тестер незаметно добавляет <code>g</code> внутренне, чтобы пройтись по каждому совпадению, не меняя то, что вы ввели.',
        how_p2='Сопоставление выполняется при каждом нажатии клавиши: тестер вызывает <code>exec()</code> в цикле, собирая текст совпадения, позицию и группы захвата. Две защиты обеспечивают корректность: совпадения нулевой длины (от шаблонов вроде <code>a*</code>) получают ручное продвижение индекса, чтобы цикл не крутился бесконечно, а итерации ограничены 5000 совпадениями. Подсветка строится путём однократного прохода по вашей тестовой строке и обёртывания каждого совпавшего участка, при этом весь текст сначала экранируется в HTML, чтобы совпадение, содержащее <code>&lt;script&gt;</code>, отображалось как текст, а не как разметка.',
        how_p3='Всё остаётся в вашей вкладке; панель Network в DevTools показывает ноль запросов во время ввода, поэтому тестовые строки с реальными данными никогда не покидают ваш компьютер.',
        how_p4='Стоит знать одну ловушку: вложенные квантификаторы вроде <code>(a+)+$</code> могут вызвать катастрофический бэктрекинг, при котором время сопоставления экспоненциально растёт на длинном почти совпадающем вводе. Если страница зависает на таком шаблоне, дело не в инструменте, а в самом регулярном выражении, и оно точно так же подвесит ваш продакшен-код. Перепишите шаблон так, чтобы квантифицированные группы не могли совпадать с одними и теми же символами несколькими способами.',
    ),
    related_tools=[
        ("json-formatter.html", "Форматирование JSON", "Форматирует и проверяет JSON."),
        ("seo-slug-generator.html", "Генератор SEO-слагов", "Чистые URL-слаги из заголовков."),
        ("case-converter.html", "Конвертер регистра", "Преобразование текста между регистрами."),
    ],
)

PAGES["ja"] = dict(
    title="正規表現テストツール：リアルタイムでテスト | norito",
    meta_desc="サンプルテキストに対して正規表現をリアルタイムのマッチハイライト付きでブラウザ内でテスト。キャプチャグループとすべての一致を確認。アップロードなし。",
    app_name="正規表現テストツール", h1="正規表現テストツール", breadcrumb_label="正規表現テストツール",
    lede="サンプルテキストに対して正規表現をテストし、入力するとリアルタイムに一致箇所がハイライトされます。すべての一致とキャプチャグループを確認できます。",
    t=dict(
        pattern="パターン", flags="フラグ", test_string="テスト文字列",
        sample_text="素早い茶色のキツネが怠け者の犬を飛び越える。",
        highlighted="ハイライトされた一致", all_matches="すべての一致",
        flags_ref="フラグ一覧",
        flags_ref_body='<strong>g</strong> グローバル（すべての一致を検索、ここでは常に内部的に適用）、<strong>i</strong> 大文字小文字を区別しない、<strong>m</strong> 複数行（^と$が行境界に一致）、<strong>s</strong> dotAll（.が改行にも一致）、<strong>u</strong> Unicode、<strong>y</strong> sticky。',
        how_h2="仕組み",
        how_p1='あなたのパターンはブラウザネイティブの<code>RegExp</code>エンジンでコンパイルされます。これはあなたのJavaScriptコードが本番環境で使用するのとまったく同じエンジンです。これが、PCREベースのツールではなくここでテストする意味です。方言間で異なる構文（後読みのサポート、<code>u</code>フラグ下での<code>\\d</code>の意味論、名前付きグループ）は、ここではNodeやブラウザとまったく同じように動作します。フラグフィールドは有効なセット（<code>d g i m s u y</code>）にサニタイズされ、テストツールはすべての一致を巡回できるよう内部的に静かに<code>g</code>を追加しますが、あなたが入力した内容自体は変更されません。',
        how_p2='マッチングはキー入力のたびに実行されます。テストツールはループ内で<code>exec()</code>を呼び出し、一致テキスト、位置、キャプチャグループを収集します。2つの保護機構が正確性を保ちます。ゼロ長の一致（<code>a*</code>のようなパターンから）は手動でインデックスを進めることでループが無限に回らないようにし、繰り返しは最大5,000件の一致に制限されます。ハイライトはテスト文字列を一度走査し、一致した各範囲を囲むことで構築されます。すべてのテキストは先にHTMLエスケープされるため、<code>&lt;script&gt;</code>を含む一致もマークアップとしてではなくテキストとして表示されます。',
        how_p3='すべてはあなたのタブ内にとどまります。入力中、DevToolsのNetworkパネルにはリクエストが一切表示されないため、実データを含むテスト文字列があなたのマシンから外に出ることはありません。',
        how_p4='知っておく価値のある落とし穴が一つあります。<code>(a+)+$</code>のようなネストした量指定子は、破滅的バックトラッキングを引き起こす可能性があり、長いほぼ一致する入力に対してマッチ時間が指数関数的に爆発します。このようなパターンでページがフリーズした場合、それはツールの問題ではなく正規表現自体の問題であり、本番コードでも同じようにハングします。量指定されたグループが同じ文字を複数の方法で一致させられないよう、パターンを書き直してください。',
    ),
    related_tools=[
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証。"),
        ("seo-slug-generator.html", "SEOスラグジェネレーター", "タイトルからクリーンなURLスラグを生成。"),
        ("case-converter.html", "大文字小文字変換ツール", "テキストの大文字小文字を変換。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "regex-tester.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-regex-tester.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/regex-tester.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
