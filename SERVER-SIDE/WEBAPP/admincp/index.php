<?php
session_start();
error_reporting(0);
include "../include/database.config.php";
include "../include/get.account.php";

$UID = $_SESSION["UID"];

if (isset($_SESSION['UID'])) {
    // Display navigation bar for logged-in users
    echo ' ';
} else {
    // Display navigation bar for guests
    echo '<script>window.location.href = "../pages/login";</script>';
}

define('AREA', "ADMIN");
include dirname(__FILE__).'/core/init.php';

cn_sendheaders();
cn_load_skin();
cn_register_form();

if (cn_login()) {
    hook('index/invoke_module', array($_module) );
} else {
    cn_login_form();
}