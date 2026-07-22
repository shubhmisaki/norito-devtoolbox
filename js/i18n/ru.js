// Auto-generated i18n dictionary for the ru localized pages.
// Loaded before js/i18n-runtime.js and the app-*.js scripts on every
// /ru/ page, so i18nFor(fileId) resolves to translated strings
// instead of falling back to the English defaults baked into each script.
window.NORITO_I18N = {
  "common": {
    "copied": "Скопировано",
    "please_choose_image": "Выберите файл изображения.",
    "working": "Обработка…"
  },
  "app-compress": {
    "compressing_label": "Сжатие…",
    "err_invalid_target": "Введите корректный целевой размер.",
    "err_no_outcome": "Не удалось уложиться в {target} даже при минимальном качестве. Попробуйте больший размер, смените формат или включите «Разрешить изменение размера».",
    "dims_resized": "изменён размер до {w}×{h} (было {ow}×{oh})",
    "dims_original": "исходный размер {w}×{h}",
    "status_within_target": "в пределах вашей цели, с {dims}.",
    "status_closest_resized": "максимально близкий размер (цель была слишком мала даже с изменением размера), с {dims}.",
    "status_closest_noresize": "минимально возможный размер без изменения размеров, с {dims}.",
    "resize_nudge_question": "Это минимально возможный файл без изменения размеров. Включить изменение размера, чтобы достичь {target}?",
    "enable_resize_retry_btn": "Включить изменение размера и сжать заново",
    "format_nudge_question": "PNG не имеет потерь, поэтому обычно даёт файлы больше, чем JPEG или WebP для фото. Переключиться на JPEG и сжать заново?",
    "switch_to_jpeg_retry_btn": "Переключиться на JPEG и сжать заново",
    "result_success": "<strong>Изображение успешно сжато.</strong> <strong>{size}</strong>. {statusLine}",
    "result_partial": "<strong>Сжато настолько, насколько возможно.</strong> <strong>{size}</strong>. {statusLine}",
    "result_larger_than_original": "<strong>Это максимум сжатия без изменения размеров:</strong> <strong>{size}</strong>, немного больше вашего оригинала ({origSize}). {statusLine}",
    "download_button": "Скачать {filename}",
    "err_generic": "<strong>Не удалось сжать это изображение.</strong> {msg}. Попробуйте другое изображение или смените формат и повторите попытку.",
    "btn_compress_default": "Сжать до цели"
  },
  "app-json": {
    "empty_input": "Пустой ввод",
    "line_col_suffix": " (строка {line}, столбец {col})",
    "item_singular": "элемент",
    "item_plural": "элементов",
    "more_items_not_shown": "… ещё {n} элементов не показано"
  },
  "app-markdown": {
    "preview_unavailable": "Предпросмотр сейчас недоступен.",
    "renderer_failed": "Не удалось загрузить рендерер markdown. Проверьте подключение и перезагрузите страницу. Ничего из написанного не потеряно.",
    "render_failed_title": "Не удалось отрендерить этот markdown.",
    "render_failed_suffix": ". Попробуйте отменить последнее изменение."
  },
  "app-password": {
    "strength_weak": "Слабый",
    "strength_fair": "Приемлемый",
    "strength_strong": "Надёжный",
    "strength_vstrong": "Очень надёжный",
    "entropy_out": "~{n} бит энтропии"
  },
  "app-placeholder": {
    "placeholder_ready": "Заполнитель готов: {w}×{h}, {size}, {fmt}",
    "swatch_brand_pink": "Фирменный розовый",
    "swatch_neutral_gray": "Нейтральный серый",
    "swatch_slate": "Грифельный",
    "swatch_sky_blue": "Небесно-голубой",
    "swatch_soft_beige": "Мягкий бежевый",
    "swatch_mint": "Мятный"
  },
  "app-qrcode": {
    "prompt_enter_text": "Введите URL или текст, чтобы создать QR-код.",
    "err_too_much_text": "Слишком много текста для одного QR-кода. Попробуйте сократить его.",
    "err_not_an_image": "Это не похоже на файл изображения. Попробуйте PNG, JPG или SVG.",
    "err_load_failed": "Не удалось загрузить это изображение. Попробуйте другой файл."
  },
  "app-removebg": {
    "err_lib_not_loaded": "Не удалось загрузить библиотеку для удаления фона. Проверьте подключение и перезагрузите страницу.",
    "err_model_timeout": "Модель сегментации загружалась слишком долго. Проверьте подключение и повторите попытку.",
    "err_processing_timeout": "Обработка заняла слишком много времени. Попробуйте изображение поменьше (менее 4 мегапикселей работает лучше).",
    "loading_model_label": "Загрузка модели…",
    "processing_label": "Обработка…",
    "loading_model_status": "Загружается модель портретного маттинга и её среда выполнения: около 18 МБ в сумме, происходит только раз за сессию браузера.",
    "result_success": "<strong>Фон успешно удалён.</strong> Лучше всего работает с фото, где человек — главный объект.",
    "err_generic_prefix": "Не удалось удалить фон.",
    "err_unexpected": "Произошло что-то неожиданное.",
    "btn_remove_default": "Удаление фона"
  },
  "app-slug": {
    "batch_empty_hint": "Вставьте заголовки выше, по одному на строку.",
    "copied_all": "Всё скопировано"
  },
  "app-testfile": {
    "err_invalid_size": "Введите корректный положительный размер.",
    "err_max_size": "Максимальный поддерживаемый в браузере размер — 2 ГБ (файлы больше рискуют закрыть вкладку).",
    "generating_label": "Генерация…",
    "result_exact": "<strong>Точное совпадение.</strong> Создано {size}.",
    "result_offby": "Создано <strong>{actual}</strong> (запрошено {target}, разница {diff} байт; у некоторых форматов есть структурный минимум или отступ).",
    "result_success_prefix": "Файл успешно создан.",
    "download_button": "Скачать {filename}",
    "err_generic": "<strong>Не удалось создать этот файл.</strong> {msg}. Попробуйте меньший размер или другое расширение.",
    "btn_generate_default": "Создать файл"
  },
  "app-textlimit": {
    "err_invalid_limit": "Введите число символов от 1 и больше.",
    "result_generated": "<strong>Создано ровно {n} символов</strong>",
    "spaces_included": " (пробелы включены).",
    "spaces_excluded": " (пробелы исключены из подсчёта).",
    "preset_suffix_characters": "{n} символов"
  }
};
