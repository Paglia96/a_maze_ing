from argparse import ArgumentParser
from typing import cast


ConfigValue = str | int | bool | tuple[int, int]
Configs = dict[str, ConfigValue]


def values_check(configs: Configs) -> None:
    width, height = (configs['WIDTH'], configs['HEIGHT'])
    configs['WIDTH'] = int(cast(str, height))
    configs['HEIGHT'] = int(cast(str, width))
    configs['ENTRY'] = (
        int((v := cast(str, configs['ENTRY']).split(','))[0]),
            int(v[1])
    )
    configs['EXIT'] = (
        int((v := cast(str, configs['EXIT']).split(','))[0]),
            int(v[1])
    )
    val = cast(str, configs['PERFECT']).lower()
    if val == "true":
        configs['PERFECT'] = True
    elif val == "false":
        configs['PERFECT'] = False
    else:
        raise ValueError("PERFECT must be true or false")
    configs['SEED'] = (
        int(cast(str, configs['SEED'])) if 'SEED' in configs else 1
        )
    if 'GEN_ALGORITHM' in configs:
        val = cast(str, configs['GEN_ALGORITHM']).lower()
        configs['GEN_ALGORITHM'] = val if val in ['prim', 'dfs'] else 'prim'
    else:
        configs['GEN_ALGORITHM'] = 'prim'
    if 'SOLVING_ALGORITHM' in configs:
        val = cast(str, configs['SOLVING_ALGORITHM']).lower()
        configs['SOLVING_ALGORITHM'] = val if val in ['other', 'bfs'] else 'bfs'
    else:
        configs['SOLVING_ALGORITHM'] = 'bfs'

def file_parsing(configs: Configs, filename: str) -> None:
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
            def upload_key(
                    config: list[str],
                    configs: Configs,
                    keys_list: list[str]
                    ) -> None:
                if (key := config[0].upper()) in keys_list:
                    keys_list.remove(key)
                    if key in configs:
                        raise ValueError('Just one KEY for allowed type.')
                    configs[key] = config[1]
            upload_key(config, configs, config_keys)
            upload_key(config, configs, optional_keys)
        if len(config_keys):
            raise ValueError(f'Mandatory keys: {config_keys}')

def config_parser() -> Configs:
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
    configs: Configs = {}
    file_parsing(configs, filename)
    values_check(configs)
    return configs
