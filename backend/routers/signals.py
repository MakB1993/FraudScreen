from fastapi import APIRouter

from backend.schemas import SignalDefinitionResponse
from backend.signals.signal_registry import get_all_signal_definitions, get_allowed_operators 

# FastAPI can serialize a dataclass such as SignalDefinition into JSON

router = APIRouter(
    prefix="/signals",
    tags=["signals"],
)


@router.get("",
            response_model=dict[str, SignalDefinitionResponse],
            )
def get_signals(): #build the response from the registry. adding allowed_operators to the response for each signal based on its data_type
    signal_definitions = get_all_signal_definitions()

    response = {}

    for signal_key, definition in signal_definitions.items():
        response[signal_key] = {
            "display_name": definition.display_name,
            "data_type": definition.data_type,
            "category": definition.category,
            "uses_window": definition.uses_window,
            "description": definition.description,
            "allowed_operators": list(
                get_allowed_operators(signal_key)
            ),
        }

    return response