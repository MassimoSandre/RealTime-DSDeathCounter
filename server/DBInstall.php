<?php
    if($_POST) {
        // getting database info
        include_once("config.php");

        // checking password
        if(hash("sha512",$_POST["password"]) == $dbinstallpw) {
            // checking if the database needs to be created
            if($createDB) {
                // conneting to dtabase
                $con = new mysqli($hostname, $username, $password);
                
                // checking connection
                if($con->connect_error) {
                    die ("Connessione fallita: " . $con->connect_error);
                }

                // creating datatabsae
                $sql = "CREATE DATABASE IF NOT EXISTS $database";
                if($con->query($sql) === TRUE) {
                    echo "Database successfully created<br><br>";
                }   
                else{
                    echo "Failed to create the database";
                }

                $con->close();
            }

            // connecting to database
            $con = new mysqli($hostname, $username, $password, $database);
                
            // checking connection
            if($con->connect_error) {
                die ("Connessione fallita: " . $con->connect_error);
            }

            // ------ tables ------
            // creating 'Users'
            $sql = "
                CREATE TABLE IF NOT EXISTS `Users` (
                    `UserID` INT(16) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    `username` VARCHAR(255) NOT NULL
                ) ENGINE=InnoDB;
                
                ";
            
            if($con->query($sql) === TRUE) {
                echo "Users table successfully created<br><br>";
            }   
            else{
                die ("failed to create Users table'" . $con->error);
            }
            
            // creating 'Deaths'
            $sql = "
                CREATE TABLE IF NOT EXISTS `Deaths`(

                    `DeathID` INT(16) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    `count` INT(16) NOT NULL,
                    `timestamp` DATETIME,
                    `UserID` INT(16) NOT NULL,
                    FOREIGN KEY (`UserID`) REFERENCES `Users`(`UserID`)

                )ENGINE=InnoDB;";
            
            if($con->query($sql) === TRUE) {
                echo "Deaths table successfully created<br><br>";
            }   
            else{
                die ("failed to create Deaths table'" . $con->error);
            }

            // Inserting sample data in Users table
            $sql = "
                INSERT INTO Users(username)
                VALUES  ('User1'),
                        ('User2'),
                        ('User3'),
                        ('User4');";
            if($con->query($sql) === TRUE) {
                echo "users correctly inserted in the Users table<br><br>";
            }   
            else{
                die ("failed to insert users in the Users table " . $con->error);
            }
            
            echo "Database successfully created";
            $installed = true;

            $con->close();
        }
        else {
            echo "Wrong password<br><br>";
        }
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DBinstall</title>
</head>
<body>
    <?php
    if(!isset($installed) || !$installed) {
        echo "Installation password:
            <form action='". $_SERVER["PHP_SELF"] ."' method='POST'>
                <input type='password' name='password' placeholder='password'>
                <input type='submit' value='Submit'>
            </form>";
        }
    ?>
</body>
</html>