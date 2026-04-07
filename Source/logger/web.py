from . import bc, filter


def get_message(log_filter: filter.filter_type_web, bcolors: bc.bcolors, text: bytes, is_error: bool) -> str | None:
    if not is_error:
        if not log_filter.urls:
            return
        return (
            f'{bcolors.OKCYAN}[Webserver]{bcolors.ENDC} %s'
        ) % (
            text.decode('utf-8'),
        )

    if not log_filter.errors:
        return
    return (
        f'{bcolors.FAIL}[Webserver Error]\n%s{bcolors.ENDC}'
    ) % (
        text.decode('utf-8'),
    )
