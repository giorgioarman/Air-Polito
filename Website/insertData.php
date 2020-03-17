<?php
/*
* Template Name: insertRestAqi
* description: >-
Page template without sidebar
*/

// Additional code goes here...
// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

// get database connection
include_once get_template_directory() . '/aqi/Database.php';

// instantiate AQI object
include_once get_template_directory() . '/aqi/AQI.php';

$database = new Database();
$db = $database->getConnection();

$aqi = new Aqi($db);

// get posted data
$data = json_decode(file_get_contents("php://input"));
//TODO : Add authentication for insert data

// make sure data is not empty
if(
    !empty($data->aqi_value) &&
    !empty($data->aqi_status) &&
    !empty($data->aqi_date_collect)
){
     // set product property values
    $aqi->aqiValue = $data->aqi_value;
    $aqi->aqiStatus = $data->aqi_status;
    $aqi->aqiDateCollect = $data->aqi_date_collect;

    // create the product
    if($aqi->create()){

        // set response code - 201 created
        http_response_code(201);

        // tell the user
        echo json_encode(array("message" => "AQI was Inserted."));
    }

    // if unable to create the product, tell the user
    else{

        // set response code - 503 service unavailable
        http_response_code(503);

        // tell the user
        echo json_encode(array("message" => "Unable to insert AQI."));
    }
}

// tell the user data is incomplete
else{

    // set response code - 400 bad request
    http_response_code(400);

    // tell the user
    echo json_encode(array("message" => "Unable to insert AQI. Data is incomplete."));
}
?>