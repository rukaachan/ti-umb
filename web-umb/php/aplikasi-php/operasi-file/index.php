<?php
// index.php

// Sertakan file konfigurasi
require_once __DIR__ . '/config.php';

// Sertakan file logika operasi file
require_once __DIR__ . '/file_operations.php'; // Sesi sudah dimulai di dalam file ini jika belum

?>
<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📝 Manajer File PHP Modern</title>
    <link rel="stylesheet" href="style.css?v=<?php echo time(); ?>">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit&display=swap" rel="stylesheet">
    <style>
        .button-group button .emoji {
            margin-right: 6px;
            font-size: 1.1em;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1><span class="emoji">🗂️</span> Manajer File Sederhana</h1>

        <div class="storage-info">
            <strong><span class="emoji">ℹ️</span> Info:</strong> Semua file disimpan dan dioperasikan di dalam folder <code><?php echo htmlspecialchars(basename(DATA_DIR)); ?>/</code><br>
            (Lokasi absolut: <code><?php echo htmlspecialchars(DATA_DIR); ?></code>)
        </div>

        <?php if (!empty($message)): ?>
            <div class="message-area <?php echo htmlspecialchars($messageType); ?>" style="margin-bottom: 1em;">
                <?php
                // Tambahkan emoji berdasarkan tipe pesan
                $emojiMessage = '';
                if ($messageType === 'success') {
                    $emojiMessage = '✅ ';
                } elseif ($messageType === 'error') {
                    $emojiMessage = '❌ ';
                } elseif ($messageType === 'info') {
                    $emojiMessage = '💡 ';
                }
                echo $emojiMessage . htmlspecialchars($message);
                ?>
            </div>
        <?php endif; ?>

        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="POST">
            <div>
                <label for="filename"><span class="emoji">📄</span> Nama File:</label>
                <input type="text" id="filename" name="filename" value="<?php echo htmlspecialchars($filenameToDisplay); ?>" placeholder="contoh: catatan_penting.txt" required>
            </div>

            <div>
                <label for="content"><span class="emoji">✍️</span> Konten File:</label>
                <textarea id="content" name="content" placeholder="Tuliskan atau tempelkan konten di sini..."></textarea>
            </div>

            <div class="button-group">
                <button type="submit" name="create_write" class="btn-create"><span class="emoji">💾</span> Buat / Timpa</button>
                <button type="submit" name="read" class="btn-read"><span class="emoji">📖</span> Baca File</button>
                <button type="submit" name="append" class="btn-append"><span class="emoji">➕</span> Tambah ke File</button>
                <button type="submit" name="delete" class="btn-delete" onclick="return confirm('Apakah Anda yakin ingin menghapus file ini? Operasi ini tidak dapat diurungkan.');"><span class="emoji">🗑️</span> Hapus File</button>
            </div>
        </form>

        <?php
        $shouldDisplayContent = ($messageType === 'success' && isset($_POST['read']));
        if ($shouldDisplayContent && !empty($filenameFromPost) && file_exists(DATA_DIR . $filenameFromPost)):
        ?>
            <div class="file-content-wrapper">
                <h3><span class="emoji">🧐</span> Isi File '<?php echo htmlspecialchars($filenameFromPost); ?>':</h3>
                <pre><?php echo htmlspecialchars($fileContent); ?></pre>
            </div>
        <?php endif; ?>

    </div>
</body>

</html>