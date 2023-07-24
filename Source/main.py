import subprocess
import argparse
import launcher.studio
import launcher.server
import launcher.player
import versions

CLASSES: dict[str, type[subprocess.Popen]] = {
    'studio': launcher.studio.Studio,
    'server': launcher.server.Server,
    'player': launcher.player.Player,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version', '-v',
        choices=list(versions.Version),
        type=lambda v: versions.VERSION_MAP[v],
    )
    mode_parsers = parser.add_subparsers(dest='mode')

    studio_parser = mode_parsers.add_parser('studio')
    studio_parser.add_argument(
        dest='args', nargs='*',
    )

    server_parser = mode_parsers.add_parser('server')
    server_parser.add_argument(
        '--place', '-p', dest='data',
        type=lambda n: open(n, 'rb'),
        default=None, nargs='?',
    )
    server_parser.add_argument(
        '--rcc_port', '-rp',
        dest='rcc_port',
        type=int, nargs='?',
    )
    server_parser.add_argument(
        '--web_port', '-wp',
        dest='web_port',
        type=int, nargs='?',
    )

    player_parser = mode_parsers.add_parser('player')
    player_parser.add_argument(
        '--rcc_host', '-rh',
        dest='rcc_host', type=str,
        default=None, required=True,
    )
    player_parser.add_argument(
        '--rcc_port', '-rp',
        dest='rcc_port',
        type=int, nargs='?',
    )
    player_parser.add_argument(
        '--web_host', '-wh',
        dest='web_host', type=str,
        default=None, nargs='?',
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

    args = parser.parse_args()
    instance = CLASSES[args.mode](
        **{i: v for i, v in args.__dict__.items() if v}
    )
    try:
        instance.communicate()
    except KeyboardInterrupt:
        pass
    finally:
        del instance
