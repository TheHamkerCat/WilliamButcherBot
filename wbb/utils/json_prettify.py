"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


async def json_object_prettify(objecc):
    dicc = objecc.__dict__
    output = ""
    for key, value in dicc.items():
        if key in ["pinned_message", "photo", "_", "_client"]:
            continue
        output += f"**{key}:** `{value}`\n"
    return output


async def json_prettify(data):
    output = ""
    try:
        for key, value in data.items():
            output += f"**{str(key).capitalize()}:** `{value}`\n"
    except Exception:
        for datas in data:
            for key, value in datas.items():
                output += f"**{str(key).capitalize()}:** `{value}`\n"
            output += "------------------------\n"
    return output
