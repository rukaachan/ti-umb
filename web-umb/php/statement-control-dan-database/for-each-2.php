<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>For eaach</title>
</head>

<body>

    <?php
    
    $UsiaKaryawan["Lisa"] = "28";
    $UsiaKaryawan["Jack"] = "16";
    $UsiaKaryawan["Ryan"] = "35";
    $UsiaKaryawan["Rachel"] = "46";
    $UsiaKaryawan["Grace"] = "34";

    foreach ($UsiaKaryawan as $Nama => $umur) {
        echo "Nama Karyawan: $Nama, Usia: $umur th<br>";
    }

    ?>

</body>

</html>