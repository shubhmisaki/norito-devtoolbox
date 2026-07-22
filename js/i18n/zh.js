// Auto-generated i18n dictionary for the zh localized pages.
// Loaded before js/i18n-runtime.js and the app-*.js scripts on every
// /zh/ page, so i18nFor(fileId) resolves to translated strings
// instead of falling back to the English defaults baked into each script.
window.NORITO_I18N = {
  "common": {
    "copied": "已复制",
    "please_choose_image": "请选择一个图片文件。",
    "working": "处理中…"
  },
  "app-compress": {
    "compressing_label": "压缩中…",
    "err_invalid_target": "请输入有效的目标大小。",
    "err_no_outcome": "即使使用最低质量,也无法压缩到 {target} 以下。请尝试更大的目标大小、更换格式,或开启“允许调整尺寸”。",
    "dims_resized": "已调整为 {w}×{h}（原为 {ow}×{oh}）",
    "dims_original": "保持原始尺寸 {w}×{h}",
    "status_within_target": "已达到你的目标大小,{dims}。",
    "status_closest_resized": "已生成最接近的可行大小（即使调整尺寸,目标仍然过小）,{dims}。",
    "status_closest_noresize": "在不调整尺寸的情况下能达到的最小大小,{dims}。",
    "resize_nudge_question": "这已经是不调整尺寸能达到的最小文件了。要开启调整尺寸以达到 {target} 吗?",
    "enable_resize_retry_btn": "开启调整尺寸并重新压缩",
    "format_nudge_question": "PNG 是无损格式,对于照片通常比 JPEG 或 WebP 生成更大的文件。要切换到 JPEG 并重新压缩吗?",
    "switch_to_jpeg_retry_btn": "切换到 JPEG 并重新压缩",
    "result_success": "<strong>图片压缩成功。</strong> 大小为 <strong>{size}</strong>。{statusLine}",
    "result_partial": "<strong>已尽可能缩小。</strong> 大小为 <strong>{size}</strong>。{statusLine}",
    "result_larger_than_original": "<strong>这是不调整尺寸情况下能压缩到的最小体积:</strong> <strong>{size}</strong>,比原文件（{origSize}）略大。{statusLine}",
    "download_button": "下载 {filename}",
    "err_generic": "<strong>无法压缩该图片。</strong>{msg}。请尝试其他图片,或更换格式后重试。",
    "btn_compress_default": "压缩到目标大小"
  },
  "app-json": {
    "empty_input": "输入为空",
    "line_col_suffix": "（第 {line} 行，第 {col} 列）",
    "item_singular": "项",
    "item_plural": "项",
    "more_items_not_shown": "……还有 {n} 项未显示"
  },
  "app-markdown": {
    "preview_unavailable": "预览暂时不可用。",
    "renderer_failed": "Markdown 渲染器未能加载。请检查网络连接并刷新页面。你输入的内容不会丢失。",
    "render_failed_title": "无法渲染此 Markdown。",
    "render_failed_suffix": "。请尝试撤销你最后的修改。"
  },
  "app-password": {
    "strength_weak": "弱",
    "strength_fair": "中等",
    "strength_strong": "强",
    "strength_vstrong": "非常强",
    "entropy_out": "~{n} 比特熵"
  },
  "app-placeholder": {
    "placeholder_ready": "占位图已生成：{w}×{h}，{size}，{fmt}",
    "swatch_brand_pink": "品牌粉",
    "swatch_neutral_gray": "中性灰",
    "swatch_slate": "石板灰",
    "swatch_sky_blue": "天空蓝",
    "swatch_soft_beige": "柔和米色",
    "swatch_mint": "薄荷绿"
  },
  "app-qrcode": {
    "prompt_enter_text": "输入网址或文本以生成二维码。",
    "err_too_much_text": "文本过长,无法生成单个二维码。请尝试缩短内容。",
    "err_not_an_image": "这似乎不是图片文件。请尝试 PNG、JPG 或 SVG 格式。",
    "err_load_failed": "无法加载该图片。请尝试其他文件。"
  },
  "app-removebg": {
    "err_lib_not_loaded": "背景去除库未能加载。请检查网络连接并刷新页面。",
    "err_model_timeout": "分割模型加载时间过长。请检查网络连接后重试。",
    "err_processing_timeout": "处理时间过长。请尝试更小的图片（400 万像素以内效果最佳）。",
    "loading_model_label": "正在加载模型…",
    "processing_label": "处理中…",
    "loading_model_status": "正在加载人像抠图模型及其运行环境：约 18 MB,每个浏览器会话仅需加载一次。",
    "result_success": "<strong>背景去除成功。</strong>在人物是照片主体的情况下效果最佳。",
    "err_generic_prefix": "无法去除背景。",
    "err_unexpected": "发生了意外错误。",
    "btn_remove_default": "去除背景"
  },
  "app-slug": {
    "batch_empty_hint": "在上方粘贴标题,每行一个。",
    "copied_all": "已全部复制"
  },
  "app-testfile": {
    "err_invalid_size": "请输入有效的正数大小。",
    "err_max_size": "浏览器内支持的最大尺寸为 2 GB（更大的文件可能导致标签页崩溃）。",
    "generating_label": "生成中…",
    "result_exact": "<strong>精确匹配。</strong>已生成 {size}。",
    "result_offby": "已生成 <strong>{actual}</strong>（目标为 {target},相差 {diff} 字节;部分格式存在最小结构或填充要求）。",
    "result_success_prefix": "文件生成成功。",
    "download_button": "下载 {filename}",
    "err_generic": "<strong>无法生成该文件。</strong>{msg}。请尝试更小的大小,或更换扩展名。",
    "btn_generate_default": "生成文件"
  },
  "app-textlimit": {
    "err_invalid_limit": "请输入 1 或以上的字符数。",
    "result_generated": "<strong>已精确生成 {n} 个字符</strong>",
    "spaces_included": "（含空格）。",
    "spaces_excluded": "（计数不含空格）。",
    "preset_suffix_characters": "{n} 个字符"
  }
};
