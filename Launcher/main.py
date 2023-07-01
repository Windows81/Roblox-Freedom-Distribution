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
        metavar='place', dest='data',
        type=lambda n: open(n, 'rb'),
        default=None, nargs='?',
    )
    player_parser = mode_parsers.add_parser('player')

    try:
        args = parser.parse_args()
        c = CLASSES[args.mode](**args.__dict__)
        c.communicate()
    except KeyboardInterrupt:
        pass
