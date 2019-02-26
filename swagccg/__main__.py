
if __name__ == '__main__':
    import argparse
    from swagccg.src.make_client import main as make_client

    parser = argparse.ArgumentParser()
    parser.add_argument('--confi-path', '-c', action='store', default='confi.json')
    args = parser.parse_args()
    make_client(confi_path=args.confi_path)
