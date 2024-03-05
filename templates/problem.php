<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Problem</title>
    <?php include("_site_header.php"); ?>
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
    <div style="display:flex;">
    <div style="color:white;width:10vw;height:100vh;display:flex;flex-direction: column;">
        <div style="background-color: #6A7FC1;height:15.6vh">測試</div>
        <div>提交答案</div>
        <div>排行</div>
        <div>分析</div>
        <div>切換程式語言</div>
    </div>
    <div>
        a001.哈囉
        學習所有程式語言的第一個練習題 請寫一個程式，可以讀入指定的字串，並且輸出指定的字串。
        比如：輸入字串 "world", 則請輸出 "hello, world"
    </div>
    </div>
</body>

</html>