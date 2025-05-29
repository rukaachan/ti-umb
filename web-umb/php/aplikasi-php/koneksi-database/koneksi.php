<?php
$servername = "localhost";
$username = "root";
$password = "";
$database = "tb1_web_programming";


$conn = new mysqli($servername, $username, $password, $database);


if ($conn->connect_error) {
    die("Koneksi gagal: " . $conn->connect_error);
}
