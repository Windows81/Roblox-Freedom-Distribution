from . import bcolors, filter
import textwrap

URL_PREFIX = b'http'


def get_message(text: bytes, filter: filter.filter_type) -> str | None:
    if text.startswith(URL_PREFIX):
        if not filter.web_logs.urls:
            return
        return (
            f'{bcolors.bcolors.OKCYAN}[Webserver]{bcolors.bcolors.ENDC} %s' %
            (text.decode('utf-8'),)
        )

    if not filter.web_logs.errors:
        return
    return (
        f'{bcolors.bcolors.FAIL}[Webserver Error]\n%s{bcolors.bcolors.ENDC}' %
        (text.decode('utf-8'),)
    )
