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

// 顯示和隱藏 loading 視窗的函數
function showLoading() {
    document.getElementById("staticBackdrop").style.display = "block";
}

function hideLoading() {
    document.getElementById("staticBackdrop").style.display = "none";
    // 手動移除 backdrop
    var backdrops = document.getElementsByClassName('modal-backdrop');
    while (backdrops.length > 0) {
        backdrops[0].parentNode.removeChild(backdrops[0]);
    }
}
// 取得下拉選單
var selectLanguageButton = document.getElementById('select_language_button');
var mode = 'python';
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

// 定義變數以保存使用者 ID
var userId = null;
document.addEventListener("DOMContentLoaded", function () {

    // 發送請求以獲取使用者 ID
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_user_id", true);  // 這裡的路徑是之前後端定義的接口
    xhr.send();

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                userId = response.user_id;
                // console.log("使用者 ID: ", userId);
                // 你可以在這裡使用 userId 或將其保存到全局變數中以供後續使用
            }
        }
    };
});
// 監聽按鈕點擊事件
document.getElementById("test_btn").addEventListener("click", function () {
    var loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    var loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

    if (!userId) {
        // 如果沒有取得 userId，顯示登入提示模態視窗
        loginModal.show();
        return;  // 阻止請求發送
    } else {
        // 如果已登入，顯示測試中的模態視窗
        loadingModal.show();

        // 這裡可以繼續執行你的後續請求邏輯
        var type = 'test';  // 預設是 test
        var urlParams = new URLSearchParams(window.location.search);
        var source = urlParams.get('source');
        var contestId = urlParams.get('contest_id');
        var problem_id = document.getElementById('problem_id').innerHTML;
        var language = mode;

        // 獲取編輯器中的程式碼
        var code = editor.getValue();

        // 構建表單數據
        var formData = new FormData();
        formData.append("user_id", userId);  // 添加使用者 ID
        formData.append("type", type);
        formData.append("problem_id", problem_id);
        formData.append("language", language);
        formData.append("code", code);
        formData.append("source", source);

        // 發送 POST 請求到伺服器
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/problem");
        xhr.send(formData);

        // 處理伺服器返回的數據
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    loadingModal.hide();  // 請求完成後隱藏 loading 視窗
                    var responseData = JSON.parse(xhr.responseText);
                    var result = responseData.result;
                    var message = responseData.message;
                    var runTime = responseData.run_time;
                    var memory = responseData.memory;

                    if (result) {
                        document.getElementById("passed_status").innerText = "測試通過";
                        document.getElementById("passed_run_time").innerText = "執行時間：" + runTime + "毫秒";
                        document.getElementById("passed_memory").innerText = "記憶體使用量：" + memory + "MB";
                        document.getElementById("passed").style.display = "block";
                    } else {
                        document.getElementById("failed_status").innerText = "測試失敗";
                        document.getElementById("failed_error_reason").innerText = "錯誤原因：" + message;
                        document.getElementById("failed").style.display = "block";
                    }
                } else {
                    console.error('請求失敗');
                }
            }
        };
    }
});
//上傳
// 監聽按鈕點擊事件
document.getElementById("upload_btn").addEventListener("click", function () {
    // 初始化模態視窗
    var loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    var loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

    // 檢查使用者是否已登入
    if (!userId) {
        loginModal.show(); // 如果沒有取得 userId，顯示登入提示模態視窗
        return;  // 阻止請求發送
    }

    // 如果已登入，顯示測試中的模態視窗
    loadingModal.show();

    // 獲取必要的參數
    var type = 'upload';
    var urlParams = new URLSearchParams(window.location.search);
    var problem_id = document.getElementById('problem_id').innerText;
    var language = mode;  // mode 應該是你在代碼其他地方定義的變數
    var source = urlParams.get('source');
    var contestId = urlParams.get('contest_id');
    var code = editor.getValue(); // 從編輯器中獲取程式碼

    // 構建表單數據
    var formData = new FormData();
    formData.append("type", type);
    formData.append("problem_id", problem_id);
    formData.append("language", language);
    formData.append("code", code);
    formData.append("source", source);

    // 如果是來自 contest 的請求，添加 contest_id
    if (source === 'contest' && contestId) {
        formData.append("contest_id", contestId);
    }

    // 發送 POST 請求到伺服器
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/problem", true);

    // 處理伺服器返回的數據
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // 隱藏 loading 視窗
                loadingModal.hide();

                // 處理伺服器返回的響應
                var responseData = JSON.parse(xhr.responseText);
                var result = responseData.result;
                var message = responseData.message;
                var runTime = responseData.run_time;
                var memory = responseData.memory;

                if (result) {
                    // 測試通過，顯示成功信息
                    document.getElementById("passed_status").innerText = "測試通過";
                    document.getElementById("passed_run_time").innerText = "執行時間：" + runTime + "毫秒";
                    document.getElementById("passed_memory").innerText = "記憶體使用量：" + memory + "MB";
                    document.getElementById("passed").style.display = "block"; // 顯示 passed 的信息
                } else {
                    // 測試失敗，顯示錯誤信息
                    document.getElementById("failed_status").innerText = "測試失敗";
                    document.getElementById("failed_error_reason").innerText = "錯誤原因：" + message;
                    document.getElementById("failed").style.display = "block"; // 顯示 failed 的信息
                }
            } else {
                // 請求失敗，隱藏 loading 視窗並顯示錯誤信息
                loadingModal.hide();
                console.error('請求失敗，狀態碼：', xhr.status);
                alert('提交失敗，請稍後再試。');
            }
        }
    };

    // 發送表單數據
    xhr.send(formData);
});