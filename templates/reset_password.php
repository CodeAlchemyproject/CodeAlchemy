<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset-CodeAlchemy</title>
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
    <div class="login_box">
        <div style="margin-top: 5vh;margin-bottom: 2vh;">
            <h1>忘記密碼</h1>
        </div>
        <div><input type="password" placeholder="新密碼"></div>
        <div><input type="password" placeholder="確認新密碼"></div>
        <div><a href="./login.php">
                <button class="submit_btn">送出</button>
            </a>
        </div>
    </div>
</body>

</html>