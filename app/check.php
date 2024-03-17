<?php

$url = 'http://62.72.46.229:1234/api/'; // Thay đổi URL tới API của bạn

$data = array('image_url' => 'https://toi.sgp1.digitaloceanspaces.com/p/2024/03/65f65cf26a7db1d328081432_large.jpg'); // Dữ liệu bạn muốn gửi, thay 'value' bằng dữ liệu thực tế

$payload = json_encode($data);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

$response = curl_exec($ch);

if (curl_errno($ch)) {
    echo 'Error:' . curl_error($ch);
} else {
    echo $response;
}

curl_close($ch);

?>
