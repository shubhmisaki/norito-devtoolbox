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
            <input type="number" id="width" min="1" max="20000" value="1080" />
          </div>
          <div class="field">
            <label for="height">{t['height_px']}</label>
            <input type="number" id="height" min="1" max="20000" value="1080" />
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
    title="Redimensionar Imagen para Instagram (1080x1080) Gratis | norito",
    meta_desc="Redimensiona una foto al tamaño de publicación cuadrada 1080x1080 de Instagram, en tu navegador. También funciona para publicaciones verticales y horizontales. No se sube nada.",
    app_name="Redimensionar Imagen para Instagram", h1="Redimensionar Imagen para Instagram", breadcrumb_label="Redimensionar Imagen para Instagram",
    lede="Redimensiona una foto al tamaño de publicación cuadrada 1080x1080 de Instagram con un clic, en tu navegador. Los valores por defecto ya están fijados, solo suelta una foto. También funciona para publicaciones verticales y horizontales.",
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
        how_p1="Esto es un redimensionado con canvas con los números de Instagram ya rellenados. Tu foto se decodifica en el navegador, se dibuja sobre un <code>&lt;canvas&gt;</code> fijado a 1080x1080 con <code>drawImage()</code>, que remuestrea los píxeles con el filtro de suavizado incorporado del navegador, y se vuelve a exportar con <code>canvas.toBlob()</code> (JPEG y WebP a calidad 0.92, PNG sin pérdida). Sin app, sin subida, y los valores por defecto ya son los correctos para una publicación cuadrada del feed.",
        how_p2="Por qué 1080 específicamente: Instagram almacena las imágenes del feed a hasta 1080 píxeles de ancho y recomprime todo lo que subes. Envía una foto de 4000 píxeles e Instagram la reduce ella misma, con ajustes de compresión que no controlas; envía exactamente 1080 y ya has hecho el escalado con un remuestreo limpio, dejándole a Instagram menos que estropear. Los tres tamaños que importan son 1080x1080 para cuadrado, 1080x1350 para vertical (el más alto permitido, y el que más espacio de pantalla ocupa en el feed), y 1080x608 para horizontal. Cambia el campo de alto para lograr los otros dos.",
        how_p3="Una cosa a vigilar: si tu original no es cuadrado y fuerzas exactamente 1080x1080 con el bloqueo de proporción desactivado, la imagen se estira, no se recorta, y las caras lo mostrarán. El orden correcto es recortar primero a la forma que quieres (la herramienta Recortar Imagen hace cuadrado con un clic), y luego redimensionar aquí con el bloqueo activado.",
        how_p4="Todo ocurre en tu pestaña. Abre el panel Red de las DevTools mientras redimensionas: tu foto nunca se sube a este sitio ni a ningún otro, lo cual no es cierto para la mayoría de herramientas de \"redimensionar para Instagram\" que silenciosamente hacen ida y vuelta con tu imagen a través de sus servidores.",
    ),
    related_tools=[
        ("compress-image.html", "Comprimir imagen", "Consigue un tamaño de archivo exacto en vez de dimensiones específicas."),
        ("crop-image.html", "Recortar Imagen", "Recorta una región específica en vez de escalar la imagen completa."),
        ("image-converter.html", "Conversor de imágenes", "Convierte entre JPG, PNG, y WebP."),
    ],
)

PAGES["zh"] = dict(
    title="为 Instagram 调整图片尺寸（1080x1080）免费 | norito",
    meta_desc="在浏览器中将照片调整为 Instagram 的 1080x1080 方形帖子尺寸。同样适用于竖版和横版帖子。不上传任何内容。",
    app_name="为 Instagram 调整图片尺寸", h1="为 Instagram 调整图片尺寸", breadcrumb_label="为 Instagram 调整图片尺寸",
    lede="一键将照片调整为 Instagram 的 1080x1080 方形帖子尺寸，全部在浏览器中完成。默认值已经设好，直接拖入照片即可。同样适用于竖版和横版帖子。",
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
        how_p1="这本质上是一次预先填好了 Instagram 参数的 canvas 尺寸调整。你的照片会在浏览器中解码，通过 <code>drawImage()</code> 绘制到一个设为 1080x1080 的 <code>&lt;canvas&gt;</code> 上，浏览器内置的平滑滤镜会对像素进行重采样，然后通过 <code>canvas.toBlob()</code> 重新导出（JPEG 和 WebP 质量为 0.92，PNG 无损）。不需要 App，不会上传，而且默认值本身就适合方形动态帖子。",
        how_p2="为什么具体是 1080：Instagram 会将动态图片以最高 1080 像素宽存储，并对你上传的所有内容重新压缩。如果你发送一张 4000 像素的照片，Instagram 会自行缩小它，压缩设置由不得你控制；而如果你直接发送 1080 像素的照片，你已经用干净的重采样完成了缩放，留给 Instagram 处理和破坏的空间就更小。真正重要的三种尺寸是：1080x1080 用于方形，1080x1350 用于竖版（允许的最高高度，也是动态中占屏幕空间最多的），1080x608 用于横版。修改高度字段即可得到另外两种尺寸。",
        how_p3="需要注意一点：如果你的原图不是正方形，而你在关闭宽高比锁定的情况下强制设为精确的 1080x1080，图片会被拉伸而不是裁剪，人脸会明显看出变形。正确的顺序是先裁剪成你想要的形状（裁剪图片工具一键即可裁成正方形），然后在这里开启锁定进行调整尺寸。",
        how_p4="一切都在你的标签页内完成。调整尺寸时打开开发者工具的 Network 面板：你的照片从不会上传到这个网站或其他任何地方，而大多数「Instagram 尺寸调整」工具其实会悄悄把你的图片来回传输到它们的服务器，这一点与它们不同。",
    ),
    related_tools=[
        ("compress-image.html", "压缩图片", "直接压缩到指定文件大小，而不是指定尺寸。"),
        ("crop-image.html", "裁剪图片", "裁剪出特定区域，而不是缩放整张图片。"),
        ("image-converter.html", "图片格式转换器", "在 JPG、PNG 和 WebP 之间转换。"),
    ],
)

PAGES["ar"] = dict(
    title="تغيير حجم الصورة لإنستغرام (1080×1080) مجانًا | norito",
    meta_desc="غيّر حجم صورة إلى حجم منشور إنستغرام المربع 1080×1080، مباشرة في متصفحك. يعمل أيضًا للمنشورات العمودية والأفقية. لا شيء يُرفَع.",
    app_name="تغيير حجم الصورة لإنستغرام", h1="تغيير حجم الصورة لإنستغرام", breadcrumb_label="تغيير حجم الصورة لإنستغرام",
    lede="غيّر حجم صورة إلى حجم منشور إنستغرام المربع 1080×1080 بنقرة واحدة، مباشرة في متصفحك. الإعدادات الافتراضية مضبوطة بالفعل، فقط أسقط صورة. يعمل أيضًا للمنشورات العمودية والأفقية.",
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
        how_p1='هذا تغيير حجم بواسطة canvas مع أرقام إنستغرام مُعبَّأة مسبقًا. تُفكّ ترميز صورتك في المتصفح، وتُرسَم على <code>&lt;canvas&gt;</code> مضبوط على 1080×1080 بواسطة <code>drawImage()</code>، الذي يعيد أخذ عينات البكسلات بمرشّح التنعيم المدمج في المتصفح، وتُعاد التصدير بـ <code>canvas.toBlob()</code> (JPEG وWebP بجودة 0.92، وPNG بدون فقدان). بلا تطبيق، بلا رفع، والإعدادات الافتراضية هي بالفعل الصحيحة لمنشور مربع في الخلاصة.',
        how_p2="لماذا 1080 تحديدًا: يخزّن إنستغرام صور الخلاصة بعرض يصل إلى 1080 بكسل ويعيد ضغط كل ما ترفعه. أرسل صورة بعرض 4000 بكسل وسيقلّصها إنستغرام بنفسه، بإعدادات ضغط لا تتحكم بها؛ أرسل بالضبط 1080 وتكون قد أنجزت التحجيم بإعادة أخذ عينات نظيفة، تاركًا لإنستغرام أقل ما يُفسده. الأحجام الثلاثة المهمة هي 1080×1080 للمربع، و1080×1350 للعمودي (الأطول المسموح به، وأكبر مساحة شاشة في الخلاصة)، و1080×608 للأفقي. غيّر حقل الارتفاع للوصول إلى الاثنين الآخرين.",
        how_p3="شيء يجب مراقبته: إذا لم يكن أصلك مربعًا وفرضت بالضبط 1080×1080 مع إيقاف قفل نسبة العرض إلى الارتفاع، تُمدَّد الصورة، لا تُقصّ، وستُظهر الوجوه ذلك. الترتيب الصحيح هو القص إلى الشكل الذي تريده أولًا (أداة قص الصورة تفعل المربع بنقرة واحدة)، ثم تغيير الحجم هنا مع تفعيل القفل.",
        how_p4="كل شيء يحدث في تبويبك. افتح لوحة Network في أدوات المطوّر أثناء تغيير الحجم: صورتك لا تُرفَع أبدًا إلى هذا الموقع أو أي مكان آخر، وهذا ليس صحيحًا بالنسبة لمعظم أدوات «تغيير الحجم لإنستغرام» التي تُمرّر صورتك بصمت ذهابًا وإيابًا عبر خوادمها.",
    ),
    related_tools=[
        ("compress-image.html", "ضغط الصور", "احصل على حجم ملف دقيق بدلاً من أبعاد محددة."),
        ("crop-image.html", "قص الصورة", "اقصص منطقة محددة بدلاً من تحجيم الصورة كاملة."),
        ("image-converter.html", "محول الصور", "حوّل بين JPG وPNG وWebP."),
    ],
)

PAGES["hi"] = dict(
    title="इंस्टाग्राम के लिए इमेज रीसाइज़ करें (1080x1080) मुफ़्त | norito",
    meta_desc="अपने ब्राउज़र में ही एक फ़ोटो को इंस्टाग्राम के 1080x1080 स्क्वेयर पोस्ट साइज़ में रीसाइज़ करें। पोर्ट्रेट और लैंडस्केप पोस्ट्स के लिए भी काम करता है। कुछ भी अपलोड नहीं होता।",
    app_name="इंस्टाग्राम के लिए इमेज रीसाइज़ करें", h1="इंस्टाग्राम के लिए इमेज रीसाइज़ करें", breadcrumb_label="इंस्टाग्राम के लिए इमेज रीसाइज़ करें",
    lede="एक क्लिक में एक फ़ोटो को इंस्टाग्राम के 1080x1080 स्क्वेयर पोस्ट साइज़ में रीसाइज़ करें, आपके ब्राउज़र में ही। डिफ़ॉल्ट्स पहले से सेट हैं, बस एक फ़ोटो डालें। पोर्ट्रेट और लैंडस्केप पोस्ट्स के लिए भी काम करता है।",
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
        how_p1='यह इंस्टाग्राम के नंबर्स पहले से भरे हुए एक canvas रीसाइज़ है। आपकी फ़ोटो ब्राउज़र में डिकोड होती है, <code>drawImage()</code> से 1080x1080 पर सेट एक <code>&lt;canvas&gt;</code> पर ड्रॉ की जाती है, जो ब्राउज़र के बिल्ट-इन स्मूदिंग फ़िल्टर से पिक्सल्स को रीसैंपल करता है, और <code>canvas.toBlob()</code> से री-एक्सपोर्ट होती है (JPEG और WebP 0.92 क्वालिटी पर, PNG लॉसलेस)। कोई ऐप नहीं, कोई अपलोड नहीं, और डिफ़ॉल्ट्स पहले से ही स्क्वेयर फ़ीड पोस्ट के लिए सही हैं।',
        how_p2="1080 ही क्यों ख़ासतौर पर: इंस्टाग्राम फ़ीड इमेजेज़ को 1080 पिक्सल चौड़ाई तक स्टोर करता है और आप जो भी अपलोड करते हैं उसे दोबारा कंप्रेस करता है। एक 4,000-पिक्सल की फ़ोटो भेजें और इंस्टाग्राम उसे ख़ुद स्केल डाउन करता है, कंप्रेशन सेटिंग्स के साथ जो आपके कंट्रोल में नहीं हैं; ठीक 1080 भेजें और आपने साफ़ रीसैंपलिंग के साथ स्केलिंग कर ली है, जिससे इंस्टाग्राम के पास बर्बाद करने के लिए कम बचता है। तीन साइज़ जो मायने रखते हैं वे हैं स्क्वेयर के लिए 1080x1080, पोर्ट्रेट के लिए 1080x1350 (सबसे लंबा जो अलाउड है, और फ़ीड में सबसे ज़्यादा स्क्रीन स्पेस), और लैंडस्केप के लिए 1080x608। बाक़ी दो पाने के लिए हाइट फ़ील्ड बदलें।",
        how_p3="एक बात पर ध्यान दें: अगर आपका ओरिजिनल पहले से स्क्वेयर नहीं है और आप एस्पेक्ट-रेशो लॉक बंद करके इसे ठीक 1080x1080 पर फ़ोर्स करते हैं, तो इमेज स्ट्रेच होती है, क्रॉप नहीं, और चेहरे यह दिखा देंगे। सही क्रम है पहले उस शेप में क्रॉप करना जो आप चाहते हैं (Crop Image टूल एक क्लिक में स्क्वेयर कर देता है), फिर लॉक ऑन के साथ यहां रीसाइज़ करना।",
        how_p4="सब कुछ आपके टैब में होता है। रीसाइज़ करते समय डेवटूल्स का Network पैनल खोलें: आपकी फ़ोटो कभी इस साइट या कहीं और अपलोड नहीं होती, जो ज़्यादातर \"रीसाइज़ फ़ॉर इंस्टाग्राम\" टूल्स के लिए सच नहीं है जो चुपचाप आपकी इमेज को अपने सर्वर्स के ज़रिए राउंड-ट्रिप करते हैं।",
    ),
    related_tools=[
        ("compress-image.html", "इमेज कंप्रेस करें", "स्पेसिफ़िक डाइमेंशंस के बजाय एक सटीक फ़ाइल साइज़ टारगेट पाएं।"),
        ("crop-image.html", "इमेज क्रॉप करें", "पूरी इमेज को स्केल करने के बजाय एक स्पेसिफ़िक क्षेत्र काटें।"),
        ("image-converter.html", "इमेज कन्वर्टर", "JPG, PNG, और WebP के बीच कन्वर्ट करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Изменить размер изображения для Instagram (1080x1080) бесплатно | norito",
    meta_desc="Измените размер фото до квадратного формата поста Instagram 1080x1080 прямо в браузере. Также работает для портретных и альбомных постов. Ничего не загружается.",
    app_name="Изменить размер изображения для Instagram", h1="Изменить размер изображения для Instagram", breadcrumb_label="Изменить размер изображения для Instagram",
    lede="Измените размер фото до квадратного формата поста Instagram 1080x1080 в один клик, прямо в браузере. Значения по умолчанию уже настроены — просто добавьте фото. Также подходит для портретных и альбомных постов.",
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
        how_p1="Это изменение размера через canvas с уже заполненными числами Instagram. Ваше фото декодируется в браузере, отрисовывается на <code>&lt;canvas&gt;</code>, установленном на 1080x1080, с помощью <code>drawImage()</code>, которая ресемплирует пиксели встроенным фильтром сглаживания браузера, и повторно экспортируется через <code>canvas.toBlob()</code> (JPEG и WebP с качеством 0.92, PNG без потерь). Никакого приложения, никакой загрузки, а значения по умолчанию уже правильные для квадратного поста в ленте.",
        how_p2="Почему именно 1080: Instagram хранит изображения ленты шириной до 1080 пикселей и повторно сжимает всё, что вы загружаете. Отправьте фото на 4000 пикселей — и Instagram сам уменьшит его, с настройками сжатия, которые вы не контролируете; отправьте ровно 1080 — и вы уже выполнили масштабирование с чистой ресемплировкой, оставив Instagram меньше возможностей испортить изображение. Три важных размера: 1080x1080 для квадрата, 1080x1350 для портрета (максимально допустимая высота и наибольшее пространство экрана в ленте), и 1080x608 для альбомной ориентации. Измените поле высоты, чтобы получить остальные два.",
        how_p3="Одна вещь, за которой нужно следить: если ваш оригинал не квадратный, а вы принудительно задаёте точно 1080x1080 с отключённой фиксацией пропорций, изображение растягивается, а не обрезается, и это будет заметно на лицах. Правильный порядок — сначала обрезать до нужной формы (инструмент Обрезать изображение делает квадрат в один клик), затем изменить размер здесь с включённой фиксацией.",
        how_p4="Всё происходит в вашей вкладке. Откройте панель Network в DevTools во время изменения размера: ваше фото никогда не загружается ни на этот сайт, ни куда-либо ещё, что нельзя сказать о большинстве инструментов «изменить размер для Instagram», которые незаметно пропускают ваше изображение туда и обратно через свои серверы.",
    ),
    related_tools=[
        ("compress-image.html", "Сжатие изображения", "Достигните точного размера файла вместо конкретных размеров."),
        ("crop-image.html", "Обрезать изображение", "Вырежьте определённую область вместо масштабирования всего изображения."),
        ("image-converter.html", "Конвертер изображений", "Конвертируйте между JPG, PNG и WebP."),
    ],
)

PAGES["ja"] = dict(
    title="Instagram用に画像をリサイズ（1080x1080）無料 | norito",
    meta_desc="ブラウザ内で写真をInstagramの1080x1080正方形投稿サイズにリサイズ。縦長・横長の投稿にも対応。アップロードなし。",
    app_name="Instagram用に画像をリサイズ", h1="Instagram用に画像をリサイズ", breadcrumb_label="Instagram用に画像をリサイズ",
    lede="ブラウザ内でワンクリックで写真をInstagramの1080x1080正方形投稿サイズにリサイズします。デフォルト設定はすでに済んでいるので、写真をドロップするだけです。縦長・横長の投稿にも対応しています。",
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
        how_p1='これはInstagramの数値があらかじめ入力されたcanvasリサイズです。あなたの写真はブラウザ内でデコードされ、<code>drawImage()</code>によって1080x1080に設定された<code>&lt;canvas&gt;</code>上に描画され、ブラウザ組み込みの平滑化フィルターでピクセルがリサンプリングされ、<code>canvas.toBlob()</code>で再エクスポートされます（JPEGとWebPは品質0.92、PNGは可逆）。アプリは不要、アップロードも不要で、デフォルト設定はすでに正方形フィード投稿に最適な値になっています。',
        how_p2="なぜ具体的に1080なのか。Instagramはフィード画像を最大幅1080ピクセルで保存し、アップロードされたものすべてを再圧縮します。4000ピクセルの写真を送ると、Instagramはあなたがコントロールできない圧縮設定で自らそれを縮小します。一方、ちょうど1080で送れば、あなたはすでにクリーンなリサンプリングでスケーリングを済ませたことになり、Instagramに任せる劣化の余地が少なくなります。重要な3つのサイズは、正方形用の1080x1080、縦長用の1080x1350（許容される最大の高さで、フィードで最も画面を占める）、横長用の1080x608です。高さのフィールドを変更すれば、残りの2つのサイズが得られます。",
        how_p3="注意すべき点が一つあります。もし元の画像が正方形でないのに、アスペクト比ロックをオフにしてちょうど1080x1080に強制すると、画像は切り取られるのではなく引き伸ばされ、顔にその歪みが表れます。正しい順序は、まず希望する形にトリミングし（画像トリミングツールならワンクリックで正方形にできます）、その後ロックをオンにしたままここでリサイズすることです。",
        how_p4="すべてはあなたのタブ内で行われます。リサイズ中にDevToolsのNetworkパネルを開いてみてください。あなたの写真がこのサイトや他のどこかにアップロードされることは決してありません。これは、静かに画像をサーバー経由で往復させている、ほとんどの「Instagram用リサイズ」ツールには当てはまらない特徴です。",
    ),
    related_tools=[
        ("compress-image.html", "画像を圧縮", "特定のサイズではなく正確なファイルサイズを実現。"),
        ("crop-image.html", "画像をトリミング", "画像全体を拡大縮小するのではなく特定の領域を切り取り。"),
        ("image-converter.html", "画像コンバーター", "JPG、PNG、WebP間で変換。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "resize-image-for-instagram.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-resize-image.js", "js/prefill.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/resize-image-for-instagram.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
