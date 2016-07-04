# Stubs for docopt (Python 2.7, 3.5)

from typing import (
    Any,
    # Don't shadow docopt's Dict class.
    Dict as TDict,
    List,
    # Don't shadow docopt's Optional class.
    Optional as TOptional,
    Tuple,
    Union,
)

TMatch = Tuple[bool, Pattern, List[Pattern]]
TSingleMatch = Tuple[Union[int, None], Union[Argument, Command, None]]


class DocoptLanguageError(Exception): ...

class DocoptExit(SystemExit):
    usage = ...  # type: str
    def __init__(self, message: TOptional[str]='') -> None: ...

class Pattern:
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def fix(self) -> Pattern: ...
    def fix_identities(
        self,
        uniq: TOptional[List[Pattern]]=None) -> None: ...
    def fix_repeating_arguments(self) -> Pattern: ...

def transform(pattern: Pattern) -> Either: ...

class LeafPattern(Pattern):
    def __init__(
        self,
        name: str,
        value: TOptional[Pattern]=None) -> None: ...
    def flat(self, *types: List[type]) -> List[Pattern]: ...
    def match(
        self,
        left: Pattern,
        collected: TOptional[List[Pattern]]=None) -> Tuple[bool, Pattern, List[Pattern]]: ...

class BranchPattern(Pattern):
    children = ...  # type: List[Pattern]
    def __init__(self, *children: List[Pattern]) -> None: ...
    def flat(self, *types: List[type]) -> List[Pattern]: ...

class Argument(LeafPattern):
    def single_match(self, left: List[Argument]) -> TSingleMatch: ...
    @classmethod
    def parse(class_, source: str) -> Argument: ...

class Command(Argument):
    def __init__(
        self,
        name: str,
        value: bool=False) -> None: ...
    def single_match(self, left: List[Argument]) -> TSingleMatch: ...

class Option(LeafPattern):
    value = ...  # type: Pattern
    def __init__(
        self,
        short: TOptional[str]=None,
        long: TOptional[str]=None,
        argcount: TOptional[int]=0,
        value: TOptional[bool]=False) -> None: ...
    @classmethod
    def parse(class_, option_description: str) -> Option: ...
    def single_match(self, left: List[LeafPattern]) -> TSingleMatch: ...
    @property
    def name(self) -> str: ...

class Required(BranchPattern):
    def match(
        self,
        left: Pattern,
        collected: TOptional[List[Pattern]]=None) -> TMatch: ...

class Optional(BranchPattern):
    def match(
        self,
        left: Pattern,
        collected: TOptional[List[Pattern]]=None) -> TMatch: ...

class OptionsShortcut(Optional): ...

class OneOrMore(BranchPattern):
    def match(
        self,
        left: List[BranchPattern],
        collected: TOptional[List[Pattern]]=None) -> TMatch: ...

class Either(BranchPattern):
    def match(
        self,
        left: List[BranchPattern],
        collected: TOptional[List[Pattern]]=None) -> TMatch: ...

class Tokens(list):
    error = ...  # type: type
    def __init__(
        self,
        source: Union[str, List[str]],
        error: type=...) -> None: ...
    @staticmethod
    def from_pattern(source: str) -> Tokens: ...
    def move(self) -> TOptional[str]: ...
    def current(self) -> TOptional[str]: ...

def parse_long(
    tokens: Tokens,
    options: List[Option]) -> List[Option]: ...
def parse_shorts(
    tokens: Tokens,
    options: List[Option]) -> List[Option]: ...
def parse_pattern(
    source: str,
    options: List[Option]) -> Required: ...
def parse_expr(
    tokens: Tokens,
    options: List[Option]) -> List[Union[Either, Required]]: ...
def parse_seq(
    tokens: Tokens,
    options: List[Option]) -> List[OneOrMore]: ...
def parse_atom(
    tokens: Tokens,
    options: List[Option]) -> List[Union[LeafPattern, BranchPattern]]: ...
def parse_argv(
    tokens: Tokens,
    options: List[Option],
    options_first: bool=False) -> List[Union[Option, Argument]]: ...
def parse_defaults(doc: str) -> List[Option]: ...
def parse_section(name: str, source: str) -> List[str]: ...
def formal_usage(section: str) -> str: ...
def extras(
    help: bool,
    version: str,
    options: List[Option],
    doc: str) -> None: ...

class Dict(dict): ...

def docopt(
    doc: str,
    argv: TOptional[List[str]]=None,
    help: TOptional[bool]=True,
    version: TOptional[str]=None,
    options_first: TOptional[bool]=False) -> TDict: ...
