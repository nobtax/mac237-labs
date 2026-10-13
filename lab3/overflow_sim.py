
TOKEN = '529f98b148caaec3'

BUF_OFF, BUF_LEN = 0, 64
SFP_OFF, SFP_LEN = 64, 8
RET_OFF, RET_LEN = 72, 8
FRAME_LEN = 80

RETURN_TO = 0x0000000000401136
SAVED_FP = 0x00007ffddeadbeef

def new_frame():
    f = bytearray(FRAME_LEN)
    f[SFP_OFF:SFP_OFF + SFP_LEN] = SAVED_FP.to_bytes(SFP_LEN, 'little')
    f[RET_OFF:RET_OFF + RET_LEN] = RETURN_TO.to_bytes(RET_LEN, 'little')
    return f

def ret_of(frame):
    return int.from_bytes(frame[RET_OFF:RET_OFF + RET_LEN], 'little')

def unsafe_copy(frame, data):
    spilled = 0
    for i, b in enumerate(data):
        if BUF_OFF + i < FRAME_LEN:
            frame[BUF_OFF + i] = b
        else:
            spilled += 1
    return frame, spilled

def safe_copy(frame, data):
    n = min(len(data), BUF_LEN - 1)
    frame[BUF_OFF:BUF_OFF + n] = data[:n]
    frame[BUF_OFF + n] = 0
    return frame, max(0, len(data) - n)

def fields_reached(n):
    hit = []
    if n > BUF_LEN:
        hit.append('saved frame pointer')
    if n > SFP_OFF + SFP_LEN:
        hit.append('saved return address')
    if n > FRAME_LEN:
        hit.append('caller frame')
    return hit or ['buffer only']

print('token:', TOKEN)
print()
print('Part A. How far does an input of length n reach?')
print(f'{"n":>5} {"fields reached":<55} spilled')

for n in (32, 64, 65, 72, 73, 80, 96):
    f, sp = unsafe_copy(new_frame(), b'A' * n)
    print(f"{n:>5} {', '.join(fields_reached(n)):<55} {sp}")



print()
ATTACK = int(TOKEN[:8], 16)
payload = b'A' * RET_OFF + ATTACK.to_bytes(RET_LEN, 'little')
f, sp = unsafe_copy(new_frame(), payload)

print('Part B. Overwriting the saved return address')
print(f' payload length : {len(payload)}')
print(f' intended return : {RETURN_TO:#018x}')
print(f' return after copy : {ret_of(f):#018x}')
print(f' attacker value : {ATTACK:#018x}')

assert ret_of(f) == ATTACK, 'payload did not land on the return address'
print(' CHECK PASS: the saved return address now holds your token-derived value')



print()
g, dropped = safe_copy(new_frame(), payload)

print('Part C. The same payload through a bounded copy')
print(f' bytes refused    : {dropped}')
print(f' return after copy : {ret_of(g):#018x}')

assert ret_of(g) == RETURN_TO, 'bounded copy should not touch the return address'
print(' CHECK PASS: the saved return address is unchanged')



print()
def alloc_size_32(count, item):
    return (count * item) % (2 ** 32)

print('Part D. Integer overflow in a size computation')

for count, item in ((10, 16), (0x10000001, 16), (0x40000001, 4)):
    want, got = count * item, alloc_size_32(count, item)
    print(f' count={count:<12} item={item:<3} asked for {want:>12} bytes, '
          f"allocated {got:>12} bytes {'WRAPPED' if got != want else 'ok'}")



print()
def strncpy_like(frame, data, n):
    m = min(len(data), n)
    frame[BUF_OFF:BUF_OFF + m] = data[:m]
    return frame

print('Part E. The missing terminator')

h = strncpy_like(new_frame(), b'B' * 64, BUF_LEN)
first_zero = h.find(0, BUF_OFF)

print(f' buffer occupies offsets 0 to {BUF_LEN - 1}')
print(f' first zero byte at offset {first_zero}')
print(f' a later read of this string consumes {first_zero - BUF_LEN + 1} bytes '
      f'beyond the buffer, inside the saved frame pointer')

assert first_zero >= BUF_LEN
print(' CHECK PASS: a full-width bounded copy left no terminator inside the buffer')
