<?php
// config.php

define('DATA_DIR', __DIR__ . '/data/');

if (!is_dir(DATA_DIR)) {
    if (!mkdir(DATA_DIR, 0775, true)) {
        die("GAGAL: Tidak dapat membuat direktori data di '" . DATA_DIR . "'. Pastikan direktori induk ('" . dirname(__DIR__) . "') writable oleh server web.");
    }
}
