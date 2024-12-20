from . import bcolors, filter, flog_table
import re


def get_message(text: bytes, filter: filter.filter_type) -> str | None:
    if not filter.other_logs:
        return
    return (
        f'{bcolors.bcolors.OKCYAN}[Webserver]{bcolors.bcolors.ENDC} %s' %
        (text.decode('utf-8'),)
    )
