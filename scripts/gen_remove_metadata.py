#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>'
ICON_CLASS = "c-rose"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="dropzone" id="drop">
          <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>
          <p><strong>{t['dz_click']}</strong>{t['dz_drag']}</p>
          <p class="note" style="margin-top:2px;">{t['dz_hint']}</p>
          <input type="file" id="fileInput" accept="image/*" />
        </div>
        <p class="note" id="originalInfo" style="display:none;"></p>

        <div class="meta-panel" id="metaPanel" style="display:none;">
          <p class="meta-summary"></p>
          <div class="meta-list" id="metaList"></div>
        </div>

        <button id="cleanBtn" disabled style="margin-top:20px;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>
          {t['remove_download']}
        </button>
        <div class="result-box" id="result" style="display:none;"></div>
      </div>

      <div>
        <div class="panel" style="text-align:center;">
          <img class="preview" id="preview" style="display:none; max-width:100%;" alt="{t['cleaned_alt']}" />
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
    title="Eliminar Metadatos de Imagen: Borra EXIF y GPS | norito",
    meta_desc="Elimina EXIF, ubicación GPS, y otros metadatos ocultos de una foto, en tu navegador. Ve lo que se encuentra antes de eliminarlo. No se sube nada.",
    app_name="Eliminar Metadatos", h1="Eliminar Metadatos", breadcrumb_label="Eliminar Metadatos",
    lede="Elimina EXIF, ubicación GPS, información de cámara, y marcas de tiempo de una foto. Ve exactamente qué está incrustado antes de eliminarlo.",
    t=dict(
        dz_click="Haz clic para elegir una imagen", dz_drag=", o arrástrala aquí",
        dz_hint="JPG funciona mejor para leer metadatos existentes. PNG/WebP también son compatibles. Se queda en tu dispositivo.",
        remove_download="Eliminar metadatos y descargar",
        cleaned_alt="Imagen limpiada", preview_hint="Tu imagen limpiada aparecerá aquí una vez generada.",
        side_note="Las fotos de teléfonos y cámaras suelen incrustar datos EXIF: las coordenadas GPS exactas de dónde se tomó, el modelo de cámara o teléfono, y una marca de tiempo. Esto lee primero lo que realmente hay en tu archivo, y luego elimina todo volviendo a codificar la imagen desde cero.",
        how_h2="Cómo funciona",
        how_p1='Cuando sueltas un JPEG, la herramienta lee los bytes crudos del archivo con un <code>DataView</code> y recorre la estructura de marcadores JPEG buscando el segmento APP1, que es donde vive el EXIF. Dentro, analiza el árbol de directorios TIFF: IFD0 (marca y modelo de cámara, software, fecha de modificación), el subdirectorio Exif (hora de captura original, exposición, apertura, ISO), y el subdirectorio GPS. Maneja ambos órdenes de bytes (archivos estilo Intel y Motorola) y valores tanto en línea como almacenados por desplazamiento, y luego te muestra una lista sencilla de lo que encontró antes de que confirmes nada.',
        how_p2='Esa lista es el punto: la mayoría de la gente nunca ha visto lo que viaja junto con una foto de teléfono. Un JPEG típico lleva el modelo exacto del dispositivo, el segundo en que se disparó el obturador, el software de edición usado, y, si la ubicación estaba activada, coordenadas GPS lo suficientemente precisas como para identificar una casa. Publicar una foto original publica todo eso junto con ella.',
        how_p3='El paso de limpieza es hermosamente contundente. La imagen se dibuja en un <code>&lt;canvas&gt;</code> fresco y se vuelve a exportar con <code>canvas.toBlob()</code>, que por diseño solo escribe datos de píxeles: EXIF, XMP, perfiles ICC, miniaturas, todo eso simplemente no tiene a dónde ir en el archivo nuevo. Nada se elimina selectivamente, así que nada puede pasarse por alto. La única contrapartida es que los JPEG se vuelven a codificar (a calidad 0.95, visualmente indistinguible para fotos), y se descartaría un perfil de color personalizado. Los archivos PNG y WebP rara vez llevan EXIF pero pueden contener fragmentos de texto y perfiles; el mismo redibujado también los elimina.',
        how_p4='Tanto la inspección a nivel de byte como la recodificación con canvas se ejecutan en tu pestaña. Observa el panel Red de las DevTools mientras cargas y limpias una foto: la imagen nunca se sube a ningún lado, que es exactamente lo que quieres de una herramienta cuyo único trabajo es proteger tus metadatos.',
    ),
    related_tools=[
        ("compress-image.html", "Comprimir imagen", "Reduce el tamaño del archivo después de limpiar."),
        ("image-converter.html", "Conversor de imágenes", "Convierte a un formato diferente."),
        ("watermark-image.html", "Marca de agua en imagen", "Añade una marca de agua de texto para proteger tus fotos."),
    ],
)

PAGES["zh"] = dict(
    title="删除图片元数据：清除 EXIF 和 GPS 数据 | norito",
    meta_desc="在浏览器中删除照片中的 EXIF、GPS 位置及其他隐藏元数据。在清除之前先查看发现了哪些信息。不上传任何内容。",
    app_name="删除元数据", h1="删除元数据", breadcrumb_label="删除元数据",
    lede="清除照片中的 EXIF、GPS 位置、相机信息和时间戳。在删除之前先准确查看嵌入了哪些信息。",
    t=dict(
        dz_click="点击选择一张图片", dz_drag="，或将其拖放到此处",
        dz_hint="JPG 格式最适合读取现有元数据。同样支持 PNG/WebP。文件保留在你的设备上。",
        remove_download="删除元数据并下载",
        cleaned_alt="已清理的图片", preview_hint="生成后，清理后的图片会显示在这里。",
        side_note="手机和相机拍摄的照片通常会嵌入 EXIF 数据：拍摄时的精确 GPS 坐标、相机或手机型号，以及时间戳。该工具会先读取你文件中实际存在的信息，然后通过从头重新编码图片来清除所有这些数据。",
        how_h2="工作原理",
        how_p1='当你拖入一张 JPEG 图片时，工具会用 <code>DataView</code> 读取文件的原始字节，并遍历 JPEG 标记结构以寻找 APP1 分段，EXIF 数据就存放在那里。在其内部，工具会解析 TIFF 目录树：IFD0（相机品牌和型号、软件、修改日期）、Exif 子目录（原始拍摄时间、曝光、光圈、ISO），以及 GPS 子目录。它可以处理两种字节序（Intel 和 Motorola 风格的文件）以及内联和偏移存储两种值的方式，然后在你确认操作之前，向你展示一份找到内容的清晰列表。',
        how_p2='这份列表正是关键所在：大多数人从未见过一张手机照片中都携带了哪些信息。一张典型的 JPEG 照片会携带确切的设备型号、快门按下的具体秒数、使用的编辑软件，以及——如果开启了定位——精确到足以识别某栋房子的 GPS 坐标。发布一张原始照片，也就等于把这一切都一并发布了出去。',
        how_p3='清理步骤简单粗暴，效果极佳。图片会被绘制到一个全新的 <code>&lt;canvas&gt;</code> 上，并通过 <code>canvas.toBlob()</code> 重新导出，按设计该方法只写入像素数据：EXIF、XMP、ICC 配置文件、缩略图，这一切在新文件中根本没有存放的地方。没有任何内容是被选择性删除的，因此也不会有遗漏。唯一的取舍是 JPEG 会被重新编码（质量为 0.95，在照片上视觉上几乎无法察觉差异），并且自定义颜色配置文件会被丢弃。PNG 和 WebP 文件很少携带 EXIF，但可能包含文本块和配置文件；同样的重绘过程也会一并清除这些内容。',
        how_p4='字节级检查和 canvas 重新编码都在你的标签页中运行。在加载和清理照片时打开开发者工具的 Network 面板看看：图片从未被上传到任何地方，而这正是一个专门用于保护你元数据的工具所应该做到的。',
    ),
    related_tools=[
        ("compress-image.html", "压缩图片", "清理后缩小文件大小。"),
        ("image-converter.html", "图片格式转换器", "转换为不同的格式。"),
        ("watermark-image.html", "图片水印", "添加文字水印以保护你的照片。"),
    ],
)

PAGES["ar"] = dict(
    title="إزالة بيانات الصورة الوصفية: امسح EXIF وGPS | norito",
    meta_desc="أزل EXIF وموقع GPS وبيانات وصفية مخفية أخرى من صورة، مباشرة في متصفحك. شاهد ما وُجد قبل إزالته. لا شيء يُرفَع.",
    app_name="إزالة البيانات الوصفية", h1="إزالة البيانات الوصفية", breadcrumb_label="إزالة البيانات الوصفية",
    lede="امسح EXIF وموقع GPS ومعلومات الكاميرا والطوابع الزمنية من صورة. شاهد بالضبط ما هو مضمَّن قبل إزالته.",
    t=dict(
        dz_click="انقر لاختيار صورة", dz_drag="، أو اسحبها وأفلتها هنا",
        dz_hint="يعمل JPG بشكل أفضل لقراءة البيانات الوصفية الموجودة. PNG/WebP مدعومان أيضًا. تبقى على جهازك.",
        remove_download="إزالة البيانات الوصفية والتنزيل",
        cleaned_alt="صورة نظيفة", preview_hint="ستظهر صورتك النظيفة هنا بمجرد إنشائها.",
        side_note="غالبًا ما تُضمِّن صور الهواتف والكاميرات بيانات EXIF: إحداثيات GPS الدقيقة لمكان الالتقاط، وطراز الكاميرا أو الهاتف، وطابعًا زمنيًا. تقرأ هذه الأداة أولًا ما هو موجود فعليًا في ملفك، ثم تزيل كل ذلك بإعادة ترميز الصورة من الصفر.",
        how_h2="كيف يعمل",
        how_p1='عندما تُسقِط ملف JPEG، تقرأ الأداة البايتات الخام للملف بواسطة <code>DataView</code> وتمرّ عبر بنية علامات JPEG بحثًا عن مقطع APP1، حيث يعيش EXIF. في الداخل، تحلّل شجرة دليل TIFF: IFD0 (ماركة وطراز الكاميرا، البرنامج، تاريخ التعديل)، دليل Exif الفرعي (وقت الالتقاط الأصلي، التعريض، الفتحة، ISO)، ودليل GPS الفرعي. تتعامل مع كلا ترتيبي البايت (ملفات بأسلوب Intel وMotorola) والقيم المضمَّنة والمخزَّنة بإزاحة، ثم تعرض لك قائمة بسيطة بما وجدته قبل أن تلتزم بأي شيء.',
        how_p2='تلك القائمة هي بيت القصيد: معظم الناس لم يروا أبدًا ما يرافق صورة الهاتف. يحمل ملف JPEG نموذجي طراز الجهاز الدقيق، واللحظة التي فُتِّح فيها الغالق، وبرنامج التحرير المستخدَم، وإذا كان الموقع مفعّلًا، إحداثيات GPS دقيقة بما يكفي لتحديد منزل. نشر صورة أصلية يعني نشر كل ذلك معها.',
        how_p3='خطوة التنظيف صريحة بشكل رائع. تُرسَم الصورة على <code>&lt;canvas&gt;</code> جديد وتُعاد تصديرها بـ <code>canvas.toBlob()</code>، التي تكتب بيانات البكسل فقط بالتصميم: EXIF وXMP وملفات ICC والصور المصغَّرة، كل ذلك ببساطة لا مكان له في الملف الجديد. لا يُحذَف شيء بشكل انتقائي، لذا لا يمكن تفويت أي شيء. المفاضلة الوحيدة هي أن ملفات JPEG تُعاد ترميزها (بجودة 0.95، لا تُميَّز بصريًا للصور)، وسيُتخلَّص من ملف تعريف لون مخصص. نادرًا ما تحمل ملفات PNG وWebP بيانات EXIF لكن يمكن أن تحتوي على أجزاء نصية وملفات تعريف؛ نفس عملية إعادة الرسم تزيل تلك أيضًا.',
        how_p4='يعمل كل من الفحص على مستوى البايت وإعادة ترميز canvas في تبويبك. راقب لوحة Network في أدوات المطوّر أثناء تحميل وتنظيف صورة: لا تُرفَع الصورة أبدًا إلى أي مكان، وهذا بالضبط ما تريده من أداة مهمتها الوحيدة هي حماية بياناتك الوصفية.',
    ),
    related_tools=[
        ("compress-image.html", "ضغط الصور", "قلّص حجم الملف بعد التنظيف."),
        ("image-converter.html", "محول الصور", "حوّل إلى تنسيق مختلف."),
        ("watermark-image.html", "علامة مائية على الصورة", "أضف علامة مائية نصية لحماية صورك."),
    ],
)

PAGES["hi"] = dict(
    title="इमेज मेटाडेटा हटाएं: EXIF और GPS डेटा हटाएं | norito",
    meta_desc="अपने ब्राउज़र में ही किसी फ़ोटो से EXIF, GPS लोकेशन, और अन्य छिपा हुआ मेटाडेटा हटाएं। हटाने से पहले देखें कि क्या मिला। कुछ भी अपलोड नहीं होता।",
    app_name="मेटाडेटा हटाएं", h1="मेटाडेटा हटाएं", breadcrumb_label="मेटाडेटा हटाएं",
    lede="किसी फ़ोटो से EXIF, GPS लोकेशन, कैमरा जानकारी, और टाइमस्टैंप्स हटाएं। हटाने से पहले देखें कि बिल्कुल क्या एम्बेडेड है।",
    t=dict(
        dz_click="इमेज चुनने के लिए क्लिक करें", dz_drag=", या इसे यहां ड्रैग करके ड्रॉप करें",
        dz_hint="मौजूदा मेटाडेटा पढ़ने के लिए JPG सबसे अच्छा काम करता है। PNG/WebP भी सपोर्टेड हैं। आपकी डिवाइस पर ही रहता है।",
        remove_download="मेटाडेटा हटाएं और डाउनलोड करें",
        cleaned_alt="साफ़ की गई इमेज", preview_hint="जनरेट होने के बाद आपकी साफ़ की गई इमेज यहां दिखेगी।",
        side_note="फ़ोन और कैमरों की फ़ोटोज़ अक्सर EXIF डेटा एम्बेड करती हैं: वह सटीक GPS कोऑर्डिनेट्स जहां वह ली गई, कैमरा या फ़ोन मॉडल, और एक टाइमस्टैंप। यह पहले आपकी फ़ाइल में असल में जो है उसे पढ़ता है, फिर इमेज को स्क्रैच से री-एनकोड करके यह सब कुछ हटा देता है।",
        how_h2="यह कैसे काम करता है",
        how_p1='जब आप एक JPEG डालते हैं, टूल <code>DataView</code> से फ़ाइल की रॉ बाइट्स पढ़ता है और APP1 सेगमेंट की तलाश में JPEG मार्कर स्ट्रक्चर से गुज़रता है, जहां EXIF रहता है। इसके अंदर यह TIFF डायरेक्टरी ट्री पार्स करता है: IFD0 (कैमरा मेक और मॉडल, सॉफ़्टवेयर, मॉडिफ़िकेशन डेट), Exif सब-डायरेक्टरी (ओरिजिनल कैप्चर टाइम, एक्सपोज़र, अपर्चर, ISO), और GPS सब-डायरेक्टरी। यह दोनों बाइट ऑर्डर्स (Intel और Motorola स्टाइल फ़ाइलें) और इनलाइन और ऑफ़सेट-स्टोर्ड दोनों वैल्यूज़ को हैंडल करता है, फिर आपको कमिट करने से पहले जो मिला उसकी एक सादी लिस्ट दिखाता है।',
        how_p2="वह लिस्ट ही पूरी बात है: ज़्यादातर लोगों ने कभी नहीं देखा कि फ़ोन फ़ोटो के साथ क्या-क्या चलता है। एक टिपिकल JPEG में एग्ज़ैक्ट डिवाइस मॉडल, शटर चलने का ठीक वह सेकंड, इस्तेमाल किया गया एडिटिंग सॉफ़्टवेयर, और, अगर लोकेशन ऑन थी, तो एक घर की पहचान कर सकने लायक सटीक GPS कोऑर्डिनेट्स होते हैं। एक ओरिजिनल फ़ोटो पोस्ट करने का मतलब है यह सब कुछ भी उसके साथ पोस्ट करना।",
        how_p3="क्लीनिंग स्टेप ख़ूबसूरती से बेधड़क है। इमेज को एक फ़्रेश <code>&lt;canvas&gt;</code> पर ड्रॉ किया जाता है और <code>canvas.toBlob()</code> से री-एक्सपोर्ट किया जाता है, जो डिज़ाइन के हिसाब से सिर्फ़ पिक्सल डेटा लिखता है: EXIF, XMP, ICC प्रोफ़ाइल्स, थंबनेल्स, इन सबके पास नई फ़ाइल में जाने की कोई जगह ही नहीं होती। कुछ भी सिलेक्टिवली डिलीट नहीं किया जाता, इसलिए कुछ भी मिस नहीं हो सकता। एक ट्रेडऑफ़ यह है कि JPEGs री-एनकोड होते हैं (0.95 क्वालिटी पर, फ़ोटोज़ के लिए विज़ुअली अंतर न दिखने लायक), और एक कस्टम कलर प्रोफ़ाइल हट जाएगी। PNG और WebP फ़ाइलें शायद ही कभी EXIF ले जाती हैं लेकिन टेक्स्ट चंक्स और प्रोफ़ाइल्स रख सकती हैं; वही रीड्रॉ उन्हें भी हटा देता है।",
        how_p4="बाइट-लेवल इंस्पेक्शन और canvas री-एनकोड दोनों आपके टैब में चलते हैं। किसी फ़ोटो को लोड और क्लीन करते समय डेवटूल्स का Network पैनल देखें: इमेज कभी कहीं भी अपलोड नहीं होती, जो बिल्कुल वही है जो आप एक ऐसे टूल से चाहते हैं जिसका पूरा काम ही आपके मेटाडेटा की सुरक्षा करना है।",
    ),
    related_tools=[
        ("compress-image.html", "इमेज कंप्रेस करें", "साफ़ करने के बाद फ़ाइल साइज़ छोटा करें।"),
        ("image-converter.html", "इमेज कन्वर्टर", "किसी दूसरे फ़ॉर्मैट में कन्वर्ट करें।"),
        ("watermark-image.html", "इमेज पर वॉटरमार्क", "अपनी फ़ोटोज़ को प्रोटेक्ट करने के लिए एक टेक्स्ट वॉटरमार्क जोड़ें।"),
    ],
)

PAGES["ru"] = dict(
    title="Удаление метаданных изображения: очистка EXIF и GPS | norito",
    meta_desc="Удалите EXIF, GPS-координаты и другие скрытые метаданные из фото прямо в браузере. Посмотрите, что найдено, прежде чем удалять. Ничего не загружается.",
    app_name="Удаление метаданных", h1="Удаление метаданных", breadcrumb_label="Удаление метаданных",
    lede="Удалите EXIF, GPS-координаты, информацию о камере и метки времени из фото. Точно узнайте, что встроено, прежде чем удалять.",
    t=dict(
        dz_click="Нажмите, чтобы выбрать изображение", dz_drag=", или перетащите его сюда",
        dz_hint="JPG лучше всего подходит для чтения существующих метаданных. PNG/WebP также поддерживаются. Остаётся на вашем устройстве.",
        remove_download="Удалить метаданные и скачать",
        cleaned_alt="Очищенное изображение", preview_hint="Очищенное изображение появится здесь после создания.",
        side_note="Фото с телефонов и камер часто содержат встроенные EXIF-данные: точные GPS-координаты места съёмки, модель камеры или телефона и метку времени. Инструмент сначала считывает, что действительно есть в вашем файле, а затем удаляет всё это, полностью перекодируя изображение с нуля.",
        how_h2="Как это работает",
        how_p1='Когда вы добавляете JPEG, инструмент считывает необработанные байты файла с помощью <code>DataView</code> и проходит по структуре маркеров JPEG в поисках сегмента APP1, где хранится EXIF. Внутри он разбирает дерево каталогов TIFF: IFD0 (марка и модель камеры, программное обеспечение, дата изменения), подкаталог Exif (время оригинальной съёмки, экспозиция, диафрагма, ISO) и подкаталог GPS. Он обрабатывает оба порядка байтов (файлы в стиле Intel и Motorola) и как встроенные, так и хранимые со смещением значения, а затем показывает вам простой список найденного, прежде чем вы что-либо подтвердите.',
        how_p2="Этот список — вся суть: большинство людей никогда не видели, что путешествует вместе с телефонным фото. Типичный JPEG несёт точную модель устройства, секунду срабатывания затвора, использованное программное обеспечение для редактирования и, если геолокация была включена, GPS-координаты, достаточно точные, чтобы определить конкретный дом. Публикуя оригинальное фото, вы публикуете всё это вместе с ним.",
        how_p3="Этап очистки прекрасно прямолинеен. Изображение отрисовывается на новом <code>&lt;canvas&gt;</code> и повторно экспортируется через <code>canvas.toBlob()</code>, который по своей природе записывает только пиксельные данные: EXIF, XMP, ICC-профили, миниатюры — всему этому просто негде оказаться в новом файле. Ничего не удаляется выборочно, поэтому ничего не может быть пропущено. Единственный компромисс — JPEG-файлы перекодируются (с качеством 0.95, визуально неотличимо для фотографий), а пользовательский цветовой профиль будет отброшен. Файлы PNG и WebP редко содержат EXIF, но могут хранить текстовые блоки и профили; тот же процесс перерисовки удаляет и их.",
        how_p4="И проверка на уровне байтов, и повторное кодирование canvas выполняются в вашей вкладке. Понаблюдайте за панелью Network в DevTools во время загрузки и очистки фото: изображение никогда никуда не загружается, что именно и требуется от инструмента, единственная задача которого — защита ваших метаданных.",
    ),
    related_tools=[
        ("compress-image.html", "Сжатие изображения", "Уменьшите размер файла после очистки."),
        ("image-converter.html", "Конвертер изображений", "Конвертируйте в другой формат."),
        ("watermark-image.html", "Водяной знак на изображении", "Добавьте текстовый водяной знак для защиты ваших фото."),
    ],
)

PAGES["ja"] = dict(
    title="画像のメタデータ削除：EXIFとGPSデータを消去 | norito",
    meta_desc="ブラウザ内で写真からEXIF、GPS位置情報、その他の隠されたメタデータを削除。削除前に何が見つかったか確認できます。アップロードなし。",
    app_name="メタデータを削除", h1="メタデータを削除", breadcrumb_label="メタデータを削除",
    lede="写真からEXIF、GPS位置情報、カメラ情報、タイムスタンプを消去します。削除する前に、何が埋め込まれているか正確に確認できます。",
    t=dict(
        dz_click="クリックして画像を選択", dz_drag="、またはここにドラッグ＆ドロップ",
        dz_hint="既存のメタデータを読み取るにはJPGが最も適しています。PNG/WebPにも対応。デバイス内にとどまります。",
        remove_download="メタデータを削除してダウンロード",
        cleaned_alt="クリーンにされた画像", preview_hint="生成されると、クリーンにされた画像がここに表示されます。",
        side_note="スマートフォンやカメラの写真には、撮影された正確なGPS座標、カメラやスマートフォンの機種、タイムスタンプなどのEXIFデータがよく埋め込まれています。このツールはまずファイルに実際に含まれている内容を読み取り、その後画像をゼロから再エンコードすることですべてを消去します。",
        how_h2="仕組み",
        how_p1='JPEGをドロップすると、ツールは<code>DataView</code>でファイルの生バイトを読み取り、EXIFが格納されているAPP1セグメントを探してJPEGのマーカー構造をたどります。その内部では、TIFFディレクトリツリーを解析します。IFD0（カメラのメーカーとモデル、ソフトウェア、更新日時）、Exifサブディレクトリ（実際の撮影時刻、露出、絞り、ISO）、GPSサブディレクトリです。両方のバイト順（IntelスタイルとMotorolaスタイルのファイル）と、インライン値・オフセット格納値の両方を処理し、何かを確定する前に見つかった内容をシンプルなリストとして表示します。',
        how_p2="そのリストこそが重要なポイントです。ほとんどの人は、スマートフォンの写真に何が同梱されているかを見たことがありません。典型的なJPEGには、正確な機種名、シャッターが切られた瞬間の時刻、使用された編集ソフトウェア、そして位置情報がオンになっていれば家を特定できるほど正確なGPS座標が含まれています。オリジナルの写真を投稿するということは、それらすべてを一緒に投稿することを意味します。",
        how_p3="クリーニングのステップは見事なまでに単純明快です。画像は新しい<code>&lt;canvas&gt;</code>に描画され、<code>canvas.toBlob()</code>で再エクスポートされます。これは設計上ピクセルデータのみを書き出すため、EXIF、XMP、ICCプロファイル、サムネイルなど、それらすべてが新しいファイルの中に単純に入り込む余地がありません。何かを選択的に削除するわけではないので、見落としも起こり得ません。唯一のトレードオフは、JPEGが再エンコードされること（品質0.95で、写真では視覚的に区別がつきません）と、カスタムのカラープロファイルが失われることです。PNGとWebPファイルはEXIFを持つことはまれですが、テキストチャンクやプロファイルを保持することがあり、同じ再描画処理でそれらも削除されます。",
        how_p4="バイトレベルの検査もcanvasの再エンコードも、すべてあなたのタブ内で実行されます。写真を読み込んでクリーンにする間、DevToolsのNetworkパネルを見てみてください。画像はどこにもアップロードされません。これはメタデータを守ることだけを目的としたツールにとって、まさに求められる動作です。",
    ),
    related_tools=[
        ("compress-image.html", "画像を圧縮", "クリーニング後にファイルサイズを縮小。"),
        ("image-converter.html", "画像コンバーター", "別の形式に変換。"),
        ("watermark-image.html", "画像に透かしを追加", "写真を保護するためのテキスト透かしを追加。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "remove-metadata.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-remove-metadata.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/remove-metadata.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
