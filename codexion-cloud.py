import argparse
from cloud import init


def main():
    parser = argparse.ArgumentParser(description="Codexion Cloud CLI")
    subparsers = parser.add_subparsers(dest="cloud", help="Available commands")

    # Register the 'init' command
    init.add_subparser(subparsers)

    # Add more commands here later









    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)  # ✅ Pass the entire args to the function
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
