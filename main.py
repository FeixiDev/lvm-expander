import argparse
from control import LVMExtend


def main():
    parser = argparse.ArgumentParser(description='LVM Extend Tool')
    parser.add_argument('-v', '--version', action='version', version='v1.0.0')
    args = parser.parse_args()

    if not vars(args):
        LVMExtend().extend_lvm()


if __name__ == '__main__':
    main()
