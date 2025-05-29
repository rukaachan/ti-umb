<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>For</title>
</head>

<body>
    <?php

    $harga_sikat = 1500;

    echo "<table border='1' align='center'>";
    echo "<tr><td><b>Jumlah Sikat</b></td>";
    echo "<td><b>Harga</b></td></tr>";

    for ($jumlah_sikat = 10; $jumlah_sikat <= 100; $jumlah_sikat += 10) {
        echo "<tr><td>";
        echo $jumlah_sikat;
        echo "</td><td>";
        echo "Rp. " . ($harga_sikat * $jumlah_sikat);
        echo "</td></tr>";
    }

    echo "</table>";

    ?>
</body>

</html>