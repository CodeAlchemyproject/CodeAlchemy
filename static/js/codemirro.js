//C:text/x-csrc C++:text/x-c++src Python:python Java:text/x-java
// 載入 CodeMirror 編輯器

// 初始化 CodeMirror 編輯器
var editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
    lineNumbers: true,
    indentUnit: 4,
    mode: 'python',
    extraKeys: { "Ctrl-Space": "autocomplete" },
});

// 註冊自定義提示詞
CodeMirror.registerHelper('hint', 'customHint', function (editor) {
    var cursor = editor.getCursor();
    var token = editor.getTokenAt(cursor);
    var currentWord = token.string;

    // 自定義的提示詞列表
    var keywords = [];
    switch (editor.getOption("mode")) {
        case 'python':
            keywords = [
                'def', 'class', 'import', 'from', 'for', 'while', 'if', 'elif', 'else', 'try', 'except', 'finally',
                'with', 'as', 'lambda', 'return', 'yield', 'global', 'nonlocal', 'assert', 'break', 'continue',
                'del', 'pass', 'raise', 'True', 'False', 'None', 'and', 'or', 'not', 'is', 'in', 'print', 'input',
                'len', 'open', 'range', 'int', 'float', 'str', 'list', 'dict', 'set', 'tuple', 'super', '__init__',
                'property', 'staticmethod', 'classmethod', 'abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes',
                'callable', 'chr', 'complex', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'format', 'frozenset',
                'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'isinstance', 'issubclass', 'iter',
                'len', 'locals', 'map', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'repr', 'reversed', 'round',
                'setattr', 'slice', 'sorted', 'sum', 'type', 'vars', 'zip', 'math', 'sys', 'os', 'random', 'time',
                're', 'subprocess', 'shutil', 'itertools', 'functools', 'collections', 'asyncio', 'threading',
                'multiprocessing', 'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'flask', 'django', 'bool',
                'bytes', 'complex', 'memoryview', 'frozenset', 'range', 'bytearray', 'Exception', 'BaseException',
                'FileNotFoundError', 'IndexError','KeyError', 'KeyboardInterrupt', 'ValueError', 'AttributeError',
                'TypeError', 'IOError', 'OSError','ArithmeticError', 'ImportError', 'NameError', 'OverflowError',
                'ZeroDivisionError', 'StopIteration','GeneratorExit', 'MemoryError', 'NotImplemented', 'super',
                'self', '__name__', '__main__', '__file__'
            ];
            break;
        case 'text/x-csrc':
        case 'text/x-c++src':
            keywords = [
                'int', 'float', 'double', 'char', 'void', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default',
                'return', 'break', 'continue', 'struct', 'union', 'typedef', 'enum', 'const', 'volatile', 'static', 'extern',
                'register', 'signed', 'unsigned', 'short', 'long', 'goto', 'sizeof', '#include', '#define', '#ifdef', '#ifndef',
                '#endif', '#pragma', 'printf', 'scanf', 'fgets', 'fputs', 'fopen', 'fclose', 'malloc', 'free', 'NULL',
                'fwrite', 'fread', 'stderr', 'stdin', 'stdout', 'time', 'clock', 'exit', 'system', 'memcmp', 'memcpy', 'memmove',
                'strcat', 'strcmp', 'strcpy', 'strlen', 'strncmp', 'strncpy', 'strstr', 'fseek', 'ftell', 'rewind', 'fgetc',
                'fputc', 'feof', 'rand', 'srand', 'perror', 'abort', 'qsort', 'bsearch', 'va_list', 'va_start', 'va_end',
                'inline', 'restrict', 'complex', '_Bool', '_Complex', '_Imaginary', 'offsetof', 'static_assert', 'aligned_alloc',
                'calloc', 'realloc', 'free', 'memset', 'memchr', 'sprintf', 'sscanf', 'vprintf', 'vfprintf', 'vsprintf'
            ];
            break;
        case 'text/x-java':
            keywords = [
                'public', 'private', 'protected', 'class', 'interface', 'abstract', 'implements', 'extends', 'static',
                'final', 'void', 'int', 'float', 'double', 'char', 'boolean', 'String', 'new', 'return', 'if', 'else', 'switch',
                'case', 'default', 'for', 'while', 'do', 'break', 'continue', 'try', 'catch', 'finally', 'throw', 'throws',
                'import', 'package', 'super', 'this', 'null', 'true', 'false', 'instanceof', 'enum', 'synchronized',
                'volatile', 'transient', 'native', 'strictfp', 'assert', 'System.out.println', 'Scanner', 'List', 'ArrayList',
                'HashMap', 'LinkedList', 'Set', 'Map', 'Iterator', 'Comparable', 'Comparator', 'Thread', 'Runnable',
                'Callable', 'Executor', 'Executors', 'try-with-resources', 'File', 'InputStream', 'OutputStream',
                'FileInputStream', 'FileOutputStream', 'BufferedReader', 'BufferedWriter', 'StringBuilder', 'StringBuffer',
                'TreeMap', 'TreeSet', 'PriorityQueue', 'Deque', 'Arrays', 'Collections', 'Math', 'Random', 'Optional',
                'Stream', 'Collectors', 'Files', 'Paths', 'Path', 'Charset', 'FileReader', 'FileWriter', 'ObjectInputStream',
                'ObjectOutputStream', 'Serializable', 'URLConnection', 'HttpURLConnection', 'Socket', 'ServerSocket',
                'AtomicInteger', 'AtomicLong', 'ReentrantLock', 'Lock', 'Semaphore', 'CyclicBarrier', 'CountDownLatch',
                'CompletableFuture', 'Future', 'ExecutorService', 'ScheduledExecutorService', 'ForkJoinPool', 'Phaser',
                'Annotation', 'Override', 'Deprecated', 'SuppressWarnings', 'FunctionalInterface', 'Predicate', 'Consumer',
                'Supplier', 'BiFunction', 'UnaryOperator', 'BinaryOperator'
            ];
            break;
        default:
            keywords = [
                'function', 'var', 'let', 'const', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue',
                'return', 'try', 'catch', 'finally', 'throw', 'new', 'this', 'typeof', 'instanceof', 'in', 'of', 'null',
                'undefined', 'true', 'false', 'class', 'extends', 'constructor', 'static', 'import', 'export', 'default',
                'async', 'await', 'yield', 'Promise', 'console.log', 'JSON.parse', 'JSON.stringify', 'Math', 'Date', 'setTimeout',
                'setInterval', 'clearTimeout', 'clearInterval', 'fetch', 'window', 'document', 'getElementById',
                'querySelector', 'addEventListener', 'removeEventListener', 'Object', 'Array', 'Map', 'Set', 'WeakMap',
                'WeakSet', 'reduce', 'filter', 'forEach', 'includes', 'push', 'pop', 'shift', 'unshift', 'slice', 'splice',
                'Promise.all', 'Promise.race', 'Promise.resolve', 'Promise.reject', 'localStorage', 'sessionStorage',
                'history', 'location', 'navigator', 'screen', 'alert', 'confirm', 'prompt', 'RegExp', 'Error', 'TypeError',
                'fetch', 'async function', 'await', 'Symbol', 'Proxy', 'Reflect', 'Intl', 'atob', 'btoa', 'encodeURIComponent',
                'decodeURIComponent', 'performance', 'WebSocket', 'XMLHttpRequest', 'Promise.any', 'Promise.allSettled',
                'BigInt', 'WeakRef', 'FinalizationRegistry', 'AbortController', 'AbortSignal', 'structuredClone',
                'queueMicrotask', 'DataView', 'ArrayBuffer', 'SharedArrayBuffer', 'Atomics', 'import.meta', 'globalThis'
            ];
    }



    // 顯示符合條件的提示
    var list = keywords.filter(function (keyword) {
        return keyword.startsWith(currentWord);
    });

    // 構建 from 和 to 的位置對象
    var from = CodeMirror.Pos(cursor.line, token.start);
    var to = CodeMirror.Pos(cursor.line, token.end);

    return {
        list: list,
        from: from,
        to: to
    };
});

// 自動顯示提示詞的邏輯
editor.on('changes', function (cm, changeObj) {
    // 使用 "changes" 而不是 "inputRead" 來監聽編輯器變更
    cm.showHint({
        hint: CodeMirror.hint.customHint,
        completeSingle: false  // 不自動選擇第一個提示詞，讓用戶自行選擇
    });

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
selectLanguageButton.addEventListener('click', function (event) {
    if (event.target.tagName === 'A') {
        // 取得選項中的 data-mode 屬性值
        mode = event.target.getAttribute('data-mode');
        // 設定編輯器模式
        editor.setOption('mode', mode);
        // 自動完成提示可能會根據語言模式有所變化
        console.log("Mode changed to:", mode); // 調試輸出
        editor.setOption('extraKeys', {
            "Ctrl-Space": function (cm) {
                cm.showHint({ hint: CodeMirror.hint.customHint });
            }
        });
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
    // 隱藏之前的結果
    document.getElementById("passed").style.display = "none";
    document.getElementById("failed").style.display = "none";
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
        if (source === 'contest' && contestId) {
            formData.append("contest_id", contestId);
        }
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
    // 隱藏之前的結果
    document.getElementById("passed").style.display = "none";
    document.getElementById("failed").style.display = "none";
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
    var title = document.getElementsByClassName('display-6 mt-4')[0].innerText;
    var language = mode;  // mode 應該是你在代碼其他地方定義的變數
    var source = urlParams.get('source');
    var contestId = urlParams.get('contest_id');
    var code = editor.getValue(); // 從編輯器中獲取程式碼

    // 構建表單數據
    var formData = new FormData();
    formData.append("type", type);
    formData.append("problem_id", problem_id);
    formData.append("title", title);
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