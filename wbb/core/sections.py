def section(
    title: str, body: dict, indent: int = 2, underline: bool = True
) -> str:
    text = f"**--{title}**--:\n" if underline else f"**{title}**:\n"
    for key, value in body.items():
        if not isinstance(value, list):
            text += f"{' ' * indent}`→` **{key}:** `{value}`\n"
        else:
            text += f"{' ' * indent}`→` **{key}:** {value[0]}\n"
    return text
