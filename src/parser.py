from argparse import ArgumentParser

def config_parser():
    """Parse and validate the maze configuration file.

    The configuration file path is read from the command-line arguments.
    Each non-empty line must contain a single ``KEY=VALUE`` pair.
    Lines beginning with ``#`` and inline comments are ignored.

    Returns:
        dict: A dictionary containing the parsed configuration values.
            ``WIDTH`` and ``HEIGHT`` are integers.
            ``ENTRY`` and ``EXIT`` are coordinate tuples.
            ``PERFECT`` is a boolean.

    Raises:
        SystemExit: if the number of given arguments is different from 1.
        ValueError: If a configuration line is malformed or a mandatory
            configuration key is missing.
        FileNotFoundError: If the specified configuration file does not exist.
        PermissionError: If the configuration file cannot be opened.
    """
    parser = ArgumentParser(
            description='Receives the maze configuration settings as an argument'
            )
    parser.add_argument('filename', help='file path')
    arg = parser.parse_args()
    filename = arg.filename
    configs: dict = {}
    with open(filename, 'r') as f:
        config_keys: list[str] = [
                'WIDTH',
                'HEIGHT',
                'ENTRY',
                'EXIT',
                'OUTPUT_FILE',
                'PERFECT'
                ]
        optional_keys: list[str] = [
                'SEED',
                'GEN_ALGORITHM',
                'SOLVING_ALGORITHM'
                ]
        for line in f:
            if line.startswith('#') or line == '\n':
                continue
            elif '#' in line:
                line = line.split('#')[0] 
            config = line.split('=')
            if len(config) != 2:
                raise ValueError(
                        "The configuration file must contain one ‘KEY=VALUE‘ pair per line."
                        )
            config[0] = config[0].strip()
            config[1] = config[1][:-1].strip()  # remove ending \n e spaces
            def upload_key(config, configs, keys_list):
                if (key := config[0].upper()) in keys_list:
                    keys_list.remove(key)
                    if key in configs:
                        raise ValueError('Just one KEY for allowed type.')
                    configs[key] = config[1]
            upload_key(config, configs, config_keys)
            upload_key(config, configs, optional_keys)
        if len(config_keys):
            raise ValueError(f'Mandatory keys: {config_keys}')
    configs['WIDTH'] = int(configs['WIDTH'])
    configs['HEIGHT'] = int(configs['HEIGHT'])
    configs['ENTRY'] = (int((v := configs['ENTRY'].split(','))[0]), int(v[1]))
    configs['EXIT'] = (int((v := configs['EXIT'].split(','))[0]), int(v[1]))
    configs['PERFECT'] = bool(configs['PERFECT'])
    configs['SEED'] = int(configs['SEED']) if 'SEED' in configs else 1
    if 'GEN_ALGORITHM' in configs:
        value = configs['GEN_ALGORITHM'].lower()
        configs['GEN_ALGORITHM'] = value if value in ['prim', 'dfs'] else 'prim'
    else:
        configs['GEN_ALGORITHM'] = 'prim'
    if 'SOLVING_ALGORITHM' in configs:
        value = configs['SOLVING_ALGORITHM'].lower()
        configs['SOLVING_ALGORITHM'] = value if value in ['prim', 'bfs'] else 'prim'
    else:
        configs['SOLVING_ALGORITHM'] = 'prim'
    return configs
