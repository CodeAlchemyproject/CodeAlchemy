// 取得下拉選單
var selectLanguageButton = document.getElementById('select_language_button');
mode='c'
// 監聽點擊事件
selectLanguageButton.addEventListener('click', function (event) {
    // 確保點擊的是 a 標籤
    if (event.target.tagName === 'A') {
        // 取得選項中的 value 屬性值
        mode = event.target.getAttribute('value');
    }
});


document.getElementById("test_btn").addEventListener("click", function () {
    var language = mode
    // 获取包含 <span> 标签的内容
    var code = document.querySelector('.cm-number')?document.querySelector('.cm-number').innerHTML : null;
    var formData = new FormData();
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