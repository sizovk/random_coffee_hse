import yaml


def load_yml_file(filename: str):
    with open(filename, encoding='utf-8') as fin:
        text_data = fin.read()
    return yaml.unsafe_load(text_data) 