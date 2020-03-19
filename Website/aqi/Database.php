<?php
class Database{

    // specify your own database credentials
    private $host = "airpolitoit.mydb-aruba.it";
    private $db_name = "Swp1375751-prod";
    private $username = "Swp1375751";
    private $password = "6zg134ou8d";
    public $conn;

    // get the database connection
    public function getConnection(){

        $this->conn = null;

        try{
            $this->conn = new PDO("mysql:host=" . $this->host . ";dbname=" . $this->db_name, $this->username, $this->password);
            $this->conn->exec("set names utf8");
        }catch(PDOException $exception){
            echo "Connection error: " . $exception->getMessage();
        }

        return $this->conn;
    }
}
?>