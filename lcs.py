import numpy as np


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


def increasing_son_series(data):
    """
    查找一个数据的最长递增子集
    :param data:
    :return:
    """
    f = np.zeros(len(data))  # 存放当前索引位置上以它为七点可能存在的最长子序列个数
    max_index = -1
    max_len = -1

    for i in range(len(data)-1, -1, -1):
        f[i] = 1
        if i == len(data) - 1:
            continue
        for j in range(i+1, len(data)):
            if data[i] < data[j] and f[i] <= f[j]:
                f[i] = f[j] + 1
        if f[i] > max_len:
            max_len = f[i]
            max_index = i

    for i in range(max_index, len(data)):
        if f[i] == max_len:
            print(data[i])
            max_len -= 1


# if __name__ == '__main__':
#     data = [3, 18, 7, 14, 10, 12, 23, 41, 16, 24]
#     increasing_son_series(data)

if __name__ == '__main__':
    s1 = 'ascdgfawe'
    s2 = 'cdvfggfaw'
    lcs(s1, s2)
