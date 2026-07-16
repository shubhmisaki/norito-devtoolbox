// Auto-generated i18n dictionary for the ja localized pages.
// Loaded before js/i18n-runtime.js and the app-*.js scripts on every
// /ja/ page, so i18nFor(fileId) resolves to translated strings
// instead of falling back to the English defaults baked into each script.
window.NORITO_I18N = {
  "common": {
    "copied": "コピーしました",
    "please_choose_image": "画像ファイルを選択してください。",
    "working": "処理中…"
  },
  "app-compress": {
    "compressing_label": "圧縮中…",
    "err_invalid_target": "有効な目標サイズを入力してください。",
    "err_no_outcome": "最低品質でも{target}まで下げられませんでした。より大きな目標を試すか、形式を変更するか、「リサイズを許可」を有効にしてください。",
    "dims_resized": "{w}×{h}にリサイズ(元は{ow}×{oh})",
    "dims_original": "元のサイズ{w}×{h}",
    "status_within_target": "目標内、{dims}。",
    "status_closest_resized": "可能な限り近いサイズ(リサイズしても目標が小さすぎました)、{dims}。",
    "status_closest_noresize": "リサイズなしで可能な最小サイズ、{dims}。",
    "resize_nudge_question": "これがリサイズなしでの最小ファイルです。{target}に到達するためリサイズを有効にしますか?",
    "enable_resize_retry_btn": "リサイズを有効にして再圧縮",
    "format_nudge_question": "PNGは可逆圧縮のため、写真ではJPEGやWebPより大きなファイルになりがちです。JPEGに切り替えて再圧縮しますか?",
    "switch_to_jpeg_retry_btn": "JPEGに切り替えて再圧縮",
    "result_success": "<strong>画像を正常に圧縮しました。</strong> <strong>{size}</strong>。{statusLine}",
    "result_partial": "<strong>可能な限り縮小しました。</strong> <strong>{size}</strong>。{statusLine}",
    "result_larger_than_original": "<strong>リサイズなしで圧縮できる限界です:</strong> <strong>{size}</strong>。元のファイル({origSize})よりわずかに大きくなっています。{statusLine}",
    "download_button": "{filename}をダウンロード",
    "err_generic": "<strong>この画像を圧縮できませんでした。</strong> {msg}。別の画像を試すか、形式を変えて再試行してください。",
    "btn_compress_default": "目標サイズまで圧縮"
  },
  "app-json": {
    "empty_input": "入力が空です",
    "line_col_suffix": " ({line}行目、{col}列目)",
    "item_singular": "件",
    "item_plural": "件",
    "more_items_not_shown": "…他{n}件は非表示"
  },
  "app-markdown": {
    "preview_unavailable": "現在プレビューは利用できません。",
    "renderer_failed": "Markdownレンダラーの読み込みに失敗しました。接続を確認してページを再読み込みしてください。入力内容は失われていません。",
    "render_failed_title": "このMarkdownをレンダリングできませんでした。",
    "render_failed_suffix": "。直前の変更を元に戻してみてください。"
  },
  "app-password": {
    "strength_weak": "弱い",
    "strength_fair": "普通",
    "strength_strong": "強い",
    "strength_vstrong": "非常に強い",
    "entropy_out": "エントロピー ~{n} ビット"
  },
  "app-placeholder": {
    "placeholder_ready": "プレースホルダー完成:{w}×{h}、{size}、{fmt}",
    "swatch_brand_pink": "ブランドピンク",
    "swatch_neutral_gray": "ニュートラルグレー",
    "swatch_slate": "スレートグレー",
    "swatch_sky_blue": "スカイブルー",
    "swatch_soft_beige": "ソフトベージュ",
    "swatch_mint": "ミント"
  },
  "app-qrcode": {
    "prompt_enter_text": "URLまたはテキストを入力してQRコードを生成してください。",
    "err_too_much_text": "1つのQRコードには文字数が多すぎます。短くしてみてください。",
    "err_not_an_image": "これは画像ファイルではないようです。PNG、JPG、SVGを試してください。",
    "err_load_failed": "その画像を読み込めませんでした。別のファイルを試してください。"
  },
  "app-removebg": {
    "err_lib_not_loaded": "背景削除ライブラリの読み込みに失敗しました。接続を確認してページを再読み込みしてください。",
    "err_model_timeout": "セグメンテーションモデルの読み込みに時間がかかりすぎました。接続を確認して再試行してください。",
    "err_processing_timeout": "処理に時間がかかりすぎました。より小さい画像(400万画素未満が最適)を試してください。",
    "loading_model_label": "モデルを読み込み中…",
    "processing_label": "処理中…",
    "loading_model_status": "セグメンテーションモデルを読み込み中:約5.5MB、ブラウザセッションごとに一度だけ発生します。",
    "result_success": "<strong>背景を正常に削除しました。</strong> 人物が主要な被写体の写真で最もよく機能します。品質は軽量モデルに依存し、画像自体には依存しません。",
    "err_generic_prefix": "背景を削除できませんでした。",
    "err_unexpected": "予期しないエラーが発生しました。",
    "btn_remove_default": "背景を削除"
  },
  "app-slug": {
    "batch_empty_hint": "上にタイトルを貼り付けてください。1行に1つ。",
    "copied_all": "すべてコピーしました"
  },
  "app-testfile": {
    "err_invalid_size": "有効な正の数値サイズを入力してください。",
    "err_max_size": "ブラウザでサポートされる最大サイズは2GBです(それ以上だとタブが閉じるおそれがあります)。",
    "generating_label": "生成中…",
    "result_exact": "<strong>正確に一致しました。</strong> {size}を生成しました。",
    "result_offby": "<strong>{actual}</strong>を生成しました({target}を要求、差は{diff}バイト。一部の形式には構造上の最小サイズやパディングがあります)。",
    "result_success_prefix": "ファイルを正常に生成しました。",
    "download_button": "{filename}をダウンロード",
    "err_generic": "<strong>このファイルを生成できませんでした。</strong> {msg}。より小さいサイズか別の拡張子を試してください。",
    "btn_generate_default": "ファイルを生成"
  },
  "app-textlimit": {
    "err_invalid_limit": "1以上の文字数を入力してください。",
    "result_generated": "<strong>正確に{n}文字を生成しました</strong>",
    "spaces_included": "(スペースを含む)。",
    "spaces_excluded": "(スペースはカウントに含まれません)。",
    "preset_suffix_characters": "{n}文字"
  }
};
