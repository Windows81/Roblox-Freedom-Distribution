import versions
import argparse
import studio
import server
import player
import uwamp

CLASSES = {
    'studio': studio.Studio,
    'server': server.Server,
    'player': player.Player,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=list(CLASSES))
    parser.add_argument('--version', '-v', choices=versions.VERSION_MAP)
    args = parser.parse_args()

    version = versions.VERSION_MAP[args.version]
    CLASSES[args.mode](version=version)
