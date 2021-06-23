#
# IMPORTS
#
import numpy as np

from numpy.random import default_rng
from numpy.typing import ArrayLike


#
# CONSTANTS
#
MEAN = 0
VARIANCE = 1


#
# CODE
#
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
    message_bytes = message.encode(encoding='UTF-8', errors='replace')
    message_int = int(message_bytes.hex(), 16)
    message_bin = bin(message_int).lstrip('0b')

    # initialize codeword
    code = np.array([], dtype=np.float64)

    # TODO actually encode message
    for bit in message_bin:
        pass

    # return codeword
    return code


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
    # TODO actually decode message
    pass

    # convert message bits to string
    message_bin = str()
    message_hex = hex(int(message_bin, 2)).lstrip('0x')
    message = bytearray.fromhex(message_hex).decode(encoding='UTF-8',
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
