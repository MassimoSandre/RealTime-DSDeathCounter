import requests
import subprocess
import time
import json

def main() -> None:
    # reading configuration data from the 'config.json' file
    with open("config.json", 'r') as f:
        data = json.load(f)

    # program will continuo to run until no Dark Souls (/Sekiro) game is detected as open
    running = True

    while running:
        # Launches the 'DSDeaths.exe' application as a subprocess and captures its output
        process = subprocess.Popen(["counter\\DSDeaths.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Pauses the program for 5 seconds to allow the subprocess to run
        time.sleep(5)

        # Terminates the subprocess
        process.terminate()

        # Collects the output (stdout) from the subprocess
        stdout, _ = process.communicate()

        # Checks if the string "Found" is not in the output; if not, no game is currently running
        if "Found" not in stdout.decode("ascii"):
            running = False # Stops the loop if no game is found
        else:
            # Opens and reads the number of deaths from the 'DSDeaths.txt' file
            with open("DSDeaths.txt", 'r') as f:
                deaths = int(f.readline())

            # If the number of deaths has changed since last recorded, update the record
            if deaths != 0 and deaths != data["lastDeathsRecorded"]:
                data["lastDeathsRecorded"] = deaths # Update the last recorded death count

                # Sends an HTTP GET request to update the death count on a remote server
                request = requests.get(f"{ data['baseURL'] }?user={data['username']}&deaths={deaths}").content

                # Prints the server's response (debug)
                print(request.decode())

            # Pauses for 25 seconds before the next iteration
            time.sleep(25)
    
    # Writes the updated data back to the 'config.json' file after the loop ends
    with open("config.json", 'w') as f:
        json.dump(data, f, indent=4)

# Ensures that the main function is called when the script is run directly
if __name__ == "__main__":
    main()