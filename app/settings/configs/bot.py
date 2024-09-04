from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    """Creates the TgBot object from environment variables."""

    token: str

    @staticmethod
    def from_env(env: Env):
        """Creates the TgBot object from environment variables."""
        token = env.str("BOT_TOKEN")
        return TgBot(token=token)
