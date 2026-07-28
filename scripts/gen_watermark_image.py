#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg>'
ICON_CLASS = "c-purple"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="dropzone" id="drop">
          <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg>
          <p><strong>{t['dz_click']}</strong>{t['dz_drag']}</p>
          <p class="note" style="margin-top:2px;">{t['dz_hint']}</p>
          <input type="file" id="fileInput" accept="image/*" />
        </div>
        <p class="note" id="originalInfo" style="display:none;"></p>

        <div id="editorWrap" style="display:none;">
          <div class="stage-wrap" id="stage">
            <img id="stageImg" alt="{t['wm_preview_alt']}" />
            <span class="wm-live-preview" id="wmPreviewText">{t['sample']}</span>
          </div>
        </div>

        <div class="field" style="margin-top:16px;">
          <label for="wmText">{t['wm_text']}</label>
          <input type="text" id="wmText" value="{t['default_wm']}" maxlength="80" />
        </div>

        <div class="field-row">
          <div class="field">
            <label for="wmSize">{t['font_size']}</label>
            <input type="number" id="wmSize" min="8" max="200" value="32" />
          </div>
          <div class="field">
            <label for="wmOpacity">{t['opacity']}</label>
            <input type="number" id="wmOpacity" min="1" max="100" value="40" />
          </div>
          <div class="field">
            <label for="wmAngle">{t['angle']}</label>
            <input type="number" id="wmAngle" min="-180" max="180" value="0" />
          </div>
          <div class="field">
            <label for="wmColor">{t['color']}</label>
            <input type="color" id="wmColor" value="#ffffff" />
          </div>
        </div>

        <div class="field">
          <label for="wmPosition">{t['position']}</label>
          <select id="wmPosition">
            <option value="top-left">{t['top_left']}</option>
            <option value="top-center">{t['top_center']}</option>
            <option value="top-right">{t['top_right']}</option>
            <option value="center-left">{t['center_left']}</option>
            <option value="center" selected>{t['center']}</option>
            <option value="center-right">{t['center_right']}</option>
            <option value="bottom-left">{t['bottom_left']}</option>
            <option value="bottom-center">{t['bottom_center']}</option>
            <option value="bottom-right">{t['bottom_right']}</option>
          </select>
        </div>

        <button id="applyBtn" disabled style="margin-top:8px;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg>
          {t['apply_download']}
        </button>
        <div class="result-box" id="result" style="display:none;"></div>
      </div>

      <div>
        <div class="panel" style="text-align:center;">
          <img class="preview" id="preview" style="display:none; max-width:100%;" alt="{t['result_alt']}" />
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
    title="Añadir Marca de Agua a una Imagen Online | norito",
    meta_desc="Añade una marca de agua de texto a una foto con vista previa en vivo, en tu navegador. Controla tamaño, opacidad, ángulo, color, y posición. No se sube nada.",
    app_name="Marca de Agua en Imagen", h1="Marca de Agua en Imagen", breadcrumb_label="Marca de Agua en Imagen",
    lede="Añade una marca de agua de texto a una foto, con vista previa en vivo sobre la imagen real para que veas exactamente cómo se verán el tamaño, la opacidad, el ángulo, y la posición.",
    t=dict(
        dz_click="Haz clic para elegir una imagen", dz_drag=", o arrástrala aquí",
        dz_hint="JPG, PNG, WebP. Se queda en tu dispositivo, no se sube nada.",
        wm_preview_alt="Vista previa de marca de agua", sample="MUESTRA",
        wm_text="Texto de la marca de agua", default_wm="© Tu Nombre",
        font_size="Tamaño de fuente (px)", opacity="Opacidad (%)", angle="Ángulo (°)", color="Color",
        position="Posición", top_left="Arriba izquierda", top_center="Arriba centro", top_right="Arriba derecha",
        center_left="Centro izquierda", center="Centro", center_right="Centro derecha",
        bottom_left="Abajo izquierda", bottom_center="Abajo centro", bottom_right="Abajo derecha",
        apply_download="Aplicar marca de agua y descargar",
        result_alt="Resultado con marca de agua", preview_hint="Tu imagen con marca de agua aparecerá aquí una vez generada.",
        side_note="La vista previa de arriba muestra tu marca de agua en vivo sobre la imagen real mientras ajustas tamaño, opacidad, ángulo, color, y posición. La descarga final coincide con lo que ves, escalada a la resolución completa de tu imagen.",
        how_h2="Cómo funciona",
        how_p1='La vista previa en vivo es un elemento DOM posicionado en capas sobre tu foto, pero la imagen final es trabajo de píxeles real sobre un <code>&lt;canvas&gt;</code>. Cuando pulsas aplicar, la imagen original se dibuja a resolución completa, luego el contexto del canvas se traslada a uno de nueve puntos de anclaje (esquinas, puntos medios de bordes, centro, cada uno con un margen del 6%), se rota según tu ángulo, y el texto se dibuja con <code>fillText()</code> usando tu color y opacidad vía <code>globalAlpha</code>. La alineación de texto y la línea base se ajustan según el ancla para que "abajo derecha" en la vista previa aterrice en el mismo punto relativo en la salida.',
        how_p2='La parte sutil es la escala. Tu vista previa en pantalla puede tener 500 píxeles de ancho mientras que la foto real tiene 4000, así que una herramienta ingenua renderiza una marca de agua que se veía bien en la vista previa pero sale microscópica. Esta mide la proporción entre el ancho de vista previa mostrado y el ancho natural de la imagen y multiplica el tamaño de fuente por ello, así que 48px en la vista previa significa el mismo tamaño proporcional en el archivo de resolución completa. El resultado se vuelve a codificar en el formato original: JPEG a calidad 0.95, PNG sin pérdida (elige PNG si quieres los bordes de texto más nítidos posibles).',
        how_p3='Vale la pena entender qué es una marca de agua: este texto se hornea en los píxeles, no se almacena como una capa o metadato, así que nadie puede eliminarlo de la forma en que se eliminan los datos EXIF. Eso corta en ambos sentidos. Una marca pequeña y de baja opacidad en una esquina es presa fácil para herramientas de recorte e inpainting con IA; una marca de agua que realmente protege una imagen se superpone al sujeto, en ángulo, con opacidad moderada, que es exactamente para lo que sirven los controles de posición, ángulo, y opacidad.',
        how_p4='Tanto la vista previa como el renderizado final se ejecutan en tu pestaña. Revisa el panel Red de las DevTools mientras trabajas: la foto nunca se sube, así que las pruebas de cliente y las tomas no publicadas se quedan en tu máquina.',
    ),
    related_tools=[
        ("remove-metadata.html", "Eliminar metadatos", "Elimina EXIF y datos GPS antes de compartir una foto."),
        ("compress-image.html", "Comprimir imagen", "Reduce el tamaño del archivo después de poner la marca de agua."),
        ("pdf/add-watermark.html", "Añadir marca de agua (PDF)", "Marca cada página de un documento PDF en su lugar."),
    ],
)

PAGES["zh"] = dict(
    title="在线为图片添加水印 | norito",
    meta_desc="在浏览器中为照片添加带实时预览的文字水印。可控制大小、不透明度、角度、颜色和位置。不上传任何内容。",
    app_name="图片水印", h1="图片水印", breadcrumb_label="图片水印",
    lede="为照片添加文字水印，实时预览直接显示在原图上，让你精确查看大小、不透明度、角度和位置的实际效果。",
    t=dict(
        dz_click="点击选择一张图片", dz_drag="，或将其拖放到此处",
        dz_hint="支持 JPG、PNG、WebP。文件保留在你的设备上，不会上传任何内容。",
        wm_preview_alt="水印预览", sample="示例",
        wm_text="水印文字", default_wm="© 你的名字",
        font_size="字体大小（px）", opacity="不透明度（%）", angle="角度（°）", color="颜色",
        position="位置", top_left="左上", top_center="上居中", top_right="右上",
        center_left="左中", center="居中", center_right="右中",
        bottom_left="左下", bottom_center="下居中", bottom_right="右下",
        apply_download="应用水印并下载",
        result_alt="加水印后的结果", preview_hint="生成后，加了水印的图片会显示在这里。",
        side_note="上方预览会在你调整大小、不透明度、角度、颜色和位置时，实时显示水印在原图上的效果。最终下载结果与你看到的一致，并会按图片的完整分辨率进行缩放。",
        how_h2="工作原理",
        how_p1='实时预览是叠加在你照片上方的一个定位 DOM 元素，但最终图片是在 <code>&lt;canvas&gt;</code> 上进行的真正像素处理。当你点击应用时，原始图片会以完整分辨率绘制，然后 canvas 上下文会移动到九个锚点之一（四角、边缘中点、中心，每个都有 6% 的内边距），按你设置的角度旋转，再通过 <code>fillText()</code> 绘制文字，并使用 <code>globalAlpha</code> 应用你设置的颜色和不透明度。文字对齐和基线会根据锚点设置，因此预览中的「右下」在输出中也会落在相对相同的位置。',
        how_p2='微妙之处在于缩放比例。你屏幕上的预览可能只有 500 像素宽，而实际照片有 4000 像素宽，因此一个简单粗暴的工具渲染出的水印在预览中看起来正常，实际却小得几乎看不见。这个工具会计算显示预览宽度与图片原始宽度之间的比例，并按此比例放大字体大小，因此预览中的 48px 在完整分辨率文件中对应相同的比例大小。结果会以原始格式重新编码：JPEG 质量为 0.95，PNG 无损（如果你想要最清晰的文字边缘，请选择 PNG）。',
        how_p3='值得了解水印的本质：这段文字被直接烘焙进像素中，而不是作为图层或元数据存储的，所以没有人能像清除 EXIF 数据那样把它剥离掉。这也是一把双刃剑。放在角落、透明度很低的小水印，很容易被裁剪工具或 AI 图像修复轻松去除；真正能保护图片的水印会与主体重叠、带有一定角度、透明度适中——这正是位置、角度和不透明度控制项存在的意义。',
        how_p4='预览和最终渲染都在你的标签页中完成。工作时打开开发者工具的 Network 面板看看：照片从未被上传，因此客户样片和未发布的照片都只留在你的电脑上。',
    ),
    related_tools=[
        ("remove-metadata.html", "删除元数据", "在分享照片前清除 EXIF 和 GPS 数据。"),
        ("compress-image.html", "压缩图片", "加水印后缩小文件大小。"),
        ("pdf/add-watermark.html", "添加水印（PDF）", "改为为 PDF 文档的每一页添加水印。"),
    ],
)

PAGES["ar"] = dict(
    title="إضافة علامة مائية إلى صورة أونلاين | norito",
    meta_desc="أضف علامة مائية نصية إلى صورة مع معاينة مباشرة، مباشرة في متصفحك. تحكم في الحجم والشفافية والزاوية واللون والموضع. لا شيء يُرفَع.",
    app_name="علامة مائية على الصورة", h1="علامة مائية على الصورة", breadcrumb_label="علامة مائية على الصورة",
    lede="أضف علامة مائية نصية إلى صورة، مع معاينة مباشرة على الصورة الفعلية حتى ترى بالضبط كيف سيبدو الحجم والشفافية والزاوية والموضع.",
    t=dict(
        dz_click="انقر لاختيار صورة", dz_drag="، أو اسحبها وأفلتها هنا",
        dz_hint="JPG وPNG وWebP. تبقى على جهازك، لا شيء يُرفَع.",
        wm_preview_alt="معاينة العلامة المائية", sample="عيّنة",
        wm_text="نص العلامة المائية", default_wm="© اسمك",
        font_size="حجم الخط (بكسل)", opacity="الشفافية (%)", angle="الزاوية (°)", color="اللون",
        position="الموضع", top_left="أعلى يسار", top_center="أعلى وسط", top_right="أعلى يمين",
        center_left="وسط يسار", center="الوسط", center_right="وسط يمين",
        bottom_left="أسفل يسار", bottom_center="أسفل وسط", bottom_right="أسفل يمين",
        apply_download="تطبيق العلامة المائية والتنزيل",
        result_alt="نتيجة بعلامة مائية", preview_hint="ستظهر صورتك بعلامة مائية هنا بمجرد إنشائها.",
        side_note="تُظهر المعاينة أعلاه علامتك المائية مباشرة على الصورة الفعلية أثناء ضبط الحجم والشفافية والزاوية واللون والموضع. يطابق التنزيل النهائي ما تراه، بحجم مكبّر إلى الدقة الكاملة لصورتك.",
        how_h2="كيف يعمل",
        how_p1='المعاينة المباشرة هي عنصر DOM موضوع فوق صورتك، لكن الصورة النهائية هي عمل بكسل حقيقي على <code>&lt;canvas&gt;</code>. عندما تضغط تطبيق، تُرسَم الصورة الأصلية بالدقة الكاملة، ثم يُنقَل سياق canvas إلى واحدة من تسع نقاط ارتساء (الزوايا، منتصفات الحواف، المركز، كل منها بهامش 6%)، ويُدار بزاويتك، ويُرسَم النص بـ <code>fillText()</code> باستخدام لونك وشفافيتك عبر <code>globalAlpha</code>. تُضبَط محاذاة النص وخط الأساس حسب نقطة الارتساء بحيث تهبط «أسفل يمين» في المعاينة في نفس النقطة النسبية في الإخراج.',
        how_p2='الجزء الدقيق هو المقياس. قد تكون معاينتك على الشاشة بعرض 500 بكسل بينما الصورة الفعلية 4000، لذا تعرض أداة ساذجة علامة مائية بدت صحيحة في المعاينة لكنها تخرج مجهرية. هذه الأداة تقيس النسبة بين عرض المعاينة المعروض والعرض الطبيعي للصورة وتضرب حجم الخط بها، لذا 48 بكسل في المعاينة تعني نفس الحجم النسبي في الملف بالدقة الكاملة. تُعاد ترميز النتيجة بالتنسيق الأصلي: JPEG بجودة 0.95، PNG بدون فقدان (اختر PNG إذا كنت تريد أكثر حواف نص وضوحًا ممكنة).',
        how_p3='يستحق فهم ما هي العلامة المائية: هذا النص مخبوز في البكسلات، ليس مخزَّنًا كطبقة أو بيانات وصفية، لذا لا يستطيع أحد إزالته كما تُزال بيانات EXIF. هذا له وجهان. علامة صغيرة منخفضة الشفافية في زاوية تكون فريسة سهلة لأدوات القص والتلوين بالذكاء الاصطناعي؛ العلامة المائية التي تحمي صورة فعليًا تتداخل مع الموضوع، بزاوية، بشفافية معتدلة، وهذا بالضبط ما تُستخدم من أجله عناصر تحكم الموضع والزاوية والشفافية.',
        how_p4='تعمل كل من المعاينة والعرض النهائي في تبويبك. تحقّق من لوحة Network في أدوات المطوّر أثناء العمل: لا تُرفَع الصورة أبدًا، لذا تبقى نسخ العملاء واللقطات غير المنشورة على جهازك.',
    ),
    related_tools=[
        ("remove-metadata.html", "إزالة البيانات الوصفية", "أزل بيانات EXIF وGPS قبل مشاركة صورة."),
        ("compress-image.html", "ضغط الصور", "قلّص حجم الملف بعد وضع العلامة المائية."),
        ("pdf/add-watermark.html", "إضافة علامة مائية (PDF)", "ضع علامة مائية على كل صفحة من مستند PDF بدلاً من ذلك."),
    ],
)

PAGES["hi"] = dict(
    title="इमेज पर ऑनलाइन वॉटरमार्क जोड़ें | norito",
    meta_desc="अपने ब्राउज़र में ही एक फ़ोटो पर लाइव प्रीव्यू के साथ टेक्स्ट वॉटरमार्क जोड़ें। साइज़, ओपैसिटी, एंगल, कलर, और पोज़िशन कंट्रोल करें। कुछ भी अपलोड नहीं होता।",
    app_name="इमेज पर वॉटरमार्क", h1="इमेज पर वॉटरमार्क", breadcrumb_label="इमेज पर वॉटरमार्क",
    lede="किसी फ़ोटो पर एक टेक्स्ट वॉटरमार्क जोड़ें, असली इमेज पर लाइव प्रीव्यू के साथ ताकि आप बिल्कुल देख सकें कि साइज़, ओपैसिटी, एंगल, और पोज़िशन कैसे दिखेंगे।",
    t=dict(
        dz_click="इमेज चुनने के लिए क्लिक करें", dz_drag=", या इसे यहां ड्रैग करके ड्रॉप करें",
        dz_hint="JPG, PNG, WebP। आपकी डिवाइस पर ही रहता है, कुछ भी अपलोड नहीं होता।",
        wm_preview_alt="वॉटरमार्क प्रीव्यू", sample="सैंपल",
        wm_text="वॉटरमार्क टेक्स्ट", default_wm="© आपका नाम",
        font_size="फ़ॉन्ट साइज़ (px)", opacity="ओपैसिटी (%)", angle="एंगल (°)", color="कलर",
        position="पोज़िशन", top_left="टॉप लेफ़्ट", top_center="टॉप सेंटर", top_right="टॉप राइट",
        center_left="सेंटर लेफ़्ट", center="सेंटर", center_right="सेंटर राइट",
        bottom_left="बॉटम लेफ़्ट", bottom_center="बॉटम सेंटर", bottom_right="बॉटम राइट",
        apply_download="वॉटरमार्क लागू करें और डाउनलोड करें",
        result_alt="वॉटरमार्क किया गया परिणाम", preview_hint="जनरेट होने के बाद आपकी वॉटरमार्क की गई इमेज यहां दिखेगी।",
        side_note="ऊपर दिया गया प्रीव्यू आपका वॉटरमार्क असली इमेज पर लाइव दिखाता है जैसे ही आप साइज़, ओपैसिटी, एंगल, कलर, और पोज़िशन एडजस्ट करते हैं। फ़ाइनल डाउनलोड वही मैच करता है जो आप देखते हैं, आपकी इमेज के फ़ुल रिज़ॉल्यूशन तक स्केल्ड।",
        how_h2="यह कैसे काम करता है",
        how_p1='लाइव प्रीव्यू आपकी फ़ोटो के ऊपर लेयर्ड एक पोज़िशन्ड DOM एलिमेंट है, लेकिन फ़ाइनल इमेज एक <code>&lt;canvas&gt;</code> पर असली पिक्सल वर्क है। जब आप अप्लाई दबाते हैं, ओरिजिनल इमेज फ़ुल रिज़ॉल्यूशन पर ड्रॉ होती है, फिर canvas कॉन्टेक्स्ट को नौ एंकर पॉइंट्स में से एक पर ट्रांसलेट किया जाता है (कॉर्नर्स, एज मिडपॉइंट्स, सेंटर, हर एक 6% मार्जिन से इनसेट), आपके एंगल से रोटेट किया जाता है, और टेक्स्ट को <code>fillText()</code> से आपके कलर और ओपैसिटी के साथ <code>globalAlpha</code> के ज़रिए ड्रॉ किया जाता है। टेक्स्ट एलाइनमेंट और बेसलाइन हर एंकर के हिसाब से सेट होते हैं ताकि प्रीव्यू में "बॉटम-राइट" आउटपुट में उसी रिलेटिव जगह पर पहुंचे।',
        how_p2="सूक्ष्म हिस्सा स्केल है। आपका ऑन-स्क्रीन प्रीव्यू 500 पिक्सल चौड़ा हो सकता है जबकि असली फ़ोटो 4,000 है, इसलिए एक नैव टूल एक ऐसा वॉटरमार्क रेंडर करता है जो प्रीव्यू में सही दिखा लेकिन माइक्रोस्कोपिक निकलता है। यह डिस्प्ले किए गए प्रीव्यू विड्थ और इमेज की नैचुरल विड्थ के बीच का रेशो नापता है और फ़ॉन्ट साइज़ को उससे गुणा करता है, इसलिए प्रीव्यू में 48px का मतलब है फ़ुल-रिज़ॉल्यूशन फ़ाइल में वही प्रोपोर्शनल साइज़। रिज़ल्ट ओरिजिनल फ़ॉर्मैट में री-एनकोड होता है: JPEG 0.95 क्वालिटी पर, PNG लॉसलेस (सबसे शार्प संभव टेक्स्ट एजेज़ चाहिए तो PNG चुनें)।",
        how_p3="वॉटरमार्क क्या है इसके बारे में जानना ज़रूरी है: यह टेक्स्ट पिक्सल्स में बेक किया जाता है, किसी लेयर या मेटाडेटा के रूप में स्टोर नहीं होता, इसलिए कोई भी इसे उस तरह नहीं हटा सकता जैसे EXIF डेटा हटाया जाता है। यह दोनों तरफ़ काटता है। किसी कोने में एक छोटा, लो-ओपैसिटी वाला निशान क्रॉप टूल्स और AI इनपेंटिंग के लिए आसान शिकार है; एक वॉटरमार्क जो वाक़ई किसी इमेज को प्रोटेक्ट करता है वह सब्जेक्ट के ऊपर ओवरलैप करता है, एंगल पर, मॉडरेट ओपैसिटी पर, और यही बिल्कुल वह है जिसके लिए पोज़िशन, एंगल, और ओपैसिटी कंट्रोल्स हैं।",
        how_p4="प्रीव्यू और फ़ाइनल रेंडर दोनों आपके टैब में चलते हैं। काम करते समय डेवटूल्स का Network पैनल चेक करें: फ़ोटो कभी अपलोड नहीं होती, इसलिए क्लाइंट प्रूफ़्स और अनरिलीज़्ड शॉट्स आपकी मशीन पर ही रहते हैं।",
    ),
    related_tools=[
        ("remove-metadata.html", "मेटाडेटा हटाएं", "किसी फ़ोटो को शेयर करने से पहले EXIF और GPS डेटा हटाएं।"),
        ("compress-image.html", "इमेज कंप्रेस करें", "वॉटरमार्किंग के बाद फ़ाइल साइज़ छोटा करें।"),
        ("pdf/add-watermark.html", "वॉटरमार्क जोड़ें (PDF)", "इसके बजाय PDF डॉक्यूमेंट के हर पेज पर वॉटरमार्क लगाएं।"),
    ],
)

PAGES["ru"] = dict(
    title="Добавить водяной знак на изображение онлайн | norito",
    meta_desc="Добавьте текстовый водяной знак на фото с живым предпросмотром прямо в браузере. Контролируйте размер, прозрачность, угол, цвет и положение. Ничего не загружается.",
    app_name="Водяной знак на изображении", h1="Водяной знак на изображении", breadcrumb_label="Водяной знак на изображении",
    lede="Добавьте текстовый водяной знак на фото с живым предпросмотром прямо на реальном изображении, чтобы точно видеть, как будут выглядеть размер, прозрачность, угол и положение.",
    t=dict(
        dz_click="Нажмите, чтобы выбрать изображение", dz_drag=", или перетащите его сюда",
        dz_hint="JPG, PNG, WebP. Остаётся на вашем устройстве, ничего не загружается.",
        wm_preview_alt="Предпросмотр водяного знака", sample="ОБРАЗЕЦ",
        wm_text="Текст водяного знака", default_wm="© Ваше имя",
        font_size="Размер шрифта (px)", opacity="Прозрачность (%)", angle="Угол (°)", color="Цвет",
        position="Положение", top_left="Слева вверху", top_center="По центру вверху", top_right="Справа вверху",
        center_left="Слева по центру", center="По центру", center_right="Справа по центру",
        bottom_left="Слева внизу", bottom_center="По центру внизу", bottom_right="Справа внизу",
        apply_download="Применить водяной знак и скачать",
        result_alt="Результат с водяным знаком", preview_hint="Изображение с водяным знаком появится здесь после создания.",
        side_note="Предпросмотр выше показывает ваш водяной знак в реальном времени прямо на изображении, пока вы настраиваете размер, прозрачность, угол, цвет и положение. Итоговый файл для скачивания соответствует тому, что вы видите, в полном разрешении вашего изображения.",
        how_h2="Как это работает",
        how_p1="Живой предпросмотр — это позиционированный DOM-элемент, наложенный поверх вашего фото, но итоговое изображение — это настоящая работа с пикселями на <code>&lt;canvas&gt;</code>. Когда вы нажимаете «применить», исходное изображение отрисовывается в полном разрешении, затем контекст canvas смещается к одной из девяти опорных точек (углы, середины краёв, центр, каждая с отступом 6%), поворачивается на заданный угол, и текст рисуется с помощью <code>fillText()</code> с вашим цветом и прозрачностью через <code>globalAlpha</code>. Выравнивание текста и базовая линия задаются в зависимости от опорной точки, поэтому «справа внизу» в предпросмотре попадает в ту же относительную точку в результате.",
        how_p2="Тонкий момент — масштаб. Ваш предпросмотр на экране может быть шириной 500 пикселей, тогда как реальное фото — 4000, поэтому наивный инструмент отрисует водяной знак, который выглядел правильно в предпросмотре, но получится микроскопическим. Этот инструмент измеряет соотношение между отображаемой шириной предпросмотра и естественной шириной изображения и умножает размер шрифта на это соотношение, поэтому 48px в предпросмотре означает тот же пропорциональный размер в файле полного разрешения. Результат перекодируется в исходном формате: JPEG с качеством 0.95, PNG без потерь (выбирайте PNG, если хотите максимально чёткие края текста).",
        how_p3="Стоит понимать, что представляет собой водяной знак: этот текст впекается в пиксели, а не хранится как слой или метаданные, поэтому никто не может удалить его так, как удаляются данные EXIF. У этого есть две стороны. Маленький знак с низкой прозрачностью в углу — лёгкая добыча для инструментов обрезки и AI-инпейнтинга; водяной знак, который действительно защищает изображение, перекрывает объект съёмки, расположен под углом, с умеренной прозрачностью — именно для этого и служат элементы управления положением, углом и прозрачностью.",
        how_p4="И предпросмотр, и финальный рендеринг выполняются в вашей вкладке. Проверьте панель Network в DevTools во время работы: фото никогда не загружается, поэтому клиентские пруфы и неопубликованные кадры остаются на вашем компьютере.",
    ),
    related_tools=[
        ("remove-metadata.html", "Удаление метаданных", "Удалите EXIF и GPS-данные перед публикацией фото."),
        ("compress-image.html", "Сжатие изображения", "Уменьшите размер файла после добавления водяного знака."),
        ("pdf/add-watermark.html", "Добавить водяной знак (PDF)", "Вместо этого добавьте водяной знак на каждую страницу PDF-документа."),
    ],
)

PAGES["ja"] = dict(
    title="オンラインで画像に透かしを追加 | norito",
    meta_desc="ブラウザ内でリアルタイムプレビュー付きで写真にテキストの透かしを追加。サイズ、不透明度、角度、色、位置を調整可能。アップロードなし。",
    app_name="画像に透かしを追加", h1="画像に透かしを追加", breadcrumb_label="画像に透かしを追加",
    lede="写真にテキストの透かしを追加します。実際の画像上でリアルタイムプレビューが表示されるため、サイズ、不透明度、角度、位置がどう見えるか正確に確認できます。",
    t=dict(
        dz_click="クリックして画像を選択", dz_drag="、またはここにドラッグ＆ドロップ",
        dz_hint="JPG、PNG、WebPに対応。デバイス内にとどまり、アップロードは一切されません。",
        wm_preview_alt="透かしプレビュー", sample="サンプル",
        wm_text="透かしテキスト", default_wm="© あなたの名前",
        font_size="フォントサイズ（px）", opacity="不透明度（%）", angle="角度（°）", color="色",
        position="位置", top_left="左上", top_center="上中央", top_right="右上",
        center_left="左中央", center="中央", center_right="右中央",
        bottom_left="左下", bottom_center="下中央", bottom_right="右下",
        apply_download="透かしを適用してダウンロード",
        result_alt="透かし適用後の結果", preview_hint="生成されると、透かしが入った画像がここに表示されます。",
        side_note="上のプレビューは、サイズ、不透明度、角度、色、位置を調整するたびに実際の画像上でリアルタイムに透かしを表示します。最終的なダウンロードファイルは、表示されているものと一致し、画像のフル解像度に拡大されます。",
        how_h2="仕組み",
        how_p1='ライブプレビューは写真の上に重ねて配置されたDOM要素ですが、最終的な画像は<code>&lt;canvas&gt;</code>上での実際のピクセル処理です。適用をクリックすると、元の画像がフル解像度で描画され、canvasのコンテキストが9つの基準点（四隅、辺の中点、中央、それぞれ6%のマージンで内側に配置）のいずれかに移動され、指定した角度で回転し、テキストが<code>fillText()</code>で描画されます。色と不透明度は<code>globalAlpha</code>を通じて適用されます。テキストの配置とベースラインは基準点ごとに設定されるため、プレビューでの「右下」は出力でも同じ相対位置に配置されます。',
        how_p2="微妙な部分はスケールです。画面上のプレビューは500ピクセル幅かもしれませんが、実際の写真は4000ピクセルあるため、単純なツールではプレビューでは正しく見えた透かしが、実際には極小になってしまいます。このツールは表示されているプレビューの幅と画像の本来の幅の比率を測定し、その比率でフォントサイズを掛け合わせます。そのため、プレビューでの48pxは、フル解像度のファイルでも同じ比率のサイズになります。結果は元の形式で再エンコードされます。JPEGは品質0.95、PNGは可逆です（できるだけシャープなテキストの縁が欲しい場合はPNGを選んでください）。",
        how_p3="透かしとは何かを理解しておく価値があります。このテキストはレイヤーやメタデータとして保存されるのではなく、ピクセルに焼き込まれるため、EXIFデータのように誰かが取り除くことはできません。これは諸刃の剣でもあります。隅にある小さく不透明度の低い透かしは、切り抜きツールやAIによるインペインティングの格好の餌食になります。実際に画像を保護する透かしは、被写体に重なり、角度がついていて、適度な不透明度を持つものです。これはまさに位置、角度、不透明度のコントロールが存在する理由です。",
        how_p4="プレビューも最終レンダリングも、あなたのタブ内で実行されます。作業中にDevToolsのNetworkパネルを確認してみてください。写真は決してアップロードされないため、クライアントの校正刷りや未公開のショットはあなたのマシン内にとどまります。",
    ),
    related_tools=[
        ("remove-metadata.html", "メタデータを削除", "写真を共有する前にEXIFとGPSデータを削除。"),
        ("compress-image.html", "画像を圧縮", "透かしを追加した後にファイルサイズを縮小。"),
        ("pdf/add-watermark.html", "透かしを追加（PDF）", "代わりにPDF文書の全ページに透かしを追加。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "watermark-image.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-watermark-image.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/watermark-image.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
