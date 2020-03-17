<?php
/*
* Template Name: readRestAqi
* description: >-
Page template without sidebar
*/

// Additional code goes here...
// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

// get database connection
include_once get_template_directory() . '/aqi/Database.php';

// instantiate AQI object
include_once get_template_directory() . '/aqi/AQI.php';

$database = new Database();
$db = $database->getConnection();
//TODO : Add authentication for reading data and the number of rows which is needed as parameter


$aqi = new Aqi($db);

// query products
$stmt = $aqi->read();
$num = $stmt->rowCount();
// check if more than 0 record found
if($num>0){

    // products array
    $rowsArr=array();
    $rowsArr["records"]=array();

    // retrieve our table contents
    // fetch() is faster than fetchAll()
    // http://stackoverflow.com/questions/2770630/pdofetchall-vs-pdofetch-in-a-loop
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)){
        // extract row
        // this will make $row['name'] to
        // just $name only
        extract($row);

        $rowItem=array(
            "aqiId" => $aqiId,
            "aqiValue" => $aqiValue,
            "aqiStatus" => $aqiStatus,
            "aqiDateInsert" => $aqiDateInsert,
            "aqiDateCollect" => $aqiDateCollect
        );

        array_push($rowsArr["records"], $rowItem);
    }

    // set response code - 200 OK
    http_response_code(200);

    // show products data in json format
    echo json_encode($rowsArr);
}
else{

    // set response code - 404 Not found
    http_response_code(404);

    // tell the user no products found
    echo json_encode(
        array("message" => "No record found.")
    );
}
?>