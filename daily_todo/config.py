from dataclasses import dataclass, field
from typing import Optional, Dict
import yaml


@dataclass
class EmailSettings:
    smtp_server: str = ""
    smtp_port: int = 0
    username: str = ""
    password: str = ""
    recipient: str = ""


@dataclass
class UserConfig:
    google_credentials_path: Optional[str] = None
    trello_api_key: Optional[str] = None
    trello_token: Optional[str] = None
    asana_access_token: Optional[str] = None
    openai_api_key: Optional[str] = None
    delivery_time: str = "08:00"
    email: EmailSettings = field(default_factory=EmailSettings)
    other_settings: Dict[str, str] = field(default_factory=dict)


CONFIG_PATH = "config.yml"


def load_config(path: str = CONFIG_PATH) -> UserConfig:
    """Load configuration from a YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)
    email = EmailSettings(**data.get("email", {}))
    return UserConfig(email=email, **{k: v for k, v in data.items() if k != "email"})
