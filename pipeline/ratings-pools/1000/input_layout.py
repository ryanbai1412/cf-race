"""Preserve the line grammar used by line-oriented accepted submissions."""


def layout(pid,text):
    words = text.split()
    fixed = {"106A":(1,2),"724A":(1,1),"777A":(1,1),"114A":(1,1),
             "479A":(1,1,1),"75A":(1,1),"604A":(5,5,2)}
    if pid in fixed:
        sizes = fixed[pid]
    elif pid in ("139A","626A","272A","389A","831A","847M","849A","864B","888B"):
        sizes = (1,len(words)-1)
    elif pid in ("450A","680B","371A","385A","435A","862A"):
        sizes = (2,len(words)-2)
    elif pid=="368A":
        sizes = (2,len(words)-3,1)
    elif pid=="779A":
        n = int(words[0])
        sizes = (1,n,n)
    else:
        return text
    if sum(sizes)!=len(words) or any(x<1 for x in sizes):
        raise ValueError("input line grammar mismatch")
    lines,offset = [],0
    for size in sizes:
        lines.append(" ".join(words[offset:offset+size]))
        offset += size
    return "\n".join(lines)+"\n"
