import launcher.subparsers._main
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    launcher.subparsers._main.process(parser)
