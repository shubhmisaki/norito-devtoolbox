#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

LOCALE_META = {
    "es": {"lang": "es", "dir": "ltr", "og_locale": "es_ES"},
    "zh": {"lang": "zh-Hans", "dir": "ltr", "og_locale": "zh_CN"},
    "ar": {"lang": "ar", "dir": "rtl", "og_locale": "ar_AR"},
    "hi": {"lang": "hi", "dir": "ltr", "og_locale": "hi_IN"},
    "ru": {"lang": "ru", "dir": "ltr", "og_locale": "ru_RU"},
    "ja": {"lang": "ja", "dir": "ltr", "og_locale": "ja_JP"},
}
ALL_LOCALES = ["en", "es", "zh", "ar", "hi", "ru", "ja"]

def url(loc, path):
    prefix = "" if loc == "en" else f"/{loc}"
    return f"https://norito.in{prefix}/{path}"

# (slug, icon_svg, accent, icon_class)
CARDS_META = [
    ("pdf-compression-explained.html", "purple", "c-purple", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m10 12-2 2 2 2M14 12l2 2-2 2"/></svg>'),
    ("how-password-entropy-works.html", "indigo", "c-indigo", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'),
    ("client-side-vs-server-side-tools.html", "coral", "c-coral", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>'),
    ("image-format-guide-2026.html", "teal", "c-teal", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/></svg>'),
    ("image-compression-without-losing-quality.html", "coral", "c-coral", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/></svg>'),
    ("jpg-vs-png-vs-webp.html", "teal", "c-teal", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/></svg>'),
    ("how-to-merge-pdfs-for-free.html", "purple", "c-purple", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"/><path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"/><path d="M15 2v5h5"/></svg>'),
    ("what-is-a-uuid.html", "indigo", "c-indigo", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m18 14 4 4-4 4"/><path d="m18 2 4 4-4 4"/><path d="M2 18h1.973a4 4 0 0 0 3.3-1.7l5.454-8.6a4 4 0 0 1 3.3-1.7H22"/><path d="M2 6h1.972a4 4 0 0 1 3.6 2.2"/><path d="M22 18h-6.041a4 4 0 0 1-3.3-1.8l-.36-.54"/></svg>'),
    ("wcag-contrast-checking-guide.html", "teal", "c-teal", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-12"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="6" r="3"/></svg>'),
]

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

# Per-locale content: title, meta_desc, h1, lede, breadcrumb_label, read_guide label,
# and list of (headline, blurb) matching CARDS_META order.
DATA = {}

DATA["es"] = dict(
    title="Blog: Guías para las Herramientas Gratis de norito | norito",
    meta_desc="Guías prácticas sobre compresión de imágenes, formatos de archivo, PDFs, y accesibilidad web, junto a las herramientas gratuitas de norito.",
    h1="Blog", breadcrumb_label="Blog", read_guide="Leer guía",
    lede="Guías prácticas sobre compresión de imágenes, formatos de archivo, PDFs, y accesibilidad web, cada una vinculada a una herramienta gratuita que puedes usar de inmediato.",
    cards=[
        ("Por qué la compresión de PDF funciona genial en escaneos y casi nada en informes", "Qué ocupa realmente el espacio en un PDF, por qué los escaneos se reducen un 90% mientras los informes de texto apenas cambian, y cómo predecir tu resultado."),
        ("Entropía de contraseñas, explicada con números reales", "Las matemáticas detrás de la fortaleza de las contraseñas, tiempos reales de descifrado, por qué ganan las frases de contraseña, y qué reglas de contraseñas son mitos."),
        ("A dónde van realmente tus archivos cuando usas una herramienta online", "Herramientas basadas en subida vs. procesamiento solo en el navegador, cómo verificar la diferencia en DevTools, y cuándo un servidor es realmente necesario."),
        ("AVIF, WebP, JPEG, PNG: qué formato usar cuándo, en 2026", "Una guía de decisión práctica con números reales de compresión, realidades de compatibilidad, y los casos donde JPEG sigue siendo la opción correcta."),
        ("Cómo comprimir imágenes sin perder calidad", "Por qué a veces los archivos más pequeños se ven peor, y los tres ajustes que realmente determinan cuánto detalle sobrevive a la compresión."),
        ("JPG vs PNG vs WebP: ¿qué formato de imagen deberías usar?", "Una comparación en lenguaje sencillo de los tres formatos, y una forma rápida de decidir cuál se ajusta a tu imagen."),
        ("Cómo unir PDFs gratis (sin software, sin registro)", "Tres formas de combinar varios PDFs en un solo archivo, incluyendo una opción basada en el navegador que nunca sube tus archivos."),
        ("¿Qué es un UUID? Una explicación en lenguaje sencillo", "Por qué un UUID está prácticamente garantizado a ser único sin una autoridad central, y cuándo realmente necesitarías uno."),
        ("Verificación de contraste WCAG: una guía práctica", "Qué miden realmente las ratios de contraste, los umbrales reales de AA y AAA, y los errores de contraste más comunes."),
    ],
)

DATA["zh"] = dict(
    title="博客：norito 免费浏览器工具使用指南 | norito",
    meta_desc="关于图片压缩、文件格式、PDF 和网页无障碍访问的实用指南，均与 norito 的免费浏览器工具相关联。",
    h1="博客", breadcrumb_label="博客", read_guide="阅读指南",
    lede="关于图片压缩、文件格式、PDF 和网页无障碍访问的实用指南，每一篇都关联一个可立即使用的免费工具。",
    cards=[
        ("为什么 PDF 压缩对扫描件效果显著，对报告文档却几乎没用", "PDF 中究竟是什么占用了空间，为什么扫描件能缩小 90%，而文本报告几乎不变，以及如何预测你的压缩结果。"),
        ("用真实数字讲清楚密码熵", "密码强度背后的数学原理、真实的破解时间数据、为什么密码短语更胜一筹，以及哪些密码规则其实是误区。"),
        ("使用在线工具时，你的文件到底去了哪里", "基于上传的工具与纯浏览器处理的对比、如何在开发者工具中验证两者的区别，以及何时才真正需要服务器。"),
        ("AVIF、WebP、JPEG、PNG：2026 年该在何时选用哪种格式", "一份附带真实压缩数据、兼容性现实情况的实用决策指南，以及 JPEG 仍是正确选择的场景。"),
        ("如何在不损失画质的情况下压缩图片", "为什么有时更小的文件反而看起来更差，以及真正决定压缩后细节留存程度的三个设置。"),
        ("JPG、PNG、WebP：你应该用哪种图片格式？", "用通俗易懂的语言对比这三种格式，并提供一个快速判断哪种格式适合你图片的方法。"),
        ("如何免费合并 PDF（无需软件，无需注册）", "三种将多个 PDF 合并为一个文件的方法，其中包括一种基于浏览器、绝不上传文件的方案。"),
        ("什么是 UUID？通俗易懂的解释", "为什么 UUID 在没有中央权威机构的情况下几乎能保证唯一，以及你何时真正需要用到它。"),
        ("WCAG 对比度检测：实用指南", "对比度实际衡量的是什么、AA 和 AAA 的真实阈值，以及最常见的对比度错误。"),
    ],
)

DATA["ar"] = dict(
    title="المدونة: أدلة لأدوات norito المجانية في المتصفح | norito",
    meta_desc="أدلة عملية حول ضغط الصور، وصيغ الملفات، وملفات PDF، وإمكانية الوصول على الويب، مرتبطة بأدوات norito المجانية في المتصفح.",
    h1="المدونة", breadcrumb_label="المدونة", read_guide="اقرأ الدليل",
    lede="أدلة عملية حول ضغط الصور، وصيغ الملفات، وملفات PDF، وإمكانية الوصول على الويب، كل واحد منها مرتبط بأداة مجانية يمكنك استخدامها فورًا.",
    cards=[
        ("لماذا يعمل ضغط PDF بشكل رائع على المستندات الممسوحة ضوئيًا ولا يكاد يعمل على التقارير", "ما الذي يشغل المساحة فعليًا في ملف PDF، ولماذا تنكمش المستندات الممسوحة ضوئيًا بنسبة 90% بينما لا تتغير تقارير النصوص كثيرًا، وكيف تتوقع نتيجتك."),
        ("إنتروبيا كلمة المرور، موضحة بأرقام حقيقية", "الرياضيات وراء قوة كلمة المرور، وأرقام حقيقية لوقت الاختراق، ولماذا تفوز عبارات المرور، وأي قواعد كلمات المرور مجرد خرافات."),
        ("إلى أين تذهب ملفاتك فعليًا عند استخدام أداة أونلاين", "الأدوات المعتمدة على الرفع مقابل المعالجة داخل المتصفح فقط، وكيفية التحقق من الفرق في أدوات المطوّر، ومتى يكون الخادم مطلوبًا فعليًا."),
        ("AVIF وWebP وJPEG وPNG: أي صيغة تستخدم ومتى، في 2026", "دليل قرار عملي بأرقام ضغط حقيقية، وحقائق التوافق، والحالات التي يظل فيها JPEG هو الخيار الصحيح."),
        ("كيف تضغط الصور دون فقدان الجودة", "لماذا تبدو الملفات الأصغر أحيانًا أسوأ، والإعدادات الثلاثة التي تحدد فعليًا مقدار التفاصيل التي تنجو من الضغط."),
        ("JPG مقابل PNG مقابل WebP: أي صيغة صورة يجب أن تستخدم؟", "مقارنة بلغة بسيطة بين الصيغ الثلاث، وطريقة سريعة لتحديد أيها يناسب صورتك."),
        ("كيف تدمج ملفات PDF مجانًا (دون برامج، دون تسجيل)", "ثلاث طرق لدمج عدة ملفات PDF في ملف واحد، بما في ذلك خيار قائم على المتصفح لا يرفع ملفاتك أبدًا."),
        ("ما هو UUID؟ شرح بلغة بسيطة", "لماذا يكاد يكون UUID مضمونًا أن يكون فريدًا دون وجود سلطة مركزية، ومتى قد تحتاج إليه فعليًا."),
        ("فحص تباين WCAG: دليل عملي", "ما الذي تقيسه نسب التباين فعليًا، وعتبات AA وAAA الحقيقية، وأكثر أخطاء التباين شيوعًا."),
    ],
)

DATA["hi"] = dict(
    title="ब्लॉग: norito के मुफ़्त ब्राउज़र टूल्स के लिए गाइड | norito",
    meta_desc="इमेज कंप्रेशन, फ़ाइल फ़ॉर्मैट, PDF, और वेब एक्सेसिबिलिटी पर व्यावहारिक गाइड, norito के मुफ़्त ब्राउज़र-आधारित टूल्स से जुड़े हुए.",
    h1="ब्लॉग", breadcrumb_label="ब्लॉग", read_guide="गाइड पढ़ें",
    lede="इमेज कंप्रेशन, फ़ाइल फ़ॉर्मैट, PDF, और वेब एक्सेसिबिलिटी पर व्यावहारिक गाइड, हर एक ऐसे मुफ़्त टूल से जुड़ी है जिसे आप तुरंत इस्तेमाल कर सकते हैं.",
    cards=[
        ("PDF कंप्रेशन स्कैन पर शानदार क्यों काम करता है और रिपोर्ट पर लगभग नहीं", "PDF में असल में जगह क्या घेरती है, स्कैन 90% क्यों सिकुड़ जाते हैं जबकि टेक्स्ट रिपोर्ट लगभग नहीं बदलती, और अपने नतीजे का अंदाज़ा कैसे लगाएं."),
        ("असली नंबरों के साथ पासवर्ड एन्ट्रॉपी, समझाया गया", "पासवर्ड की मज़बूती के पीछे का गणित, असली क्रैक-टाइम नंबर, पासफ़्रेज़ क्यों जीतते हैं, और कौन से पासवर्ड नियम सिर्फ़ मिथक हैं."),
        ("ऑनलाइन टूल इस्तेमाल करने पर आपकी फ़ाइलें असल में कहां जाती हैं", "अपलोड-आधारित टूल बनाम सिर्फ़ ब्राउज़र में प्रोसेसिंग, DevTools में फ़र्क़ कैसे जांचें, और सर्वर की वाक़ई कब ज़रूरत होती है."),
        ("AVIF, WebP, JPEG, PNG: 2026 में कब कौन-सा फ़ॉर्मैट इस्तेमाल करें", "असली कंप्रेशन नंबरों, कम्पैटिबिलिटी की हक़ीक़त, और उन मामलों के साथ एक व्यावहारिक निर्णय गाइड जहां JPEG अब भी सही चुनाव है."),
        ("बिना क्वालिटी खोए इमेज कैसे कंप्रेस करें", "छोटी फ़ाइलें कभी-कभी बदतर क्यों दिखती हैं, और वे तीन सेटिंग्स जो असल में तय करती हैं कि कंप्रेशन के बाद कितना डिटेल बचता है."),
        ("JPG बनाम PNG बनाम WebP: आपको कौन-सा इमेज फ़ॉर्मैट इस्तेमाल करना चाहिए?", "तीनों फ़ॉर्मैट की आसान भाषा में तुलना, और यह तय करने का एक तेज़ तरीका कि आपकी इमेज के लिए कौन-सा सही है."),
        ("PDFs मुफ़्त में कैसे मर्ज करें (बिना सॉफ़्टवेयर, बिना साइन-अप)", "कई PDFs को एक फ़ाइल में मिलाने के तीन तरीके, जिसमें एक ब्राउज़र-आधारित विकल्प भी शामिल है जो आपकी फ़ाइलें कभी अपलोड नहीं करता."),
        ("UUID क्या है? आसान भाषा में समझाया गया", "बिना किसी केंद्रीय अथॉरिटी के UUID के यूनीक होने की लगभग गारंटी क्यों होती है, और आपको इसकी असल में कब ज़रूरत पड़ेगी."),
        ("WCAG कंट्रास्ट चेकिंग: एक व्यावहारिक गाइड", "कंट्रास्ट रेशियो असल में क्या मापते हैं, असली AA और AAA थ्रेशहोल्ड, और सबसे आम कंट्रास्ट गलतियां."),
    ],
)

DATA["ru"] = dict(
    title="Блог: руководства по бесплатным браузерным инструментам norito | norito",
    meta_desc="Практические руководства по сжатию изображений, форматам файлов, PDF и веб-доступности, связанные с бесплатными браузерными инструментами norito.",
    h1="Блог", breadcrumb_label="Блог", read_guide="Читать руководство",
    lede="Практические руководства по сжатию изображений, форматам файлов, PDF и веб-доступности — каждое привязано к бесплатному инструменту, которым можно воспользоваться сразу же.",
    cards=[
        ("Почему сжатие PDF отлично работает на сканах и почти не работает на отчётах", "Что на самом деле занимает место в PDF, почему сканы сжимаются на 90%, а текстовые отчёты почти не меняются, и как предсказать свой результат."),
        ("Энтропия пароля, объяснённая на реальных числах", "Математика, стоящая за надёжностью пароля, реальные значения времени взлома, почему побеждают парольные фразы, и какие правила паролей — просто мифы."),
        ("Куда на самом деле уходят ваши файлы при использовании онлайн-инструмента", "Инструменты на основе загрузки файлов против обработки только в браузере, как проверить разницу в DevTools, и когда сервер действительно необходим."),
        ("AVIF, WebP, JPEG, PNG: какой формат когда использовать в 2026 году", "Практическое руководство по выбору с реальными цифрами сжатия, реалиями совместимости, и случаями, когда JPEG всё ещё правильный выбор."),
        ("Как сжимать изображения без потери качества", "Почему файлы меньшего размера иногда выглядят хуже, и три настройки, которые реально определяют, сколько деталей переживёт сжатие."),
        ("JPG против PNG против WebP: какой формат изображения использовать?", "Сравнение трёх форматов простым языком и быстрый способ решить, какой из них подходит для вашего изображения."),
        ("Как бесплатно объединить PDF (без программ, без регистрации)", "Три способа объединить несколько PDF в один файл, включая браузерный вариант, который никогда не загружает ваши файлы."),
        ("Что такое UUID? Объяснение простым языком", "Почему UUID практически гарантированно уникален без центрального органа, и когда он вам действительно понадобится."),
        ("Проверка контрастности по WCAG: практическое руководство", "Что на самом деле измеряют коэффициенты контрастности, реальные пороги AA и AAA, и самые частые ошибки с контрастом."),
    ],
)

DATA["ja"] = dict(
    title="ブログ：noritoの無料ブラウザツール活用ガイド | norito",
    meta_desc="画像圧縮、ファイル形式、PDF、Webアクセシビリティに関する実践的なガイド。noritoの無料ブラウザツールと連携しています。",
    h1="ブログ", breadcrumb_label="ブログ", read_guide="ガイドを読む",
    lede="画像圧縮、ファイル形式、PDF、Webアクセシビリティに関する実践的なガイドです。それぞれがすぐに使える無料ツールと結びついています。",
    cards=[
        ("PDF圧縮がスキャン画像には効くのに、レポートにはほとんど効かない理由", "PDFで実際にスペースを占めているものは何か、なぜスキャン画像は90%も縮むのにテキストレポートはほとんど変わらないのか、そして結果を予測する方法。"),
        ("実際の数字で解説するパスワードエントロピー", "パスワードの強度を支える数学、実際の解読時間の数値、パスフレーズが優れている理由、そしてどのパスワードルールが単なる俗説なのか。"),
        ("オンラインツールを使うとき、あなたのファイルは実際どこへ行くのか", "アップロード型ツールとブラウザのみの処理の違い、DevToolsでその違いを確認する方法、そして本当にサーバーが必要な場合。"),
        ("AVIF、WebP、JPEG、PNG：2026年、どの場面でどの形式を使うべきか", "実際の圧縮数値と互換性の実情を踏まえた実践的な判断ガイド、そしてJPEGが今なお正解となるケース。"),
        ("画質を落とさずに画像を圧縮する方法", "なぜ小さいファイルの方が見た目が悪くなることがあるのか、そして圧縮後にどれだけディテールが残るかを実際に左右する3つの設定。"),
        ("JPG対PNG対WebP：どの画像形式を使うべきか？", "3つの形式を平易な言葉で比較し、自分の画像にどれが合うかを素早く判断する方法。"),
        ("PDFを無料で結合する方法（ソフト不要、登録不要）", "複数のPDFを1つのファイルにまとめる3つの方法。ファイルを一切アップロードしないブラウザベースの選択肢を含みます。"),
        ("UUIDとは？平易な言葉での説明", "中央機関なしでUUIDがほぼ確実に一意になる理由、そして実際にいつ必要になるのか。"),
        ("WCAGコントラストチェック：実践ガイド", "コントラスト比が実際に何を測定しているのか、AAとAAAの本当のしきい値、そして最もよくあるコントラストの間違い。"),
    ],
)

for loc, d in DATA.items():
    meta = LOCALE_META[loc]
    canonical = url(loc, "blog/")
    hreflang_lines = []
    for hl in ALL_LOCALES:
        href = url(hl, "blog/")
        hreflang_lines.append(f'<link rel="alternate" hreflang="{hl}" href="{href}" />')
    hreflang_lines.append(f'<link rel="alternate" hreflang="x-default" href="{url("en", "blog/")}" />')
    hreflang_block = "\n".join(hreflang_lines)

    has_part = ",\n    ".join(
        f'{{ "@type": "Article", "headline": "{d["cards"][i][0]}", "url": "{url(loc, CARDS_META[i][0])}" }}'
        for i in range(9)
    )

    cards_html = []
    for i, (slug, accent, icon_class, icon_svg) in enumerate(CARDS_META):
        headline, blurb = d["cards"][i]
        cards_html.append(f'''      <a class="card" data-accent="{accent}" href="{slug}">
        <div class="icon-chip {icon_class}">
          {icon_svg}
        </div>
        <h3>{headline}</h3>
        <p>{blurb}</p>
        <span class="card-link">{d["read_guide"]}
          {ARROW}
        </span>
      </a>''')
    cards_block = "\n\n".join(cards_html)

    og_locale_line = f'<meta property="og:locale" content="{meta["og_locale"]}" />\n' if loc != "en" else ""

    html = f'''<!DOCTYPE html>
<html lang="{meta["lang"]}" dir="{meta["dir"]}">
<head>
    <!--INCLUDE:HEAD-COMMON-->
<title>{d["title"]}</title>
<meta name="description" content="{d["meta_desc"]}" />
<link rel="canonical" href="{canonical}" />
{hreflang_block}
<meta property="og:type" content="website" />
<meta property="og:title" content="{d["title"]}" />
<meta property="og:description" content="{d["meta_desc"]}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:site_name" content="norito" />
{og_locale_line}<meta property="og:image" content="https://norito.in/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{d["title"]}" />
<meta name="twitter:description" content="{d["meta_desc"]}" />
<meta name="twitter:image" content="https://norito.in/assets/og-image.png" />
<link rel="stylesheet" href="/css/style.css" />

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "{d["h1"]}",
  "url": "{canonical}",
  "description": "{d["meta_desc"]}",
  "isPartOf": {{ "@type": "WebSite", "name": "norito", "url": "{url(loc, "")}" }},
  "hasPart": [
    {has_part}
  ]
}}
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4040839176833351" crossorigin="anonymous"></script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "norito",
      "item": "{url(loc, "")}"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "{d["breadcrumb_label"]}",
      "item": "{canonical}"
    }}
  ]
}}
</script>
</head>
<body>
<div class="bg-blobs" aria-hidden="true">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
</div>

<!--INCLUDE:HEADER:content-->

<main>
  <div class="wrap">
    <div class="tool-hero">
    <div class="tool-hero-icon icon-chip c-coral"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></div>
    <div class="tool-hero-text">
    <p class="breadcrumb"><a href="../index.html">norito</a> / {d["breadcrumb_label"]}</p>
    <h1>{d["h1"]}</h1>
    <p class="lede">
      {d["lede"]}
    </p>
    </div>
  </div>

    <div class="grid-cards">
{cards_block}
    </div>
  </div>
</main>

<!--INCLUDE:FOOTER:standard-->

<!--INCLUDE:FOOT-SCRIPTS-MID-->
<!--INCLUDE:CMDK-OVERLAY-->

<!--INCLUDE:FOOT-SCRIPTS-TAIL-->
'''
    outdir = f"src/{loc}/blog"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/index.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
