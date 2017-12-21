import json
import os


spam_classify_chi_shuf_path = "tests/data/test_email_classify/email_classify_chi.txt"
base_path = "tests/data/"


def create_tmp_test_textfile(tmp_file):
    with open(spam_classify_chi_shuf_path) as f, open(base_path + tmp_file, 'w') as f2:
        for n, line in enumerate(f):
            if n >= 1000:
                break
            label, text = line.strip().split(" ", 1)
            f2.write(text + '\n')
        return base_path + tmp_file


def create_tmp_test_jsonfile(tmp_file):
    with open(spam_classify_chi_shuf_path) as f, open(base_path + tmp_file, 'w') as f2:
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
    return base_path + tmp_file


def rm_tmp_file(filename):
    """
    rm tmp files
    :return:
    """
    os.remove(base_path + filename)

# if __name__ == '__main__':
#     dirname = create_tmp_test_jsonfile("test_data.json")
#     print("test_data.json has been created in " + dirname)
