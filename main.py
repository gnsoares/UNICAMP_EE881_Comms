#
# IMPORTS
#
import numpy as np

from graph import viterbi
from numpy.random import default_rng
from numpy.typing import ArrayLike


#
# CONSTANTS
#
ENCODING = 'ascii'
MEAN = 0
VARIANCE = 1


#
# CODE
#
def str_to_bits(str_: str) -> str:
    """
    """
    str_bytes = str_.encode(encoding=ENCODING, errors='replace')
    str_int = int(str_bytes.hex(), 16)
    return bin(str_int).lstrip('0b')


def encode(message: str) -> ArrayLike:
    """
    Encodes a string message into a codeword.

    Parameters
    ----------
    message: message to be encoded

    Returns
    ----------
    encoded codeword
    """
    # convert string to array of bits
    message_bin = str_to_bits(message)

    # initialize codeword
    code = []

    # encode message
    window = [1, 1, 1]
    for bit in map(int, message_bin):
        symbol = (2*bit-1)
        code.extend([
            window[0]*window[1]*symbol,
            window[1]*window[2]*symbol,
            window[0]*window[2]*symbol,
            window[0]*symbol,
            window[1]*symbol,
            window[2]*symbol,
        ])
        window.pop(0)
        window.append(symbol)

    # return codeword
    return np.array(code, dtype=np.float64)


def transmit(signal: ArrayLike) -> ArrayLike:
    """
    Transmits a signal over a channel with Aditive Gaussian White Noise.

    Parameters
    ----------
    signal: signal to be transmitted

    Returns
    ----------
    transmitted signal
    """
    rng = default_rng()
    noise = rng.normal(MEAN, np.sqrt(VARIANCE), signal.size)
    return signal + noise


def decode(word: ArrayLike) -> str:
    """
    Decodes a codeword into a string message.

    Parameters
    ----------
    word: codeword to be decoded

    Returns
    ----------
    decoded message
    """
    # decode bits
    message_bin = viterbi(word)[1]

    # convert message bits to string
    message_hex = hex(int(message_bin, 2)).lstrip('0x')
    if len(message_hex) % 2 != 0:
        message_hex = '0' + message_hex
    message = bytearray.fromhex(message_hex).decode(encoding=ENCODING,
                                                    errors='replace')

    # return decoded message
    return message


if __name__ == '__main__':

    message = input()
    code = encode(message)
    received_code = transmit(code)
    received_message = decode(received_code)

    print(f'Mensagem a ser transmitida:\n\t{message}')
    print(f'Mensagem recebida:\n\t{received_message}')
