# Solution for
# /r/dailyprogrammer Challenge:298[easy] with bonus


def get_pairs(text):
    stack = list()
    for i, ch in enumerate(text):
        if ch == '(':
            stack.append(i)
        if ch == ')':
            yield (stack.pop(), i)


def remove_extra(text):
    pairs = list(get_pairs(text))
    dups_list = [x for x in pairs if (x[0]-1, x[1]+1) in pairs]
    null_list = [x for x in pairs if (x[1]-x[0]) == 1]
    bad = [x for pair in dups_list + null_list for x in pair]
    return ''.join(x for i, x in enumerate(text) if i not in bad)


if __name__ == '__main__':
    testcases = ['((a((bc)(de)))f)', '(((zbcd)(((e)fg))))', 'ab((c))',
                 '()', '((fgh()()()))', '()(abc())']
    for t in testcases:
        print(remove_extra(t))
