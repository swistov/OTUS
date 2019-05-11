import ast
import os
import collections

from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(verb_word):
    if not verb_word:
        return False
    pos_info = pos_tag([verb_word])
    return pos_info[0][1] == 'VB'


def get_file_names(path_with_file):
    file_names = []
    for dir_name, dirs, files in os.walk(path_with_file, topdown=True):
        file_names = [os.path.join(dir_name, file) for file in files if file.endswith('.py')]
        if len(file_names) == 100:
            break
    return file_names


def get_trees(_path):
    path_with_file = _path
    file_names = get_file_names(path_with_file)
    trees = []

    print(f'total {len(file_names)} files in {path_with_file}')

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
    return [verb_word for verb_word in function_name.split('_') if is_verb(verb_word)]


def get_all_words_in_path(file_path):
    trees = [t for t in get_trees(file_path) if t]
    function_names = []
    for f in flat([get_all_names(t) for t in trees]):
        if not (f.startswith('__') and f.endswith('__')):
            function_names = function_names.append(f)

    def split_name_to_words(name):
        return [n for n in name.split('_') if n]
    return flat([split_name_to_words(function_name) for function_name in function_names])


def get_ast_nodes(tree):
    ast_nodes = []
    for f in flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in tree]):
        if not (f.startswith('__') and f.endswith('__')):
            ast_nodes = ast_nodes.append(f)
    return ast_nodes


def get_top_verbs_in_path(file_path, top_path_size=10):
    trees = [t for t in get_trees(file_path) if t]
    fncs = get_ast_nodes(trees)
    print('functions extracted')
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in fncs])
    return collections.Counter(verbs).most_common(top_path_size)


def get_top_functions_names_in_path(file_path, top_path_size=10):
    t = get_trees(file_path)
    nms = get_ast_nodes(t)
    return collections.Counter(nms).most_common(top_path_size)


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
