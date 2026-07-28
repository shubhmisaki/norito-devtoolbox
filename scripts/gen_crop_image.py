#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/></svg>'
ICON_CLASS = "c-amber"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="dropzone" id="drop">
          <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/></svg>
          <p><strong>{t['dz_click']}</strong>{t['dz_drag']}</p>
          <p class="note" style="margin-top:2px;">{t['dz_hint']}</p>
          <input type="file" id="fileInput" accept="image/*" />
        </div>
        <p class="note" id="originalInfo" style="display:none;"></p>

        <div class="field" style="margin-top:20px;">
          <label for="aspect">{t['aspect_ratio']}</label>
          <select id="aspect">
            <option value="free" selected>{t['free']}</option>
            <option value="1:1">{t['square']}</option>
            <option value="4:3">4:3</option>
            <option value="16:9">16:9</option>
            <option value="9:16">{t['portrait']}</option>
          </select>
        </div>

        <div id="editorWrap" style="display:none;">
          <div class="stage-wrap" id="stage">
            <img id="stageImg" alt="{t['crop_preview_alt']}" />
            <div class="crop-box" id="cropBox">
              <div class="crop-handle"></div>
            </div>
          </div>
          <p class="note" style="margin-top:10px;">{t['drag_hint']}</p>
        </div>

        <button id="cropBtn" disabled style="margin-top:16px;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/></svg>
          {t['crop_download']}
        </button>
        <div class="result-box" id="result" style="display:none;"></div>
      </div>

      <div>
        <div class="panel" style="text-align:center;">
          <img class="preview" id="preview" style="display:none; max-width:100%;" alt="{t['cropped_result_alt']}" />
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
    title="Recortar Imagen Online: Arrastra para Recortar | norito",
    meta_desc="Recorta una imagen con un cuadro arrastrable, en tu navegador. Formato libre o proporciones fijas como 1:1, 4:3, 16:9. No se sube nada.",
    app_name="Recortar Imagen", h1="Recortar Imagen", breadcrumb_label="Recortar Imagen",
    lede="Arrastra un cuadro sobre tu imagen para recortarla. Formato libre o fijado a una proporción común, el recorte ocurre a resolución completa.",
    t=dict(
        dz_click="Haz clic para elegir una imagen", dz_drag=", o arrástrala aquí",
        dz_hint="JPG, PNG, WebP. Se queda en tu dispositivo, no se sube nada.",
        aspect_ratio="Proporción", free="Libre", square="Cuadrado (1:1)", portrait="9:16 (vertical)",
        crop_preview_alt="Vista previa de recorte", drag_hint="Arrastra dentro del cuadro para moverlo, arrastra el controlador de la esquina para redimensionarlo.",
        crop_download="Recortar y descargar",
        cropped_result_alt="Resultado recortado", preview_hint="Tu imagen recortada aparecerá aquí una vez generada.",
        side_note="Elige primero una proporción si necesitas una (como 1:1 para una foto de perfil), luego arrastra el cuadro a su posición. El recorte ocurre a la resolución completa de tu imagen, no al tamaño de visualización de la vista previa, así que la salida se mantiene nítida.",
        how_h2="Cómo funciona",
        how_p1="Tu archivo se carga a través de <code>URL.createObjectURL</code>, una referencia local en memoria, nunca una subida, y se muestra reducido para caber en el editor. El cuadro de recorte que arrastras se rastrea en píxeles de pantalla, pero en el momento en que pulsas recortar, esas coordenadas se multiplican por la proporción entre el tamaño natural de la imagen y su tamaño mostrado. Así que si tu foto de 4000px se muestra a 800px de ancho, un cuadro de 200px de ancho en pantalla selecciona una región de 1000px de ancho de la imagen real. El rectángulo seleccionado se copia entonces con la forma de rectángulo de origen de <code>drawImage</code> de la API canvas, que extrae exactamente esos píxeles del original a resolución completa.",
        how_p2="El formato de salida sigue al de entrada: PNG entra, PNG sale (sin pérdida, idéntico píxel a píxel a la región de origen), cualquier otra cosa se recodifica como JPEG al 92% de calidad vía <code>canvas.toBlob</code>. Esa distinción vale la pena conocer: recortar un JPEG significa una generación extra de compresión JPEG, normalmente invisible al 92% pero real. Si necesitas un recorte exacto a nivel de píxel, dale a la herramienta un PNG.",
        how_p3="Todo lo anterior ocurre en el propio decodificador de imágenes y canvas de tu navegador. Abre la pestaña Red de las DevTools antes de soltar una foto: ninguna petición transporta la imagen jamás, lo que también significa que no hay límite de tamaño del lado del servidor ni cola de espera.",
    ),
    related_tools=[
        ("resize-image.html", "Redimensionar imagen", "Cambia las dimensiones generales en vez de recortar una región."),
        ("compress-image.html", "Comprimir imagen", "Consigue un tamaño de archivo exacto después de recortar."),
        ("remove-background.html", "Quitar fondo", "Recorta a una persona de una foto, directamente en tu navegador."),
    ],
)

PAGES["zh"] = dict(
    title="在线裁剪图片：拖拽裁剪 | norito",
    meta_desc="在浏览器中用可拖动的裁剪框裁剪图片。自由裁剪或固定比例，如 1:1、4:3、16:9。不上传任何内容。",
    app_name="裁剪图片", h1="裁剪图片", breadcrumb_label="裁剪图片",
    lede="在图片上拖动裁剪框即可完成裁剪。可自由裁剪，也可锁定为常见比例，裁剪结果保持原始分辨率。",
    t=dict(
        dz_click="点击选择一张图片", dz_drag="，或将其拖放到此处",
        dz_hint="支持 JPG、PNG、WebP。文件保留在你的设备上，不会上传任何内容。",
        aspect_ratio="裁剪比例", free="自由", square="正方形 (1:1)", portrait="9:16（竖版）",
        crop_preview_alt="裁剪预览", drag_hint="在框内拖动可移动位置，拖动角部控制点可调整大小。",
        crop_download="裁剪并下载",
        cropped_result_alt="裁剪结果", preview_hint="生成后，裁剪后的图片会显示在这里。",
        side_note="如果需要特定比例（比如头像照片用 1:1），请先选择比例，然后把裁剪框拖到合适的位置。裁剪是按图片的完整分辨率进行的，而不是按预览的显示尺寸，因此输出结果始终保持清晰。",
        how_h2="工作原理",
        how_p1="你的文件通过 <code>URL.createObjectURL</code> 加载，这是一个本地内存引用，绝不会被上传，并会缩小显示以适配编辑器窗口。你拖动的裁剪框以屏幕像素为单位进行跟踪，但当你点击裁剪的那一刻，这些坐标会按图片原始尺寸与显示尺寸之间的比例进行换算。也就是说，如果你 4000 像素宽的照片以 800 像素宽显示，屏幕上一个 200 像素宽的裁剪框，实际选中的是原图中 1000 像素宽的区域。选中的矩形随后通过 canvas API 的 <code>drawImage</code> 源矩形形式进行复制，精确地从完整分辨率的原图中提取出对应像素。",
        how_p2="输出格式与输入保持一致：PNG 输入，PNG 输出（无损，与原始区域逐像素相同），其他格式都会通过 <code>canvas.toBlob</code> 以 92% 质量重新编码为 JPEG。这一区别值得了解：裁剪一张 JPEG 意味着多经历一次 JPEG 压缩，在 92% 质量下通常不易察觉，但确实存在。如果你需要像素级精确的裁剪，请给工具提供一张 PNG 图片。",
        how_p3="以上所有过程都在你浏览器自身的图像解码器和 canvas 中完成。在拖入照片之前打开开发者工具的 Network 标签页看看：从来没有任何请求携带过图片，这也意味着没有服务器端的大小限制，也不用排队等待。",
    ),
    related_tools=[
        ("resize-image.html", "调整图片尺寸", "改变整体尺寸，而不是裁剪出某个区域。"),
        ("compress-image.html", "压缩图片", "裁剪后达到精确的文件大小目标。"),
        ("remove-background.html", "去除背景", "在浏览器中直接从照片中抠出人像。"),
    ],
)

PAGES["ar"] = dict(
    title="قص الصور أونلاين: اسحب للقص | norito",
    meta_desc="اقصص صورة بمربع قابل للسحب، مباشرة في متصفحك. شكل حر أو نسب ثابتة مثل 1:1 و4:3 و16:9. لا شيء يُرفَع.",
    app_name="قص الصورة", h1="قص الصورة", breadcrumb_label="قص الصورة",
    lede="اسحب مربعًا فوق صورتك لقصّها. شكل حر أو مقفل على نسبة عرض إلى ارتفاع شائعة، ويحدث القص بالدقة الكاملة.",
    t=dict(
        dz_click="انقر لاختيار صورة", dz_drag="، أو اسحبها وأفلتها هنا",
        dz_hint="JPG وPNG وWebP. تبقى على جهازك، لا شيء يُرفَع.",
        aspect_ratio="نسبة العرض إلى الارتفاع", free="حر", square="مربع (1:1)", portrait="9:16 (عمودي)",
        crop_preview_alt="معاينة القص", drag_hint="اسحب داخل المربع لتحريكه، اسحب مقبض الزاوية لتغيير حجمه.",
        crop_download="قص وتنزيل",
        cropped_result_alt="النتيجة المقصوصة", preview_hint="ستظهر صورتك المقصوصة هنا بمجرد إنشائها.",
        side_note="اختر نسبة عرض إلى ارتفاع أولًا إذا كنت بحاجة إلى واحدة (مثل 1:1 لصورة ملف شخصي)، ثم اسحب المربع إلى موضعه. يحدث القص بالدقة الكاملة لصورتك، وليس بحجم عرض المعاينة، لذا يبقى الإخراج حادًا.",
        how_h2="كيف يعمل",
        how_p1='يُحمَّل ملفك عبر <code>URL.createObjectURL</code>، وهو مرجع محلي في الذاكرة، وليس رفعًا أبدًا، ويُعرَض مصغَّرًا ليناسب المحرر. يُتتبَّع مربع القص الذي تسحبه بوحدات بكسل الشاشة، لكن في اللحظة التي تضغط فيها على القص، تُضرَب تلك الإحداثيات بالنسبة بين الحجم الطبيعي للصورة وحجم عرضها. لذا إذا كانت صورتك بحجم 4000 بكسل تُعرَض بعرض 800 بكسل، فإن مربعًا بعرض 200 بكسل على الشاشة يحدد منطقة بعرض 1000 بكسل من الصورة الحقيقية. يُنسَخ المستطيل المحدَّد بعدها باستخدام شكل مستطيل المصدر لدالة <code>drawImage</code> في واجهة canvas، والتي تسحب بالضبط تلك البكسلات من الأصل بالدقة الكاملة.',
        how_p2="يتبع تنسيق الإخراج تنسيق الإدخال: PNG يدخل، PNG يخرج (بدون فقدان، مطابق بكسل لبكسل لمنطقة المصدر)، وأي شيء آخر يُعاد ترميزه كـ JPEG بجودة 92% عبر <code>canvas.toBlob</code>. هذا التمييز يستحق المعرفة: قص ملف JPEG يعني جيلًا إضافيًا من ضغط JPEG، وغالبًا غير مرئي بجودة 92% لكنه حقيقي. إذا كنت بحاجة إلى قص دقيق على مستوى البكسل، أعطِ الأداة ملف PNG.",
        how_p3="يحدث كل ما سبق في مُفكِّك ترميز الصور وcanvas الخاص بمتصفحك. افتح لسان Network في أدوات المطوّر قبل إسقاط صورة: لا يحمل أي طلب الصورة أبدًا، وهذا يعني أيضًا عدم وجود حد لحجم من جانب الخادم ولا طابور انتظار.",
    ),
    related_tools=[
        ("resize-image.html", "تغيير حجم الصورة", "غيّر الأبعاد الإجمالية بدلاً من قصّ منطقة."),
        ("compress-image.html", "ضغط الصور", "احصل على حجم ملف دقيق بعد القص."),
        ("remove-background.html", "إزالة الخلفية", "قصّ الشخص من الصورة مباشرة داخل متصفحك."),
    ],
)

PAGES["hi"] = dict(
    title="इमेज क्रॉप करें ऑनलाइन: ड्रैग करके क्रॉप करें | norito",
    meta_desc="अपने ब्राउज़र में ही एक ड्रैगेबल बॉक्स से इमेज क्रॉप करें। फ़्री-फ़ॉर्म या 1:1, 4:3, 16:9 जैसे फ़िक्स्ड एस्पेक्ट रेशो। कुछ भी अपलोड नहीं होता।",
    app_name="इमेज क्रॉप करें", h1="इमेज क्रॉप करें", breadcrumb_label="इमेज क्रॉप करें",
    lede="अपनी इमेज को क्रॉप करने के लिए उस पर एक बॉक्स ड्रैग करें। फ़्री-फ़ॉर्म या किसी कॉमन एस्पेक्ट रेशो में लॉक्ड, क्रॉप फ़ुल रिज़ॉल्यूशन पर होता है।",
    t=dict(
        dz_click="इमेज चुनने के लिए क्लिक करें", dz_drag=", या इसे यहां ड्रैग करके ड्रॉप करें",
        dz_hint="JPG, PNG, WebP। आपकी डिवाइस पर ही रहता है, कुछ भी अपलोड नहीं होता।",
        aspect_ratio="एस्पेक्ट रेशो", free="फ़्री", square="स्क्वेयर (1:1)", portrait="9:16 (पोर्ट्रेट)",
        crop_preview_alt="क्रॉप प्रीव्यू", drag_hint="इसे मूव करने के लिए बॉक्स के अंदर ड्रैग करें, रीसाइज़ करने के लिए कॉर्नर हैंडल ड्रैग करें।",
        crop_download="क्रॉप करें और डाउनलोड करें",
        cropped_result_alt="क्रॉप किया गया परिणाम", preview_hint="जनरेट होने के बाद आपकी क्रॉप की गई इमेज यहां दिखेगी।",
        side_note="अगर आपको एक एस्पेक्ट रेशो चाहिए (जैसे प्रोफ़ाइल फ़ोटो के लिए 1:1) तो पहले उसे चुनें, फिर बॉक्स को उसकी पोज़िशन में ड्रैग करें। क्रॉप आपकी इमेज के फ़ुल रिज़ॉल्यूशन पर होता है, प्रीव्यू के डिस्प्ले साइज़ पर नहीं, इसलिए आउटपुट शार्प रहता है।",
        how_h2="यह कैसे काम करता है",
        how_p1='आपकी फ़ाइल <code>URL.createObjectURL</code> के ज़रिए लोड होती है, जो एक लोकल इन-मेमोरी रेफ़रेंस है, कभी अपलोड नहीं, और एडिटर में फ़िट होने के लिए स्केल डाउन करके दिखाई जाती है। आप जो क्रॉप बॉक्स ड्रैग करते हैं वह ऑन-स्क्रीन पिक्सल्स में ट्रैक होता है, लेकिन जिस पल आप क्रॉप दबाते हैं, वे कोऑर्डिनेट्स इमेज के नैचुरल साइज़ और उसके डिस्प्ले साइज़ के बीच के रेशो से गुणा हो जाते हैं। तो अगर आपकी 4000px की फ़ोटो 800px चौड़ी दिखाई जा रही है, तो स्क्रीन पर एक 200px चौड़ा बॉक्स असली इमेज का 1000px चौड़ा क्षेत्र सिलेक्ट करता है। सिलेक्टेड रेक्टेंगल को फिर canvas API के <code>drawImage</code> सोर्स-रेक्टेंगल फ़ॉर्म से कॉपी किया जाता है, जो बिल्कुल वही पिक्सल्स फ़ुल-रिज़ॉल्यूशन ओरिजिनल से उठाता है।',
        how_p2="आउटपुट फ़ॉर्मैट इनपुट को फ़ॉलो करता है: PNG अंदर, PNG बाहर (लॉसलेस, सोर्स रीजन जैसा पिक्सल-आइडेंटिकल), बाक़ी सब कुछ <code>canvas.toBlob</code> के ज़रिए 92% क्वालिटी पर JPEG के रूप में री-एनकोड होता है। यह अंतर जानने लायक है: JPEG को क्रॉप करने का मतलब है JPEG कंप्रेशन की एक अतिरिक्त जनरेशन, जो आमतौर पर 92% पर अदृश्य होती है लेकिन असली होती है। अगर आपको पिक्सल-एग्ज़ैक्ट क्रॉप चाहिए, तो टूल को एक PNG दें।",
        how_p3="ऊपर बताया गया सब कुछ आपके ब्राउज़र के अपने इमेज डिकोडर और canvas में होता है। फ़ोटो ड्रॉप करने से पहले डेवटूल्स का Network टैब खोलें: कोई रिक्वेस्ट कभी इमेज नहीं ले जाती, जिसका मतलब यह भी है कि कोई सर्वर-साइड साइज़ लिमिट नहीं है और कोई क्यू नहीं है।",
    ),
    related_tools=[
        ("resize-image.html", "इमेज रीसाइज़ करें", "किसी क्षेत्र को काटने के बजाय पूरे डाइमेंशन बदलें।"),
        ("compress-image.html", "इमेज कंप्रेस करें", "क्रॉप करने के बाद एक सटीक फ़ाइल साइज़ टारगेट पाएं।"),
        ("remove-background.html", "बैकग्राउंड हटाएं", "फ़ोटो में से व्यक्ति को सीधे आपके ब्राउज़र में अलग करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Обрезать изображение онлайн: перетащите для обрезки | norito",
    meta_desc="Обрежьте изображение с помощью перетаскиваемой рамки прямо в браузере. Произвольная форма или фиксированные пропорции, такие как 1:1, 4:3, 16:9. Ничего не загружается.",
    app_name="Обрезать изображение", h1="Обрезать изображение", breadcrumb_label="Обрезать изображение",
    lede="Перетащите рамку по изображению, чтобы обрезать его. Произвольная форма или фиксация на распространённой пропорции — обрезка выполняется в полном разрешении.",
    t=dict(
        dz_click="Нажмите, чтобы выбрать изображение", dz_drag=", или перетащите его сюда",
        dz_hint="JPG, PNG, WebP. Остаётся на вашем устройстве, ничего не загружается.",
        aspect_ratio="Соотношение сторон", free="Произвольное", square="Квадрат (1:1)", portrait="9:16 (портрет)",
        crop_preview_alt="Предпросмотр обрезки", drag_hint="Перетаскивайте внутри рамки, чтобы переместить её, тяните за угловой маркер, чтобы изменить размер.",
        crop_download="Обрезать и скачать",
        cropped_result_alt="Результат обрезки", preview_hint="Обрезанное изображение появится здесь после создания.",
        side_note="Сначала выберите соотношение сторон, если оно вам нужно (например, 1:1 для фото профиля), затем перетащите рамку в нужное положение. Обрезка выполняется в полном разрешении вашего изображения, а не в размере отображения превью, поэтому результат остаётся чётким.",
        how_h2="Как это работает",
        how_p1="Ваш файл загружается через <code>URL.createObjectURL</code> — локальную ссылку в памяти, а не загрузку на сервер, — и отображается уменьшенным, чтобы поместиться в редакторе. Рамка обрезки, которую вы перетаскиваете, отслеживается в экранных пикселях, но в момент нажатия «обрезать» эти координаты умножаются на соотношение между естественным размером изображения и его отображаемым размером. Так что если ваше фото на 4000 пикселей показано шириной 800 пикселей, рамка шириной 200 пикселей на экране выделяет область шириной 1000 пикселей на реальном изображении. Выделенный прямоугольник затем копируется с помощью формы исходного прямоугольника метода <code>drawImage</code> API canvas, которая извлекает именно эти пиксели из оригинала полного разрешения.",
        how_p2="Формат вывода соответствует формату ввода: PNG на входе — PNG на выходе (без потерь, попиксельно идентичен исходной области), всё остальное перекодируется в JPEG с качеством 92% через <code>canvas.toBlob</code>. Это различие стоит знать: обрезка JPEG означает одно дополнительное поколение JPEG-сжатия, обычно незаметное при 92%, но реальное. Если вам нужна попиксельно точная обрезка, подайте инструменту PNG.",
        how_p3="Всё вышеперечисленное происходит в собственном декодере изображений и canvas вашего браузера. Откройте вкладку Network в DevTools перед тем, как перетащить фото: ни один запрос никогда не передаёт изображение, а это также означает отсутствие ограничения размера на стороне сервера и отсутствие очереди.",
    ),
    related_tools=[
        ("resize-image.html", "Изменение размера изображения", "Измените общие размеры вместо вырезания области."),
        ("compress-image.html", "Сжатие изображения", "Достигните точного размера файла после обрезки."),
        ("remove-background.html", "Удаление фона", "Вырезает человека с фотографии прямо в вашем браузере."),
    ],
)

PAGES["ja"] = dict(
    title="画像をオンラインでトリミング：ドラッグで切り抜き | norito",
    meta_desc="ブラウザ内でドラッグ可能なボックスを使って画像をトリミング。自由な形または1:1、4:3、16:9などの固定比率に対応。アップロードなし。",
    app_name="画像をトリミング", h1="画像をトリミング", breadcrumb_label="画像をトリミング",
    lede="画像の上にボックスをドラッグしてトリミングします。自由な形または一般的なアスペクト比に固定でき、トリミングはフル解像度で行われます。",
    t=dict(
        dz_click="クリックして画像を選択", dz_drag="、またはここにドラッグ＆ドロップ",
        dz_hint="JPG、PNG、WebPに対応。デバイス内にとどまり、アップロードは一切されません。",
        aspect_ratio="アスペクト比", free="自由", square="正方形（1:1）", portrait="9:16（縦向き）",
        crop_preview_alt="トリミングプレビュー", drag_hint="ボックス内をドラッグして移動、角のハンドルをドラッグしてサイズ変更。",
        crop_download="トリミングしてダウンロード",
        cropped_result_alt="トリミング結果", preview_hint="生成されると、トリミングされた画像がここに表示されます。",
        side_note="必要であれば先にアスペクト比を選び（プロフィール写真なら1:1など）、次にボックスを目的の位置にドラッグしてください。トリミングはプレビューの表示サイズではなく画像のフル解像度で行われるため、出力は鮮明なままです。",
        how_h2="仕組み",
        how_p1='あなたのファイルは<code>URL.createObjectURL</code>を通じて読み込まれます。これはローカルのメモリ内参照であり、アップロードでは決してありません。そしてエディターに収まるよう縮小して表示されます。あなたがドラッグするトリミングボックスは画面上のピクセルで追跡されますが、トリミングをクリックした瞬間、その座標は画像の実際のサイズと表示サイズの比率で乗算されます。つまり、4000ピクセルの写真が800ピクセル幅で表示されている場合、画面上の200ピクセル幅のボックスは、実際の画像の1000ピクセル幅の領域を選択することになります。選択された矩形はcanvas APIの<code>drawImage</code>のソース矩形形式でコピーされ、フル解像度のオリジナルからその正確なピクセルを抽出します。',
        how_p2="出力形式は入力形式に従います。PNGを入力すればPNGを出力し（可逆で、元の領域とピクセル単位で完全に同一）、それ以外は<code>canvas.toBlob</code>を介して92%の品質でJPEGとして再エンコードされます。この違いは知っておく価値があります。JPEGをトリミングするということは、JPEG圧縮がもう1世代加わることを意味し、92%の品質では通常目に見えませんが実際には発生しています。ピクセル単位で正確なトリミングが必要な場合は、ツールにPNGを渡してください。",
        how_p3="上記のすべては、あなたのブラウザ自身の画像デコーダーとcanvas内で行われます。写真をドロップする前にDevToolsのNetworkタブを開いてみてください。画像を運ぶリクエストは一切発生しません。これはサーバー側のサイズ制限も待ち行列も存在しないことを意味します。",
    ),
    related_tools=[
        ("resize-image.html", "画像のリサイズ", "領域を切り取るのではなく、全体のサイズを変更。"),
        ("compress-image.html", "画像を圧縮", "トリミング後に正確なファイルサイズを実現。"),
        ("remove-background.html", "背景を削除", "写真から人物をブラウザ内で直接切り抜きます。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "crop-image.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-crop-image.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/crop-image.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
