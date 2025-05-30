<?php
//
require_once 'config.php';
session_start();

$title = $url = $category = $description = '';
$form_errors = [];
$db_error_alert = null;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $title = sanitize_input($_POST['title']);
    $url = sanitize_input($_POST['url']);
    $category = sanitize_input($_POST['category']) ?: null;
    $description = sanitize_input($_POST['description']) ?: null;

    if (empty($title)) {
        $form_errors['title'] = "Judul tautan wajib diisi.";
    } elseif (mb_strlen($title) > 255) {
        $form_errors['title'] = "Judul maksimal 255 karakter.";
    }

    if (empty($url)) {
        $form_errors['url'] = "URL tautan wajib diisi.";
    } elseif (!filter_var($url, FILTER_VALIDATE_URL)) {
        $form_errors['url'] = "Format URL tidak valid (mis: https://contoh.com).";
    } elseif (mb_strlen($url) > 2083) {
        $form_errors['url'] = "URL terlalu panjang (maksimal 2083 karakter).";
    }


    if ($category && mb_strlen($category) > 100) {
        $form_errors['category'] = "Kategori maksimal 100 karakter.";
    }



    if (empty($form_errors)) {
        try {
            $sql = "INSERT INTO bookmarks (title, url, category, description) VALUES (?, ?, ?, ?)";
            $stmt = $mysqli_linkkeep->prepare($sql);

            if ($stmt === false) {
                throw new Exception("Gagal mempersiapkan statement: " . $mysqli_linkkeep->error);
            }

            $stmt->bind_param("ssss", $title, $url, $category, $description);

            if ($stmt->execute()) {
                set_alert_message("🎉 Tautan '" . htmlspecialchars($title) . "' berhasil ditambahkan!", 'success');
                header("Location: index.php");
                exit();
            } else {

                throw new Exception("Gagal mengeksekusi statement: " . $stmt->error);
            }
        } catch (Exception $e) {
            error_log("Create link database error: " . $e->getMessage());
            $db_error_alert = "Oops! Terjadi kesalahan internal saat mencoba menyimpan tautan. Silakan coba lagi.";
        }
    }
}
?>
<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tambah Tautan Baru 💡 - TautanKita</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link href="style.css" rel="stylesheet">
</head>

<body class="form-page">
    <nav class="navbar navbar-expand-lg navbar-custom sticky-top">
        <div class="container">
            <a class="navbar-brand" href="index.php"><i class="fas fa-rocket me-2"></i>TautanKita</a>
        </div>
    </nav>

    <main class="container container-form">
        <section class="card card-form">
            <header class="card-header card-header-form create-header text-center">
                <h2><i class="fas fa-magic me-2"></i>Tambah Tautan Baru</h2>
            </header>
            <div class="card-body p-4 p-md-5">
                <?php /* Error database akan ditampilkan oleh SweetAlert di <script> bawah */ ?>

                <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post" novalidate>
                    <div class="mb-4">
                        <label for="title" class="form-label">Judul Tautan <span style="color: var(--vibrant-pink);">*</span></label>
                        <input type="text" name="title" id="title" class="form-control <?php echo isset($form_errors['title']) ? 'is-invalid' : ''; ?>" value="<?php echo htmlspecialchars($title); ?>" required maxlength="255" placeholder="Contoh: Belajar Desain Grafis untuk Pemula">
                        <?php if (isset($form_errors['title'])): ?>
                            <div class="invalid-feedback"><?php echo htmlspecialchars($form_errors['title']); ?></div>
                        <?php endif; ?>
                    </div>

                    <div class="mb-4">
                        <label for="url" class="form-label">Alamat URL <span style="color: var(--vibrant-pink);">*</span></label>
                        <input type="url" name="url" id="url" class="form-control <?php echo isset($form_errors['url']) ? 'is-invalid' : ''; ?>" value="<?php echo htmlspecialchars($url); ?>" required placeholder="https://www.websitekeren.com/tutorial/desain">
                        <?php if (isset($form_errors['url'])): ?>
                            <div class="invalid-feedback"><?php echo htmlspecialchars($form_errors['url']); ?></div>
                        <?php endif; ?>
                    </div>

                    <div class="mb-4">
                        <label for="category" class="form-label">Kategori (Opsional)</label>
                        <input type="text" name="category" id="category" class="form-control <?php echo isset($form_errors['category']) ? 'is-invalid' : ''; ?>" value="<?php echo htmlspecialchars($category); ?>" maxlength="100" placeholder="Mis: Desain, Edukasi, Inspirasi">
                        <?php if (isset($form_errors['category'])): ?>
                            <div class="invalid-feedback"><?php echo htmlspecialchars($form_errors['category']); ?></div>
                        <?php endif; ?>
                    </div>

                    <div class="mb-4">
                        <label for="description" class="form-label">Deskripsi Singkat (Opsional)</label>
                        <textarea name="description" id="description" class="form-control" rows="4" placeholder="Deskripsi singkat mengenai tautan ini agar mudah diingat..."><?php echo htmlspecialchars($description); ?></textarea>
                    </div>

                    <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-4">
                        <a href="index.php" class="btn btn-secondary btn-cancel-form"><i class="fas fa-arrow-left me-2"></i>Kembali</a>
                        <button type="submit" class="btn btn-submit-form create-btn"><i class="fas fa-paper-plane me-2"></i>Simpan Tautan</button>
                    </div>
                </form>
            </div>
        </section>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const dbError = <?php echo json_encode($db_error_alert); ?>;
            if (dbError) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops! Gagal Menyimpan',
                    text: dbError,
                    confirmButtonText: 'Mengerti'
                });
            }
        });
    </script>
</body>

</html>