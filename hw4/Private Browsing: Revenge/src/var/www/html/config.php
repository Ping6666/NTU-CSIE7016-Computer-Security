<?php
require_once __DIR__ . '/../vendor/autoload.php';

$redis = new Predis\Client('tcp://redis:6379');
$handler = new Predis\Session\Handler($redis);

$handler->register();
session_start();

if (!isset($_SESSION['history'])) {
    $_SESSION['history'] = [];
}
