// 取得下拉選單
var selectLanguageButton = document.getElementById('select_language_button');
mode='python'
// 監聽點擊事件
selectLanguageButton.addEventListener('click', function (event) {
    // 確保點擊的是 a 標籤
    if (event.target.tagName === 'A') {
        // 取得選項中的 value 屬性值
        mode = event.target.getAttribute('value');
    }
});
var editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
    // 設定行號
    lineNumbers: true,
  });
document.getElementById("test_btn").addEventListener("click", function () {
    var type = 'test'
    var problem_id = document.getElementById('problem_id').innerHTML
    var language = mode
    // 获取所有具有类名为 'CodeMirror-line' 的 <pre> 元素
    var preElements = document.querySelectorAll('pre.CodeMirror-line');
    // 遍历每个 <pre> 元素并提取其内容
    var code = editor.getValue();;

    var formData = new FormData();
    formData.append("type", type)
    formData.append("problem_id", problem_id)
    formData.append("language", language);
    formData.append("code", code);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/problem_submit");
    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log(xhr.responseText);
        } else {
            console.error(xhr.responseText);
        }
    };
    xhr.send(formData);
});