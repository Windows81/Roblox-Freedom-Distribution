from .logic import LaunchMode, min_version
import launcher.studio
import argparse


@min_version(LaunchMode.STUDIO)
def _(parser: argparse.ArgumentParser, sub_parser: argparse.ArgumentParser):
    sub_parser.add_argument(
        dest='args', nargs='*',
    )
    args = parser.parse_args()
    instance = launcher.studio.Studio(
        **{i: v for i, v in args.__dict__.items() if v}
    )
    try:
        instance.communicate()
    except KeyboardInterrupt:
        pass
    finally:
        del instance
