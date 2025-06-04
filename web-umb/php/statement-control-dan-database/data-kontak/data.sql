CREATE DATABASE IF NOT EXISTS datakontak;
USE datakontak;


CREATE TABLE tbl_kontak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    alamat VARCHAR(255) NOT NULL,
    telpon VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    tgl_lahir DATE NOT NULL
);

-- Insert dummy data
INSERT INTO tbl_kontak (nama, alamat, telpon, email, tgl_lahir) VALUES
('John Doe', '123 Main St, Jakarta', '08123456789', 'john@example.com', '1990-05-15'),
('Jane Smith', '456 Elm St, Bandung', '08765432109', 'jane@example.com', '1985-12-01'),
('Bob Johnson', '789 Oak St, Surabaya', '08987654321', 'bob@example.com', '1995-08-22'),
('Alice Brown', '101 Pine St, Yogyakarta', '08111222333', 'alice@example.com', '1988-03-30');
