from dataclasses import dataclass


@dataclass
class AuditHubContext:
    base_url: str
    oidc_configuration_url: str
    oidc_client_id: str
    oidc_client_secret: str
