from dataclasses import dataclass


@dataclass(frozen=True) #frozen: immutable config
class SignalWindowConfig:
    ip_velocity: int = 15
    device_velocity: int = 15
    card_velocity: int = 15

    customer_velocity: int = 15
    session_velocity: int = 15

    relationship_counts: int = 15
    country_velocity: int = 15
    decline_velocity: int = 15