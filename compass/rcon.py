import asyncio
import struct
import os
from compass.bot import bot, command, initialize

@command('whitelist', 'wl')
async def whitelist(player):
    """
    Add player to the whitelist.
    """
    host, _, password = os.environ['MINECRAFT_RCON'].partition('/')
    hostname, _, port = host.partition(':')
    if not(port):
        port = 25575
    return await rcon_command(hostname, port, password, 'whitelist add ' + player)

async def rcon_command(hostname, port, password, command):
    reader, writer = await asyncio.open_connection(hostname, int(port))
    try:
        # send auth packet
        writer.write(rcon_packet(42, 3, password))
        # check for response
        pkt, kind, payload = await read_rcon_packet(reader)
        if pkt != 42 or kind != 2:
            raise ValueError("Bad auth")
        
        # send command
        writer.write(rcon_packet(43, 2, command))
        writer.write_eof()
        resp = b''

        try:
            while True:
                pkt, kind, payload = await read_rcon_packet(reader)
                if pkt != 43:
                    continue
                if kind != 0:
                    raise ValueError('Bad response')
                resp += payload
        except:
            pass

        return resp.decode('utf-8')
    finally:
        writer.close()

def rcon_packet(id, kind, payload):
    length = len(payload) + 10
    return struct.pack('<iii', length, id, kind) + payload.encode('utf-8') + b'\0\0'

async def read_rcon_packet(reader):
    length, = struct.unpack('<i', await reader.readexactly(4))
    remainder = await reader.readexactly(length)
    id, kind = struct.unpack_from('<ii', remainder)
    payload = remainder[8:-2]
    return id, kind, payload