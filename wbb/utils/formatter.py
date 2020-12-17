import time, math


def time_formatter(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
    )
    return tmp[:-2]


def time_parser(start, end):
    time_end = end - start
    month = time_end // 2678400
    days = time_end // 86400
    hours = time_end // 3600 % 24
    minutes = time_end // 60 % 60
    seconds = time_end % 60
    times = ""
    if month:
        times += "{} month, ".format(month)
    if days:
        times += "{} days, ".format(days)
    if hours:
        times += "{} hours, ".format(hours)
    if minutes:
        times += "{} minutes, ".format(minutes)
    if seconds:
        times += "{} seconds".format(seconds)
    if times == "":
        times = "{} miliseconds".format(time_end)
    return times


def time_parser_int(time_end):
    month = time_end // 2678400
    days = time_end // 86400
    hours = time_end // 3600 % 24
    minutes = time_end // 60 % 60
    seconds = time_end % 60
    times = ""
    if month:
        times += "{} month, ".format(month)
    if days:
        times += "{} days, ".format(days)
    if hours:
        times += "{} hours, ".format(hours)
    if minutes:
        times += "{} minutes, ".format(minutes)
    if seconds:
        times += "{} seconds".format(seconds)
    if times == "":
        times = "{} miliseconds".format(time_end)
    return times[:-2] if times[-2:] == ", " else times


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def extract_time(time_val):
    if not any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        return False
    unit = time_val[-1]
    time_num = time_val[:-1]  # type: str
    if not time_num.isdigit():
        return False

    if unit == "d":
        bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
    elif unit == "h":
        bantime = int(time.time() + int(time_num) * 60 * 60)
    elif unit == "m":
        bantime = int(time.time() + int(time_num) * 60)
    else:
        return False
    return bantime


def make_time(time_val):
    if int(time_val) == 0:
        return "0"
    if int(time_val) <= 3600:
        bantime = str(int(time_val / 60)) + "m"
    elif int(time_val) >= 3600 and time_val <= 86400:
        bantime = str(int(time_val / 60 / 60)) + "h"
    elif int(time_val) >= 86400:
        bantime = str(int(time_val / 24 / 60 / 60)) + "d"
    return bantime


def extract_time_set(time_val):
    if not any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        return False
    unit = time_val[-1]
    time_num = time_val[:-1]  # type: str
    if not time_num.isdigit():
        return False

    if unit == "d":
        bantime = int(int(time_num) * 24 * 60 * 60)
    elif unit == "h":
        bantime = int(int(time_num) * 60 * 60)
    elif unit == "m":
        bantime = int(int(time_num) * 60)
    else:
        return False
    return bantime


def escape_invalid_curly_brackets(text, valids):  # sourcery skip
    new_text = ""
    idx = 0
    while idx < len(text):
        if text[idx] == "{":
            if idx + 1 < len(text) and text[idx + 1] == "{":
                idx += 2
                new_text += "{{{{"
                continue
            else:
                success = False
                for v in valids:
                    if text[idx:].startswith("{" + v + "}"):
                        success = True
                        break
                    if success:
                        new_text += text[idx : idx + len(v) + 2]
                        idx += len(v) + 2
                        continue
                    else:
                        new_text += "{{"

        elif text[idx] == "}":
            if idx + 1 < len(text) and text[idx + 1] == "}":
                idx += 2
                new_text += "}}}}"
                continue
            else:
                new_text += "}}"

        else:
            new_text += text[idx]
        idx += 1

    return new_text
