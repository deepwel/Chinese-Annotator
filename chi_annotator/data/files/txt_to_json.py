import simplejson

with open("spam_classify_chi_shuf.txt") as f, open('spam_classify_chi_shuf_top1000.json', 'w') as f2:
    samples = []
    line_num = 0
    for line in f:
        line_num += 1
        if line_num > 1000:
            break
        tokens = line.strip().split()
        print(tokens)
        label = tokens[0]
        text = " ".join(tokens[1:])
        sample = {}
        sample.setdefault("label", label)
        sample.setdefault("text", text)
        samples.append(sample)
    f2.write(simplejson.dumps({"data_set": samples}, ensure_ascii=False, indent=2))