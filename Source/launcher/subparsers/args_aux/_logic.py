import argparse


class action:
    def process(self) -> None:
        raise NotImplementedError()

    @staticmethod
    def add_args(
        parser: argparse.ArgumentParser,
        sub_parser: argparse.ArgumentParser,
    ) -> None:
        raise NotImplementedError()

    @staticmethod
    def serialise_args(
        parser: argparse.ArgumentParser,
        args_ns: argparse.Namespace,
    ) -> None:
        raise NotImplementedError()
