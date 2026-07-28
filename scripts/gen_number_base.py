#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><rect x="14" y="14" width="6" height="6" rx="1"/></svg>'
ICON_CLASS = "c-coral"

def base_options(base_word, selected):
    opts = []
    for n in range(2, 37):
        sel = " selected" if n == selected else ""
        opts.append(f'<option value="{n}"{sel}>{base_word} {n}</option>')
    return "\n            ".join(opts)

def body(t):
    from_opts = base_options(t['base_word'], 10)
    to_opts = base_options(t['base_word'], 16)
    return f'''
    <div class="panel">
      <div class="result-box error" id="errorBox" style="display:none; margin-bottom:16px;">
        <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
        <div class="r-body"></div>
      </div>

      <div class="two-col" style="margin-bottom:16px;">
        <div class="field">
          <label for="baseDecimal">{t['decimal']}</label>
          <input type="text" id="baseDecimal" class="mono-area" placeholder="255" />
        </div>
        <div class="field">
          <label for="baseHex">{t['hex']}</label>
          <input type="text" id="baseHex" class="mono-area" placeholder="ff" />
        </div>
        <div class="field">
          <label for="baseBinary">{t['binary']}</label>
          <input type="text" id="baseBinary" class="mono-area" placeholder="11111111" />
        </div>
        <div class="field">
          <label for="baseOctal">{t['octal']}</label>
          <input type="text" id="baseOctal" class="mono-area" placeholder="377" />
        </div>
      </div>
      <p class="note" style="margin-top:0;">{t['type_hint']}</p>
    </div>

    <div class="panel">
      <h3 style="margin-top:0;">{t['custom_h']}</h3>
      <p class="note" style="margin-top:0; margin-bottom:16px;">{t['custom_sub']}</p>
      <div class="field" style="margin-bottom:16px;">
        <label for="customValue">{t['value']}</label>
        <input type="text" id="customValue" class="mono-area" placeholder="1a2b3c" value="1a2b3c" />
      </div>
      <div class="two-col" style="margin-bottom:16px;">
        <div class="field">
          <label for="customFrom">{t['from_base']}</label>
          <select id="customFrom">
            {from_opts}
          </select>
        </div>
        <div class="field">
          <label for="customTo">{t['to_base']}</label>
          <select id="customTo">
            {to_opts}
          </select>
        </div>
      </div>
      <div class="result-box error" id="customError" style="display:none; margin-bottom:16px;">
        <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
        <div class="r-body"></div>
      </div>
      <div class="field">
        <label for="customOutput">{t['result']}</label>
        <input type="text" id="customOutput" class="mono-area" readonly />
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
    title="Conversor de Base Numérica: Binario, Octal, Decimal, Hex | norito",
    meta_desc="Convierte números entre binario, octal, decimal y hexadecimal en vivo, más cualquier base personalizada de 2 a 36. Maneja números negativos y arbitrariamente grandes.",
    app_name="Conversor de Base Numérica", h1="Conversor de Base Numérica", breadcrumb_label="Conversor de Base Numérica",
    lede="Convierte un número entre binario, octal, decimal y hexadecimal en vivo, o entre dos bases cualesquiera de 2 a 36.",
    t=dict(
        base_word="Base",
        decimal="Decimal (base 10)", hex="Hexadecimal (base 16)", binary="Binario (base 2)", octal="Octal (base 8)",
        type_hint="Escribe en cualquier campo, los otros tres se actualizan en vivo. Admite números negativos y enteros arbitrariamente grandes.",
        custom_h="Conversión de base personalizada", custom_sub="Convierte entre dos bases cualesquiera de 2 a 36.",
        value="Valor", from_base="Desde base", to_base="A base", result="Resultado",
        how_h2="Cómo funciona",
        how_p1='Cada valor que escribes se analiza como un <code>BigInt</code> de JavaScript, un tipo entero de precisión arbitraria integrado en el navegador. El análisis recorre tu entrada dígito por dígito, multiplicando el total acumulado por la base y sumando el valor de cada dígito; la conversión de vuelta divide repetidamente entre la base objetivo y recopila los restos. Los dígitos por encima de 9 usan letras, así que la base 36 recorre 0-9 y luego a-z. Los números negativos también funcionan: se separa un signo menos inicial antes de analizar y se vuelve a pegar al final.',
        how_p2='La parte de BigInt es el detalle que vale la pena conocer. Los conversores construidos sobre números planos de JavaScript corrompen silenciosamente cualquier valor por encima de 9.007.199.254.740.991 (2^53 - 1), porque ahí es donde la coma flotante deja de representar cada entero exactamente. Pega un valor hexadecimal de 16 dígitos como <code>ffffffffffffffff</code> en uno de esos y obtienes una respuesta redondeada e incorrecta sin ninguna advertencia. Aquí la matemática es exacta a cualquier longitud: un decimal de 100 dígitos se convierte a binario correctamente, solo requiere más dígitos.',
        how_p3='Cada campo se valida contra su propia base mientras escribes, así que introducir un 9 en la casilla octal o una g en hex muestra un error en vez de un resultado erróneo, y los otros tres campos se actualizan en vivo desde el que hayas editado. Todo esto ocurre en tu pestaña: revisa el panel Red de las DevTools y verás que la página no hace ninguna petición mientras escribes, así que los números que conviertes nunca salen de tu máquina.',
    ),
    related_tools=[
        ("hash-generator.html", "Generador de hashes", "MD5, SHA-1, SHA-256 y SHA-512."),
        ("url-encoder-decoder.html", "Codificador / Decodificador de URL", "Codifica o decodifica en porcentaje una URL."),
        ("timestamp-converter.html", "Conversor de Timestamp", "Unix time a fecha, en ambas direcciones."),
    ],
)

PAGES["zh"] = dict(
    title="进制转换器：二进制、八进制、十进制、十六进制 | norito",
    meta_desc="实时在二进制、八进制、十进制和十六进制之间转换数字，还支持 2 到 36 之间任意自定义进制。支持负数和任意大的数字。",
    app_name="进制转换器", h1="进制转换器", breadcrumb_label="进制转换器",
    lede="在二进制、八进制、十进制和十六进制之间实时转换数字，或在 2 到 36 之间任意两个进制之间转换。",
    t=dict(
        base_word="进制",
        decimal="十进制（10 进制）", hex="十六进制（16 进制）", binary="二进制（2 进制）", octal="八进制（8 进制）",
        type_hint="在任意一个字段中输入，其余三个字段会实时更新。支持负数和任意大的整数。",
        custom_h="自定义进制转换", custom_sub="在 2 到 36 之间任意两个进制之间转换。",
        value="值", from_base="源进制", to_base="目标进制", result="结果",
        how_h2="工作原理",
        how_p1='你输入的每个值都会被解析为 JavaScript 的 <code>BigInt</code>，这是浏览器内置的一种任意精度整数类型。解析过程逐位处理你的输入，将累计总数乘以进制基数并加上每一位的值；反向转换则反复除以目标进制并收集余数。大于 9 的数字使用字母表示，所以 36 进制会依次使用 0-9 再到 a-z。负数同样支持：解析前会先剥离开头的负号，最后再拼接回去。',
        how_p2='BigInt 这部分是值得了解的细节。基于普通 JavaScript 数字构建的转换器，在处理超过 9,007,199,254,740,991（2^53 - 1）的数值时会悄悄发生错误，因为超过这个值浮点数就无法精确表示每一个整数了。把一个 16 位的十六进制值（比如 <code>ffffffffffffffff</code>）粘贴进这类工具，你会得到一个四舍五入后的错误答案，且没有任何警告。而这里的运算在任意长度下都是精确的：一个 100 位的十进制数也能正确转换为二进制，只是需要更多位数而已。',
        how_p3='每个字段在你输入时都会针对自身进制进行校验，因此在八进制框中输入 9，或在十六进制框中输入 g，会显示错误提示而不是给出一个无意义的结果，其余三个字段会根据你编辑的那个字段实时更新。这一切都发生在你的标签页内：查看开发者工具的 Network 面板，你会看到页面在你输入时不会发出任何请求，因此你转换的数字永远不会离开你的电脑。',
    ),
    related_tools=[
        ("hash-generator.html", "哈希生成器", "MD5、SHA-1、SHA-256、SHA-512。"),
        ("url-encoder-decoder.html", "URL 编码 / 解码工具", "对 URL 进行百分号编码或解码。"),
        ("timestamp-converter.html", "时间戳转换器", "Unix 时间与日期互转。"),
    ],
)

PAGES["ar"] = dict(
    title="محول قاعدة الأرقام: ثنائي، ثماني، عشري، ست عشري | norito",
    meta_desc="حوّل الأرقام بين الثنائي والثماني والعشري والست عشري مباشرة، بالإضافة إلى أي قاعدة مخصصة من 2 إلى 36. يتعامل مع الأرقام السالبة والكبيرة جدًا.",
    app_name="محول قاعدة الأرقام", h1="محول قاعدة الأرقام", breadcrumb_label="محول قاعدة الأرقام",
    lede="حوّل رقمًا بين الثنائي والثماني والعشري والست عشري مباشرة، أو بين أي قاعدتين من 2 إلى 36.",
    t=dict(
        base_word="القاعدة",
        decimal="عشري (قاعدة 10)", hex="ست عشري (قاعدة 16)", binary="ثنائي (قاعدة 2)", octal="ثماني (قاعدة 8)",
        type_hint="اكتب في أي حقل، وستتحدّث الحقول الثلاثة الأخرى مباشرة. يدعم الأرقام السالبة والأعداد الصحيحة الكبيرة بشكل عشوائي.",
        custom_h="تحويل قاعدة مخصصة", custom_sub="حوّل بين أي قاعدتين من 2 إلى 36.",
        value="القيمة", from_base="من قاعدة", to_base="إلى قاعدة", result="النتيجة",
        how_h2="كيف يعمل",
        how_p1='كل قيمة تكتبها تُحلَّل إلى <code>BigInt</code> في جافاسكريبت، وهو نوع عدد صحيح ذو دقة عشوائية مدمج في المتصفح. يمر التحليل عبر إدخالك رقمًا رقمًا، مضاعفًا المجموع الجاري بالقاعدة ومضيفًا قيمة كل رقم؛ والتحويل العكسي يقسّم بشكل متكرر على القاعدة الهدف ويجمع الباقي. الأرقام فوق 9 تستخدم أحرفًا، لذا تمر القاعدة 36 عبر 0-9 ثم a-z. الأرقام السالبة تعمل أيضًا: تُنزَع علامة الطرح البادئة قبل التحليل وتُعاد في النهاية.',
        how_p2='جزء BigInt هو التفصيل الذي يستحق المعرفة. المحوّلات المبنية على أرقام جافاسكريبت العادية تُفسد بصمت أي قيمة فوق 9,007,199,254,740,991 (2^53 - 1)، لأن هذا هو المكان الذي تتوقف فيه الفاصلة العائمة عن تمثيل كل عدد صحيح بدقة. الصق قيمة ست عشرية من 16 رقمًا مثل <code>ffffffffffffffff</code> في واحدة من تلك الأدوات وستحصل على إجابة مقرّبة وخاطئة دون أي تحذير. هنا الرياضيات دقيقة بأي طول: يتحول عدد عشري من 100 رقم إلى ثنائي بشكل صحيح، فقط يستغرق أرقامًا أكثر.',
        how_p3='يتحقق كل حقل من صحته وفق قاعدته الخاصة أثناء الكتابة، لذا يؤدي إدخال 9 في خانة الثماني أو g في الست عشري إلى إظهار خطأ بدلاً من نتيجة عشوائية، وتتحدّث الحقول الثلاثة الأخرى مباشرة وفقًا للحقل الذي عدّلته. كل هذا يحدث في تبويبك: تحقّق من لوحة Network في أدوات المطوّر وسترى أن الصفحة لا تُجري أي طلبات أثناء الكتابة، لذا الأرقام التي تحوّلها لا تغادر جهازك أبدًا.',
    ),
    related_tools=[
        ("hash-generator.html", "مولّد التجزئة", "MD5 وSHA-1 وSHA-256 وSHA-512."),
        ("url-encoder-decoder.html", "ترميز / فك ترميز URL", "رمّز بالنسبة المئوية أو فكّ ترميز رابط."),
        ("timestamp-converter.html", "محول الطابع الزمني", "توقيت Unix إلى تاريخ، في كلا الاتجاهين."),
    ],
)

PAGES["hi"] = dict(
    title="नंबर बेस कन्वर्टर: बाइनरी, ऑक्टल, डेसिमल, हेक्स | norito",
    meta_desc="बाइनरी, ऑक्टल, डेसिमल, और हेक्साडेसिमल के बीच लाइव कन्वर्ट करें, साथ ही 2 से 36 तक कोई भी कस्टम बेस। नेगेटिव और आर्बिट्ररिली बड़े नंबर्स को हैंडल करता है।",
    app_name="नंबर बेस कन्वर्टर", h1="नंबर बेस कन्वर्टर", breadcrumb_label="नंबर बेस कन्वर्टर",
    lede="बाइनरी, ऑक्टल, डेसिमल, और हेक्साडेसिमल के बीच किसी नंबर को लाइव कन्वर्ट करें, या 2 से 36 तक किन्हीं भी दो बेस के बीच।",
    t=dict(
        base_word="बेस",
        decimal="डेसिमल (बेस 10)", hex="हेक्साडेसिमल (बेस 16)", binary="बाइनरी (बेस 2)", octal="ऑक्टल (बेस 8)",
        type_hint="किसी भी फ़ील्ड में टाइप करें, बाक़ी तीनों लाइव अपडेट होते हैं। नेगेटिव नंबर्स और आर्बिट्ररिली बड़े इंटिजर्स सपोर्ट करता है।",
        custom_h="कस्टम बेस कन्वर्जन", custom_sub="2 से 36 तक किन्हीं भी दो बेस के बीच कन्वर्ट करें।",
        value="वैल्यू", from_base="बेस से", to_base="बेस में", result="परिणाम",
        how_h2="यह कैसे काम करता है",
        how_p1='आप जो भी वैल्यू टाइप करते हैं वह JavaScript के <code>BigInt</code> में पार्स होती है, जो ब्राउज़र में बिल्ट-इन एक आर्बिट्ररी-प्रिसीज़न इंटिजर टाइप है। पार्सिंग आपके इनपुट को अंक-दर-अंक चलती है, रनिंग टोटल को बेस से गुणा करते हुए और हर अंक की वैल्यू जोड़ते हुए; वापस कन्वर्ट करना बार-बार टारगेट बेस से डिवाइड करता है और रिमेंडर्स इकट्ठा करता है। 9 से ऊपर के अंक लेटर्स इस्तेमाल करते हैं, इसलिए बेस 36 में 0-9 फिर a-z चलता है। नेगेटिव नंबर्स भी काम करते हैं: पार्स करने से पहले एक लीडिंग माइनस साइन को हटाया जाता है और आख़िर में वापस जोड़ा जाता है।',
        how_p2='BigInt वाला हिस्सा जानने लायक डिटेल है। प्लेन JavaScript नंबर्स पर बने कन्वर्टर्स 9,007,199,254,740,991 (2^53 - 1) से ऊपर की किसी भी चीज़ को चुपचाप ख़राब कर देते हैं, क्योंकि यहीं फ़्लोटिंग पॉइंट हर इंटिजर को एग्ज़ैक्टली रिप्रज़ेंट करना बंद कर देता है। <code>ffffffffffffffff</code> जैसी 16-डिजिट हेक्स वैल्यू को उनमें से किसी में पेस्ट करें और आपको बिना किसी चेतावनी के एक राउंडेड, ग़लत जवाब मिलता है। यहां गणित किसी भी लंबाई पर एग्ज़ैक्ट है: 100-डिजिट का डेसिमल सही तरीक़े से बाइनरी में कन्वर्ट होता है, बस ज़्यादा डिजिट लगते हैं।',
        how_p3='हर फ़ील्ड टाइप करते समय अपने ख़ुद के बेस के ख़िलाफ़ वैलिडेट होती है, इसलिए ऑक्टल बॉक्स में 9 या हेक्स में g डालने पर एक ग़लत रिज़ल्ट के बजाय एरर दिखता है, और बाक़ी तीनों फ़ील्ड्स लाइव अपडेट होती हैं जिस भी फ़ील्ड को आपने एडिट किया उससे। यह सब आपके टैब में होता है: डेवटूल्स का Network पैनल चेक करें और आप देखेंगे कि टाइप करते समय पेज कोई रिक्वेस्ट नहीं करता, इसलिए आप जो नंबर्स कन्वर्ट करते हैं वे कभी आपकी मशीन से बाहर नहीं जाते।',
    ),
    related_tools=[
        ("hash-generator.html", "हैश जनरेटर", "MD5, SHA-1, SHA-256, SHA-512."),
        ("url-encoder-decoder.html", "URL एनकोडर / डिकोडर", "किसी URL को पर्सेंट-एनकोड या डिकोड करें।"),
        ("timestamp-converter.html", "टाइमस्टैंप कन्वर्टर", "Unix टाइम से तारीख़, दोनों दिशाओं में।"),
    ],
)

PAGES["ru"] = dict(
    title="Конвертер систем счисления: двоичная, восьмеричная, десятичная, шестнадцатеричная | norito",
    meta_desc="Конвертируйте числа между двоичной, восьмеричной, десятичной и шестнадцатеричной системами в реальном времени, а также в любой пользовательской системе от 2 до 36. Поддерживает отрицательные и произвольно большие числа.",
    app_name="Конвертер систем счисления", h1="Конвертер систем счисления", breadcrumb_label="Конвертер систем счисления",
    lede="Конвертируйте число между двоичной, восьмеричной, десятичной и шестнадцатеричной системами в реальном времени, или между любыми двумя системами от 2 до 36.",
    t=dict(
        base_word="Основание",
        decimal="Десятичная (основание 10)", hex="Шестнадцатеричная (основание 16)", binary="Двоичная (основание 2)", octal="Восьмеричная (основание 8)",
        type_hint="Введите значение в любое поле — остальные три обновятся автоматически. Поддерживает отрицательные числа и произвольно большие целые числа.",
        custom_h="Конвертация в произвольную систему", custom_sub="Конвертируйте между любыми двумя системами от 2 до 36.",
        value="Значение", from_base="Из системы", to_base="В систему", result="Результат",
        how_h2="Как это работает",
        how_p1='Каждое введённое вами значение разбирается в JavaScript-тип <code>BigInt</code> — целое число произвольной точности, встроенное в браузер. Разбор проходит по вашему вводу цифра за цифрой, умножая текущий итог на основание системы и прибавляя значение каждой цифры; обратная конвертация многократно делит на целевое основание и собирает остатки. Цифры выше 9 используют буквы, поэтому в системе с основанием 36 идёт последовательность 0-9, а затем a-z. Отрицательные числа тоже работают: ведущий знак минус отделяется перед разбором и добавляется обратно в конце.',
        how_p2='Часть с BigInt — это деталь, которую стоит знать. Конвертеры, построенные на обычных числах JavaScript, незаметно повреждают любое значение выше 9 007 199 254 740 991 (2^53 - 1), потому что именно с этого момента числа с плавающей точкой перестают точно представлять каждое целое число. Вставьте в такой конвертер 16-значное шестнадцатеричное значение вроде <code>ffffffffffffffff</code>, и вы получите округлённый, неверный ответ без какого-либо предупреждения. Здесь же вычисления точны при любой длине: 100-значное десятичное число корректно конвертируется в двоичное, просто получится больше цифр.',
        how_p3='Каждое поле проверяется на соответствие своей системе счисления по мере ввода, поэтому ввод 9 в восьмеричное поле или g в шестнадцатеричное покажет ошибку вместо бессмысленного результата, а остальные три поля обновляются в реальном времени в зависимости от того, какое вы редактировали. Всё это происходит в вашей вкладке: проверьте панель Network в DevTools, и вы увидите, что страница не отправляет ни одного запроса во время ввода, поэтому конвертируемые вами числа никогда не покидают ваш компьютер.',
    ),
    related_tools=[
        ("hash-generator.html", "Генератор хешей", "MD5, SHA-1, SHA-256, SHA-512."),
        ("url-encoder-decoder.html", "Кодировщик / декодировщик URL", "Кодируйте в процентном формате или декодируйте URL."),
        ("timestamp-converter.html", "Конвертер меток времени", "Unix-время в дату и обратно."),
    ],
)

PAGES["ja"] = dict(
    title="進数変換ツール：2進数、8進数、10進数、16進数 | norito",
    meta_desc="2進数、8進数、10進数、16進数の間でリアルタイムに数値を変換。2〜36の任意のカスタム進数にも対応。負の数や任意の大きさの数値も扱えます。",
    app_name="進数変換ツール", h1="進数変換ツール", breadcrumb_label="進数変換ツール",
    lede="2進数、8進数、10進数、16進数の間で数値をリアルタイムに変換、または2〜36の任意の2つの進数間で変換します。",
    t=dict(
        base_word="基数",
        decimal="10進数（基数10）", hex="16進数（基数16）", binary="2進数（基数2）", octal="8進数（基数8）",
        type_hint="いずれかのフィールドに入力すると、残りの3つがリアルタイムに更新されます。負の数や任意の大きさの整数に対応しています。",
        custom_h="カスタム進数変換", custom_sub="2〜36の任意の2つの進数間で変換します。",
        value="値", from_base="変換元の基数", to_base="変換先の基数", result="結果",
        how_h2="仕組み",
        how_p1='入力した各値は、ブラウザに組み込まれた任意精度整数型であるJavaScriptの<code>BigInt</code>として解析されます。解析は入力を1桁ずつ処理し、累計値を基数倍しながら各桁の値を加算します。逆変換は目標の基数で繰り返し除算し、余りを収集します。9より大きい桁は文字を使用するため、基数36では0-9の後にa-zが続きます。負の数も扱えます。解析前に先頭のマイナス記号が取り除かれ、最後に再び付加されます。',
        how_p2='知っておく価値があるのはBigInt部分です。通常のJavaScript数値の上に構築された変換ツールは、9,007,199,254,740,991（2^53 - 1）を超える値を警告なしに静かに壊してしまいます。これは浮動小数点がすべての整数を正確に表現できなくなる境界だからです。<code>ffffffffffffffff</code>のような16桁の16進値をそうしたツールに貼り付けると、警告なしに丸められた誤った答えが返ってきます。ここでの計算はどんな桁数でも正確です。100桁の10進数も正しく2進数に変換されます。ただ、桁数が多くなるだけです。',
        how_p3='各フィールドは入力中にそれぞれの基数に対して検証されるため、8進数ボックスに9を入力したり16進数にgを入力したりすると、無意味な結果ではなくエラーが表示されます。他の3つのフィールドは、編集したフィールドに基づいてリアルタイムに更新されます。これらはすべてタブ内で行われます。DevToolsのNetworkパネルを確認すると、入力中にページが一切リクエストを送信していないことがわかります。そのため、変換する数値があなたのマシンから外に出ることはありません。',
    ),
    related_tools=[
        ("hash-generator.html", "ハッシュジェネレーター", "MD5、SHA-1、SHA-256、SHA-512。"),
        ("url-encoder-decoder.html", "URLエンコード/デコードツール", "URLをパーセントエンコードまたはデコード。"),
        ("timestamp-converter.html", "タイムスタンプ変換ツール", "Unix時間と日付を双方向に変換。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "number-base-converter.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-base-converter.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/number-base-converter.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
