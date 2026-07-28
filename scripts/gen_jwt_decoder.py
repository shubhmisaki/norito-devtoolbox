#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/happy-keen-sagan/mnt/norito/scripts")
from i18n_lib import render_page

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

ICON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="16" r="1"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
ICON_CLASS = "c-rose"

def body(t):
    return f'''
    <div class="two-col">
      <div class="panel">
        <div class="field">
          <label for="jwtInput">{t['jwt']}</label>
          <textarea id="jwtInput" class="mono-output" rows="6" spellcheck="false" placeholder="{t['ph_jwt']}">eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c</textarea>
        </div>
        <div class="result-box" id="result" style="display:none;"></div>
        <div class="meta-panel" id="claimsPanel" style="display:none;">
          <p class="meta-summary">{t['claims_summary']}</p>
          <div class="meta-list" id="claimsList"></div>
        </div>
      </div>

      <div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['header']}</h3>
          <pre class="code-output" id="headerOut"></pre>
        </div>
        <div class="panel">
          <h3 style="margin-top:0;">{t['payload']}</h3>
          <pre class="code-output" id="payloadOut"></pre>
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
    title="Decodificador de JWT: Decodifica Tokens JSON Web Online | norito",
    meta_desc="Decodifica el header y payload de un JWT, en tu navegador. Ve la expiración y los claims estándar explicados. La firma nunca se verifica, no se sube nada.",
    app_name="Decodificador de JWT", h1="Decodificador de JWT", breadcrumb_label="Decodificador de JWT",
    lede="Pega un JWT para ver su header y payload decodificados, con los claims estándar como la expiración explicados. No se sube nada, las firmas nunca se verifican ni se comprueban contra un secreto.",
    t=dict(
        jwt="JWT", ph_jwt="Pega un JWT, p. ej. eyJhbGciOi...",
        claims_summary="Claims estándar reconocidos", header="Header", payload="Payload",
        how_h2="Cómo funciona",
        how_p1='Un JWT son tres segmentos Base64URL unidos por puntos: header, payload, firma. La herramienta divide en los puntos, luego decodifica los primeros dos segmentos mapeando el alfabeto seguro para URL de vuelta a Base64 estándar (<code>-</code> a <code>+</code>, <code>_</code> a <code>/</code>), restaurando el padding que los JWT omiten, ejecutando <code>atob()</code>, y decodificando los bytes como UTF-8 con <code>TextDecoder</code>. Cada segmento se procesa con <code>JSON.parse</code> y se formatea. Los claims estándar (<code>iss</code>, <code>sub</code>, <code>aud</code>, <code>exp</code>, <code>nbf</code>, <code>iat</code>, <code>jti</code>) reciben etiquetas legibles, los timestamps unix se convierten en fechas legibles, y <code>exp</code> se compara con tu reloj para decirte si el token ha expirado. El tercer segmento, la firma, nunca se analiza en absoluto.',
        how_p2='Esa es la distinción con la que esta herramienta es estricta: decodificar no es verificar. El payload de cualquier JWT es legible por cualquiera, está codificado, no encriptado. Probar que el token es genuino significa recalcular la firma, lo que requiere el secreto de firma (para HMAC) o la clave del emisor (para RSA/ECDSA). Esta herramienta deliberadamente no ofrece una caja de "pega tu secreto": acostumbrarse a pegar secretos de firma de producción en páginas web es un riesgo que ninguna comodidad justifica, y la verificación pertenece de todos modos a tu servidor. Nunca confíes en un claim decodificado que no hayas verificado del lado del servidor.',
        how_p3='Todo se ejecuta en el JavaScript de esta página usando <code>atob</code> y las APIs de decodificación de texto. Pega un token real con la pestaña Red de las DevTools abierta y observa: no se hace ninguna petición, el token nunca sale de la pestaña del navegador.',
    ),
    related_tools=[
        ("base64-encoder.html", "Codificar / Decodificar Base64", "Decodifica manualmente un único segmento Base64."),
        ("timestamp-converter.html", "Conversor de Timestamp", "Convierte un timestamp Unix a una fecha legible."),
        ("json-formatter.html", "Formateador JSON", "Formatea el payload decodificado para leerlo más fácilmente."),
    ],
)

PAGES["zh"] = dict(
    title="JWT 解码器：在线解码 JSON Web Token | norito",
    meta_desc="在浏览器中解码 JWT 的 header 和 payload。查看过期时间以及标准声明的解释。签名永远不会被验证，不会上传任何内容。",
    app_name="JWT 解码器", h1="JWT 解码器", breadcrumb_label="JWT 解码器",
    lede="粘贴一个 JWT，查看解码后的 header 和 payload，并附带过期时间等标准声明的解释。不会上传任何内容，签名永远不会被验证或与密钥进行核对。",
    t=dict(
        jwt="JWT", ph_jwt="粘贴一个 JWT，例如 eyJhbGciOi...",
        claims_summary="已识别的标准声明", header="Header", payload="Payload",
        how_h2="工作原理",
        how_p1='一个 JWT 由三个用点连接的 Base64URL 片段组成：header、payload、signature。工具按点进行拆分，然后通过把 URL 安全字母表映射回标准 Base64（<code>-</code> 变回 <code>+</code>，<code>_</code> 变回 <code>/</code>），恢复 JWT 省略的填充字符，运行 <code>atob()</code>，再用 <code>TextDecoder</code> 将字节解码为 UTF-8，从而解码前两个片段。每个片段随后都会经过 <code>JSON.parse</code> 处理并进行格式化输出。标准声明（<code>iss</code>、<code>sub</code>、<code>aud</code>、<code>exp</code>、<code>nbf</code>、<code>iat</code>、<code>jti</code>）会被赋予易读的标签，Unix 时间戳会转换成可读日期，<code>exp</code> 会与你的系统时钟进行比较，从而告诉你该令牌是否已过期。第三段——签名——则完全不会被解析。',
        how_p2='这正是该工具严格遵循的区别：解码不是验证。任何 JWT 的 payload 都可以被任何人读取，它是编码过的，而不是加密的。要证明令牌真实有效，需要重新计算签名，这需要签名密钥（对于 HMAC）或颁发者的密钥（对于 RSA/ECDSA）。该工具刻意不提供「粘贴你的密钥」输入框：习惯性地把生产环境的签名密钥粘贴到网页中，是任何便利性都无法证明其合理的风险，而且验证本来就应该在你的服务器上完成。永远不要信任一个你没有在服务器端验证过的解码声明。',
        how_p3='一切都在这个页面自身的 JavaScript 中运行，使用 <code>atob</code> 和文本解码 API。打开开发者工具的 Network 标签页，粘贴一个真实令牌观察一下：不会发出任何请求，令牌永远不会离开浏览器标签页。',
    ),
    related_tools=[
        ("base64-encoder.html", "Base64 编码 / 解码", "手动解码单个 Base64 片段。"),
        ("timestamp-converter.html", "时间戳转换器", "将 Unix 时间戳转换为可读日期。"),
        ("json-formatter.html", "JSON 格式化", "格式化解码后的 payload，便于阅读。"),
    ],
)

PAGES["ar"] = dict(
    title="فاك تشفير JWT: فكّ ترميز رموز JSON Web أونلاين | norito",
    meta_desc="فكّ ترميز رأس وحمولة JWT، مباشرة في متصفحك. شاهد الانتهاء والمطالبات القياسية موضّحة. لا يُتحقَّق من التوقيع أبدًا، لا شيء يُرفَع.",
    app_name="فاك تشفير JWT", h1="فاك تشفير JWT", breadcrumb_label="فاك تشفير JWT",
    lede="الصق JWT لرؤية رأسه وحمولته بعد فكّ الترميز، مع شرح للمطالبات القياسية مثل الانتهاء. لا شيء يُرفَع، ولا يُتحقَّق من التوقيعات أبدًا مقابل سرّ.",
    t=dict(
        jwt="JWT", ph_jwt="الصق JWT، مثل eyJhbGciOi...",
        claims_summary="المطالبات القياسية المعروفة", header="الرأس (Header)", payload="الحمولة (Payload)",
        how_h2="كيف يعمل",
        how_p1='الـ JWT هو ثلاثة مقاطع Base64URL مفصولة بنقاط: رأس، حمولة، توقيع. تقسّم الأداة عند النقاط، ثم تفكّ ترميز المقطعين الأولين بتحويل الأبجدية الآمنة للرابط مرة أخرى إلى Base64 القياسي (<code>-</code> إلى <code>+</code>، <code>_</code> إلى <code>/</code>)، مستعيدةً الحشو الذي تحذفه رموز JWT، مشغِّلةً <code>atob()</code>، وفكّ ترميز البايتات كـ UTF-8 بواسطة <code>TextDecoder</code>. يُعالَج كل مقطع بعدها بـ <code>JSON.parse</code> ويُنسَّق. تحصل المطالبات القياسية (<code>iss</code>، <code>sub</code>، <code>aud</code>، <code>exp</code>، <code>nbf</code>، <code>iat</code>، <code>jti</code>) على تسميات مفهومة، وتتحول طوابع Unix الزمنية إلى تواريخ قابلة للقراءة، ويُقارَن <code>exp</code> بساعتك لإخبارك ما إذا كان الرمز منتهي الصلاحية. المقطع الثالث، التوقيع، لا يُحلَّل أبدًا.',
        how_p2='هذا هو الفرق الذي تلتزم به هذه الأداة بصرامة: فكّ الترميز ليس تحققًا. حمولة أي JWT قابلة للقراءة من قِبل أي شخص، فهي مُرمَّزة، لا مشفّرة. إثبات أن الرمز أصلي يعني إعادة حساب التوقيع، وهو ما يتطلب سرّ التوقيع (لـ HMAC) أو مفتاح المُصدِر (لـ RSA/ECDSA). لا تقدّم هذه الأداة عمدًا مربّع «الصق سرّك»: التعوّد على لصق أسرار توقيع الإنتاج في صفحات الويب مخاطرة لا تبرّرها أي راحة، والتحقّق ينتمي إلى خادمك على أي حال. لا تثق أبدًا بمطالبة مفكوكة الترميز لم تتحقّق منها من جانب الخادم.',
        how_p3='كل شيء يعمل في جافاسكريبت هذه الصفحة باستخدام <code>atob</code> وواجهات فكّ ترميز النص. الصق رمزًا حقيقيًا مع فتح لسان Network في أدوات المطوّر وراقب: لا يُرسَل أي طلب، والرمز لا يغادر تبويب المتصفح أبدًا.',
    ),
    related_tools=[
        ("base64-encoder.html", "ترميز / فك ترميز Base64", "فكّ ترميز مقطع Base64 واحد يدويًا."),
        ("timestamp-converter.html", "محول الطابع الزمني", "حوّل طابعًا زمنيًا Unix إلى تاريخ قابل للقراءة."),
        ("json-formatter.html", "منسّق JSON", "نسّق الحمولة المفكوكة الترميز لتسهيل قراءتها."),
    ],
)

PAGES["hi"] = dict(
    title="JWT डिकोडर: JSON वेब टोकन ऑनलाइन डिकोड करें | norito",
    meta_desc="अपने ब्राउज़र में ही JWT का header और payload डिकोड करें। एक्सपायरी और स्टैंडर्ड क्लेम्स को समझाया गया देखें। सिग्नेचर कभी वेरिफ़ाई नहीं होता, कुछ भी अपलोड नहीं होता।",
    app_name="JWT डिकोडर", h1="JWT डिकोडर", breadcrumb_label="JWT डिकोडर",
    lede="डिकोड किया गया header और payload देखने के लिए एक JWT पेस्ट करें, एक्सपायरी जैसे स्टैंडर्ड क्लेम्स को समझाया गया। कुछ भी अपलोड नहीं होता, सिग्नेचर कभी वेरिफ़ाई या किसी सीक्रेट के ख़िलाफ़ चेक नहीं होते।",
    t=dict(
        jwt="JWT", ph_jwt="एक JWT पेस्ट करें, जैसे eyJhbGciOi...",
        claims_summary="पहचाने गए स्टैंडर्ड क्लेम्स", header="Header", payload="Payload",
        how_h2="यह कैसे काम करता है",
        how_p1='एक JWT डॉट्स से जुड़े तीन Base64URL सेगमेंट होते हैं: header, payload, signature। टूल डॉट्स पर स्प्लिट करता है, फिर पहले दो सेगमेंट्स को URL-सेफ़ अल्फ़ाबेट को वापस स्टैंडर्ड Base64 में मैप करके डिकोड करता है (<code>-</code> को <code>+</code>, <code>_</code> को <code>/</code>), JWT द्वारा छोड़ी गई पैडिंग को रीस्टोर करते हुए, <code>atob()</code> चलाते हुए, और <code>TextDecoder</code> से बाइट्स को UTF-8 के रूप में डिकोड करते हुए। हर सेगमेंट को फिर <code>JSON.parse</code> किया जाता है और प्रेटी-प्रिंट किया जाता है। स्टैंडर्ड क्लेम्स (<code>iss</code>, <code>sub</code>, <code>aud</code>, <code>exp</code>, <code>nbf</code>, <code>iat</code>, <code>jti</code>) को ह्यूमन लेबल्स मिलते हैं, यूनिक्स टाइमस्टैंप्स पढ़ने लायक तारीख़ों में बदल जाते हैं, और <code>exp</code> की तुलना आपकी घड़ी से की जाती है यह बताने के लिए कि टोकन एक्सपायर हो चुका है या नहीं। तीसरा सेगमेंट, सिग्नेचर, कभी पार्स ही नहीं होता।',
        how_p2='यही वह भेद है जिस पर यह टूल सख़्त है: डिकोड करना वेरिफ़ाई करना नहीं है। किसी भी JWT का payload किसी के भी द्वारा पढ़ा जा सकता है, यह एनकोडेड है, एन्क्रिप्टेड नहीं। टोकन को असली साबित करने का मतलब है सिग्नेचर को दोबारा कैलकुलेट करना, जिसके लिए साइनिंग सीक्रेट (HMAC के लिए) या इशूअर की की (RSA/ECDSA के लिए) चाहिए होती है। यह टूल जानबूझकर "अपना सीक्रेट पेस्ट करें" बॉक्स ऑफ़र नहीं करता: प्रोडक्शन साइनिंग सीक्रेट्स को वेब पेजेज़ में पेस्ट करने की आदत डालना एक ऐसा रिस्क है जिसे कोई भी सुविधा जस्टिफ़ाई नहीं कर सकती, और वेरिफ़िकेशन वैसे भी आपके सर्वर पर होनी चाहिए। किसी ऐसे डिकोड किए गए क्लेम पर कभी भरोसा न करें जिसे आपने सर्वर-साइड वेरिफ़ाई न किया हो।',
        how_p3='यह सब इस पेज के JavaScript में <code>atob</code> और टेक्स्ट डिकोडिंग APIs इस्तेमाल करते हुए चलता है। डेवटूल्स का Network टैब खोलकर एक असली टोकन पेस्ट करें और देखें: कोई रिक्वेस्ट नहीं होती, टोकन कभी ब्राउज़र टैब से बाहर नहीं जाता।',
    ),
    related_tools=[
        ("base64-encoder.html", "Base64 एनकोड / डिकोड", "किसी सिंगल Base64 सेगमेंट को मैनुअली डिकोड करें।"),
        ("timestamp-converter.html", "टाइमस्टैंप कन्वर्टर", "किसी Unix टाइमस्टैंप को पढ़ने लायक तारीख़ में बदलें।"),
        ("json-formatter.html", "JSON फ़ॉर्मैटर", "पढ़ने में आसानी के लिए डिकोड किए गए payload को फ़ॉर्मैट करें।"),
    ],
)

PAGES["ru"] = dict(
    title="Декодер JWT: декодируйте JSON Web Token онлайн | norito",
    meta_desc="Декодируйте заголовок и payload JWT прямо в браузере. Смотрите срок действия и объяснение стандартных claims. Подпись никогда не проверяется, ничего не загружается.",
    app_name="Декодер JWT", h1="Декодер JWT", breadcrumb_label="Декодер JWT",
    lede="Вставьте JWT, чтобы увидеть его декодированный заголовок и payload с объяснением стандартных claims, таких как срок действия. Ничего не загружается, подписи никогда не проверяются и не сверяются с секретом.",
    t=dict(
        jwt="JWT", ph_jwt="Вставьте JWT, например eyJhbGciOi...",
        claims_summary="Распознанные стандартные claims", header="Заголовок", payload="Payload",
        how_h2="Как это работает",
        how_p1='JWT — это три сегмента Base64URL, соединённых точками: заголовок, payload, подпись. Инструмент разбивает по точкам, затем декодирует первые два сегмента, преобразуя URL-безопасный алфавит обратно в стандартный Base64 (<code>-</code> в <code>+</code>, <code>_</code> в <code>/</code>), восстанавливая опущенное в JWT дополнение, запуская <code>atob()</code> и декодируя байты как UTF-8 с помощью <code>TextDecoder</code>. Каждый сегмент затем обрабатывается через <code>JSON.parse</code> и красиво форматируется. Стандартные claims (<code>iss</code>, <code>sub</code>, <code>aud</code>, <code>exp</code>, <code>nbf</code>, <code>iat</code>, <code>jti</code>) получают понятные метки, unix-метки времени превращаются в читаемые даты, а <code>exp</code> сравнивается с вашими часами, чтобы сообщить, истёк ли срок действия токена. Третий сегмент, подпись, вообще никогда не разбирается.',
        how_p2='Это и есть строгое различие, которого придерживается этот инструмент: декодирование — это не проверка. Payload любого JWT доступен для чтения кому угодно, он закодирован, а не зашифрован. Доказать подлинность токена означает пересчитать подпись, для чего требуется секрет подписи (для HMAC) или ключ издателя (для RSA/ECDSA). Этот инструмент намеренно не предлагает поле «вставьте свой секрет»: привычка вставлять производственные секреты подписи в веб-страницы — это риск, который не оправдывает никакое удобство, а проверка в любом случае должна выполняться на вашем сервере. Никогда не доверяйте декодированному claim, который вы не проверили на стороне сервера.',
        how_p3='Всё выполняется в JavaScript этой страницы с использованием <code>atob</code> и API декодирования текста. Вставьте настоящий токен при открытой вкладке Network в DevTools и понаблюдайте: ни один запрос не отправляется, токен никогда не покидает вкладку браузера.',
    ),
    related_tools=[
        ("base64-encoder.html", "Кодировщик / декодировщик Base64", "Вручную декодируйте один сегмент Base64."),
        ("timestamp-converter.html", "Конвертер меток времени", "Преобразуйте метку времени Unix в читаемую дату."),
        ("json-formatter.html", "Форматирование JSON", "Отформатируйте декодированный payload для удобного чтения."),
    ],
)

PAGES["ja"] = dict(
    title="JWTデコーダー：JSON Web Tokenをオンラインでデコード | norito",
    meta_desc="ブラウザ内でJWTのヘッダーとペイロードをデコード。有効期限と標準クレームの説明を確認できます。署名は検証されません。アップロードなし。",
    app_name="JWTデコーダー", h1="JWTデコーダー", breadcrumb_label="JWTデコーダー",
    lede="JWTを貼り付けると、デコードされたヘッダーとペイロード、そして有効期限などの標準クレームの説明が表示されます。何もアップロードされず、署名が検証されたり秘密鍵と照合されたりすることもありません。",
    t=dict(
        jwt="JWT", ph_jwt="JWTを貼り付け、例：eyJhbGciOi...",
        claims_summary="認識された標準クレーム", header="ヘッダー", payload="ペイロード",
        how_h2="仕組み",
        how_p1='JWTはドットで結合された3つのBase64URLセグメントです。ヘッダー、ペイロード、署名です。このツールはドットで分割し、最初の2つのセグメントをデコードします。URLセーフなアルファベットを標準のBase64に戻し（<code>-</code>を<code>+</code>に、<code>_</code>を<code>/</code>に）、JWTが省略しているパディングを復元し、<code>atob()</code>を実行し、<code>TextDecoder</code>でバイト列をUTF-8としてデコードします。各セグメントはその後<code>JSON.parse</code>され、整形されて表示されます。標準クレーム（<code>iss</code>、<code>sub</code>、<code>aud</code>、<code>exp</code>、<code>nbf</code>、<code>iat</code>、<code>jti</code>）にはわかりやすいラベルが付き、Unixタイムスタンプは読みやすい日付に変換され、<code>exp</code>はあなたの時計と比較されてトークンが期限切れかどうかを教えてくれます。3番目のセグメントである署名は、一切解析されません。',
        how_p2='これがこのツールが厳密に守っている区別です。デコードは検証ではありません。あらゆるJWTのペイロードは誰でも読むことができます。それは暗号化ではなくエンコードされているだけです。トークンが本物であることを証明するには署名を再計算する必要があり、そのためには署名用の秘密鍵（HMACの場合）または発行者の鍵（RSA/ECDSAの場合）が必要です。このツールは意図的に「秘密鍵を貼り付ける」ボックスを提供していません。本番環境の署名用秘密鍵をウェブページに貼り付ける習慣は、どんな利便性をもってしても正当化できないリスクであり、検証はいずれにせよサーバー側で行うべきものです。サーバー側で検証していないデコード済みのクレームを決して信用しないでください。',
        how_p3='すべての処理は、<code>atob</code>とテキストデコードAPIを使ってこのページのJavaScript内で実行されます。DevToolsのNetworkタブを開いた状態で実際のトークンを貼り付けて観察してみてください。リクエストは一切発生せず、トークンがブラウザのタブから外に出ることはありません。',
    ),
    related_tools=[
        ("base64-encoder.html", "Base64 エンコード / デコード", "単一のBase64セグメントを手動でデコード。"),
        ("timestamp-converter.html", "タイムスタンプ変換ツール", "Unixタイムスタンプを読みやすい日付に変換。"),
        ("json-formatter.html", "JSONフォーマッタ", "デコードされたペイロードを整形して読みやすくします。"),
    ],
)

for loc, data in PAGES.items():
    html = render_page(
        loc, "jwt-decoder.html",
        title=data["title"], meta_desc=data["meta_desc"], app_name=data["app_name"],
        icon_svg=ICON_SVG, icon_class=ICON_CLASS,
        breadcrumb_label=data["breadcrumb_label"], h1=data["h1"], lede=data["lede"],
        body_html=body(data["t"]),
        related_tools=data["related_tools"],
        i18n_scripts=["js/app-jwt-decoder.js"],
        use_foot_scripts_head=True,
    )
    outdir = f"src/{loc}"
    os.makedirs(outdir, exist_ok=True)
    outpath = f"{outdir}/jwt-decoder.html"
    open(outpath, "w", encoding="utf-8").write(html)
    print("wrote", outpath, len(html), "bytes")
