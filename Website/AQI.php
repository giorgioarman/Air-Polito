<?php
class Aqi{

    // database connection and table name
    private $conn;
    private $table_name = "AQI_Data";

    //TODO compare all the variable which is needed in the Raspberry with online database
    // object properties
    public $aqiId;
    public $aqiValue;
    public $aqiStatus;
    public $aqiDateCollect;
    public $aqiDateInsert;

    // constructor with $db as database connection
    public function __construct($db){
        $this->conn = $db;
    }

    // create product
    function create(){

        // query to insert record
        $query = "INSERT INTO
                    " . $this->table_name . "
                SET // name in the database=:name of object
                    aqi_value=:aqiValue, aqi_status=:aqiStatus, aqi_date_collect=:aqiDateCollect";

        // prepare query
        $stmt = $this->conn->prepare($query);

        // sanitize
        $this->aqiValue=htmlspecialchars(strip_tags($this->aqiValue));
        $this->aqiStatus=htmlspecialchars(strip_tags($this->aqiStatus));
        $this->aqiDateCollect=htmlspecialchars(strip_tags($this->aqiDateCollect));

        // bind values
        $stmt->bindParam(":aqiValue", $this->aqiValue);
        $stmt->bindParam(":aqiStatus", $this->aqiStatus);
        $stmt->bindParam(":aqiDateCollect", $this->aqiDateCollect);

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