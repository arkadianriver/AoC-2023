from .utils import Utils
u = Utils(__file__)

total = 0
with open(f'{u.inbase}.txt') as f:
  for line in f.readlines():
    first = last = 0
    gotfirst = False
    for c in line:
      if c >= '0' and c <= '9':
        if gotfirst:
          last = int(c)
        else:
          first = last = int(c)
          gotfirst = True
    total += (first*10) + last

u.output(f'Calibration value sum: {total}')
