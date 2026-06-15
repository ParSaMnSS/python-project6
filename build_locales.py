import os
import struct


# Parse a .po file into a dictionary of msgid -> msgstr.
def parse_po(path):
    entries = {}
    msgid = None
    msgstr = None
    target = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("msgid "):
                if msgid is not None and msgstr is not None:
                    entries[msgid] = msgstr
                msgid = unquote(line[6:])
                msgstr = None
                target = "id"
            elif line.startswith("msgstr "):
                msgstr = unquote(line[7:])
                target = "str"
            elif line.startswith('"'):
                if target == "id":
                    msgid += unquote(line)
                elif target == "str":
                    msgstr += unquote(line)
        if msgid is not None and msgstr is not None:
            entries[msgid] = msgstr
    return entries


# Remove the surrounding quotes from a .po string token.
def unquote(text):
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text.replace("\\n", "\n").replace('\\"', '"')


# Write a GNU MO file from the entries dictionary.
def write_mo(entries, path):
    keys = sorted(entries.keys())
    offsets = []
    ids = b""
    strs = b""
    for key in keys:
        value = entries[key]
        key_bytes = key.encode("utf-8")
        value_bytes = value.encode("utf-8")
        offsets.append((len(ids), len(key_bytes), len(strs), len(value_bytes)))
        ids += key_bytes + b"\x00"
        strs += value_bytes + b"\x00"

    count = len(keys)
    key_table_offset = 7 * 4
    value_table_offset = key_table_offset + count * 8
    ids_offset = value_table_offset + count * 8
    strs_offset = ids_offset + len(ids)

    key_table = b""
    value_table = b""
    for o1, l1, o2, l2 in offsets:
        key_table += struct.pack("II", l1, ids_offset + o1)
        value_table += struct.pack("II", l2, strs_offset + o2)

    # MO header with the GNU magic number.
    header = struct.pack("Iiiiiii", 0x950412DE, 0, count, key_table_offset, value_table_offset, 0, 0)

    with open(path, "wb") as f:
        f.write(header + key_table + value_table + ids + strs)


if __name__ == "__main__":
    # Compile each language .po into a .mo.
    for lang in ["en", "tr"]:
        folder = os.path.join("locales", lang, "LC_MESSAGES")
        po_path = os.path.join(folder, "messages.po")
        mo_path = os.path.join(folder, "messages.mo")
        entries = parse_po(po_path)
        write_mo(entries, mo_path)
        print(f"Compiled {mo_path}")
