import yaml
import os

from os.path import join, dirname
from ..constants import Flags, example_dir


def add_examples(list_of_examples, path, example_type=None, skip=None):
    example_path = join(example_dir, path)

    if skip is not None:
        skip = set(skip)

    for file in os.listdir(example_path):
        flags = 0

        if file.startswith(('_', '.')):
            continue
        elif file.endswith(".py"):
            if example_type is not None:
                flags |= example_type
            elif "server" in file or "animate" in file:
                flags |= Flags.server
            else:
                flags |= Flags.file
        elif file.endswith(".ipynb"):
            flags |= Flags.notebook
        else:
            continue

        if "animate" in file:
            flags |= Flags.animated

            if flags & Flags.file:
                raise ValueError("file examples can't be animated")

        if skip and file in skip:
            flags |= Flags.skip

        list_of_examples.append((join(example_path, file), flags))

    return list_of_examples


def get_all_examples(all_notebooks):
    # Make a list of all the examples
    list_of_examples = []
    with open(join(dirname(__file__), "examples.yaml"), "r") as f:
        examples = yaml.load(f.read())
    for example in examples:
        path = example["path"]
        try:
            example_type = getattr(Flags, example["type"])
        except KeyError:
            example_type = None

        if not all_notebooks:
            skip_status = example.get("skip") or example.get("skip_travis")
        else:
            skip_status = example.get("skip")

        list_of_examples = add_examples(list_of_examples, path, example_type=example_type, skip=skip_status)

    return list_of_examples


def get_file_examples(all_notebooks):
    all_examples = get_all_examples(all_notebooks)
    file_examples = [example for example, flags in all_examples if flags & Flags.file]
    return file_examples[:1]


def get_server_examples(all_notebooks):
    all_examples = get_all_examples(all_notebooks)
    server_examples = [example for example, flags in all_examples if flags & Flags.server]
    return server_examples


def get_notebook_examples(all_notebooks):
    all_examples = get_all_examples(all_notebooks)
    notebook_examples = [example for example, flags in all_examples if flags & Flags.notebook]
    return notebook_examples
