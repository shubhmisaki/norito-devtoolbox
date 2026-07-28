#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
ICON_CLASS = "c-amber"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <h3 style="margin-top:0;">{t['unix_ts']}</h3>
        <div class="field-row">
          <div class="field" style="flex:1;">
            <label for="tsInput">{t['timestamp']}</label>
            <input type="text" id="tsInput" class="mono-output" style="height:42px; font-size:0.95rem;" inputmode="numeric" />
          </div>
          <div class="field">
            <label for="tsUnit">{t['unit']}</label>
            <select id="tsUnit">
              <option value="s">{t['seconds']}</option>
              <option value="ms" selected>{t['milliseconds']}</option>
            </select>
          </div>
          <button id="nowBtn" class="secondary" style="align-self:flex-end;">{t['now']}</button>
        </div>

        <div class="result-box error" id="errorBox" style="display:none; margin-bottom:16px;">
          <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
          <div class="r-body"></div>
        </div>

        <div class="field" style="margin-bottom:14px;">
          <label>{t['local_time']}</label>
          <input type="text" id="localOut" class="mono-output" style="height:42px; font-size:0.9rem;" readonly />
        </div>
        <div class="field" style="margin-bottom:14px;">
          <label>{t['utc']}</label>
          <input type="text" id="utcOut" class="mono-output" style="height:42px; font-size:0.9rem;" readonly />
        </div>
        <div class="field" style="margin-bottom:14px;">
          <label>{t['iso']}</label>
          <input type="text" id="isoOut" class="mono-output" style="height:42px; font-size:0.9rem;" readonly />
        </div>
        <div class="field">
          <label>{t['relative']}</label>
          <input type="text" id="relativeOut" class="mono-output" style="height:42px; font-size:0.9rem;" readonly />
        </div>

        <h3>{t['date_time']}</h3>
        <div class="field" style="margin-bottom:16px;">
          <label for="dateInput">{t['pick_date']}</label>
          <input type="datetime-local" id="dateInput" step="1" />
        </div>
        <div class="field-row">
          <div class="field" style="flex:1;">
            <label>{t['unix_seconds']}</label>
            <input type="text" id="secOut" class="mono-output" style="height:42px; font-size:0.9rem;" readonly />
          </div>
          <button id="copySecBtn" class="secondary" style="align-self:flex-end;">{t['copy']}</button>
        </div>
        <div class="field-row">
          <div class="field" style="flex:1;">
            <label>{t['unix_ms']}</label>
            <input type="text" id="msOut" class="mono-output" style="height:42px; font-size:0.9rem;" readonly />
          </div>
          <button id="copyMsBtn" class="secondary" style="align-self:flex-end;">{t['copy']}</button>
        </div>
      </div>

      <div>
        <div class="panel">
          <div class="panel-header">
            <div class="icon-chip c-amber" style="width:36px;height:36px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            </div>
            <div>
              <h3>{t['faq1_q']}</h3>
              <p>{t['faq1_short']}</p>
            </div>
          </div>
          <p class="note" style="margin-top:0;">
            {t['faq1_a']}
          </p>
        </div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['faq2_q']}</h3>
          <p class="note" style="margin-top:0;">
            {t['faq2_a']}
          </p>
        </div>
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
    title="Conversor de Timestamp: Unix Time y Fechas | norito",
    meta_desc="Convierte entre timestamps Unix y fechas legibles, en ambas direcciones, en vivo. Salida en hora local, UTC e ISO 8601.",
    app_name="Conversor de Timestamp", h1="Conversor de Timestamp", breadcrumb_label="Conversor de Timestamp",
    lede="Convierte timestamps Unix a fechas legibles y viceversa; ambas direcciones se mantienen sincronizadas mientras editas cualquiera de las dos.",
    t=dict(
        unix_ts="Timestamp Unix", timestamp="Timestamp", unit="Unidad", seconds="Segundos", milliseconds="Milisegundos", now="Ahora",
        local_time="Hora local", utc="UTC", iso="ISO 8601", relative="Relativo",
        date_time="Fecha y hora", pick_date="Elige una fecha y hora (tu zona horaria local)",
        unix_seconds="Segundos Unix", unix_ms="Milisegundos Unix", copy="Copiar",
        faq1_q="¿Qué es un timestamp Unix?", faq1_short="Segundos (o ms) desde el 1 de enero de 1970.",
        faq1_a='La época Unix es la medianoche UTC del 1 de enero de 1970. Un timestamp es simplemente el número de segundos (o milisegundos) transcurridos desde entonces, por eso se ordena y compara como un número simple, a diferencia de una cadena de fecha con formato.',
        faq2_q="Segundos vs. milisegundos",
        faq2_a='Unix, Linux y la mayoría de las APIs de backend usan segundos. El propio <code>Date.now()</code> de JavaScript y la mayoría del código frontend usan milisegundos. Confundir ambos es uno de los errores de timestamp más comunes: un valor en "segundos" pegado en un campo de "milisegundos" cae en algún punto de 1970.',
        how_h2="Cómo funciona",
        how_p1='Todo pasa por el objeto <code>Date</code> del navegador, que almacena internamente un solo número: milisegundos desde la época Unix, medianoche UTC del 1 de enero de 1970. Al convertir un timestamp, la herramienta multiplica por 1000 si indicaste segundos, construye un <code>Date</code>, y lo muestra de cuatro formas: tu hora local vía <code>toLocaleString</code> (el formateador Intl del navegador, usando tu propia zona horaria e idioma), UTC, ISO 8601, y una etiqueta relativa "en 3 días / hace 2 horas" calculada agrupando la diferencia con el ahora en años, meses, días, horas, minutos o segundos.',
        how_p2='En la dirección contraria, el valor del selector de fecha se interpreta como hora local y se convierte de nuevo a segundos y milisegundos. El campo datetime-local se alimenta desplazando primero el timestamp por tu desfase horario, que es la parte delicada que la mayoría de los conversores hacen mal sutilmente: <code>toISOString()</code> siempre habla en UTC, así que sin ese desplazamiento el selector mostraría una hora desviada varias horas de la hora de reloj que esperas.',
        how_p3='El error clásico contra el que esta herramienta protege haciendo la unidad explícita: segundos vs milisegundos. Los timestamps Unix actuales tienen 10 dígitos en segundos y 13 en milisegundos. Interpreta un valor en milisegundos como segundos y aterrizas más de 50.000 años en el futuro; haz lo contrario y obtienes enero de 1970. Si una conversión se ve absurda, cambia el desplegable de unidad, eso casi siempre es todo el error. Los valores fuera de rango (las fechas de JavaScript tienen un tope de 100 millones de días a cada lado de la época, aproximadamente el año 275760) producen un error claro en lugar de basura.',
        how_p4='Todo el análisis y formateo son trabajo de la API local del navegador. Abre la pestaña Red de las DevTools mientras conviertes: no se dispara ninguna petición, y los timestamps de tus logs nunca salen de tu máquina.',
    ),
    related_tools=[
        ("uuid-generator.html", "Generador de UUID", "Identificadores UUID v4 aleatorios en lote."),
        ("hash-generator.html", "Generador de hashes", "MD5, SHA-1, SHA-256 y SHA-512 de cualquier texto."),
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica JSON con una vista de árbol."),
    ],
)

PAGES["zh"] = dict(
    title="时间戳转换器：Unix 时间与日期互转 | norito",
    meta_desc="在 Unix 时间戳与可读日期之间实时双向转换。支持本地时间、UTC 和 ISO 8601 输出。",
    app_name="时间戳转换器", h1="时间戳转换器", breadcrumb_label="时间戳转换器",
    lede="将 Unix 时间戳转换为可读日期，也可反向转换；编辑任意一方，两边都会实时同步。",
    t=dict(
        unix_ts="Unix 时间戳", timestamp="时间戳", unit="单位", seconds="秒", milliseconds="毫秒", now="当前时间",
        local_time="本地时间", utc="UTC", iso="ISO 8601", relative="相对时间",
        date_time="日期和时间", pick_date="选择日期和时间（你的本地时区）",
        unix_seconds="Unix 秒数", unix_ms="Unix 毫秒数", copy="复制",
        faq1_q="什么是 Unix 时间戳？", faq1_short="自 1970 年 1 月 1 日起的秒数（或毫秒数）。",
        faq1_a="Unix 纪元是 1970 年 1 月 1 日 UTC 零点。时间戳就是自那时起经过的秒数（或毫秒数），因此它可以像普通数字一样排序和比较，而不像格式化的日期字符串那样。",
        faq2_q="秒和毫秒的区别",
        faq2_a="Unix、Linux 以及大多数后端 API 使用秒。JavaScript 自身的 <code>Date.now()</code> 和大多数前端代码使用毫秒。混淆这两者是最常见的时间戳错误之一——把一个「秒」值粘贴到「毫秒」字段中，结果会落在 1970 年附近。",
        how_h2="工作原理",
        how_p1="一切都通过浏览器的 <code>Date</code> 对象处理，该对象内部只存储一个数字：自 Unix 纪元（1970 年 1 月 1 日 UTC 零点）以来的毫秒数。转换时间戳时，如果你选择了「秒」，工具会先乘以 1000，构建一个 <code>Date</code> 对象，然后以四种方式呈现：通过 <code>toLocaleString</code>（浏览器的 Intl 格式化器，使用你自己的时区和语言）显示本地时间、UTC、ISO 8601，以及一个通过将与当前时刻的差值归入年、月、日、时、分或秒来计算出的「3 天后 / 2 小时前」相对时间标签。",
        how_p2="反过来，日期选择器的值会被解析为本地时间，再转换回秒和毫秒。datetime-local 字段的填充方式是先按你的时区偏移量对时间戳进行平移，这是大多数转换工具容易出微妙错误的细节：<code>toISOString()</code> 始终以 UTC 表示，如果没有这一步平移，选择器显示的时间会与你预期的挂钟时间相差数小时。",
        how_p3="这个工具通过明确单位来防范一个经典错误：秒 vs 毫秒。当前的 Unix 时间在「秒」单位下是 10 位数字，在「毫秒」单位下是 13 位数字。把一个毫秒值当作秒来解析，你会跳到 5 万多年后的未来；反过来则会得到 1970 年 1 月。如果转换结果看起来很荒谬，切换一下单位下拉框，几乎总能解决问题。超出范围的值（JavaScript 日期在纪元两侧最多支持 1 亿天，大约到公元 275760 年）会给出清晰的错误提示，而不是无意义的结果。",
        how_p4="所有解析和格式化都是本地浏览器 API 的工作。转换时打开开发者工具的 Network 面板：不会发出任何请求，你日志里的时间戳永远不会离开你的电脑。",
    ),
    related_tools=[
        ("uuid-generator.html", "UUID 生成器", "批量生成随机 UUID v4 标识符。"),
        ("hash-generator.html", "哈希生成器", "任意文本的 MD5、SHA-1、SHA-256 和 SHA-512。"),
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩 JSON，附带树状视图。"),
    ],
)

PAGES["ar"] = dict(
    title="محول الطابع الزمني: توقيت Unix وتحويل التاريخ | norito",
    meta_desc="حوّل بين طوابع Unix الزمنية والتواريخ القابلة للقراءة، في كلا الاتجاهين، مباشرة. إخراج بالتوقيت المحلي وUTC وISO 8601.",
    app_name="محول الطابع الزمني", h1="محول الطابع الزمني", breadcrumb_label="محول الطابع الزمني",
    lede="حوّل طوابع Unix الزمنية إلى تواريخ قابلة للقراءة والعكس، ويبقى الاتجاهان متزامنين أثناء تعديل أيّ منهما.",
    t=dict(
        unix_ts="طابع Unix الزمني", timestamp="الطابع الزمني", unit="الوحدة", seconds="ثوانٍ", milliseconds="ميلي ثانية", now="الآن",
        local_time="التوقيت المحلي", utc="UTC", iso="ISO 8601", relative="نسبي",
        date_time="التاريخ والوقت", pick_date="اختر تاريخًا ووقتًا (منطقتك الزمنية المحلية)",
        unix_seconds="ثوانٍ Unix", unix_ms="ميلي ثانية Unix", copy="نسخ",
        faq1_q="ما هو الطابع الزمني Unix؟", faq1_short="ثوانٍ (أو ميلي ثانية) منذ 1 يناير 1970.",
        faq1_a="حِقبة Unix هي منتصف ليل UTC يوم 1 يناير 1970. الطابع الزمني هو ببساطة عدد الثواني (أو الميلي ثانية) المنقضية منذ ذلك الحين، ولهذا يُرتَّب ويُقارَن كرقم عادي، بخلاف سلسلة تاريخ منسّقة.",
        faq2_q="الفرق بين الثواني والميلي ثانية",
        faq2_a='يستخدم Unix وLinux ومعظم واجهات برمجة التطبيقات الخلفية الثواني. تستخدم <code>Date.now()</code> الخاصة بجافاسكريبت ومعظم كود الواجهة الأمامية الميلي ثانية. الخلط بينهما واحد من أكثر أخطاء الطابع الزمني شيوعًا، فقيمة «ثوانٍ» تُلصَق في حقل «ميلي ثانية» تهبط في مكان ما في عام 1970.',
        how_h2="كيف يعمل",
        how_p1="يمرّ كل شيء عبر كائن <code>Date</code> الخاص بالمتصفح، الذي يخزّن داخليًا رقمًا واحدًا: الميلي ثانية منذ حِقبة Unix، منتصف ليل UTC يوم 1 يناير 1970. عند تحويل طابع زمني، تضرب الأداة في 1000 إذا اخترت الثواني، وتبني كائن <code>Date</code>، ثم تعرضه بأربع طرق: توقيتك المحلي عبر <code>toLocaleString</code> (منسّق Intl الخاص بالمتصفح، باستخدام منطقتك الزمنية ولغتك)، وUTC، وISO 8601، وتسمية نسبية مثل «بعد 3 أيام / منذ ساعتين» تُحسَب بتصنيف الفرق عن الآن إلى سنوات أو أشهر أو أيام أو ساعات أو دقائق أو ثوانٍ.",
        how_p2="في الاتجاه الآخر، تُفسَّر قيمة منتقي التاريخ كتوقيت محلي وتُحوَّل مرة أخرى إلى كل من الثواني والميلي ثانية. يُغذَّى حقل datetime-local بإزاحة الطابع الزمني أولًا بفارق منطقتك الزمنية، وهو الجزء الدقيق الذي تخطئ فيه معظم أدوات التحويل بشكل خفي: <code>toISOString()</code> يتحدث دائمًا بتوقيت UTC، فبدون تلك الإزاحة سيعرض المنتقي وقتًا يفصله ساعات عن الوقت الفعلي الذي تتوقعه.",
        how_p3="الخطأ الكلاسيكي الذي تحمي منه هذه الأداة بجعل الوحدة صريحة: ثوانٍ مقابل ميلي ثانية. أوقات Unix الحالية مكوّنة من 10 أرقام بالثواني و13 رقمًا بالميلي ثانية. حلّل قيمة بالميلي ثانية كثوانٍ وستهبط بعد أكثر من 50,000 سنة في المستقبل؛ افعل العكس وستحصل على يناير 1970. إذا بدا التحويل غير منطقي، بدّل القائمة المنسدلة للوحدة، فهذا يحل المشكلة في الغالب دائمًا. القيم خارج النطاق (تواريخ جافاسكريبت محدودة بـ 100 مليون يوم على جانبي الحِقبة، أي حوالي عام 275760) تُنتِج خطأً واضحًا بدلاً من نتيجة عشوائية.",
        how_p4="كل التحليل والتنسيق هو عمل واجهة برمجة تطبيقات محلية في المتصفح. افتح لسان Network في أدوات المطوّر أثناء التحويل: لن يُطلَق أي طلب، والطوابع الزمنية من سجلاتك لن تغادر جهازك أبدًا.",
    ),
    related_tools=[
        ("uuid-generator.html", "مولّد UUID", "معرّفات UUID v4 عشوائية بالجملة."),
        ("hash-generator.html", "مولّد التجزئة", "MD5 وSHA-1 وSHA-256 وSHA-512 لأي نص."),
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق وضغط JSON مع عرض شجري."),
    ],
)

PAGES["hi"] = dict(
    title="टाइमस्टैंप कन्वर्टर: Unix टाइम और डेट कन्वर्टर | norito",
    meta_desc="Unix टाइमस्टैंप और आसानी से पढ़ी जाने वाली तारीखों के बीच, दोनों दिशाओं में, लाइव कन्वर्ट करें। लोकल टाइम, UTC, और ISO 8601 आउटपुट।",
    app_name="टाइमस्टैंप कन्वर्टर", h1="टाइमस्टैंप कन्वर्टर", breadcrumb_label="टाइमस्टैंप कन्वर्टर",
    lede="Unix टाइमस्टैंप को पढ़ने लायक तारीखों में बदलें और वापस भी; किसी भी एक को एडिट करने पर दोनों दिशाएं सिंक में रहती हैं।",
    t=dict(
        unix_ts="Unix टाइमस्टैंप", timestamp="टाइमस्टैंप", unit="यूनिट", seconds="सेकंड", milliseconds="मिलीसेकंड", now="अभी",
        local_time="लोकल टाइम", utc="UTC", iso="ISO 8601", relative="रिलेटिव",
        date_time="तारीख और समय", pick_date="एक तारीख और समय चुनें (आपकी लोकल टाइमज़ोन)",
        unix_seconds="Unix सेकंड", unix_ms="Unix मिलीसेकंड", copy="कॉपी करें",
        faq1_q="Unix टाइमस्टैंप क्या है?", faq1_short="1 जनवरी 1970 से सेकंड (या ms)।",
        faq1_a="Unix एपॉक 1 जनवरी 1970 की UTC आधी रात है। टाइमस्टैंप बस तब से गुज़रे सेकंड (या मिलीसेकंड) की संख्या है, इसीलिए यह एक फ़ॉर्मैटेड डेट स्ट्रिंग के उलट, एक सादे नंबर की तरह सॉर्ट और कंपेयर होता है।",
        faq2_q="सेकंड और मिलीसेकंड टाइमस्टैंप में अंतर",
        faq2_a='Unix, Linux, और ज़्यादातर बैकएंड APIs सेकंड इस्तेमाल करते हैं। JavaScript का अपना <code>Date.now()</code> और ज़्यादातर फ़्रंटएंड कोड मिलीसेकंड इस्तेमाल करते हैं। इन दोनों को मिला देना सबसे कॉमन टाइमस्टैंप बग्स में से एक है, एक "सेकंड" वैल्यू को "मिलीसेकंड" फ़ील्ड में पेस्ट करने पर वह 1970 के आसपास कहीं पहुंच जाती है।',
        how_h2="यह कैसे काम करता है",
        how_p1="सब कुछ ब्राउज़र के <code>Date</code> ऑब्जेक्ट से होकर गुज़रता है, जो इंटरनली सिर्फ़ एक नंबर स्टोर करता है: Unix एपॉक यानी 1 जनवरी 1970 की UTC आधी रात से मिलीसेकंड। किसी टाइमस्टैंप को कन्वर्ट करने पर, अगर आपने सेकंड बताया है तो टूल उसे 1,000 से गुणा करता है, एक <code>Date</code> बनाता है, फिर उसे चार तरीकों से दिखाता है: <code>toLocaleString</code> के ज़रिए आपका लोकल टाइम (ब्राउज़र का Intl फ़ॉर्मैटर, आपकी अपनी टाइमज़ोन और भाषा इस्तेमाल करते हुए), UTC, ISO 8601, और एक रिलेटिव लेबल जैसे \"3 दिन में / 2 घंटे पहले\" जो अभी के फ़र्क़ को साल, महीने, दिन, घंटे, मिनट, या सेकंड में बांटकर कैलकुलेट होता है।",
        how_p2="दूसरी तरफ़, डेट पिकर की वैल्यू को लोकल टाइम के रूप में पार्स करके वापस सेकंड और मिलीसेकंड दोनों में कन्वर्ट किया जाता है। datetime-local फ़ील्ड को पहले टाइमस्टैंप को आपके टाइमज़ोन ऑफ़सेट से शिफ़्ट करके फ़ीड किया जाता है, जो वह पेचीदा हिस्सा है जिसे ज़्यादातर कन्वर्टर सूक्ष्म रूप से ग़लत कर देते हैं: <code>toISOString()</code> हमेशा UTC में बात करता है, इसलिए उस शिफ़्ट के बिना पिकर आपकी उम्मीद से घंटों दूर का समय दिखाएगा।",
        how_p3="जो क्लासिक गलती से यह टूल यूनिट को स्पष्ट बनाकर बचाता है: सेकंड बनाम मिलीसेकंड। मौजूदा Unix टाइम सेकंड में 10 अंकों का और मिलीसेकंड में 13 अंकों का होता है। किसी मिलीसेकंड वैल्यू को सेकंड मानकर पार्स करें तो आप 50,000+ साल आगे भविष्य में पहुंच जाते हैं; उलटा करें तो जनवरी 1970 मिलता है। अगर कोई कन्वर्ज़न अजीब लगे, यूनिट ड्रॉपडाउन बदल दें, लगभग हमेशा यही पूरी गड़बड़ होती है। रेंज से बाहर की वैल्यू (JavaScript डेट्स एपॉक के हर तरफ़ 10 करोड़ दिनों तक सीमित हैं, यानी लगभग साल 275760) एक साफ़ एरर देती हैं, बकवास आउटपुट नहीं।",
        how_p4="सारी पार्सिंग और फ़ॉर्मैटिंग लोकल ब्राउज़र API का काम है। कन्वर्ट करते समय डेवटूल्स का Network टैब खोलें: कोई रिक्वेस्ट फ़ायर नहीं होती, और आपके लॉग्स के टाइमस्टैंप कभी आपकी मशीन से बाहर नहीं जाते।",
    ),
    related_tools=[
        ("uuid-generator.html", "UUID जनरेटर", "बल्क रैंडम UUID v4 आइडेंटिफ़ायर।"),
        ("hash-generator.html", "हैश जनरेटर", "किसी भी टेक्स्ट के MD5, SHA-1, SHA-256, और SHA-512."),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "ट्री व्यू के साथ JSON फ़ॉर्मैट, वैलिडेट और मिनिफ़ाई करें."),
    ],
)

PAGES["ru"] = dict(
    title="Конвертер меток времени: Unix Time и дата | norito",
    meta_desc="Конвертируйте между метками времени Unix и читаемыми датами в обе стороны, в реальном времени. Вывод в местном времени, UTC и ISO 8601.",
    app_name="Конвертер меток времени", h1="Конвертер меток времени", breadcrumb_label="Конвертер меток времени",
    lede="Конвертируйте метки времени Unix в читаемые даты и обратно — оба направления остаются синхронизированными при редактировании любого из них.",
    t=dict(
        unix_ts="Метка времени Unix", timestamp="Метка времени", unit="Единица", seconds="Секунды", milliseconds="Миллисекунды", now="Сейчас",
        local_time="Местное время", utc="UTC", iso="ISO 8601", relative="Относительно",
        date_time="Дата и время", pick_date="Выберите дату и время (ваш местный часовой пояс)",
        unix_seconds="Секунды Unix", unix_ms="Миллисекунды Unix", copy="Копировать",
        faq1_q="Что такое метка времени Unix?", faq1_short="Секунды (или мс) с 1 января 1970 года.",
        faq1_a="Эпоха Unix — это полночь UTC 1 января 1970 года. Метка времени — это просто число секунд (или миллисекунд), прошедших с тех пор, поэтому она сортируется и сравнивается как обычное число, в отличие от отформатированной строки даты.",
        faq2_q="Разница между секундами и миллисекундами",
        faq2_a="Unix, Linux и большинство серверных API используют секунды. Собственный <code>Date.now()</code> JavaScript и большая часть фронтенд-кода используют миллисекунды. Путаница между ними — одна из самых распространённых ошибок с метками времени: значение в «секундах», вставленное в поле «миллисекунды», попадает куда-то в 1970 год.",
        how_h2="Как это работает",
        how_p1="Всё проходит через объект <code>Date</code> браузера, который внутренне хранит одно число: миллисекунды с эпохи Unix, полуночи UTC 1 января 1970 года. При конвертации метки времени инструмент умножает на 1000, если вы указали секунды, строит <code>Date</code>, а затем отображает его четырьмя способами: ваше местное время через <code>toLocaleString</code> (форматтер Intl браузера, использующий ваш часовой пояс и язык), UTC, ISO 8601 и относительную метку «через 3 дня / 2 часа назад», вычисляемую путём разбиения разницы с текущим моментом на годы, месяцы, дни, часы, минуты или секунды.",
        how_p2="В обратном направлении значение выбора даты интерпретируется как местное время и конвертируется обратно в секунды и миллисекунды. Поле datetime-local заполняется путём сдвига метки времени на смещение вашего часового пояса — это та тонкая деталь, в которой большинство конвертеров ошибаются незаметно: <code>toISOString()</code> всегда работает в UTC, поэтому без этого сдвига выбор даты показывал бы время, отличающееся на несколько часов от ожидаемого настенного времени.",
        how_p3="Классическая ошибка, от которой защищает этот инструмент, делая единицу измерения явной: секунды против миллисекунд. Текущее время Unix — это 10 цифр в секундах и 13 цифр в миллисекундах. Разберите значение в миллисекундах как секунды — и вы окажетесь более чем на 50 000 лет в будущем; сделайте наоборот — получите январь 1970 года. Если результат конвертации выглядит абсурдно, переключите выпадающий список единиц — почти всегда в этом вся ошибка. Значения вне диапазона (даты JavaScript ограничены 100 миллионами дней в каждую сторону от эпохи, примерно до 275760 года) выдают понятную ошибку вместо бессмыслицы.",
        how_p4="Весь разбор и форматирование — это работа локального API браузера. Откройте вкладку Network в DevTools во время конвертации: ни один запрос не отправляется, а метки времени из ваших логов никогда не покидают ваш компьютер.",
    ),
    related_tools=[
        ("uuid-generator.html", "Генератор UUID", "Массовая генерация случайных идентификаторов UUID v4."),
        ("hash-generator.html", "Генератор хешей", "MD5, SHA-1, SHA-256 и SHA-512 любого текста."),
        ("json-formatter.html", "Форматирование JSON", "Форматирует, проверяет и минифицирует JSON с древовидным представлением."),
    ],
)

PAGES["ja"] = dict(
    title="タイムスタンプ変換ツール：Unix時間と日付の変換 | norito",
    meta_desc="Unixタイムスタンプと読みやすい日付をリアルタイムで双方向に変換。ローカル時間、UTC、ISO 8601形式に対応。",
    app_name="タイムスタンプ変換ツール", h1="タイムスタンプ変換ツール", breadcrumb_label="タイムスタンプ変換ツール",
    lede="Unixタイムスタンプを読みやすい日付に変換、またはその逆も可能。どちらを編集しても双方向がリアルタイムで同期します。",
    t=dict(
        unix_ts="Unixタイムスタンプ", timestamp="タイムスタンプ", unit="単位", seconds="秒", milliseconds="ミリ秒", now="現在",
        local_time="ローカル時間", utc="UTC", iso="ISO 8601", relative="相対表示",
        date_time="日付と時刻", pick_date="日付と時刻を選択（あなたのローカルタイムゾーン）",
        unix_seconds="Unix秒", unix_ms="Unixミリ秒", copy="コピー",
        faq1_q="Unixタイムスタンプとは？", faq1_short="1970年1月1日からの秒数（またはミリ秒数）。",
        faq1_a="Unixエポックは1970年1月1日UTC午前0時です。タイムスタンプはそれ以降経過した秒数（またはミリ秒数）にすぎず、そのためフォーマット済みの日付文字列とは異なり、単純な数値としてソートや比較ができます。",
        faq2_q="秒とミリ秒のタイムスタンプの違い",
        faq2_a="Unix、Linux、ほとんどのバックエンドAPIは秒を使用します。JavaScript自身の<code>Date.now()</code>やほとんどのフロントエンドコードはミリ秒を使用します。この2つを混同することは最もよくあるタイムスタンプのバグの一つで、「秒」の値を「ミリ秒」フィールドに貼り付けると1970年付近の日付になってしまいます。",
        how_h2="仕組み",
        how_p1="すべての処理はブラウザの<code>Date</code>オブジェクトを経由し、内部的には1つの数値のみを保持します。Unixエポック（1970年1月1日UTC午前0時）からのミリ秒数です。タイムスタンプを変換する際、秒を指定した場合はツールが1,000を掛けて<code>Date</code>を構築し、4つの形式で表示します。<code>toLocaleString</code>（ブラウザのIntlフォーマッターで、あなた自身のタイムゾーンと言語を使用）によるローカル時間、UTC、ISO 8601、そして現在との差を年・月・日・時間・分・秒に振り分けて計算する「3日後 / 2時間前」のような相対表示ラベルです。",
        how_p2="逆方向では、日付ピッカーの値がローカル時間として解析され、秒とミリ秒の両方に再変換されます。datetime-localフィールドは、まずタイムゾーンのオフセット分だけタイムスタンプをずらしてから値が設定されます。この部分は、多くの変換ツールが微妙に間違えやすい箇所です。<code>toISOString()</code>は常にUTCで表現するため、このずらし処理がないと、ピッカーには期待する壁時計時間から数時間ずれた時刻が表示されてしまいます。",
        how_p3="このツールが単位を明示することで防いでいる典型的なミスが、秒とミリ秒の混同です。現在のUnix時間は秒表記で10桁、ミリ秒表記で13桁です。ミリ秒の値を秒として解析すると、5万年以上先の未来に飛んでしまいます。逆の場合は1970年1月になります。変換結果がおかしいと感じたら、単位のドロップダウンを切り替えてみてください。ほとんどの場合、それが原因のすべてです。範囲外の値（JavaScriptの日付はエポックの前後それぞれ約1億日、おおよそ西暦275760年まで）は、意味不明な結果ではなく明確なエラーとして表示されます。",
        how_p4="すべての解析と整形はローカルのブラウザAPIの処理です。変換中にDevToolsのNetworkタブを開いてみてください。リクエストは一切発生せず、ログのタイムスタンプがあなたのマシンから外に出ることはありません。",
    ),
    related_tools=[
        ("uuid-generator.html", "UUIDジェネレーター", "ランダムなUUID v4識別子を一括生成。"),
        ("hash-generator.html", "ハッシュジェネレーター", "任意のテキストのMD5、SHA-1、SHA-256、SHA-512。"),
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証・圧縮し、ツリー表示できます。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "timestamp-converter.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-timestamp.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/timestamp-converter.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
