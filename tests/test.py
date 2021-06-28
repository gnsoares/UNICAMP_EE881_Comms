from main import encode, transmit, decode
from tests.random import ascii
from tests.random import emoji

import pandas as pd


METHODS = {
    'ascii': ascii,
    'emoji': emoji,
}


def test(message_len: int, n: int, method: str):

    result = {
        'sent': [],
        'received': [],
        'differences': [],
    }

    for _ in range(n):
        message = METHODS[method](message_len)
        result['sent'].append(message)

        code = encode(message)
        received_code = transmit(code)
        received_message = decode(received_code)
        result['received'].append(received_message)

        d = abs(message_len - len(received_message))
        for i in range(message_len):
            if i < len(received_message) and message[i] != received_message[i]:
                d += 1
        result['differences'].append(d)

        if n >= 100 and _ % (n//100) == 0:
            print('|', end='')
        else:
            print('|'*(100//n), end='')
    print()

    df = pd.DataFrame(result)
    mean = df['differences'].mean()
    pct = mean/message_len

    return df, mean, pct
