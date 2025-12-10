from typing import Dict, Callable
import re

# --- Validation patterns ---
GREEK_ALLOWED = re.compile(r"^[\u0370-\u03FF\u1F00-\u1FFF\s.,;:!¡¿?()\[\]{}\"'«»-–—…·]*$")

# --- Maps (uppercase) ---
GREEK_LETTERS = [
    "Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", "Ι", "Κ", "Λ", "Μ",
    "Ν", "Ξ", "Ο", "Π", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω"
]

GREEK_NORMAL_MAP = {ch: i + 1 for i, ch in enumerate(GREEK_LETTERS)}
GREEK_REVERSE_MAP = {ch: len(GREEK_LETTERS) - i for i, ch in enumerate(GREEK_LETTERS)}

LOWER_TO_UPPER_MAP = {
    "α": "Α", "ά": "Α", "β": "Β", "γ": "Γ", "δ": "Δ", "ε": "Ε", "έ": "Ε",
    "ζ": "Ζ", "η": "Η", "ή": "Η", "θ": "Θ", "ι": "Ι", "ί": "Ι", "κ": "Κ",
    "λ": "Λ", "μ": "Μ", "ν": "Ν", "ξ": "Ξ", "ο": "Ο", "ό": "Ο", "π": "Π",
    "ρ": "Ρ", "σ": "Σ", "ς": "Σ", "τ": "Τ", "υ": "Υ", "ύ": "Υ",
    "φ": "Φ", "χ": "Χ", "ψ": "Ψ", "ω": "Ω", "ώ": "Ω"
}

# Morse-like mappings
GREEK_MORSE = {
    "Α": ".-", "Β": "-...", "Γ": "--.", "Δ": "-..", "Ε": ".", "Ζ": "--..", "Η": "....",
    "Θ": "-.-.", "Ι": "..", "Κ": "-.-", "Λ": ".-..", "Μ": "--", "Ν": "-.", "Ξ": "-..-",
    "Ο": "---", "Π": ".--.", "Ρ": ".-.", "Σ": "...", "Τ": "-", "Υ": "-.--", "Φ": "..-.",
    "Χ": "----", "Ψ": "--.-", "Ω": ".--"
}

GREEK_MORSE_MUSIC = {
    "Α": "♩♬", "Β": "♬♩♩♩", "Γ": "--.", "Δ": "♬♩♩", "Ε": "♩", "Ζ": "♬♬♩♩",
    "Η": "♩♩♩♩", "Θ": "♬♩♬♩", "Ι": "♩♩", "Κ": "♬♩♬", "Λ": "♩♬♩♩", "Μ": "♬♬",
    "Ν": "♬♩", "Ξ": "♬♩♩♬", "Ο": "♬♬♬", "Π": "♩♬♬♩", "Ρ": "♩♬♩", "Σ": "♩♩♩",
    "Τ": "♬", "Υ": "♬♩♬♬", "Φ": "♩♩♬♩", "Χ": "♬♬♬♬", "Ψ": "♬♬♩♬", "Ω": "♩♬♬"
}

# Word mapping (example words)
GREEK_WORDS = {
    "Α": "ΑΣΤΡΙΤΗ", "Β": "ΒΟΓΔΑΝΟΣ", "Γ": "ΓΕΜΙΣΤΑ", "Δ": "ΔΙΑΣ",
    "Ε": "ΕΝΩΜΟΤΙΑ", "Ζ": "ΖΠ", "Η": "ΗΤΑΝ", "Θ": "ΘΕΑ", "Ι": "ΙΣΚΙΟΣ",
    "Κ": "ΚΑΛΛΙΣΤΩ", "Λ": "ΛΑΙΜΟΣ", "Μ": "ΜΟΝΑΑ", "Ν": "ΝΕΟΣ", "Ξ": "ΞΕΝΟΣ",
    "Ο": "ΟΜΑΔΑ", "Π": "ΠΛΟΥΤΩΝΑΣ", "Ρ": "ΡΑΨΩΔΙΑ", "Σ": "ΣΩΖΟΠΟΛΗ",
    "Τ": "ΣΤΕΛΕΧΟΣ", "Υ": "ΥΠΕΝΩΜΟΤΑΡΧΗΣ", "Φ": "ΦΑΓΟΥΡΑ", "Χ": "ΧΑΖΕΥΩ",
    "Ψ": "ΨΩΝΙΑ", "Ω": "ΩΡΑ"
}

# Element mapping (short symbols)
GREEK_TO_ELEMENTS = {
    "Α": "H",   "Β": "He",  "Γ": "Li",  "Δ": "Be",  "Ε": "B",   "Ζ": "C",   "Η": "N",
    "Θ": "O",   "Ι": "F",   "Κ": "Ne",  "Λ": "Na",  "Μ": "Mg",  "Ν": "Al",  "Ξ": "Si",
    "Ο": "P",   "Π": "S",   "Ρ": "Cl",  "Σ": "Ar",  "Τ": "K",   "Υ": "Ca",  "Φ": "Sc",
    "Χ": "Ti",  "Ψ": "V",   "Ω": "Cr"
}

# Hieroglyphs (one-to-one)
GREEK_HIEROGLYPHS = {
    "Α": "𓀀", "Β": "𓀁", "Γ": "𓀂", "Δ": "𓀃", "Ε": "𓀄", "Ζ": "𓀅", "Η": "𓀆", "Θ": "𓀇",
    "Ι": "𓀈", "Κ": "𓀉", "Λ": "𓀊", "Μ": "𓀋", "Ν": "𓀌", "Ξ": "𓀍", "Ο": "𓀎", "Π": "𓀏",
    "Ρ": "𓀐", "Σ": "𓀑", "Τ": "𓀒", "Υ": "𓀓", "Φ": "𓀔", "Χ": "𓀕", "Ψ": "𓀖", "Ω": "𓀗"
}

# --- Reverse maps for decoding ---
NUM_TO_GREEK_NORMAL = {str(v): k for k, v in GREEK_NORMAL_MAP.items()}
NUM_TO_GREEK_REVERSE = {str(v): k for k, v in GREEK_REVERSE_MAP.items()}

MORSE_TO_GREEK = {v: k for k, v in GREEK_MORSE.items()}
MUSIC_TO_GREEK = {v: k for k, v in GREEK_MORSE_MUSIC.items()}

WORDS_TO_GREEK = {v: k for k, v in GREEK_WORDS.items()}
ELEMENT_TO_GREEK = {v: k for k, v in GREEK_TO_ELEMENTS.items()}
HIERO_TO_GREEK = {v: k for k, v in GREEK_HIEROGLYPHS.items()}

# --- Helpers ---

def ensure_greek_only(text: str):
    if not GREEK_ALLOWED.match(text):
        raise ValueError("F_CK!! Only thing i need is U! <br> Μόνο ελληνικοί χαρακτήρες.")


def normalize_upper(char: str) -> str:
    return LOWER_TO_UPPER_MAP.get(char, char)

# --- Encoders ---

def encode_numeric(text: str, reverse: bool = False) -> str:
    ensure_greek_only(text)
    mapping = GREEK_REVERSE_MAP if reverse else GREEK_NORMAL_MAP
    out = []
    for ch in text:
        up = normalize_upper(ch)
        out.append(str(mapping.get(up, ch)))
    return "/".join(out)


def decode_numeric(text: str, reverse: bool = False) -> str:
    # Accept numbers separated by '/' or whitespace
    mapping = NUM_TO_GREEK_REVERSE if reverse else NUM_TO_GREEK_NORMAL
    tokens = re.split(r"[\s/]+", text.strip())
    out = []
    for tok in tokens:
        if tok == '':
            continue
        out.append(mapping.get(tok, tok))
    return "".join(out)


def greek_caesar_encode(text: str, shift: int = 3) -> str:
    ensure_greek_only(text)
    out = []
    for ch in text:
        up = normalize_upper(ch)
        if up in GREEK_LETTERS:
            idx = GREEK_LETTERS.index(up)
            out.append(GREEK_LETTERS[(idx + shift) % len(GREEK_LETTERS)])
        else:
            out.append(ch)
    return "".join(out)


def greek_caesar_decode(text: str, shift: int = 3) -> str:
    # decoding is encoding with negative shift
    return greek_caesar_encode(text, shift=-shift)


def greek_to_morse_encode(text: str) -> str:
    ensure_greek_only(text)
    out = []
    for ch in text:
        up = normalize_upper(ch)
        out.append(GREEK_MORSE.get(up, ch))
    return "/".join(out)


def greek_to_morse_decode(text: str) -> str:
    tokens = re.split(r"[\s/]+", text.strip())
    out = []
    for tok in tokens:
        if tok == '':
            continue
        out.append(MORSE_TO_GREEK.get(tok, tok))
    return "".join(out)


def greek_to_music_encode(text: str) -> str:
    ensure_greek_only(text)
    out = []
    for ch in text:
        up = normalize_upper(ch)
        out.append(GREEK_MORSE_MUSIC.get(up, ch))
    return "/".join(out)


def greek_to_music_decode(text: str) -> str:
    tokens = re.split(r"[\s/]+", text.strip())
    out = []
    for tok in tokens:
        if tok == '':
            continue
        out.append(MUSIC_TO_GREEK.get(tok, tok))
    return "".join(out)


def greek_to_words_encode(text: str) -> str:
    ensure_greek_only(text)
    out = []
    for ch in text:
        up = normalize_upper(ch)
        out.append(GREEK_WORDS.get(up, ch))
    return " ".join(out)


def greek_to_words_decode(text: str) -> str:
    tokens = re.split(r"\s+", text.strip())
    out = []
    for tok in tokens:
        if tok == '':
            continue
        out.append(WORDS_TO_GREEK.get(tok, tok))
    return "".join(out)


def greek_to_elements_encode(text: str) -> str:
    ensure_greek_only(text)
    out = []
    for ch in text:
        up = normalize_upper(ch)
        out.append(GREEK_TO_ELEMENTS.get(up, ch))
    return "/".join(out)


def greek_to_elements_decode(text: str) -> str:
    tokens = re.split(r"[\s/]+", text.strip())
    out = []
    for tok in tokens:
        if tok == '':
            continue
        out.append(ELEMENT_TO_GREEK.get(tok, tok))
    return "".join(out)


def greek_to_hieroglyphs_encode(text: str) -> str:
    ensure_greek_only(text)
    out = []
    for ch in text:
        up = normalize_upper(ch)
        out.append(GREEK_HIEROGLYPHS.get(up, ch))
    return "".join(out)


def greek_to_hieroglyphs_decode(text: str) -> str:
    out = []
    for ch in text:
        out.append(HIERO_TO_GREEK.get(ch, ch))
    return "".join(out)

# --- Unified registry ---
ENCODERS: Dict[str, Callable[[str], str]] = {
    "Αριθμητικό 1-24": lambda t: encode_numeric(t, reverse=False),
    "Αριθμητικό 24-1": lambda t: encode_numeric(t, reverse=True),
    "Mετατόπιση +3 Caesar Cipher": lambda t: greek_caesar_encode(t, shift=3),
    "Morse": greek_to_morse_encode,
    "Morse σε Μουσική": greek_to_music_encode,
    "Λέξεις": greek_to_words_encode,
    "Στοιχεία Περιοδικού Πίνακα": greek_to_elements_encode,
    "Ιερογλυφικά": greek_to_hieroglyphs_encode
}

DECODERS: Dict[str, Callable[[str], str]] = {
    "Αριθμητικό 1-24": lambda t: decode_numeric(t, reverse=False),
    "Αριθμητικό 24-1": lambda t: decode_numeric(t, reverse=True),
    "Mετατόπιση +3 Caesar Cipher": lambda t: greek_caesar_decode(t, shift=3),
    "Morse": greek_to_morse_decode,
    "Morse σε Μουσική": greek_to_music_decode,
    "Λέξεις": greek_to_words_decode,
    "Στοιχεία Περιοδικού Πίνακα": greek_to_elements_decode,
    "Ιερογλυφικά": greek_to_hieroglyphs_decode
}

# Convenience wrapper

def encode(encoding_name: str, text: str) -> str:
    fn = ENCODERS.get(encoding_name)
    if not fn:
        raise ValueError(f"Unknown encoding: {encoding_name}")
    return fn(text)


def decode(encoding_name: str, text: str) -> str:
    fn = DECODERS.get(encoding_name)
    if not fn:
        raise ValueError(f"Unknown decoding: {encoding_name}")
    return fn(text)


