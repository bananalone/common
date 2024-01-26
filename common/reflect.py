'''
Author: bananalone
Date: 2024-01-04
Copyright (c) 2024 by bananalone, All Rights Reserved.
'''


import importlib


class ModuleAgent:
    def __init__(self, module: str) -> None:
        self._module = importlib.import_module(module)

    def has_member(self, name: str):
        return hasattr(self._module, name)
    
    def get_member(self, name: str):
        if not self.has_member(name):
            raise MemberNotFoundError
        return getattr(self._module, name)
    
    def trigger(self, name: str, inputs: dict = None):
        if not self.has_member(name):
            raise MemberNotFoundError(self._module, name)
        member = self.get_member(name)
        if not callable(member):
            raise TriggerError(self._module, name)
        inputs = inputs if inputs else {}
        return member(**inputs)


class MemberNotFoundError(Exception):
    def __init__(self, module: str, member: str) -> None:
        super().__init__()
        self._module = module
        self._member = member

    def __str__(self) -> str:
        return f'no {self._member} found in {self._module}'


class TriggerError(Exception):
    def __init__(self, module: str, member: str) -> None:
        super().__init__()
        self._module = module
        self._member = member

    def __str__(self) -> str:
        return f'{self._member} in {self._module} is not callable'
