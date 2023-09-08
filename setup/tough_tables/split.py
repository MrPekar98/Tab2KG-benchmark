base = '/home/tough_tables/'
filename = base + 'wikidata/wikidata.nt'
split_size = 10000000	# 10M
split_index = 1

def write_nt(index, lines):
    with open(base + 'wikidata/wikidata_' + str(index) + '.nt', 'w') as out_file:
        for line in lines:
            out_file.write(line + '\n')

with open(filename, 'r') as in_file:
    lines = list()
    i = 0

    for line in in_file:
        lines.append(line.strip())
        i += 1

        if i ==	split_size:
            write_nt(split_index, lines)
            i = 0
            split_index += 1
            lines = list()

    write_nt(split_index, lines)
