from encoders import encode, decode


def test_roundtrip_numeric():
    s = 'ΑΒΓ'
    enc = encode('Αριθμητικό 1-24', s)
    dec = decode('Αριθμητικό 1-24', enc)
    assert dec == 'ΑΒΓ'


def test_caesar():
    s = 'ΑΒΓ'
    enc = encode('Mετατόπιση +3 Caesar Cipher', s)
    dec = decode('Mετατόπιση +3 Caesar Cipher', enc)
    assert dec == 'ΑΒΓ'
