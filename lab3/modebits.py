def allows(mode, who, op):
  shift = {'owner': 6, 'group': 3, 'other': 0}[who]
  bit = {'r': 4, 'w': 2, 'x': 1}[op]
  return bool((mode >> shift) & bit)

TESTS = [(0o600, 'owner', 'r', True), (0o600, 'other', 'r', False),
      (0o640, 'group', 'r', True), (0o640, 'group', 'w', False),
      (0o777, 'other', 'w', True), (0o755, 'other', 'w', False),
      (0o700, 'other', 'x', False), (0o755, 'other', 'x', True)]
for mode, who, op, want in TESTS:
   got = allows(mode, who, op)
   print(f'{oct(mode)} {who:6s} {op} -> {str(got):5s} '
       f'{"PASS" if got == want else "FAIL"}')
