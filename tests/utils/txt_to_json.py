import json
import os

def create_tmp_test_textfile(tmp_file):
    with open("chi_annotator/data/files/spam_classify_chi_shuf.txt") as f, open('tests/data/'+tmp_file, 'w') as f2:
        for n, line in enumerate(f):
            if n >= 1000:
                break
            label, text = line.strip().split(" ", 1)
            f2.write(text+'\n')
        return 'tests/data/'+tmp_file
            

def create_tmp_test_jsonfile(tmp_file):
    with open("chi_annotator/data/files/spam_classify_chi_shuf.txt") as f, open('tests/data/'+tmp_file, 'w') as f2:
        samples = []
        for n, line in enumerate(f): 
            if n >= 1000:
                break
            label, text = line.strip().split(" ", 1)
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
    dirname = create_tmp_test_jsonfile("test_data.json")
    print("test_data.json has been created in " + dirname)
