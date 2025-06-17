from . import _logic
import re

# https://github.com/MaximumADHD/Roblox-File-Format/blob/d44a590bb2e814f08edae91e7ef3e20fb09416e1/Utility/FontUtility.cs#L30
FONTS = {
    b'rbxasset://fonts/families/Fondamento.json\x90\x01\x00': 0x19,
    b'rbxasset://fonts/families/Merriweather.json\x90\x01\x00': 0x21,
    b'rbxasset://fonts/families/SourceSansPro.json\x90\x01\x01': 0x06,
    b'rbxasset://fonts/families/Ubuntu.json\x90\x01\x00': 0x2d,
    b'rbxasset://fonts/families/JosefinSans.json\x90\x01\x00': 0x1d,
    b'rbxasset://fonts/families/JosefinSans.json\xbc\x02\x00': 0x1d,
    b'rbxasset://fonts/families/PatrickHand.json\x90\x01\x00': 0x25,
    b'rbxasset://fonts/families/Bangers.json\x90\x01\x00': 0x16,
    b'rbxasset://fonts/families/Inconsolata.json\x90\x01\x00': 0x0a,
    b'rbxasset://fonts/families/FredokaOne.json\x90\x01\x00': 0x1a,
    b'rbxasset://fonts/families/FredokaOne.json\xf4\x01\x00': 0x1a,
    b'rbxasset://fonts/families/SourceSansPro.json\xbc\x02\x00': 0x04,
    b'rbxasset://fonts/families/GothamSSm.json\x90\x01\x00': 0x11,
    b'rbxasset://fonts/families/SourceSansPro.json\x2c\x01\x00': 0x05,
    b'rbxasset://fonts/families/GrenzeGotisch.json\x90\x01\x00': 0x1b,
    b'rbxasset://fonts/families/Arial.json\xbc\x02\x00': 0x02,
    b'rbxasset://fonts/families/TitilliumWeb.json\x90\x01\x00': 0x2c,
    b'rbxasset://fonts/families/Guru.json\x90\x01\x00': 0x08,
    b'rbxasset://fonts/families/Michroma.json\x90\x01\x00': 0x22,
    b'rbxasset://fonts/families/RobotoCondensed.json\x90\x01\x00': 0x28,
    b'rbxasset://fonts/families/ComicNeueAngular.json\x90\x01\x00': 0x09,
    b'rbxasset://fonts/families/Creepster.json\x90\x01\x00': 0x17,
    b'rbxasset://fonts/families/GothamSSm.json\xbc\x02\x00': 0x13,
    b'rbxasset://fonts/families/AccanthisADFStd.json\x90\x01\x00': 0x07,
    b'rbxasset://fonts/families/LegacyArial.json\x90\x01\x00': 0x00,
    b'rbxasset://fonts/families/RobotoMono.json\x90\x01\x00': 0x29,
    b'rbxasset://fonts/families/PressStart2P.json\x90\x01\x00': 0x0d,
    b'rbxasset://fonts/families/SourceSansPro.json\x90\x01\x00': 0x03,
    b'rbxasset://fonts/families/Sarpanch.json\x90\x01\x00': 0x2a,
    b'rbxasset://fonts/families/DenkOne.json\x90\x01\x00': 0x18,
    b'rbxasset://fonts/families/IndieFlower.json\x90\x01\x00': 0x1c,
    b'rbxasset://fonts/families/SourceSansPro.json\x58\x02\x00': 0x10,
    b'rbxasset://fonts/families/RomanAntique.json\x90\x01\x00': 0x0f,
    b'rbxasset://fonts/families/AmaticSC.json\x90\x01\x00': 0x15,
    b'rbxasset://fonts/families/Kalam.json\x90\x01\x00': 0x1f,
    b'rbxasset://fonts/families/PermanentMarker.json\x90\x01\x00': 0x26,
    b'rbxasset://fonts/families/Roboto.json\x90\x01\x00': 0x27,
    b'rbxasset://fonts/families/LuckiestGuy.json\x90\x01\x00': 0x20,
    b'rbxasset://fonts/families/Arial.json\x90\x01\x00': 0x01,
    b'rbxasset://fonts/families/Nunito.json\x90\x01\x00': 0x23,
    b'rbxasset://fonts/families/HighwayGothic.json\x90\x01\x00': 0x0b,
    b'rbxasset://fonts/families/Oswald.json\x90\x01\x00': 0x24,
    b'rbxasset://fonts/families/SpecialElite.json\x90\x01\x00': 0x2b,
    b'rbxasset://fonts/families/SpecialElite.json\xf4\x01\x00': 0x2b,
    b'rbxasset://fonts/families/GothamSSm.json\x84\x03\x00': 0x14,
    b'rbxasset://fonts/families/GothamSSm.json\xf4\x01\x00': 0x12,
    b'rbxasset://fonts/families/Balthazar.json\x90\x01\x00': 0x0e,
    b'rbxasset://fonts/families/Zekton.json\x90\x01\x00': 0x0c,
    b'rbxasset://fonts/families/Jura.json\x90\x01\x00': 0x1e,
}


def get_new_values(chunk_data: bytes) -> bytes:
    new_values: list[int] = []
    length = len(chunk_data)
    index = 0
    # https://github.com/RobloxAPI/spec/blob/master/formats/rbxl.md#font
    while index < length:
        family_len = int.from_bytes(
            chunk_data[index:index+_logic.INT_SIZE],
            'little',
        )
        font_beg = index + _logic.INT_SIZE
        font_end = font_beg + (family_len + 3)
        # The variable `font` contains all of `Family`, `Weight`, and `Style`.
        font = chunk_data[font_beg:font_end]
        index = font_end

        cache_len = int.from_bytes(
            chunk_data[index:index+_logic.INT_SIZE],
            'little',
        )
        cache_beg = index + _logic.INT_SIZE
        cache_end = cache_beg + cache_len
        index = cache_end

        new_values.append(FONTS.get(font, 0x03))
    return bytes(new_values)


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    old_prop_head = _logic.wrap_string(b'FontFace') + b'\x20'
    new_prop_head = _logic.wrap_string(b'Font') + b'\x12'
    if not info.chunk_data.startswith(old_prop_head, _logic.INT_SIZE):
        return None

    class_id = info.chunk_data[0:_logic.INT_SIZE]
    chunk_data = info.chunk_data[len(class_id + old_prop_head):]
    new_values = get_new_values(chunk_data)

    # Fonts (just like all enums) are stored as an INTERLEAVED array of big-endian `uint32`s.
    # Why the large string of zeroes?  We're taking advantage of the fact that `Enum.Font` never goes above 256.
    # Because integers here are big-endian, we put the least significant bytes at the end.
    return b''.join([
        class_id,
        new_prop_head,
        b'\x00' * len(new_values) * 3,
        new_values,
    ])
