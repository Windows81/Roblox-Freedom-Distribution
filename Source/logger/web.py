from . import filter


def get_message(text: bytes, log_filter: filter.filter_type, is_error: bool) -> str | None:
    if not is_error:
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
