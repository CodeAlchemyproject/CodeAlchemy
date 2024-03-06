<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!--CSS -->
    <script>
        fetch('./_site_header.html')
            .then(response => response.text())
            .then(data => {
                // 插入到指定位置
                document.body.innerHTML = data + document.body.innerHTML;
            })
            .catch(error => console.error('Error fetching nav.html:', error));
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-p34f1UUtsS3wqzfto5wAAmdvj+osOnFyQFpp4Ua3gs/ZVWx6oOypYoCJhGGScy+8" crossorigin="anonymous"></script>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            // 获取所有 .problem_bar_item 元素
            var items = document.querySelectorAll('.problem_bar_item');
            // 设置全局 CSS 变量 --count 的值为元素的数量
            document.documentElement.style.setProperty('--count', items.length);
        });
    </script>
</head>

<body>
    <script>
        fetch('./nav.html')
            .then(response => response.text())
            .then(data => {
                // 插入到指定位置
                document.body.innerHTML = data + document.body.innerHTML;
            })
            .catch(error => console.error('Error fetching nav.html:', error));
    </script>
    <!-- <div style="display:flex;"> -->
    <h1 class="display-6">a001.哈囉</h1>
    <h3 class="w-25 overflow-auto">學習所有程式語言的第一個練習題 請寫一個程式，可以讀入指定的字串，並且輸出指定的字串。
        比如：輸入字串 "world", 則請輸出 "hello, world"</h3>
    <!-- <div class="problem_bar">
            <div class="problem_bar_item">測試</div>
            <div class="problem_bar_item">提交答案</div>
            <div class="problem_bar_item">排行</div>
            <div class="problem_bar_item">分析</div>
            <div class="problem_bar_item show">切換程式語言</div>
            <div class="problem_bar_item hide">Python</div>
            <div class="problem_bar_item hide">C++</div>
            <div class="problem_bar_item hide">Java</div>
        </div> -->
    <!-- </div> -->
</body>

</html>