#!/usr/bin/php-cgi
<?php
$uploadDir = $_SERVER['DOCUMENTS'] . '/../appweb/images/';
$defaultID = '0';

if (!file_exists($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_SERVER['UPLOAD'])) {
        if (!isset($_SERVER['FILE_CLIENT_FILENAME_IMAGE']) || !isset($_SERVER['FILE_FILENAME_IMAGE'])) {
            printf('<head><title>Settings - Manage</title></head><script language="javascript">alert("Upload image error"); window.location="%s"</script>', $_SERVER['PHP_SELF']);
            exit(1);
        }
        $fileName = $_SERVER['FILE_CLIENT_FILENAME_IMAGE'];
        $filePath = $_SERVER['FILE_FILENAME_IMAGE'];
        $fileID = isset($_SERVER['IMAGE_ID']) ? $_SERVER['IMAGE_ID'] : $defaultID;
        $fileExtension = pathinfo($fileName, PATHINFO_EXTENSION);
        $targetPath = $uploadDir . $fileID . '.' . $fileExtension;
        copy($filePath, $targetPath);
    } elseif (isset($_SERVER['DOWNLOAD'])) {
        $url = isset($_SERVER['URL']) ? $_SERVER['URL'] : '';
        $id = isset($_SERVER['IMAGE_ID']) ? $_SERVER['IMAGE_ID'] : '';

        if (empty($url) || empty($id)) {
            printf('<head><title>Settings - Manage</title></head><script language="javascript">alert("Download image error."); window.location="%s"</script>', $_SERVER['PHP_SELF']);
            exit(1);
        } else {
            $ch = curl_init();
            $fp = fopen($uploadDir . $id . '.' . pathinfo($url, PATHINFO_EXTENSION), 'w');
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_FILE, $fp);
            curl_setopt($ch, CURLOPT_HEADER, 0);

            $response = curl_exec($ch);

            if ($response === false) {
                printf('<head><title>Settings - Manage</title></head><script language="javascript">alert("Download image error"); window.location="%s"</script>', $_SERVER['PHP_SELF']);
                exit(1);
            }

            curl_close($ch);
            fclose($fp);
        }
    } elseif (isset($_SERVER['DELETE'])) {
        $fileName = isset($_SERVER['DELETEIMAGE']) ? $_SERVER['DELETEIMAGE'] : $defaultID;
        $targetPath = $uploadDir . $fileName;
        if (file_exists($targetPath)) {
            unlink($targetPath);
        }
    }

    header('Location: '. $_SERVER['PHP_SELF']);
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Settings - Manage</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    <script>
        function changeFileName() {
            try {
                const fileName = document.querySelector('input[name="image"]').files[0].name;
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
                    <li class="is-active"><a href="/cgi-bin/manage.cgi">Manage</a></li>
                    <li><a href="/cgi-bin/firmware.cgi">Firmware</a></li>
                    <li><a href="/cgi-bin/show_secret.cgi">Show Secret</a></li>
                </ul>
            </div>
        
            <div class id="imageSettings">
                <div class="box">
                    <h2 class="subtitle">Upload Image</h2>
                    <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post" enctype="multipart/form-data">
                        <div class="file has-name">
                            <label class="file-label">
                                <input class="file-input" type="file" name="image" onchange="changeFileName()">
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
                        <div class="field">
                            <label class="label">Image ID</label>
                            <div class="control">
                                <input class="input" type="text" name="image_id" placeholder="Enter Image ID">
                            </div>
                        </div>
                        <br>
                        <button class="button is-primary" type="submit" name="upload">Upload</button>
                    </form>
                </div>

                <div class="box">
                    <h2 class="subtitle">Download Image From URL</h2>
                    <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post" enctype="multipart/form-data">
                        <div class="field has-addons">
                            <div class="control">
                                
                                <input class="input" type="text" name="url" placeholder="Image URL">
                            </div>
                            <br>
                            <div class="field">
                                
                                <div class="control">
                                    <input class="input" type="text" name="image_id" placeholder="Enter Image ID">
                                </div>
                            </div>
                            <br>
                            <div class="control">
                                <button class="button is-primary" type="submit" name="download">Download</button>
                            </div>
                        </div>
                    </form>
                </div>

                <div class="box">
                    <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post" enctype="multipart/form-data">
                        <h2 class="subtitle">Delete Image</h2>
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
                                    echo '<input type="radio" name="deleteImage" value="' . $imageFile . '"> ';
                                    echo "&nbsp;&nbsp;";
                                    echo '<img src="' . $imageUrl . '" alt="' . $imageFile . '" style="max-height: 50px; max-width: 50px;"> ';
                                    echo pathinfo($imageFile, PATHINFO_FILENAME);
                                    echo '</label>';
                                    echo '</div>';
                                }
                                echo '<br>';
                                echo '<button class="button is-danger" type="submit" name="delete">Delete</button>';
                            } else {
                                echo '<p>No images found.</p>';
                            }
                        ?>
                    </form>
                </div>
            </div>
        </div>
    </section>
</body>
</html>
