import math


def h(p):
    if p == 1 or p == 0:
        return 0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


class Tree:
    def __init__(self):
        self.store = [[]]
        self.count = 0
        self.created_flag = False

    def add_rule(self, parent_index, rule):
        child_index_1 = self.count + 1
        child_index_2 = self.count + 2
        self.store[parent_index] = [rule, child_index_1, child_index_2]
        self.count += 2
        self.store.append([])
        self.store.append([])
        return self.count - 1, self.count

    def add_leaf(self, index, category):
        self.store[index] = ['DONE', category]

    def recursive_create(self, cat1, cat2, feats_list, cat1list, cat2list, index):

        if len(cat1list) == 0 or len(cat2list) == 0:
            if len(cat2list) == 0:
                self.add_leaf(index, cat1)
            else:
                self.add_leaf(index, cat2)
            return

        best_feature_index = None
        best_h = 0
        left = [[], []]
        right = [[], []]
        for i1 in range(len(feats_list)):
            temp1 = []
            temp2 = []
            for j1 in range(len(cat1list)):
                if cat1list[j1][i1] == 1:
                    temp1.append(1)
                else:
                    temp2.append(1)
            for j1 in range(len(cat2list)):
                if cat2list[j1][i1] == 1:
                    temp1.append(0)
                else:
                    temp2.append(0)
            if len(temp1) == 0 or len(temp2) == 0:
                continue
            p1 = sum(temp1) / len(temp1)
            p2 = sum(temp2) / len(temp2)
            the_h = h(0.5) - (len(temp1) * h(p1) + len(temp2) * h(p2)) / (len(temp1) + len(temp2))
            if the_h > best_h:
                best_feature_index = i1
                best_h = the_h
                left = [[], []]
                right = [[], []]
                for j1 in range(len(cat1list)):
                    if cat1list[j1][i1] == 1:
                        left[0].append(cat1list[j1])
                    else:
                        right[0].append(cat1list[j1])

                for j1 in range(len(cat2list)):
                    if cat2list[j1][i1] == 1:
                        left[1].append(cat2list[j1])
                    else:
                        right[1].append(cat2list[j1])
        if best_h == 0:
            print("No way to find out the solution")
            return
        a, b = self.add_rule(index, feats_list[best_feature_index])
        self.recursive_create(cat1, cat2, feats_list, left[0], left[1], a)
        self.recursive_create(cat1, cat2, feats_list, right[0], right[1], b)

    def create_tree(self, cat1, cat2, feats_list, cat1list, cat2list):
        if self.created_flag:
            print("the tree is created!")
            return False

        self.created_flag = True
        self.recursive_create(cat1, cat2, feats_list, cat1list, cat2list, 0)


# ------------------- input data ----------------------------- #

category_1 = input('Enter category 1: ')
category_2 = input('Enter category 2: ')
features_count = int(input('Enter number of features: '))
features_list = []
for i in range(features_count):
    features_list.append(input(f'Enter feature {i + 1}: '))
cat_1_count = int(input(f'Enter number of {category_1}: '))
cat_2_count = int(input(f'Enter number of {category_2}: '))

category_1_list = []
category_2_list = []

for i in range(cat_1_count):
    temp = []
    for j in range(features_count):
        temp.append(int(input(f'Does {category_1} {i + 1} has {features_list[j]}?(0/1): ')))
    category_1_list.append(temp)

for i in range(cat_2_count):
    temp = []
    for j in range(features_count):
        temp.append(int(input(f'Does {category_2} {i + 1} has {features_list[j]}?(0/1): ')))
    category_2_list.append(temp)

print(category_1_list)
print(category_2_list)

# -------------------------create tree------------------------------ #
the_tree = Tree()
the_tree.create_tree(cat1=category_1, cat2=category_2, feats_list=features_list, cat1list=category_1_list,
                     cat2list=category_2_list)
print(the_tree.store)
