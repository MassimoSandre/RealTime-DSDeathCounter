class Game:
    def __init__(self, process_name:str, name:str, offsets64:tuple) -> None:
        """
        Initializes a Game object with the process name, user-friendly name, and memory offsets.

        :param process_name: The name of the game's executable file (e.g., "DarkSoulsIII.exe").
        :param name: The user-friendly name of the game (e.g., "Dark Souls III").
        :param offsets64: A tuple of memory offsets used to locate the death counter in the game's memory.
        """
        self.process_name = process_name
        self.name = name
        self.offsets64 = offsets64