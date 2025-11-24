
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from flask import Flask, render_template_string, request

GREEK_ALLOWED = re.compile(r"^[\u0370-\u03FF\u1F00-\u1FFF\s.,;:!¡¿?()\[\]{}\"'«»-–—…·]*$")

app = Flask(__name__)

# --- Mapping logic for Greek Reverse ---
greek_reverse_map = {
    "Α": 24, "Β": 23, "Γ": 22, "Δ": 21, "Ε": 20, "Ζ": 19, "Η": 18, "Θ": 17,
    "Ι": 16, "Κ": 15, "Λ": 14, "Μ": 13, "Ν": 12, "Ξ": 11, "Ο": 10, "Π": 9,
    "Ρ": 8, "Σ": 7, "Τ": 6, "Υ": 5, "Φ": 4, "Χ": 3, "Ψ": 2, "Ω": 1
}

greek_normal_map = {
    "Α": 1,  "Β": 2,  "Γ": 3,  "Δ": 4,  "Ε": 5,  "Ζ": 6,  "Η": 7,  "Θ": 8,
    "Ι": 9,  "Κ": 10, "Λ": 11, "Μ": 12, "Ν": 13, "Ξ": 14, "Ο": 15, "Π": 16,
    "Ρ": 17, "Σ": 18, "Τ": 19, "Υ": 20, "Φ": 21, "Χ": 22, "Ψ": 23, "Ω": 24
}

lower_to_upper_map = {
    "α": "Α", "ά": "Α", "β": "Β", "γ": "Γ", "δ": "Δ", "ε": "Ε", "έ": "Ε",
    "ζ": "Ζ", "η": "Η", "ή": "Η", "θ": "Θ", "ι": "Ι", "ί": "Ι", "κ": "Κ",
    "λ": "Λ", "μ": "Μ", "ν": "Ν", "ξ": "Ξ", "ο": "Ο", "ό": "Ο", "π": "Π",
    "ρ": "Ρ", "σ": "Σ", "ς": "Σ", "τ": "Τ", "υ": "Υ", "ύ": "Υ",
    "φ": "Φ", "χ": "Χ", "ψ": "Ψ", "ω": "Ω", "ώ": "Ω"
}

greek_morse = {
    "Α": ".-", "Β": "-...", "Γ": "--.", "Δ": "-..", "Ε": ".", "Ζ": "--..", "Η": "....",
    "Θ": "-.-.", "Ι": "..", "Κ": "-.-", "Λ": ".-..", "Μ": "--", "Ν": "-.", "Ξ": "-..-",
    "Ο": "---", "Π": ".--.", "Ρ": ".-.", "Σ": "...", "Τ": "-", "Υ": "-.--", "Φ": "..-.",
    "Χ": "----", "Ψ": "--.-", "Ω": ".--"
}

greek_morse_music = {
    "Α": "♩♬", "Β": "♬♩♩♩", "Γ": "--.", "Δ": "♬♩♩", "Ε": "♩", "Ζ": "♬♬♩♩",
    "Η": "♩♩♩♩", "Θ": "♬♩♬♩", "Ι": "♩♩", "Κ": "♬♩♬", "Λ": "♩♬♩♩", "Μ": "♬♬",
    "Ν": "♬♩", "Ξ": "♬♩♩♬", "Ο": "♬♬♬", "Π": "♩♬♬♩", "Ρ": "♩♬♩", "Σ": "♩♩♩",
    "Τ": "♬", "Υ": "♬♩♬♬", "Φ": "♩♩♬♩", "Χ": "♬♬♬♬", "Ψ": "♬♬♩♬", "Ω": "♩♬♬"
}

greek_words = {
    "Α": "ΑΣΤΡΙΤΗ", "Β": "ΒΟΓΔΑΝΟΣ", "Γ": "ΓΕΜΙΣΤΑ", "Δ": "ΔΙΑΣ",
    "Ε": "ΕΝΩΜΟΤΙΑ", "Ζ": "ΖΠ", "Η": "ΗΤΑΝ", "Θ": "ΘΕΑ", "Ι": "ΙΣΚΙΟΣ",
    "Κ": "ΚΑΛΛΙΣΤΩ", "Λ": "ΛΑΙΜΟΣ", "Μ": "ΜΟΝΑΑ", "Ν": "ΝΕΟΣ", "Ξ": "ΞΕΝΟΣ",
    "Ο": "ΟΜΑΔΑ", "Π": "ΠΛΟΥΤΩΝΑΣ", "Ρ": "ΡΑΨΩΔΙΑ", "Σ": "ΣΩΖΟΠΟΛΗ",
    "Τ": "ΣΤΕΛΕΧΟΣ", "Υ": "ΥΠΕΝΩΜΟΤΑΡΧΗΣ", "Φ": "ΦΑΓΟΥΡΑ", "Χ": "ΧΑΖΕΥΩ",
    "Ψ": "ΨΩΝΙΑ", "Ω": "ΩΡΑ"
}

greek_to_elements = {
    "Α": "H",   "Β": "He",  "Γ": "Li",  "Δ": "Be",  "Ε": "B",   "Ζ": "C",   "Η": "N",
    "Θ": "O",   "Ι": "F",   "Κ": "Ne",  "Λ": "Na",  "Μ": "Mg",  "Ν": "Al",  "Ξ": "Si",
    "Ο": "P",   "Π": "S",   "Ρ": "Cl",  "Σ": "Ar",  "Τ": "K",   "Υ": "Ca",  "Φ": "Sc",
    "Χ": "Ti",  "Ψ": "V",   "Ω": "Cr"
}

greek_hieroglyphs = {
    "Α": "𓀀", "Β": "𓀁", "Γ": "𓀂", "Δ": "𓀃", "Ε": "𓀄", "Ζ": "𓀅", "Η": "𓀆", "Θ": "𓀇",
    "Ι": "𓀈", "Κ": "𓀉", "Λ": "𓀊", "Μ": "𓀋", "Ν": "𓀌", "Ξ": "𓀍", "Ο": "𓀎", "Π": "𓀏",
    "Ρ": "𓀐", "Σ": "𓀑", "Τ": "𓀒", "Υ": "𓀓", "Φ": "𓀔", "Χ": "𓀕", "Ψ": "𓀖", "Ω": "𓀗"
}

def ensure_greek_only(text: str):
    if not GREEK_ALLOWED.match(text):
        raise ValueError("Μη επιτρεπόμενοι λατινικοί χαρακτήρες.")

def encode_text(text: str, mapping: dict) -> str:
    ensure_greek_only(text)
    transformed = []
    for char in text:
        char_upper = lower_to_upper_map.get(char, char)
        num = mapping.get(char_upper, char)
        transformed.append(str(num))
    return "/".join(transformed)

def greek_caesar(text: str, shift: int = 3) -> str:
    ensure_greek_only(text)
    greek_letters = [
        "Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", "Ι", "Κ", "Λ", "Μ",
        "Ν", "Ξ", "Ο", "Π", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω"
    ]
    transformed = []
    for char in text:
        char_upper = lower_to_upper_map.get(char, char)
        if char_upper in greek_letters:
            idx = greek_letters.index(char_upper)
            new_idx = (idx + shift) % 24
            transformed.append(greek_letters[new_idx])
        else:
            transformed.append(char)
    return "".join(transformed)

def greek_to_morse(text: str) -> str:
    ensure_greek_only(text)
    transformed = []
    for char in text:
        char_upper = lower_to_upper_map.get(char, char)
        code = greek_morse.get(char_upper, char)  # Keep punctuation and spaces
        transformed.append(code)
    return "/".join(transformed)

def greek_to_music_morse(text: str) -> str:
    ensure_greek_only(text)
    transformed = []
    for char in text:
        char_upper = lower_to_upper_map.get(char, char)
        code = greek_morse_music.get(char_upper, char)  # Keep punctuation and spaces
        transformed.append(code)
    return "/".join(transformed)

def greek_to_words(text: str) -> str:
    ensure_greek_only(text)
    transformed = []
    for char in text:
        char_upper = lower_to_upper_map.get(char, char)
        word = greek_words.get(char_upper, char)  # Preserve punctuation & spaces
        transformed.append(word)
    return " ".join(transformed)

def greek_to_elements_encoder(text: str) -> str:
    ensure_greek_only(text)
    transformed = []
    for char in text:
        char_upper = lower_to_upper_map.get(char, char)
        element = greek_to_elements.get(char_upper, char)  # Preserve punctuation & spaces
        transformed.append(element)
    return "/".join(transformed)

def greek_to_hieroglyphs(text: str) -> str:
    ensure_greek_only(text)
    transformed = []
    for char in text:
        char_upper = lower_to_upper_map.get(char, char)
        glyph = greek_hieroglyphs.get(char_upper, char)  # Keep punctuation & spaces
        transformed.append(glyph)
    return "".join(transformed)

# --- Encoding options ---
encodings = {
    "Αριθμητικό 1-24": lambda t: encode_text(t, greek_normal_map),
    "Αριθμητικό 24-1": lambda t: encode_text(t, greek_reverse_map),
    "Mετατόπιση +3 Caesar Cipher": lambda t: greek_caesar(t, shift=3),
    "Morse": greek_to_morse,
    "Morse σε Μουσική": greek_to_music_morse,
    "Λέξεις": greek_to_words,
    "Στοιχεία Περιοδικού Πίνακα": greek_to_elements_encoder,
    "Ιερογλυφικά": greek_to_hieroglyphs
}

# --- Flask routes ---
HTML_TEMPLATE = """
<!doctype html>
<html lang="el">
<head>
    <meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>⚜️ 7η Ομάδα Εξοχής ⚜️</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #1f1f1f;
            color: #eee;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            justify-content: center;
            align-items: center;
        }
        
        h1 {
            color: #f0a500;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 1em;
        }
        
        form {
            display: flex;
            flex-direction: column;
            width: 90%;
            max-width: 600px;
            text-align: center;
            justify-content: center;
            align-items: center;
        }
        
        label {
            font-weight: bold;
            margin-top: 1em;
            margin-bottom: 0.5em;
            font-size: 1.5em;            
        }
        
        textarea, select, input[type=submit], button.copy-btn {
            width: 100%;
            padding: 0.7rem;
            font-size: 1rem;
            border-radius: 5px;
            border: 1px solid #444;
            background: #2b2b2b;
            color: #eee;
            transition: border 0.2s, background 0.2s;
            text-align: center;
        }
        
        textarea, select, .output {
            width: 90%;
            max-width: 600px;
            min-width: 250px;
            #text-align: center;
        }

        textarea:focus, select:focus {
            border-color: #f0a500;
            outline: none;
            background: #333;
        }
        
        input[type=submit] {
            padding: 0.7em;
            margin-top: 1.5em;
            font-size: 1.1em;
            border-radius: 5px;
            border: none;
            background: #f0a500;
            color: #1f1f1f;
            cursor: pointer;
            transition: background 0.2s;
            align: center;
        }
        
        input[type=submit]:hover {
            background: #ffaa00;
        }
        
        .output-container {
            margin-top: 1.5em;
            display: flex;
            justify-content: center;
            flex-direction: column;
            gap: 0.5em;
            width: 100%;
        }
        
        .output {
            font-weight: bold;
            font-size: 1.2em;
            word-wrap: break-word;
            background: #2b2b2b;
            padding: 0.8em;
            border-radius: 5px;
            text-align: center;
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .button-group {
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }
        
        button.copy-btn, input[type=submit] {
            width: 150px;          /* fixed width */
            min-width: 120px;      /* ensures they don’t shrink too much on small screens */
            max-width: 180px;      /* optional limit for large screens */
            padding: 0.7em 1em;    /* internal spacing */
            font-size: 1em;        /* consistent text size */
            border-radius: 5px;
            border: none;
            background: #f0a500;
            color: #1f1f1f;
            cursor: pointer;
            transition: background 0.2s;
            text-align: center;    /* center text inside button */
        }
        
        button.copy-btn:hover {
            background: #ffaa00;
        }
        
        @media (max-width: 400px) {
            textarea, select, input[type=submit], button.copy-btn {
                font-size: 0.9rem;
                padding: 0.5rem;
                width: 120px;
            }
        }
    </style>
</head>
<body>
    <h1>⚜️ <br>7η Ομάδα Ποσκόπων <br>Εξοχής</h1>
    <form method="post">
        <label for="input_text">Βάλε κείμενο προς κωδικοποίηση:</label>
        <textarea id="input_text" name="input_text" rows="5" placeholder="Πληκτρολόγησε ή επικόλλησε κείμενο εδώ...">{{ input_text|default('') }}</textarea>        

        <label for="encoding_type">Επέλεξε τύπο κωδικοποίησης:</label>
        <select id="encoding_type" name="encoding_type">
            {% for name in encodings.keys() %}
            <option value="{{ name }}" {% if encoding_type==name %}selected{% endif %}>{{ name }}</option>
            {% endfor %}
        </select>

        <input type="submit" value="Κωδικοποίηση">
    </form>

    {% if encoded %}
    <div class="output-container">
        <div class="output" id="encoded">{{ encoded }}</div>
        <div class="button-group">
            <button class="copy-btn" onclick="copyToClipboard()">Αντιγραφή</button>
            <button class="copy-btn" onclick="clearAll()">Καθαρισμός</button>
        </div>
    </div>
    <script>
        function copyToClipboard() {
            const text = document.getElementById('encoded').innerText;
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(text).then(() => {
                    alert('Το κείμενο αντιγράφηκε!');
                }, (err) => {
                    alert('Αποτυχία αντιγραφής: ' + err);
                });
            } else {
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                document.body.appendChild(textarea);
                textarea.focus();
                textarea.select();
                try {
                    document.execCommand('copy');
                    alert('Το κείμενο αντιγράφηκε!');
                } catch (err) {
                    alert('Αποτυχία αντιγραφής: ' + err);
                }
                document.body.removeChild(textarea);
            }
        }

        function clearAll() {
            document.getElementById('encoded').innerText = '';
            document.getElementById('input_text').value = '';
        }
    </script>
    {% endif %}
    {% if error_msg %}
    <div style="color: red; margin-top: 10px; text-align: center;">
    F_CK!! Only thing i need is U<br>Μόνο ελληνικά 😎
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    input_text = ""
    encoded = None
    encoding_type = "Αριθμητικό 24-1"
    error_msg = None
    
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        encoding_type = request.form.get("encoding_type", encoding_type)

        func = encodings.get(encoding_type)

        try:
            if func:
                encoded = func(input_text)
        except ValueError as e:
            error_msg = str(e)

    return render_template_string(
        HTML_TEMPLATE,
        input_text=input_text,
        encoded=encoded,
        error_msg=error_msg,
        encodings=encodings,
        encoding_type=encoding_type
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
