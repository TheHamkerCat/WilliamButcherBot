async def json_object_prettify(objecc):
    dicc = objecc.__dict__
    output = ""
    for key , value in dicc.items():
        if key == "pinned_message" or key == "photo":
            continue
        output += f"**{key}:** `{value}`\n"
    return output

async def json_prettify(data):
    output = ""
    for key , value in data.items():
        output += f"**{key}:** `{value}`\n"
    return output
