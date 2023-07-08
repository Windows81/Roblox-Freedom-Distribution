import subprocess
import versions
import argparse
import studio
import server
import player
import uwamp

CLASSES: dict[str, type[subprocess.Popen]] = {
    'studio': studio.Studio,
    'server': server.Server,
    'player': player.Player,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version', '-v',
        type=lambda v: versions.VERSION_MAP[v],
    )
    mode_parsers = parser.add_subparsers(dest='mode')

    studio_parser = mode_parsers.add_parser('studio')
    server_parser = mode_parsers.add_parser('server')
    server_parser.add_argument(
        '--place', '-p', dest='data',
        type=lambda n: open(n, 'rb'),
        default=None, nargs='?',
    )
    player_parser = mode_parsers.add_parser('player')
    player_parser.add_argument(
        '--rcc_host', '-rh',
        dest='rcc_host', type=str,
        default=None, required=True,
    )
    player_parser.add_argument(
        '--web_host', '-wh',
        dest='web_host', type=str,
        default=None, nargs='?',
    )
    player_parser.add_argument(
        '--rcc_port', '-rp',
        dest='rcc_port',
        type=int, nargs='?',
    )
    player_parser.add_argument(
        '--web_port', '-wp',
        dest='web_port',
        type=int, nargs='?',
    )
    player_parser.add_argument(
        '--username', '-u',
        dest='username',
        type=str, nargs='?',
        default='VisualPlugin'
    )

    try:
        args = parser.parse_args()
        c = CLASSES[args.mode](**args.__dict__)
        c.communicate()
    except KeyboardInterrupt:
        pass
