<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo "belajar php"; ?></title>
</head>

<body>
    <?php

    $StringKu = "Hello!";

    echo $StringKu;

    echo "<h5>Gunakan PHP</h5>";
    ?>

    <?php
    echo "<font face=\"verdana\" size=\"4\">I love using PHP!</font>";
    ?>

    <?php
    echo "<font face='verdana' size='4'>I love using PHP!</h5>";
    ?>

    <?php

    $string_ku = "Hello.. Nama saya: ";

    $bilangan_ku = 4;

    $huruf_ku = "a";

    echo $string_ku;
    echo $bilangan_ku;
    echo $huruf_ku;

    ?>

    <?php
    $string_ku = "Hello. Nama saya:";
    $baris_baru = "<br>";
    echo $string_ku . "Ari" . $baris_baru;
    echo "Hi, Nama saya Ari. Kamu siapa?" . $string_ku . $baris_baru;
    echo "Hi, Nama saya Ari. Kamu siapa?" . $string_ku . "Amalia";
    ?>

    <?php
    $string_ku = "Hello. Nama saya:";
    $baris_baru = "<br>";
    echo $string_ku . "Ari" . $baris_baru;
    echo "Hi, Nama saya Ari. Kamu siapa?" . $string_ku . $baris_baru;
    echo "Hi, Nama saya Ari. Kamu siapa?" . $string_ku . "Amalia";
    ?>

</body>

</html>