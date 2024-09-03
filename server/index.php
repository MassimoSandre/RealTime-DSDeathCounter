<?php
	// if no GET parameters are provided, terminate the script with an error message
    if(!$_GET) die("no param");

    // Include the configuration file which contains database connection details
	include_once("config.php");


    // Check if the 'user' parameter is set and 'deaths' parameter is not set in the GET request
	if (isset($_GET["user"]) && !isset($_GET["deaths"])) {
        $user = $_GET["user"]; // Get the 'user' parameter from the GET request
        
        // Establish a new connection to the database
        $con = new mysqli($hostname, $username, $password, $database);

        // Execute a query to retrieve user information and their latest death count
        $res = $con -> query("SELECT * FROM `Users` u INNER JOIN `Deaths` d ON (u.`UserID` = d.`UserID`) WHERE u.`username` = '$user' ORDER BY d.`timestamp` DESC") or die("Failed to retrieve deaths");

        // If no data is found for the specified user, terminate the script with an error message
		if(mysqli_num_rows($res) == 0) die("no data available for this user");

        // Fetch the first row from the result set
        $row = $res -> fetch_assoc();

        // Output the HTML to display the death count, and include a script to refresh the page every 5 seconds
        echo "
			<html>
				<head>
					<link rel=\"stylesheet\" href=\"style.css\">
				</head>
				<body>
					<div class = 'deathcount'>".$row['count']."</div>

					<script>
						function reloadPage() {
							window.location.reload();
						}

						var intervalId = window.setInterval(function(){
							reloadPage();
						}, 5000);
					</script>
				</body>
			</html>";
        
	}
    // If the 'deaths' parameter is also in the GET request, update the death count for the user
	else if(isset($_GET["user"]) && isset($_GET["deaths"])){
        $user = $_GET["user"]; // Get the 'user' parameter from the GET request
        $deaths = $_GET["deaths"]; // Get the 'deaths' parameter from the GET request
        $datetime = date("Y-m-d H:i:s");  // Get the current date and time
        
        // Establish a new connection to the database
        $con = new mysqli($hostname, $username, $password, $database);

        // Execute a query to check if the user exists in the 'Users' table
        $res = $con -> query("SELECT * FROM `Users` u WHERE u.`username` = '$user';") or die("Failed to retrieve the UserID: " . $con->error);
        
        // If the user does not exist, insert the user into the 'Users' table
        if(mysqli_num_rows($res) == 0)
			$con -> query("INSERT INTO `Users`(`username`) VALUES ('$user');") or die ("Failed to insert the new user in the database");
            $res = $con -> query("SELECT * FROM `Users` u WHERE u.`username` = '$user';") or die("Failed to retrieve the UserID upon insertion: " . $con->error);
        
        // Get the 'UserID' for the specified user
		$userID = $res -> fetch_assoc()['UserID'];

		// Insert a new record into the 'Deaths' table with the death count and timestamp
		$con->query("INSERT INTO `Deaths` (`count`, `timestamp`, `UserID`) VALUES ($deaths, '$datetime', $userID);") or die ("Failed to insert the updated deaths value in the database");

        // Close the database connection
		$con->close();

        // Output a completion message
		echo $user . "'s deaths counter was successfully updated :P";
    }
?>