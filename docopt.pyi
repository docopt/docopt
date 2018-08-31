# Stubs for docopt (Python 2.7, 3.5)

from typing import (
    Any,
    List,
    Tuple,
    Union,
    # These docopt classes must not be clobbered.
    Dict as TDict,
    Optional as TOptional,
)


# Acceptable values in a Docopt Dict.
TDocoptValue = Union[bool, int, str, List[str]]

# A map of flags/options to their acceptable values.
TDocoptDict = TDict[str, TDocoptValue]

# Argument or Option
TArgumentOption = Union[Argument, Option]

# Acceptable source types for parsing.
TSource = Union[str, List[str]]

# match() result.
TMatch = Tuple[
    bool,
    TArgumentOption,
    List[TArgumentOption]
]

# single_match() result, with optional values.
TSingleMatch = Tuple[
    Union[int, None],
    Union[Argument, Command, None]
]

class DocoptLanguageError(Exception): ...

class DocoptExit(SystemExit):
    usage = ...  # type: str
    def __init__(self, message: TOptional[str]='') -> None: ...

class Pattern:
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def fix(self) -> LeafPattern: ...
    def fix_identities(
        self,
        uniq: TOptional[List[Pattern]]=None) -> None: ...
    def fix_repeating_arguments(self) -> Pattern: ...

def transform(pattern: Pattern) -> Either: ...

class LeafPattern(Pattern):
    def __init__(
        self,
        name: str,
        value: TOptional[Union[str, int, List[Union[str, Pattern]]]]=None) -> None: ...
    def flat(self, *types: type) -> List[Pattern]: ...
    def match(
        self,
        left: List[LeafPattern],
        collected: TOptional[List[Pattern]]=None) -> Tuple[bool, Pattern, List[Pattern]]: ...

class BranchPattern(Pattern):
    children = ...  # type: List[BranchPattern]
    def __init__(self, *children: Pattern) -> None: ...
    def flat(self, *types: type) -> List[Pattern]: ...

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
        value: TOptional[Union[str, bool]]=False) -> None: ...
    @classmethod
    def parse(class_, option_description: str) -> Option: ...
    def single_match(self, left: List[LeafPattern]) -> TSingleMatch: ...
    @property
    def name(self) -> str: ...

class Required(BranchPattern):
    def match(
        self,
        left: List[TArgumentOption],
        collected: TOptional[List[BranchPattern]]=None) -> TMatch: ...

class Optional(BranchPattern):
    def match(
        self,
        left: List[TArgumentOption],
        collected: TOptional[List[BranchPattern]]=None) -> TMatch: ...

class OptionsShortcut(Optional): ...

class OneOrMore(BranchPattern):
    def match(
        self,
        left: List[TArgumentOption],
        collected: TOptional[List[BranchPattern]]=None) -> TMatch: ...

class Either(BranchPattern):
    def match(
        self,
        left: List[TArgumentOption],
        collected: TOptional[List[BranchPattern]]=None) -> TMatch: ...

class Tokens(list):
    error = ...  # type: type
    def __init__(
        self,
        source: TSource,
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
    options_first: bool=False) -> List[TArgumentOption]: ...
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
    argv: TOptional[TSource]=None,
    help: TOptional[bool]=True,
    version: TOptional[str]=None,
    options_first: TOptional[bool]=False) -> TDocoptDict: ...

x = ...  # type: str
