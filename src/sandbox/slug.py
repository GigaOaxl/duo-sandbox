import re


def slug(text: str) -> str:
    """Wandelt einen gegebenen Text in einen URL-Slug um."""
    if not text:
        return ""

    # Umlaute und scharfes S ersetzen
    replacements = {
        "ä": "ae",
        "Ä": "ae",
        "ö": "oe",
        "Ö": "oe",
        "ü": "ue",
        "Ü": "ue",
        "ß": "ss",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)

    # In Kleinbuchstaben umwandeln
    text = text.lower()

    # Alle Zeichen, die nicht a-z oder 0-9 sind, durch Bindestrich ersetzen
    text = re.sub(r"[^a-z0-9]+", "-", text)

    # Bindestriche am Anfang und Ende entfernen
    text = text.strip("-")

    # Auf maximal 100 Zeichen kürzen
    text = text[:100]

    # Nach dem Kürzen sicherstellen, dass kein Bindestrich am Ende steht
    text = text.rstrip("-")

    return text
