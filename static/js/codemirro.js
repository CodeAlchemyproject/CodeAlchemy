//C:text/x-csrc C++:text/x-c++src Python:python Java:text/x-java
// 載入 CodeMirror 編輯器

var editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
  // 設定行號
  lineNumbers: true,
  // 設定縮排單位
  indentUnit: 4,
  // 初始模式（默认为 C）
  mode: 'python'
});

// 取得下拉選單
var selectLanguageButton = document.getElementById('select_language_button');
var mode='python';
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
//測試
document.getElementById("test_btn").addEventListener("click", function () {
  var type = 'test'
  var problem_id = document.getElementById('problem_id').innerHTML
  var language = mode
  // 获取所有具有类名为 'CodeMirror-line' 的 <pre> 元素
  var code = editor.getValue();;
  var formData = new FormData();
  formData.append("type", type)
  formData.append("problem_id", problem_id)
  formData.append("language", language);
  formData.append("code", code);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/problem");
  xhr.send(formData);
});
//上傳
document.getElementById("upload_btn").addEventListener("click", function () {
  var type = 'upload'
  var problem_id = document.getElementById('problem_id').innerHTML
  var language = mode
  // 获取所有具有类名为 'CodeMirror-line' 的 <pre> 元素
  var code = editor.getValue();;
  var formData = new FormData();
  formData.append("type", type)
  formData.append("problem_id", problem_id)
  formData.append("language", language);
  formData.append("code", code);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/problem");
  xhr.send(formData);
});