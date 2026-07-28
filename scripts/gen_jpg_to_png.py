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
          <select id="format" data-lock="true">
            <option value="jpeg">JPEG</option>
            <option value="png" selected>PNG</option>
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
    title="Conversor de JPG a PNG, Gratis y Online | norito",
    meta_desc="Convierte una foto JPG o JPEG a PNG, en tu navegador. Salida sin pérdida, no se sube nada a un servidor.",
    app_name="Conversor de JPG a PNG", h1="Conversor de JPG a PNG", breadcrumb_label="Conversor de JPG a PNG",
    lede="Convierte una foto JPG o JPEG a PNG con un clic. El formato objetivo ya está fijado a PNG, solo suelta una foto. Salida sin pérdida, todo ocurre en tu dispositivo.",
    t=dict(
        dz_click="Haz clic para elegir una imagen", dz_drag=", o arrástrala aquí",
        dz_hint="JPG, PNG, WebP. Se queda en tu dispositivo, no se sube nada. Selecciona varias para convertir en lote.",
        convert_to="Convertir a", quality="Calidad",
        convert_image="Convertir imagen", convert_all="Convertir todas", download_zip="Descargar todo como .zip",
        converted_preview_alt="Vista previa convertida", preview_hint="Tu imagen convertida aparecerá aquí una vez generada.",
        side_note="PNG no tiene pérdida (archivos más grandes, admite transparencia). JPEG y WebP tienen pérdida con un control deslizante de calidad (archivos más pequeños, sin transparencia para JPEG). WebP suele superar a JPEG a la misma calidad visual, pero JPEG tiene la mayor compatibilidad.",
        how_h2="Cómo funciona",
        how_p1='El navegador decodifica tu JPG en píxeles crudos, esos píxeles se dibujan en un canvas al ancho y alto natural completo de la imagen, y <code>canvas.toBlob("image/png")</code> escribe el resultado como un PNG. No hay control de calidad para esta dirección porque la compresión DEFLATE de PNG no tiene pérdida: cada píxel que produjo el decodificador se almacena exactamente. El archivo en sí nunca sale de tu máquina; se referencia a través de una URL de objeto local, no una subida.',
        how_p2="Dos cosas para mantener las expectativas claras. Primero, convertir a PNG no puede deshacer la compresión JPEG: los bloques y el ringing que ya existen en el JPG se conservan píxel por píxel, así que PNG es el objetivo correcto cuando vas a editar o volver a guardar la imagen repetidamente de aquí en adelante, no una forma de mejorarla. Segundo, las imágenes fotográficas están llenas de ruido de sensor que DEFLATE no puede comprimir bien, por eso el PNG suele ser varias veces más grande que el JPG del que provino. Eso es normal, no un error.",
        how_p3="El ida y vuelta por canvas también reescribe el archivo desde cero, así que los datos EXIF (información de cámara, posición GPS) se eliminan de la salida. La orientación sigue viéndose correcta, porque los navegadores modernos incorporan la rotación EXIF en los píxeles durante la decodificación. Y como todo el pipeline son APIs del navegador, puedes abrir la pestaña Red de las DevTools mientras conviertes y ver exactamente cero peticiones salir con tu foto.",
    ),
    related_tools=[
        ("compress-image.html", "Comprimir imagen", "Consigue un tamaño de archivo exacto después de convertir."),
        ("resize-image.html", "Redimensionar imagen", "Cambia las dimensiones antes o después de convertir el formato."),
        ("remove-metadata.html", "Eliminar metadatos", "Elimina EXIF y datos de ubicación de una foto."),
    ],
)

PAGES["zh"] = dict(
    title="JPG 转 PNG 转换器，免费在线使用 | norito",
    meta_desc="在浏览器中把 JPG 或 JPEG 照片转换为 PNG。无损输出，不会上传到任何服务器。",
    app_name="JPG 转 PNG 转换器", h1="JPG 转 PNG 转换器", breadcrumb_label="JPG 转 PNG 转换器",
    lede="一键把 JPG 或 JPEG 照片转换为 PNG。目标格式已经设为 PNG，只需拖入照片即可。无损输出，一切都在你的设备上完成。",
    t=dict(
        dz_click="点击选择一张图片", dz_drag="，或将其拖放到此处",
        dz_hint="支持 JPG、PNG、WebP。文件保留在你的设备上，不会上传任何内容。可多选进行批量转换。",
        convert_to="转换为", quality="质量",
        convert_image="转换图片", convert_all="全部转换", download_zip="以 .zip 下载全部",
        converted_preview_alt="转换后预览", preview_hint="生成后，转换后的图片会显示在这里。",
        side_note="PNG 无损（文件更大，支持透明度）。JPEG 和 WebP 有损，可通过滑块调节质量（文件更小，JPEG 不支持透明度）。在同等视觉质量下，WebP 通常优于 JPEG，但 JPEG 的兼容性最广。",
        how_h2="工作原理",
        how_p1='浏览器会把你的 JPG 解码为原始像素，这些像素会以图片完整的原始宽度和高度绘制到一个 canvas 上，然后 <code>canvas.toBlob("image/png")</code> 会把结果写为一个 PNG 文件。这个方向没有质量滑块，因为 PNG 的 DEFLATE 压缩是无损的：解码器生成的每一个像素都会被精确保存。文件本身永远不会离开你的电脑，它只是通过一个本地对象 URL 被引用，而不是被上传。',
        how_p2="有两点需要保持清晰的预期。第一，转换为 PNG 无法撤销 JPEG 压缩：JPG 中已经存在的块状伪影和振铃效应会被逐像素完整保留，因此 PNG 适合作为接下来要反复编辑或重新保存图片的目标格式，而不是一种改善画质的手段。第二，摄影图像中充满了传感器噪点，DEFLATE 对此压缩效果不佳，这就是为什么生成的 PNG 通常会比原始 JPG 大好几倍。这是正常现象，不是故障。",
        how_p3="canvas 往返处理还会从头重写文件，因此 EXIF 数据（相机信息、GPS 位置）会从输出中被移除。方向仍然显示正确，因为现代浏览器会在解码时把 EXIF 旋转信息直接烘焙进像素中。而且由于整个流程都是浏览器 API，你可以在转换时打开开发者工具的 Network 标签页，观察到确实没有任何携带你照片的请求被发出。",
    ),
    related_tools=[
        ("compress-image.html", "压缩图片", "转换后达到精确的文件大小目标。"),
        ("resize-image.html", "调整图片尺寸", "在转换格式前后更改尺寸。"),
        ("remove-metadata.html", "删除元数据", "从照片中清除 EXIF 和位置信息。"),
    ],
)

PAGES["ar"] = dict(
    title="محول JPG إلى PNG، مجاني وأونلاين | norito",
    meta_desc="حوّل صورة JPG أو JPEG إلى PNG، مباشرة في متصفحك. إخراج بدون فقدان، لا شيء يُرفَع إلى خادم.",
    app_name="محول JPG إلى PNG", h1="محول JPG إلى PNG", breadcrumb_label="محول JPG إلى PNG",
    lede="حوّل صورة JPG أو JPEG إلى PNG بنقرة واحدة. تنسيق الهدف مضبوط بالفعل على PNG، فقط أسقط صورة. إخراج بدون فقدان، كل شيء يحدث على جهازك.",
    t=dict(
        dz_click="انقر لاختيار صورة", dz_drag="، أو اسحبها وأفلتها هنا",
        dz_hint="JPG وPNG وWebP. تبقى على جهازك، لا شيء يُرفَع. اختر عدة صور للتحويل بالجملة.",
        convert_to="تحويل إلى", quality="الجودة",
        convert_image="تحويل الصورة", convert_all="تحويل الكل", download_zip="تنزيل الكل كملف .zip",
        converted_preview_alt="معاينة محوَّلة", preview_hint="ستظهر صورتك المحوَّلة هنا بمجرد إنشائها.",
        side_note="PNG بدون فقدان (ملفات أكبر، يدعم الشفافية). JPEG وWebP بفقدان مع منزلق جودة (ملفات أصغر، بلا شفافية لـ JPEG). عادةً ما يتفوّق WebP على JPEG بنفس الجودة البصرية، لكن JPEG يتمتع بأوسع توافق.",
        how_h2="كيف يعمل",
        how_p1='يفكّ المتصفح ترميز JPG إلى بكسلات خام، وتُرسَم تلك البكسلات على canvas بعرض وارتفاع الصورة الطبيعيين الكاملين، وتكتب <code>canvas.toBlob("image/png")</code> النتيجة كملف PNG. لا يوجد منزلق جودة لهذا الاتجاه لأن ضغط DEFLATE الخاص بـ PNG بدون فقدان: كل بكسل أنتجه المُفكِّك يُخزَّن بالضبط. الملف نفسه لا يغادر جهازك أبدًا؛ يُشار إليه عبر رابط كائن محلي، وليس رفعًا.',
        how_p2="أمران للحفاظ على التوقعات واضحة. أولًا، التحويل إلى PNG لا يمكنه التراجع عن ضغط JPEG: التكتّل والرنين الموجودان بالفعل في JPG يُحفَظان بدقة كل بكسل، لذا PNG هو الهدف الصحيح عندما ستحرر أو تعيد حفظ الصورة مرارًا من الآن فصاعدًا، وليس طريقة لتحسينها. ثانيًا، الصور الفوتوغرافية مليئة بضوضاء المستشعر التي لا يستطيع DEFLATE ضغطها جيدًا، ولهذا يكون PNG عادةً أكبر عدة مرات من JPG الذي جاء منه. هذا طبيعي، وليس خطأً.",
        how_p3="تعيد جولة canvas ذهابًا وإيابًا أيضًا كتابة الملف من الصفر، لذا تُحذَف بيانات EXIF (معلومات الكاميرا، موقع GPS) من الإخراج. لا يزال الاتجاه يبدو صحيحًا، لأن المتصفحات الحديثة تدمج دوران EXIF في البكسلات أثناء فك الترميز. وبما أن خط الأنابيب بأكمله هو واجهات برمجة تطبيقات المتصفح، يمكنك فتح لسان Network في أدوات المطوّر أثناء التحويل ومشاهدة صفر طلبات بالضبط تخرج مع صورتك.",
    ),
    related_tools=[
        ("compress-image.html", "ضغط الصور", "احصل على حجم ملف دقيق بعد التحويل."),
        ("resize-image.html", "تغيير حجم الصورة", "غيّر الأبعاد قبل أو بعد تحويل التنسيق."),
        ("remove-metadata.html", "إزالة البيانات الوصفية", "أزل بيانات EXIF والموقع من صورة."),
    ],
)

PAGES["hi"] = dict(
    title="JPG से PNG कन्वर्टर, मुफ़्त और ऑनलाइन | norito",
    meta_desc="अपने ब्राउज़र में ही एक JPG या JPEG फ़ोटो को PNG में कन्वर्ट करें। लॉसलेस आउटपुट, किसी सर्वर पर कुछ भी अपलोड नहीं होता।",
    app_name="JPG से PNG कन्वर्टर", h1="JPG से PNG कन्वर्टर", breadcrumb_label="JPG से PNG कन्वर्टर",
    lede="एक क्लिक में एक JPG या JPEG फ़ोटो को PNG में कन्वर्ट करें। टारगेट फ़ॉर्मैट पहले से PNG पर सेट है, बस एक फ़ोटो डालें। लॉसलेस आउटपुट, सब कुछ आपकी डिवाइस पर होता है।",
    t=dict(
        dz_click="इमेज चुनने के लिए क्लिक करें", dz_drag=", या इसे यहां ड्रैग करके ड्रॉप करें",
        dz_hint="JPG, PNG, WebP। आपकी डिवाइस पर ही रहता है, कुछ भी अपलोड नहीं होता। बैच कन्वर्ट करने के लिए कई चुनें।",
        convert_to="इसमें कन्वर्ट करें", quality="क्वालिटी",
        convert_image="इमेज कन्वर्ट करें", convert_all="सभी कन्वर्ट करें", download_zip="सभी को .zip के रूप में डाउनलोड करें",
        converted_preview_alt="कन्वर्ट किया गया प्रीव्यू", preview_hint="जनरेट होने के बाद आपकी कन्वर्ट की गई इमेज यहां दिखेगी।",
        side_note="PNG लॉसलेस है (बड़ी फ़ाइलें, ट्रांसपेरेंसी सपोर्ट करता है)। JPEG और WebP क्वालिटी स्लाइडर के साथ लॉसी हैं (छोटी फ़ाइलें, JPEG के लिए कोई ट्रांसपेरेंसी नहीं)। WebP आमतौर पर उसी विज़ुअल क्वालिटी पर JPEG से बेहतर होता है, लेकिन JPEG की कम्पैटिबिलिटी सबसे ज़्यादा है।",
        how_h2="यह कैसे काम करता है",
        how_p1='ब्राउज़र आपके JPG को रॉ पिक्सल्स में डिकोड करता है, वे पिक्सल्स इमेज की पूरी नैचुरल चौड़ाई और ऊंचाई पर एक canvas पर ड्रॉ किए जाते हैं, और <code>canvas.toBlob("image/png")</code> रिज़ल्ट को एक PNG के रूप में लिखता है। इस दिशा के लिए कोई क्वालिटी स्लाइडर नहीं है क्योंकि PNG का DEFLATE कंप्रेशन लॉसलेस है: डिकोडर द्वारा प्रोड्यूस किया गया हर पिक्सल बिल्कुल वैसे ही स्टोर होता है। फ़ाइल ख़ुद कभी आपकी मशीन से बाहर नहीं जाती; इसे एक लोकल ऑब्जेक्ट URL से रेफ़र किया जाता है, अपलोड से नहीं।',
        how_p2="उम्मीदों को साफ़ रखने के लिए दो बातें। पहली, PNG में कन्वर्ट करना JPEG कंप्रेशन को पूर्ववत नहीं कर सकता: JPG में पहले से मौजूद ब्लॉकीनेस और रिंगिंग पिक्सल-परफ़ेक्ट तरीक़े से बनी रहती है, इसलिए PNG सही टारगेट है जब आप यहां से आगे इमेज को बार-बार एडिट या री-सेव करने वाले हैं, इसे बेहतर बनाने का तरीक़ा नहीं। दूसरी, फ़ोटोग्राफ़िक इमेजेज़ सेंसर नॉइज़ से भरी होती हैं जिसे DEFLATE अच्छी तरह कंप्रेस नहीं कर पाता, इसीलिए PNG आमतौर पर उस JPG से कई गुना बड़ा होता है जिससे यह आया। यह नॉर्मल है, कोई बग नहीं।",
        how_p3="canvas राउंड-ट्रिप फ़ाइल को स्क्रैच से भी दोबारा लिखता है, इसलिए EXIF डेटा (कैमरा जानकारी, GPS पोज़िशन) आउटपुट से हट जाता है। ओरिएंटेशन फिर भी सही दिखता है, क्योंकि मॉडर्न ब्राउज़र्स डिकोडिंग के दौरान EXIF रोटेशन को पिक्सल्स में बेक कर देते हैं। और चूंकि पूरी पाइपलाइन ब्राउज़र APIs है, आप कन्वर्ट करते समय डेवटूल्स का Network टैब खोल सकते हैं और देख सकते हैं कि आपकी फ़ोटो के साथ बिल्कुल ज़ीरो रिक्वेस्ट्स जाती हैं।",
    ),
    related_tools=[
        ("compress-image.html", "इमेज कंप्रेस करें", "कन्वर्ट करने के बाद एक सटीक फ़ाइल साइज़ टारगेट पाएं।"),
        ("resize-image.html", "इमेज रीसाइज़ करें", "फ़ॉर्मैट कन्वर्ट करने से पहले या बाद में डाइमेंशंस बदलें।"),
        ("remove-metadata.html", "मेटाडेटा हटाएं", "किसी फ़ोटो से EXIF और लोकेशन डेटा हटाएं।"),
    ],
)

PAGES["ru"] = dict(
    title="Конвертер JPG в PNG, бесплатно и онлайн | norito",
    meta_desc="Конвертируйте фото JPG или JPEG в PNG прямо в браузере. Вывод без потерь, ничего не загружается на сервер.",
    app_name="Конвертер JPG в PNG", h1="Конвертер JPG в PNG", breadcrumb_label="Конвертер JPG в PNG",
    lede="Конвертируйте фото JPG или JPEG в PNG в один клик. Целевой формат уже установлен на PNG, просто добавьте фото. Вывод без потерь, всё происходит на вашем устройстве.",
    t=dict(
        dz_click="Нажмите, чтобы выбрать изображение", dz_drag=", или перетащите его сюда",
        dz_hint="JPG, PNG, WebP. Остаётся на вашем устройстве, ничего не загружается. Выберите несколько для пакетной конвертации.",
        convert_to="Конвертировать в", quality="Качество",
        convert_image="Конвертировать изображение", convert_all="Конвертировать все", download_zip="Скачать всё как .zip",
        converted_preview_alt="Предпросмотр после конвертации", preview_hint="Конвертированное изображение появится здесь после создания.",
        side_note="PNG без потерь (файлы больше, поддерживает прозрачность). JPEG и WebP с потерями, с ползунком качества (файлы меньше, без прозрачности для JPEG). WebP обычно превосходит JPEG при том же визуальном качестве, но JPEG обладает наибольшей совместимостью.",
        how_h2="Как это работает",
        how_p1='Браузер декодирует ваш JPG в необработанные пиксели, эти пиксели отрисовываются на canvas в полной естественной ширине и высоте изображения, и <code>canvas.toBlob("image/png")</code> записывает результат как PNG. Для этого направления нет ползунка качества, потому что сжатие DEFLATE у PNG выполняется без потерь: каждый пиксель, произведённый декодером, сохраняется в точности. Сам файл никогда не покидает ваш компьютер; на него ссылаются через локальный object URL, а не через загрузку.',
        how_p2="Две вещи, которые стоит понимать чётко. Во-первых, конвертация в PNG не может отменить сжатие JPEG: блочность и звон, уже присутствующие в JPG, сохраняются попиксельно точно, поэтому PNG — правильная цель, когда вы собираетесь многократно редактировать или пересохранять изображение впредь, а не способ его улучшить. Во-вторых, фотографические изображения полны шума сенсора, который DEFLATE не может хорошо сжать, поэтому PNG обычно в несколько раз больше исходного JPG. Это нормально, а не ошибка.",
        how_p3="Прохождение через canvas также полностью переписывает файл с нуля, поэтому данные EXIF (информация о камере, GPS-позиция) удаляются из результата. Ориентация по-прежнему выглядит правильно, потому что современные браузеры встраивают поворот EXIF в пиксели во время декодирования. А поскольку весь конвейер состоит из API браузера, вы можете открыть вкладку Network в DevTools во время конвертации и увидеть ровно ноль запросов, уходящих с вашим фото.",
    ),
    related_tools=[
        ("compress-image.html", "Сжатие изображения", "Достигните точного размера файла после конвертации."),
        ("resize-image.html", "Изменение размера изображения", "Измените размеры до или после конвертации формата."),
        ("remove-metadata.html", "Удаление метаданных", "Удалите EXIF и данные о местоположении из фото."),
    ],
)

PAGES["ja"] = dict(
    title="JPGからPNGへの変換ツール、無料オンライン | norito",
    meta_desc="ブラウザ内でJPGまたはJPEG写真をPNGに変換。可逆出力、サーバーへのアップロードなし。",
    app_name="JPGからPNGへの変換ツール", h1="JPGからPNGへの変換ツール", breadcrumb_label="JPGからPNGへの変換ツール",
    lede="ワンクリックでJPGまたはJPEG写真をPNGに変換します。変換先の形式はすでにPNGに設定されているので、写真をドロップするだけです。可逆出力で、すべてお使いのデバイス上で行われます。",
    t=dict(
        dz_click="クリックして画像を選択", dz_drag="、またはここにドラッグ＆ドロップ",
        dz_hint="JPG、PNG、WebPに対応。デバイス内にとどまり、アップロードは一切されません。複数選択で一括変換。",
        convert_to="変換先", quality="品質",
        convert_image="画像を変換", convert_all="すべて変換", download_zip="すべてを.zipでダウンロード",
        converted_preview_alt="変換後プレビュー", preview_hint="生成されると、変換された画像がここに表示されます。",
        side_note="PNGは可逆です（ファイルサイズは大きいが透明度に対応）。JPEGとWebPは非可逆で品質スライダーがあります（ファイルサイズは小さいが、JPEGは透明度なし）。同じ視覚的品質ではWebPが通常JPEGを上回りますが、JPEGは互換性が最も広範です。",
        how_h2="仕組み",
        how_p1='ブラウザはあなたのJPGを生のピクセルにデコードし、そのピクセルは画像の本来の幅と高さのままcanvasに描画され、<code>canvas.toBlob("image/png")</code>が結果をPNGとして書き出します。この方向には品質スライダーがありません。なぜならPNGのDEFLATE圧縮は可逆であり、デコーダーが生成したすべてのピクセルが正確に保存されるからです。ファイル自体はあなたのマシンから外に出ることはなく、アップロードではなくローカルのオブジェクトURLを通じて参照されます。',
        how_p2="期待値を正しく保つために知っておくべきことが2つあります。第一に、PNGへの変換はJPEG圧縮を元に戻すことはできません。JPGにすでに存在するブロックノイズやリンギングはピクセル単位でそのまま保持されます。そのため、PNGは今後何度も編集したり保存し直したりする場合の適切な変換先であり、画質を改善する手段ではありません。第二に、写真画像はDEFLATEがうまく圧縮できないセンサーノイズに満ちているため、生成されるPNGは元のJPGより通常数倍大きくなります。これは正常な動作であり、不具合ではありません。",
        how_p3="canvasを介した往復処理は、ファイルをゼロから書き直すため、EXIFデータ（カメラ情報、GPS位置）は出力から失われます。それでも向きは正しく見えます。これは、最新のブラウザがデコード時にEXIFの回転情報をピクセルに焼き込むためです。そしてパイプライン全体がブラウザAPIで構成されているため、変換中にDevToolsのNetworkタブを開けば、あなたの写真とともに送信されるリクエストが正確にゼロ件であることを確認できます。",
    ),
    related_tools=[
        ("compress-image.html", "画像を圧縮", "変換後に正確なファイルサイズを実現。"),
        ("resize-image.html", "画像のリサイズ", "形式変換の前後でサイズを変更。"),
        ("remove-metadata.html", "メタデータを削除", "写真からEXIFと位置情報を削除。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "jpg-to-png-converter.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-image-converter.js", "js/prefill.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/jpg-to-png-converter.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
