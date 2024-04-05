//C:text/x-csrc C++:text/x-c++src Python:python Java:text/x-java
// 載入 CodeMirror 編輯器
var editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
  // 設定行號
  lineNumbers: true,
  // 設定縮排單位
  indentUnit: 4,
  // 初始模式（默认为 C）
  mode: 'text/x-csrc'
});

// 取得下拉選單
var selectLanguageButton = document.getElementById('select_language_button');

// 監聽點擊事件
selectLanguageButton.addEventListener('click', function (event) {
  // 確保點擊的是 a 標籤
  if (event.target.tagName === 'A') {
    // 取得選項中的 data-mode 屬性值
    mode = event.target.getAttribute('data-mode');
    // 設定編輯器模式
    editor.setOption('mode', mode);
  }
});