from argparse import ArgumentParser
from typing import cast


ConfigValue = str | int | bool | tuple[int, int] | float
Configs = dict[str, ConfigValue]


def values_check(configs: Configs) -> None:
    """Convert and validate the configuration values.
    Args:
        configs: The configuration dictionary.

    Raises:
        ValueError: If a configuration value is invalid
    """
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

    if (val := cast(str, configs["PERFECT"]).lower()) in ("true", "false"):
        configs["PERFECT"] = cast(bool, eval(val.capitalize()))
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
        configs["SOLVING_ALGORITHM"] = "bfs"


def file_parsing(configs: Configs, filename: str) -> None:
    """Read the configuration file and store its values.

    Args:
        configs: The configuration dictionary.
        filename: The configuration file path.

    Raises:
        ValueError: If the file has invalid or missing keys.
    """
    with open(filename, 'r') as f:
        config_keys: list[str] = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        ]
        optional_keys: list[str] = [
            "SEED", "GEN_ALGORITHM", "SOLVING_ALGORITHM"
            ]
        for line in f:
            if line.startswith("#") or line == "\n":
                continue
            elif "#" in line:
                line = line.split("#")[0]
            config = line.split("=")
            if len(config) != 2:
                raise ValueError(
                    "The configuration file must contain one "
                    "'KEY=VALUE' pair per line."
                )
            config[0] = config[0].strip()
            config[1] = config[1][:-1].strip()  # remove ending \n e spaces
            def upload_key(
                    config: list[str],
                    configs: Configs,
                    keys_list: list[str]
                    ) -> None:
                """Add a valid key to the configuration dictionary.

                Args:
                    config: The key and its value.
                    configs: The configuration dictionary.
                    keys_list: The list of allowed keys.

                Raises:
                    ValueError: If the key is already present.
                """
                if (key := config[0].upper()) in keys_list:
                    keys_list.remove(key)
                    if key in configs:
                        raise ValueError(
                            "Just one KEY for allowed type."
                            )
                    configs[key] = config[1]

            upload_key(config, configs, config_keys)
            upload_key(config, configs, optional_keys)
        if len(config_keys):
            raise ValueError(f"Mandatory keys: {config_keys}")


def config_parser() -> Configs:
    """Parse and validate the maze configuration file.

    The configuration file path is read from the command-line arguments.
    Each non-empty line must contain a single KEY=VALUE pair.
    Lines beginning with # and inline comments are ignored.

    Returns:
        dict: A dictionary containing the parsed configuration values or default ones.
            WIDTH and HEIGHT are integers.
            ENTRY and EXIT are coordinate tuples.
            OUTPUT_FILE is a string.
            PERFECT is a boolean.
            GEN_ALGORITHM and SOLVING_ALGORITHM are strings.
            SEED is an integer.

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
    parser.add_argument("filename", help="file path")
    filename = parser.parse_args().filename
    configs: Configs = {}
    file_parsing(configs, filename)
    values_check(configs)
    return configs
