# -*- coding: utf-8 -*-
from dataclasses import dataclass


class User:
    id: int
    name: str
    birthdate: date
    admin: bool = False

# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
@dataclass
class RenameWork:
    '''
    An rename work details
    '''
    name: str
    old_name: str
    seq: int = 1


class RenameHistory:
    '''
    Rename work history
    '''
    def __init__(self):
        '''
        Initialization
        '''
        self.history = {}

    def add(self, name, old_name):
        '''
        Add a new file name to history
        '''
        if name in self.history:
            x = self.history.get(name)
            x.seq += 1
        else:
            x = RenameWork()
            x.name = name
            x.old_name = old_name
            self.history[name] = x

        return x.seq