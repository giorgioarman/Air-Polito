﻿<?php /* Template Name: realMonitoring */

get_header();

include_once get_template_directory() . '/aqi/Database.php';
include_once get_template_directory() . '/aqi/AQI.php';

$database = new Database();
$db = $database->getConnection();
$aqi = new Aqi($db);

$stmt = $aqi->read();
$num = $stmt->rowCount();
if($num>0){
    $rowsArr=array();
    $rowsArr["records"]=array();
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)){
        extract($row);
        $rowItem=array(
            "aqiId" => $aqiId,
            "aqiValue" => $aqiValue,
            "aqiStatus" => $aqiStatus,
            "aqiDateInsert" => $aqiDateInsert,
            "aqiDateCollect" => $aqiDateCollect,
            "aqiSensorData" => $aqiSensorData
        );
        array_push($rowsArr["records"], $rowItem);
    }
    $response = json_encode($rowsArr);
}
else{
    echo 'there is no data';
}

$responseJson = json_decode($response, true);
//APQI values
$lastAPQI = $responseJson['records'][0];
$aqiValue = $lastAPQI['aqiValue'];
$aqiStatus = $lastAPQI['aqiStatus'];
$aqiDateCollect = $lastAPQI['aqiDateCollect'];
$aqiSensorDataJson = json_decode(json_decode($lastAPQI['aqiSensorData'], true), true);

// Sensor's values
$pm10 = $aqiSensorDataJson['pm10'];
$pm25 = $aqiSensorDataJson['pm25'];
$no2 = $aqiSensorDataJson['no2'];
$o3 = $aqiSensorDataJson['o3'];
$temp = $aqiSensorDataJson['temp'];
$hum = $aqiSensorDataJson['hum'];

// select Avatar Status
if ($aqiStatus == "Ottima") {
   $avatarUrl = get_template_directory_uri() . '/aqi/resources/Ottima.gif';
   $avatarComment = 'Continuiamo ad impegnarci così.';
} elseif ($aqiStatus == "Buona") {
    $avatarUrl = get_template_directory_uri() . '/aqi/resources/Buona.gif';
    $avatarComment = 'Bene! Ma possiamo fare di meglio.';
} elseif ($aqiStatus == "Accettabile") {
    $avatarUrl = get_template_directory_uri() . '/aqi/resources/Accettabile.gif';
    $avatarComment = 'Possiamo e dobbiamo migliorare!';
} elseif ($aqiStatus == "Cattiva") {
    $avatarUrl = get_template_directory_uri() . '/aqi/resources/Cattiva.gif';
    $avatarComment = 'La situazione non è per nulla buona.';
} else {
    $avatarUrl = get_template_directory_uri() . '/aqi/resources/Pessima.gif';
    $avatarComment = 'Stiamo rischiando! Non va affatto bene!';
}
$bgUrl = get_template_directory_uri() . '/aqi/resources/hero-bg.png'
?>

<meta http-equiv="refresh" content="30">
<link href="<?php echo get_template_directory_uri() . '/aqi/CSS/styleAvatar.css' ?>" rel="stylesheet">
<link href="<?php echo get_template_directory_uri() . '/aqi/CSS/bootstrap.min.css' ?>" rel="stylesheet">


div class="container page-box" style="background: url('<?php echo $bgUrl ?>') center bottom no-repeat;">
    <div class="page_content row">
      <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
        <section id="hero" >
          <div class="hero-container">
            <h2 class="avatar-name">Evan</h2>
            <img src="<?php echo $avatarUrl; ?>" alt="Hero Imgs" width="350">
            <a class="btn-get-started <?php echo $aqiStatus . '-color' ?>">In questo momento la qualità dell aria
              è <?php echo $aqiStatus?></a>
            <div class="comment-hero">
              <h2 class=""> <?php echo $avatarComment?></h2>
            </div>
          </div>
        </section>
      </div>

      <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12">
        <div id="info" class="">
            <h2 class="text-center custumTagH">Dettagli</h2>
            <ul class="list-group">
              <li class=" text-body list-group-item list-group-item-info">Stato IPQA: <?php echo $aqiStatus; ?></li>
              <li class="text-body list-group-item list-group-item-info">Valore IPQA: <?php echo $aqiValue; ?></li>
              <li class="text-body list-group-item list-group-item-info">Temperatura: <?php echo $temp; ?> &#8451;</li>
              <li class="text-body list-group-item list-group-item-info">Umidità: <?php echo $hum; ?>%</li>
              <li class="text-body list-group-item list-group-item-info">Data ultimo rilevamento: <?php echo $aqiDateCollect; ?></li>
            </ul>

            <h3 class="text-center custumTagH">Valori rilevati dai sensori</h3>
            <ul class="list-group">
              <li class=" text-body list-group-item list-group-item-info">PM10: <?php echo $pm10; ?></li>
              <li class="text-body list-group-item list-group-item-info">PM2.5: <?php echo $pm25; ?></li>
              <li class="text-body list-group-item list-group-item-info">NO2: <?php echo $no2; ?></li>
              <li class="text-body list-group-item list-group-item-info">O3: <?php echo $o3; ?></li>
            </ul>
        </div>
      </div>
      <div class="clear"></div>
    </div>
  </div>