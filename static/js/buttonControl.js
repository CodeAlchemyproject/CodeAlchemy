

// 函數用於設置loginStatus值
function setLoginStatus(status) {
    loginStatus = status;
}

// 如果loginStatus為False，則禁用測試和上傳按鈕
if (!loginStatus) {
    document.getElementById("test_btn").disabled = true;
    document.getElementById("upload_btn").disabled = true;
}
function test() {
    // 檢查登錄狀態
    if (!loginStatus) {
        // 如果未登錄，顯示警告視窗
        alert("Please login to perform this action.");
        return;
    }
}

function upload() {
    // 檢查登錄狀態
    if (!loginStatus) {
        // 如果未登錄，顯示警告視窗
        alert("Please login to perform this action.");
        return;
    }
}
