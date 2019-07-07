
if __name__ == '__main__':
    import argparse
    from swagccg.src.make_client import main as make_client

    parser = argparse.ArgumentParser()
    parser.add_argument('--config-path', '-c', action='store', default='config.json')
    args = parser.parse_args()
    make_client(config_path=args.config_path)
