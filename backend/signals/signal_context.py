from dataclasses import dataclass

                    # @dataclass : if implementing metadata together
                    # class SignalContext:
                    #     ip_velocity: int = field(
                    #         metadata={
                    #             "display_name": "IP Velocity",
                    #             "category": "Velocity",
                    #             "uses_window": True,
                    #             "description": "...",
                    #         }
                    #     )
@dataclass
class SignalContext:
    amount: float
    ip_velocity: int
    device_velocity: int
    card_velocity: int
    new_device: bool
    new_card: bool
    new_ip_for_customer: bool
    distinct_customers_per_device: int
    distinct_cards_per_device: int
    distinct_customers_per_ip: int
    distinct_cards_per_ip: int
    customer_velocity: int
    session_velocity: int
    card_ip_country_mismatch: bool
    new_ip_country_for_customer: bool #has customer used ip country before
    new_card_country_for_customer: bool #has customer used card with same country before
    distinct_ip_countries_per_customer: int
    customer_decline_velocity: int
    card_decline_velocity: int
    ip_decline_velocity: int
    distinct_cards_per_session: int
    declines_per_session: int
    authorized_after_declines_in_session: bool
    distinct_devices_per_customer: int
    distinct_ips_per_customer: int