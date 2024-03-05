<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login-CodeAlchemy</title>
    <script src="https://accounts.google.com/gsi/client" async></script>
    <?php include("_site_header.php"); ?>
</head>

<body>
    <?php include("_site_navbar.php") ?>
    <div class="login_box">
        <div style="margin-top: 5vh;margin-bottom: 2vh;">
            <h1>登入</h1>
        </div>
        <div><input type="text" placeholder="暱稱或電子郵件"></div>
        <div><input type="password" placeholder="密碼"></div>
        <div><a href="./forget_password.php" style="text-decoration: none;color: black;">忘記密碼</a></div>
        <div><a href="#">
                <button class="submit_btn">登入</button>
            </a>
        </div>
        <!-- Google登入按鈕 -->
        <div style="margin: 10px;">
            <div id="g_id_onload" data-client_id="570075629720-t8lnamkjs4kggo6dimruitguvs6usch8.apps.googleusercontent.com" data-context="signin" data-ux_mode="popup" data-login_uri="http://localhost/problem_list.php" data-nonce="" data-auto_prompt="false">
            </div>

            <div class="g_id_signin" data-type="standard" data-shape="rectangular" data-theme="outline" data-text="signin_with" data-size="large" data-logo_alignment="left" data-width="50%">
            </div>
        </div>
</body>

</html>