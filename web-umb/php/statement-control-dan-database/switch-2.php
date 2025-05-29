<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Switch</title>
</head>

<body>
    <?php

    $nilai_ujian = 90;
    print "Nilai Anda " . $nilai_ujian;
    print "<br>";

    switch (true) {
        case ($nilai_ujian < 50):
            print "Maaf, tidak lulus";
            break;
        case ($nilai_ujian >= 50):
            print "Anda lulus";
            break;
        default:
            break;
    }

    ?>
</body>

</html>