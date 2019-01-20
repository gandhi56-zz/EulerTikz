import re, sys

s = ""
for line in sys.stdin:
    s += line;

string = "@@ cat $$ @@dog$^"

print(re.findall(r'\tikzpicture(.*?)\tikzpicture', s))
graphTex = re.findall(r'(tikzpicture)(.*?)(tikzpicture)', s)

print(graphTex)


# nodes = re.findall(r'{tikzpicture}.*?/path', graphTex)

# print(nodes)

# nodes = re.findall(r'{.*?}', nodes)

# print(nodes)

