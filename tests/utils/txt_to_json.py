import json
import os


def create_tmp_test_file(tmp_file):
    with open("chi_annotator/data/files/spam_classify_chi_shuf.txt") as f, open('tests/data/'+tmp_file, 'w') as f2:
        samples = []
        line_num = 0
        for line in f:
            line_num += 1
            if line_num > 1000:
                break
            tokens = line.strip().split()
            label = tokens[0]
            text = " ".join(tokens[1:])
            sample = {}
            sample.setdefault("label", label)
            sample.setdefault("text", text)
            samples.append(sample)
        f2.write(json.dumps({"data_set": samples}, ensure_ascii=False, indent=2))
    return 'tests/data/'+tmp_file


def rm_tmp_file(filename):
    """
    rm tmp files
    :return:
    """
    os.remove('tests/data/'+filename)

if __name__ == '__main__':
    dirname = create_tmp_test_file("test_data.json")
    print("test_data.json has been created in " + dirname)
