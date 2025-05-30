<?php
// delete.php
session_start();
require_once 'config.php';

$id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);

if (!$id) {
    set_session_message("ID tautan tidak valid untuk dihapus.", 'error');
} else {
    try {
        $title_to_delete = "Tautan";
        $stmt_title = $mysqli_linkkeep->prepare("SELECT title FROM bookmarks WHERE id = ?");
        if ($stmt_title) {
            $stmt_title->bind_param("i", $id);
            $stmt_title->execute();
            $result_title = $stmt_title->get_result();
            if ($row_title = $result_title->fetch_assoc()) {
                $title_to_delete = "'" . htmlspecialchars($row_title['title']) . "'";
            }
            $stmt_title->close();
        }

        $stmt_delete = $mysqli_linkkeep->prepare("DELETE FROM bookmarks WHERE id = ?");
        if (!$stmt_delete) throw new Exception("DB prep: " . $mysqli_linkkeep->error);

        $stmt_delete->bind_param("i", $id);
        if ($stmt_delete->execute()) {
            if ($stmt_delete->affected_rows > 0) {
                set_session_message("Tautan " . $title_to_delete . " berhasil dihapus!", 'success');
            } else {
                set_session_message("Tautan tidak ditemukan atau sudah dihapus.", 'warning');
            }
        } else {
            throw new Exception("DB exec: " . $stmt_delete->error);
        }
        $stmt_delete->close();
    } catch (Exception $e) {
        error_log("Delete error: " . $e->getMessage());
        set_session_message("Kesalahan server saat menghapus tautan.", 'error');
    }
}

header("Location: index.php");
exit();
