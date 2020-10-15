def copy_list(lst: list):
    new_list = lst[:]
    return new_list


def copy_2d_list(lst: list):
    new_list = []
    for item in lst:
        new_list.append(copy_list(item))
    return new_list


def clone_list(li1):
    li_copy = li1.copy()
    return li_copy


def copy_dict(dct: dict):
    new_dict = {}
    for key in dct:
        new_dict[key] = dct[key]
    return new_dict
