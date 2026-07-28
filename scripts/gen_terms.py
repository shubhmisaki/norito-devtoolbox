#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

LOCS = ["", "es", "zh", "ar", "hi", "ru", "ja"]
DIR = {"ar": "rtl"}

TITLE = {
    "": "Terms of Service | norito",
    "es": "Términos de servicio | norito",
    "zh": "服务条款 | norito",
    "ar": "شروط الخدمة | norito",
    "hi": "सेवा की शर्तें | norito",
    "ru": "Условия использования | norito",
    "ja": "利用規約 | norito",
}
META_DESC = {
    "": "The terms for using norito's free browser-based tools: acceptable use, no warranty, and limitation of liability.",
    "es": "Los términos para usar las herramientas gratuitas basadas en navegador de norito: uso aceptable, sin garantía, y limitación de responsabilidad.",
    "zh": "使用 norito 免费浏览器工具的条款：可接受使用、无担保声明，以及责任限制。",
    "ar": "شروط استخدام أدوات norito المجانية القائمة على المتصفح: الاستخدام المقبول، عدم الضمان، وحدود المسؤولية.",
    "hi": "norito के मुफ़्त ब्राउज़र-आधारित टूल्स इस्तेमाल करने की शर्तें: स्वीकार्य उपयोग, कोई वारंटी नहीं, और दायित्व की सीमा।",
    "ru": "Условия использования бесплатных браузерных инструментов norito: допустимое использование, отсутствие гарантий и ограничение ответственности.",
    "ja": "norito の無料ブラウザベースツールの利用規約：許容される使用方法、無保証、および責任の制限について。",
}
BREADCRUMB_LABEL = {
    "": "Terms of Service", "es": "Términos de servicio", "zh": "服务条款",
    "ar": "شروط الخدمة", "hi": "सेवा की शर्तें", "ru": "Условия использования", "ja": "利用規約",
}
LAST_UPDATED = {
    "": "Last updated: July 2026.",
    "es": "Última actualización: julio de 2026.",
    "zh": "最后更新：2026 年 7 月。",
    "ar": "آخر تحديث: يوليو 2026.",
    "hi": "आख़िरी अपडेट: जुलाई 2026.",
    "ru": "Последнее обновление: июль 2026 г.",
    "ja": "最終更新日：2026年7月。",
}

# body content: dict of loc -> dict(lede, h2_1..h2_9 / p1..p9-ish, contact_p)
C = {}

C[""] = dict(
    lede="By using norito, you agree to these terms. They're short because the service is simple: free browser-based tools with no accounts and no server-side processing of your files.",
    h2_1="Acceptance of these terms", p1="Using any tool on norito means you accept these terms. If you don't agree with them, the only requirement is that you stop using the site, there's no account to cancel and nothing else to undo.",
    h2_2="What norito is", p2="norito is a collection of free, browser-based utilities, image compression, PDF tools, text and developer formatters, and similar. Each tool runs as JavaScript in your browser tab and processes your files locally, without uploading them to a server, except where a tool's own page explicitly says otherwise.",
    h2_3="Acceptable use", p3="You agree not to use norito to process content you don't have the right to process, to attempt to disrupt, overload, or reverse-engineer the site for malicious purposes, or to use automated scripts to scrape or hammer the site in a way that degrades it for other users. Beyond that, use the tools however you like, for personal or commercial work.",
    h2_4="No accounts, your files stay yours", p4="norito doesn't have user accounts, and since most tools run locally in your browser, we never receive, store, or have access to the files or text you process. You retain full ownership and responsibility for anything you create or process with these tools.",
    h2_5="Intellectual property", p5="The norito name, logo, and site design belong to norito. The code that runs the tools is provided for use through the website; it isn't licensed to you for redistribution or resale as your own product. Content you generate using the tools, compressed images, converted files, generated text, is entirely yours.",
    h2_6="Third-party services", p6="norito displays ads through Google AdSense and loads fonts from Google Fonts, both of which involve requests to third-party servers as described in the <a href=\"privacy.html\">Privacy Policy</a>. norito isn't responsible for the content, availability, or practices of these third-party services.",
    h2_7="No warranty", p7="norito is provided “as is,” without warranty of any kind, express or implied. We don't guarantee the tools will be error-free, available at all times, or suitable for any particular purpose. Always keep your own backup of important files before processing them with any online tool, this one included.",
    h2_8="Limitation of liability", p8="To the fullest extent permitted by law, norito and its operator aren't liable for any indirect, incidental, or consequential damages arising from your use of the site, including data loss or corrupted output. Your sole remedy if you're unhappy with the service is to stop using it.",
    h2_9="Changes to these terms", p9="These terms may be updated as the site evolves, most likely when new tools are added. Continued use of norito after a change means you accept the updated terms.",
    contact_p="Questions about these terms can be sent to",
)

C["es"] = dict(
    lede="Al usar norito, aceptas estos términos. Son breves porque el servicio es simple: herramientas gratuitas basadas en el navegador, sin cuentas y sin procesamiento de tus archivos en el servidor.",
    h2_1="Aceptación de estos términos", p1="Usar cualquier herramienta de norito significa que aceptas estos términos. Si no estás de acuerdo con ellos, el único requisito es que dejes de usar el sitio, no hay cuenta que cancelar ni nada más que deshacer.",
    h2_2="Qué es norito", p2="norito es una colección de utilidades gratuitas basadas en el navegador: compresión de imágenes, herramientas de PDF, formateadores de texto y de desarrollo, y similares. Cada herramienta funciona como JavaScript en la pestaña de tu navegador y procesa tus archivos localmente, sin subirlos a un servidor, salvo que la página de la propia herramienta indique explícitamente lo contrario.",
    h2_3="Uso aceptable", p3="Aceptas no usar norito para procesar contenido sobre el que no tengas derecho a hacerlo, no intentar interrumpir, sobrecargar o realizar ingeniería inversa del sitio con fines maliciosos, ni usar scripts automatizados para extraer datos o saturar el sitio de una forma que lo degrade para otros usuarios. Más allá de eso, usa las herramientas como quieras, para trabajo personal o comercial.",
    h2_4="Sin cuentas, tus archivos siguen siendo tuyos", p4="norito no tiene cuentas de usuario, y como la mayoría de las herramientas funcionan localmente en tu navegador, nunca recibimos, almacenamos ni tenemos acceso a los archivos o textos que procesas. Conservas la propiedad total y la responsabilidad de todo lo que crees o proceses con estas herramientas.",
    h2_5="Propiedad intelectual", p5="El nombre de norito, el logotipo y el diseño del sitio pertenecen a norito. El código que ejecuta las herramientas se proporciona para su uso a través del sitio web; no se te licencia para su redistribución o reventa como producto propio. El contenido que generas usando las herramientas, imágenes comprimidas, archivos convertidos, texto generado, es completamente tuyo.",
    h2_6="Servicios de terceros", p6="norito muestra anuncios a través de Google AdSense y carga fuentes desde Google Fonts, ambos implican solicitudes a servidores de terceros como se describe en la <a href=\"privacy.html\">Política de privacidad</a>. norito no es responsable del contenido, la disponibilidad ni las prácticas de estos servicios de terceros.",
    h2_7="Sin garantía", p7="norito se proporciona “tal cual”, sin garantía de ningún tipo, expresa o implícita. No garantizamos que las herramientas estén libres de errores, disponibles en todo momento, o adecuadas para un propósito particular. Mantén siempre tu propia copia de seguridad de los archivos importantes antes de procesarlos con cualquier herramienta en línea, esta incluida.",
    h2_8="Limitación de responsabilidad", p8="En la máxima medida permitida por la ley, norito y su operador no son responsables de ningún daño indirecto, incidental o consecuente derivado del uso del sitio, incluida la pérdida de datos o resultados dañados. Tu único recurso si no estás satisfecho con el servicio es dejar de usarlo.",
    h2_9="Cambios a estos términos", p9="Estos términos pueden actualizarse a medida que el sitio evoluciona, lo más probable cuando se añadan nuevas herramientas. Seguir usando norito después de un cambio significa que aceptas los términos actualizados.",
    contact_p="Las preguntas sobre estos términos pueden enviarse a",
)

C["zh"] = dict(
    lede="使用 norito 即表示你同意这些条款。它们很简短，因为这项服务很简单：免费的基于浏览器的工具，没有账户，也不在服务器端处理你的文件。",
    h2_1="接受这些条款", p1="使用 norito 上的任何工具即表示你接受这些条款。如果你不同意，唯一的要求是停止使用本网站——没有需要取消的账户，也没有其他需要撤销的东西。",
    h2_2="norito 是什么", p2="norito 是一系列免费的基于浏览器的实用工具集合：图片压缩、PDF 工具、文本和开发者格式化工具等等。每个工具都作为 JavaScript 在你的浏览器标签页中运行，并在本地处理你的文件，不会上传到服务器，除非工具自身的页面明确说明并非如此。",
    h2_3="可接受的使用方式", p3="你同意不使用 norito 来处理你无权处理的内容，不试图出于恶意目的干扰、过载或逆向工程本网站，也不使用自动化脚本以损害其他用户体验的方式抓取或冲击本网站。除此之外，无论是个人还是商业用途，你都可以随意使用这些工具。",
    h2_4="没有账户，你的文件始终属于你", p4="norito 没有用户账户，并且由于大多数工具都在你的浏览器本地运行，我们从不接收、存储或访问你处理的文件或文本。你对使用这些工具创建或处理的任何内容都保留完全的所有权和责任。",
    h2_5="知识产权", p5="norito 的名称、标志和网站设计归 norito 所有。运行这些工具的代码仅供通过本网站使用；并未授权你将其重新分发或作为你自己的产品转售。你使用这些工具生成的内容——压缩后的图片、转换后的文件、生成的文本——完全属于你。",
    h2_6="第三方服务", p6="norito 通过 Google AdSense 展示广告，并从 Google Fonts 加载字体，这两者都涉及向第三方服务器发出请求，具体说明见<a href=\"privacy.html\">隐私政策</a>。norito 不对这些第三方服务的内容、可用性或做法负责。",
    h2_7="不提供担保", p7="norito 按“现状”提供，不提供任何形式的明示或暗示担保。我们不保证这些工具没有错误、始终可用，或适用于任何特定目的。在使用任何在线工具（包括本站）处理重要文件之前，请务必自行保留备份。",
    h2_8="责任限制", p8="在法律允许的最大范围内，norito 及其运营者对因使用本网站而产生的任何间接、附带或后果性损害（包括数据丢失或输出损坏）不承担责任。如果你对本服务不满意，唯一的补救办法是停止使用它。",
    h2_9="条款变更", p9="随着网站的发展，这些条款可能会更新，最常见的情况是新增工具时。条款变更后继续使用 norito，即表示你接受更新后的条款。",
    contact_p="有关这些条款的问题可以发送至",
)

C["ar"] = dict(
    lede="باستخدامك norito، فإنك توافق على هذه الشروط. إنها قصيرة لأن الخدمة بسيطة: أدوات مجانية قائمة على المتصفح دون حسابات ودون معالجة ملفاتك من جانب الخادم.",
    h2_1="قبول هذه الشروط", p1="استخدام أي أداة على norito يعني أنك تقبل هذه الشروط. إذا كنت لا توافق عليها، فالمطلب الوحيد هو التوقف عن استخدام الموقع، لا يوجد حساب لإلغائه ولا شيء آخر للتراجع عنه.",
    h2_2="ما هو norito", p2="norito هو مجموعة من الأدوات المجانية القائمة على المتصفح: ضغط الصور، أدوات PDF، منسقات النصوص والمطورين، وما شابه. كل أداة تعمل كجافاسكريبت في تبويب متصفحك وتعالج ملفاتك محليًا، دون رفعها إلى خادم، إلا إذا نصت صفحة الأداة نفسها صراحةً على خلاف ذلك.",
    h2_3="الاستخدام المقبول", p3="أنت توافق على عدم استخدام norito لمعالجة محتوى ليس لديك الحق في معالجته، وعدم محاولة تعطيل الموقع أو إثقاله أو إجراء هندسة عكسية له لأغراض ضارة، وعدم استخدام نصوص برمجية آلية لكشط الموقع أو إثقاله بطريقة تُضعف تجربته لمستخدمين آخرين. بخلاف ذلك، استخدم الأدوات كما تشاء، لعمل شخصي أو تجاري.",
    h2_4="بلا حسابات، ملفاتك تبقى ملكك", p4="لا يملك norito حسابات مستخدمين، وبما أن معظم الأدوات تعمل محليًا في متصفحك، فإننا لا نستقبل أو نخزّن أو نصل أبدًا إلى الملفات أو النصوص التي تعالجها. تحتفظ بالملكية الكاملة والمسؤولية عن أي شيء تنشئه أو تعالجه باستخدام هذه الأدوات.",
    h2_5="الملكية الفكرية", p5="اسم norito وشعاره وتصميم الموقع ملك لـ norito. الكود الذي يشغّل الأدوات مُقدَّم للاستخدام عبر الموقع؛ ولست مرخَّصًا بإعادة توزيعه أو إعادة بيعه كمنتج خاص بك. المحتوى الذي تولّده باستخدام الأدوات، كالصور المضغوطة والملفات المحوَّلة والنصوص المولَّدة، هو ملكك بالكامل.",
    h2_6="خدمات الطرف الثالث", p6="يعرض norito إعلانات عبر Google AdSense ويحمّل خطوطًا من Google Fonts، وكلاهما يتضمن طلبات إلى خوادم طرف ثالث كما هو موصوف في <a href=\"privacy.html\">سياسة الخصوصية</a>. norito غير مسؤول عن محتوى أو توفر أو ممارسات خدمات الطرف الثالث هذه.",
    h2_7="بلا ضمان", p7="يُقدَّم norito «كما هو»، دون أي ضمان من أي نوع، صريح أو ضمني. نحن لا نضمن أن الأدوات ستكون خالية من الأخطاء، أو متاحة طوال الوقت، أو مناسبة لأي غرض معين. احتفظ دائمًا بنسخة احتياطية خاصة بك من الملفات المهمة قبل معالجتها بأي أداة عبر الإنترنت، بما في ذلك هذه الأداة.",
    h2_8="حدود المسؤولية", p8="إلى أقصى حد يسمح به القانون، لا يتحمل norito ومشغّله المسؤولية عن أي أضرار غير مباشرة أو عرضية أو تبعية ناشئة عن استخدامك للموقع، بما في ذلك فقدان البيانات أو تلف المخرجات. تعويضك الوحيد إذا لم تكن راضيًا عن الخدمة هو التوقف عن استخدامها.",
    h2_9="التغييرات على هذه الشروط", p9="قد يتم تحديث هذه الشروط مع تطور الموقع، على الأرجح عند إضافة أدوات جديدة. استمرار استخدام norito بعد أي تغيير يعني أنك تقبل الشروط المحدَّثة.",
    contact_p="يمكن إرسال الأسئلة حول هذه الشروط إلى",
)

C["hi"] = dict(
    lede="norito इस्तेमाल करके, आप इन शर्तों से सहमत होते हैं। ये छोटी हैं क्योंकि सेवा सिंपल है: बिना अकाउंट और बिना आपकी फ़ाइलों की सर्वर-साइड प्रोसेसिंग वाले मुफ़्त ब्राउज़र-आधारित टूल्स।",
    h2_1="इन शर्तों की स्वीकृति", p1="norito पर किसी भी टूल का इस्तेमाल करने का मतलब है कि आप इन शर्तों को स्वीकार करते हैं। अगर आप इनसे सहमत नहीं हैं, तो सिर्फ़ एक ज़रूरत है कि आप साइट इस्तेमाल करना बंद कर दें, कैंसल करने के लिए कोई अकाउंट नहीं है और पूर्ववत करने के लिए कुछ और नहीं है।",
    h2_2="norito क्या है", p2="norito मुफ़्त, ब्राउज़र-आधारित यूटिलिटीज़ का एक कलेक्शन है, इमेज कंप्रेशन, PDF टूल्स, टेक्स्ट और डेवलपर फ़ॉर्मैटर्स, और इसी तरह के अन्य। हर टूल आपके ब्राउज़र टैब में JavaScript के रूप में चलता है और आपकी फ़ाइलों को लोकली प्रोसेस करता है, बिना उन्हें सर्वर पर अपलोड किए, सिवाय उन मामलों के जहां किसी टूल का अपना पेज साफ़ तौर पर कुछ और कहता है।",
    h2_3="स्वीकार्य इस्तेमाल", p3="आप norito का इस्तेमाल ऐसे कंटेंट को प्रोसेस करने के लिए न करने पर सहमत होते हैं जिसे प्रोसेस करने का आपके पास अधिकार नहीं है, मैलिशियस मक़सद से साइट को बाधित करने, ओवरलोड करने, या रिवर्स-इंजीनियर करने की कोशिश न करने पर, या साइट को स्क्रैप करने या इस तरह हैमर करने के लिए ऑटोमेटेड स्क्रिप्ट्स इस्तेमाल न करने पर सहमत होते हैं जो इसे दूसरे यूज़र्स के लिए ख़राब कर दे। इसके अलावा, टूल्स को जैसे चाहें इस्तेमाल करें, पर्सनल या कमर्शियल काम के लिए।",
    h2_4="कोई अकाउंट नहीं, आपकी फ़ाइलें आपकी ही रहती हैं", p4="norito के पास यूज़र अकाउंट नहीं हैं, और चूंकि ज़्यादातर टूल्स आपके ब्राउज़र में लोकली चलते हैं, हम कभी भी आपकी प्रोसेस की गई फ़ाइलों या टेक्स्ट को प्राप्त, स्टोर, या एक्सेस नहीं करते। आप इन टूल्स से जो कुछ भी बनाते या प्रोसेस करते हैं उसका पूरा स्वामित्व और ज़िम्मेदारी आपकी बनी रहती है।",
    h2_5="बौद्धिक संपदा", p5="norito का नाम, लोगो, और साइट डिज़ाइन norito का है। टूल्स चलाने वाला कोड वेबसाइट के ज़रिए इस्तेमाल के लिए प्रदान किया जाता है; इसे आपको अपने ख़ुद के प्रोडक्ट के रूप में दोबारा वितरित करने या फिर से बेचने का लाइसेंस नहीं दिया गया है। टूल्स का इस्तेमाल करके आप जो कंटेंट बनाते हैं, कंप्रेस्ड इमेज, कन्वर्ट की गई फ़ाइलें, जनरेट किया गया टेक्स्ट, पूरी तरह आपका है।",
    h2_6="थर्ड-पार्टी सर्विसेज़", p6="norito Google AdSense के ज़रिए विज्ञापन दिखाता है और Google Fonts से फ़ॉन्ट लोड करता है, दोनों में थर्ड-पार्टी सर्वर को रिक्वेस्ट शामिल है जैसा <a href=\"privacy.html\">प्राइवेसी पॉलिसी</a> में बताया गया है। norito इन थर्ड-पार्टी सर्विसेज़ के कंटेंट, उपलब्धता, या प्रैक्टिस के लिए ज़िम्मेदार नहीं है।",
    h2_7="कोई वारंटी नहीं", p7="norito “जैसा है वैसा” प्रदान किया जाता है, बिना किसी तरह की वारंटी के, स्पष्ट या निहित। हम गारंटी नहीं देते कि टूल्स एरर-फ़्री होंगे, हर समय उपलब्ध रहेंगे, या किसी ख़ास मक़सद के लिए उपयुक्त होंगे। किसी भी ऑनलाइन टूल से, इसे भी शामिल करते हुए, महत्वपूर्ण फ़ाइलों को प्रोसेस करने से पहले हमेशा अपना ख़ुद का बैकअप रखें।",
    h2_8="दायित्व की सीमा", p8="क़ानून द्वारा अनुमत पूरी सीमा तक, norito और इसका ऑपरेटर साइट के इस्तेमाल से होने वाले किसी भी इनडायरेक्ट, इंसीडेंटल, या कॉन्सीक्वेंशियल डैमेज के लिए ज़िम्मेदार नहीं हैं, जिसमें डेटा लॉस या ख़राब हुआ आउटपुट शामिल है। अगर आप सर्विस से नाख़ुश हैं, तो आपका एकमात्र उपाय इसका इस्तेमाल बंद करना है।",
    h2_9="इन शर्तों में बदलाव", p9="जैसे-जैसे साइट डेवलप होती है, ये शर्तें अपडेट हो सकती हैं, ज़्यादातर तब जब नए टूल्स जोड़े जाते हैं। बदलाव के बाद norito का इस्तेमाल जारी रखने का मतलब है कि आप अपडेटेड शर्तों को स्वीकार करते हैं।",
    contact_p="इन शर्तों के बारे में सवाल यहां भेजे जा सकते हैं",
)

C["ru"] = dict(
    lede="Используя norito, вы соглашаетесь с этими условиями. Они короткие, потому что сервис простой: бесплатные браузерные инструменты без учётных записей и без серверной обработки ваших файлов.",
    h2_1="Принятие настоящих условий", p1="Использование любого инструмента на norito означает, что вы принимаете эти условия. Если вы не согласны с ними, единственное требование — прекратить использование сайта; нет учётной записи для отмены и больше нечего отменять.",
    h2_2="Что такое norito", p2="norito — это набор бесплатных браузерных утилит: сжатие изображений, инструменты для PDF, форматирование текста и инструменты для разработчиков и тому подобное. Каждый инструмент работает как JavaScript во вкладке вашего браузера и обрабатывает ваши файлы локально, не загружая их на сервер, за исключением случаев, когда страница самого инструмента прямо указывает иное.",
    h2_3="Допустимое использование", p3="Вы соглашаетесь не использовать norito для обработки контента, на обработку которого у вас нет прав, не пытаться нарушать работу сайта, перегружать его или проводить обратную разработку в злонамеренных целях, а также не использовать автоматизированные скрипты для сбора данных или атак на сайт способом, ухудшающим его работу для других пользователей. В остальном используйте инструменты как вам угодно, для личной или коммерческой работы.",
    h2_4="Без учётных записей, ваши файлы остаются вашими", p4="У norito нет учётных записей пользователей, и поскольку большинство инструментов работают локально в вашем браузере, мы никогда не получаем, не храним и не имеем доступа к файлам или тексту, которые вы обрабатываете. Вы сохраняете полное право собственности и ответственность за всё, что вы создаёте или обрабатываете с помощью этих инструментов.",
    h2_5="Интеллектуальная собственность", p5="Название norito, логотип и дизайн сайта принадлежат norito. Код, на котором работают инструменты, предоставляется для использования через веб-сайт; он не лицензирован вам для распространения или перепродажи в качестве собственного продукта. Контент, который вы создаёте с помощью инструментов — сжатые изображения, конвертированные файлы, сгенерированный текст — полностью принадлежит вам.",
    h2_6="Сторонние сервисы", p6="norito показывает рекламу через Google AdSense и загружает шрифты из Google Fonts, оба варианта предполагают запросы к серверам третьих сторон, как описано в <a href=\"privacy.html\">Политике конфиденциальности</a>. norito не несёт ответственности за содержание, доступность или практики этих сторонних сервисов.",
    h2_7="Отсутствие гарантий", p7="norito предоставляется «как есть», без каких-либо гарантий, явных или подразумеваемых. Мы не гарантируем, что инструменты будут безошибочными, доступными в любое время или подходящими для какой-либо конкретной цели. Всегда сохраняйте собственную резервную копию важных файлов перед обработкой их любым онлайн-инструментом, включая этот.",
    h2_8="Ограничение ответственности", p8="В максимальной степени, допустимой законом, norito и его оператор не несут ответственности за любые косвенные, случайные или последующие убытки, возникающие в результате использования вами сайта, включая потерю данных или повреждённый результат. Ваше единственное средство правовой защиты, если вы недовольны сервисом, — прекратить его использование.",
    h2_9="Изменения настоящих условий", p9="Эти условия могут обновляться по мере развития сайта, чаще всего при добавлении новых инструментов. Продолжение использования norito после изменения означает, что вы принимаете обновлённые условия.",
    contact_p="Вопросы об этих условиях можно отправлять на",
)

C["ja"] = dict(
    lede="norito を利用することで、あなたはこれらの規約に同意したことになります。サービスがシンプルであるため、規約も短くまとめています。無料のブラウザベースツールであり、アカウントもサーバー側でのファイル処理もありません。",
    h2_1="本規約への同意", p1="norito のいずれかのツールを使用することは、本規約に同意することを意味します。同意しない場合、必要なのはサイトの利用を停止することだけです。解約すべきアカウントも、取り消すべきその他の事項もありません。",
    h2_2="norito とは", p2="norito は、画像圧縮、PDFツール、テキストおよび開発者向けフォーマッターなど、無料のブラウザベースユーティリティの集合体です。各ツールはブラウザタブ内でJavaScriptとして動作し、ツール自体のページで明示的に別の記載がない限り、ファイルをサーバーにアップロードすることなくローカルで処理します。",
    h2_3="許容される利用", p3="あなたは、処理する権利のないコンテンツを norito で処理しないこと、悪意ある目的でサイトを妨害・過負荷・リバースエンジニアリングしようとしないこと、また他のユーザーの利用体験を損なうような方法でサイトをスクレイピングしたり負荷をかけたりする自動化スクリプトを使用しないことに同意します。それ以外については、個人利用でも商用利用でも、自由にツールを使用できます。",
    h2_4="アカウントなし、あなたのファイルはあなたのもの", p4="norito にはユーザーアカウントがなく、ほとんどのツールはブラウザ内でローカルに動作するため、私たちはあなたが処理するファイルやテキストを受け取ることも、保存することも、アクセスすることも一切ありません。これらのツールを使用して作成または処理したものについては、完全な所有権と責任があなたに帰属します。",
    h2_5="知的財産権", p5="norito の名称、ロゴ、サイトデザインは norito に帰属します。ツールを動作させるコードはウェブサイトを通じての使用のために提供されており、自分自身の製品として再配布または再販売することは許諾されていません。ツールを使って生成したコンテンツ、つまり圧縮された画像、変換されたファイル、生成されたテキストは、完全にあなたのものです。",
    h2_6="第三者サービス", p6="norito は Google AdSense を通じて広告を表示し、Google Fonts からフォントを読み込んでいます。どちらも<a href=\"privacy.html\">プライバシーポリシー</a>に記載の通り、第三者のサーバーへのリクエストを伴います。norito はこれら第三者サービスのコンテンツ、可用性、または慣行について責任を負いません。",
    h2_7="無保証", p7="norito は「現状のまま」提供され、明示または黙示を問わずいかなる保証もありません。ツールにエラーがないこと、常に利用可能であること、または特定の目的に適していることを保証するものではありません。重要なファイルをオンラインツール（本サイトを含む）で処理する前は、必ず自分自身でバックアップを取ってください。",
    h2_8="責任の制限", p8="法律で許される最大限の範囲において、norito およびその運営者は、データの損失や出力の破損を含め、本サイトの利用に起因する間接的、付随的、または結果的な損害について責任を負いません。サービスに不満がある場合の唯一の救済手段は、利用を停止することです。",
    h2_9="本規約の変更", p9="本規約は、サイトの発展に伴い、主に新しいツールが追加される際に更新される場合があります。変更後も norito を使い続けることは、更新された規約に同意したことを意味します。",
    contact_p="本規約に関するご質問は、以下までお送りください",
)

BASE = "https://norito.in"

def hreflang_block(slug):
    lines = []
    for l in LOCS:
        code = l if l else "en"
        href = f"{BASE}/{l+'/' if l else ''}{slug}"
        lines.append(f'<link rel="alternate" hreflang="{code}" href="{href}" />')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/{slug}" />')
    return "\n".join(lines)

for loc in LOCS:
    c = C[loc]
    slug = "terms.html"
    canonical = f"{BASE}/{loc+'/' if loc else ''}{slug}"
    lang_code = loc if loc else "en"
    dir_attr = f' dir="{DIR[loc]}"' if loc in DIR else ""
    home_href = "index.html"
    breadcrumb_item = f"{BASE}/{loc+'/' if loc else ''}"

    body_sections = "\n\n".join(
        f'    <h2>{c[f"h2_{i}"]}</h2>\n    <p>{c[f"p{i}"]}</p>' for i in range(1, 10)
    )

    html = f'''<!DOCTYPE html>
<html lang="{lang_code}"{dir_attr}>
<head>
    <!--INCLUDE:HEAD-COMMON-->
<title>{TITLE[loc]}</title>
<meta name="description" content="{META_DESC[loc]}" />
<link rel="canonical" href="{canonical}" />
{hreflang_block(slug)}
<meta name="robots" content="noindex, follow" />
<link rel="stylesheet" href="/css/style.css" />
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "norito",
      "item": "{breadcrumb_item}"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "{BREADCRUMB_LABEL[loc]}",
      "item": "{canonical}"
    }}
  ]
}}
</script>
</head>
<body>
<div class="bg-blobs" aria-hidden="true">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
</div>

<!--INCLUDE:HEADER:standard-->

<main>
  <div class="wrap legal-content">
    <p class="breadcrumb"><a href="{home_href}">norito</a> / {BREADCRUMB_LABEL[loc]}</p>
    <h1>{BREADCRUMB_LABEL[loc]}</h1>
    <p class="lede">
      {c["lede"]}
    </p>

{body_sections}

    <p class="note">{LAST_UPDATED[loc]}</p>

    <h2>{ {"":"Contact", "es":"Contacto", "zh":"联系我们", "ar":"اتصل بنا", "hi":"संपर्क करें", "ru":"Контакты", "ja":"お問い合わせ"}[loc] }</h2>
    <p>{c["contact_p"]}
      <a href="mailto:shubhamsingh1604@gmail.com">shubhamsingh1604@gmail.com</a>.</p>
  </div>
</main>

<!--INCLUDE:FOOTER:standard-->

<!--INCLUDE:FOOT-SCRIPTS-MID-->
<!--INCLUDE:CMDK-OVERLAY-->

<!--INCLUDE:FOOT-SCRIPTS-TAIL-->
'''
    outdir = f"src/{loc}" if loc else "src"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/terms.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
