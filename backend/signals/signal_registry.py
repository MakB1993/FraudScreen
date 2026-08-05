from dataclasses import fields

from backend.signals.signal_context import SignalContext


AVAILABLE_SIGNALS = {
    field.name
    for field in fields(SignalContext)
}