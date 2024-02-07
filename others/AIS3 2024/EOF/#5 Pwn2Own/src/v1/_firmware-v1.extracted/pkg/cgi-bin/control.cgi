#!/usr/bin/php-cgi
<?php
$displayDir = '/var/www/html/';
$displayFile = $displayDir . 'display.html';
$displayTemplate = $displayDir . 'template.html';
$previewFile = $displayDir . 'preview.html';
$configFile = $displayDir . 'config';
$contestFile = $displayDir . 'contest.html';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_SERVER['RESTART'])) {
        $config = file_get_contents($configFile);
        system("echo '$config' | nc 127.0.0.1 5487");
        header('Location: ' . $_SERVER['PHP_SELF']);
        exit;
    }
    $checkedOption = isset($_POST['displayType']) ? $_POST['displayType'] : '';
    $error = '';
    switch ($checkedOption) {
        case 'contest':
            file_put_contents($configFile, $contestFile);
            copy($contestFile, $previewFile);
            break;
        case 'picture':
            if ((! isset($_POST['image'])) || empty($_POST['image'])) {
                $error = "You should select an image to show.";
            }
            else {
                $image = $_POST['image'];
                $dir = $_SERVER['DOCUMENTS'] . '/../appweb/images/';
                $filePath = $dir . $image;
                if (!file_exists($filePath)) {
                    $error = "Image not found.";
                } else {
                    $targetPath = $displayDir . $image;
                    copy($filePath, $targetPath);
                    $content = file_get_contents($displayTemplate);
                    $content = str_replace("%displayType%", "image", $content);
                    $preview = str_replace("%imageURL%", "/images/" . $image, $content);
                    file_put_contents($previewFile, $preview);
                    $display = str_replace("%imageURL%", $displayDir . $image, $content);
                    file_put_contents($displayFile, $display);
                    file_put_contents($configFile, $displayFile);
                }
            }
            break;
        case 'text':
            if ((! isset($_POST['text'])) || empty($_POST['text'])) {
                $error = "You should input non-empty text content to show.";
            }
            else {
                $text = $_POST['text'];
                $content = file_get_contents($displayTemplate);
                $content = str_replace("%displayType%", "scrollingText", $content);
                $content = str_replace("%scrollText%", $text, $content);
                file_put_contents($previewFile, $content);
                file_put_contents($displayFile, $content);
                file_put_contents($configFile, $displayFile);
            }
            break;
        case 'video':
            if ((! isset($_POST['url'])) || empty($_POST['url'])) {
                http_response_code(400);
                $error = "You should provide the video URL to show.";
            }
            else {
              $url = $_POST['url'];
              printf('<head><title>Control Display</title></head><script language="javascript">alert("Please subscribe to our Premium Plan in order to show the video on the display."); window.location="%s"</script>', $url);
              exit();
            }
            break;
        default:
            http_response_code(400);
            exit("Unknown option.");
    }
    if (empty($error)) { ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control Display Done</title>
</head>
<body>
    <h2>Success!</h2>
    <a href="<?php echo $_SERVER['PHP_SELF']; ?>?action=preview">Preview</a>
    <a href="<?php echo $_SERVER['PHP_SELF']; ?>">Back</a>
</body>
    <?php } else { ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control Display</title>
</head>
<body>
    <h2>Error: <?php echo($error); ?></h2>
    <a href="<?php echo $_SERVER['PHP_SELF']; ?>">Back</a>
</body>
    <?php } ?>
<?php
} else if ($_SERVER['REQUEST_METHOD'] == 'GET' && isset($_GET) && isset($_GET['action']) && $_GET['action'] == 'preview') {
    $preview = file_get_contents($previewFile);
    print($preview);
} else { 
?>
  <!DOCTYPE html>
<html>
<head>
    <title>Settings - Display</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">

    <script>
        function changeDisplayType() {
            const displayType = document.querySelector('input[name="displayType"]:checked').id;
            if (displayType == "displayTypeContestActivity") {
                document.getElementById("contestSettings").classList.remove("is-hidden");
                document.getElementById("imageSettings").classList.add("is-hidden");
                document.getElementById("scrollingTextSettings").classList.add("is-hidden");
                document.getElementById("videoSettings").classList.add("is-hidden");
            } else if (displayType == "displayTypeImage") {
                document.getElementById("contestSettings").classList.add("is-hidden");
                document.getElementById("imageSettings").classList.remove("is-hidden");
                document.getElementById("scrollingTextSettings").classList.add("is-hidden");
                document.getElementById("videoSettings").classList.add("is-hidden");
            } else if (displayType == "displayTypeScrollingText") {
                document.getElementById("contestSettings").classList.add("is-hidden");
                document.getElementById("imageSettings").classList.add("is-hidden");
                document.getElementById("scrollingTextSettings").classList.remove("is-hidden");
                document.getElementById("videoSettings").classList.add("is-hidden");
            } else if (displayType == "displayTypeVideo") {
                document.getElementById("contestSettings").classList.add("is-hidden");
                document.getElementById("imageSettings").classList.add("is-hidden");
                document.getElementById("scrollingTextSettings").classList.add("is-hidden");
                document.getElementById("videoSettings").classList.remove("is-hidden");
            }
        }

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
            changeDisplayType();
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
                    <li class="is-active"><a href="/cgi-bin/control.cgi">Display</a></li>
                    <li><a href="/cgi-bin/manage.cgi">Manage</a></li>
                    <li><a href="/cgi-bin/firmware.cgi">Firmware</a></li>
                    <li><a href="/cgi-bin/show_secret.cgi">Show Secret</a></li>
                </ul>
            </div>
            <form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
                <div class="block">
                    <button class="button is-warning" name="restart">Restart Display</button>
                </div>

                <div class="box">
                    <h2 class="subtitle">Select Display Type</h2>
                    <label class="radio"><input type="radio" name="displayType" value="contest" onchange="changeDisplayType()" id="displayTypeContestActivity" checked> Contest Activity</label><br>
                    <label class="radio"><input type="radio" name="displayType" value="picture" onchange="changeDisplayType()" id="displayTypeImage"> Image</label><br>
                    <label class="radio"><input type="radio" name="displayType" value="text" onchange="changeDisplayType()" id="displayTypeScrollingText"> Scrolling Text</label><br>
                    <label class="radio"><input type="radio" name="displayType" value="video" onchange="changeDisplayType()" id="displayTypeVideo"> Video</label><br>
                </div>

                <div class="box is-hidden" id="contestSettings">
                    <h2 class="subtitle">Set Contest</h2>
                    <button class="button is-danger">Set</button>
                </div>

                <div class="is-hidden" id="imageSettings">
                    <div class="box">
                        <h2 class="subtitle">Select Image</h2>
                        <?php
                            $imageDirectory = "../appweb/images/";
                            $allowedExtensions = array("jpg", "png");
                            $imageFiles = array();

                            if ($handle = opendir($imageDirectory)) {
                                while (false !== ($entry = readdir($handle))) {
                                    $extension = pathinfo($entry, PATHINFO_EXTENSION);
                                    if (in_array($extension, $allowedExtensions)) {
                                        $imageFiles[] = $entry;
                                    }
                                }
                                closedir($handle);
                            }

                            if (!empty($imageFiles)) {
                                foreach ($imageFiles as $imageFile) {
                                    $imageUrl = "/images/" . $imageFile;
                                    echo '<div class="control">';
                                    echo '<label class="radio">';
                                    echo '<input type="radio" name="image" value="' . $imageFile . '"> ';
                                    echo "&nbsp;&nbsp;";
                                    echo '<img src="' . $imageUrl . '" alt="' . $imageFile . '" style="max-height: 50px; max-width: 50px;"> ';
                                    echo pathinfo($imageFile, PATHINFO_FILENAME);
                                    echo '</label>';
                                    echo '</div>';
                                }
                                echo '<br>';
                                echo '<button class="button is-danger" type="submit">Select</button>';
                            } else {
                                echo '<p>No images found.</p>';
                            }
                        ?>
                    </div>
                </div>

                <div class="box is-hidden" id="scrollingTextSettings">
                    <h2 class="subtitle">Scrolling Text Settings</h2>
                    <label class="label">Set the text be displayed</label>
                    <div class="field is-grouped">
                        <div class="control is-expanded">
                            <input class="input" type="text" name="text" placeholder="Text">
                        </div>
                        <div class="control">
                            <button class="button is-primary">Submit</button>
                        </div>
                    </div>
                </div>

                <div class="box is-hidden" id="videoSettings">
                    <h2 class="subtitle">Video Settings</h2>
                    <label class="label">Set the video url to be displayed</label>
                    <div class="field is-grouped">
                        <div class="control is-expanded">
                            <input class="input" type="text" name="url" placeholder="URL">
                        </div>
                        <div class="control">
                            <button class="button is-primary">Submit</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </section>
</body>
</html>

<?php } ?>
