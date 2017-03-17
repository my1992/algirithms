import re


def re_search1():
    patterns = ['this', 'that']
    text = 'Does this text match the pattern?'
    for pattern in patterns:
        print('Looking for "%s" in "%s" ->' % (pattern, text))
        if re.search(pattern, text):
            print('found a match!')
        else:
            print('no match')


def re_search2():
    # re.search()方法能从任意位置开始查找，re.match()只能从字符串的开头进行匹配
    pattern = 'this'
    text = 'Does this text match the pattern?'
    match = re.match(pattern, text)
    s = match.start()
    e = match.end()

    print('Found "%s" in "%s" from %d to %d ("%s")' %
          (match.re.pattern, match.string, s, e, text[s:e]))


def re_compile():
    regexes = [re.compile(p) for p in ['this', 'that']]
    text = 'Does this text match the pattern?'
    for regex in regexes:
        print('Looking for "%s" in "%s" ->' % (regex.pattern, text))
        if regex.search(text):
            print('found a match')
        else:
            print('no match')


def re_findall():
    text = 'abbaaabbbbaaaaa'
    pattern = 'ab'
    for match in re.findall(pattern, text):
        print('Found "%s"' % match)


def re_finditer():
    text = 'abbaaabbbbaaaaa'
    pattern = 'ab'
    for match in re.finditer(pattern, text):
        s = match.start()
        e = match.end()
        print('Found "%s" at %d:%d' % (text[s:e], s, e))


def test_patterns(text, pattens=None):
    # Show the character positions and input text
    if pattens is None:
        pattens = []
    print()
    print(' '.join(str(i / 10 or ' ') for i in range(len(text))))
    print(' '.join(str(i % 10) for i in range(len(text))))
    print(text)

    # Look for each pattern in the text and print the results
    for patten in pattens:
        print()
        print('Matching "%s"' % patten)
        for match in re.finditer(patten, text):
            s = match.start()
            e = match.end()
            print(' %d : %d = "%s"' % (s, e - 1, text[s:e]))
    return


def re_repetition(text, pattens=None):
    """
    * 表示pattern重复0次或者多次
    + 表示pattern至少出现一次
    ? 表示pattern出现0次或者出现一次
    {m} 用在pattern后面，m表示pattern应该重复的次数
    {m,n} 用在pattern后面，m表示pattern应该出现的最小次数，n表示pattern应该出现的最大次数
    {m,} 用在pattern后面，m表示pattern至少应该出现m次，无最大次限制

    # 贪婪模式匹配：匹配满足条件的最长的子串
    ['ab*',  # a followed by zero or more b
      'ab+',  # a followed by one or more b
      'ab?',  # a followed by zero or one b
      'ab{3}',  # a followed by three b
      'ab{2,3}',  # a followed by two to three b
      ]

    # 非贪婪模式：通过增加一个?来关闭贪婪模式，匹配满足条件的最短的子串
    [ 'ab*?',     # a followed by zero or more b
        'ab+?',     # a followed by one or more b
        'ab??',     # a followed by zero or one b
        'ab{3}?',   # a followed by three b
        'ab{2,3}?', # a followed by two to three b
        ]

    # 字符集合
    [ '[ab]',    # either a or b
        'a[ab]+',  # a followed by one or more a or b
        'a[ab]+?', # a followed by one or more a or b, not greedy
        ]

    # 排除：^
    [ '[^-. ]+',  # sequences without -, ., or space
        ]

    #
    [ '[a-z]+',      # sequences of lower case letters
        '[A-Z]+',      # sequences of upper case letters
        '[a-zA-Z]+',   # sequences of lower or upper case letters
        '[A-Z][a-z]+', # one upper case letter followed by lower case letters
        ]

    # .
    [ 'a.',   # a followed by any one character
        'b.',   # b followed by any one character
        'a.*b', # a followed by anything, ending in b
        'a.*?b', # a followed by anything, ending in b
        ]

    # 转义码
    \d	a digit
    \D	a non-digit
    \s	whitespace (tab, space, newline, etc.)
    \S	non-whitespace
    \w	alphanumeric
    \W	non-alphanumeric
    [ r'\d+', # sequence of digits
        r'\D+', # sequence of non-digits
        r'\s+', # sequence of whitespace
        r'\S+', # sequence of non-whitespace
        r'\w+', # alphanumeric characters
        r'\W+', # non-alphanumeric
        ]

    # 类似转义码的字符匹配
    [r'\\d\+',
       r'\\D\+',
       r'\\s\+',
       r'\\S\+',
       r'\\w\+',
       r'\\W\+',
       ]

    # Anchoring （锚定）
    [r'^\w+',  # word at start of string
       r'\A\w+',  # word at start of string
       r'\w+\S*$',  # word at end of string, with optional punctuation
       r'\w+\S*\Z',  # word at end of string, with optional punctuation
       r'\w*t\w*',  # word containing 't'
       r'\bt\w+',  # 't' at start of word
       r'\w+t\b',  # 't' at end of word
       r'\Bt\B',  # 't', not start or end of word
       ]
    :param text:
    :param pattens:
    :return:
    """
    if pattens is None:
        pattens = []
    test_patterns(text, pattens)


if __name__ == '__main__':
    re_repetition('This is some text -- with punctuation.',
                  [r'^\w+',  # word at start of string
                   r'\A\w+',  # word at start of string
                   r'\w+\S*$',  # word at end of string, with optional punctuation
                   r'\w+\S*\Z',  # word at end of string, with optional punctuation
                   r'\w*t\w*',  # word containing 't'
                   r'\bt\w+',  # 't' at start of word
                   r'\w+t\b',  # 't' at end of word
                   r'\Bt\B',  # 't', not start or end of word
                   ])
