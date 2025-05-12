<?php
include 'koneksi.php';

if (!isset($conn) || $conn->connect_error) {
    die("Koneksi ke database gagal. Pastikan 'koneksi.php' benar dan server MySQL berjalan. Error: " . (isset($conn) ? $conn->connect_error : 'Variabel koneksi tidak ada.'));
}

$nama_tabel = "mahasiswa";
$kolom_id = "id";
$kolom_nama = "nama";
$kolom_email = "email";
$kolom_jurusan = "jurusan";

$sql = "SELECT $kolom_id, $kolom_nama, $kolom_email, $kolom_jurusan FROM $nama_tabel ORDER BY $kolom_id ASC";
$result = $conn->query($sql);

if ($result === false) {
    die("Error saat menjalankan query: " . $conn->error);
}
?>

<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <title>Data Mahasiswa Modern</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7f6;
            /* Softer background */
            color: #333;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 950px;
            margin: 30px auto;
            background-color: #ffffff;
            padding: 25px 30px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #2c3e50;
            /* Darker blue-gray */
            text-align: center;
            margin-bottom: 25px;
            border-bottom: 2px solid #3498db;
            /* Accent color underline */
            padding-bottom: 10px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        th,
        td {
            border: 1px solid #e0e0e0;
            /* Lighter border */
            padding: 12px 15px;
            text-align: left;
        }

        th {
            background-color: #3498db;
            /* Primary accent color */
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Zebra striping for better readability */
        tbody tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        tbody tr:hover {
            background-color: #e9ecef;
            /* Hover effect */
            cursor: default;
            /* Or 'pointer' if rows were clickable */
        }

        .pesan,
        .error {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            font-size: 0.95em;
        }

        .pesan {
            background-color: #d1ecf1;
            border-left: 6px solid #007bff;
            /* Bootstrap info blue */
            color: #0c5460;
        }

        .error {
            background-color: #f8d7da;
            border-left: 6px solid #dc3545;
            /* Bootstrap danger red */
            color: #721c24;
        }

        /* A general button style (not used in this specific PHP, but good for consistency if you add buttons) */
        .btn {
            display: inline-block;
            padding: 10px 20px;
            margin-top: 20px;
            font-size: 1em;
            font-weight: bold;
            text-align: center;
            text-decoration: none;
            color: white;
            background-color: #5cb85c;
            /* Success green */
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .btn:hover {
            background-color: #4cae4c;
        }

        .btn-secondary {
            background-color: #6c757d;
            /* Gray */
        }

        .btn-secondary:hover {
            background-color: #5a6268;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Data Mahasiswa</h1>

        <?php
        if ($result->num_rows > 0) {
            echo "<table>";
            echo "<thead>";
            echo "<tr>";
            echo "<th>ID</th>";
            echo "<th>Nama</th>";
            echo "<th>Email</th>";
            echo "<th>Jurusan</th>";
            echo "</tr>";
            echo "</thead>";
            echo "<tbody>";

            while ($row = $result->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . htmlspecialchars($row[$kolom_id]) . "</td>";
                echo "<td>" . htmlspecialchars($row[$kolom_nama]) . "</td>";
                echo "<td>" . htmlspecialchars($row[$kolom_email]) . "</td>";
                echo "<td>" . htmlspecialchars($row[$kolom_jurusan]) . "</td>";
                echo "</tr>";
            }
            echo "</tbody>";
            echo "</table>";
        } else {
            echo "<div class='pesan'>Tidak ada data mahasiswa yang ditemukan di tabel '" . htmlspecialchars($nama_tabel) . "'.</div>";
        }

        $conn->close();
        ?>

    </div>
</body>

</html>