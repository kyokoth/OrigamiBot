from typing import List, Callable
from inspect import getmembers


class CommandContainer:
    """Class that contains objects that contain bot's commands as methods"""
    def __init__(self):
        self.command_holders = []
        self._cache = dict()

    def add_command(self, obj, cache=True):
        """Add object to command container."""
        self.command_holders.append(obj)

        if cache:
            for c_name, c_call in getmembers(obj, lambda item: callable(item)):
                if c_name.startswith('_'):
                    continue
                if c_name in self._cache.keys():
                    self._cache[c_name].append(c_call)
                else:
                    self._cache[c_name] = [c_call]

    def remove_by_filter(self, filter_func: Callable):
        """Remove commands from container by filter

        Filter must be a callable with single argument(item)
        and should return True for each item that needs removing
        """
        removables = [
            i
            for i in self.command_holders
            if filter_func(i)
        ]

        if removables:
            self._cache = dict()

        for r in removables:
            self.command_holders.remove(r)

    def clear(self):
        """Remove all commands"""
        self.command_holders.clear()
        self._cache = dict()

    def find_command(self, command: str) -> List[Callable]:
        """Find a method for given command.

        Returns a list of all matched methods.
        """
        if command.startswith('/'):
            command = command[1:]

        if command in self._cache.keys():
            return self._cache[command]

        # Do not look for protected/private methods
        if command.startswith('_'):
            return []

        matches = []
        for holder in self.command_holders:
            if hasattr(holder, command):
                command_handle = getattr(holder, command)
                if callable(command_handle):
                    matches.append(command_handle)
        self._cache[command] = matches
        return matches
