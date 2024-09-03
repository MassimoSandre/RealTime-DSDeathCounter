from game import Game
from pointer import Pointer

import os
import time

from pymem import Pymem
import pymem
import psutil
import requests
import json

# List of games with their respective executable names, user-friendly names, and memory offsets for death counters.
games = [
    Game("DarkSoulsII.exe", "Dark Souls II", (0x16148F0, 0xD0, 0x490, 0x104)),
    Game("DarkSoulsIII.exe", "Dark Souls III", (0x47572B8, 0x98)),
    Game("DarkSoulsRemastered.exe", "Dark Souls Remastered", (0x1C8A530, 0x98)),
    Game("Sekiro.exe", "Sekiro", (0x3D5AAC0, 0x90)),
    Game("eldenring.exe", "Elden Ring", (0x3CD4D88, 0x94))
]

def get_processes_by_name(name) -> list[psutil.Process]:
    """
    Returns a list of all processes with the given name.
    :param name: Name of the process to search for.
    :return: List of matching psutil.Process objects.
    """
    return [process for process in psutil.process_iter() if process.name() == name]

def is_windows_64bit() -> bool:
    """
    Checks if the current operating system is 64-bit.
    :return: True if the OS is 64-bit, False otherwise.
    """
    if 'PROCESSOR_ARCHITEW6432' in os.environ:
        return True
    return os.environ['PROCESSOR_ARCHITECTURE'].endswith('64')

def scan_processes() -> tuple[psutil.Process, Game]:
    """
    Scans running processes to find a game process from the predefined list.
    :return: A tuple containing the first found process and the corresponding game object.
    """
    proc = None
    game = None
    for g in games:
        processes = get_processes_by_name(g.process_name)
        if len(processes) != 0:
            print("Found: " + g.name)
            proc = processes[0]
            game = g
            break
    return (proc, game)

def retrieve_deaths_pointer(process:psutil.Process, offsets) -> Pointer:
    """
    Retrieves a pointer to the death counter in the game's memory.
    :param process: The psutil.Process object representing the game.
    :param offsets: The memory offsets for the death counter.
    :return: A Pointer object to the death counter memory address.
    """
    pymemProcess = Pymem(process.name())
    
    # Get the base address of the game's executable in memory.
    address = pymem.process.module_from_name(pymemProcess.process_handle, process.name()).lpBaseOfDll

    # Traverse the memory offsets to reach the death counter's address.
    for offset in offsets[:-1]:
        if address == 0:
            print("Encountered null pointer")
            return 0

        address = pymemProcess.read_ulonglong(address + offset)
    
    # Add the final offset to get the exact address.
    address += offsets[-1]

    # Create a Pointer object to the final memory address.
    p = Pointer(pymemProcess, address)
    return p


def main() -> None:
    """
    The main function of the script. Monitors the game's death counter and sends updates to the server when the count changes.
    """
    # Load configuration data from JSON file.
    with open("config.json", 'r') as f:
        data = json.load(f)

    print("Looking for Dark Souls process...")

    # Scan for the game's process and retrieve the corresponding game object.
    process, game = scan_processes()
    if(not process or not game):
        print("No game process found, open the game and then run this script")
        return
    
    offsets = None
    isWin64 = is_windows_64bit()
    if isWin64:
        print("64 bits system detected")
        offsets = game.offsets64
    else:
        print("32 bits system detected: this script only works for 64 bits systems")
        return

    # Retrieve the pointer to the death counter in the game's memory.
    deaths_pointer = retrieve_deaths_pointer(process, offsets)

    # Continuously monitor the death counter while the game is running.
    while process.is_running():
        # Read the current value of the death counter.
        deaths = deaths_pointer.read_pointed_value()
        print("Deaths: ", deaths)

        # If the death count has changed, send an update to the server.
        if deaths != 0 and deaths != data["lastDeathsRecorded"]:
            print("\tsending update to the server...", end='')
            request = requests.get(f"{ data['baseURL'] }?user={data['username']}&deaths={deaths}")
            if request.ok:
                print(" update succedeed: ", request.text)
                data["lastDeathsRecorded"] = deaths
            else:
                print(" update failed, retrying...")

        # Wait for 5 seconds before checking again.
        time.sleep(5)

    print("game closed")

    # Save the updated death count back to the configuration file.
    with open("config.json", 'w') as f:
        json.dump(data, f, indent=4)
        


if __name__ == "__main__":
    main()