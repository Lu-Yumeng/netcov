import os

lines_to_read = set([65, 66, 67, 68, 69, 70, 71, 73, 74, 75, 76, 77, 78,
                 79, 81, 82, 83, 84, 85, 86, 87, 89, 90, 91, 92, 93,
                 94, 95, 97, 98, 99, 100, 101, 102, 103, 105, 107,
                 108, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122])
with open("fattree4/configs/core-0000", 'r') as cf:
    start_line = float("inf")
    end_line = float("inf")
    flag = 1
    for i, line in enumerate(cf):
        i += 1
        # record the fist line
        if line.startswith("interface"):
            start_line = min(start_line,i)
        # check which lines needed to be written
        # header should be added to the set
        if i < start_line:
            lines_to_read.add(i)
        # body
        else:
            if line.startswith("router bgp"):
                end_line = i
            if i >= end_line and flag:
                end_line = max(end_line,i)

            if i <= end_line:
                if not line.startswith(" ") and not line.startswith("!"):
                    begin = i
                elif line.startswith(" "):
                    continue
                # line starts with !
                elif line.startswith("!"):
                    if set(range(begin,i)).intersection(lines_to_read):
                        lines_to_read.add(begin)
                        lines_to_read.add(i)
                    if i == end_line:
                        end_line = i
                        flag = 0

            elif i > end_line:
                lines_to_read.add(i)

print(lines_to_read)