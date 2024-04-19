// 設置全局變量用於存儲 interval ID
var intervalId;

// 監聽開始按鈕點擊事件
document.getElementById("test_btn").addEventListener("click", function () {
  // 重置進度條
  var progressBar = document.querySelector(".progress-bar");
  progressBar.style.width = "0%";
  progressBar.textContent = "0%";

  // 開始新的 interval，並保存其 ID
  var current_progress = 0;
  intervalId = setInterval(function () {
    current_progress += 5;
    progressBar.style.width = current_progress + "%";
    progressBar.textContent = current_progress + "%";

    if (current_progress >= 100) {
      clearInterval(intervalId);
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
