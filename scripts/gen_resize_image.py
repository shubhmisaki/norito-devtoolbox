#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>'
ICON_CLASS = "c-indigo"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="dropzone" id="drop">
          <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
          <p><strong>{t['dz_click']}</strong>{t['dz_drag']}</p>
          <p class="note" style="margin-top:2px;">{t['dz_hint']}</p>
          <input type="file" id="fileInput" accept="image/*" multiple />
        </div>
        <p class="note" id="originalInfo" style="display:none;"></p>
        <div class="batch-file-list" id="batchList" style="display:none;"></div>
        <div class="batch-actions" id="batchActions" style="display:none;">
          <button type="button" id="batchResizeBtn">{t['resize_all']}</button>
          <button type="button" class="secondary" id="batchZipBtn" disabled>{t['download_zip']}</button>
        </div>

        <div class="field-row" style="margin-top:20px;">
          <div class="field">
            <label for="mode">{t['resize_by']}</label>
            <select id="mode">
              <option value="exact" selected>{t['exact_dims']}</option>
              <option value="percent">{t['percentage']}</option>
            </select>
          </div>
          <div class="field">
            <label for="format">{t['output_format']}</label>
            <select id="format">
              <option value="keep" selected>{t['keep_original']}</option>
              <option value="jpeg">JPEG</option>
              <option value="png">PNG</option>
              <option value="webp">WebP</option>
            </select>
          </div>
        </div>

        <div class="field-row" id="exactFields">
          <div class="field">
            <label for="width">{t['width_px']}</label>
            <input type="number" id="width" min="1" max="20000" />
          </div>
          <div class="field">
            <label for="height">{t['height_px']}</label>
            <input type="number" id="height" min="1" max="20000" />
          </div>
        </div>
        <div class="field" id="percentFields" style="display:none;">
          <label for="percent">{t['percent_of_original']}</label>
          <input type="number" id="percent" min="1" max="500" value="50" />
        </div>

        <div class="option-row" style="margin-bottom:20px;">
          <div>
            <div class="option-label">{t['lock_ratio']}</div>
            <div class="option-hint">{t['lock_ratio_hint']}</div>
          </div>
          <label class="switch"><input type="checkbox" id="lockRatio" checked /><span class="track"></span></label>
        </div>

        <button id="resizeBtn" disabled>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
          {t['resize_image']}
        </button>
        <div class="result-box" id="result" style="display:none;"></div>
      </div>

      <div>
        <div class="panel" style="text-align:center;">
          <img class="preview" id="preview" style="display:none; max-width:100%;" alt="{t['resized_preview_alt']}" />
          <p class="note" id="previewHint" style="margin-top:0;">{t['preview_hint']}</p>
        </div>
        <p class="note">
          {t['side_note']}
        </p>
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
    title="Redimensionar Imagen: Cambia Ancho y Alto Online | norito",
    meta_desc="Redimensiona una imagen a dimensiones exactas o a un porcentaje, en tu navegador. Bloquea la proporción para evitar distorsión. No se sube nada.",
    app_name="Redimensionar Imagen", h1="Redimensionar Imagen", breadcrumb_label="Redimensionar Imagen",
    lede="Cambia el ancho y alto de una imagen, por píxeles exactos o por porcentaje. Bloquea la proporción para evitar estiramientos, o desactívala para control total.",
    note_html='¿Redimensionando para Instagram? Prueba el <a href="/resize-image-for-instagram.html">preset de 1080x1080</a>.',
    t=dict(
        dz_click="Haz clic para elegir imágenes", dz_drag=", o arrástralas aquí",
        dz_hint="JPG, PNG, WebP. Selecciona más de una para redimensionar en lote. Se queda en tu dispositivo, no se sube nada.",
        resize_all="Redimensionar todas", download_zip="Descargar todo como .zip",
        resize_by="Redimensionar por", exact_dims="Dimensiones exactas", percentage="Porcentaje",
        output_format="Formato de salida", keep_original="Mantener original",
        width_px="Ancho (px)", height_px="Alto (px)", percent_of_original="Porcentaje del original",
        lock_ratio="Bloquear proporción", lock_ratio_hint="Cambiar el ancho actualiza automáticamente el alto para coincidir, y viceversa.",
        resize_image="Redimensionar imagen",
        resized_preview_alt="Vista previa redimensionada", preview_hint="Tu imagen redimensionada aparecerá aquí una vez generada.",
        side_note="Dimensiones exactas estira o encoge a el ancho y alto que introduzcas (bloquea la proporción para evitar distorsión). Porcentaje escala proporcionalmente desde el tamaño original. No se sube nada, el redimensionado ocurre en tu dispositivo usando la API canvas.",
        how_h2="Cómo funciona",
        how_p1="El redimensionado en sí es una primitiva del navegador: tu imagen se decodifica, se crea un <code>&lt;canvas&gt;</code> con las dimensiones objetivo, y <code>drawImage()</code> escala los píxeles sobre él en una sola pasada. El navegador aplica su filtro de suavizado incorporado (un remuestreo tipo bilineal) mientras hace esto, que promedia píxeles vecinos en vez de simplemente elegir el más cercano, así que las fotos reducidas de tamaño salen suaves en vez de dentadas. El canvas se vuelve a exportar entonces con <code>canvas.toBlob()</code> como JPEG o WebP a calidad 0.92, o como PNG sin pérdida, dependiendo de la opción de formato.",
        how_p2="Algunas verdades prácticas sobre el escalado que refleja el comportamiento de la herramienta. Reducir es donde brilla el redimensionado: promediar muchos píxeles de origen en cada píxel de salida mantiene las fotos nítidas. Ampliar no puede inventar detalle, el mismo filtro solo esparce los píxeles existentes, así que cualquier cosa por encima de 2x aproximadamente empieza a verse suave; si necesitas una versión grande, empieza desde el original más grande que tengas. Y el filtrado suave es incorrecto para exactamente un caso, el pixel art, donde en realidad quieres bordes duros de vecino más cercano; una herramienta de fotos como esta está ajustada para fotos.",
        how_p3="El modo porcentaje calcula las dimensiones objetivo a partir del tamaño original, el modo exacto toma tus números, y el interruptor de bloqueo de proporción mantiene el ancho y alto ligados a la proporción original para que las personas en tus fotos no salgan estiradas. Las dimensiones están limitadas a 20.000 píxeles por lado porque un canvas mayor que eso puede agotar la memoria del navegador. El modo por lotes ejecuta el mismo pipeline de canvas sobre cada archivo por turno y empaqueta los resultados en un ZIP que también se ensambla en JavaScript.",
        how_p4="Como todo el pipeline es decodificar, dibujar, y volver a codificar dentro de tu pestaña, tus fotos nunca salen de tu máquina. Puedes verificarlo: abre las DevTools, cambia a la pestaña Red, y redimensiona algo. No aparece ninguna petición de subida, y la herramienta sigue funcionando sin conexión.",
    ),
    related_tools=[
        ("compress-image.html", "Comprimir imagen", "Consigue un tamaño de archivo exacto en vez de dimensiones específicas."),
        ("crop-image.html", "Recortar Imagen", "Recorta una región específica en vez de escalar la imagen completa."),
        ("image-converter.html", "Conversor de imágenes", "Convierte entre JPG, PNG, y WebP."),
    ],
)

PAGES["zh"] = dict(
    title="调整图片尺寸：在线修改宽度和高度 | norito",
    meta_desc="在浏览器中把图片调整到精确尺寸或按百分比缩放。锁定宽高比以避免变形。不上传任何内容。",
    app_name="调整图片尺寸", h1="调整图片尺寸", breadcrumb_label="调整图片尺寸",
    lede="按精确像素或按百分比修改图片的宽度和高度。锁定宽高比可避免拉伸变形，或关闭以获得完全控制。",
    note_html='要为 Instagram 调整尺寸？试试 <a href="/resize-image-for-instagram.html">1080x1080 预设</a>。',
    t=dict(
        dz_click="点击选择图片", dz_drag="，或将其拖放到此处",
        dz_hint="支持 JPG、PNG、WebP。可多选批量调整尺寸。文件保留在你的设备上，不会上传任何内容。",
        resize_all="全部调整尺寸", download_zip="以 .zip 下载全部",
        resize_by="调整方式", exact_dims="精确尺寸", percentage="百分比",
        output_format="输出格式", keep_original="保持原格式",
        width_px="宽度（像素）", height_px="高度（像素）", percent_of_original="相对原图的百分比",
        lock_ratio="锁定宽高比", lock_ratio_hint="更改宽度会自动更新高度以保持匹配，反之亦然。",
        resize_image="调整图片尺寸",
        resized_preview_alt="调整后预览", preview_hint="生成后，调整尺寸后的图片会显示在这里。",
        side_note="精确尺寸会按你输入的宽度和高度拉伸或缩小图片（锁定宽高比可避免变形）。百分比会按原始尺寸等比例缩放。不会上传任何内容，调整尺寸的操作使用 canvas API 在你的设备上完成。",
        how_h2="工作原理",
        how_p1="调整尺寸本身是一个浏览器原生操作：你的图片会被解码，系统会创建一个目标尺寸的 <code>&lt;canvas&gt;</code>，然后 <code>drawImage()</code> 在一次操作中把像素缩放绘制到该画布上。浏览器在此过程中会应用内置的平滑滤镜（一种双线性风格的重采样），对相邻像素取平均值，而不是简单地选取最近的一个像素，因此缩小后的照片看起来平滑而不会出现锯齿。之后，canvas 会根据所选的格式选项，通过 <code>canvas.toBlob()</code> 以 0.92 质量重新导出为 JPEG 或 WebP，或导出为无损 PNG。",
        how_p2="这里有几个关于缩放的实用常识，也体现在这个工具的行为中。缩小正是调整尺寸真正出色的地方：把多个源像素平均合并到每个输出像素中，能让照片保持清晰。放大则无法凭空创造细节，同样的滤镜只是把已有的像素铺开，所以一旦放大超过大约 2 倍，画面就会开始变得模糊；如果你需要一个大尺寸版本，最好从你手头最大的原图开始处理。而平滑滤镜恰恰只在一种情况下不适用，那就是像素艺术（pixel art），这种场景其实需要生硬的最近邻边缘；而像这样的照片工具是为照片调校的。",
        how_p3="百分比模式会根据原始尺寸计算目标尺寸，精确模式则直接采用你输入的数值，而锁定宽高比开关会让宽度和高度始终与原始比例保持一致，这样照片中的人物就不会被拉伸变形。尺寸每边上限为 20,000 像素，因为超过这个数值的画布可能会耗尽浏览器内存。批量模式会依次对每个文件运行相同的 canvas 处理流程，并将结果打包成一个同样在 JavaScript 中组装的 ZIP 文件。",
        how_p4="由于整个处理流程——解码、绘制、重新编码——都在你的标签页内完成，你的照片永远不会离开你的电脑。你可以自己验证这一点：打开开发者工具，切换到 Network 标签页，然后调整一张图片的尺寸。你不会看到任何上传请求，而且即使离线，工具依然可以正常工作。",
    ),
    related_tools=[
        ("compress-image.html", "压缩图片", "直接压缩到指定文件大小，而不是指定尺寸。"),
        ("crop-image.html", "裁剪图片", "裁剪出特定区域，而不是缩放整张图片。"),
        ("image-converter.html", "图片格式转换器", "在 JPG、PNG 和 WebP 之间转换。"),
    ],
)

PAGES["ar"] = dict(
    title="تغيير حجم الصورة: غيّر العرض والارتفاع أونلاين | norito",
    meta_desc="غيّر حجم صورة إلى أبعاد دقيقة أو نسبة مئوية، مباشرة في متصفحك. اقفل نسبة العرض إلى الارتفاع لتجنّب التشويه. لا شيء يُرفَع.",
    app_name="تغيير حجم الصورة", h1="تغيير حجم الصورة", breadcrumb_label="تغيير حجم الصورة",
    lede="غيّر عرض وارتفاع صورة، بالبكسل الدقيق أو بنسبة مئوية. اقفل نسبة العرض إلى الارتفاع لتجنّب التمدد، أو أوقفها للتحكم الكامل.",
    note_html='تغيّر الحجم لإنستغرام؟ جرّب <a href="/resize-image-for-instagram.html">إعداد 1080×1080 المسبق</a>.',
    t=dict(
        dz_click="انقر لاختيار صور", dz_drag="، أو اسحبها وأفلتها هنا",
        dz_hint="JPG وPNG وWebP. اختر أكثر من صورة لتغيير الحجم بالجملة. تبقى على جهازك، لا شيء يُرفَع.",
        resize_all="تغيير حجم الكل", download_zip="تنزيل الكل كملف .zip",
        resize_by="تغيير الحجم حسب", exact_dims="أبعاد دقيقة", percentage="نسبة مئوية",
        output_format="تنسيق الإخراج", keep_original="الاحتفاظ بالأصلي",
        width_px="العرض (بكسل)", height_px="الارتفاع (بكسل)", percent_of_original="نسبة من الأصل",
        lock_ratio="قفل نسبة العرض إلى الارتفاع", lock_ratio_hint="تغيير العرض يحدّث الارتفاع تلقائيًا ليتطابق، والعكس صحيح.",
        resize_image="تغيير حجم الصورة",
        resized_preview_alt="معاينة بعد تغيير الحجم", preview_hint="ستظهر صورتك المُعدَّل حجمها هنا بمجرد إنشائها.",
        side_note="الأبعاد الدقيقة تمدّد أو تقلّص إلى العرض والارتفاع اللذين تُدخلهما (اقفل نسبة العرض إلى الارتفاع لتجنّب التشويه). النسبة المئوية تُغيّر الحجم تناسبيًا من الحجم الأصلي. لا شيء يُرفَع، يحدث تغيير الحجم على جهازك باستخدام واجهة canvas.",
        how_h2="كيف يعمل",
        how_p1='تغيير الحجم نفسه هو عملية بدائية واحدة في المتصفح: تُفكّ ترميز صورتك، ويُنشَأ <code>&lt;canvas&gt;</code> بالأبعاد المستهدفة، وتُغيّر <code>drawImage()</code> حجم البكسلات عليه في مرور واحد. يطبّق المتصفح مرشّح التنعيم المدمج (إعادة أخذ عينات بأسلوب ثنائي الخط) أثناء ذلك، الذي يأخذ متوسط البكسلات المجاورة بدلًا من اختيار الأقرب فقط، لذا تخرج الصور المصغَّرة ناعمة بدلًا من مسننة. تُعاد تصدير اللوحة بعدها بـ <code>canvas.toBlob()</code> كـ JPEG أو WebP بجودة 0.92، أو كـ PNG بدون فقدان، حسب خيار التنسيق.',
        how_p2="بعض الحقائق العملية حول التحجيم التي يعكسها سلوك الأداة. التصغير هو حيث يتألق تغيير الحجم: أخذ متوسط بكسلات مصدر كثيرة في كل بكسل إخراج يبقي الصور حادة. التكبير لا يمكنه اختراع تفاصيل، فنفس المرشّح يوزّع البكسلات الموجودة فقط، لذا أي شيء بعد حوالي 2x يبدأ بالظهور ناعمًا؛ إذا احتجت نسخة كبيرة، ابدأ من أكبر أصل لديك. والتنعيم خاطئ في حالة واحدة بالضبط، فن البكسل، حيث تريد فعليًا حواف الجار الأقرب الحادة؛ أداة صور مثل هذه مضبوطة للصور.",
        how_p3="يحسب وضع النسبة المئوية الأبعاد المستهدفة من الحجم الأصلي، والوضع الدقيق يأخذ أرقامك، ومفتاح قفل النسبة يبقي العرض والارتفاع مرتبطين بالنسبة الأصلية حتى لا يتمدد الأشخاص في صورك. الأبعاد محدودة بـ 20,000 بكسل لكل جانب لأن لوحة أكبر من ذلك يمكن أن تستنزف ذاكرة المتصفح. يشغّل وضع الدُفعة نفس خط أنابيب canvas على كل ملف بالتناوب ويحزم النتائج في ملف ZIP يُجمَّع أيضًا في جافاسكريبت.",
        how_p4="بما أن خط الأنابيب بأكمله هو فك ترميز، رسم، وإعادة ترميز داخل تبويبك، فإن صورك لا تغادر جهازك أبدًا. يمكنك التحقق من هذا: افتح أدوات المطوّر، انتقل إلى لسان Network، وغيّر حجم شيء ما. لا يظهر أي طلب رفع، وتستمر الأداة في العمل دون اتصال.",
    ),
    related_tools=[
        ("compress-image.html", "ضغط الصور", "احصل على حجم ملف دقيق بدلاً من أبعاد محددة."),
        ("crop-image.html", "قص الصورة", "اقصص منطقة محددة بدلاً من تحجيم الصورة كاملة."),
        ("image-converter.html", "محول الصور", "حوّل بين JPG وPNG وWebP."),
    ],
)

PAGES["hi"] = dict(
    title="इमेज रीसाइज़ करें: विड्थ और हाइट ऑनलाइन बदलें | norito",
    meta_desc="अपने ब्राउज़र में ही इमेज को सटीक डाइमेंशंस या पर्सेंटेज में रीसाइज़ करें। डिस्टॉर्शन से बचने के लिए एस्पेक्ट रेशो लॉक करें। कुछ भी अपलोड नहीं होता।",
    app_name="इमेज रीसाइज़ करें", h1="इमेज रीसाइज़ करें", breadcrumb_label="इमेज रीसाइज़ करें",
    lede="किसी इमेज की चौड़ाई और ऊंचाई बदलें, सटीक पिक्सल्स से या पर्सेंटेज से। स्ट्रेचिंग से बचने के लिए एस्पेक्ट रेशो लॉक करें, या फ़ुल कंट्रोल के लिए इसे बंद करें।",
    note_html='इंस्टाग्राम के लिए रीसाइज़ कर रहे हैं? <a href="/resize-image-for-instagram.html">1080x1080 प्रीसेट</a> ट्राई करें।',
    t=dict(
        dz_click="इमेजेज़ चुनने के लिए क्लिक करें", dz_drag=", या उन्हें यहां ड्रैग करके ड्रॉप करें",
        dz_hint="JPG, PNG, WebP। बल्क में रीसाइज़ करने के लिए एक से ज़्यादा चुनें। आपकी डिवाइस पर ही रहता है, कुछ भी अपलोड नहीं होता।",
        resize_all="सभी को रीसाइज़ करें", download_zip="सभी को .zip के रूप में डाउनलोड करें",
        resize_by="इससे रीसाइज़ करें", exact_dims="सटीक डाइमेंशंस", percentage="पर्सेंटेज",
        output_format="आउटपुट फ़ॉर्मैट", keep_original="ओरिजिनल रखें",
        width_px="चौड़ाई (px)", height_px="ऊंचाई (px)", percent_of_original="ओरिजिनल का प्रतिशत",
        lock_ratio="एस्पेक्ट रेशो लॉक करें", lock_ratio_hint="चौड़ाई बदलने पर मैच करने के लिए ऊंचाई अपने आप अपडेट होती है, और इसका उल्टा भी।",
        resize_image="इमेज रीसाइज़ करें",
        resized_preview_alt="रीसाइज़्ड प्रीव्यू", preview_hint="जनरेट होने के बाद आपकी रीसाइज़ की गई इमेज यहां दिखेगी।",
        side_note="Exact dimensions आपकी डाली गई चौड़ाई और ऊंचाई तक स्ट्रेच या श्रिंक करता है (डिस्टॉर्शन से बचने के लिए एस्पेक्ट रेशो लॉक करें)। Percentage ओरिजिनल साइज़ से प्रोपोर्शनली स्केल करता है। कुछ भी अपलोड नहीं होता, रीसाइज़ canvas API इस्तेमाल करके आपकी डिवाइस पर होता है।",
        how_h2="यह कैसे काम करता है",
        how_p1='रीसाइज़ ख़ुद एक ब्राउज़र प्रिमिटिव है: आपकी इमेज डिकोड होती है, टारगेट डाइमेंशंस पर एक <code>&lt;canvas&gt;</code> बनाया जाता है, और <code>drawImage()</code> एक ही पास में पिक्सल्स को उस पर स्केल करता है। ऐसा करते समय ब्राउज़र अपना बिल्ट-इन स्मूदिंग फ़िल्टर (एक बाइलीनियर-स्टाइल रीसैंपल) लगाता है, जो नज़दीकी पिक्सल्स को एवरेज करता है बजाय सिर्फ़ सबसे नज़दीकी वाला चुनने के, इसलिए डाउनस्केल्ड फ़ोटोज़ जैगेड होने के बजाय स्मूथ आती हैं। कैनवस को फिर <code>canvas.toBlob()</code> से JPEG या WebP के रूप में 0.92 क्वालिटी पर, या फ़ॉर्मैट ऑप्शन के आधार पर लॉसलेस PNG के रूप में री-एक्सपोर्ट किया जाता है।',
        how_p2="स्केलिंग के बारे में कुछ प्रैक्टिकल सच्चाइयां जो टूल के बर्ताव में दिखती हैं। डाउनस्केलिंग वह जगह है जहां रीसाइज़िंग चमकती है: हर आउटपुट पिक्सल में कई सोर्स पिक्सल्स को एवरेज करना फ़ोटोज़ को क्रिस्प रखता है। अपस्केलिंग डिटेल इन्वेंट नहीं कर सकती, वही फ़िल्टर बस मौजूदा पिक्सल्स को फैला देता है, इसलिए लगभग 2x के बाद कुछ भी सॉफ़्ट दिखने लगता है; अगर आपको बड़ा वर्ज़न चाहिए, तो अपने सबसे बड़े ओरिजिनल से शुरू करें। और स्मूथ फ़िल्टरिंग बिल्कुल एक ही मामले में ग़लत है, पिक्सल आर्ट, जहां आप असल में हार्ड नियरेस्ट-नेबर एजेज़ चाहते हैं; इस जैसा फ़ोटो टूल फ़ोटोज़ के लिए ट्यून किया गया है।",
        how_p3="Percentage मोड ओरिजिनल साइज़ से टारगेट डाइमेंशंस कैलकुलेट करता है, exact मोड आपके नंबर्स लेता है, और लॉक-रेशो टॉगल चौड़ाई और ऊंचाई को ओरिजिनल एस्पेक्ट से बांधे रखता है ताकि आपकी फ़ोटोज़ में लोग स्ट्रेच न हों। डाइमेंशंस हर तरफ़ 20,000 पिक्सल पर कैप्ड हैं क्योंकि इससे बड़ा कैनवस ब्राउज़र मेमोरी ख़त्म कर सकता है। बैच मोड हर फ़ाइल पर बारी-बारी से वही कैनवस पाइपलाइन चलाता है और रिज़ल्ट्स को एक ZIP में पैक करता है जो JavaScript में भी असेंबल होता है।",
        how_p4="चूंकि पूरी पाइपलाइन आपके टैब के अंदर डिकोड, ड्रॉ, री-एनकोड है, आपकी फ़ोटोज़ कभी आपकी मशीन से बाहर नहीं जातीं। आप इसे वेरिफ़ाई कर सकते हैं: डेवटूल्स खोलें, Network टैब पर स्विच करें, और कुछ रीसाइज़ करें। कोई अपलोड रिक्वेस्ट नहीं दिखती, और टूल ऑफ़लाइन भी काम करता रहता है।",
    ),
    related_tools=[
        ("compress-image.html", "इमेज कंप्रेस करें", "स्पेसिफ़िक डाइमेंशंस के बजाय एक सटीक फ़ाइल साइज़ टारगेट पाएं।"),
        ("crop-image.html", "इमेज क्रॉप करें", "पूरी इमेज को स्केल करने के बजाय एक स्पेसिफ़िक क्षेत्र काटें।"),
        ("image-converter.html", "इमेज कन्वर्टर", "JPG, PNG, और WebP के बीच कन्वर्ट करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Изменить размер изображения: ширина и высота онлайн | norito",
    meta_desc="Измените размер изображения до точных размеров или в процентах прямо в браузере. Зафиксируйте пропорции, чтобы избежать искажения. Ничего не загружается.",
    app_name="Изменить размер изображения", h1="Изменить размер изображения", breadcrumb_label="Изменить размер изображения",
    lede="Измените ширину и высоту изображения — по точным пикселям или в процентах. Зафиксируйте соотношение сторон, чтобы избежать растяжения, или отключите его для полного контроля.",
    note_html='Меняете размер для Instagram? Попробуйте <a href="/resize-image-for-instagram.html">пресет 1080x1080</a>.',
    t=dict(
        dz_click="Нажмите, чтобы выбрать изображения", dz_drag=", или перетащите их сюда",
        dz_hint="JPG, PNG, WebP. Выберите несколько файлов для массового изменения размера. Остаётся на вашем устройстве, ничего не загружается.",
        resize_all="Изменить размер всех", download_zip="Скачать всё как .zip",
        resize_by="Изменить размер по", exact_dims="Точные размеры", percentage="Процент",
        output_format="Формат вывода", keep_original="Оставить исходный",
        width_px="Ширина (пикс.)", height_px="Высота (пикс.)", percent_of_original="Процент от оригинала",
        lock_ratio="Зафиксировать пропорции", lock_ratio_hint="Изменение ширины автоматически обновляет высоту в соответствии, и наоборот.",
        resize_image="Изменить размер изображения",
        resized_preview_alt="Предпросмотр после изменения размера", preview_hint="Изображение с изменённым размером появится здесь после создания.",
        side_note="Точные размеры растягивают или сжимают изображение до введённых вами ширины и высоты (зафиксируйте пропорции, чтобы избежать искажения). Процент масштабирует пропорционально от исходного размера. Ничего не загружается, изменение размера происходит на вашем устройстве с помощью API canvas.",
        how_h2="Как это работает",
        how_p1="Само изменение размера — это один браузерный примитив: ваше изображение декодируется, создаётся <code>&lt;canvas&gt;</code> с целевыми размерами, и <code>drawImage()</code> масштабирует пиксели на него за один проход. При этом браузер применяет свой встроенный фильтр сглаживания (билинейную ресемплировку), которая усредняет соседние пиксели вместо простого выбора ближайшего, поэтому уменьшенные фотографии получаются гладкими, а не зазубренными. Затем canvas повторно экспортируется через <code>canvas.toBlob()</code> как JPEG или WebP с качеством 0.92, либо как PNG без потерь, в зависимости от выбранного формата.",
        how_p2="Несколько практических истин о масштабировании, которые отражает поведение инструмента. Уменьшение — это то, в чём изменение размера действительно раскрывается: усреднение множества исходных пикселей в каждый выходной пиксель сохраняет чёткость фотографий. Увеличение не может изобрести детали — тот же фильтр просто растягивает существующие пиксели, поэтому всё, что больше примерно 2x, начинает выглядеть размыто; если вам нужна большая версия, начните с самого крупного имеющегося оригинала. А сглаживающая фильтрация неверна ровно в одном случае — для пиксель-арта, где на самом деле нужны жёсткие края по методу ближайшего соседа; такой инструмент, как этот, настроен именно для фотографий.",
        how_p3="Режим процентов вычисляет целевые размеры из исходного размера, точный режим берёт ваши числа, а переключатель фиксации пропорций удерживает ширину и высоту привязанными к исходному соотношению, чтобы люди на ваших фотографиях не растягивались. Размеры ограничены 20 000 пикселей на сторону, потому что canvas больше этого может исчерпать память браузера. Пакетный режим последовательно прогоняет один и тот же конвейер canvas по каждому файлу и упаковывает результаты в ZIP, который также собирается в JavaScript.",
        how_p4="Поскольку весь конвейер — декодирование, отрисовка, повторное кодирование — происходит внутри вашей вкладки, ваши фотографии никогда не покидают ваш компьютер. Вы можете это проверить: откройте DevTools, переключитесь на вкладку Network и измените размер чего-нибудь. Никакого запроса на загрузку не появится, и инструмент продолжает работать в офлайне.",
    ),
    related_tools=[
        ("compress-image.html", "Сжатие изображения", "Достигните точного размера файла вместо конкретных размеров."),
        ("crop-image.html", "Обрезать изображение", "Вырежьте определённую область вместо масштабирования всего изображения."),
        ("image-converter.html", "Конвертер изображений", "Конвертируйте между JPG, PNG и WebP."),
    ],
)

PAGES["ja"] = dict(
    title="画像のリサイズ：幅と高さをオンラインで変更 | norito",
    meta_desc="ブラウザ内で画像を正確なサイズまたはパーセンテージでリサイズ。アスペクト比をロックして歪みを防止。アップロードなし。",
    app_name="画像のリサイズ", h1="画像のリサイズ", breadcrumb_label="画像のリサイズ",
    lede="画像の幅と高さを、正確なピクセル値またはパーセンテージで変更します。アスペクト比をロックして伸縮を防ぐか、オフにして自由にコントロールできます。",
    note_html='Instagram用にリサイズしますか？<a href="/resize-image-for-instagram.html">1080x1080プリセット</a>をお試しください。',
    t=dict(
        dz_click="クリックして画像を選択", dz_drag="、またはここにドラッグ＆ドロップ",
        dz_hint="JPG、PNG、WebPに対応。複数選択で一括リサイズ。デバイス内にとどまり、アップロードは一切されません。",
        resize_all="すべてリサイズ", download_zip="すべてを.zipでダウンロード",
        resize_by="リサイズ方法", exact_dims="正確なサイズ", percentage="パーセンテージ",
        output_format="出力形式", keep_original="元の形式を維持",
        width_px="幅（px）", height_px="高さ（px）", percent_of_original="元のサイズに対する割合",
        lock_ratio="アスペクト比をロック", lock_ratio_hint="幅を変更すると高さが自動的に更新されて一致します。逆も同様です。",
        resize_image="画像をリサイズ",
        resized_preview_alt="リサイズプレビュー", preview_hint="生成されると、リサイズされた画像がここに表示されます。",
        side_note="正確なサイズは、入力した幅と高さに合わせて伸縮します（歪みを防ぐにはアスペクト比をロックしてください）。パーセンテージは元のサイズから比例して拡大縮小します。何もアップロードされず、リサイズはcanvas APIを使ってお使いのデバイス上で行われます。",
        how_h2="仕組み",
        how_p1='リサイズ自体は1つのブラウザプリミティブです。画像がデコードされ、目標サイズで<code>&lt;canvas&gt;</code>が作成され、<code>drawImage()</code>が1回のパスでピクセルをその上にスケーリングします。この際、ブラウザは組み込みの平滑化フィルター（バイリニア方式のリサンプリング）を適用し、単に最も近いピクセルを選ぶのではなく近隣のピクセルを平均化するため、縮小した写真はギザギザではなく滑らかに仕上がります。その後、フォーマットのオプションに応じて、<code>canvas.toBlob()</code>を使って品質0.92のJPEGまたはWebP、あるいは可逆のPNGとして再エクスポートされます。',
        how_p2="このツールの動作に反映されている、スケーリングに関するいくつかの実用的な事実があります。縮小はリサイズが真価を発揮する場面です。多くの元ピクセルを各出力ピクセルに平均化することで、写真はシャープなまま保たれます。拡大はディテールを新たに生み出すことはできず、同じフィルターが既存のピクセルを引き伸ばすだけなので、およそ2倍を超えると滑らかで甘い見た目になり始めます。大きなバージョンが必要な場合は、手元にある最大のオリジナル画像から始めてください。そして平滑化フィルターがちょうど不向きなケースが一つあります。それはピクセルアートで、実際には最近傍法によるくっきりしたエッジが必要な場合です。このような写真ツールは写真向けに調整されています。",
        how_p3="パーセンテージモードは元のサイズから目標サイズを計算し、正確モードは入力した数値をそのまま使い、比率ロックのトグルは幅と高さを元のアスペクト比に紐づけたままにするため、写真の中の人物が引き伸ばされることはありません。サイズは各辺20,000ピクセルまでに制限されています。これはそれ以上大きいcanvasがブラウザのメモリを枯渇させる可能性があるためです。一括モードは各ファイルに対して順番に同じcanvasパイプラインを実行し、結果をJavaScriptで組み立てられたZIPにまとめます。",
        how_p4="デコード、描画、再エンコードというパイプライン全体があなたのタブ内で完結するため、あなたの写真がマシンの外に出ることはありません。これは自分で確認できます。DevToolsを開き、Networkタブに切り替えて、何かをリサイズしてみてください。アップロードリクエストは一切表示されず、ツールはオフラインでも動作し続けます。",
    ),
    related_tools=[
        ("compress-image.html", "画像を圧縮", "特定のサイズではなく正確なファイルサイズを実現。"),
        ("crop-image.html", "画像をトリミング", "画像全体を拡大縮小するのではなく特定の領域を切り取り。"),
        ("image-converter.html", "画像コンバーター", "JPG、PNG、WebP間で変換。"),
    ],
)

for loc, data in PAGES.items():
    body_html = body(data["t"])
    # replace the hero note paragraph placeholder we didn't template - append after lede via lede itself
    lede_with_note = data["lede"] + f'\n    </p>\n    <p class="note">{data["note_html"]}'
    html = render_page(
        loc, "resize-image.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=lede_with_note,
        body_html=body_html,
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-resize-image.js", "js/prefill.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/resize-image.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
