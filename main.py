# Условие для поиска детей конкретного узла дерева.
class Requirement:
    def __init__(self, class_name, level):
        self.class_name = class_name
        self.level = level
        self.checked = False


class Node:
    def __init__(self, class_name):
        self.children = []
        self.class_name = class_name
        self.is_leaf = False

    def __eq__(self, other):
        return self.class_name == Node(other).class_name


class Tree:
    root = Node('root')

    def __init__(self, df, *args):
        self.column_names = args

        for row_number in range(len(df)):
            previous_node = self.root
            for column_number in range(0, len(args)):
                new_node = Node(df._get_value(row_number, args[column_number]))
                if (new_node not in previous_node.children):
                    previous_node.children.append(new_node)
                    previous_node = new_node
                else:
                    previous_node = previous_node.children[previous_node.children.index(new_node)]

            new_leaf = Node(df.iat[row_number, 0])
            new_leaf.is_leaf = True
            previous_node.children.append(new_leaf)

    def get_children(self, *args):
        all_leaves = []
        pairs = self.make_requirements(args)
        self.search_tree(self.root, 0, all_leaves, pairs)
        return all_leaves

    def make_requirements(self, args):
        pairs = []
        if len(args) == 0:
            pairs.append(Requirement('root', 0))
        else:
            for arg in args:
                level = self.column_names.index(arg[0]) + 1
                class_name = arg[1]
                pairs.append(Requirement(class_name, level))
        return pairs

    def search_tree(self, current_node: Node, current_level, all_leaves, pairs):
        leaves = []
        have_concurrency = self.check_for_concurrency(current_level, current_node, pairs)
        all_correct = True
        for pair in pairs:
            all_correct &= pair.checked
        if all_correct:
            self.get_leaves(current_node, leaves)
            all_leaves.extend(leaves)
            for pair in pairs:
                pair.checked = False

        have_concurrency_in_children = False
        for child in current_node.children:
            have_concurrency_in_children |= self.search_tree(child, current_level + 1, all_leaves, pairs)
        if (not have_concurrency_in_children) & have_concurrency:
            for pair in pairs:
                pair.checked = False
        return have_concurrency

    def check_for_concurrency(self, current_level, current_node, pairs):
        have_concurrency = False
        for pair in pairs:
            if (current_level == pair.level) & (str(current_node.class_name) == str(pair.class_name)):
                pair.checked = True
                have_concurrency = True
        return have_concurrency

    def get_leaves(self, node: Node, leaves: list):
        for child in node.children:
            if child.is_leaf:
                leaves.append(child.class_name)
            else:
                self.get_leaves(child, leaves)

    def print_tree(self, node, counter):
        print(str(node.class_name) + " " + str(counter))
        for child in node.children:
            self.print_tree(child, counter + 1)
