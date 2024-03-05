<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login-CodeAlchemy</title>
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
        <div><input type="text" placeholder="輸入電子郵件"></div>
        <div><a href="./resect_password.php">
                <button class="submit_btn">驗證</button>
            </a>
        </div>
    </div>
</body>

</html>