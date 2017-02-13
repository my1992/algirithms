def lcs(s1, s2):
    """
    查找两个字符串的最长公共子串
    :param s1:
    :param s2:
    :return:
    """
    l1 = len(s1)
    l2 = len(s2)

    common_strings = set()
    for i in range(l1):
        for j in range(l2):
            tmp = ''
            if s1[i] == s2[j]:
                tmp += s1[i]
                count = 1
                while i + count < l1 and j + count < l2:
                    if s1[i + count] == s2[j + count]:
                        tmp += s1[i + count]
                        count += 1
                    else:
                        break
            if len(tmp) > 0:
                common_strings.add(tmp)

    len_dict = {}
    for s in common_strings:
        len_dict[s] = len(s)

    sorted_result = sorted(len_dict.items(), key=lambda t: t[1], reverse=True)
    return sorted_result

if __name__ == '__main__':
    s1 = 'ascdgfawe'
    s2 = 'cdvfggfaw'
    lcs(s1, s2)
