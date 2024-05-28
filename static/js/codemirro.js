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
}
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
// 監聽按鈕點擊事件
document.getElementById("test_btn").addEventListener("click", function () {
  var type = 'test';
  var problem_id = document.getElementById('problem_id').innerHTML;
  var language = mode;
  // 獲取編輯器中的程式碼
  var code = editor.getValue();
  // 構建表單數據
  var formData = new FormData();
  formData.append("type", type);
  formData.append("problem_id", problem_id);
  formData.append("language", language);
  formData.append("code", code);
  // 發送 POST 請求到伺服器
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/problem");
  xhr.send(formData);
  // 顯示 loading 視窗
  //showLoading();

  // 處理伺服器返回的數據
  xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
              hideLoading();  // 隱藏 loading 視窗
              var responseData = JSON.parse(xhr.responseText);
              // 提取返回的數據
              var result = responseData.result;
              var message = responseData.message;
              var runTime = responseData.run_time;
              var memory = responseData.memory;

              // 根據測試結果更新頁面內容
              if (result) {
                  // 測試通過，顯示 passed 狀態的信息
                  document.getElementById("passed_status").innerText = "測試通過";
                  document.getElementById("passed_run_time").innerText = "執行時間：" + runTime + "毫秒";
                  document.getElementById("passed_memory").innerText = "記憶體使用量：" + memory + "MB";
                  document.getElementById("passed").style.display = "block"; // 顯示 passed 的信息
              } else {
                  // 測試失敗，顯示 failed 狀態的信息
                  document.getElementById("failed_status").innerText = "測試失敗";
                  document.getElementById("failed_error_reason").innerText = "錯誤原因：" + message;
                  document.getElementById("failed").style.display = "block"; // 顯示 failed 的信息
              }
          } else {
              // 請求失敗，輸出錯誤信息到控制台
              console.error('請求失敗');
          }
      }
  };
});
//上傳
// 監聽按鈕點擊事件
document.getElementById("upload_btn").addEventListener("click", function () {
  var type = 'upload';
  var problem_id = document.getElementById('problem_id').innerHTML;
  var language = mode;
  // 獲取編輯器中的程式碼
  var code = editor.getValue();
  // 構建表單數據
  var formData = new FormData();
  formData.append("type", type);
  formData.append("problem_id", problem_id);
  formData.append("language", language);
  formData.append("code", code);
  // 發送 POST 請求到伺服器
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/problem");
  xhr.send(formData);
  // 顯示 loading 視窗
  showLoading();

  // 處理伺服器返回的數據
  xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
              hideLoading();  // 隱藏 loading 視窗
              var responseData = JSON.parse(xhr.responseText);
              // 提取返回的數據
              var result = responseData.result;
              var message = responseData.message;
              var runTime = responseData.run_time;
              var memory = responseData.memory;

              // 根據測試結果更新頁面內容
              if (result) {
                  // 測試通過，顯示 passed 狀態的信息
                  document.getElementById("passed_status").innerText = "測試通過";
                  document.getElementById("passed_run_time").innerText = "執行時間：" + runTime + "毫秒";
                  document.getElementById("passed_memory").innerText = "記憶體使用量：" + memory + "MB";
                  document.getElementById("passed").style.display = "block"; // 顯示 passed 的信息
              } else {
                  // 測試失敗，顯示 failed 狀態的信息
                  document.getElementById("failed_status").innerText = "測試失敗";
                  document.getElementById("failed_error_reason").innerText = "錯誤原因：" + message;
                  document.getElementById("failed").style.display = "block"; // 顯示 failed 的信息
              }
          } else {
              // 請求失敗，輸出錯誤信息到控制台
              console.error('請求失敗');
          }
      }
  };
});
