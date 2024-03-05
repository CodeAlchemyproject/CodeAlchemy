<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-signin-client_id" content="570075629720-t8lnamkjs4kggo6dimruitguvs6usch8.apps.googleusercontent.com"> <!-- XXXXXXXXXXXXX為Client ID-->
    <title>Document</title>

    <script src="https://apis.google.com/js/platform.js" async defer></script>
    <script src="https://code.jquery.com/jquery-3.7.1.js" integrity="sha256-UgvvN8vBkgO0luPSUl2s8TIlOSYRoGFAX4jlCIm9Adc=" crossorigin="anonymous"></script>
</head>
<body>
    <div id="profileinfo"></div>
    <div class="g-signin2" data-onsuccess="onSignIn"></div>
    <script>
        function onSignIn(googleUser){
            var profile = googleUser.getBasicProfile();

            $("#profileinfo").append("<h2>Name- " + profile.getName() + "</h2>");
            $("#profileinfo").append("<img style='width: 150px;height:150px' src='"+profile.getImageUrl()+"'><br><br>");
            $("#profileinfo").append("<p>Your email is: "+profile.getEmail()+"</p>");
        }
    </script>
    <br>
    <button type="button" class="btn btn-danger" onclick="signOut();">Sign Out</button>
    <script>
        function signOut(){
            var auth2 = gapi.auth2.getAuthInstance();
            auth2.signOut().then(function(){
                console.log("User signed out.");
            $("#profileinfo").empty();
            $("#profileinfo").append("<h2>Signed Out.</h2>")
            })
        }
    </script>
</body>
</html>