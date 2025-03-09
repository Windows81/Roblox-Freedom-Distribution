from . import filter

URL_PREFIX = b'http'


def get_message(text: bytes, log_filter: filter.filter_type) -> str | None:
    if text.startswith(URL_PREFIX):
        if not log_filter.web_logs.urls:
            return
        return (
            f'{log_filter.bcolors.OKCYAN}[Webserver]{log_filter.bcolors.ENDC} %s'
        ) % (
            text.decode('utf-8'),
        )

    if not log_filter.web_logs.errors:
        return
    return (
        f'{log_filter.bcolors.FAIL}[Webserver Error]\n%s{log_filter.bcolors.ENDC}'
    ) % (
        text.decode('utf-8'),
    )
