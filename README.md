# Real-Time Death Counter for Dark Souls/Sekiro

## Project Description
This project allows you to monitor in real-time the number of player deaths during gameplay sessions of Dark Souls or Sekiro. The death count can be displayed through a web interface that automatically updates and can be integrated as an external source in software like OBS, allowing players to stream with a live-updating death counter for viewers to see.

### Project Components
- Client: A Python application that reads the game's process memory to retrieve the death count and send it to the server.
- Server: A PHP application that receives data from the client, stores it in a database, and provides a web interface to display the death count. 

## Credits
This project was inspired by [@Quidrex](https://github.com/Quidrex)'s [DSDeaths](https://github.com/Quidrex/DSDeaths), which was initially used to track and log the number of deaths. Although this project no longer relies on DSDeaths, its concepts and implementation provided a fundation that greatly contributed to the development of this project.

### Project Authors:
- Massimo Albino Sandretti ([@MassimoSandre](https://github.com/MassimoSandre))
- Valentino Angelo Lenzi ([@ReiettoAyanami](https://github.com/ReiettoAyanami))

## Requirements
- Python 3.12 and the following modules: `pymem`, `psutil`, `requests`, `json`
- PHP 7.x or higher
- MySQL/MariaDB

## Installation
### Client Configuration
1. Open the **`config.json`** file in the **`client`** folder and modify the following parameters to fit you system:
    - **`baseURL`**: the server URL where the data will be sent
    - **`username`**: the username to identify the player
    - **`lastDeathsRecorded`**: leave it as 0 or set it to the last recorded death count
2. Install the necessary Python modules: `pymem`, `psutil`, `requests`, `json`

### Server Configuration
1. Open the **`config.php`** file in the **`server`** folder and modify the following parameters:
    - **`$hostname`**: your MySQL/MariaDB server hostname
    - **`$username`**: your MySQL/MariaDB database username
    - **`$password`**: your MySQL/MariaDB database password
    - **`$database`**: the name of the MySQL/MariaDB to be used/created
    - **`$adminPassword`**: the sha512 hash of the password required to install the database via the **`DBInstallation.php`** script
    - **`$createDB`**: to specify if a new database needs to be created (otherwise an existing database with the provided name will be used)

### Database Installation
1. Upload all server files to your web server
2. Open a browser and navigate to the **`DBInstallation.php`** file
3. Enter the password set in **`config.php`**
Following these instructions you will create the necessary database and tables, and populate it with some example users (you might want to check the **`DBInstallation.php`** file to edit the starting users).

## Usage
1. Run the Python client to start monitoring deaths during the gameplay session. **Start the client while the game is running, otherwise the process will end**.
2. Access the web interface provided by the server to view the death count in real-time. **To do this, you must pass the `user` parameter via a GET request to the `index.php` page on the server.** For example, if your server is hosted at `http://sample.smp`, you would navigate to `https://sample.smp?user=yourusername`.
3. To integrate the counter into OBS, use the same URL (`https://sample.smp?user=yourusername`) as a browser source in your streaming scene.