from __future__ import annotations


METADATA_SUM = 0

# generator yielding one number at a time
# https://stackoverflow.com/a/56623255/4283100
# ([0-9]+\s[0-9]+\s)        $1\n
def generator_input(path):
    with open(path) as file:
        for line in file:
            for word in line.split():
                yield int(word)

def generator_number() -> int:
    n = 1
    while True:
        yield n
        n += 1

def get_single_header(gen_input) -> tuple[int, int]:
    first  = next(gen_input)
    second = next(gen_input)
    # print(f"header ({first}, {second})")
    return first, second

def get_metadata(series: int, gen_input) -> list[int]:
    metadata = list()
    for _ in range(series):
        val = next(gen_input)
        metadata.append(val)
    return metadata

def collect_indices(indexes: list, nchildren: int) -> dict():
    new_dict = dict()
    for index in indexes:
        if index == 0 or index > nchildren: # take only indeces that point to children
            continue
        if index not in new_dict:
            new_dict[index] = 1
        else:
            new_dict[index] += 1
    # 1-base to 0-base indexing
    return {key - 1: value for key, value in new_dict.items()}

class Node:
    def __init__(self, nMetadatas: int, parent: Node) -> None:
        self.label: int = next(labels)
        self._nMetadatas: int = nMetadatas
        self._parent: Node = parent
        self.__children: list[Node] = list()
        self.__metadata: list[int] = list()

    def addChild(self, child: Node) -> None:
        self.__children.append(child)

    def addMetadata(self, metadata: list[int]) -> None:
        self.__metadata = metadata

    def sum_metadata(self):
        global METADATA_SUM
        METADATA_SUM += sum(self.__metadata)
        for child in self.__children:
            child.sum_metadata()

    def print_root(self, indent = 0):
        text = ' ' * 2 * indent + f"{self.label}: {self.__metadata}"
        print(text)
        indent += 1
        for child in self.__children:
            child.print_root(indent)

    def __repr__(self):
        return f"{self.label}({self.__metadata}): {self.__children}"

    def evaluate(self):
        if not self.__children:
            return sum(self.__metadata)
        
        node_value = 0
        indices_dict = collect_indices(self.__metadata, len(self.__children))
        for index, n_times in indices_dict.items():
            node_value += n_times * self.__children[index].evaluate()
        return node_value


def process_node(parent_node: Node, n_children: int, input):
    for _ in range(n_children):
        # for every child create a node and parse header
        n_children, n_metadata = get_single_header(input)
        new_node = Node(n_metadata, parent_node)
        # reqursion termination condition
        if n_children == 0:
            metadata_list = get_metadata(n_metadata, input)
            new_node.addMetadata(metadata_list)
            parent_node.addChild(new_node)
            continue
        else:
            # move one level deeper
            process_node(new_node, n_children, input)
            parent_node.addChild(new_node)
    # we reached metadata info of the parent
    metadata_list = get_metadata(parent_node._nMetadatas, input)
    parent_node.addMetadata(metadata_list)


if __name__ == "__main__":
    # generators for parsing input and labaling nodes
    input = generator_input("inputs/aoc-8.txt")
    labels = generator_number()
    # induction base
    n_children, n_metadata = get_single_header(input)
    root = Node(n_metadata, None)
    # recursively create whole data structure
    process_node(root, n_children, input)
    
    root.sum_metadata()
    print(f"check on metadata (A): {METADATA_SUM}")
    # print("PRINTING ROOT")
    # root.print_root()
    print("evaluating root node (B)")
    value = root.evaluate()
    print(value)
