import hashlib, struct, sys, base58, json, binascii
from codaledgercli import schnorr

# whole version byte tables for coda
value_to_version_byte = {
        'user_command':                     b'\x17',
        'web_pipe':                         b'\x41',
        'data_hash':                        b'\x37',
        'proof':                            b'\x70',
        'signature':                        b'\x9a',
        'non_zero_curve_point':             b'\xce',
        'non_zero_curve_point_compressed':  b'\xcb',
        'random_oracle_base':               b'\x03',
        'private_key':                      b'\x5a',
        'user_command_memo':                b'\xa2',
        'receipt_chain_hash':               b'\x9d',
        'secret_box_byteswr':               b'\x02',
        'ledger_hash':                      b'\x63'
}

version_byte_to_value = {
        b'\x17': 'user_command',
        b'\x41': 'web_pipe',
        b'\x37': 'data_hash',
        b'\x70': 'proof',
        b'\x9a': 'signature',
        b'\xce': 'non_zero_curve_point',
        b'\xcb': 'non_zero_curve_point_compressed' ,
        b'\x03': 'random_oracle_base',
        b'\x5a': 'private_key',
        b'\xa2': 'user_command_memo',
        b'\x9d': 'receipt_chain_hash',
        b'\x02': 'secret_box_byteswr',
        b'\x63': 'ledger_hash'
}

def split(in_bytes, request):
    l = len(in_bytes)
    assert l//2 * 2 == l
    b0 = bytes(in_bytes[:l//2])
    b1 = bytes(in_bytes[l//2:])
    # convert bytes to int to check correct size
    int0 = int.from_bytes(b0, 'big')
    int1 = int.from_bytes(b1, 'big')
    if request == 'sig':
        assert int0 < schnorr.p and int1 < schnorr.n
    else:
        assert int0 < schnorr.p and int1 < schnorr.p
    # convert bytes to base58 encoded string
    bb0 = base58.b58encode(b0).decode("utf8")
    bb1 = base58.b58encode(b1).decode("utf8")
    return bb0, bb1

def sig_encode(bs):
    r, s = split(bs, 'sig')
    print(json.dumps({'status': 'Ok', 'field': r, 'scalar': s}))
    return

# versionbyte length = 1 byte
def pk_encode(bpk):
    x, y = split(bpk, 'pk')
    print(json.dumps({'status': 'Ok', 'x': x, 'y': y}))
    return

# b58_pk is version byte || sign bit || x coord
def pk_decode(b58_pk):
    bpk = base58.b58decode_check(b58_pk)
    vb = bytes([bpk[0]])
    assert vb == value_to_version_byte['non_zero_curve_point_compressed']
    sign_bit = bytes([bpk[-1]])
    pkx = bpk[3:-1]
    x = int.from_bytes(pkx, byteorder='little')
    pkx = x.to_bytes(96, byteorder='little')
    assert schnorr.is_curve_point(x) == True
    return sign_bit, pkx


"""
field elts:
  [ x_coord of receiver/delegate pubkey
  ]

bitstrings:
  [ sign_bit of receiver/delegate pubkey
  , tag bits
  , amount (8 bytes)
  , fee (8 bytes)
  , nonce (4 bytes)
  , valid-until (4 bytes)
  , memo (32 bytes)
  ]
"""

def txn_dict_to_bytes(txn_info):
    sign_bit, to = pk_decode(txn_info['to'])
    # change this to just two bits?
    tag_bits = bytes([1]) if txn_info['is_delegation'] == 'True' else bytes([0])
    amount  = txn_info['amount'].to_bytes(8, 'big')
    fee     = txn_info['fee'].to_bytes(8, 'big')
    nonce   = txn_info['nonce'].to_bytes(4, 'big')
    vu      = txn_info['valid_until'].to_bytes(4, 'big')
    memo    = bytes(txn_info['memo'], 'utf8')
    return to, sign_bit + tag_bits + amount + fee + nonce + vu + memo

def json_to_transaction(txn):
    data = json.loads(txn)
    for _, txn_info in data.items():
        return txn_dict_to_bytes(txn_info)

# INS_VERSION       0x01
# INS_PUBLIC_KEY    0x02
# INS_SIGN          0x04
# INS_HASH          0x08

def handle_txn_input(pkno, txn):
    to, msg = json_to_transaction(txn)
    apdu = b'\xE0'  # CLA byte
    apdu += b'\x04' # INS byte
    apdu += b'\x00' # P1 byte
    apdu += b'\x00' # P2 byte
    apdu += b'\x00' # LC byte
    apdu += struct.pack('<I', int(pkno)) # DATA bytes
    apdu += struct.pack("<96s", to)
    apdu += struct.pack("<96s", msg)
    return apdu

def handle_ints_input(pkno, msgx, msgm):
    to = int(msgx).to_bytes(96, byteorder='big')
    msg = int(msgm).to_bytes(96, byteorder='big')
    apdu = b'\xE0'  # CLA byte
    apdu += b'\x04' # INS byte
    apdu += b'\x00' # P1 byte
    apdu += b'\x00' # P2 byte
    apdu += b'\x00' # LC byte
    apdu += struct.pack('<I', int(pkno)) # DATA bytes
    apdu += struct.pack("<96s", to)
    apdu += struct.pack("<96s", msg)
    return apdu

def handle_txn_reply(reply):
    return sig_encode(reply)

def handle_pk_reply(pk):
    return pk_encode(pk)

def check_key(x, y):
    assert ((y*y) % schnorr.p == (x*x*x + x*schnorr.a + schnorr.b) % schnorr.p)

hex_keys = [b'0000f4fd0743422f322b44c02e217203b5ddf63d09d5fd5852f7115aeb513904a35dc4e8a41de21fc52440074f710d17624ba6862b4294d7e7ae95a861c93aa5c776d158fc29ad51c2b4d0e9c032be5d3077a04fe286b1190f194b5e9776a72f0000756d810cba0389484ebf6862334db6888cfa69a9bcb19168b89dc5b367bb7e12d0aa29eb5fae2fb09ebb49b636fd95ab0a583bcb4a8a3d6c5a398d5842abc28ae3e521e0fbe64dca7c716b4703c923f4a248935e57e49065c0869e888bfe',
        b'00013888cd3ea12884d68218bb261df48ac46b8f582d3b95f2cdec71cc9fc4becb1e0f246bf0b7a92d4efd6b7533ddb18ccc4f054878c7cc89d283eb3e7aca070164f58865da75e3d0ca12ff8205df240f3885b7bc54881194c3c09dd38dd9d900003989933b60503506d09749415539b8bb89277ab8d314f774e573a3cd9eda384c5677c00a0e19a7bde254ad2a1a279d3c8d72457f6dc28b9327299f5ea85d69d100f65b97cbd4442defa1c89b8be5e84766175d99bbc7f4cca0358d78385b',
        b'0000a03b50185e6c05f3bb96f40699906d63d176350ac6d34bde7703cf150c7a93faffbea82e75100c4a53de4bb225a411bd4a9b0d8a80c9efe24b373a984efc7a25b6ebede8d5365124b044f04ab74ab431c85a1b5055e0de2a9320a88b13270000afb05b585921ef045bb8bd2b0b4050e13c6216b0cf2d044154793fcdd9986afc8f7c99bffeabb35cd7797b5513fc1bdfee72d9349ea96a3145f88a3e33b665e4a6f1e3eee8d06cd4b7f5e65768c48ffc08d11e5fd510b738a91145f3adb8']

int_keys_from_ledger = [[0x0000f4fd0743422f322b44c02e217203b5ddf63d09d5fd5852f7115aeb513904a35dc4e8a41de21fc52440074f710d17624ba6862b4294d7e7ae95a861c93aa5c776d158fc29ad51c2b4d0e9c032be5d3077a04fe286b1190f194b5e9776a72f, 0x0000756d810cba0389484ebf6862334db6888cfa69a9bcb19168b89dc5b367bb7e12d0aa29eb5fae2fb09ebb49b636fd95ab0a583bcb4a8a3d6c5a398d5842abc28ae3e521e0fbe64dca7c716b4703c923f4a248935e57e49065c0869e888bfe],
        [0x0000a03b50185e6c05f3bb96f40699906d63d176350ac6d34bde7703cf150c7a93faffbea82e75100c4a53de4bb225a411bd4a9b0d8a80c9efe24b373a984efc7a25b6ebede8d5365124b044f04ab74ab431c85a1b5055e0de2a9320a88b1327, 0x0000afb05b585921ef045bb8bd2b0b4050e13c6216b0cf2d044154793fcdd9986afc8f7c99bffeabb35cd7797b5513fc1bdfee72d9349ea96a3145f88a3e33b665e4a6f1e3eee8d06cd4b7f5e65768c48ffc08d11e5fd510b738a91145f3adb8],
        [0x000072076b1ced72c972633bcb6d7789de299887c8cdb4834fca1f71379277fd506f997fc96665ae7cdb78f60a355bf79b0972eddbbb54d1f11779672e70ff9270123a9c6c1d781a6754bd6b3a91c5682a0288e360a044044cba50a785462160, 0x0001bf58931265d2a56d1024ee282a27f440353d08e1eb59b5ec2aac07df62382518d9f5af7fcbb366437fa07a49e69d270258b6e181cf75835b8e496c20913ea8f4d1846eb42e4dfc0aebbfb32567a6ce5907aba09e7b0338756a73d9369463]]


handled_keys = ['{"x": "115LFY15j2xqcFJXLYvScasi93wyTdmeKPiVgsfzfiBRctYgps77to5Mq4GobohnqQyHxPC7TRMjNL6L4zY259o1SpJPXZYrNARJm7iN9M9rUya6UQJkuf46SosRdEQJwdx", "y": "1135RuKoqPCei8Dc45nmk5i5aAyGpW1iqAoqS34sewCnYMzdWX3ZEM3fcddBxAC26ksXpgEn6G3H4LqAYBiiYhEPFNv62CCu162naUjj1Je35U2FYhFD11EoGFxJAeEbkku"}',
    '{"x": "113qKzQQ3gXzgFTgaaSPLoJMhJgiYdELLbDQPKXz5qdEjksbbFQLemv4yWCWwoJjUCzXkbE1qMcbE8pJyGDKeStZo9i7fPaa1ChnCGRGygyN2eNcDQCdUzKEUvATsqRVJZc", "y": "1147BRZuBzZKLqwRnd96uA7Gt1zd7ezZM9uFMZ1oSgVhydctV5fATtL5dEv54K8uL1rj2SYiGEhZA1UTjPwCnsvUZKiGp3ekHt1Q7yvF9mc4PiSUEdQ7FEJQksZsybNkyM9"}',
    '{"x": "1131wjbrr6XG8nwF7sXDTi7NRXfxeqQCmPSNYUKv1wTMywoLkUDLJ4gJsSeM6YqXKmkcVhmLRyycLVUtnAqJjEicoyJoE46655NGkPav5cm3c2RBxKioTn13zzV7Z98erw9", "y": "18unHHsRQGiskhHV9KoJeRrQCRDdu4i2JArKadf2xnp217S2HBr1AeGt7FBoNfm9yHykW4YJG7bwuwGf1dKbVGuHyZAiVrECEpPgbq5dyHooeTssHTVvgwEuMD3BE8z4TU"}']

# unsalted
# hex_signatures = [b'0001905ef9b5eb81762996821bbe1716f3d5c6e0ae2ca948a154880005bb721996a9f6e31a009f8d66dea8818398a3ad6424a23b2d9a9b3abd6731a98c43869458a15621adf6723bf88ae6999c101fc3d1dfd813f5b0c4abafe50f06e111f590000e7afa76dcad5896374bb371109f1cd0bdec4df4f2d36ede705ea8a0313e0520c89f1383b9ae9f8d42a4d1bbeb3411873c82a8f6c0633c3ea1801e7125eed0494c0426130b60b7308fec74568c3b0d0a5cdf4b59caaf0a1eeb26f440b3ccc']
# r = 0x0001905ef9b5eb81762996821bbe1716f3d5c6e0ae2ca948a154880005bb721996a9f6e31a009f8d66dea8818398a3ad6424a23b2d9a9b3abd6731a98c43869458a15621adf6723bf88ae6999c101fc3d1dfd813f5b0c4abafe50f06e111f590
# s = 0x0000e7afa76dcad5896374bb371109f1cd0bdec4df4f2d36ede705ea8a0313e0520c89f1383b9ae9f8d42a4d1bbeb3411873c82a8f6c0633c3ea1801e7125eed0494c0426130b60b7308fec74568c3b0d0a5cdf4b59caaf0a1eeb26f440b3ccc

# salted
hex_sig = b'000158edcd4c48a4045830e7e4228a0d824a3732ba6fb5424dfe313ddbf1cd4c53a4c527c7cc9767f5dcba62a1152ff677b7e5b0d93c408e8b39c66d368cd94682d168683f1492537b93fba8d137d007d812b52f92e456ebcb91177bba4b60a600001508027ae10bc81444d002258ab4a02abeba8666f618ef4175c2b0c1b4720b674521eb0b3221afa6d7b0bfb5ad825a35e74b8e44e94c833be10ce144e098e1e821a965d4f4a79499c8161744d2f58b7cc93536063df61c787f78464bab03'

def b58_to_int(b58_bytes):
    return int.from_bytes(base58.b58decode(b58_bytes), byteorder='little') % schnorr.p

def int_to_b58(ii):
    return base58.b58encode(schnorr.bytes_from_int(ii))

if __name__ == "__main__":
    assert base58.b58encode(b'hello') == b'Cn8eVZg'
    assert base58.b58encode_check(b'hello') == b'2L5B5yqsVG8Vt'
    assert base58.b58decode(b'Cn8eVZg') == b'hello'
    assert base58.b58decode(b'EUYUqQf') == b'world'
    assert base58.b58decode_check(b'2L5B5yqsVG8Vt') == b'hello'
    assert base58.b58decode(b'a') == b'!'
    assert b58_to_int(b'113BbGK8KghQV7Agy8W9YDev1rnQWFncJNbX6FNk5xt3i85ArogCLyxcAFmtCQXdqW1N83mmzxPjTEbk2ZSJ2HBQXb296kVvCg5ntqkFQTj7W15dcccHbSc4YwFwhBiwQpx') == 11422395288969951266668318517247797610158769971697294414104000319354108053709789800993457876168384338057945990070182946671950057475934120004133141526633780465748593106560360725236740562531793133853926323126879462811998959299673
    assert b58_to_int(b'113JiNkNmUXjoZFZkfB17UfkgU6qwXjseCJY7u8iTw8j9c5b3Gjh2YTkCU1XQVYS9r4xQEcUwz7AMtH247VgEBaweRQZRAqEYkYmMwzGPvPyfiiJ6DNFY93pv83T9zRCDvF') == 12065073978853608390151781695805078280181820006872152624266968017931029341197429495647513274590720850751139309265446457816736158553413796964167609808052788939737267906950034021628473817867647283771188497811472057195260597361304
