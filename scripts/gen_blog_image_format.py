#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from blog_lib import render_article

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

SLUG = "image-format-guide-2026.html"
DATE_ISO = "2026-07-20"
DATE_HUMAN = {
    "es": "20 de julio de 2026", "zh": "2026年7月20日", "ar": "20 يوليو 2026",
    "hi": "20 जुलाई, 2026", "ru": "20 июля 2026 г.", "ja": "2026年7月20日",
}
ICON = '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'

def body(t):
    return f'''    <h2>{t['h2_1']}</h2>
    <p>{t['p1']}</p>

    <h2>{t['h2_2']}</h2>
    <p>{t['p2']}</p>

    <h2>{t['h2_3']}</h2>
    <p>{t['p3']}</p>
    <p>{t['p4']}</p>
    <p>{t['p5']}</p>

    <h2>{t['h2_4']}</h2>
    <p>{t['p6']}</p>

    <h2>{t['h2_5']}</h2>
    <p>{t['p7']}</p>

    <h2>{t['h2_6']}</h2>
    <p>{t['p8']}</p>
    <p>{t['p9']}</p>

    <h2>{t['h2_7']}</h2>
    <p>{t['p10']}</p>
    <p>{t['p11']}</p>
    <p>{t['p12']}</p>

    <div class="result-box ok" style="margin-top:32px;">
      {ICON}
      <div class="r-body"><strong>{t['try_it']}</strong> <a href="../image-converter.html">{t['try_link']}</a> {t['try_desc']}</div>
    </div>
'''

DATA = {}

DATA["es"] = dict(
    title="AVIF, WebP, JPEG, PNG: Qué Formato Usar Cuándo, en 2026 | norito",
    meta_desc="Una guía práctica de AVIF, WebP, JPEG, y PNG en 2026: números de compresión, realidades de compatibilidad, transparencia, animación, y cuándo JPEG sigue ganando.",
    headline="AVIF, WebP, JPEG, PNG: Qué Formato Usar Cuándo, en 2026",
    breadcrumb_label="AVIF, WebP, JPEG, PNG: Qué Formato Usar Cuándo, en 2026",
    lede="Cuatro formatos cubren esencialmente toda imagen en la web en 2026, y la buena noticia es que rara vez necesitas pensar en más de dos de ellos para cualquier tarea dada. Aquí hay una guía práctica de decisión con números reales, más los casos donde el JPEG de 30 años sigue siendo la respuesta correcta.",
    t=dict(
        h2_1="Los contendientes, una línea cada uno",
        p1="JPEG (1992): con pérdida, hecho para fotografías, aceptado universalmente. PNG (1996): sin pérdida, transparencia, bordes nítidos, aceptado universalmente. WebP (2010): modos con y sin pérdida, transparencia, animación, aproximadamente una generación mejor que JPEG en compresión. AVIF (2019, construido sobre el códec de video AV1): el campeón de compresión actual, con soporte de transparencia, animación, y HDR, a costa de una codificación lenta y un soporte más irregular fuera de los navegadores.",
        h2_2="¿Qué pasa con HEIC y JPEG XL?",
        p2="Dos formatos con los que te encontrarás pero que en general no deberías publicar. HEIC es lo que los iPhone capturan por defecto: excelente compresión, pero efectivamente un formato del ecosistema Apple, con soporte poco fiable en navegadores y en Windows, así que conviértelo a JPEG antes de compartir. JPEG XL es técnicamente excelente, posiblemente el mejor todoterreno sobre el papel, pero su historia de adopción es un lío: Chrome eliminó su soporte experimental en 2022 mientras Safari lo añadió después, y el estancamiento lo ha mantenido fuera de la lista segura. Trata a ambos como formatos de captura o archivo, no de entrega, hasta que eso se resuelva.",
        h2_3="Compresión, con números",
        p3="Para una fotografía típica con calidad visual equivalente, WebP queda alrededor de un 25 a 30 por ciento más pequeño que JPEG, y AVIF alrededor de un 40 a 50 por ciento más pequeño que JPEG, con su mayor ventaja en niveles de compresión agresivos. Concretamente: un JPEG de 1.2 MB guardado a calidad 80 suele salir alrededor de 850 KB como WebP y 600 a 700 KB como AVIF a calidad comparable. Para trabajo sin pérdida, el PNG optimizado es la base, y el WebP sin pérdida típicamente lo supera por un 20 a 25 por ciento.",
        p4="Los números de AVIF vienen con dos advertencias. La codificación es lenta, segundos por imagen en lugar de milisegundos, lo cual importa para pipelines de build y conversiones masivas. Y a ajustes de calidad muy bajos AVIF falla de forma diferente a JPEG: en lugar de artefactos en bloques, suaviza textura fina como el grano de la piel y el follaje. Eso se ve más limpio a primera vista pero puede leerse plástico al inspeccionar de cerca.",
        p5='Una trampa al comparar: los deslizadores de calidad no son comparables entre formatos. La calidad 80 de JPEG, la calidad 80 de WebP, y la calidad 80 de AVIF describen tres escalas internas diferentes, así que las comparaciones de "mismo ajuste de calidad" no tienen sentido. Compara por tamaño de salida a una calidad visual que encuentres aceptable, lo que en la práctica significa comprimir a un tamaño objetivo e inspeccionar el resultado lado a lado.',
        h2_4="El soporte de navegadores está resuelto; todo lo demás no",
        p6="A partir de 2026 la cuestión de navegadores es fácil: todo navegador moderno renderiza los cuatro formatos. WebP ha sido seguro en todas partes desde 2020, y AVIF desde que Safari 16 se lanzó en 2022. Los problemas de compatibilidad reales ahora viven fuera del navegador: clientes de correo que no renderizarán WebP o AVIF, visores de fotos integrados más antiguos, formularios de subida que solo aceptan .jpg y .png, imprentas, y pipelines de CMS o redes sociales que recodifican o rechazan formatos desconocidos. Eso lleva a la regla más útil de esta guía: en páginas web que controlas, usa formatos modernos libremente; para archivos que entregas al sistema de otra persona, JPEG y PNG siguen siendo la lengua franca.",
        h2_5="Transparencia y animación",
        p7="JPEG no tiene transparencia, punto; PNG, WebP, y AVIF soportan todos canales alfa. El caso interesante son las imágenes fotográficas con transparencia, como fotos de producto recortadas de su fondo: como PNG estas son enormes, porque PNG comprime mal el detalle fotográfico, y convertir una a WebP con alfa habitualmente recorta un 80 a 90 por ciento del tamaño. Para animación, el WebP y AVIF animados son mucho más pequeños que GIF, que está atascado con 256 colores y compresión de la era 1987. Para cualquier cosa más larga que un par de segundos, sin embargo, un archivo de video en bucle sin sonido supera a cualquier formato de imagen.",
        h2_6="Cuándo JPEG y PNG siguen siendo correctos",
        p8="JPEG sigue siendo correcto cuando la compatibilidad supera a los bytes: adjuntos de correo, archivos destinados a formularios y portales, cualquier cosa camino a impresión, y plataformas que recodifican las subidas de todas formas (la mayoría de redes sociales), donde tu AVIF cuidadosamente ajustado se convierte a su JPEG al llegar. También codifica esencialmente al instante y soporta renderizado progresivo, así que una conexión lenta muestra una imagen utilizable pronto.",
        p9='PNG sigue siendo correcto para capturas de pantalla, maquetas de UI, diagramas, y logos, en cualquier lugar donde dominen los bordes duros y el color plano, porque los códecs con pérdida producen halos visibles alrededor de bordes nítidos. El error clásico va en el otro sentido: guardar fotografías como PNG, lo que produce archivos de 5 a 10 veces más grandes sin beneficio visible. Cubrimos esa trampa, y lo básico de los tres formatos más antiguos, en <a href="jpg-vs-png-vs-webp.html">JPG vs PNG vs WebP</a>.',
        h2_7="La decisión en cinco líneas",
        p10="Foto en un sitio que controlas: AVIF, con un respaldo WebP o JPEG vía el elemento picture. Foto que va a correo, un formulario de subida, o impresión: JPEG. Captura de pantalla, diagrama, o logo: PNG, o WebP sin pérdida donde controles el destino. Foto que necesita transparencia: WebP o AVIF. Animación corta: WebP o AVIF animados, o mejor aún un pequeño video en bucle.",
        p11='Y antes de la elección de formato: revisa la resolución. Una foto de 4000 píxeles de ancho mostrada en una columna de 800 píxeles desperdicia más bytes de los que cualquier códec puede recuperar, así que <a href="../resize-image.html">redimensiona al tamaño de visualización</a> primero, luego elige el formato.',
        p12='Para las conversiones en sí, el <a href="../image-converter.html">conversor de imágenes</a> de norito cambia entre JPG, PNG, y WebP directamente en tu navegador, y el <a href="../compress-image.html">compresor de imágenes</a> comprimirá cualquiera de ellos a un tamaño de archivo objetivo. Si estás decidiendo cuánto puedes comprimir antes de que la calidad se vea visiblemente afectada, <a href="image-compression-without-losing-quality.html">esta guía</a> cubre los ajustes que importan.',
        try_it="Pruébalo tú mismo:", try_link="Conversor de Imágenes", try_desc="convierte entre JPG, PNG, y WebP localmente en tu navegador. No se sube nada.",
    ),
)

DATA["zh"] = dict(
    title="AVIF、WebP、JPEG、PNG：2026 年该在何时选用哪种格式 | norito",
    meta_desc="2026 年 AVIF、WebP、JPEG 和 PNG 的实用指南：压缩数据、兼容性现实、透明度、动画，以及 JPEG 仍能胜出的场景。",
    headline="AVIF、WebP、JPEG、PNG：2026 年，该在何时选用哪种格式",
    breadcrumb_label="AVIF、WebP、JPEG、PNG：2026 年，该在何时选用哪种格式",
    lede="到了 2026 年，四种格式基本上涵盖了网络上的所有图片，而好消息是，对于任何一项具体任务，你几乎不需要在两种以上的格式中纠结。这里是一份带有真实数据的实用决策指南，外加那些沿用了 30 年的 JPEG 仍然是正确答案的场景。",
    t=dict(
        h2_1="候选者，一句话概括",
        p1="JPEG（1992 年）：有损压缩，为照片而生，被普遍接受。PNG（1996 年）：无损压缩，支持透明，边缘清晰，被普遍接受。WebP（2010 年）：兼具有损和无损模式，支持透明和动画，压缩效果大致比 JPEG 领先一代。AVIF（2019 年，基于 AV1 视频编解码器构建）：当前的压缩冠军，支持透明、动画和 HDR，代价是编码速度慢，浏览器之外的支持也比较参差不齐。",
        h2_2="那 HEIC 和 JPEG XL 呢？",
        p2="有两种格式你会遇到，但大多数情况下不应该用它们来发布内容。HEIC 是 iPhone 默认拍摄的格式：压缩效果出色，但实际上是苹果生态系统专属的格式，在浏览器和 Windows 上的支持并不可靠，所以分享前请先转换成 JPEG。JPEG XL 在技术上非常出色，纸面上可以说是最全能的选手，但它的普及之路相当混乱：Chrome 在 2022 年移除了对它的实验性支持，而 Safari 后来又加入了支持，这种僵持局面让它一直无法进入「安全使用」的名单。在这一局面尘埃落定之前，最好把这两种格式当作拍摄或存档格式，而不是用于最终发布的格式。",
        h2_3="压缩效果，附上具体数字",
        p3="对于视觉质量相当的典型照片而言，WebP 通常比 JPEG 小 25% 到 30%，而 AVIF 通常比 JPEG 小 40% 到 50%，且在高压缩强度下优势最为明显。具体来说：一张以质量 80 保存的 1.2 MB JPEG，转换成 WebP 后通常约为 850 KB，而在相近质量下转换成 AVIF 则约为 600 到 700 KB。对于无损处理，经过优化的 PNG 是基准线，无损 WebP 通常能比它再小 20% 到 25%。",
        p4="AVIF 的这些数据有两个附带条件。首先，编码速度较慢，每张图片需要几秒钟而不是几毫秒，这一点对构建流水线和批量转换来说很重要。其次，在非常低的质量设置下，AVIF 的失真方式和 JPEG 不同：它不是产生块状伪影，而是把皮肤纹理、树叶等精细纹理抹平。乍一看会显得更「干净」，但仔细观察时可能会显得有塑料感。",
        p5="比较时有一个陷阱：质量滑块在不同格式之间并不可比。JPEG 质量 80、WebP 质量 80、AVIF 质量 80 描述的其实是三种不同的内部刻度，所以「相同质量设置」的比较毫无意义。正确的做法是在你认为可接受的视觉质量水平下比较输出文件大小，实际操作起来就是压缩到目标大小后并排检查结果。",
        h2_4="浏览器支持已经不是问题；其他方面则未必",
        p6="到 2026 年，浏览器兼容性这个问题已经很简单了：每一款主流常青浏览器都能渲染这四种格式。WebP 自 2020 年起在各处都很安全，AVIF 则自 2022 年 Safari 16 发布起也是如此。真正的兼容性问题现在都出现在浏览器之外：无法渲染 WebP 或 AVIF 的邮件客户端、较旧的内置图片查看器、只接受 .jpg 和 .png 的上传表单、印刷厂，以及会重新编码或拒绝陌生格式的 CMS 或社交平台流水线。这就引出了本指南中最实用的一条规则：在你自己能控制的网页上，可以放心使用现代格式；而对于要交给别人系统处理的文件，JPEG 和 PNG 仍然是通用语言。",
        h2_5="透明度与动画",
        p7="JPEG 完全不支持透明，这一点毫无争议；PNG、WebP 和 AVIF 都支持 alpha 通道。有意思的情况是带透明背景的照片类图像，比如从背景中抠出的产品图：如果保存为 PNG，这类文件会非常庞大，因为 PNG 对照片级细节的压缩效果很差，而把它转换成带 alpha 通道的 WebP 通常能把体积削减 80% 到 90%。至于动画，动态 WebP 和 AVIF 都比 GIF 小得多，因为 GIF 受限于 256 色和 1987 年那个时代的压缩技术。不过对于超过几秒钟的内容，一个静音的循环视频文件会胜过任何图片格式。",
        h2_6="什么时候 JPEG 和 PNG 依然是正确选择",
        p8="当兼容性比字节数更重要时，JPEG 依然是正确的选择：邮件附件、要提交到表单和门户网站的文件、任何要送去印刷的内容，以及那些反正会重新编码上传内容的平台（大多数社交网络），在这种情况下，你精心调校的 AVIF 到达后还是会被转换成他们自己的 JPEG。JPEG 编码几乎是瞬时完成的，并且支持渐进式渲染，因此在网速较慢时也能较早地显示出一张可用的图片。",
        p9='PNG 在截图、UI 原型图、图表和 Logo 等场景下依然是正确的选择，也就是那些以硬边缘和纯色为主的场合，因为有损编解码器会在锐利的边缘周围产生明显的振铃伪影。经典的反向错误是：把照片保存成 PNG，这会导致文件体积大出 5 到 10 倍，却没有任何肉眼可见的好处。我们在<a href="jpg-vs-png-vs-webp.html">《JPG 对比 PNG 对比 WebP》</a>一文中详细讲过这个坑，以及这三种较老格式的基础知识。',
        h2_7="五句话讲清楚该怎么选",
        p10="放在你自己能控制的网站上的照片：用 AVIF，并通过 picture 元素提供 WebP 或 JPEG 作为后备方案。要发送到邮件、上传表单或用于印刷的照片：用 JPEG。截图、图表或 Logo：用 PNG，或者在你能控制目标环境时使用无损 WebP。需要透明背景的照片：用 WebP 或 AVIF。短动画：用动态 WebP 或 AVIF，或者更好的做法是用一个体积小的循环视频。",
        p11='而在选择格式之前，先检查一下分辨率。一张 4000 像素宽的照片如果显示在一个只有 800 像素宽的栏目里，浪费掉的字节数是任何编解码器都无法帮你挽回的，所以应该先<a href="../resize-image.html">调整到实际显示尺寸</a>，再来挑选格式。',
        p12='至于转换本身，norito 的<a href="../image-converter.html">图片格式转换工具</a>可以直接在你的浏览器中在 JPG、PNG 和 WebP 之间切换，而<a href="../compress-image.html">图片压缩工具</a>则能把这几种格式的任意一种压缩到目标文件大小。如果你正在纠结在画质明显受损之前究竟能压缩到什么程度，<a href="image-compression-without-losing-quality.html">这篇指南</a>介绍了真正重要的那些设置。',
        try_it="亲自试试：", try_link="图片格式转换工具", try_desc="在你的浏览器本地完成 JPG、PNG 和 WebP 之间的转换。不上传任何内容。",
    ),
)

DATA["ar"] = dict(
    title="AVIF وWebP وJPEG وPNG: أي صيغة تستخدم ومتى، في 2026 | norito",
    meta_desc="دليل عملي لصيغ AVIF وWebP وJPEG وPNG في 2026: أرقام الضغط، حقائق التوافق، الشفافية، الرسوم المتحركة، ومتى يظل JPEG هو الفائز.",
    headline="AVIF وWebP وJPEG وPNG: أي صيغة تستخدم ومتى، في 2026",
    breadcrumb_label="AVIF وWebP وJPEG وPNG: أي صيغة تستخدم ومتى، في 2026",
    lede="تغطي أربع صيغ تقريبًا كل صورة على الويب في 2026، والخبر الجيد أنك نادرًا ما تحتاج للتفكير في أكثر من اثنتين منها لأي مهمة معينة. إليك دليل قرار عملي بأرقام حقيقية، بالإضافة إلى الحالات التي يظل فيها JPEG البالغ من العمر 30 عامًا الإجابة الصحيحة.",
    t=dict(
        h2_1="المتنافسون، سطر واحد لكل منهم",
        p1="JPEG (1992): مفقِد للبيانات، صُمم للصور الفوتوغرافية، مقبول عالميًا. PNG (1996): بلا فقدان، شفافية، حواف حادة، مقبول عالميًا. WebP (2010): أوضاع فقدان وبلا فقدان، شفافية، رسوم متحركة، أفضل تقريبًا بجيل كامل من JPEG في الضغط. AVIF (2019، مبني على مُرمِّز فيديو AV1): بطل الضغط الحالي، مع دعم الشفافية والرسوم المتحركة وHDR، على حساب ترميز بطيء ودعم أكثر تفاوتًا خارج المتصفحات.",
        h2_2="ماذا عن HEIC وJPEG XL؟",
        p2="صيغتان ستصادفهما لكن يجب ألا تنشر بهما في الغالب. HEIC هو ما تلتقطه أجهزة آيفون افتراضيًا: ضغط ممتاز، لكنه فعليًا صيغة خاصة بنظام أبل البيئي، بدعم غير موثوق في المتصفحات وعلى ويندوز، لذا حوّله إلى JPEG قبل المشاركة. JPEG XL ممتاز تقنيًا، وربما الأفضل شمولاً على الورق، لكن قصة تبنّيه فوضوية: أزال Chrome دعمه التجريبي في 2022 بينما أضافه Safari لاحقًا، وأبقى هذا الجمود عليه خارج قائمة الآمن. تعامل مع كليهما كصيغتي التقاط أو أرشفة، لا صيغتي تسليم، حتى يستقر الوضع.",
        h2_3="الضغط، بالأرقام",
        p3="بالنسبة لصورة فوتوغرافية نموذجية بجودة بصرية معادلة، يصبح WebP أصغر بنحو 25 إلى 30 بالمئة من JPEG، وAVIF أصغر بنحو 40 إلى 50 بالمئة من JPEG، مع أكبر ميزة له عند مستويات الضغط العدوانية. بشكل ملموس: ملف JPEG بحجم 1.2 ميغابايت محفوظ بجودة 80 يميل للخروج بحجم نحو 850 كيلوبايت كـ WebP و600 إلى 700 كيلوبايت كـ AVIF بجودة مماثلة. للعمل بلا فقدان، PNG المُحسَّن هو خط الأساس، وWebP بلا فقدان يتفوق عليه عادةً بنسبة 20 إلى 25 بالمئة.",
        p4="تأتي أرقام AVIF مع تحذيرين. الترميز بطيء، ثوانٍ لكل صورة بدلاً من أجزاء من الثانية، وهذا يهم في خطوط بناء المشاريع والتحويلات الجماعية. وعند إعدادات الجودة المنخفضة جدًا يفشل AVIF بشكل مختلف عن JPEG: بدلاً من التشوهات الكتلية، يُنعِّم الملمس الدقيق مثل حبيبات البشرة وأوراق الشجر. يبدو ذلك أنظف للوهلة الأولى لكن قد يبدو بلاستيكيًا عند الفحص الدقيق.",
        p5='فخ عند المقارنة: أشرطة الجودة غير قابلة للمقارنة عبر الصيغ. جودة 80 في JPEG، وجودة 80 في WebP، وجودة 80 في AVIF تصف ثلاثة مقاييس داخلية مختلفة، لذا فإن مقارنات "نفس إعداد الجودة" لا معنى لها. قارن بحجم الإخراج عند جودة بصرية تجدها مقبولة، وهو ما يعني عمليًا الضغط إلى حجم مستهدف وفحص النتيجة جنبًا إلى جنب.',
        h2_4="دعم المتصفحات محلول؛ كل شيء آخر ليس كذلك",
        p6="اعتبارًا من 2026، سؤال المتصفحات سهل: كل متصفح حديث يعرض الصيغ الأربع جميعها. WebP آمن في كل مكان منذ 2020، وAVIF منذ إطلاق Safari 16 في 2022. مشاكل التوافق الحقيقية تعيش الآن خارج المتصفح: عملاء البريد الإلكتروني التي لن تعرض WebP أو AVIF، عارضات الصور المدمجة الأقدم، نماذج الرفع التي تقبل فقط .jpg و.png، محلات الطباعة، وخطوط أنظمة إدارة المحتوى أو الشبكات الاجتماعية التي تعيد الترميز أو ترفض الصيغ غير المألوفة. يؤدي ذلك إلى القاعدة الأكثر فائدة في هذا الدليل: على صفحات الويب التي تتحكم بها، استخدم الصيغ الحديثة بحرية؛ للملفات التي تسلّمها لنظام شخص آخر، يظل JPEG وPNG اللغة المشتركة.",
        h2_5="الشفافية والرسوم المتحركة",
        p7="لا يملك JPEG شفافية، نقطة انتهى؛ يدعم PNG وWebP وAVIF جميعًا قنوات ألفا. الحالة المثيرة للاهتمام هي الصور الفوتوغرافية ذات الشفافية، مثل صور المنتجات المقصوصة من خلفيتها: كـ PNG تكون هذه ضخمة، لأن PNG يضغط التفاصيل الفوتوغرافية بشكل سيء، وتحويل واحدة إلى WebP بألفا يقطع بشكل روتيني 80 إلى 90 بالمئة من الحجم. بالنسبة للرسوم المتحركة، WebP وAVIF المتحركان أصغر بكثير من GIF، العالق بـ 256 لونًا وضغط من عصر 1987. لكن بالنسبة لأي شيء أطول من ثانيتين أو ثلاث، يتفوق ملف فيديو متكرر بلا صوت على كل صيغة صورة.",
        h2_6="متى يظل JPEG وPNG صحيحين",
        p8="يظل JPEG صحيحًا عندما يتفوق التوافق على البايتات: مرفقات البريد الإلكتروني، الملفات المتجهة إلى النماذج والبوابات، أي شيء متجه للطباعة، والمنصات التي تعيد ترميز الرفوعات على أي حال (معظم الشبكات الاجتماعية)، حيث يُحوَّل ملف AVIF الذي ضبطته بعناية إلى JPEG الخاص بهم عند الوصول. كما أنه يُرمَّز فوريًا تقريبًا ويدعم العرض التدريجي، لذا يُظهر اتصال بطيء صورة قابلة للاستخدام مبكرًا.",
        p9='يظل PNG صحيحًا للقطات الشاشة، ونماذج واجهات المستخدم، والمخططات، والشعارات، في أي مكان تهيمن فيه الحواف الصلبة والألوان المسطحة، لأن المرمّزات المفقِدة للبيانات تُنتج تموجات مرئية حول الحواف الحادة. الخطأ الكلاسيكي يسير في الاتجاه الآخر: حفظ الصور الفوتوغرافية كـ PNG، ما يُنتج ملفات أكبر بـ 5 إلى 10 مرات دون فائدة مرئية. تناولنا ذلك الفخ، وأساسيات الصيغ الثلاث الأقدم جميعًا، في <a href="jpg-vs-png-vs-webp.html">JPG مقابل PNG مقابل WebP</a>.',
        h2_7="القرار في خمسة أسطر",
        p10="صورة على موقع تتحكم به: AVIF، مع بديل WebP أو JPEG عبر عنصر picture. صورة متجهة إلى بريد إلكتروني، أو نموذج رفع، أو طباعة: JPEG. لقطة شاشة، أو مخطط، أو شعار: PNG، أو WebP بلا فقدان حيث تتحكم بالوجهة. صورة تحتاج شفافية: WebP أو AVIF. رسوم متحركة قصيرة: WebP أو AVIF متحركان، أو الأفضل فيديو صغير متكرر.",
        p11='وقبل اختيار الصيغة على الإطلاق: تحقق من الدقة. صورة بعرض 4000 بكسل معروضة في عمود بعرض 800 بكسل تُهدر بايتات أكثر مما يمكن لأي مُرمِّز استعادته، لذا <a href="../resize-image.html">غيّر الحجم إلى حجم العرض</a> أولاً، ثم اختر الصيغة.',
        p12='بالنسبة للتحويلات نفسها، يُبدِّل <a href="../image-converter.html">محوّل الصور</a> الخاص بـ norito بين JPG وPNG وWebP مباشرةً في متصفحك، وسيضغط <a href="../compress-image.html">ضاغط الصور</a> أيًا منها إلى حجم ملف مستهدف. إذا كنت تقرر مدى قوة الضغط التي يمكنك تحملها قبل أن تتأثر الجودة بشكل مرئي، يغطي <a href="image-compression-without-losing-quality.html">هذا الدليل</a> الإعدادات المهمة.',
        try_it="جرّبه بنفسك:", try_link="محوّل الصور", try_desc="يحوّل بين JPG وPNG وWebP محليًا في متصفحك. لا شيء يُرفَع.",
    ),
)

DATA["hi"] = dict(
    title="AVIF, WebP, JPEG, PNG: 2026 में कब कौन-सा फ़ॉर्मैट इस्तेमाल करें | norito",
    meta_desc="2026 में AVIF, WebP, JPEG, और PNG की एक व्यावहारिक गाइड: कंप्रेशन नंबर, कम्पैटिबिलिटी की हक़ीक़त, ट्रांसपेरेंसी, एनिमेशन, और JPEG कब अब भी जीतता है।",
    headline="AVIF, WebP, JPEG, PNG: 2026 में कब कौन-सा फ़ॉर्मैट इस्तेमाल करें",
    breadcrumb_label="AVIF, WebP, JPEG, PNG: 2026 में कब कौन-सा फ़ॉर्मैट इस्तेमाल करें",
    lede="2026 में चार फ़ॉर्मैट वेब पर लगभग हर इमेज को कवर करते हैं, और अच्छी ख़बर यह है कि किसी भी काम के लिए आपको शायद ही कभी इनमें से दो से ज़्यादा के बारे में सोचना पड़े। यहां है असली नंबरों के साथ एक व्यावहारिक निर्णय गाइड, साथ ही वे मामले जहां 30 साल पुराना JPEG अब भी सही जवाब है।",
    t=dict(
        h2_1="दावेदार, हर एक के लिए एक लाइन",
        p1="JPEG (1992): लॉसी, फ़ोटोग्राफ़ के लिए बनाया गया, यूनिवर्सली स्वीकार किया गया। PNG (1996): लॉसलेस, ट्रांसपेरेंसी, शार्प एज, यूनिवर्सली स्वीकार किया गया। WebP (2010): लॉसी और लॉसलेस मोड, ट्रांसपेरेंसी, एनिमेशन, कंप्रेशन में JPEG से लगभग एक जनरेशन बेहतर। AVIF (2019, AV1 वीडियो कोडेक पर बना): मौजूदा कंप्रेशन चैंपियन, ट्रांसपेरेंसी, एनिमेशन, और HDR सपोर्ट के साथ, धीमी एनकोडिंग और ब्राउज़र के बाहर कम भरोसेमंद सपोर्ट की क़ीमत पर।",
        h2_2="HEIC और JPEG XL का क्या?",
        p2="दो फ़ॉर्मैट जिनसे आप टकराएंगे लेकिन ज़्यादातर पब्लिश नहीं करने चाहिए। HEIC वह है जो iPhone डिफ़ॉल्ट रूप से शूट करते हैं: शानदार कंप्रेशन, लेकिन असल में एक Apple-इकोसिस्टम फ़ॉर्मैट, ब्राउज़र और Windows पर अविश्वसनीय सपोर्ट के साथ, इसलिए शेयर करने से पहले JPEG में कन्वर्ट करें। JPEG XL तकनीकी रूप से शानदार है, कागज़ पर शायद सबसे बेहतर ऑल-राउंडर, लेकिन इसकी अडॉप्शन कहानी गड़बड़ है: Chrome ने 2022 में अपना एक्सपेरिमेंटल सपोर्ट हटा दिया जबकि Safari ने बाद में इसे जोड़ा, और इस गतिरोध ने इसे सेफ़ लिस्ट से बाहर रखा है। जब तक यह सुलझ नहीं जाता, दोनों को कैप्चर या आर्काइवल फ़ॉर्मैट मानें, डिलीवरी फ़ॉर्मैट नहीं।",
        h2_3="कंप्रेशन, नंबरों के साथ",
        p3="बराबर विज़ुअल क्वालिटी पर एक आम फ़ोटोग्राफ़ के लिए, WebP JPEG से लगभग 25 से 30 प्रतिशत छोटा आता है, और AVIF JPEG से लगभग 40 से 50 प्रतिशत छोटा, जिसका सबसे बड़ा फ़ायदा एग्रेसिव कंप्रेशन लेवल पर होता है। ठोस रूप में: क्वालिटी 80 पर सेव किया गया 1.2 MB का JPEG WebP के रूप में करीब 850 KB और तुलनीय क्वालिटी पर AVIF के रूप में 600 से 700 KB आता है। लॉसलेस काम के लिए, ऑप्टिमाइज़्ड PNG बेसलाइन है, और लॉसलेस WebP आम तौर पर इसे 20 से 25 प्रतिशत से बेहतर करता है।",
        p4="AVIF के नंबर दो चेतावनियों के साथ आते हैं। एनकोडिंग धीमी है, मिलीसेकंड की बजाय प्रति इमेज सेकंड, जो बिल्ड पाइपलाइन और बल्क कन्वर्ज़न के लिए मायने रखता है। और बहुत कम क्वालिटी सेटिंग्स पर AVIF JPEG से अलग तरह से फ़ेल होता है: ब्लॉकी आर्टिफ़ैक्ट की बजाय, यह स्किन ग्रेन और पत्तियों जैसी बारीक बनावट को स्मूद कर देता है। यह पहली नज़र में साफ़-सुथरा लगता है लेकिन क़रीब से देखने पर प्लास्टिकी लग सकता है।",
        p5="तुलना करते वक़्त एक जाल: क्वालिटी स्लाइडर फ़ॉर्मैट के बीच तुलनीय नहीं हैं। JPEG क्वालिटी 80, WebP क्वालिटी 80, और AVIF क्वालिटी 80 तीन अलग-अलग इंटरनल स्केल बताते हैं, इसलिए \"वही क्वालिटी सेटिंग\" वाली तुलनाएं मायने नहीं रखतीं। ऐसी विज़ुअल क्वालिटी पर आउटपुट साइज़ से तुलना करें जो आपको स्वीकार्य लगे, जिसका व्यावहारिक मतलब है एक टारगेट साइज़ तक कंप्रेस करना और नतीजे को साथ-साथ जांचना।",
        h2_4="ब्राउज़र सपोर्ट सुलझ चुका है; बाक़ी सब नहीं",
        p6="2026 तक ब्राउज़र वाला सवाल आसान है: हर एवरग्रीन ब्राउज़र चारों फ़ॉर्मैट रेंडर करता है। WebP 2020 से हर जगह सेफ़ है, और AVIF तब से जब 2022 में Safari 16 शिप हुआ। असली कम्पैटिबिलिटी प्रॉब्लम अब ब्राउज़र के बाहर रहती हैं: ईमेल क्लाइंट जो WebP या AVIF रेंडर नहीं करेंगे, पुराने बिल्ट-इन फ़ोटो व्यूअर, अपलोड फ़ॉर्म जो सिर्फ़ .jpg और .png स्वीकार करते हैं, प्रिंट शॉप, और CMS या सोशल पाइपलाइन जो अनजान फ़ॉर्मैट को री-एनकोड या रिजेक्ट करती हैं। इससे इस गाइड का सबसे उपयोगी नियम निकलता है: वेब पेजों पर जो आप कंट्रोल करते हैं, मॉडर्न फ़ॉर्मैट खुलकर इस्तेमाल करें; उन फ़ाइलों के लिए जो आप किसी और के सिस्टम को सौंपते हैं, JPEG और PNG लिंगुआ फ़्रैंका बने रहते हैं।",
        h2_5="ट्रांसपेरेंसी और एनिमेशन",
        p7="JPEG में कोई ट्रांसपेरेंसी नहीं है, पूरी बात; PNG, WebP, और AVIF सभी अल्फ़ा चैनल सपोर्ट करते हैं। दिलचस्प मामला है ट्रांसपेरेंसी वाली फ़ोटोग्राफ़िक इमेजें, जैसे प्रोडक्ट शॉट्स जो अपने बैकग्राउंड से काटी गई हैं: PNG के रूप में ये बहुत बड़ी होती हैं, क्योंकि PNG फ़ोटोग्राफ़िक डिटेल को खराब तरीक़े से कंप्रेस करता है, और एक को अल्फ़ा के साथ WebP में कन्वर्ट करने से रूटीनली साइज़ का 80 से 90 प्रतिशत कट जाता है। एनिमेशन के लिए, एनिमेटेड WebP और AVIF GIF से कहीं छोटे हैं, जो 256 रंगों और 1987-युग के कंप्रेशन में फंसा है। हालांकि, कुछ सेकंड से लंबी किसी भी चीज़ के लिए, एक म्यूट लूपिंग वीडियो फ़ाइल हर इमेज फ़ॉर्मैट को हरा देती है।",
        h2_6="JPEG और PNG कब अब भी सही हैं",
        p8="JPEG तब सही रहता है जब कम्पैटिबिलिटी बाइट्स से ऊपर हो: ईमेल अटैचमेंट, फ़ॉर्म और पोर्टल के लिए तय फ़ाइलें, प्रिंट की तरफ़ जाने वाली कोई भी चीज़, और प्लेटफ़ॉर्म जो वैसे भी अपलोड्स को री-एनकोड करते हैं (ज़्यादातर सोशल नेटवर्क), जहां आपका सावधानी से ट्यून किया गया AVIF पहुंचने पर उनके JPEG में बदल जाता है। यह लगभग तुरंत एनकोड भी होता है और प्रोग्रेसिव रेंडरिंग सपोर्ट करता है, इसलिए एक धीमा कनेक्शन जल्दी एक इस्तेमाल लायक इमेज दिखाता है।",
        p9='PNG स्क्रीनशॉट, UI मॉकअप, डायग्राम, और लोगो के लिए सही रहता है, हर जगह जहां हार्ड एज और फ़्लैट कलर हावी हों, क्योंकि लॉसी कोडेक्स शार्प एज के आसपास दिखने वाली रिंगिंग पैदा करते हैं। क्लासिक ग़लती दूसरी तरफ़ जाती है: फ़ोटोग्राफ़ को PNG के रूप में सेव करना, जो बिना किसी नज़र आने वाले फ़ायदे के 5 से 10 गुना बड़ी फ़ाइलें बनाता है। हमने उस जाल को, और सभी तीन पुराने फ़ॉर्मैट की बेसिक्स को, <a href="jpg-vs-png-vs-webp.html">JPG बनाम PNG बनाम WebP</a> में कवर किया।',
        h2_7="पांच लाइनों में फ़ैसला",
        p10="किसी ऐसी साइट पर फ़ोटो जिसे आप कंट्रोल करते हैं: AVIF, picture एलिमेंट के ज़रिए WebP या JPEG फ़ॉलबैक के साथ। ईमेल, अपलोड फ़ॉर्म, या प्रिंट पर जाने वाली फ़ोटो: JPEG। स्क्रीनशॉट, डायग्राम, या लोगो: PNG, या जहां आप डेस्टिनेशन कंट्रोल करते हैं वहां लॉसलेस WebP। ट्रांसपेरेंसी चाहने वाली फ़ोटो: WebP या AVIF। छोटा एनिमेशन: एनिमेटेड WebP या AVIF, या इससे भी बेहतर एक छोटा लूपिंग वीडियो।",
        p11='और फ़ॉर्मैट चुनने से पहले भी: रिज़ॉल्यूशन चेक करें। 800-पिक्सेल कॉलम में दिखाई गई 4000-पिक्सेल चौड़ी फ़ोटो किसी भी कोडेक की वापस जीती जा सकने वाली सीमा से ज़्यादा बाइट्स बर्बाद करती है, इसलिए पहले <a href="../resize-image.html">डिस्प्ले साइज़ पर रीसाइज़ करें</a>, फिर फ़ॉर्मैट चुनें।',
        p12='ख़ुद कन्वर्ज़न के लिए, norito का <a href="../image-converter.html">इमेज कन्वर्टर</a> सीधे आपके ब्राउज़र में JPG, PNG, और WebP के बीच स्विच करता है, और <a href="../compress-image.html">इमेज कंप्रेसर</a> इनमें से किसी को भी एक टारगेट फ़ाइल साइज़ तक दबा देगा। अगर आप तय कर रहे हैं कि क्वालिटी के नज़र आने लायक ख़राब होने से पहले आप कितनी कड़ाई से कंप्रेस कर सकते हैं, तो <a href="image-compression-without-losing-quality.html">यह गाइड</a> उन सेटिंग्स को कवर करती है जो मायने रखती हैं।',
        try_it="खुद आज़माएं:", try_link="इमेज कन्वर्टर", try_desc="आपके ब्राउज़र में लोकली JPG, PNG, और WebP के बीच कन्वर्ट करता है। कुछ भी अपलोड नहीं होता।",
    ),
)

DATA["ru"] = dict(
    title="AVIF, WebP, JPEG, PNG: какой формат когда использовать в 2026 году | norito",
    meta_desc="Практическое руководство по AVIF, WebP, JPEG и PNG в 2026 году: цифры сжатия, реалии совместимости, прозрачность, анимация, и когда JPEG всё ещё побеждает.",
    headline="AVIF, WebP, JPEG, PNG: какой формат когда использовать, в 2026 году",
    breadcrumb_label="AVIF, WebP, JPEG, PNG: какой формат когда использовать, в 2026 году",
    lede="Четыре формата покрывают практически все изображения в вебе в 2026 году, и хорошая новость в том, что для любой конкретной задачи вам редко нужно думать больше чем о двух из них. Вот практическое руководство по выбору с реальными цифрами, а также случаи, где 30-летний JPEG всё ещё остаётся правильным ответом.",
    t=dict(
        h2_1="Претенденты, по одной строке на каждого",
        p1="JPEG (1992): с потерями, создан для фотографий, принимается повсеместно. PNG (1996): без потерь, прозрачность, чёткие края, принимается повсеместно. WebP (2010): режимы с потерями и без потерь, прозрачность, анимация, примерно на поколение лучше JPEG по сжатию. AVIF (2019, построен на видеокодеке AV1): нынешний чемпион по сжатию, с поддержкой прозрачности, анимации и HDR, ценой чего являются медленное кодирование и более неравномерная поддержка за пределами браузеров.",
        h2_2="А что насчёт HEIC и JPEG XL?",
        p2="Два формата, с которыми вы столкнётесь, но в которых в основном не стоит публиковать. HEIC — это то, что iPhone снимает по умолчанию: отличное сжатие, но фактически формат, привязанный к экосистеме Apple, с ненадёжной поддержкой в браузерах и на Windows, поэтому конвертируйте в JPEG перед публикацией. JPEG XL технически превосходен, возможно, лучший универсал на бумаге, но история его внедрения запутана: Chrome убрал экспериментальную поддержку в 2022 году, тогда как Safari позже её добавил, и это противостояние удержало его вне безопасного списка. Относитесь к обоим как к форматам съёмки или архивирования, а не доставки, пока ситуация не прояснится.",
        h2_3="Сжатие, с цифрами",
        p3="Для типичной фотографии при эквивалентном визуальном качестве WebP получается примерно на 25–30 процентов меньше JPEG, а AVIF примерно на 40–50 процентов меньше JPEG, с наибольшим преимуществом при агрессивных уровнях сжатия. Конкретно: JPEG на 1.2 МБ, сохранённый с качеством 80, обычно получается около 850 КБ в виде WebP и 600–700 КБ в виде AVIF при сопоставимом качестве. Для работы без потерь оптимизированный PNG служит базовой линией, а WebP без потерь обычно превосходит его на 20–25 процентов.",
        p4="Цифры AVIF сопровождаются двумя оговорками. Кодирование медленное — секунды на изображение вместо миллисекунд, что важно для конвейеров сборки и массовых конвертаций. И при очень низких настройках качества AVIF деградирует иначе, чем JPEG: вместо блочных артефактов он сглаживает тонкую текстуру, такую как текстура кожи и листва. На первый взгляд это выглядит чище, но при close-up рассмотрении может казаться пластиковым.",
        p5="Одна ловушка при сравнении: ползунки качества не сопоставимы между форматами. Качество 80 в JPEG, качество 80 в WebP и качество 80 в AVIF описывают три разные внутренние шкалы, поэтому сравнения «одинаковой настройки качества» бессмысленны. Сравнивайте по размеру выходного файла при визуальном качестве, которое вы считаете приемлемым, что на практике означает сжатие до целевого размера и сравнение результата бок о бок.",
        h2_4="Поддержка браузеров решена; всё остальное — нет",
        p6="По состоянию на 2026 год вопрос браузеров прост: каждый современный браузер отображает все четыре формата. WebP безопасен повсеместно с 2020 года, а AVIF — с тех пор как Safari 16 вышел в 2022 году. Реальные проблемы совместимости теперь живут за пределами браузера: почтовые клиенты, которые не отображают WebP или AVIF, более старые встроенные программы просмотра фото, формы загрузки, принимающие только .jpg и .png, типографии, а также конвейеры CMS или соцсетей, которые перекодируют или отклоняют незнакомые форматы. Это приводит к самому полезному правилу этого руководства: на веб-страницах, которые вы контролируете, свободно используйте современные форматы; для файлов, которые вы передаёте в чужую систему, JPEG и PNG остаются общим языком.",
        h2_5="Прозрачность и анимация",
        p7="У JPEG нет прозрачности, точка; PNG, WebP и AVIF все поддерживают альфа-каналы. Интересный случай — фотографические изображения с прозрачностью, такие как снимки товаров, вырезанные из фона: в формате PNG они огромны, потому что PNG плохо сжимает фотографическую детализацию, а конвертация в WebP с альфа-каналом обычно урезает 80–90 процентов размера. Что касается анимации, анимированные WebP и AVIF намного меньше GIF, который застрял на 256 цветах и сжатии эпохи 1987 года. Однако для всего, что длиннее пары секунд, зацикленный видеофайл без звука превосходит любой формат изображения.",
        h2_6="Когда JPEG и PNG всё ещё правильны",
        p8="JPEG остаётся верным выбором, когда совместимость важнее байтов: вложения в письма, файлы для форм и порталов, всё, что идёт в печать, и платформы, которые в любом случае перекодируют загрузки (большинство соцсетей), где ваш тщательно настроенный AVIF конвертируется в их JPEG по прибытии. Он также кодируется практически мгновенно и поддерживает прогрессивный рендеринг, поэтому при медленном соединении рано появляется пригодное для использования изображение.",
        p9='PNG остаётся верным выбором для скриншотов, макетов интерфейса, диаграмм и логотипов — везде, где преобладают чёткие края и плоский цвет, потому что кодеки с потерями создают заметное окантовывание вокруг резких границ. Классическая ошибка идёт в обратном направлении: сохранение фотографий в PNG, что даёт файлы в 5–10 раз больше без видимой выгоды. Мы рассмотрели эту ловушку, а также основы всех трёх более старых форматов, в статье <a href="jpg-vs-png-vs-webp.html">JPG против PNG против WebP</a>.',
        h2_7="Решение в пяти строках",
        p10="Фото на сайте, который вы контролируете: AVIF с резервным вариантом WebP или JPEG через элемент picture. Фото, отправляемое по почте, в форму загрузки или на печать: JPEG. Скриншот, диаграмма или логотип: PNG, либо WebP без потерь там, где вы контролируете назначение. Фото, которому нужна прозрачность: WebP или AVIF. Короткая анимация: анимированный WebP или AVIF, а ещё лучше — небольшое зацикленное видео.",
        p11='А ещё до выбора формата вообще: проверьте разрешение. Фотография шириной 4000 пикселей, показанная в колонке шириной 800 пикселей, тратит впустую больше байтов, чем может вернуть любой кодек, поэтому сначала <a href="../resize-image.html">измените размер под размер отображения</a>, затем выбирайте формат.',
        p12='Что касается самих конвертаций, <a href="../image-converter.html">конвертер изображений</a> norito переключается между JPG, PNG и WebP прямо в вашем браузере, а <a href="../compress-image.html">компрессор изображений</a> сожмёт любой из них до целевого размера файла. Если вы решаете, насколько сильно можно сжать, прежде чем качество заметно пострадает, <a href="image-compression-without-losing-quality.html">это руководство</a> рассматривает настройки, которые действительно важны.',
        try_it="Попробуйте сами:", try_link="Конвертер изображений", try_desc="конвертирует между JPG, PNG и WebP локально в вашем браузере. Ничего не загружается.",
    ),
)

DATA["ja"] = dict(
    title="AVIF、WebP、JPEG、PNG：2026年、どの場面でどの形式を使うべきか | norito",
    meta_desc="2026年のAVIF、WebP、JPEG、PNGの実践ガイド：圧縮数値、互換性の実情、透明度、アニメーション、そしてJPEGが今なお勝る場面。",
    headline="AVIF、WebP、JPEG、PNG：2026年、どの場面でどの形式を使うべきか",
    breadcrumb_label="AVIF、WebP、JPEG、PNG：2026年、どの場面でどの形式を使うべきか",
    lede="2026年には、4つの形式でウェブ上のほぼすべての画像がカバーされており、良いニュースは、どんな作業であっても、実際に検討すべき形式は2つ程度で済むことがほとんどだという点です。ここでは実際の数値に基づく実践的な判断ガイドと、30年前から使われているJPEGが今なお正解となるケースを紹介します。",
    t=dict(
        h2_1="候補たちを一行ずつ",
        p1="JPEG（1992年）：非可逆、写真向けに作られ、あらゆる場所で受け入れられている。PNG（1996年）：可逆、透明度対応、シャープな輪郭、あらゆる場所で受け入れられている。WebP（2010年）：可逆・非可逆の両モード、透明度、アニメーションに対応し、圧縮性能はJPEGよりおおよそ一世代分優れている。AVIF（2019年、AV1動画コーデックをベースに構築）：現時点での圧縮チャンピオンで、透明度、アニメーション、HDRに対応しているが、そのぶんエンコードが遅く、ブラウザ以外でのサポートにはばらつきがある。",
        h2_2="HEICとJPEG XLはどうなのか",
        p2="遭遇はするものの、基本的に公開用としては使うべきでない2つの形式があります。HEICはiPhoneがデフォルトで撮影する形式です。圧縮効率は優れていますが、実質的にAppleエコシステム専用の形式であり、ブラウザやWindowsでのサポートは不安定なため、共有前にJPEGへ変換すべきです。JPEG XLは技術的には非常に優れており、机上の性能だけを見れば最も万能と言えるかもしれませんが、その普及の経緯は混乱しています。Chromeは2022年に実験的サポートを削除した一方、Safariは後になって対応を追加し、この対立状態のせいで「安全に使える形式」のリストには入れないままになっています。この状況が落ち着くまでは、両方とも配信用ではなく撮影用またはアーカイブ用の形式として扱うのが賢明です。",
        h2_3="具体的な数値で見る圧縮効率",
        p3="同等の視覚的品質で典型的な写真を比較すると、WebPはJPEGよりおよそ25〜30パーセント小さくなり、AVIFはJPEGよりおよそ40〜50パーセント小さくなります。特にAVIFの優位性は、圧縮率を強めに設定した場合に最も顕著です。具体的には、品質80で保存された1.2MBのJPEGは、WebPに変換するとおよそ850KB、同程度の品質のAVIFでは600〜700KB程度になる傾向があります。可逆圧縮の作業では、最適化されたPNGが基準となり、可逆WebPは通常それより20〜25パーセント優れています。",
        p4="AVIFのこうした数値には2つの注意点が伴います。まずエンコードが遅く、1画像あたりミリ秒ではなく秒単位の時間がかかるため、ビルドパイプラインや一括変換において無視できない要素です。さらに、非常に低い品質設定にすると、AVIFはJPEGとは異なる形で劣化します。ブロック状のアーティファクトが出る代わりに、肌の質感や葉のディテールといった細かいテクスチャを平滑化してしまうのです。一見するときれいに見えますが、じっくり見るとプラスチックのような質感に見えることがあります。",
        p5="比較する際の落とし穴が1つあります。品質スライダーは形式をまたいで比較できません。JPEGの品質80、WebPの品質80、AVIFの品質80は、それぞれ内部的にまったく異なる尺度を表しているため、「同じ品質設定」での比較には意味がありません。自分が許容できると感じる視覚的品質のもとで、出力サイズを基準に比較すべきです。実際には、目標サイズまで圧縮してから結果を並べて確認する、という形になります。",
        h2_4="ブラウザ対応は解決済み。それ以外は未解決",
        p6="2026年現在、ブラウザに関する問題はシンプルです。あらゆる主要なモダンブラウザが4つの形式すべてをレンダリングできます。WebPは2020年以降どこでも安全に使え、AVIFは2022年にSafari 16がリリースされて以降、同様に安全です。実際の互換性の問題は、今やブラウザの外側にあります。WebPやAVIFをレンダリングしないメールクライアント、旧式の内蔵フォトビューア、.jpgと.pngしか受け付けないアップロードフォーム、印刷会社、そして見慣れない形式を再エンコードしたり拒否したりするCMSやSNSのパイプラインなどです。これが、このガイドで最も実用的なルールにつながります。自分が管理するウェブページ上では最新の形式を自由に使い、他人のシステムに渡すファイルについては、JPEGとPNGが依然として共通言語であり続けるということです。",
        h2_5="透明度とアニメーション",
        p7="JPEGには透明度がまったくありません。これは議論の余地がありません。PNG、WebP、AVIFはいずれもアルファチャンネルに対応しています。興味深いのは、背景を切り抜いた商品写真のような、透明度を持つ写真系の画像です。これをPNGとして保存すると非常に巨大になります。PNGは写真のディテールをうまく圧縮できないためです。これをアルファ付きのWebPに変換すると、サイズを80〜90パーセントも削減できるのが常です。アニメーションについては、アニメーションWebPとAVIFは、256色と1987年当時の圧縮技術に縛られたGIFよりもはるかに小さくなります。ただし数秒を超える長さになると、音声なしのループ動画ファイルがどの画像形式よりも優れています。",
        h2_6="JPEGとPNGが今も正解であるケース",
        p8="互換性がバイト数よりも優先される場面では、JPEGは依然として正しい選択肢です。メールの添付ファイル、フォームやポータルサイトに送る予定のファイル、印刷に回すもの、そしてどのみちアップロードを再エンコードするプラットフォーム（ほとんどのソーシャルネットワーク）などです。こうした場では、せっかく丁寧に調整したAVIFも、到着時に相手側のJPEGへ変換されてしまいます。JPEGはほぼ瞬時にエンコードでき、プログレッシブレンダリングにも対応しているため、低速な回線でも早い段階で使える画像が表示されます。",
        p9='PNGは、スクリーンショット、UIモックアップ、図表、ロゴなど、はっきりした輪郭とベタ塗りの色が支配的な場面で今も正解です。非可逆コーデックは鋭い輪郭の周りに目に見えるリンギングを生じさせるためです。よくある逆方向の間違いは、写真をPNGとして保存してしまうことです。これは目に見える恩恵がないまま、ファイルサイズを5〜10倍に膨らませてしまいます。この落とし穴と、3つの古い形式それぞれの基礎については、<a href="jpg-vs-png-vs-webp.html">「JPG対PNG対WebP」</a>で取り上げています。',
        h2_7="5行でわかる判断基準",
        p10="自分が管理するサイト上の写真：picture要素を通じてWebPまたはJPEGのフォールバックを備えたAVIF。メール、アップロードフォーム、印刷に向かう写真：JPEG。スクリーンショット、図表、ロゴ：PNG、または配信先を自分で管理できる場合は可逆WebP。透明度が必要な写真：WebPまたはAVIF。短いアニメーション：アニメーションWebPまたはAVIF、あるいはそれ以上に望ましいのは小さなループ動画。",
        p11='そして形式を選ぶよりも前に、解像度を確認してください。幅800ピクセルのカラムに表示される幅4000ピクセルの写真は、どんなコーデックを使っても取り戻せないほど多くのバイトを無駄にします。まずは<a href="../resize-image.html">表示サイズに合わせてリサイズ</a>し、それから形式を選んでください。',
        p12='変換作業そのものについては、noritoの<a href="../image-converter.html">画像コンバーター</a>がブラウザ内で直接JPG、PNG、WebPを相互に変換し、<a href="../compress-image.html">画像圧縮ツール</a>はそのいずれも目標のファイルサイズまで圧縮します。画質が目に見えて劣化する前にどこまで圧縮できるか迷っている場合は、<a href="image-compression-without-losing-quality.html">このガイド</a>で重要な設定を解説しています。',
        try_it="自分で試してみる：", try_link="画像コンバーター", try_desc="ブラウザ内でローカルにJPG、PNG、WebPを相互変換します。アップロードは一切ありません。",
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
