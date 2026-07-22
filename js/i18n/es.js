// Auto-generated i18n dictionary for the es localized pages.
// Loaded before js/i18n-runtime.js and the app-*.js scripts on every
// /es/ page, so i18nFor(fileId) resolves to translated strings
// instead of falling back to the English defaults baked into each script.
window.NORITO_I18N = {
  "common": {
    "copied": "Copiado",
    "please_choose_image": "Elige un archivo de imagen.",
    "working": "Procesando…"
  },
  "app-compress": {
    "compressing_label": "Comprimiendo…",
    "err_invalid_target": "Introduce un tamaño objetivo válido.",
    "err_no_outcome": "No se pudo bajar de {target} ni con la calidad mínima. Prueba con un objetivo mayor, cambia el formato o activa \"Permitir redimensionar\".",
    "dims_resized": "redimensionada a {w}×{h} (desde {ow}×{oh})",
    "dims_original": "tamaño original {w}×{h}",
    "status_within_target": "dentro de tu objetivo, con {dims}.",
    "status_closest_resized": "el tamaño más cercano posible (el objetivo era demasiado pequeño incluso redimensionando), con {dims}.",
    "status_closest_noresize": "el tamaño más pequeño posible sin redimensionar, con {dims}.",
    "resize_nudge_question": "Este es el archivo más pequeño posible sin redimensionar. ¿Quieres activar el redimensionado para alcanzar {target}?",
    "enable_resize_retry_btn": "Activar redimensionado y comprimir de nuevo",
    "format_nudge_question": "PNG no tiene pérdida, así que suele producir archivos más grandes que JPEG o WebP en fotos. ¿Quieres cambiar a JPEG y comprimir de nuevo?",
    "switch_to_jpeg_retry_btn": "Cambiar a JPEG y comprimir de nuevo",
    "result_success": "<strong>Imagen comprimida correctamente.</strong> <strong>{size}</strong>. {statusLine}",
    "result_partial": "<strong>Se redujo todo lo posible.</strong> <strong>{size}</strong>. {statusLine}",
    "result_larger_than_original": "<strong>Esto es lo máximo que pudimos comprimir sin redimensionar:</strong> <strong>{size}</strong>, un poco más grande que tu original ({origSize}). {statusLine}",
    "download_button": "Descargar {filename}",
    "err_generic": "<strong>No se pudo comprimir esa imagen.</strong> {msg}. Prueba con otra imagen, o cambia el formato e inténtalo de nuevo.",
    "btn_compress_default": "Comprimir al objetivo"
  },
  "app-json": {
    "empty_input": "Entrada vacía",
    "line_col_suffix": " (línea {line}, columna {col})",
    "item_singular": "elemento",
    "item_plural": "elementos",
    "more_items_not_shown": "… {n} elementos más sin mostrar"
  },
  "app-markdown": {
    "preview_unavailable": "La vista previa no está disponible ahora mismo.",
    "renderer_failed": "El renderizador de markdown no se cargó. Comprueba tu conexión y recarga la página. No se ha perdido nada de lo que escribiste.",
    "render_failed_title": "No se pudo renderizar este markdown.",
    "render_failed_suffix": ". Intenta deshacer tu último cambio."
  },
  "app-password": {
    "strength_weak": "Débil",
    "strength_fair": "Aceptable",
    "strength_strong": "Segura",
    "strength_vstrong": "Muy segura",
    "entropy_out": "~{n} bits de entropía"
  },
  "app-placeholder": {
    "placeholder_ready": "Marcador listo: {w}×{h}, {size}, {fmt}",
    "swatch_brand_pink": "Rosa de marca",
    "swatch_neutral_gray": "Gris neutro",
    "swatch_slate": "Pizarra",
    "swatch_sky_blue": "Azul cielo",
    "swatch_soft_beige": "Beige suave",
    "swatch_mint": "Menta"
  },
  "app-qrcode": {
    "prompt_enter_text": "Escribe una URL o algo de texto para generar un código QR.",
    "err_too_much_text": "Demasiado texto para un solo código QR. Prueba a acortarlo.",
    "err_not_an_image": "Eso no parece un archivo de imagen. Prueba con un PNG, JPG o SVG.",
    "err_load_failed": "No se pudo cargar esa imagen. Prueba con otro archivo."
  },
  "app-removebg": {
    "err_lib_not_loaded": "La librería para quitar el fondo no se cargó. Comprueba tu conexión y recarga la página.",
    "err_model_timeout": "El modelo de segmentación tardó demasiado en cargar. Comprueba tu conexión e inténtalo de nuevo.",
    "err_processing_timeout": "El procesamiento tardó demasiado. Prueba con una imagen más pequeña (menos de 4 megapíxeles funciona mejor).",
    "loading_model_label": "Cargando modelo…",
    "processing_label": "Procesando…",
    "loading_model_status": "Cargando el modelo de recorte de retrato y su runtime: unos 18 MB en total, solo ocurre una vez por sesión de navegador.",
    "result_success": "<strong>Fondo eliminado correctamente.</strong> Funciona mejor en fotos donde una persona es el sujeto principal.",
    "err_generic_prefix": "No se pudo quitar el fondo.",
    "err_unexpected": "Ocurrió algo inesperado.",
    "btn_remove_default": "Quitar fondo"
  },
  "app-slug": {
    "batch_empty_hint": "Pega títulos arriba, uno por línea.",
    "copied_all": "Todo copiado"
  },
  "app-testfile": {
    "err_invalid_size": "Introduce un tamaño válido y positivo.",
    "err_max_size": "El tamaño máximo compatible en el navegador es 2 GB (archivos más grandes arriesgan cerrar la pestaña).",
    "generating_label": "Generando…",
    "result_exact": "<strong>Coincidencia exacta.</strong> Se generaron {size}.",
    "result_offby": "Se generaron <strong>{actual}</strong> (se pidieron {target}, una diferencia de {diff} bytes; algunos formatos tienen un mínimo estructural o de relleno).",
    "result_success_prefix": "Archivo generado correctamente.",
    "download_button": "Descargar {filename}",
    "err_generic": "<strong>No se pudo generar ese archivo.</strong> {msg}. Prueba con un tamaño menor o una extensión distinta.",
    "btn_generate_default": "Generar archivo"
  },
  "app-textlimit": {
    "err_invalid_limit": "Introduce un número de caracteres de 1 o más.",
    "result_generated": "<strong>Se generaron exactamente {n} caracteres</strong>",
    "spaces_included": " (espacios incluidos).",
    "spaces_excluded": " (espacios excluidos del conteo).",
    "preset_suffix_characters": "{n} caracteres"
  }
};
