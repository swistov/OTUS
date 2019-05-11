import ast
import os
import collections

from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_file_names(path_with_file):
    file_names = []
    for dir_name, dirs, files in os.walk(path_with_file, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
                if len(file_names) == 100:
                    break
    return file_names


def get_trees(_path):
    path_with_file = ''
    file_names = get_file_names(path_with_file)
    trees = []

    print('total %s files' % len(file_names))

    for filename in file_names:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        trees.append(tree)
    print('trees generated')
    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_words_in_path(path):
    trees = [t for t in get_trees(path) if t]

    for f in flat([get_all_names(t) for t in trees]):
        if not (f.startswith('__') and f.endswith('__')):
            names_func = f

    def split_name_to_words(name):
        return [n for n in name.split('_') if n]
    return flat([split_name_to_words(func_name) for func_name in names_func])


def get_nodes(tree):
    nodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            nodes = nodes.append(node)
    return nodes.name.lower()


def get_lower_tree(tree):
    lower_tree = []
    flat_list = []

    for t in tree:
        flat_list = flat_list.append(get_nodes(t))

    for f in flat(flat_list):
        if not (f.startswith('__') and f.endswith('__')):
            lower_tree = lower_tree.append(f)

    return lower_tree


def get_top_verbs_in_path(path, top_size=10):
    # global Path
    # Path = path
    trees = [t for t in get_trees(None) if t]
    print('functions extracted')
    x = []
    for function_name in get_lower_tree(trees):
        x = x.append(get_verbs_from_function_name(function_name))
    verbs = flat(x)

    return collections.Counter(verbs).most_common(top_size)


def get_top_functions_names_in_path(path, top_size=10):
    t = get_trees(path)
    return collections.Counter(get_lower_tree(t)).most_common(top_size)


wds = []
projects = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]
for project in projects:
    path = os.path.join('.', project)
    wds += get_top_verbs_in_path(path)

top_size = 200
print('total %s words, %s unique' % (len(wds), len(set(wds))))
for word, occurence in collections.Counter(wds).most_common(top_size):
    print(word, occurence)
