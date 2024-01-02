#!/usr/bin/bash

#
# Build
#

# Run only those apps with changed content

for i in $(python3 -c 'from aoc import utils;utils.list_changed()'); do
  python3 -m aoc.day_$i
done

# Re-write the results doc

mkdir -p ./out
touch ./out/.nojekyll
python3 -c 'from aoc import utils;utils.print_outfile()'
