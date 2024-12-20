import web_server._logic as web_server_logic
import logger.bcolors
import logger

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints import _


def make_server(
    port: web_server_logic.port_typ,
    *args,
    **kwargs,
) -> web_server_logic.web_server:
    logger.log(
        (
            f"{logger.bcolors.bcolors.BOLD}[TCP %d %s]{logger.bcolors.bcolors.ENDC}: initialising webserver" %
            (port.port_num, 'IPv6' if port.is_ipv6 else 'IPv4',)
        ),
        context=logger.log_context.PYTHON_SETUP,
    )
    cls = web_server_logic.web_server_ssl if port.is_ssl else web_server_logic.web_server
    return cls(port, *args, **kwargs)
