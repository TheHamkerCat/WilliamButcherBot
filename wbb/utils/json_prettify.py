async def json_object_prettify(objecc):
    dicc = objecc.__dict__
    output = ""
    for key, value in dicc.items():
        if key == "pinned_message" or key == "photo" \
                or key == "_" or key == "_client":
            continue
        output += f"**{key}:** `{value}`\n"
    return output


async def json_prettify(data):
    output = ""
    try:
        for key, value in data.items():
            output += f"**{key}:** `{value}`\n"
    except Exception:
        for datas in data:
            for key, value in datas.items():
                output += f"**{key}:** `{value}`\n"
            output += "------------------------\n"
    return output
