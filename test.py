from main import encode, transmit, decode
from random import choice

import argparse
import pandas as pd
import string


def test(message_len: int, n: int):

    result = {
        'sent': [],
        'received': [],
        'differences': [],
    }

    for _ in range(n):
        message = ''.join(
            choice(string.ascii_letters + string.digits)
            for _ in range(message_len)
        )
        result['sent'].append(message)

        code = encode(message)
        received_code = transmit(code, 1)
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


if __name__ == '__main__':

    # creates an argparse object to parse command line option
    parser = argparse.ArgumentParser()
    parser.add_argument('message_len',
                        help='Length of messages',
                        type=int)
    parser.add_argument('n',
                        help='Number of repetitions',
                        type=int)

    # waits for command line input
    # (proceeds only if it is validated against the options set before)
    args = parser.parse_args()

    pct = test(args.message_len, args.n)[-1]

    print(f'Error percentage: {100*pct:.2f}%')
