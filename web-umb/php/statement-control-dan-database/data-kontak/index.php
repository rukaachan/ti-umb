<!DOCTYPE html>
<html>

<head>
    <title>Database Data Kontak</title>
</head>

<body>

    <?php
    $host = "localhost";
    $user = "root";
    $passwd = "";
    $db = "datakontak";

    $sql = "SELECT * FROM tbl_kontak";
    $conn = mysqli_connect($host, $user, $passwd, $db);
    $qry = mysqli_query($conn, $sql);
    ?>

    <table border="1">
        <tr>
            <td bgcolor="#f32142">Nama</td>
            <td bgcolor="#f32142">Alamat</td>
            <td bgcolor="#f32142">Telepon</td>
            <td bgcolor="#f32142">Email</td>
            <td bgcolor="#f32142">Tanggal Lahir</td>
        </tr>

        <?php while ($row = mysqli_fetch_array($qry)) { ?>
            <tr>
                <td bgcolor="#f7efde"><?php echo $row['nama']; ?></td>
                <td bgcolor="#f7efde"><?php echo $row['alamat']; ?></td>
                <td bgcolor="#f7efde"><?php echo $row['telpon']; ?></td>
                <td bgcolor="#f7efde"><?php echo $row['email']; ?></td>
                <td bgcolor="#f7efde"><?php echo $row['tgl_lahir']; ?></td>
            </tr>
        <?php } ?>

    </table>

</body>

</html>