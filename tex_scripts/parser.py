import re, sys

s = ""
for line in sys.stdin:
    s += line;

nodeData = re.findall(r'\\node(.+);', s)

print("nodes:")
for nd in nodeData:
    print(re.findall(r'\{(.*)\}', nd))

edgeData = re.findall(r'(\(.*\))(?:.*)edge(?:.*)(\(.*\))', s)

for e in edgeData:
    print("{} <-> {}".format(e[0], e[1]))

# nodes = re.findall(r'{tikzpicture}.*?/path', graphTex)

# print(nodes)

# nodes = re.findall(r'{.*?}', nodes)

# print(nodes)

