#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88M14.47 14.48 20 20M8.12 8.12 12 12"/></svg>'
ICON_CLASS = "c-coral"

def body(t):
    return f'''
    <div class="result-box" style="margin-bottom:28px;">
      <span class="r-body">
        <strong>{t['heads_up']}:</strong> {t['heads_up_body']}
      </span>
    </div>

    <div class="two-col">
      <div class="panel">
        <div class="dropzone" id="drop">
          <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
          <p>{t['dz_click']}</p>
          <p class="note" style="margin-top:2px;">{t['dz_hint']}</p>
          <input type="file" id="fileInput" accept="image/*" multiple />
        </div>
        <p class="note" id="originalInfo" style="display:none;"></p>

        <div class="field-row" style="margin-top:20px;">
          <div class="field">
            <label for="bgMode">{t['bg_mode']}</label>
            <select id="bgMode">
              <option value="transparent" selected>{t['transparent']}</option>
              <option value="color">{t['solid_color']}</option>
            </select>
          </div>
          <div class="field" id="bgColorField" style="display:none;">
            <label for="bgColor">{t['color']}</label>
            <input type="color" id="bgColor" value="#ffffff" />
          </div>
        </div>

        <button id="processBtn" disabled>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88M14.47 14.48 20 20M8.12 8.12 12 12"/></svg>
          {t['remove_bg']}
        </button>
        <div class="result-box" id="result" style="display:none;"></div>

        <div class="batch-file-list" id="batchList" style="display:none;"></div>
        <div class="batch-actions" id="batchActions" style="display:none;">
          <button type="button" id="batchProcessBtn">{t['batch_process']}</button>
          <button type="button" class="secondary" id="batchZipBtn" disabled>{t['batch_zip']}</button>
        </div>
      </div>

      <div>
        <div class="panel" style="text-align:center;">
          <img class="preview" id="preview" style="display:none; max-width:100%;" alt="{t['result_alt']}" />
          <p class="note" id="previewHint" style="margin-top:0;">{t['preview_hint']}</p>
        </div>
        <button id="downloadBtn" class="secondary" disabled style="width:100%;">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
  {t['download_png']}
</button>
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
    title="Quitar Fondo de Imagen Gratis, Sin Registro | norito",
    meta_desc="Quita el fondo de una foto gratis, sin registro, sin marca de agua, sin límite de subidas. Funciona por completo en tu navegador, exporta como PNG transparente.",
    app_name="Quitar Fondo de Imagen Gratis", h1="Quitar Fondo de Imagen, Gratis", breadcrumb_label="Quitar Fondo de Imagen Gratis",
    lede="Recorta a una persona de una foto gratis, sin registro, sin marca de agua, sin límite de cuántas fotos proceses. Todo funciona en tu navegador, la imagen nunca sale de tu dispositivo.",
    t=dict(
        heads_up="Ten en cuenta", heads_up_body="esto usa MODNet, un modelo de recorte de retrato ajustado para personas, no para objetos o productos en general. Los retratos y selfies funcionan mejor. El modelo y el runtime de WebAssembly que necesita pesan unos 18 MB en total y se descargan una vez por sesión de navegador, luego quedan en caché.",
        dz_click="<strong>Haz clic para elegir una foto</strong>, arrástrala aquí o pégala con Ctrl+V",
        dz_hint="Funciona mejor con una sola persona, claramente encuadrada. Selecciona varias fotos para procesar por lotes.",
        bg_mode="Fondo del resultado", transparent="Transparente", solid_color="Color sólido", color="Color",
        remove_bg="Quitar fondo", batch_process="Quitar fondo a todas", batch_zip="Descargar todo como .zip",
        result_alt="Resultado sin fondo", preview_hint="Tu recorte aparecerá aquí una vez procesado.", download_png="Descargar PNG",
        faq_h2="Preguntas frecuentes",
        faq1_q="¿Es realmente gratis, sin necesidad de registrarse?",
        faq1_a="Sí. No hay cuenta, ni marca de agua, ni límite en cuántas fotos proceses. La herramienta funciona por completo en tu navegador usando un modelo de segmentación gratuito y de código abierto, no hay coste de servidor por imagen que tengamos que recuperar.",
        faq2_q="¿Funciona con fotos de productos, no solo de personas?",
        faq2_a="Está ajustado específicamente para personas, los retratos y selfies funcionan mejor. Los resultados en objetos o productos serán menos fiables ya que el modelo subyacente no fue entrenado para eso.",
        faq3_q="¿Se sube mi foto a un servidor?",
        faq3_a="No. El procesamiento ocurre por completo en tu dispositivo tras descargar un pequeño modelo una vez por sesión de navegador. Tu foto nunca se envía a ningún sitio.",
        how_h2="Cómo funciona",
        how_p1='El trabajo pesado lo hace MODNet, una red de recorte de retrato de código abierto, ejecutada a través de ONNX Runtime Web (la compilación WebAssembly de Microsoft del motor de inferencia ONNX) dentro de tu navegador. La primera vez que pulsas el botón, la página descarga el modelo y el runtime (unos 18 MB en total, cacheados para la sesión), luego ejecuta la inferencia sobre tu foto localmente. A diferencia de un modelo de segmentación simple, MODNet predice una máscara alfa real, un valor de opacidad por píxel, en lugar de una decisión tosca de "persona o fondo", así que el pelo y los bordes suaves salen más cerca de la transparencia real.',
        how_p2='Incluso una máscara alfa real tiene algo de ruido en sus bordes, así que la herramienta hace igualmente una pasada de limpieza ligera: un pequeño desenfoque de caja suaviza los artefactos de redimensionado, luego la curva alfa recibe un remapeo suave tipo smoothstep para que la neblina cercana a cero se vuelva totalmente transparente y los píxeles seguros del sujeto se vuelvan totalmente opacos, mientras la transición suave entre medias (pelo, desenfoque, movimiento) se conserva en lugar de aplanarse. El resultado limpio se aplica píxel a píxel mediante <code>getImageData</code> del canvas, y se exporta como PNG (para conservar la transparencia) o compuesto sobre un color sólido que elijas.',
        how_p3="Esto también explica por qué los resultados difieren de los servicios de pago en la nube: esos ejecutan modelos cientos de veces más grandes en GPUs, así que ganan en pelo y fondos complejos. Aquí la contrapartida es la opuesta, y es deliberada: tu foto nunca sale de tu máquina. Eso es verificable, no una promesa: abre la pestaña Red de las DevTools y procesa una imagen. Verás cómo se descargan los archivos del modelo y el runtime, y ninguna solicitud lleva tu foto, nunca.",
    ),
    related_tools=[
        ("compress-image.html", "Comprimir imagen", "Consigue un tamaño de archivo exacto sin adivinar la calidad."),
        ("placeholder-generator.html", "Generador de marcadores", "Imágenes de marcador instantáneas, de cualquier tamaño y color."),
        ("qr-code-generator.html", "Generador de códigos QR", "Códigos QR personalizados con colores y logo central."),
    ],
)

PAGES["zh"] = dict(
    title="免费去除图片背景，无需注册 | norito",
    meta_desc="免费去除照片背景，无需注册，无水印，无上传数量限制。完全在浏览器中运行，导出为透明 PNG。",
    app_name="免费去除图片背景", h1="免费去除图片背景", breadcrumb_label="免费去除图片背景",
    lede="免费从照片中抠出人像，无需注册、无水印，处理数量不限。全部在你的浏览器中完成，图片不会离开你的设备。",
    t=dict(
        heads_up="小提示", heads_up_body="本工具使用 MODNet，一个专为人物优化的人像抠图模型，而非通用物体或商品。人像和自拍效果最佳。模型及其所需的 WebAssembly 运行环境共约 18 MB，每个浏览器会话下载一次，之后会被缓存。",
        dz_click="<strong>点击选择照片</strong>，拖放到此处，或使用 Ctrl+V 粘贴",
        dz_hint="最适合画面中只有一个人、人物清晰可见的照片。可选择多张照片批量处理。",
        bg_mode="结果背景", transparent="透明", solid_color="纯色", color="颜色",
        remove_bg="去除背景", batch_process="全部去除背景", batch_zip="全部下载为 .zip",
        result_alt="去除背景后的结果", preview_hint="处理完成后，抠图结果将显示在这里。", download_png="下载 PNG",
        faq_h2="常见问题",
        faq1_q="真的免费、无需注册吗？",
        faq1_a="是的。没有账号，没有水印，也不限制处理数量。该工具完全在你的浏览器中运行，使用免费的开源分割模型，我们不需要为每张图片承担服务器成本。",
        faq2_q="它能处理商品照片，还是只能处理人物？",
        faq2_a="它专门针对人物进行了调优，人像和自拍效果最佳。由于底层模型并未针对物体或商品进行训练，处理这类照片的效果会不太可靠。",
        faq3_q="我的照片会被上传到服务器吗？",
        faq3_a="不会。处理完全在你的设备上进行，只需在每个浏览器会话中下载一次小型模型。你的照片绝不会被发送到任何地方。",
        how_h2="工作原理",
        how_p1="核心处理由 MODNet 完成，这是一个开源人像抠图网络，通过 ONNX Runtime Web（微软基于 WebAssembly 构建的 ONNX 推理引擎）在你的浏览器内运行。你第一次点击按钮时，页面会下载模型和运行时（共约 18 MB，缓存于本次会话），然后在本地对你的照片执行推理。与普通的分割模型不同，MODNet 会为每个像素预测真实的 alpha 遮罩（透明度值），而不是简单粗暴地判断「人物还是背景」，因此头发和柔和边缘会更接近真实的透明效果。",
        how_p2="即便是真实的 alpha 遮罩，边缘处仍会有一些噪点，因此工具还会进行一次轻量清理：先用一个小型方框模糊平滑缩放产生的瑕疵，再对 alpha 曲线做一次柔和的平滑重映射，使接近零的雾状边缘变为完全透明，而可信的主体像素变为完全不透明，同时保留两者之间的柔和过渡（头发、模糊、运动）。清理后的结果通过 canvas 的 <code>getImageData</code> 逐像素应用，并导出为 PNG（以保留透明度）或与你选择的纯色合成。",
        how_p3="这也是为什么结果会和付费云服务不同：那些服务在 GPU 上运行大几百倍的模型，因此在处理头发和复杂背景时更有优势。这里的取舍正好相反，而且是刻意为之：你的照片永远不会离开你的设备。这是可以验证的，而不只是一句承诺——打开开发者工具的 Network 面板并处理一张图片，你会看到模型和运行时文件在下载，而没有任何请求携带你的照片。",
    ),
    related_tools=[
        ("compress-image.html", "压缩图片", "无需猜测质量，精确控制文件大小。"),
        ("placeholder-generator.html", "占位图生成器", "任意尺寸和颜色的即时占位图。"),
        ("qr-code-generator.html", "二维码生成器", "自定义颜色和中心 Logo 的二维码。"),
    ],
)

PAGES["ar"] = dict(
    title="إزالة خلفية الصورة مجانًا، دون تسجيل | norito",
    meta_desc="أزل خلفية صورة مجانًا، دون تسجيل، دون علامة مائية، دون حد أقصى للرفع. يعمل بالكامل في متصفحك، صدّر كـ PNG شفاف.",
    app_name="إزالة خلفية الصورة مجانًا", h1="إزالة خلفية الصورة، مجانًا", breadcrumb_label="إزالة خلفية الصورة مجانًا",
    lede="قصّ شخصًا من صورة مجانًا، دون تسجيل، دون علامة مائية، ودون حد لعدد الصور. كل شيء يعمل في متصفحك، ولا تغادر الصورة جهازك أبدًا.",
    t=dict(
        heads_up="تنبيه", heads_up_body="تستخدم هذه الأداة MODNet، وهو نموذج لفصل الصور الشخصية مخصص للأشخاص، وليس للأجسام أو المنتجات العامة. الصور الشخصية والسيلفي تعطي أفضل النتائج. يبلغ حجم النموذج مع محرّك WebAssembly الذي يحتاجه نحو 18 ميغابايت إجمالاً، ويُحمَّلان مرة واحدة فقط في كل جلسة متصفح، ثم يبقيان محفوظين مؤقتًا.",
        dz_click="<strong>انقر لاختيار صورة</strong>، أو اسحبها وأفلتها هنا، أو الصقها باستخدام Ctrl+V",
        dz_hint="تعطي أفضل النتائج مع شخص واحد واضح داخل الإطار. اختر عدة صور للمعالجة الدفعية.",
        bg_mode="خلفية النتيجة", transparent="شفافة", solid_color="لون موحّد", color="اللون",
        remove_bg="إزالة الخلفية", batch_process="إزالة الخلفية من الكل", batch_zip="تنزيل الكل كملف .zip",
        result_alt="نتيجة إزالة الخلفية", preview_hint="ستظهر الصورة المقصوصة هنا بعد معالجتها.", download_png="تحميل PNG",
        faq_h2="أسئلة شائعة",
        faq1_q="هل هذا مجاني حقًا، دون الحاجة للتسجيل؟",
        faq1_a="نعم. لا يوجد حساب، ولا علامة مائية، ولا حد لعدد الصور التي تعالجها. تعمل الأداة بالكامل في متصفحك باستخدام نموذج تجزئة مجاني ومفتوح المصدر، فلا توجد تكلفة خادم لكل صورة نحتاج لتغطيتها.",
        faq2_q="هل تعمل على صور المنتجات، وليس فقط الأشخاص؟",
        faq2_a="مُعدّة خصيصًا للأشخاص، وتعطي الصور الشخصية والسيلفي أفضل النتائج. ستكون النتائج على الأجسام أو المنتجات أقل موثوقية لأن النموذج الأساسي لم يُدرَّب على ذلك.",
        faq3_q="هل تُرفَع صورتي إلى خادم؟",
        faq3_a="لا. تتم المعالجة بالكامل على جهازك بعد تنزيل نموذج صغير مرة واحدة لكل جلسة متصفح. لا تُرسَل صورتك إلى أي مكان أبدًا.",
        how_h2="كيف تعمل",
        how_p1='العمل الأساسي تقوم به شبكة MODNet مفتوحة المصدر المتخصصة في فصل الصور الشخصية، وتعمل عبر ONNX Runtime Web (نسخة مايكروسوفت من محرك الاستدلال ONNX المبنية على WebAssembly) داخل متصفحك. عند أول ضغطة على الزر، يُنزِّل الموقع النموذج ومحرك التشغيل (نحو 18 ميغابايت إجمالاً، محفوظان مؤقتًا لهذه الجلسة)، ثم يُجري الاستدلال على صورتك محليًا. وخلافًا لنموذج التجزئة البسيط، تتوقع MODNet قيمة شفافية حقيقية لكل بكسل، بدلًا من قرار حاد بين "شخص" أو "خلفية"، فيخرج الشعر والحواف الناعمة أقرب إلى شفافية واقعية.',
        how_p2="حتى القيمة الحقيقية للشفافية تحتوي على بعض الضوضاء عند الحواف، لذا تُجري الأداة أيضًا تنظيفًا خفيفًا: تمويه بسيط يُنعّم عيوب تغيير الحجم، ثم إعادة تخطيط سلسة لمنحنى الشفافية بحيث تصبح الضبابية القريبة من الصفر شفافة تمامًا وبكسلات الموضوع الواثقة معتمة تمامًا، مع الحفاظ على الانتقال الناعم بينهما (كالشعر والحركة) بدلًا من تسطيحه. تُطبَّق النتيجة المنظّفة بكسلًا بكسل عبر <code>getImageData</code> الخاص بالـ canvas، وتُصدَّر كـ PNG (للحفاظ على الشفافية) أو مركّبة فوق لون موحّد تختاره.",
        how_p3="هذا يفسّر أيضًا سبب اختلاف النتائج عن الخدمات السحابية المدفوعة: تلك تُشغّل نماذج أكبر بمئات المرات على وحدات معالجة رسومية، فتتفوق في الشعر والخلفيات المزدحمة. المفاضلة هنا معاكسة، وهي مقصودة: صورتك لا تغادر جهازك أبدًا. هذا أمر يمكن التحقق منه، وليس مجرد وعد: افتح تبويب Network في أدوات المطوّر وعالج صورة. سترى تحميل ملفات النموذج ومحرك التشغيل، ولا يحمل أي طلب صورتك أبدًا.",
    ),
    related_tools=[
        ("compress-image.html", "ضغط الصور", "احصل على حجم ملف دقيق دون الحاجة لتخمين الجودة."),
        ("placeholder-generator.html", "مولّد صور بديلة", "صور بديلة فورية بأي مقاس ولون تريده."),
        ("qr-code-generator.html", "مولّد رمز QR", "رموز QR مخصصة بألوان وشعار في المنتصف."),
    ],
)

PAGES["hi"] = dict(
    title="इमेज बैकग्राउंड मुफ़्त हटाएं, बिना साइन-अप | norito",
    meta_desc="किसी फ़ोटो का बैकग्राउंड मुफ़्त में हटाएं, बिना साइन-अप, बिना वॉटरमार्क, बिना अपलोड लिमिट. पूरी तरह आपके ब्राउज़र में चलता है, ट्रांसपेरेंट PNG के रूप में एक्सपोर्ट करें.",
    app_name="इमेज बैकग्राउंड मुफ़्त हटाएं", h1="इमेज बैकग्राउंड हटाएं, मुफ़्त में", breadcrumb_label="इमेज बैकग्राउंड मुफ़्त हटाएं",
    lede="फ़ोटो में से किसी व्यक्ति को मुफ़्त में अलग करें, बिना साइन-अप, बिना वॉटरमार्क, और कितनी भी फ़ोटो प्रोसेस करने की कोई लिमिट नहीं. सब कुछ आपके ब्राउज़र में चलता है, इमेज कभी आपकी डिवाइस से बाहर नहीं जाती.",
    t=dict(
        heads_up="ध्यान दें", heads_up_body="यह MODNet इस्तेमाल करता है, जो लोगों के लिए ट्यून किया गया एक पोर्ट्रेट-मैटिंग मॉडल है, सामान्य ऑब्जेक्ट या प्रोडक्ट के लिए नहीं. पोर्ट्रेट और सेल्फ़ी सबसे बेहतर काम करती हैं. मॉडल और इसके लिए ज़रूरी WebAssembly रनटाइम, दोनों मिलाकर करीब 18 MB के हैं और हर ब्राउज़र सेशन में एक बार डाउनलोड होते हैं, फिर कैश हो जाते हैं.",
        dz_click="<strong>फ़ोटो चुनने के लिए क्लिक करें</strong>, यहां खींचकर लाएं या Ctrl+V से पेस्ट करें",
        dz_hint="एक अकेले, साफ़ तौर पर फ़्रेम में आए व्यक्ति के साथ सबसे बेहतर काम करता है. बैच प्रोसेसिंग के लिए कई फ़ोटो चुनें.",
        bg_mode="रिज़ल्ट का बैकग्राउंड", transparent="ट्रांसपेरेंट", solid_color="सॉलिड रंग", color="रंग",
        remove_bg="बैकग्राउंड हटाएं", batch_process="सभी से बैकग्राउंड हटाएं", batch_zip="सभी को .zip के रूप में डाउनलोड करें",
        result_alt="बिना बैकग्राउंड का रिज़ल्ट", preview_hint="प्रोसेस होने के बाद आपका कटआउट यहां दिखेगा.", download_png="PNG डाउनलोड करें",
        faq_h2="सामान्य सवाल",
        faq1_q="क्या यह वाक़ई मुफ़्त है, बिना साइन-अप के?",
        faq1_a="हां. कोई अकाउंट नहीं, कोई वॉटरमार्क नहीं, और आप कितनी भी फ़ोटो प्रोसेस करें कोई लिमिट नहीं. यह टूल पूरी तरह आपके ब्राउज़र में एक मुफ़्त, ओपन-सोर्स सेगमेंटेशन मॉडल का इस्तेमाल करके चलता है, हमें हर इमेज के लिए कोई सर्वर लागत वसूल नहीं करनी पड़ती.",
        faq2_q="क्या यह प्रोडक्ट फ़ोटो पर भी काम करता है, सिर्फ़ लोगों पर नहीं?",
        faq2_a="यह खास तौर पर लोगों के लिए ट्यून किया गया है, पोर्ट्रेट और सेल्फ़ी सबसे बेहतर काम करती हैं. ऑब्जेक्ट या प्रोडक्ट पर नतीजे कम भरोसेमंद होंगे क्योंकि अंदर का मॉडल इसके लिए ट्रेन नहीं किया गया था.",
        faq3_q="क्या मेरी फ़ोटो किसी सर्वर पर अपलोड होती है?",
        faq3_a="नहीं. हर ब्राउज़र सेशन में एक छोटा मॉडल डाउनलोड होने के बाद, प्रोसेसिंग पूरी तरह आपकी डिवाइस पर होती है. आपकी फ़ोटो कभी कहीं नहीं भेजी जाती.",
        how_h2="यह कैसे काम करता है",
        how_p1='मुख्य काम MODNet करता है, एक ओपन-सोर्स पोर्ट्रेट-मैटिंग नेटवर्क, जो ONNX Runtime Web (ONNX इंफरेंस इंजन का माइक्रोसॉफ्ट का WebAssembly संस्करण) के ज़रिए आपके ब्राउज़र के अंदर चलता है. पहली बार बटन दबाने पर, पेज मॉडल और रनटाइम डाउनलोड करता है (करीब 18 MB मिलाकर, सेशन के लिए कैश्ड), फिर आपकी फ़ोटो पर लोकली इंफरेंस चलाता है. एक सामान्य सेगमेंटेशन मॉडल के विपरीत, जो सिर्फ "व्यक्ति या बैकग्राउंड" का कड़ा अंदाज़ा लगाता है, MODNet हर पिक्सेल के लिए वास्तविक अल्फा मैट, यानी असली ओपैसिटी वैल्यू, पूर्वानुमान करने के लिए प्रशिक्षित है, इसलिए बाल और मुलायम किनारे असली पारदर्शिता के ज़्यादा करीब आते हैं.',
        how_p2="असली अल्फा मैट में भी किनारों पर कुछ नॉइज़ रहता है, इसलिए यह टूल एक हल्की सफाई भी करता है: एक छोटा बॉक्स ब्लर रीसाइज़िंग की खामियों को स्मूद करता है, फिर अल्फा कर्व को धीरे से रीमैप किया जाता है ताकि शून्य के करीब की धुंध पूरी तरह पारदर्शी हो जाए और भरोसेमंद विषय वाले पिक्सेल पूरी तरह अपारदर्शी, जबकि बीच का मुलायम ट्रांज़िशन (बाल, ब्लर, मूवमेंट) चपटा किए बिना बना रहे. साफ़ किया गया नतीजा canvas के <code>getImageData</code> के ज़रिए पिक्सेल-दर-पिक्सेल लागू होता है, और PNG के रूप में एक्सपोर्ट होता है (ट्रांसपेरेंसी बनाए रखने के लिए) या आपके चुने रंग के ऊपर कंपोज़िट होता है.",
        how_p3="यही वजह है कि नतीजे पेड क्लाउड सर्विसेज़ से अलग होते हैं: वे GPU पर सैकड़ों गुना बड़े मॉडल चलाती हैं, इसलिए बाल और बिज़ी बैकग्राउंड में बेहतर होती हैं. यहां ट्रेडऑफ़ उल्टा है, और यह जान-बूझकर है: आपकी फ़ोटो कभी आपकी मशीन से बाहर नहीं जाती. यह जांचा जा सकता है, सिर्फ़ वादा नहीं: DevTools का Network टैब खोलें और एक इमेज प्रोसेस करें. आप मॉडल और रनटाइम फाइलें डाउनलोड होते देखेंगे, और कोई भी रिक्वेस्ट आपकी फ़ोटो नहीं ले जाती, कभी नहीं.",
    ),
    related_tools=[
        ("compress-image.html", "इमेज कंप्रेस करें", "बिना क्वालिटी का अंदाज़ा लगाए बिल्कुल सही फ़ाइल साइज़ पाएं."),
        ("placeholder-generator.html", "प्लेसहोल्डर जनरेटर", "किसी भी साइज़ और रंग की तुरंत बनी प्लेसहोल्डर इमेज."),
        ("qr-code-generator.html", "QR कोड जनरेटर", "कस्टम रंग और सेंटर लोगो वाले QR कोड."),
    ],
)

PAGES["ru"] = dict(
    title="Удалить фон изображения бесплатно, без регистрации | norito",
    meta_desc="Удалите фон с фото бесплатно, без регистрации, без водяного знака, без лимита загрузок. Работает полностью в браузере, экспорт в прозрачный PNG.",
    app_name="Удалить фон изображения бесплатно", h1="Удаление фона изображения, бесплатно", breadcrumb_label="Удалить фон изображения бесплатно",
    lede="Вырежьте человека с фотографии бесплатно, без регистрации, без водяного знака, без ограничения по количеству фото. Всё работает в вашем браузере, изображение никогда не покидает ваше устройство.",
    t=dict(
        heads_up="Обратите внимание", heads_up_body="здесь используется MODNet — модель портретного маттинга, настроенная на людей, а не на объекты или товары в целом. Портреты и селфи работают лучше всего. Модель вместе с необходимой средой выполнения WebAssembly весит около 18 МБ в сумме и загружается один раз за сессию браузера, затем кешируется.",
        dz_click="<strong>Нажмите, чтобы выбрать фото</strong>, перетащите его сюда или вставьте через Ctrl+V",
        dz_hint="Лучше всего работает с одним чётко видимым человеком в кадре. Выберите несколько фото для пакетной обработки.",
        bg_mode="Фон результата", transparent="Прозрачный", solid_color="Сплошной цвет", color="Цвет",
        remove_bg="Удалить фон", batch_process="Удалить фон у всех", batch_zip="Скачать всё как .zip",
        result_alt="Результат без фона", preview_hint="Ваш вырезанный результат появится здесь после обработки.", download_png="Скачать PNG",
        faq_h2="Частые вопросы",
        faq1_q="Это действительно бесплатно, без регистрации?",
        faq1_a="Да. Нет аккаунта, нет водяного знака, и нет ограничения на количество обрабатываемых фото. Инструмент работает полностью в вашем браузере, используя бесплатную модель сегментации с открытым кодом — нам не нужно окупать серверные расходы за каждое изображение.",
        faq2_q="Он работает с фото товаров, а не только людей?",
        faq2_a="Он настроен специально на людей, портреты и селфи работают лучше всего. Результаты на объектах или товарах будут менее надёжными, так как базовая модель не обучалась для этого.",
        faq3_q="Моя фотография загружается на сервер?",
        faq3_a="Нет. Обработка происходит полностью на вашем устройстве после загрузки небольшой модели один раз за сессию браузера. Ваше фото никуда не отправляется.",
        how_h2="Как это работает",
        how_p1="Основную работу выполняет MODNet — open-source нейросеть для портретного матирования, работающая через ONNX Runtime Web (сборку движка вывода ONNX на WebAssembly от Microsoft) прямо в вашем браузере. При первом нажатии кнопки страница загружает модель и рантайм (около 18 МБ в сумме, кешируются на сессию), затем выполняет вывод по вашему фото локально. В отличие от обычной модели сегментации, которая просто грубо решает «человек или фон», MODNet обучена предсказывать настоящую альфа-маску — значение прозрачности для каждого пикселя, — поэтому волосы и мягкие края получаются ближе к настоящей прозрачности.",
        how_p2="Даже настоящая альфа-маска содержит немного шума на краях, поэтому инструмент выполняет лёгкую очистку: небольшое размытие сглаживает артефакты масштабирования, а затем кривая альфа-канала плавно переназначается так, чтобы дымка около нуля становилась полностью прозрачной, а уверенные пиксели объекта — полностью непрозрачными, сохраняя при этом мягкий переход между ними (волосы, размытие, движение) вместо того, чтобы его сглаживать. Очищенный результат применяется попиксельно через <code>getImageData</code> canvas и экспортируется как PNG (чтобы сохранить прозрачность) или накладывается на выбранный вами сплошной цвет.",
        how_p3="Это также объясняет, почему результаты отличаются от платных облачных сервисов: те запускают модели в сотни раз крупнее на GPU, поэтому выигрывают на волосах и сложных фонах. Здесь компромисс обратный, и он сделан намеренно: ваше фото никогда не покидает ваш компьютер. Это можно проверить, а не просто поверить на слово: откройте вкладку Network в DevTools и обработайте изображение. Вы увидите загрузку файлов модели и рантайма, и ни один запрос никогда не будет содержать ваше фото.",
    ),
    related_tools=[
        ("compress-image.html", "Сжатие изображения", "Точный размер файла без угадывания качества."),
        ("placeholder-generator.html", "Генератор заполнителей", "Мгновенные изображения-заполнители любого размера и цвета."),
        ("qr-code-generator.html", "Генератор QR-кодов", "QR-коды с настраиваемыми цветами и логотипом в центре."),
    ],
)

PAGES["ja"] = dict(
    title="無料で画像の背景を削除、登録不要 | norito",
    meta_desc="写真の背景を無料で削除。登録不要、透かしなし、アップロード制限なし。すべてブラウザ内で動作し、透過PNGとして書き出せます。",
    app_name="無料で画像の背景を削除", h1="画像の背景を無料で削除", breadcrumb_label="無料で画像の背景を削除",
    lede="写真から人物を無料で切り抜きます。登録不要、透かしなし、処理できる枚数に制限もありません。すべてブラウザ内で完結し、画像が端末から出ることはありません。",
    t=dict(
        heads_up="ご注意ください", heads_up_body="これは人物向けに調整されたポートレートマッティングモデル「MODNet」を使用しており、物体や商品全般には対応していません。ポートレートや自撮り写真で最もよく機能します。モデルと必要なWebAssemblyランタイムは合計約18MBで、ブラウザセッションごとに一度ダウンロードされ、その後はキャッシュされます。",
        dz_click="<strong>クリックして写真を選択</strong>、ここにドラッグするか Ctrl+V で貼り付けてください",
        dz_hint="1人がはっきりと写っている写真で最もよく機能します。複数の写真を選択すると一括処理できます。",
        bg_mode="結果の背景", transparent="透明", solid_color="単色", color="色",
        remove_bg="背景を削除", batch_process="すべての背景を削除", batch_zip="すべてを.zipでダウンロード",
        result_alt="背景を削除した結果", preview_hint="処理が完了すると、切り抜き結果がここに表示されます。", download_png="PNGをダウンロード",
        faq_h2="よくある質問",
        faq1_q="本当に無料で、登録も不要ですか？",
        faq1_a="はい。アカウントは不要で、透かしもなく、処理できる枚数にも制限はありません。このツールは無料のオープンソースのセグメンテーションモデルを使ってブラウザ内で完全に動作するため、画像ごとにサーバーコストを回収する必要がありません。",
        faq2_q="人物だけでなく、商品写真にも使えますか？",
        faq2_a="人物向けに特化して調整されているため、ポートレートや自撮り写真で最もよく機能します。基盤となるモデルは物体や商品向けに学習されていないため、それらの写真では結果の信頼性が下がります。",
        faq3_q="写真はサーバーにアップロードされますか？",
        faq3_a="いいえ。ブラウザセッションごとに一度小さなモデルをダウンロードした後、処理はすべて端末上で行われます。あなたの写真がどこかに送信されることはありません。",
        how_h2="仕組み",
        how_p1="中心的な処理はMODNetが担っています。これはオープンソースのポートレートマッティングネットワークで、ONNX Runtime Web（MicrosoftによるONNX推論エンジンのWebAssembly版）を通じてブラウザ内で実行されます。ボタンを初めてクリックすると、ページはモデルとランタイム（合計約18MB、セッション中はキャッシュされます）をダウンロードし、その後写真に対してローカルで推論を実行します。単純なセグメンテーションモデルとは異なり、MODNetは「人物か背景か」という大まかな判定ではなく、ピクセルごとに実際のアルファマット（不透明度の値）を予測するよう学習されているため、髪や柔らかい輪郭がより自然な透明感に近づきます。",
        how_p2="実際のアルファマットでも輪郭部分には多少のノイズが残るため、このツールは軽いクリーンアップも行います。小さなボックスブラーでリサイズによるアーティファクトを滑らかにし、続いてアルファカーブを緩やかにスムーズステップで再マッピングすることで、ゼロに近いかすみは完全に透明に、確信度の高い被写体のピクセルは完全に不透明になり、その間の柔らかい移行（髪、ぼけ、動き）は平坦化されずに保たれます。クリーンアップされた結果はcanvasの<code>getImageData</code>を通じてピクセルごとに適用され、透明度を保つためにPNGとして書き出されるか、選択した単色と合成されます。",
        how_p3="これは、有料のクラウドサービスと結果が異なる理由でもあります。それらはGPU上で桁違いに大きなモデルを実行するため、髪や複雑な背景の処理で優れています。ここでのトレードオフはその逆で、意図的なものです。あなたの写真は端末から一切出ません。これは約束ではなく検証可能です。DevToolsのNetworkタブを開いて画像を処理してみてください。モデルとランタイムファイルがダウンロードされる様子は見えますが、写真を運ぶリクエストは一つもありません。",
    ),
    related_tools=[
        ("compress-image.html", "画像を圧縮", "画質を推測することなく、目標のファイルサイズに正確に合わせる。"),
        ("placeholder-generator.html", "プレースホルダー画像を生成", "任意のサイズと色の画像を即座に生成。"),
        ("qr-code-generator.html", "QRコードを生成", "色とセンターロゴをカスタマイズしたQRコード。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "remove-image-background-free.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/vendor/onnxruntime/ort.wasm.min.js", "js/app-removebg.js", "js/prefill.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/remove-image-background-free.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
