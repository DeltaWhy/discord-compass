import asyncio
import struct
import json
import compass.bot
from compass.bot import command

def read_varint(data):
    i = 0
    j = 0
    while True:
        k = data[0]
        data = data[1:]
        i |= (k & 0x7f) << j * 7
        j += 1
        if j > 5:
            raise 'VarInt too big'
        if (k & 0x80) != 0x80:
            break
    return (i, data)

class ServerPingProtocol(asyncio.Protocol):
    def __init__(self, address, port, future):
        self.address = address
        self.port = port
        self.resp_len = None
        self.resp = None
        self.future = future
    def connection_made(self, transport):
        self.transport = transport
        data = struct.pack('bbb', 0, 4, len(self.address))
        data += self.address.encode('utf-8')
        data += struct.pack('!hb', self.port, 1)
        data = struct.pack('b', len(data)) + data + struct.pack('bb', 1, 0)
        transport.write(data)
    def data_received(self, data):
        if not self.resp_len:
            self.resp_len, data = read_varint(data)
        if not self.resp:
            if data[0] != 0:
                raise 'Bad packet'
            self.resp = data[1:]
        else:
            self.resp += data
        if len(self.resp) < self.resp_len - 1:
            return

        # we have the whole message
        _, self.resp = read_varint(self.resp)
        self.transport.close()
        self.future.set_result(json.loads(self.resp.decode('utf-8')))

async def run(address, port):
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    await loop.create_connection(lambda: ServerPingProtocol(address, port, future), address, port)
    return await future

@command('status', 'mcstatus')
async def status(address, port=25565):
    """
    Get server status.
    """
    resp = await run(address, int(port))
    if not(resp) or 'players' not in resp:
        return 'No result.'
    if 'online' not in resp['players'] or not resp['players']['online']:
        return 'No players online.'
    if 'sample' not in resp['players']:
        return '{} players online.', resp['players']['online']
    return 'Online: ' + ', '.join([p['name'] for p in resp['players']['sample']])
