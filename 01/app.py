total = 0
with open('input.txt') as f:
  for line in f.readlines():
    first = last = 0
    gotfirst = False
    for c in line:
      if c >= '0' and c <= '9':
        if gotfirst:
          last = int(c)
        else:
          first = last = int(c)
    total += (first*10) + last
print(total)
