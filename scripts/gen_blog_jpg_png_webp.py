#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from blog_lib import render_article

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

SLUG = "jpg-vs-png-vs-webp.html"
DATE_ISO = "2026-07-15"
DATE_HUMAN = {
    "es": "15 de julio de 2026", "zh": "2026年7月15日", "ar": "15 يوليو 2026",
    "hi": "15 जुलाई, 2026", "ru": "15 июля 2026 г.", "ja": "2026年7月15日",
}
ICON = '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'

def body(t):
    return f'''    <h2>{t['h2_1']}</h2>
    <p>{t['p1']}</p>

    <h2>{t['h2_2']}</h2>
    <p>{t['p2']}</p>

    <h2>{t['h2_3']}</h2>
    <p>{t['p3']}</p>

    <h2>{t['h2_4']}</h2>
    <p>{t['p4']}</p>

    <h2>{t['h2_5']}</h2>
    <p>{t['p5']}</p>

    <div class="result-box ok" style="margin-top:32px;">
      {ICON}
      <div class="r-body"><strong>{t['try_it']}</strong> <a href="../image-converter.html">{t['try_link']}</a>{t['try_desc']}</div>
    </div>
'''

DATA = {}

DATA["es"] = dict(
    title="JPG vs PNG vs WebP: ¿Qué Formato Deberías Usar? | norito",
    meta_desc="Una comparación en lenguaje sencillo de JPG, PNG, y WebP, cuándo cada uno es la elección correcta, y por qué WebP suele ganar para fotos hoy en día.",
    headline="JPG vs PNG vs WebP: ¿Qué Formato de Imagen Deberías Usar?",
    breadcrumb_label="JPG vs PNG vs WebP: ¿Qué Formato de Imagen Deberías Usar?",
    lede="Tres formatos, tres compromisos distintos. Aquí está lo que realmente los separa, y una forma rápida de decidir cuál se ajusta a tu imagen.",
    t=dict(
        h2_1="La respuesta corta",
        p1="Usa <strong>PNG</strong> para capturas de pantalla, logos, y cualquier cosa que necesite un fondo transparente. Usa <strong>JPEG</strong> para fotos donde el tamaño de archivo pequeño importa más que la calidad perfecta y necesitas máxima compatibilidad. Usa <strong>WebP</strong> para fotos cuando quieras el mejor equilibrio entre calidad y tamaño de archivo y no necesites soportar software muy antiguo.",
        h2_2="PNG: sin pérdida, y el único con soporte real de transparencia",
        p2="PNG nunca descarta datos de imagen, cada píxel que guardas es exactamente el píxel que recuperas. Eso lo hace la elección correcta para cualquier cosa con bordes nítidos o colores planos, capturas de pantalla, maquetas de UI, logos, diagramas, ya que la compresión con pérdida tiende a introducir borrosidad visible alrededor de bordes duros y texto. PNG también soporta un canal de transparencia alfa completo, así que es el formato al que recurrir siempre que parte de la imagen necesite ser transparente. El compromiso: para contenido fotográfico, los archivos PNG son típicamente de 3 a 10 veces más grandes que un JPEG o WebP equivalente, porque las fotos están llenas del tipo de degradados sutiles y ruido que la compresión sin pérdida no puede reducir mucho.",
        h2_3="JPEG: el formato de foto universal",
        p3="JPEG existe desde 1992 y es soportado por esencialmente todo software, navegador, y dispositivo fabricado desde entonces. Usa compresión con pérdida ajustada para contenido fotográfico, descartando detalle de formas difíciles de notar a tamaños de visualización normales. No tiene ningún soporte de transparencia, y tiende a mostrar artefactos en bloque visibles alrededor de texto nítido o bordes gráficos, por lo que es una mala opción para capturas de pantalla. Para fotos ordinarias donde la amplia compatibilidad importa (adjuntos de correo, sistemas más antiguos, laboratorios de impresión que solo aceptan JPEG), sigue siendo un valor predeterminado completamente razonable.",
        h2_4="WebP: normalmente el mejor formato de foto hoy en día",
        p4="Desarrollado por Google y ahora soportado en todo navegador importante, WebP típicamente produce archivos 25 a 35% más pequeños que JPEG a la misma calidad visual, y soporta tanto transparencia como compresión sin pérdida si las necesitas. Para una foto estándar destinada a un sitio web, una publicación social, o almacenamiento general, WebP suele ser el mejor compromiso disponible entre calidad y tamaño. La razón principal para evitarlo es la compatibilidad: algún software más antiguo, ciertos flujos de trabajo de impresión, o formularios de subida específicos pueden todavía aceptar solo JPEG o PNG.",
        h2_5="Una guía de decisión simple",
        p5="¿Necesitas transparencia, o es una captura de pantalla, logo, o gráfico con bordes nítidos y texto? Usa PNG. ¿Es una foto, y el destino requiere explícitamente JPEG (un sistema antiguo, un laboratorio de impresión, un formulario de subida exigente)? Usa JPEG. ¿Es una foto y tienes libre elección de formato? Usa WebP, obtendrás archivos notablemente más pequeños a la misma calidad sin ninguna desventaja real para casi cualquier caso de uso moderno.",
        try_it="Pruébalo tú mismo:", try_link="Conversor de Imágenes", try_desc=", para convertir entre JPG, PNG, y WebP directamente en tu navegador.",
    ),
)

DATA["zh"] = dict(
    title="JPG、PNG、WebP：你应该用哪种图片格式？ | norito",
    meta_desc="用通俗易懂的语言对比 JPG、PNG 和 WebP，说明各自适用的场合，以及为什么如今照片通常首选 WebP。",
    headline="JPG、PNG、WebP：你应该用哪种图片格式？",
    breadcrumb_label="JPG、PNG、WebP：你应该用哪种图片格式？",
    lede="三种格式，三种不同的取舍。这里说的是它们真正的区别，以及一个能快速判断哪种格式适合你的图片的方法。",
    t=dict(
        h2_1="简短答案",
        p1="截图、Logo，以及任何需要透明背景的内容，用<strong>PNG</strong>。当小文件体积比完美画质更重要，并且你需要最大程度兼容性时，照片用<strong>JPEG</strong>。当你想在画质和文件大小之间取得最佳平衡、又不需要支持非常旧的软件时，照片用<strong>WebP</strong>。",
        h2_2="PNG：无损，且是唯一真正支持透明度的格式",
        p2="PNG 从不丢弃图像数据，你保存的每一个像素，取回时都还是原来那个像素。这使它成为任何带有锐利边缘或纯色的内容——截图、UI 原型图、Logo、图表——的正确选择，因为有损压缩往往会在硬边缘和文字周围产生明显的模糊感。PNG 还支持完整的 alpha 透明通道，因此每当图像的某部分需要透明时，PNG 都是首选格式。代价是：对于照片类内容，PNG 文件通常比同等的 JPEG 或 WebP 大 3 到 10 倍，因为照片中充满了那种细腻的渐变和噪点，而无损压缩对这类内容的压缩效果非常有限。",
        h2_3="JPEG：通用的照片格式",
        p3="JPEG 自 1992 年问世以来，几乎被此后制造的每一款软件、浏览器和设备所支持。它使用专为照片类内容调校过的有损压缩，以正常查看尺寸下很难察觉的方式舍弃细节。它完全不支持透明度，并且在锐利文字或图形边缘周围往往会出现明显的块状伪影，这正是它不适合截图的原因。但对于需要广泛兼容性的普通照片场景（邮件附件、较旧的系统、只接受 JPEG 的印刷店），它依然是一个完全合理的默认选择。",
        h2_4="WebP：如今通常是最佳的照片格式",
        p4="WebP 由 Google 开发，现已被所有主流浏览器支持，在相同视觉质量下，它产生的文件通常比 JPEG 小 25% 到 35%，而且如果需要的话，它同时支持透明度和无损压缩。对于用于网站、社交媒体帖子或一般存储的标准照片，WebP 通常是画质与体积之间可获得的最佳折中方案。避免使用它的主要原因是兼容性：一些较旧的软件、某些印刷工作流程，或特定的上传表单可能仍然只接受 JPEG 或 PNG。",
        h2_5="一份简单的决策指南",
        p5="需要透明度，或者这是一张带有锐利边缘和文字的截图、Logo 或图形吗？用 PNG。这是一张照片，而目标平台明确要求使用 JPEG（比如老旧系统、印刷店，或者挑剔的上传表单）吗？用 JPEG。这是一张照片，而你可以自由选择格式吗？用 WebP——在几乎所有现代使用场景下，你都能在同等画质下获得明显更小的文件，而没有真正的缺点。",
        try_it="亲自试试：", try_link="图片格式转换工具", try_desc="，直接在你的浏览器中完成 JPG、PNG 和 WebP 之间的转换。",
    ),
)

DATA["ar"] = dict(
    title="JPG مقابل PNG مقابل WebP: أي صيغة يجب أن تستخدم؟ | norito",
    meta_desc="مقارنة بلغة بسيطة بين JPG وPNG وWebP، ومتى يكون كل منها الخيار الصحيح، ولماذا يفوز WebP عادةً للصور اليوم.",
    headline="JPG مقابل PNG مقابل WebP: أي صيغة صورة يجب أن تستخدم؟",
    breadcrumb_label="JPG مقابل PNG مقابل WebP: أي صيغة صورة يجب أن تستخدم؟",
    lede="ثلاث صيغ، ثلاث مقايضات مختلفة. إليك ما يفصل بينها فعليًا، وطريقة سريعة لتحديد أيها يناسب صورتك.",
    t=dict(
        h2_1="الإجابة القصيرة",
        p1="استخدم <strong>PNG</strong> للقطات الشاشة والشعارات وأي شيء يحتاج خلفية شفافة. استخدم <strong>JPEG</strong> للصور حيث يهم حجم الملف الصغير أكثر من الجودة المثالية وتحتاج توافقًا أقصى. استخدم <strong>WebP</strong> للصور عندما تريد أفضل توازن بين الجودة وحجم الملف ولا تحتاج دعم برامج قديمة جدًا.",
        h2_2="PNG: بلا فقدان، والوحيد بدعم شفافية حقيقي",
        p2="لا يتخلص PNG أبدًا من بيانات الصورة، كل بكسل تحفظه هو بالضبط البكسل الذي تستعيده. هذا يجعله الخيار الصحيح لأي شيء بحواف حادة أو ألوان مسطحة، لقطات الشاشة، نماذج واجهات المستخدم، الشعارات، المخططات، لأن الضغط المفقِد للبيانات يميل لإدخال ضبابية مرئية حول الحواف الصلبة والنص. يدعم PNG أيضًا قناة شفافية ألفا كاملة، لذا فهو الصيغة التي يُلجأ إليها كلما احتاج جزء من الصورة أن يكون شفافًا. المقايضة: بالنسبة للمحتوى الفوتوغرافي، ملفات PNG عادةً أكبر بـ 3 إلى 10 مرات من JPEG أو WebP المكافئ، لأن الصور مليئة بنوع التدرجات الدقيقة والضوضاء التي لا يستطيع الضغط بلا فقدان تصغيرها كثيرًا.",
        h2_3="JPEG: صيغة الصور الشاملة",
        p3="يوجد JPEG منذ 1992 ومدعوم عمليًا من كل برنامج ومتصفح وجهاز صُنع منذ ذلك الحين. يستخدم ضغطًا مفقِدًا للبيانات مضبوطًا للمحتوى الفوتوغرافي، متخلصًا من التفاصيل بطرق يصعب ملاحظتها بأحجام العرض العادية. لا يملك أي دعم للشفافية على الإطلاق، ويميل لإظهار تشوهات كتلية مرئية حول النص الحاد أو الحواف الرسومية، وهذا سبب كونه خيارًا سيئًا للقطات الشاشة. بالنسبة للصور العادية حيث يهم التوافق الواسع (مرفقات البريد الإلكتروني، الأنظمة الأقدم، معامل الطباعة التي تقبل JPEG فقط)، لا يزال خيارًا افتراضيًا معقولًا تمامًا.",
        h2_4="WebP: عادةً أفضل صيغة صور اليوم",
        p4="طُوِّر بواسطة Google ومدعوم الآن في كل متصفح رئيسي، ينتج WebP عادةً ملفات أصغر بنسبة 25 إلى 35% من JPEG بنفس الجودة المرئية، ويدعم كلاً من الشفافية والضغط بلا فقدان إذا احتجت إليهما. بالنسبة لصورة قياسية متجهة لموقع ويب، أو منشور اجتماعي، أو تخزين عام، WebP عادةً هو أفضل مقايضة متاحة بين الجودة والحجم. السبب الرئيسي لتجنّبه هو التوافق: قد لا تزال بعض البرامج الأقدم، أو تدفقات عمل طباعة معينة، أو نماذج رفع محددة تقبل JPEG أو PNG فقط.",
        h2_5="دليل قرار بسيط",
        p5="هل تحتاج شفافية، أو هي لقطة شاشة، أو شعار، أو رسم بحواف حادة ونص؟ استخدم PNG. هل هي صورة، وتتطلب الوجهة صراحةً JPEG (نظام قديم، معمل طباعة، نموذج رفع صارم)؟ استخدم JPEG. هل هي صورة ولديك حرية اختيار الصيغة؟ استخدم WebP، ستحصل على ملفات أصغر بشكل ملحوظ بنفس الجودة دون أي عيب حقيقي لأي حالة استخدام حديثة تقريبًا.",
        try_it="جرّبه بنفسك:", try_link="محوّل الصور", try_desc="، للتحويل بين JPG وPNG وWebP مباشرةً في متصفحك.",
    ),
)

DATA["hi"] = dict(
    title="JPG बनाम PNG बनाम WebP: आपको कौन-सा फ़ॉर्मैट इस्तेमाल करना चाहिए? | norito",
    meta_desc="JPG, PNG, और WebP की आसान भाषा में तुलना, कब हर एक सही चुनाव है, और आज फ़ोटो के लिए WebP आम तौर पर क्यों जीतता है।",
    headline="JPG बनाम PNG बनाम WebP: आपको कौन-सा इमेज फ़ॉर्मैट इस्तेमाल करना चाहिए?",
    breadcrumb_label="JPG बनाम PNG बनाम WebP: आपको कौन-सा इमेज फ़ॉर्मैट इस्तेमाल करना चाहिए?",
    lede="तीन फ़ॉर्मैट, तीन अलग-अलग ट्रेडऑफ़। यहां है वह जो असल में इन्हें अलग करता है, और यह तय करने का एक तेज़ तरीक़ा कि आपकी इमेज के लिए कौन-सा सही है।",
    t=dict(
        h2_1="छोटा जवाब",
        p1="स्क्रीनशॉट, लोगो, और ऐसी किसी भी चीज़ के लिए जिसे ट्रांसपेरेंट बैकग्राउंड चाहिए, <strong>PNG</strong> इस्तेमाल करें। उन फ़ोटो के लिए जहां छोटा फ़ाइल साइज़ परफ़ेक्ट क्वालिटी से ज़्यादा मायने रखता है और आपको अधिकतम कम्पैटिबिलिटी चाहिए, <strong>JPEG</strong> इस्तेमाल करें। जब आप क्वालिटी और फ़ाइल साइज़ का सबसे अच्छा बैलेंस चाहते हैं और बहुत पुराने सॉफ़्टवेयर को सपोर्ट करने की ज़रूरत नहीं है, तो फ़ोटो के लिए <strong>WebP</strong> इस्तेमाल करें।",
        h2_2="PNG: लॉसलेस, और असली ट्रांसपेरेंसी सपोर्ट वाला अकेला फ़ॉर्मैट",
        p2="PNG कभी इमेज डेटा नहीं फेंकता, आप जो भी पिक्सेल सेव करते हैं वह ठीक वही पिक्सेल है जो आपको वापस मिलता है। यह इसे शार्प एज या फ़्लैट रंगों वाली किसी भी चीज़, स्क्रीनशॉट, UI मॉकअप, लोगो, डायग्राम के लिए सही चुनाव बनाता है, क्योंकि लॉसी कंप्रेशन हार्ड एज और टेक्स्ट के आसपास नज़र आने वाली धुंधली छाप डालता है। PNG एक पूरा अल्फ़ा ट्रांसपेरेंसी चैनल भी सपोर्ट करता है, इसलिए जब भी इमेज के किसी हिस्से को पारदर्शी होना चाहिए, यह वही फ़ॉर्मैट है जिस तक पहुंचना चाहिए। ट्रेडऑफ़: फ़ोटोग्राफ़िक कंटेंट के लिए, PNG फ़ाइलें आम तौर पर बराबर के JPEG या WebP से 3 से 10 गुना बड़ी होती हैं, क्योंकि फ़ोटो उस तरह के सूक्ष्म ग्रेडिएंट और नॉइज़ से भरी होती हैं जिन्हें लॉसलेस कंप्रेशन ज़्यादा छोटा नहीं कर सकता।",
        h2_3="JPEG: यूनिवर्सल फ़ोटो फ़ॉर्मैट",
        p3="JPEG 1992 से मौजूद है और तब से बना लगभग हर सॉफ़्टवेयर, ब्राउज़र, और डिवाइस इसे सपोर्ट करता है। यह फ़ोटोग्राफ़िक कंटेंट के लिए ट्यून किया गया लॉसी कंप्रेशन इस्तेमाल करता है, ऐसे तरीक़ों से डिटेल फेंकता है जिन्हें सामान्य देखने के साइज़ पर नोटिस करना मुश्किल है। इसमें कोई ट्रांसपेरेंसी सपोर्ट बिल्कुल नहीं है, और यह शार्प टेक्स्ट या ग्राफ़िक एज के आसपास नज़र आने वाले ब्लॉकी आर्टिफ़ैक्ट दिखाता है, यही वजह है कि यह स्क्रीनशॉट के लिए एक ख़राब फ़िट है। ऐसी सामान्य फ़ोटो के लिए जहां व्यापक कम्पैटिबिलिटी मायने रखती है (ईमेल अटैचमेंट, पुराने सिस्टम, प्रिंट लैब जो सिर्फ़ JPEG स्वीकार करते हैं), यह अब भी एक पूरी तरह उचित डिफ़ॉल्ट है।",
        h2_4="WebP: आज आम तौर पर सबसे अच्छा फ़ोटो फ़ॉर्मैट",
        p4="Google द्वारा डेवलप किया गया और अब हर बड़े ब्राउज़र में सपोर्टेड, WebP आम तौर पर उसी विज़ुअल क्वालिटी पर JPEG से 25 से 35% छोटी फ़ाइलें बनाता है, और अगर आपको चाहिए तो यह ट्रांसपेरेंसी और लॉसलेस कंप्रेशन दोनों सपोर्ट करता है। किसी वेबसाइट, सोशल पोस्ट, या सामान्य स्टोरेज के लिए तय एक स्टैंडर्ड फ़ोटो के लिए, WebP आम तौर पर क्वालिटी और साइज़ के बीच उपलब्ध सबसे अच्छा ट्रेडऑफ़ है। इससे बचने की मुख्य वजह है कम्पैटिबिलिटी: कुछ पुराना सॉफ़्टवेयर, कुछ प्रिंट वर्कफ़्लो, या ख़ास अपलोड फ़ॉर्म अब भी सिर्फ़ JPEG या PNG स्वीकार कर सकते हैं।",
        h2_5="एक सिंपल निर्णय गाइड",
        p5="ट्रांसपेरेंसी चाहिए, या यह शार्प एज और टेक्स्ट वाला स्क्रीनशॉट, लोगो, या ग्राफ़िक है? PNG इस्तेमाल करें। यह एक फ़ोटो है, और डेस्टिनेशन साफ़ तौर पर JPEG मांगती है (एक पुराना सिस्टम, एक प्रिंट लैब, एक चूज़ी अपलोड फ़ॉर्म)? JPEG इस्तेमाल करें। यह एक फ़ोटो है और आपके पास फ़ॉर्मैट का आज़ाद चुनाव है? WebP इस्तेमाल करें, आपको लगभग किसी भी मॉडर्न इस्तेमाल के मामले में बिना किसी असली नुक़सान के उसी क्वालिटी पर काफ़ी छोटी फ़ाइलें मिलेंगी।",
        try_it="खुद आज़माएं:", try_link="इमेज कन्वर्टर", try_desc=", अपने ब्राउज़र में ही JPG, PNG, और WebP के बीच कन्वर्ट करने के लिए।",
    ),
)

DATA["ru"] = dict(
    title="JPG против PNG против WebP: какой формат использовать? | norito",
    meta_desc="Сравнение JPG, PNG и WebP простым языком: когда каждый из них правильный выбор, и почему WebP сегодня обычно побеждает для фотографий.",
    headline="JPG против PNG против WebP: какой формат изображения использовать?",
    breadcrumb_label="JPG против PNG против WebP: какой формат изображения использовать?",
    lede="Три формата, три разных компромисса. Вот что на самом деле их различает, и быстрый способ решить, какой из них подходит для вашего изображения.",
    t=dict(
        h2_1="Короткий ответ",
        p1="Используйте <strong>PNG</strong> для скриншотов, логотипов и всего, что требует прозрачного фона. Используйте <strong>JPEG</strong> для фотографий, где малый размер файла важнее идеального качества, и вам нужна максимальная совместимость. Используйте <strong>WebP</strong> для фотографий, когда хотите наилучший баланс качества и размера файла и вам не нужно поддерживать очень старое программное обеспечение.",
        h2_2="PNG: без потерь, и единственный с настоящей поддержкой прозрачности",
        p2="PNG никогда не отбрасывает данные изображения — каждый пиксель, который вы сохранили, это именно тот пиксель, который вы получите обратно. Это делает его правильным выбором для всего с резкими краями или плоскими цветами: скриншотов, макетов интерфейса, логотипов, диаграмм, поскольку сжатие с потерями склонно создавать заметную размытость вокруг жёстких краёв и текста. PNG также поддерживает полноценный альфа-канал прозрачности, так что это формат, к которому стоит обращаться всякий раз, когда часть изображения должна быть прозрачной. Компромисс: для фотографического контента файлы PNG обычно в 3–10 раз крупнее эквивалентного JPEG или WebP, потому что фотографии полны тех тонких градиентов и шума, которые сжатие без потерь не может значительно уменьшить.",
        h2_3="JPEG: универсальный формат фото",
        p3="JPEG существует с 1992 года и поддерживается практически любым программным обеспечением, браузером и устройством, созданным с тех пор. Он использует сжатие с потерями, настроенное для фотографического контента, отбрасывая детали так, что это трудно заметить при обычных размерах просмотра. У него вообще нет поддержки прозрачности, и он склонен показывать заметные блочные артефакты вокруг чёткого текста или графических краёв, поэтому он плохо подходит для скриншотов. Для обычных фотографий, где важна широкая совместимость (вложения в письма, старые системы, типографии, принимающие только JPEG), это по-прежнему совершенно разумный вариант по умолчанию.",
        h2_4="WebP: сегодня обычно лучший формат для фото",
        p4="Разработанный Google и теперь поддерживаемый в каждом крупном браузере, WebP обычно даёт файлы на 25–35% меньше, чем JPEG при том же визуальном качестве, и поддерживает как прозрачность, так и сжатие без потерь, если они вам нужны. Для стандартной фотографии, предназначенной для веб-сайта, публикации в соцсети или общего хранения, WebP обычно является лучшим доступным компромиссом между качеством и размером. Главная причина избегать его — совместимость: некоторое старое ПО, определённые рабочие процессы печати или специфические формы загрузки могут по-прежнему принимать только JPEG или PNG.",
        h2_5="Простое руководство по принятию решения",
        p5="Нужна прозрачность, или это скриншот, логотип, или графика с резкими краями и текстом? Используйте PNG. Это фото, и назначение явно требует JPEG (старая система, типография, привередливая форма загрузки)? Используйте JPEG. Это фото, и у вас есть свободный выбор формата? Используйте WebP — вы получите заметно меньшие файлы при том же качестве без реальных недостатков практически для любого современного случая использования.",
        try_it="Попробуйте сами:", try_link="Конвертер изображений", try_desc=" — для конвертации между JPG, PNG и WebP прямо в вашем браузере.",
    ),
)

DATA["ja"] = dict(
    title="JPG対PNG対WebP：どの形式を使うべきか？ | norito",
    meta_desc="JPG、PNG、WebPを平易な言葉で比較し、それぞれがいつ正しい選択となるか、そして今日なぜWebPが写真においてたいてい勝るのかを解説。",
    headline="JPG対PNG対WebP：どの画像形式を使うべきか？",
    breadcrumb_label="JPG対PNG対WebP：どの画像形式を使うべきか？",
    lede="3つの形式、3つの異なるトレードオフ。ここでは実際にそれらを分けているものと、自分の画像にどれが合うかを素早く判断する方法を紹介します。",
    t=dict(
        h2_1="端的な答え",
        p1="スクリーンショット、ロゴ、透明な背景が必要なものには<strong>PNG</strong>を使いましょう。完璧な画質よりも小さいファイルサイズが重要で、最大限の互換性が必要な写真には<strong>JPEG</strong>を使いましょう。画質とファイルサイズの最良のバランスを求めていて、非常に古いソフトウェアへの対応が不要な写真には<strong>WebP</strong>を使いましょう。",
        h2_2="PNG：可逆で、本物の透明度サポートを持つ唯一の形式",
        p2="PNGは画像データを一切捨てません。保存したピクセルは、取り出すときもまったく同じピクセルのままです。これにより、スクリーンショット、UIモックアップ、ロゴ、図表など、はっきりした輪郭やベタ塗りの色を持つものにとって正しい選択となります。非可逆圧縮は硬い輪郭やテキストの周りに目に見えるぼやけを生じさせがちだからです。PNGは完全なアルファ透明チャンネルもサポートしているため、画像の一部を透過させる必要がある場合に頼るべき形式です。トレードオフとしては、写真系のコンテンツに対しては、PNGファイルは同等のJPEGやWebPよりも通常3〜10倍大きくなります。写真には可逆圧縮ではあまり縮められない、微妙なグラデーションやノイズが満載だからです。",
        h2_3="JPEG：万能の写真形式",
        p3="JPEGは1992年から存在しており、それ以降に作られたほぼすべてのソフトウェア、ブラウザ、デバイスでサポートされています。写真系コンテンツ向けに調整された非可逆圧縮を使用し、通常の閲覧サイズでは気づきにくい形でディテールを捨てます。透明度のサポートはまったくなく、くっきりしたテキストや図形の輪郭の周りに目に見えるブロック状のアーティファクトが現れがちで、これがスクリーンショットに向かない理由です。幅広い互換性が重要な通常の写真（メールの添付ファイル、古いシステム、JPEGしか受け付けない印刷ラボなど）については、今なお完全に妥当なデフォルトです。",
        h2_4="WebP：今日ではたいてい最良の写真形式",
        p4="Googleによって開発され、現在ではすべての主要ブラウザでサポートされているWebPは、同じ視覚的品質でJPEGより通常25〜35%小さいファイルを生成し、必要であれば透明度と可逆圧縮の両方にも対応しています。ウェブサイト、SNS投稿、または一般的な保存を目的とする標準的な写真であれば、WebPは通常、画質とサイズの間で得られる最良のトレードオフです。避けるべき主な理由は互換性です。一部の古いソフトウェア、特定の印刷ワークフロー、あるいは特定のアップロードフォームは、依然としてJPEGかPNGしか受け付けない場合があります。",
        h2_5="シンプルな判断ガイド",
        p5="透明度が必要か、あるいはくっきりした輪郭とテキストを持つスクリーンショット、ロゴ、図形か？PNGを使いましょう。写真であり、送信先が明示的にJPEGを要求しているか（古いシステム、印刷ラボ、うるさいアップロードフォームなど）？JPEGを使いましょう。写真であり、形式を自由に選べるか？WebPを使いましょう。ほぼどんな現代的な用途でも、実質的な欠点なしに、同じ画質で目に見えて小さいファイルが得られます。",
        try_it="自分で試してみる：", try_link="画像コンバーター", try_desc="で、ブラウザ内で直接JPG、PNG、WebPを相互変換できます。",
    ),
)

for loc, d in DATA.items():
    body_html = body(d["t"])
    html = render_article(
        loc, SLUG,
        title=d["title"], meta_desc=d["meta_desc"], headline=d["headline"],
        breadcrumb_label=d["breadcrumb_label"], byline_date_human=DATE_HUMAN[loc],
        date_iso=DATE_ISO, lede=d["lede"], body_html=body_html,
    )
    outdir = f"src/{loc}/blog"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/{SLUG}"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
