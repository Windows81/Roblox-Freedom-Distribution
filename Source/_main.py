import launcher.subparsers.main
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    launcher.subparsers.main.process(parser)
