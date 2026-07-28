#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="M12 14v3l2 1"/></svg>'
ICON_CLASS = "c-purple"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field" style="margin-bottom:16px;">
          <label for="presetSelect">{t['common_patterns']}</label>
          <select id="presetSelect">
            <option value="">{t['choose_preset']}</option>
            <option value="* * * * *">{t['preset1']}</option>
            <option value="*/5 * * * *">{t['preset2']}</option>
            <option value="0 * * * *">{t['preset3']}</option>
            <option value="0 0 * * *">{t['preset4']}</option>
            <option value="0 9 * * 1-5">{t['preset5']}</option>
            <option value="0 0 1 * *">{t['preset6']}</option>
            <option value="30 14 * * 0">{t['preset7']}</option>
          </select>
        </div>

        <div class="field" style="margin-bottom:16px;">
          <label for="input">{t['cron_expr']}</label>
          <input type="text" id="input" class="mono-area" style="font-family:'JetBrains Mono',monospace;" value="*/15 9-17 * * 1-5" placeholder="* * * * *" />
          <p class="note" style="margin-top:6px; margin-bottom:0;">{t['field_hint']}</p>
        </div>

        <div class="result-box error" id="errorBox" style="display:none; margin-bottom:16px;">
          <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
          <div class="r-body"></div>
        </div>

        <div id="resultWrap" style="display:none;">
          <div class="result-box" style="margin-bottom:16px;">
            <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            <div class="r-body" id="description"></div>
          </div>
          <h3 style="margin-top:0;">{t['next5']}</h3>
          <ol id="nextRunsList" class="mono-area" style="list-style:decimal; padding-left:22px; line-height:2;"></ol>
          <p class="note">{t['based_on_tz']}</p>
        </div>
      </div>

      <div>
        <div class="panel">
          <div class="panel-header">
            <div class="icon-chip c-purple" style="width:36px;height:36px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="M12 14v3l2 1"/></svg>
            </div>
            <div>
              <h3>{t['side1_h']}</h3>
              <p>{t['side1_sub']}</p>
            </div>
          </div>
          <p class="note" style="margin-top:0;">
            {t['side1_body']}
          </p>
        </div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['side2_h']}</h3>
          <p class="note" style="margin-top:0;">
            {t['side2_body']}
          </p>
        </div>
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
    title="Analizador de Expresiones Cron: Explica y Previsualiza | norito",
    meta_desc="Pega una expresión cron para obtener una explicación en español sencillo y una vista previa de las próximas 5 ejecuciones. Funciona por completo en tu navegador.",
    app_name="Analizador de Expresiones Cron", h1="Analizador de Expresiones Cron", breadcrumb_label="Analizador de Expresiones Cron",
    lede="Pega una expresión cron y obtén una explicación en lenguaje sencillo más una vista previa de sus próximas 5 ejecuciones.",
    t=dict(
        common_patterns="Patrones comunes", choose_preset="Elige un preset...",
        preset1="Cada minuto", preset2="Cada 5 minutos", preset3="Cada hora, en punto",
        preset4="Cada día a medianoche", preset5="Cada día laborable a las 9:00 AM",
        preset6="El primer día de cada mes", preset7="Cada domingo a las 2:30 PM",
        cron_expr="Expresión cron", field_hint="Formato estándar de 5 campos: minuto hora día-del-mes mes día-de-la-semana.",
        next5="Próximas 5 ejecuciones", based_on_tz="Basado en la zona horaria local de tu navegador, ahora mismo.",
        side1_h="Los 5 campos", side1_sub="Minuto, hora, día del mes, mes, día de la semana.",
        side1_body='<code>*</code> significa "cada valor." <code>*/5</code> significa "cada 5 unidades." <code>1-5</code> es un rango. <code>1,3,5</code> es una lista. El día de la semana va de 0 (domingo) a 6 (sábado).',
        side2_h="Un ejemplo rápido",
        side2_body='<code>*/15 9-17 * * 1-5</code> significa "cada 15 minutos, entre las 9 AM y las 5 PM, de lunes a viernes." Prueba el desplegable de presets para más horarios comunes.',
        how_h2="Cómo funciona",
        how_p1='El analizador divide tu expresión en sus 5 campos y expande cada uno en un conjunto explícito de valores permitidos: <code>*/15</code> en el campo de minutos se convierte en el conjunto {0, 15, 30, 45}, <code>1-5</code> en día-de-la-semana se convierte en {1, 2, 3, 4, 5}, y listas como <code>1,3,5</code> se unen. Cada valor se verifica contra su rango al expandirse, por eso un error tipográfico como <code>61 * * * *</code> falla de inmediato con un mensaje que nombra el campo exacto y el rango esperado, en lugar de producir silenciosamente un horario que nunca se dispara.',
        how_p2='La lista de "próximas 5 ejecuciones" se calcula por fuerza bruta, y eso es una ventaja: comenzando desde el próximo minuto exacto, el código avanza un minuto a la vez (hasta un año, unas 527.000 comprobaciones, que toma unos pocos milisegundos) y prueba cada minuto candidato contra los conjuntos expandidos. Un efecto secundario útil de simular en vez de calcular: expresiones que son sintácticamente válidas pero que nunca pueden dispararse, como <code>0 0 30 2 *</code> (30 de febrero), no son un error, simplemente devuelven "no se encontró ninguna ejecución coincidente en el próximo año". Si ves ese mensaje, tu expresión se analiza bien pero describe una fecha que no existe o que está a más de un año de distancia.',
        how_p3="Todos los cálculos de fecha usan el objeto <code>Date</code> del navegador en tu zona horaria local, y todo se ejecuta en el JavaScript de esta página. Comprueba la pestaña Red de las DevTools: no se hace ninguna petición cuando escribes una expresión, así que nada sobre los horarios de tu infraestructura sale de tu máquina.",
    ),
    related_tools=[
        ("timestamp-converter.html", "Conversor de Timestamp", "Unix time a fecha, en ambas direcciones."),
        ("regex-tester.html", "Probador de Regex", "Prueba una expresión regular con resaltado de coincidencias en vivo."),
        ("json-formatter.html", "Formateador JSON", "Formatea, valida y minifica JSON."),
    ],
)

PAGES["zh"] = dict(
    title="Cron 表达式解析器：解释并预览下次运行时间 | norito",
    meta_desc="粘贴一个 cron 表达式，获取通俗易懂的解释以及接下来 5 次运行时间的预览。完全在浏览器中运行。",
    app_name="Cron 表达式解析器", h1="Cron 表达式解析器", breadcrumb_label="Cron 表达式解析器",
    lede="粘贴一个 cron 表达式，获取通俗易懂的解释，以及接下来 5 次运行时间的预览。",
    t=dict(
        common_patterns="常用模式", choose_preset="选择一个预设...",
        preset1="每分钟", preset2="每 5 分钟", preset3="每小时整点",
        preset4="每天午夜", preset5="每个工作日上午 9:00",
        preset6="每月第一天", preset7="每周日下午 2:30",
        cron_expr="Cron 表达式", field_hint="标准 5 字段格式：分钟 小时 日 月 星期。",
        next5="接下来 5 次运行", based_on_tz="基于你浏览器当前的本地时区。",
        side1_h="5 个字段", side1_sub="分钟、小时、日、月、星期。",
        side1_body='<code>*</code> 表示「每个值」。<code>*/5</code> 表示「每隔 5 个单位」。<code>1-5</code> 是一个范围。<code>1,3,5</code> 是一个列表。星期字段从 0（星期日）到 6（星期六）。',
        side2_h="一个简单示例",
        side2_body='<code>*/15 9-17 * * 1-5</code> 表示「周一至周五，上午 9 点到下午 5 点之间，每 15 分钟」。试试预设下拉菜单，查看更多常见的调度设置。',
        how_h2="工作原理",
        how_p1='解析器将你的表达式拆分成 5 个字段，并将每个字段展开成一组明确的允许值：分钟字段中的 <code>*/15</code> 会变成集合 {0, 15, 30, 45}，星期字段中的 <code>1-5</code> 会变成 {1, 2, 3, 4, 5}，而像 <code>1,3,5</code> 这样的列表会被合并在一起。每个值在展开时都会进行范围检查，这就是为什么像 <code>61 * * * *</code> 这样的拼写错误会立即失败，并给出明确指出具体字段和预期范围的错误提示，而不是悄无声息地生成一个永远不会触发的调度。',
        how_p2='「接下来 5 次运行」列表是通过暴力计算得出的，这其实是一个优点：从下一个整分钟开始，代码每次前进一分钟（最多推算一年，约 52.7 万次检查，只需几毫秒），并将每个候选分钟与展开后的集合进行比对。这种模拟而非直接计算的方式还有一个有用的副作用：像 <code>0 0 30 2 *</code>（2 月 30 日）这样语法正确但永远不会触发的表达式不会被当作错误，而是会返回「未来一年内未找到匹配的运行时间」。如果你看到这条提示，说明你的表达式解析没问题，但描述的日期要么不存在，要么在一年之后。',
        how_p3="所有日期计算都使用浏览器的 <code>Date</code> 对象，基于你的本地时区，并且全部在此页面的 JavaScript 中运行。查看开发者工具的 Network 标签页：输入表达式时不会发出任何请求，因此你基础设施的调度信息不会离开你的电脑。",
    ),
    related_tools=[
        ("timestamp-converter.html", "时间戳转换器", "Unix 时间与日期互转。"),
        ("regex-tester.html", "正则表达式测试工具", "测试正则表达式，实时高亮匹配结果。"),
        ("json-formatter.html", "JSON 格式化", "格式化、校验并压缩 JSON。"),
    ],
)

PAGES["ar"] = dict(
    title="محلّل تعبيرات Cron: اشرح وعاين مرات التشغيل القادمة | norito",
    meta_desc="الصق تعبير cron للحصول على شرح بلغة بسيطة ومعاينة لمرات التشغيل الخمس القادمة. يعمل بالكامل في متصفحك.",
    app_name="محلّل تعبيرات Cron", h1="محلّل تعبيرات Cron", breadcrumb_label="محلّل تعبيرات Cron",
    lede="الصق تعبير cron واحصل على شرح بلغة بسيطة بالإضافة إلى معاينة لمرات تشغيله الخمس القادمة.",
    t=dict(
        common_patterns="أنماط شائعة", choose_preset="اختر إعدادًا مسبقًا...",
        preset1="كل دقيقة", preset2="كل 5 دقائق", preset3="كل ساعة، عند الساعة تمامًا",
        preset4="كل يوم عند منتصف الليل", preset5="كل يوم عمل الساعة 9:00 صباحًا",
        preset6="أول يوم من كل شهر", preset7="كل يوم أحد الساعة 2:30 مساءً",
        cron_expr="تعبير Cron", field_hint="التنسيق القياسي المكوّن من 5 حقول: الدقيقة الساعة يوم-الشهر الشهر يوم-الأسبوع.",
        next5="مرات التشغيل الخمس القادمة", based_on_tz="بناءً على المنطقة الزمنية المحلية لمتصفحك، الآن.",
        side1_h="الحقول الخمسة", side1_sub="الدقيقة، الساعة، يوم الشهر، الشهر، يوم الأسبوع.",
        side1_body='<code>*</code> تعني «كل قيمة». <code>*/5</code> تعني «كل 5 وحدات». <code>1-5</code> نطاق. <code>1,3,5</code> قائمة. يوم الأسبوع يمتد من 0 (الأحد) إلى 6 (السبت).',
        side2_h="مثال سريع",
        side2_body='<code>*/15 9-17 * * 1-5</code> تعني «كل 15 دقيقة، بين الساعة 9 صباحًا و5 مساءً، من الاثنين إلى الجمعة». جرّب القائمة المنسدلة للإعدادات المسبقة لمزيد من الجداول الشائعة.',
        how_h2="كيف يعمل",
        how_p1='يقسّم المحلّل تعبيرك إلى حقوله الخمسة ويوسّع كل حقل إلى مجموعة صريحة من القيم المسموح بها: <code>*/15</code> في حقل الدقيقة يصبح المجموعة {0, 15, 30, 45}، و<code>1-5</code> في يوم الأسبوع يصبح {1, 2, 3, 4, 5}، والقوائم مثل <code>1,3,5</code> تُدمَج معًا. يُفحَص كل قيمة ضمن نطاقها أثناء توسيعها، ولهذا يفشل خطأ إملائي مثل <code>61 * * * *</code> فورًا برسالة تسمّي الحقل بالضبط والنطاق المتوقع، بدلًا من إنتاج جدول لا يعمل أبدًا بصمت.',
        how_p2='تُحسَب قائمة «مرات التشغيل الخمس القادمة» بالقوة الغاشمة، وهذه ميزة: بدءًا من الدقيقة الكاملة القادمة، يتقدم الكود دقيقة واحدة في كل مرة (حتى سنة كاملة، حوالي 527,000 فحص، يستغرق بضع مللي ثوانٍ) ويختبر كل دقيقة مرشحة مقابل المجموعات الموسّعة. أثر جانبي مفيد للمحاكاة بدلًا من الحساب: التعبيرات الصحيحة نحويًا لكن التي لا يمكن أن تعمل أبدًا، مثل <code>0 0 30 2 *</code> (30 فبراير)، ليست خطأً، بل تعود ببساطة برسالة «لم يُعثر على تشغيل مطابق في السنة القادمة». إذا رأيت هذه الرسالة، فإن تعبيرك يُحلَّل بشكل صحيح لكنه يصف تاريخًا غير موجود أو يبعد أكثر من سنة.',
        how_p3="كل حسابات التاريخ تستخدم كائن <code>Date</code> الخاص بالمتصفح في منطقتك الزمنية المحلية، وكل ذلك يعمل في جافاسكريبت هذه الصفحة. تحقّق من لسان Network في أدوات المطوّر: لا يُرسَل أي طلب عند كتابة تعبير، لذا لا شيء من جداول بنيتك التحتية يغادر جهازك.",
    ),
    related_tools=[
        ("timestamp-converter.html", "محول الطابع الزمني", "توقيت Unix إلى تاريخ، في كلا الاتجاهين."),
        ("regex-tester.html", "أداة اختبار Regex", "اختبر تعبيرًا نمطيًا مع تمييز مباشر للتطابقات."),
        ("json-formatter.html", "منسّق JSON", "تنسيق وتحقق وضغط JSON."),
    ],
)

PAGES["hi"] = dict(
    title="Cron एक्सप्रेशन पार्सर: समझाएं और अगले रन प्रीव्यू करें | norito",
    meta_desc="प्लेन-इंग्लिश एक्सप्लेनेशन और अगली 5 रन टाइम्स का प्रीव्यू पाने के लिए एक cron एक्सप्रेशन पेस्ट करें। पूरी तरह आपके ब्राउज़र में चलता है।",
    app_name="Cron एक्सप्रेशन पार्सर", h1="Cron एक्सप्रेशन पार्सर", breadcrumb_label="Cron एक्सप्रेशन पार्सर",
    lede="एक cron एक्सप्रेशन पेस्ट करें और उसकी अगली 5 रन टाइम्स के प्रीव्यू के साथ एक प्लेन-लैंग्वेज एक्सप्लेनेशन पाएं।",
    t=dict(
        common_patterns="कॉमन पैटर्न", choose_preset="एक प्रीसेट चुनें...",
        preset1="हर मिनट", preset2="हर 5 मिनट", preset3="हर घंटे, ठीक समय पर",
        preset4="हर दिन आधी रात को", preset5="हर वर्किंग डे सुबह 9:00 बजे",
        preset6="हर महीने का पहला दिन", preset7="हर रविवार दोपहर 2:30 बजे",
        cron_expr="Cron एक्सप्रेशन", field_hint="स्टैंडर्ड 5-फ़ील्ड फ़ॉर्मैट: मिनट घंटा दिन-का-महीना महीना दिन-का-हफ़्ता।",
        next5="अगली 5 रन", based_on_tz="अभी, आपके ब्राउज़र की लोकल टाइमज़ोन पर आधारित।",
        side1_h="5 फ़ील्ड्स", side1_sub="मिनट, घंटा, दिन-का-महीना, महीना, दिन-का-हफ़्ता।",
        side1_body='<code>*</code> का मतलब है "हर वैल्यू।" <code>*/5</code> का मतलब है "हर 5 यूनिट।" <code>1-5</code> एक रेंज है। <code>1,3,5</code> एक लिस्ट है। दिन-का-हफ़्ता 0 (रविवार) से 6 (शनिवार) तक चलता है।',
        side2_h="एक क्विक उदाहरण",
        side2_body='<code>*/15 9-17 * * 1-5</code> का मतलब है "हर 15 मिनट में, सुबह 9 बजे से शाम 5 बजे के बीच, सोमवार से शुक्रवार तक।" ज़्यादा कॉमन शेड्यूल्स के लिए प्रीसेट्स ड्रॉपडाउन आज़माएं।',
        how_h2="यह कैसे काम करता है",
        how_p1='पार्सर आपके एक्सप्रेशन को उसके 5 फ़ील्ड्स में बांटता है और हर एक को अनुमत वैल्यूज़ के एक स्पष्ट सेट में एक्सपैंड करता है: मिनट फ़ील्ड में <code>*/15</code> सेट {0, 15, 30, 45} बन जाता है, दिन-का-हफ़्ता में <code>1-5</code> {1, 2, 3, 4, 5} बन जाता है, और <code>1,3,5</code> जैसी लिस्ट्स को यूनियन किया जाता है। हर वैल्यू को एक्सपैंड करते समय रेंज-चेक किया जाता है, इसीलिए <code>61 * * * *</code> जैसा टाइपो एक ऐसा शेड्यूल चुपचाप बनाने के बजाय जो कभी फ़ायर ही न हो, तुरंत फ़ेल हो जाता है, और एक मैसेज दिखाता है जो सटीक फ़ील्ड और उसकी अपेक्षित रेंज बताता है।',
        how_p2='"अगली 5 रन" लिस्ट ब्रूट फ़ोर्स से कैलकुलेट होती है, और यह एक फ़ीचर है: अगले पूरे मिनट से शुरू करके, कोड एक बार में एक मिनट आगे बढ़ता है (एक साल तक, लगभग 527,000 चेक्स, जिसमें कुछ मिलीसेकंड लगते हैं) और हर कैंडिडेट मिनट को एक्सपैंडेड सेट्स के खिलाफ़ टेस्ट करता है। कैलकुलेट करने के बजाय सिम्युलेट करने का एक उपयोगी साइड इफ़ेक्ट: सिंटैक्टिकली वैलिड लेकिन कभी फ़ायर न होने वाले एक्सप्रेशन, जैसे <code>0 0 30 2 *</code> (30 फ़रवरी), एरर नहीं होते, वे बस "अगले साल में कोई मैचिंग रन नहीं मिला" के साथ वापस आते हैं। अगर आपको यह मैसेज दिखे, तो आपका एक्सप्रेशन ठीक से पार्स हो जाता है लेकिन एक ऐसी तारीख़ बताता है जो मौजूद नहीं है या एक साल से ज़्यादा दूर है।',
        how_p3="सारा डेट मैथ ब्राउज़र के <code>Date</code> ऑब्जेक्ट को आपकी लोकल टाइमज़ोन में इस्तेमाल करता है, और यह सब इस पेज के JavaScript में चलता है। डेवटूल्स का Network टैब चेक करें: एक्सप्रेशन टाइप करते समय कोई रिक्वेस्ट नहीं होती, इसलिए आपके इंफ्रास्ट्रक्चर के शेड्यूल्स के बारे में कुछ भी आपकी मशीन से बाहर नहीं जाता।",
    ),
    related_tools=[
        ("timestamp-converter.html", "टाइमस्टैंप कन्वर्टर", "Unix टाइम से तारीख़, दोनों दिशाओं में।"),
        ("regex-tester.html", "Regex टेस्टर", "लाइव मैच हाइलाइटिंग के साथ एक regex टेस्ट करें।"),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "JSON फ़ॉर्मैट, वैलिडेट और मिनिफ़ाई करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Парсер cron-выражений: объяснение и предпросмотр запусков | norito",
    meta_desc="Вставьте cron-выражение, чтобы получить объяснение простым языком и предпросмотр следующих 5 запусков. Работает полностью в браузере.",
    app_name="Парсер cron-выражений", h1="Парсер cron-выражений", breadcrumb_label="Парсер cron-выражений",
    lede="Вставьте cron-выражение и получите объяснение простым языком, а также предпросмотр следующих 5 запусков.",
    t=dict(
        common_patterns="Частые шаблоны", choose_preset="Выберите готовый вариант...",
        preset1="Каждую минуту", preset2="Каждые 5 минут", preset3="Каждый час, ровно",
        preset4="Каждый день в полночь", preset5="Каждый будний день в 9:00",
        preset6="Первое число каждого месяца", preset7="Каждое воскресенье в 14:30",
        cron_expr="Cron-выражение", field_hint="Стандартный 5-полевой формат: минута час день-месяца месяц день-недели.",
        next5="Следующие 5 запусков", based_on_tz="На основе местного часового пояса вашего браузера, прямо сейчас.",
        side1_h="5 полей", side1_sub="Минута, час, день месяца, месяц, день недели.",
        side1_body='<code>*</code> означает «любое значение». <code>*/5</code> означает «каждые 5 единиц». <code>1-5</code> — диапазон. <code>1,3,5</code> — список. День недели от 0 (воскресенье) до 6 (суббота).',
        side2_h="Быстрый пример",
        side2_body='<code>*/15 9-17 * * 1-5</code> означает «каждые 15 минут, с 9:00 до 17:00, с понедельника по пятницу». Попробуйте выпадающий список готовых вариантов для других частых расписаний.',
        how_h2="Как это работает",
        how_p1='Парсер разбивает ваше выражение на 5 полей и разворачивает каждое в явный набор допустимых значений: <code>*/15</code> в поле минут превращается в набор {0, 15, 30, 45}, <code>1-5</code> в дне недели превращается в {1, 2, 3, 4, 5}, а списки вроде <code>1,3,5</code> объединяются. Каждое значение проверяется на диапазон при разворачивании, поэтому опечатка вроде <code>61 * * * *</code> сразу выдаёт ошибку с указанием конкретного поля и ожидаемого диапазона, вместо того чтобы незаметно создать расписание, которое никогда не сработает.',
        how_p2='Список «следующие 5 запусков» вычисляется методом перебора, и это преимущество: начиная со следующей целой минуты, код продвигается на минуту за раз (до года вперёд, около 527 000 проверок, что занимает несколько миллисекунд) и проверяет каждую кандидатную минуту на соответствие развёрнутым наборам. Полезный побочный эффект симуляции вместо вычисления: синтаксически корректные, но никогда не срабатывающие выражения, например <code>0 0 30 2 *</code> (30 февраля), не считаются ошибкой — они просто возвращают «подходящий запуск не найден в течение следующего года». Если вы видите это сообщение, значит ваше выражение разбирается корректно, но описывает дату, которая не существует или отстоит более чем на год.',
        how_p3="Все вычисления дат используют объект <code>Date</code> браузера в вашем местном часовом поясе, и всё это работает в JavaScript этой страницы. Проверьте вкладку Network в DevTools: при вводе выражения не отправляется ни одного запроса, поэтому ничего о расписаниях вашей инфраструктуры не покидает ваш компьютер.",
    ),
    related_tools=[
        ("timestamp-converter.html", "Конвертер меток времени", "Unix-время в дату и обратно."),
        ("regex-tester.html", "Тестер регулярных выражений", "Проверьте regex с подсветкой совпадений в реальном времени."),
        ("json-formatter.html", "Форматирование JSON", "Форматирует, проверяет и минифицирует JSON."),
    ],
)

PAGES["ja"] = dict(
    title="Cron式パーサー：説明と次回実行のプレビュー | norito",
    meta_desc="cron式を貼り付けると、わかりやすい説明と次の5回の実行時刻のプレビューが得られます。すべてブラウザ内で完結します。",
    app_name="Cron式パーサー", h1="Cron式パーサー", breadcrumb_label="Cron式パーサー",
    lede="cron式を貼り付けると、わかりやすい説明と、次の5回の実行時刻のプレビューが表示されます。",
    t=dict(
        common_patterns="よく使うパターン", choose_preset="プリセットを選択...",
        preset1="毎分", preset2="5分ごと", preset3="毎時、正時に",
        preset4="毎日深夜0時", preset5="平日の午前9時",
        preset6="毎月1日", preset7="毎週日曜日の午後2時30分",
        cron_expr="Cron式", field_hint="標準的な5フィールド形式：分 時 日 月 曜日。",
        next5="次の5回の実行", based_on_tz="現在のブラウザのローカルタイムゾーンに基づきます。",
        side1_h="5つのフィールド", side1_sub="分、時、日、月、曜日。",
        side1_body='<code>*</code>は「すべての値」を意味します。<code>*/5</code>は「5単位ごと」を意味します。<code>1-5</code>は範囲です。<code>1,3,5</code>はリストです。曜日は0（日曜）から6（土曜）です。',
        side2_h="簡単な例",
        side2_body='<code>*/15 9-17 * * 1-5</code>は「月曜日から金曜日、午前9時から午後5時の間、15分ごと」を意味します。他のよくあるスケジュールについてはプリセットのドロップダウンを試してください。',
        how_h2="仕組み",
        how_p1='パーサーはあなたの式を5つのフィールドに分割し、それぞれを許可される値の明示的な集合に展開します。分フィールドの<code>*/15</code>は{0, 15, 30, 45}という集合になり、曜日フィールドの<code>1-5</code>は{1, 2, 3, 4, 5}になり、<code>1,3,5</code>のようなリストは結合されます。展開時にすべての値が範囲チェックされるため、<code>61 * * * *</code>のような誤入力は、決して実行されないスケジュールを黙って生成する代わりに、正確なフィールド名と期待される範囲を示すメッセージとともに即座に失敗します。',
        how_p2='「次の5回の実行」リストは総当たりで計算されており、それが利点でもあります。次の正分から始めて、コードは1分ずつ前進し（最大1年分、約52万7000回のチェックで、数ミリ秒しかかかりません）、各候補の分を展開された集合と照合します。計算ではなくシミュレーションすることの有用な副作用として、構文的には正しいが決して実行されない式（例えば2月30日を指す<code>0 0 30 2 *</code>）はエラーにならず、「今後1年間に一致する実行が見つかりませんでした」という結果が返されるだけです。このメッセージが表示された場合、式自体は問題なく解析されていますが、存在しない日付か、1年以上先の日付を指しています。',
        how_p3="すべての日付計算はあなたのローカルタイムゾーンでブラウザの<code>Date</code>オブジェクトを使用し、すべてこのページのJavaScript内で実行されます。DevToolsのNetworkタブを確認してみてください。式を入力してもリクエストは発生せず、あなたのインフラのスケジュールに関する情報はマシンの外に出ることはありません。",
    ),
    related_tools=[
        ("timestamp-converter.html", "タイムスタンプ変換ツール", "Unix時間と日付を双方向に変換。"),
        ("regex-tester.html", "正規表現テストツール", "正規表現をリアルタイムのハイライト付きでテスト。"),
        ("json-formatter.html", "JSONフォーマッタ", "JSONを整形・検証・圧縮。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "cron-expression-parser.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-cron-parser.js"],
        use_foot_scripts_head=False,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/cron-expression-parser.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
