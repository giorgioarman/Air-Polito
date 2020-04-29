<?php /* Template Name: realMonitoring */

get_header();

include_once get_template_directory() . '/aqi/Database.php';
include_once get_template_directory() . '/aqi/AQI.php';

$database = new Database();
$db = $database->getConnection();
$aqi = new Aqi($db);



// ====================Historic Data ==============
$chart_date = [];
for($i=0;$i<7;$i++)
{
    $curretDate = Date("Y-m-d",time()-((7-$i)*24*60*60));
    $label = date('l', strtotime($curretDate));
    switch ($label) {
        case "Monday":
            $label="lunedì";
            break;
        case "Tuesday":
            $label="martedì";
            break;
        case "Wednesday":
            $label="mercoledì";
            break;
        case "Thursday":
            $label="giovedì";
            break;
        case "Friday":
            $label="venerdì";
            break;
        case "Saturday":
            $label="sabato";
            break;
        case "Sunday":
            $label="domenica";
            break;
    }
    $chart_date[$i] = array("y" => 0, "label" => $label, "color" => "white", "indexLabel"=> "","indexLabelOrientation" => "vertical","indexLabelPlacement"=>"inside");
}

$stmtAVG = $aqi->readAVG();
$numAVG = $stmtAVG->rowCount();
if($numAVG>0){
    $rowsArr=array();
    $rowsArr["records"]=array();

    while ($row = $stmtAVG->fetch(PDO::FETCH_ASSOC)){
        extract($row);
        $rowItem=array(
            "aqiId" => $aqiId,
            "aqiValue" => $aqiValue,
            "aqiStatus" => $aqiStatus,
            "aqiDateInsert" => $aqiDateInsert,
            "aqiDateCollect" => $aqiDateCollect,
            "aqiSensorData" => $aqiSensorData,
            "average" => $average

        );
        $avgStatus = "";
        for($j=0;$j<7;$j++)
        {
            $curretDate = Date("Y-m-d",time()-((7-$j)*24*60*60));
            $recordDate = date('Y-m-d', strtotime($aqiDateCollect));
            if($curretDate == $recordDate)
            {
                if(round($average)>0 && round($average) <= 50)
                {
                    $avgStatus = "Ottima";
                    $colorBar = "#4BC52A";
                    $avg = 5;
                }
                elseif(round($average)>50 && round($average) <= 70)
                 {
                    $avgStatus = "Buona";
                    $colorBar = "#C4C524";
                    $avg = 4;
                 }
                elseif(round($average)>70 && round($average) <= 100)
                {
                    $avgStatus = "Accettabile";
                    $colorBar = "#C57003";
                    $avg = 3;
                }
                elseif(round($average)>100 && round($average) <= 200)
                {
                    $avgStatus = "Cattiva";
                    $colorBar = "#C53A00";
                    $avg = 2;
                }
                else
                {
                    $avgStatus = "Pessima";
                    $colorBar = "#c5000a";
                    $avg = 1;
                }

                $chart_date[$j]["indexLabel"] =  $avgStatus;
                $chart_date[$j]["y"] =  $avg;
                $chart_date[$j]["color"] =  $colorBar;
            }
        }
    }
}
else{
    echo 'there is no data';
}
$dataPoints = $chart_date;

// ==================================

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

/*
<h3 class="text-center custumTagH">Valori rilevati dai sensori</h3>
<ul class="list-group">
  <li class=" text-body list-group-item list-group-item-info">PM10: <?php echo $pm10; ?></li>
  <li class="text-body list-group-item list-group-item-info">PM2.5: <?php echo $pm25; ?></li>
  <li class="text-body list-group-item list-group-item-info">NO2: <?php echo $no2; ?></li>
  <li class="text-body list-group-item list-group-item-info">O3: <?php echo $o3; ?></li>
</ul>
<h4 class="text-center custumTagH">* Valori di no2 e o3 temporaneamente simulati</h4>

<li class="text-body list-group-item list-group-item-info">Valore IPQA: <?php echo $aqiValue; ?></li>
*/
?>


<meta http-equiv="refresh" content="30">
<link href="<?php echo get_template_directory_uri() . '/aqi/CSS/styleAvatar.css' ?>" rel="stylesheet">
<script src="<?php echo get_template_directory_uri() . '/aqi/CSS/canvasjs.min.js' ?>"></script>

  <div class="container page-box" style="background: url('<?php echo $bgUrl ?>') center bottom no-repeat;">
    <div class="page_content row">
      <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
        <section id="hero" >
          <div class="hero-container">
            <h2 class="avatar-name">Andy</h2>
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
              <li class="text-body list-group-item list-group-item-info">Temperatura: <?php echo $temp; ?> &#8451;</li>
              <li class="text-body list-group-item list-group-item-info">Umidità: <?php echo $hum; ?>%</li>
              <li class="text-body list-group-item list-group-item-info">Data ultimo rilevamento: <?php echo $aqiDateCollect; ?></li>
            </ul>

            <h3 class="text-center custumTagH">Storico stato IPQA</h3>
            <div id="chartContainer" style="height: 370px; width: 100%; border: 2px solid #abdde5;"></div>
        </div>
      </div>
      <div class="clear"></div>
    </div>
  </div>

<?php get_footer();?>

<script>
window.onload = function () {
var chart = new CanvasJS.Chart("chartContainer", {
    theme: "light2",
	backgroundColor: "transparent",
	axisX:{
	labelAngle: -90,
	},
	axisY: {
		labelAngle: -75,
		interval:1,
	    labelFormatter(val){
          if(val.value == 5)
            return "Ottima";
          else if(val.value == 4)
            return "Buona";
          else if(val.value == 3)
            return "Accettabile";
          else if(val.value == 2)
            return "Cattiva";
          else if(val.value == 1)
            return "Pessima";
          else
            return " "
        }
	},
	data: [{
	    indexLabelFontSize: 20,
		type: "column",
		dataPoints: <?php echo json_encode($dataPoints, JSON_NUMERIC_CHECK); ?>
	}]
});
chart.render();
}
</script>




