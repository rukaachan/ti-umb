<?php

$message = '';
$fileContent = '';
$filenameFromPost = '';
$messageType = 'info';


if (session_status() == PHP_SESSION_NONE) {
    session_start();
}


if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $filenameFromPost = isset($_POST['filename']) ? trim($_POST['filename']) : '';
    $content = isset($_POST['content']) ? $_POST['content'] : '';


    $_SESSION['last_filename'] = $filenameFromPost;


    if (empty($filenameFromPost)) {
        $message = "Nama file tidak boleh kosong.";
        $messageType = 'error';
    } elseif (preg_match('/[\/\?\*:"<>|]/', $filenameFromPost) || $filenameFromPost === "." || $filenameFromPost === "..") {
        $message = "Nama file mengandung karakter tidak valid atau tidak diizinkan.";
        $messageType = 'error';
        $_SESSION['last_filename'] = '';
    } else {
        $filePath = DATA_DIR . $filenameFromPost;


        if (isset($_POST['create_write'])) {
            if (file_put_contents($filePath, $content) !== false) {
                $message = "File '$filenameFromPost' berhasil dibuat/diperbarui di folder '" . basename(DATA_DIR) . "'.";
                $messageType = 'success';
            } else {
                $message = "Gagal menulis ke file '$filenameFromPost'. Periksa izin direktori data.";
                $messageType = 'error';
            }
        } elseif (isset($_POST['read'])) {
            if (file_exists($filePath)) {
                $fileContent = file_get_contents($filePath);
                if ($fileContent === false) {
                    $message = "Gagal membaca file '$filenameFromPost'.";
                    $messageType = 'error';
                    $fileContent = '';
                } else {
                    $message = "Berhasil membaca isi file '$filenameFromPost':";
                    $messageType = 'success';
                }
            } else {
                $message = "File '$filenameFromPost' tidak ditemukan di folder '" . basename(DATA_DIR) . "'.";
                $messageType = 'error';
            }
        } elseif (isset($_POST['append'])) {
            $canAppend = file_exists($filePath);
            if (!$canAppend && !empty($content)) {
                $canAppend = true;
            }

            if ($canAppend) {
                if (file_put_contents($filePath, $content . PHP_EOL, FILE_APPEND | LOCK_EX) !== false) {
                    $message = "Konten berhasil ditambahkan ke file '$filenameFromPost'.";
                    $messageType = 'success';
                } else {
                    $message = "Gagal menambahkan konten ke file '$filenameFromPost'.";
                    $messageType = 'error';
                }
            } else {
                $message = "File '$filenameFromPost' tidak ditemukan dan tidak ada konten untuk membuat file baru saat append.";
                $messageType = 'error';
            }
        } elseif (isset($_POST['delete'])) {
            if (file_exists($filePath)) {
                if (unlink($filePath)) {
                    $message = "File '$filenameFromPost' berhasil dihapus dari folder '" . basename(DATA_DIR) . "'.";
                    $messageType = 'success';
                } else {
                    $message = "Gagal menghapus file '$filenameFromPost'.";
                    $messageType = 'error';
                }
            } else {
                $message = "File '$filenameFromPost' tidak ditemukan untuk dihapus.";
                $messageType = 'error';
            }
        }
    }
}


$filenameToDisplay = isset($_SESSION['last_filename']) ? $_SESSION['last_filename'] : '';


if ($_SERVER["REQUEST_METHOD"] != "POST" && isset($_SESSION['last_filename'])) {


    $filenameFromPost = $_SESSION['last_filename'];
}
