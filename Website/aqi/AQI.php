<?php
class Aqi{

    // database connection and table name
    private $conn;
    private $table_name = "AQI_Data";

    // object properties
    public $aqiId;
    public $aqiValue;
    public $aqiStatus;
    public $aqiSensorData;
    public $aqiDateCollect;
    public $aqiDateInsert;

    // constructor with $db as database connection
    public function __construct($db){
        $this->conn = $db;
    }

    // create product
    function create(){

        // sanitize
        $this->aqiValue=htmlspecialchars(strip_tags($this->aqiValue));
        $this->aqiStatus=htmlspecialchars(strip_tags($this->aqiStatus));
        $this->aqiDateCollect=htmlspecialchars(strip_tags($this->aqiDateCollect));
        //$this->aqiSensorData=htmlspecialchars(strip_tags($this->aqiSensorData));

        // query to insert record
        $query = "INSERT INTO
                    " . $this->table_name . "
                SET aqi_value=:aqiValue,
                    aqi_status=:aqiStatus,
                    aqi_date_collect=:aqiDateCollect,
                    aqi_sensor_data=:aqiSensorData";

        // prepare query
        $stmt = $this->conn->prepare($query);

        // bind values
        $stmt->bindParam(":aqiValue", $this->aqiValue);
        $stmt->bindParam(":aqiStatus", $this->aqiStatus);
        $stmt->bindParam(":aqiDateCollect", $this->aqiDateCollect);
        $stmt->bindParam(":aqiSensorData", $this->aqiSensorData);

        // execute query
        if($stmt->execute()){
            return true;
        }

        return false;
    }

    // read products
    function read(){
        // select all query
        $query = "SELECT
                    p.aqi_id as aqiId,
                    p.aqi_value as aqiValue,
                    p.aqi_status as aqiStatus,
                    p.aqi_sensor_data as aqiSensorData,
                    p.aqi_date_collect as aqiDateCollect,
                    p.aqi_date_insert as aqiDateInsert
                FROM
                    " . $this->table_name . " p
                ORDER BY
                    p.aqi_date_collect DESC
                LIMIT 10";

        // prepare query statement
        $stmt = $this->conn->prepare($query);

        // execute query
        $stmt->execute();

        return $stmt;
    }
}
?>