<?php

// Penggunaan tipe data object
class himp
{
    var $divisi = "Contoh PHP yang ketiga";
    function ubah($str)
    {
        $this->divisi = $str;
    }
}
$hme = new himp;
print $hme->divisi;
print "<br>";
$hme->ubah("Belajar PHP itu menyenangkan");
print $hme->divisi;
