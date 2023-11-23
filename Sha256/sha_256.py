
import struct
import io

# fmt: off
IV = [
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
]

ROUND_CONSTANTS = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
]
# fmt: on


### Building Blocks

"""
def add32(*args):
    return sum(args) % (2**32)


def rightrotate32(x, n):
    assert x < 2**32, "x is too large. Did you use + instead of add32 somewhere?"
    right_part = x >> n
    left_part = x << (32 - n)
    return add32(left_part, right_part)
"""

def right_rotate(value, amount):
    return ((value >> amount) | (value << (32 - amount))) & 0xffffffff

def process_chunk(chunk, h0, h1, h2, h3, h4, h5, h6, h7):
    assert len(chunk) == 64
    w = [0] * 64
    for i in range(16):
        w[i] = struct.unpack(">I", chunk[i*4:i*4 + 4])[0]

    for i in range(16, 64):
        s0 = right_rotate(w[i - 15], 7) ^ right_rotate(w[i - 15], 18) ^ (w[i - 15] >> 3)
        s1 = right_rotate(w[i - 2], 17) ^ right_rotate(w[i - 2], 19) ^ (w[i - 2] >> 10)
        w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xffffffff

    a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

    for i in range(64):
        s1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
        ch = (e & f) ^ (~e & g)
        temp1 = (h + s1 + ch + ROUND_CONSTANTS[i] + w[i]) & 0xffffffff
        s0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (s0 + maj) & 0xffffffff

        h = g
        g = f
        f = e
        e = (d + temp1) & 0xffffffff
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xffffffff

    return (h0 + a) & 0xffffffff, (h1 + b) & 0xffffffff, (h2 + c) & 0xffffffff, \
           (h3 + d) & 0xffffffff, (h4 + e) & 0xffffffff, (h5 + f) & 0xffffffff, \
           (h6 + g) & 0xffffffff, (h7 + h) & 0xffffffff


class Sha256Hash(object):
    name = 'python-sha256'
    digest_size = 32
    block_size = 64

    def __init__(self, initialState=None, lengthProcessed=0):
        if initialState is None:
            self._h = (
                0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
                0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
            )
        else:
            self._h = tuple(int.from_bytes(bytes.fromhex(initialState[i:i+8]), 'big') for i in range(0, 64, 8))

        self._unprocessed = b''
        self._message_byte_length = lengthProcessed

    def update(self, arg):
        if isinstance(arg, (bytes, bytearray)):
            arg = io.BytesIO(arg)

        chunk = self._unprocessed + arg.read(self.block_size - len(self._unprocessed))
        while len(chunk) == self.block_size:
            self._h = process_chunk(chunk, *self._h)
            self._message_byte_length += self.block_size
            chunk = arg.read(self.block_size)

        self._unprocessed = chunk
        return self

    def digest(self):
        message = self._unprocessed
        message_byte_length = self._message_byte_length + len(message)

        message += b'\x80'
        message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)
        message_bit_length = message_byte_length * 8
        message += struct.pack(b'>Q', message_bit_length)

        h = process_chunk(message[:64], *self._h)
        if len(message) == 64:
            return b''.join(struct.pack(b'>I', h_i) for h_i in h)
        return b''.join(struct.pack(b'>I', h_i) for h_i in process_chunk(message[64:], *h))

    def hexdigest(self):
        return ''.join('%08x' % i for i in self._produce_digest())

    def _produce_digest(self):
        return struct.unpack('>IIIIIIII', self.digest())
    
    
### The Message Schedule
"""
def little_sigma0(word):
    return rightrotate32(word, 7) ^ rightrotate32(word, 18) ^ (word >> 3)


def little_sigma1(word):
    return rightrotate32(word, 17) ^ rightrotate32(word, 19) ^ (word >> 10)


def message_schedule_array(block):
    assert len(block) == 64
    w = []
    for i in range(16):
        assert i == len(w)
        w.append(int.from_bytes(block[4 * i : 4 * i + 4], "big"))
    for i in range(16, 64):
        s0 = little_sigma0(w[i - 15])
        s1 = little_sigma1(w[i - 2])
        w.append(add32(w[i - 16], s0, w[i - 7], s1))
    return w


### The Round Function


def big_sigma0(word):
    return rightrotate32(word, 2) ^ rightrotate32(word, 13) ^ rightrotate32(word, 22)


def big_sigma1(word):
    return rightrotate32(word, 6) ^ rightrotate32(word, 11) ^ rightrotate32(word, 25)


def choice(x, y, z):
    return (x & y) ^ (~x & z)


def majority(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def round(state, round_constant, schedule_word):
    S1 = big_sigma1(state[4])
    ch = choice(state[4], state[5], state[6])
    temp1 = add32(state[7], S1, ch, round_constant, schedule_word)
    S0 = big_sigma0(state[0])
    maj = majority(state[0], state[1], state[2])
    temp2 = add32(S0, maj)
    return [
        add32(temp1, temp2),
        state[0],
        state[1],
        state[2],
        add32(state[3], temp1),
        state[4],
        state[5],
        state[6],
    ]


### The Compression Function


def compress_block(input_state_words, block):
    w = message_schedule_array(block)
    state_words = input_state_words
    for round_number in range(64):
        round_constant = ROUND_CONSTANTS[round_number]
        schedule_word = w[round_number]
        state_words = round(state_words, round_constant, schedule_word)
    return [add32(x, y) for x, y in zip(input_state_words, state_words)]


### Padding


def padding_bytes(input_len):
    remainder_bytes = (input_len + 8) % 64
    filler_bytes = 64 - remainder_bytes
    zero_bytes = filler_bytes - 1
    encoded_bit_length = (8 * input_len).to_bytes(8, "big")
    return b"\x80" + b"\0" * zero_bytes + encoded_bit_length


### The Hash Function


def sha256(message):
    padded = message + padding_bytes(len(message))
    assert len(padded) % 64 == 0
    state_words = IV
    i = 0
    while i < len(padded):
        block = padded[i : i + 64]
        state_words = compress_block(state_words, block)
        i += 64
    return b"".join(x.to_bytes(4, "big") for x in state_words)
"""
