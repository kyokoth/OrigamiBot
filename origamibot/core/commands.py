from typing import List, Callable


class CommandContainer:
    """Class that contains objects that contain bot's commands as methods"""
    def __init__(self):
        self.command_holders = []

    def add_command(self, obj):
        """Add object to command container."""
        self.command_holders.append(obj)

    def find_command(self, command: str) -> List[Callable]:
        """Find a method for given command.

        Returns a list of all matched methods.
        """
        if command.startswith('/'):
            command = command[1:]

        # Do not look for protected/private methods
        if command.startswith('_'):
            return []

        matches = []
        for holder in self.command_holders:
            if hasattr(holder, command):
                command_handle = getattr(holder, command)
                if callable(command_handle):
                    matches.append(command_handle)
        return matches
