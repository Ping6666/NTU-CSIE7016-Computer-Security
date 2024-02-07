#!/usr/bin/php-cgi
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    if (!isset($_SERVER['FILE_FILENAME_FIRMWARE'])) {
        header('Location: '. $_SERVER['PHP_SELF']);
        exit;
    }

    $filePath = $_SERVER['FILE_FILENAME_FIRMWARE'];
    $output = null;
    $retval = null;
    exec("firmware_updater " . $filePath . " -d", $output, $retval);
    if ($retval != 0) {
        printf('<head><title>Settings - Firmware</title></head><script language="javascript">alert("Update firmware error."); window.location="%s"</script>', $_SERVER['PHP_SELF']);
        exit(1);
    }
    else {

    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Settings - Firmware</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    <script>
        function changeFileName() {
            try {
                const fileName = document.querySelector('input[name="firmware"]').files[0].name;
                document.getElementById("file-name").innerHTML = fileName;
            } catch (error) {
                document.getElementById("file-name").innerHTML = "No file chosen";
            }
        }

        function getCookie(cookieName) {
            const name = cookieName + "=";
            const decodedCookie = decodeURIComponent(document.cookie);
            const cookieArray = decodedCookie.split(';');

            for (let i = 0; i < cookieArray.length; i++) {
                let cookie = cookieArray[i].trim();
                if (cookie.indexOf(name) == 0) {
                    return cookie.substring(name.length, cookie.length);
                }
            }

            return null;
        }
        window.onload = function() {
            if (getCookie("auth.session-token") == null) {
                alert("Auth failed");
                location = "/cgi-bin/login.cgi";
            }
        };
    </script>
</head>
<body>
    <section class="section">
        <div class="container">
            <h1 class="title">Settings</h1>
            <div class="tabs">
                <ul>
                    <li><a href="/cgi-bin/control.cgi">Display</a></li>
                    <li><a href="/cgi-bin/manage.cgi">Manage</a></li>
                    <li class="is-active"><a href="/cgi-bin/firmware.cgi">Firmware</a></li>
                    <li><a href="/cgi-bin/show_secret.cgi">Show Secret</a></li>
                </ul>
            </div>

            <div class="box <?php if ($_SERVER['REQUEST_METHOD'] == "POST") {echo "is-hidden";} ?>">
                <h2 class="subtitle">Update Firmware</h2>

                <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post" enctype="multipart/form-data">
                    <div class="file has-name is-fullwidth">
                        <label class="file-label">
                            <input class="file-input" type="file" name="firmware" onchange="changeFileName()">
                            <span class="file-cta">
                                <span class="file-label">
                                    Choose a file ...
                                </span>
                            </span>
                            <span class="file-name" id="file-name">
                                No file chosen
                            </span>
                        </label>
                    </div>

                    <br>

                    <button class="button is-primary">Submit</button>
                </form>
            </div>

        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="block has-text-centered">
                <div class="box <?php if ($_SERVER['REQUEST_METHOD'] != "POST") {echo "is-hidden";} ?>" id="reboot">
                    <h1 class="title">Rebooting ...</h2>
                    <h2 class="subtitle">This page will reload automatically in 60 seconds.</h2>
                    <progress id="progress-bar" class="progress is-primary" value="0" max="100"></progress>
                    <button id="reload-button" class="button">Force Reload</button>

                    <script>
                        let start = new Date().getTime();
                        const progress = document.getElementById('progress-bar');
                        const reloadButton = document.getElementById('reload-button');

                        reloadButton.addEventListener('click', () => {
                            location = "/";
                        });

                        setInterval(() => {
                            const now = new Date().getTime();
                            const elapsed = now - start;
                            const percentage = (elapsed / 60000) * 100;
                            progress.value = percentage;
                            if (percentage >= 100) reloadButton.click();
                        }, 60);
                    </script>
                </div>
            </div>
        </div>
    </section>
</body>
</html>
