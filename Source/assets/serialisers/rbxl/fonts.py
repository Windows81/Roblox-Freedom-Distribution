from . import _logic
import re

# https://github.com/MaximumADHD/Roblox-File-Format/blob/d44a590bb2e814f08edae91e7ef3e20fb09416e1/Utility/FontUtility.cs#L30
FONTS = {
    b'Fondamento.json\x90\x01\x00': 0x19,
    b'Merriweather.json\x90\x01\x00': 0x21,
    b'SourceSansPro.json\x90\x01\x01': 0x06,
    b'Ubuntu.json\x90\x01\x00': 0x2d,
    b'JosefinSans.json\x90\x01\x00': 0x1d,
    b'JosefinSans.json\xbc\x02\x00': 0x1d,
    b'PatrickHand.json\x90\x01\x00': 0x25,
    b'Bangers.json\x90\x01\x00': 0x16,
    b'Inconsolata.json\x90\x01\x00': 0x0a,
    b'FredokaOne.json\x90\x01\x00': 0x1a,
    b'FredokaOne.json\xf4\x01\x00': 0x1a,
    b'SourceSansPro.json\xbc\x02\x00': 0x04,
    b'GothamSSm.json\x90\x01\x00': 0x11,
    b'SourceSansPro.json\x2c\x01\x00': 0x05,
    b'GrenzeGotisch.json\x90\x01\x00': 0x1b,
    b'Arial.json\xbc\x02\x00': 0x02,
    b'TitilliumWeb.json\x90\x01\x00': 0x2c,
    b'Guru.json\x90\x01\x00': 0x08,
    b'Michroma.json\x90\x01\x00': 0x22,
    b'RobotoCondensed.json\x90\x01\x00': 0x28,
    b'ComicNeueAngular.json\x90\x01\x00': 0x09,
    b'Creepster.json\x90\x01\x00': 0x17,
    b'GothamSSm.json\xbc\x02\x00': 0x13,
    b'AccanthisADFStd.json\x90\x01\x00': 0x07,
    b'LegacyArial.json\x90\x01\x00': 0x00,
    b'RobotoMono.json\x90\x01\x00': 0x29,
    b'PressStart2P.json\x90\x01\x00': 0x0d,
    b'SourceSansPro.json\x90\x01\x00': 0x03,
    b'Sarpanch.json\x90\x01\x00': 0x2a,
    b'DenkOne.json\x90\x01\x00': 0x18,
    b'IndieFlower.json\x90\x01\x00': 0x1c,
    b'SourceSansPro.jsonX\x02\x00': 0x10,
    b'RomanAntique.json\x90\x01\x00': 0x0f,
    b'AmaticSC.json\x90\x01\x00': 0x15,
    b'Kalam.json\x90\x01\x00': 0x1f,
    b'PermanentMarker.json\x90\x01\x00': 0x26,
    b'Roboto.json\x90\x01\x00': 0x27,
    b'LuckiestGuy.json\x90\x01\x00': 0x20,
    b'Arial.json\x90\x01\x00': 0x01,
    b'Nunito.json\x90\x01\x00': 0x23,
    b'HighwayGothic.json\x90\x01\x00': 0x0b,
    b'Oswald.json\x90\x01\x00': 0x24,
    b'SpecialElite.json\x90\x01\x00': 0x2b,
    b'SpecialElite.json\xf4\x01\x00': 0x2b,
    b'GothamSSm.json\x84\x03\x00': 0x14,
    b'GothamSSm.json\xf4\x01\x00': 0x12,
    b'Balthazar.json\x90\x01\x00': 0x0e,
    b'Zekton.json\x90\x01\x00': 0x0c,
    b'Jura.json\x90\x01\x00': 0x1e,
}


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    old_prop_name = b'\x08\x00\x00\x00FontFace\x20'
    new_prop_name = b'\x04\x00\x00\x00Font\x12'
    if not info.chunk_data.startswith(old_prop_name, _logic.INT_SIZE):
        return None

    class_id = info.chunk_data[0:_logic.INT_SIZE]
    chunk_values = info.chunk_data[len(class_id + old_prop_name):]

    new_values = bytes(
        FONTS.get(m.group(1), 0x03)
        for m in re.finditer(
            br'[\x10-\xff]\x00\x00\x00rbxasset://fonts/families/([^\.]+\.json.{3})' +
            br'(?:[\x10-\xff]\x00\x00\x00rbxasset://fonts/(.+?)\..tf|\x00\x00\x00\x00)',
            chunk_values,
        )
    )

    # Fonts (just like all enums) are stored as an INTERLEAVED array of big-endian `uint32`s.
    # Why the large string of zeroes?  We're taking advantage of the fact that `Enum.Font` never goes above 256.
    # Because integers here are big-endian, we put the least significant bytes at the end.
    return b''.join([
        class_id,
        new_prop_name,
        b'\x00' * len(new_values) * 3,
        new_values,
    ])
