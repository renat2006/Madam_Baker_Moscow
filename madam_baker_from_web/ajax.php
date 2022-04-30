<?php

$tg_bot_token = "5228413552:AAG0jmeiN5nsIMOjzNYgiUDVh4QctSkQWX0";

$chat_id = "-1001779922350";

$text = '';
$text .= "Новая заявка!" . "\n";
foreach ($_POST as $key => $val) {
    $text .= $key . ": " . $val . "\n";
}


$text .= "\n" . "Дата: " . date('d.m.y H:i:s');

$param = [
    "chat_id" => $chat_id,
    "text" => $text
];

$url = "https://api.telegram.org/bot" . $tg_bot_token . "/sendMessage?" . http_build_query($param);

var_dump($text);

file_get_contents($url);



die('1');
