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
    pass


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
    pass


if __name__ == '__main__':

    message = input()
    code = encode(message)
    received_code = transmit(code)
    received_message = decode(received_code)

    print(f'Mensagem a ser transmitida:\n\t{message}')
    print(f'Mensagem recebida:\n\t{received_message}')
