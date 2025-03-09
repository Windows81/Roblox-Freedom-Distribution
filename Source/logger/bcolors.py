import dataclasses


@dataclasses.dataclass(frozen=True)
class bcolors:
    HEADER: str
    OKBLUE: str
    OKCYAN: str
    OKGREEN: str
    WARNING: str
    FAIL: str
    ENDC: str
    BOLD: str
    UNDERLINE: str


BCOLORS_VISIBLE = bcolors(
    HEADER='\033[95m',
    OKBLUE='\033[94m',
    OKCYAN='\033[96m',
    OKGREEN='\033[92m',
    WARNING='\033[93m',
    FAIL='\033[91m',
    ENDC='\033[0m',
    BOLD='\033[1m',
    UNDERLINE='\033[4m',
)


BCOLORS_INVISIBLE = bcolors(
    HEADER='',
    OKBLUE='',
    OKCYAN='',
    OKGREEN='',
    WARNING='',
    FAIL='',
    ENDC='',
    BOLD='',
    UNDERLINE='',
)
