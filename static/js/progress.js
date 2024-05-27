// 設置全局變量用於存儲 interval ID
var intervalId;

// 監聽測試按鈕點擊事件
document.getElementById("test_btn").addEventListener("click", function () {
  // 重置進度條
  var progressBar = document.querySelector(".progress-bar");
  progressBar.style.width = "0%";
  progressBar.textContent = "0%";

  // 測試新的 interval，並保存其 ID
  var current_progress = 0;
  intervalId = setInterval(function () {
    current_progress += 1;
    progressBar.style.width = current_progress + "%";
    progressBar.textContent = current_progress + "%";

    if (current_progress >= 100) {
      clearInterval(intervalId);
      // 進度條到達100%自動關閉視窗
      var modal = document.getElementById("staticBackdrop");
      var modalInstance = bootstrap.Modal.getInstance(modal);
      modalInstance.hide();
    }
  }, 1000);
});

// 監聽停止按鈕點擊事件
document.getElementById("stop_btn").addEventListener("click", function () {
  // 如果 interval ID 存在，則清除 interval
  if (intervalId) {
    clearInterval(intervalId);
  }
});
/////////////////////////////////////////////////////////
// 監聽上傳按鈕點擊事件
document.getElementById("upload_btn").addEventListener("click", function () {
  // 重置進度條
  var progressBar = document.querySelector(".progress-bar");
  progressBar.style.width = "0%";
  progressBar.textContent = "0%";

  // 測試新的 interval，並保存其 ID
  var current_progress = 0;
  intervalId = setInterval(function () {
    current_progress += 5;
    progressBar.style.width = current_progress + "%";
    progressBar.textContent = current_progress + "%";

    if (current_progress >= 100) {
      clearInterval(intervalId);
      // 進度條到達100%自動關閉視窗
      var modal = document.getElementById("staticBackdrop");
      var modalInstance = bootstrap.Modal.getInstance(modal);
      modalInstance.hide();
    }
  }, 1000);
});

// 監聽停止按鈕點擊事件
document.getElementById("stop_btn").addEventListener("click", function () {
  // 如果 interval ID 存在，則清除 interval
  if (intervalId) {
    clearInterval(intervalId);
  }
});