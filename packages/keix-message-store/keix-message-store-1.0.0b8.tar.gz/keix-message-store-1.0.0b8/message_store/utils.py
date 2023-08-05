import msgpack
import datetime


def ext_hook(code, data):
    print(len(data))
    if code == -1:
        if len(data) == 4:
            secs = int.from_bytes(data, byteorder='big', signed=True)
            nsecs = 0
        elif len(data) == 8:
            data = int.from_bytes(data, byteorder='big', signed=False)
            secs = data & 0x00000003ffffffff
            nsecs = data >> 34
        elif len(data) == 12:
            import struct
            nsecs, secs = struct.unpack('!Iq', data)
        else:
            raise AssertionError("Not reached")
        return datetime.datetime.utcfromtimestamp(secs + nsecs / 1e9)

    else:
        return msgpack.ExtType(code, data)


class KludgedExtType(msgpack.ExtType):
    """
    This is an ExtType that doesn't care for rules.
    """
    def __new__(cls, code, data):
        return super(msgpack.ExtType, cls).__new__(cls, code, data)


def default(obj):
    """MsgPack object hook for encoding datetimes."""
    if isinstance(obj, datetime.datetime):
        # always encode in the 8-byte form
        secs = int(obj.timestamp())
        nsecs = obj.microsecond * 1000

        data = (nsecs << 34) | secs
        data = data.to_bytes(8, byteorder='big')

        return KludgedExtType(-1, data)

    return obj


def serializer(obj):
    return msgpack.packb(obj, default=default, use_bin_type=True)


def deserializer(buf):
    if buf == b'\xc0':
        return -1
    return msgpack.unpackb(buf, raw=False, use_list=False, ext_hook=ext_hook)
