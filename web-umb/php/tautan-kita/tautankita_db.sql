-- Buat database jika belum ada
CREATE DATABASE IF NOT EXISTS tautankita_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Gunakan database
USE tautankita_db;

-- Buat tabel bookmarks
CREATE TABLE IF NOT EXISTS bookmarks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(2083) NOT NULL,
    category VARCHAR(100) NULL,
    description TEXT NULL
);
-- Contoh data (opsional)
INSERT INTO bookmarks (title, url, category, description) VALUES
('Dokumentasi PHP Resmi', 'https://www.php.net/manual/en/', 'Pengembangan', 'Referensi utama untuk fungsi dan sintaks PHP.'),
('Bootstrap v5.3', 'https://getbootstrap.com/docs/5.3/getting-started/introduction/', 'Framework CSS', 'Untuk desain antarmuka yang responsif dan modern.'),
('Stack Overflow', 'https://stackoverflow.com/', 'Bantuan Teknis', 'Komunitas tanya jawab untuk programmer.');