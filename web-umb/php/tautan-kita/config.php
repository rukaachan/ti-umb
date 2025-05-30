<?php

define('DB_HOST_MYSQLI', 'localhost');
define('DB_USER_MYSQLI', 'root');
define('DB_PASS_MYSQLI', '');
define('DB_NAME_MYSQLI', 'tautankita_db');

$mysqli_linkkeep = new mysqli(DB_HOST_MYSQLI, DB_USER_MYSQLI, DB_PASS_MYSQLI, DB_NAME_MYSQLI);

// Periksa koneksi
if ($mysqli_linkkeep->connect_error) {
    // Handle error jika koneksi gagal
    error_log("Database connection failed: " . $mysqli_linkkeep->connect_error);
    die("Koneksi ke database gagal. Silakan coba lagi nanti.");
}

if (!$mysqli_linkkeep->set_charset("utf8mb4")) {
    // Handle error jika set_charset gagal
    error_log("Error loading character set utf8mb4: " . $mysqli_linkkeep->error);
}

// Mulai sesi
function set_session_message(string $message, string $type = 'info'): void
{
    $_SESSION['session_message'] = [
        'text' => $message,
        'type' => $type // 'success', 'error', 'warning'
    ];
}

// Fungsi untuk menampilkan pesan sesi
function set_alert_message(string $message, string $type = 'info'): void
{
    $_SESSION['alert_message'] = [
        'text' => $message,
        'type' => $type
    ];
}

// Fungsi untuk menampilkan pesan sesi
function display_alert_message(): ?array
{
    if (isset($_SESSION['alert_message'])) {
        $message_data = $_SESSION['alert_message'];
        unset($_SESSION['alert_message']);
        return $message_data;
    }
    return null;
}

// Fungsi untuk membersihkan input
function sanitize_input($data)
{
    return htmlspecialchars(stripslashes(trim($data)));
}
