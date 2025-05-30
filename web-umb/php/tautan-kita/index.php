<?php

require_once 'config.php';
session_start();

$alert_message_data = display_alert_message();
$search_term = isset($_GET['search']) ? sanitize_input($_GET['search']) : '';
$bookmarks = [];
$fetch_error = null;

try {
    $sql = "SELECT id, title, url, category, description FROM bookmarks";
    $params = [];
    $types = "";

    if (!empty($search_term)) {
        $sql .= " WHERE title LIKE ? OR category LIKE ? OR description LIKE ?";
        $search_like = "%" . $search_term . "%";
        $params = [$search_like, $search_like, $search_like];
        $types = "sss";
    }
    $sql .= " ORDER BY title ASC";

    $stmt = $mysqli_linkkeep->prepare($sql);
    if ($stmt === false) {
        throw new Exception("Database query preparation failed: " . $mysqli_linkkeep->error);
    }

    if (!empty($params)) {
        $stmt->bind_param($types, ...$params);
    }

    $stmt->execute();
    $result = $stmt->get_result();
    $bookmarks = $result->fetch_all(MYSQLI_ASSOC);
    $stmt->close();
} catch (Exception $e) {
    error_log("Fetch bookmarks error: " . $e->getMessage());

    $fetch_error = "Oops! Terjadi kesalahan saat memuat data tautan. Silakan coba lagi nanti.";
}
?>
<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TautanKita 🚀 - Simpan Tautanmu!</title>

    <!-- CDN Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- CDN Font Awesome CSS -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <!-- CDN SweetAlert2 CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
    <!-- CDN Google Font Nunito -->
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <!-- Favicon -->
    <link rel="icon" href="favicon.ico" type="image/x-icon">

    <link href="style.css" rel="stylesheet">
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-custom sticky-top">
        <div class="container">
            <a class="navbar-brand" href="index.php"><i class="fas fa-rocket me-2"></i>TautanKita</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="btn btn-add" href="create.php"><i class="fas fa-plus-circle me-1"></i> Tambah Cepat</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container container-main">
        <header class="page-header">
            <h1>Kelola Tautanmu Dengan Gaya! ✨</h1>
            <p class="lead">Tempat semua link pentingmu berkumpul dengan aman dan rapi.</p>
        </header>

        <div class="row justify-content-center">
            <div class="col-lg-6 col-md-6">
                <form action="index.php" method="GET" class="search-form mb-5">
                    <div class="input-group">
                        <input type="text" name="search" class="form-control" placeholder="Ketik untuk mencari tautan..." value="<?php echo htmlspecialchars($search_term); ?>">
                        <button class="btn btn-outline-secondary" type="submit" title="Cari"><i class="fas fa-search"></i></button>
                        <?php if (!empty($search_term)): ?>
                            <a href="index.php" class="btn btn-outline-danger" title="Hapus Pencarian"><i class="fas fa-times"></i></a>
                        <?php endif; ?>
                    </div>
                </form>
            </div>
        </div>

        <?php if (empty($bookmarks) && empty($fetch_error)): ?>
            <div class="empty-state">
                <i class="fas fa-ghost fa-3x text-secondary mb-3" style="opacity:0.6;"></i>
                <h4>Koleksimu Masih Kosong 📂</h4>
                <?php if (!empty($search_term)): ?>
                    <p class="text-muted">Tidak ada hasil untuk "<?php echo htmlspecialchars($search_term); ?>". Coba kata kunci lain!</p>
                <?php else: ?>
                    <p class="text-muted">Ayo, simpan tautan pertamamu di sini!</p>
                    <a href="create.php" class="btn btn-add mt-3"><i class="fas fa-magic me-1"></i> Mulai Sekarang!</a>
                <?php endif; ?>
            </div>
        <?php elseif (!empty($bookmarks)): ?>
            <main class="row">
                <?php foreach ($bookmarks as $bookmark): ?>
                    <div class="col-md-6 col-lg-4 d-flex align-items-stretch">
                        <article class="card card-bookmark w-100">
                            <div class="card-body d-flex flex-column">
                                <h5 class="bookmark-title"><?php echo htmlspecialchars($bookmark['title']); ?></h5>
                                <p class="bookmark-url mb-0">
                                    <a href="<?php echo htmlspecialchars($bookmark['url']); ?>" target="_blank" rel="noopener noreferrer" title="<?php echo htmlspecialchars($bookmark['url']); ?>">
                                        <i class="fas fa-external-link-square-alt fa-xs me-1"></i><?php echo htmlspecialchars(mb_strimwidth($bookmark['url'], 0, 35, "...")); ?>
                                    </a>
                                </p>
                                <?php if (!empty($bookmark['category'])): ?>
                                    <span class="badge bookmark-category"><i class="fas fa-hashtag fa-xs me-1"></i><?php echo htmlspecialchars($bookmark['category']); ?></span>
                                <?php endif; ?>
                                <?php if (!empty($bookmark['description'])): ?>
                                    <p class="bookmark-description flex-grow-1"><?php echo nl2br(htmlspecialchars($bookmark['description'])); ?></p>
                                <?php else: ?>
                                    <div class="flex-grow-1"></div>
                                <?php endif; ?>
                                <div class="mt-auto pt-2 d-flex justify-content-end btn-action-group">
                                    <a href="edit.php?id=<?php echo $bookmark['id']; ?>" class="btn btn-sm btn-edit btn-action"><i class="fas fa-pen-to-square fa-xs me-1"></i>Ubah</a>
                                    <a href="delete.php?id=<?php echo $bookmark['id']; ?>" class="btn btn-sm btn-delete btn-action btn-delete-link" data-id="<?php echo $bookmark['id']; ?>" data-title="<?php echo htmlspecialchars($bookmark['title']); ?>"><i class="fas fa-trash-can fa-xs me-1"></i>Hapus</a>
                                </div>
                            </div>
                        </article>
                    </div>
                <?php endforeach; ?>
            </main>
        <?php endif; ?>
    </div>

    <!-- CDN Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <!-- CDN SweetAlert2 JS -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const alertData = <?php echo json_encode($alert_message_data); ?>;
            if (alertData) {
                Swal.fire({
                    icon: alertData.type,
                    title: (alertData.type === "success" ? "Berhasil!" : (alertData.type === "error" ? "Oops..." : (alertData.type === "warning" ? "Perhatian!" : "Info"))),
                    text: alertData.text,
                    confirmButtonText: 'OK',
                    timer: (alertData.type === "success" ? 3000 : 5000),
                    timerProgressBar: (alertData.type === "success" ? true : false)
                });
            }

            const fetchError = <?php echo json_encode($fetch_error); ?>;
            if (fetchError) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: fetchError,
                    confirmButtonText: 'OK'
                });
            }

            document.querySelectorAll('.btn-delete-link').forEach(button => {
                button.addEventListener('click', function(event) {
                    event.preventDefault();
                    const linkId = this.dataset.id;
                    const linkTitle = this.dataset.title;

                    Swal.fire({
                        title: 'Yakin ingin menghapus?',
                        html: `Tautan "<strong>${linkTitle}</strong>" akan dihapus permanen! 💥`,
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonText: 'Ya, Hapus Saja!',
                        cancelButtonText: 'Tidak, Batalkan',
                        reverseButtons: true
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = `delete.php?id=${linkId}`;
                        }
                    });
                });
            });
        });
    </script>
</body>

</html>