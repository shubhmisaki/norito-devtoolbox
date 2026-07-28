#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/></svg>'
ICON_CLASS = "c-teal"

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

        <div class="field" style="margin-top:20px;">
          <label for="format">{t['convert_to']}</label>
          <select id="format">
            <option value="jpeg">JPEG</option>
            <option value="png">PNG</option>
            <option value="webp">WebP</option>
          </select>
        </div>
        <div class="field-row" id="qualityRow">
          <div class="field" style="flex:1;">
            <label for="quality">{t['quality']}: <span id="qualityValue">92%</span></label>
            <input type="range" id="quality" class="slider" min="10" max="100" value="92" />
          </div>
        </div>

        <button id="convertBtn" disabled style="margin-top:8px;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/></svg>
          {t['convert_image']}
        </button>
        <div class="result-box" id="result" style="display:none;"></div>

        <div class="batch-file-list" id="batchList" style="display:none;"></div>
        <div class="batch-actions" id="batchActions" style="display:none;">
          <button type="button" id="batchConvertBtn">{t['convert_all']}</button>
          <button type="button" class="secondary" id="batchZipBtn" disabled>{t['download_zip']}</button>
        </div>
      </div>

      <div>
        <div class="panel" style="text-align:center;">
          <img class="preview" id="preview" style="display:none; max-width:100%;" alt="{t['converted_preview_alt']}" />
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
    </div>
'''

PAGES = {}

PAGES["es"] = dict(
    title="Conversor de Imágenes: JPG, PNG, WebP Online | norito",
    meta_desc="Convierte imágenes entre JPG, PNG, y WebP, en tu navegador. Calidad ajustable, no se sube nada.",
    app_name="Conversor de Imágenes", h1="Conversor de Imágenes", breadcrumb_label="Conversor de Imágenes",
    lede="Convierte una imagen entre JPG, PNG, y WebP. Calidad ajustable para formatos con pérdida, todo ocurre en tu dispositivo.",
    note_html='¿Solo convirtiendo JPG a PNG? Prueba la <a href="/jpg-to-png-converter.html">página dedicada de JPG a PNG</a>.',
    t=dict(
        dz_click="Haz clic para elegir una imagen", dz_drag=", o arrástrala aquí",
        dz_hint="JPG, PNG, WebP. Se queda en tu dispositivo, no se sube nada. Selecciona varias para convertir en lote.",
        convert_to="Convertir a", quality="Calidad",
        convert_image="Convertir imagen", convert_all="Convertir todas", download_zip="Descargar todo como .zip",
        converted_preview_alt="Vista previa convertida", preview_hint="Tu imagen convertida aparecerá aquí una vez generada.",
        side_note="PNG no tiene pérdida (archivos más grandes, admite transparencia). JPEG y WebP tienen pérdida con un control deslizante de calidad (archivos más pequeños, sin transparencia para JPEG). WebP suele superar a JPEG a la misma calidad visual, pero JPEG tiene la mayor compatibilidad.",
        how_h2="Cómo funciona",
        how_p1="Tu imagen se carga a través de una URL de objeto local (<code>URL.createObjectURL</code>), se decodifica con el propio decodificador de imágenes del navegador, se dibuja en un canvas fuera de pantalla a su resolución natural completa, y se vuelve a codificar con <code>canvas.toBlob</code> en el formato y calidad que elegiste. Un detalle que se maneja por ti: JPEG no tiene canal alfa, así que antes de dibujar, el canvas se rellena de blanco cuando JPEG es el destino. Sin ese paso, las áreas transparentes de un PNG saldrían negras. El control de calidad solo aplica a JPEG y WebP; la codificación PNG no tiene pérdida y lo ignora.",
        how_p2="Un efecto secundario del ida y vuelta por canvas que vale la pena conocer en cualquier caso: la salida solo contiene píxeles. Los metadatos EXIF, el modelo de cámara, las marcas de tiempo, y las coordenadas GPS incrustadas de las fotos de teléfono no sobreviven a la recodificación. Eso convierte a este conversor en una ganancia silenciosa de privacidad antes de compartir una foto públicamente, y algo a tener en cuenta si realmente necesitabas los metadatos (conserva el original en ese caso). Los navegadores aplican el indicador de orientación EXIF al decodificar, así que las fotos de teléfono tomadas de lado siguen saliendo correctamente rotadas.",
        how_p3="La conversión, el modo por lotes, e incluso el empaquetado en .zip (ensamblado byte a byte en JavaScript) se ejecutan todos en tu navegador. Abre la pestaña Red de las DevTools y convierte algo: ninguna petición transporta la imagen, por eso tampoco hay límite de tamaño de archivo más allá de la memoria de tu máquina.",
    ),
    related_tools=[
        ("compress-image.html", "Comprimir imagen", "Consigue un tamaño de archivo exacto después de convertir."),
        ("resize-image.html", "Redimensionar imagen", "Cambia las dimensiones antes o después de convertir el formato."),
        ("remove-metadata.html", "Eliminar metadatos", "Elimina EXIF y datos de ubicación de una foto."),
    ],
)

PAGES["zh"] = dict(
    title="图片格式转换器：在线转换 JPG、PNG、WebP | norito",
    meta_desc="在浏览器中于 JPG、PNG、WebP 格式之间转换图片。质量可调，不上传任何内容。",
    app_name="图片格式转换器", h1="图片格式转换器", breadcrumb_label="图片格式转换器",
    lede="在 JPG、PNG、WebP 之间转换图片格式。有损格式支持调节质量，全部过程都在你的设备上完成。",
    note_html='只想把 JPG 转成 PNG？试试 <a href="/jpg-to-png-converter.html">JPG 转 PNG 专用页面</a>。',
    t=dict(
        dz_click="点击选择一张图片", dz_drag="，或将其拖放到此处",
        dz_hint="支持 JPG、PNG、WebP。文件保留在你的设备上，不会上传任何内容。可多选进行批量转换。",
        convert_to="转换为", quality="质量",
        convert_image="转换图片", convert_all="全部转换", download_zip="以 .zip 下载全部",
        converted_preview_alt="转换后预览", preview_hint="生成后，转换后的图片会显示在这里。",
        side_note="PNG 无损（文件更大，支持透明度）。JPEG 和 WebP 有损，可通过滑块调节质量（文件更小，JPEG 不支持透明度）。在同等视觉质量下，WebP 通常优于 JPEG，但 JPEG 的兼容性最广。",
        how_h2="工作原理",
        how_p1="你的图片通过本地对象 URL（<code>URL.createObjectURL</code>）加载，由浏览器自身的图像解码器解码，以其完整的原始分辨率绘制到一个离屏 canvas 上，然后通过 <code>canvas.toBlob</code> 按你选择的格式和质量重新编码。有一个细节已经为你处理好了：JPEG 没有 alpha 通道，因此在绘制之前，如果目标格式是 JPEG，canvas 会先填充为白色。如果没有这一步，PNG 中的透明区域在转换后会变成黑色。质量滑块只对 JPEG 和 WebP 生效；PNG 编码是无损的，会忽略该设置。",
        how_p2="canvas 往返处理还有一个值得了解的附带效应：输出结果只包含像素信息。手机照片中的 EXIF 元数据、相机型号、时间戳以及嵌入的 GPS 坐标都不会在重新编码后保留下来。这使得该转换工具在公开分享照片之前，无形中带来了隐私上的好处；但如果你确实需要这些元数据，就要注意这一点（这种情况下请保留原图）。浏览器在解码时会应用 EXIF 方向标记，因此侧拍的手机照片经过转换后仍会正确旋转显示。",
        how_p3="转换、批量模式，甚至 .zip 打包（在 JavaScript 中逐字节组装）都在你的浏览器中运行完成。打开开发者工具的 Network 标签页并转换一张图片试试：不会有任何请求携带该图片，这也是为什么除了你设备本身的内存限制外，没有其他文件大小上限。",
    ),
    related_tools=[
        ("compress-image.html", "压缩图片", "转换后达到精确的文件大小目标。"),
        ("resize-image.html", "调整图片尺寸", "在转换格式前后更改尺寸。"),
        ("remove-metadata.html", "删除元数据", "从照片中清除 EXIF 和位置信息。"),
    ],
)

PAGES["ar"] = dict(
    title="محول الصور: JPG وPNG وWebP أونلاين | norito",
    meta_desc="حوّل الصور بين JPG وPNG وWebP، مباشرة في متصفحك. جودة قابلة للتعديل، لا شيء يُرفَع.",
    app_name="محول الصور", h1="محول الصور", breadcrumb_label="محول الصور",
    lede="حوّل صورة بين JPG وPNG وWebP. جودة قابلة للتعديل للتنسيقات ذات الفقدان، كل شيء يحدث على جهازك.",
    note_html='هل تحوّل JPG إلى PNG فقط؟ جرّب <a href="/jpg-to-png-converter.html">صفحة JPG إلى PNG المخصصة</a>.',
    t=dict(
        dz_click="انقر لاختيار صورة", dz_drag="، أو اسحبها وأفلتها هنا",
        dz_hint="JPG وPNG وWebP. تبقى على جهازك، لا شيء يُرفَع. اختر عدة صور للتحويل بالجملة.",
        convert_to="تحويل إلى", quality="الجودة",
        convert_image="تحويل الصورة", convert_all="تحويل الكل", download_zip="تنزيل الكل كملف .zip",
        converted_preview_alt="معاينة محوَّلة", preview_hint="ستظهر صورتك المحوَّلة هنا بمجرد إنشائها.",
        side_note="PNG بدون فقدان (ملفات أكبر، يدعم الشفافية). JPEG وWebP بفقدان مع منزلق جودة (ملفات أصغر، بلا شفافية لـ JPEG). عادةً ما يتفوّق WebP على JPEG بنفس الجودة البصرية، لكن JPEG يتمتع بأوسع توافق.",
        how_h2="كيف يعمل",
        how_p1='تُحمَّل صورتك عبر رابط كائن محلي (<code>URL.createObjectURL</code>)، ويُفكّ ترميزها بواسطة مُفكِّك ترميز الصور الخاص بالمتصفح نفسه، وتُرسَم على canvas خارج الشاشة بدقتها الطبيعية الكاملة، وتُعاد ترميزها بـ <code>canvas.toBlob</code> بالتنسيق والجودة اللذين اخترتهما. تفصيل واحد يُدار من أجلك: JPEG ليس لديه قناة ألفا، لذا قبل الرسم، تُملَأ اللوحة بالأبيض عندما يكون JPEG هو الهدف. بدون تلك الخطوة، ستخرج المناطق الشفافة من PNG سوداء. ينطبق منزلق الجودة فقط على JPEG وWebP؛ ترميز PNG بدون فقدان ويتجاهله.',
        how_p2="أثر جانبي لجولة canpas ذهابًا وإيابًا يستحق المعرفة على أي حال: يحتوي الإخراج على بكسلات فقط. بيانات EXIF الوصفية، وطراز الكاميرا، والطوابع الزمنية، وإحداثيات GPS المضمَّنة من صور الهاتف، لا تنجو من إعادة الترميز. هذا يجعل هذه الأداة مكسبًا هادئًا للخصوصية قبل مشاركة صورة علنًا، وأمرًا يجب الانتباه إليه إذا كنت بحاجة فعلية للبيانات الوصفية (احتفظ بالأصل في تلك الحالة). تطبّق المتصفحات علامة اتجاه EXIF أثناء فك الترميز، لذا لا تزال صور الهاتف الملتقطة بشكل مائل تخرج مُدارة بشكل صحيح.",
        how_p3="التحويل، ووضع الدُفعة، وحتى تجميع .zip (المُجمَّع بايتًا بايتًا في جافاسكريبت) كلها تعمل في متصفحك. افتح لسان Network في أدوات المطوّر وحوّل شيئًا ما: لا يحمل أي طلب الصورة، ولهذا لا يوجد حد لحجم الملف يتجاوز ذاكرة جهازك.",
    ),
    related_tools=[
        ("compress-image.html", "ضغط الصور", "احصل على حجم ملف دقيق بعد التحويل."),
        ("resize-image.html", "تغيير حجم الصورة", "غيّر الأبعاد قبل أو بعد تحويل التنسيق."),
        ("remove-metadata.html", "إزالة البيانات الوصفية", "أزل بيانات EXIF والموقع من صورة."),
    ],
)

PAGES["hi"] = dict(
    title="इमेज कन्वर्टर: JPG, PNG, WebP ऑनलाइन | norito",
    meta_desc="अपने ब्राउज़र में ही JPG, PNG, और WebP के बीच इमेजेज़ कन्वर्ट करें। एडजस्टेबल क्वालिटी, कुछ भी अपलोड नहीं होता।",
    app_name="इमेज कन्वर्टर", h1="इमेज कन्वर्टर", breadcrumb_label="इमेज कन्वर्टर",
    lede="JPG, PNG, और WebP के बीच एक इमेज कन्वर्ट करें। लॉसी फ़ॉर्मैट्स के लिए एडजस्टेबल क्वालिटी, सब कुछ आपकी डिवाइस पर होता है।",
    note_html='सिर्फ़ JPG को PNG में कन्वर्ट कर रहे हैं? <a href="/jpg-to-png-converter.html">डेडिकेटेड JPG से PNG पेज</a> ट्राई करें।',
    t=dict(
        dz_click="इमेज चुनने के लिए क्लिक करें", dz_drag=", या इसे यहां ड्रैग करके ड्रॉप करें",
        dz_hint="JPG, PNG, WebP। आपकी डिवाइस पर ही रहता है, कुछ भी अपलोड नहीं होता। बैच कन्वर्ट करने के लिए कई चुनें।",
        convert_to="इसमें कन्वर्ट करें", quality="क्वालिटी",
        convert_image="इमेज कन्वर्ट करें", convert_all="सभी कन्वर्ट करें", download_zip="सभी को .zip के रूप में डाउनलोड करें",
        converted_preview_alt="कन्वर्ट किया गया प्रीव्यू", preview_hint="जनरेट होने के बाद आपकी कन्वर्ट की गई इमेज यहां दिखेगी।",
        side_note="PNG लॉसलेस है (बड़ी फ़ाइलें, ट्रांसपेरेंसी सपोर्ट करता है)। JPEG और WebP क्वालिटी स्लाइडर के साथ लॉसी हैं (छोटी फ़ाइलें, JPEG के लिए कोई ट्रांसपेरेंसी नहीं)। WebP आमतौर पर उसी विज़ुअल क्वालिटी पर JPEG से बेहतर होता है, लेकिन JPEG की कम्पैटिबिलिटी सबसे ज़्यादा है।",
        how_h2="यह कैसे काम करता है",
        how_p1='आपकी इमेज एक लोकल ऑब्जेक्ट URL (<code>URL.createObjectURL</code>) के ज़रिए लोड होती है, ब्राउज़र के अपने इमेज डिकोडर से डिकोड होती है, अपनी पूरी नैचुरल रिज़ॉल्यूशन पर एक ऑफ़स्क्रीन canvas पर ड्रॉ की जाती है, और आपके चुने हुए फ़ॉर्मैट और क्वालिटी में <code>canvas.toBlob</code> से री-एनकोड होती है। एक डिटेल जो आपके लिए हैंडल की जाती है: JPEG के पास कोई अल्फ़ा चैनल नहीं होता, इसलिए ड्रॉ करने से पहले, जब JPEG टारगेट होता है तो canvas सफ़ेद रंग से भरा जाता है। उस स्टेप के बिना, किसी PNG के ट्रांसपेरेंट एरिया काले निकलते। क्वालिटी स्लाइडर सिर्फ़ JPEG और WebP पर लागू होता है; PNG एनकोडिंग लॉसलेस है और इसे इग्नोर करती है।',
        how_p2="canvas राउंड-ट्रिप का एक साइड इफ़ेक्ट जो जानने लायक है वैसे भी: आउटपुट में सिर्फ़ पिक्सल्स होते हैं। EXIF मेटाडेटा, कैमरा मॉडल, टाइमस्टैंप्स, और फ़ोन फ़ोटोज़ से एम्बेडेड GPS कोऑर्डिनेट्स, री-एनकोडिंग में नहीं बचते। यह इस कन्वर्टर को किसी फ़ोटो को पब्लिकली शेयर करने से पहले एक क्वाइट प्राइवेसी विन बना देता है, और अगर आपको वाक़ई मेटाडेटा चाहिए था तो जानने लायक बात (उस स्थिति में ओरिजिनल रखें)। ब्राउज़र्स डिकोड करते समय EXIF ओरिएंटेशन फ़्लैग अप्लाई करते हैं, इसलिए साइडवेज़-शॉट फ़ोन फ़ोटोज़ अभी भी सही ढंग से रोटेटेड निकलती हैं।",
        how_p3="कन्वर्जन, बैच मोड, और यहां तक कि .zip बंडलिंग (JavaScript में बाइट-बाइट असेंबल की गई) सब कुछ आपके ब्राउज़र में चलता है। डेवटूल्स का Network टैब खोलें और कुछ कन्वर्ट करें: कोई रिक्वेस्ट इमेज नहीं ले जाती, इसीलिए आपकी मशीन की मेमोरी से परे कोई फ़ाइल साइज़ कैप नहीं है।",
    ),
    related_tools=[
        ("compress-image.html", "इमेज कंप्रेस करें", "कन्वर्ट करने के बाद एक सटीक फ़ाइल साइज़ टारगेट पाएं।"),
        ("resize-image.html", "इमेज रीसाइज़ करें", "फ़ॉर्मैट कन्वर्ट करने से पहले या बाद में डाइमेंशंस बदलें।"),
        ("remove-metadata.html", "मेटाडेटा हटाएं", "किसी फ़ोटो से EXIF और लोकेशन डेटा हटाएं।"),
    ],
)

PAGES["ru"] = dict(
    title="Конвертер изображений: JPG, PNG, WebP онлайн | norito",
    meta_desc="Конвертируйте изображения между JPG, PNG и WebP прямо в браузере. Регулируемое качество, ничего не загружается.",
    app_name="Конвертер изображений", h1="Конвертер изображений", breadcrumb_label="Конвертер изображений",
    lede="Конвертируйте изображение между JPG, PNG и WebP. Регулируемое качество для форматов с потерями, всё происходит на вашем устройстве.",
    note_html='Просто конвертируете JPG в PNG? Попробуйте <a href="/jpg-to-png-converter.html">специальную страницу JPG в PNG</a>.',
    t=dict(
        dz_click="Нажмите, чтобы выбрать изображение", dz_drag=", или перетащите его сюда",
        dz_hint="JPG, PNG, WebP. Остаётся на вашем устройстве, ничего не загружается. Выберите несколько для пакетной конвертации.",
        convert_to="Конвертировать в", quality="Качество",
        convert_image="Конвертировать изображение", convert_all="Конвертировать все", download_zip="Скачать всё как .zip",
        converted_preview_alt="Предпросмотр после конвертации", preview_hint="Конвертированное изображение появится здесь после создания.",
        side_note="PNG без потерь (файлы больше, поддерживает прозрачность). JPEG и WebP с потерями, с ползунком качества (файлы меньше, без прозрачности для JPEG). WebP обычно превосходит JPEG при том же визуальном качестве, но JPEG обладает наибольшей совместимостью.",
        how_h2="Как это работает",
        how_p1="Ваше изображение загружается через локальный object URL (<code>URL.createObjectURL</code>), декодируется собственным декодером изображений браузера, отрисовывается на закадровом canvas в полном естественном разрешении и повторно кодируется с помощью <code>canvas.toBlob</code> в выбранном вами формате и качестве. Одна деталь обрабатывается за вас: у JPEG нет альфа-канала, поэтому перед отрисовкой canvas заполняется белым цветом, если целевой формат — JPEG. Без этого шага прозрачные области PNG получились бы чёрными. Ползунок качества применяется только к JPEG и WebP; кодирование PNG выполняется без потерь и игнорирует его.",
        how_p2="Побочный эффект прохода через canvas, о котором стоит знать в любом случае: результат содержит только пиксели. EXIF-метаданные, модель камеры, временные метки и встроенные GPS-координаты из фотографий с телефона не сохраняются при повторном кодировании. Это делает данный конвертер незаметным выигрышем для конфиденциальности перед публичным распространением фото, но также важно учитывать, если метаданные вам действительно нужны (в этом случае сохраните оригинал). Браузеры применяют флаг ориентации EXIF при декодировании, поэтому снятые боком фотографии с телефона по-прежнему получаются правильно повёрнутыми.",
        how_p3="Конвертация, пакетный режим и даже упаковка в .zip (собираемая побайтово в JavaScript) — всё это выполняется в вашем браузере. Откройте вкладку Network в DevTools и что-нибудь сконвертируйте: ни один запрос не передаёт изображение, поэтому ограничение размера файла зависит только от памяти вашего устройства.",
    ),
    related_tools=[
        ("compress-image.html", "Сжатие изображения", "Достигните точного размера файла после конвертации."),
        ("resize-image.html", "Изменение размера изображения", "Измените размеры до или после конвертации формата."),
        ("remove-metadata.html", "Удаление метаданных", "Удалите EXIF и данные о местоположении из фото."),
    ],
)

PAGES["ja"] = dict(
    title="画像コンバーター：JPG、PNG、WebPをオンラインで変換 | norito",
    meta_desc="ブラウザ内でJPG、PNG、WebP間で画像を変換。品質調整可能、アップロードなし。",
    app_name="画像コンバーター", h1="画像コンバーター", breadcrumb_label="画像コンバーター",
    lede="JPG、PNG、WebPの間で画像を変換します。非可逆形式は品質を調整でき、すべてお使いのデバイス上で行われます。",
    note_html='JPGをPNGに変換するだけですか？<a href="/jpg-to-png-converter.html">専用のJPGからPNGへの変換ページ</a>をお試しください。',
    t=dict(
        dz_click="クリックして画像を選択", dz_drag="、またはここにドラッグ＆ドロップ",
        dz_hint="JPG、PNG、WebPに対応。デバイス内にとどまり、アップロードは一切されません。複数選択で一括変換。",
        convert_to="変換先", quality="品質",
        convert_image="画像を変換", convert_all="すべて変換", download_zip="すべてを.zipでダウンロード",
        converted_preview_alt="変換後プレビュー", preview_hint="生成されると、変換された画像がここに表示されます。",
        side_note="PNGは可逆です（ファイルサイズは大きいが透明度に対応）。JPEGとWebPは非可逆で品質スライダーがあります（ファイルサイズは小さいが、JPEGは透明度なし）。同じ視覚的品質ではWebPが通常JPEGを上回りますが、JPEGは互換性が最も広範です。",
        how_h2="仕組み",
        how_p1="あなたの画像はローカルのオブジェクトURL（<code>URL.createObjectURL</code>）を通じて読み込まれ、ブラウザ自身の画像デコーダーでデコードされ、フルの本来の解像度でオフスクリーンのcanvasに描画され、選択した形式と品質で<code>canvas.toBlob</code>によって再エンコードされます。あなたのために処理される1つの詳細があります。JPEGにはアルファチャンネルがないため、描画前に、JPEGが変換先の場合はcanvasが白で塗りつぶされます。このステップがないと、PNGの透明部分は黒くなってしまいます。品質スライダーはJPEGとWebPにのみ適用されます。PNGエンコーディングは可逆であり、これを無視します。",
        how_p2="canvasの往復処理には、いずれにせよ知っておく価値のある副作用があります。出力にはピクセルのみが含まれます。スマートフォン写真のEXIFメタデータ、カメラのモデル、タイムスタンプ、埋め込まれたGPS座標は、再エンコード後には残りません。これにより、写真を公開する前にこのコンバーターがひそかにプライバシーを守ってくれる一方、実際にメタデータが必要な場合は注意が必要です（その場合は元のファイルを保持してください）。ブラウザはデコード時にEXIFの向きフラグを適用するため、横向きに撮影されたスマートフォン写真も正しい向きで出力されます。",
        how_p3="変換、一括モード、さらには.zipへのまとめ（JavaScriptでバイト単位で組み立てられる）まで、すべてブラウザ内で実行されます。DevToolsのNetworkタブを開いて何かを変換してみてください。画像を運ぶリクエストは一切発生しません。だからこそ、お使いのマシンのメモリ以外にファイルサイズの上限はありません。",
    ),
    related_tools=[
        ("compress-image.html", "画像を圧縮", "変換後に正確なファイルサイズを実現。"),
        ("resize-image.html", "画像のリサイズ", "形式変換の前後でサイズを変更。"),
        ("remove-metadata.html", "メタデータを削除", "写真からEXIFと位置情報を削除。"),
    ],
)

for loc, data in PAGES.items():
    lede_with_note = data["lede"] + f'\n    </p>\n    <p class="note">{data["note_html"]}'
    html = render_page(
        loc, "image-converter.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=lede_with_note,
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-image-converter.js", "js/prefill.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/image-converter.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
