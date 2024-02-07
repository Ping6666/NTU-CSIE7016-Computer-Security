<?php
require_once __DIR__ . '/config.php';

function request($url, $method = 'GET', $data = null)
{
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

    if ($data !== null) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    }

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);

    $response = curl_exec($ch);
    $error = curl_error($ch);

    curl_close($ch);

    if ($error) {
        return $error;
    }

    return $response;
}

if (!isset($_GET['action'])) {
    die();
}

$action = $_GET['action'];

if ($action === 'view' && isset($_GET['url'])) {
    header("Content-Security-Policy: script-src 'none'");
    header("X-Content-Type-Options: nosniff");

    $url = $_GET['url'];
    $_SESSION['history'][] = $url;
    $hostname = parse_url($url, PHP_URL_HOST);

    if (filter_var(gethostbyname($hostname), FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE) === false) {
        die('Error: Invalid IP or intranet ip in provided URL.<br>Reason:<code>(filter_var(gethostbyname($hostname), FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE) === false</code>');
    }

    echo request($url);
} else if ($action === 'get_history') {
    header('Content-Type: application/json');
    echo json_encode($_SESSION['history']);
} else if ($action === 'clear_history') {
    $_SESSION['history'] = [];
    echo '{"status": "ok"}';
}
