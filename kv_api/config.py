import dataclasses

from environs import (
    Env,
)


@dataclasses.dataclass(frozen=True, slots=True)
class TarantoolConfig:
    """
    Configuration class for Tarantool database settings.

    This class contains the necessary configuration details to connect to
    a Tarantool database, such as the space name, host, and port.

    Attributes
    ----------
    space: str
        The name of the Tarantool space to use.
    host: str
        The hostname or IP address of the Tarantool server.
    port: int
        The port number on which the Tarantool server is listening.
    """
    space: str
    host: str
    port: int

    @staticmethod
    def from_env(env: Env) -> "TarantoolConfig":
        """
        Create a TarantoolConfig instance from environment variables.

        This method reads configuration values from environment variables
        using the provided Env instance and returns a TarantoolConfig object.

        Parameters
        ----------
        env: Env
            The Env instance used to access environment variables.

        Returns
        -------
        TarantoolConfig
            An instance of TarantoolConfig populated with values from environment variables.
        """
        space = env.str("TARANTOOL_SPACE", "example_space_5")
        host = env.str("TARANTOOL_HOST", "router")
        port = env.int("TARANTOOL_PORT", 3300)

        return TarantoolConfig(
            space=space,
            host=host,
            port=port,
        )


@dataclasses.dataclass(frozen=True, slots=True)
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes,
    providing a centralized point of access for all settings.

    Attributes
    ----------
    tarantool: TarantoolConfig
        Holds the settings specific to the tarantool
    """

    tarantool: TarantoolConfig


def load_config(path: str | None = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.

    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    env = Env()
    env.read_env(path)

    return Config(
        tarantool=TarantoolConfig.from_env(env),
    )
