import re, sys

s = ""
for line in sys.stdin: s += line;

matches = re.compile(r'(\\(?:begin|end)\{tikzpicture\})').finditer(s)
matches = [(m.start(0), m.end(0)) for m in matches]
graphData = s[matches[0][1]:matches[1][0]]

nodeData = re.findall(r'\\node(.+);', graphData)

nodeData = [re.sub(r'(\$)', "", re.findall(r'\{(.*)\}', n)[0]) for n in nodeData]
print(nodeData)

edgeData = re.findall(r'(\(.*\))(?:.*)(?:edge|--)(?:.*)(\(.*\))', graphData)

for e in edgeData:
    print("{} <-> {}".format(e[0], e[1]))
