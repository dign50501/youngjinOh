class RBNode:
    def __init__(self, key):
        self._key = key
        self._red = False
        self._left = None
        self._right = None
        self._p = None

    key = property(fget=lambda self: self._key)
    red = property(fget=lambda self: self._red)
    left = property(fget=lambda self: self._left)
    right = property(fget=lambda self: self._right)
    p = property(fget=lambda self: self._p)

    def __str__(self): return str(self.key)

    def __repr__(self): return str(self.key)


class UserRBNode(RBNode):
    def __init__(self, user_id, user_name=None):
        RBNode.__init__(self, user_id)
        self._user_name = user_name  # self.word = None => red black tree
        self.friends = []  # friends will be saved in linked lists
        self._word = []  # words will be linked lists
        self._num_of_friends = 0

    word = property(fget=lambda self: self._word)
    user_name = property(fget=lambda self: self._user_name)
    num_of_friends = property(fget=lambda self: self._num_of_friends)

    def add_friend(self, friend):
        self.friends.append(friend)
        self._num_of_friends = len(self.friends)

    def print_friend(self):
        print("Friends of %s : " % self.user_name, end=' ')

        for person in self.friends:
            if person.user_name is not None:
                print(person.user_name, end=" ")
        print()

    def add_word(self, input_word):
        self._word.append(input_word)

    def del_word(self, input_word):
        self._word.remove(input_word)

    def print_word(self):
        for i in self._word:
            print(i, end=' ')


class WordRBNode(RBNode):
    def __init__(self, word):
        RBNode.__init__(self, word)
        self._user = []

    user = property(fget=lambda self: self._user)

    def add_user(self, user_id):
        self._user.append(user_id)

    def del_user(self, user_id):
        self._user.remove(user_id)


class RBtree:
    def __init__(self):
        self._nil = RBNode(None)
        self._root = self._nil

    nil = property(fget=lambda self: self._nil)
    Root = property(fget=lambda self: self._root)

    def search(self, k, x=None):
        if x is None:  # fix when problem occurs
            x = self.Root
        while x != self.nil and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x  # x is a node!

    def insert_node(self, z):
        y = self.nil
        x = self.Root

        while x is not self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        self.rb_insert_fix_up(z)

    def rb_insert_fix_up(self, z):
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self.left_rotate(z.p.p)
        self.Root._red = False

    def left_rotate(self, x):
        y = x.right
        x._right = y.left

        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y

    def right_rotate(self, y):
        x = y.left
        y._left = x.right

        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x

    def transplant(self, u, v):
        if u.p == self.nil:
            self._root = v
        elif u == u.p.left:
            u.p._left = v
        else:
            u.p._right = v
        v._p = u.p

    def minimum(self, x=None):
        if x is None:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x

    def delete_node(self, z):  # error than fix
        y = z
        y_original_color = y.red
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.red
            x = y.right
            if y.p == z:
                x._p = y
            else:
                self.transplant(y, y.right)
                y._right = z.right
                y.right._p = y
            self.transplant(z, y)
            y._left = z.left
            y.left._p = y
            y._red = z.red
        if not y_original_color:
            self.delete_fix_up(x)

    def delete_fix_up(self, x):  # this part can be error
        while x != self.Root and not x.red:
            if x == x.p.left:
                w = x.p.right
                if w.red:
                    w._red = False
                    x.p._red = True
                    self.left_rotate(x.p)
                    w = x.p.right
                if not w.left.red and not w.right.red:
                    w._red = True
                    x = x.p
                else:
                    if not w.right.red:
                        w.left._red = False
                        w._red = True
                        self.right_rotate(w)
                        w = x.p.right
                    w._red = x.p._red
                    x.p._red = False
                    w.right._red = False
                    self.left_rotate(x.p)
                    x = self.Root
            else:
                w = x.p.left
                if w.red:
                    w._red = False
                    x.p._red = True
                    self.right_rotate(x.p)
                    w = x.p.left
                if not w.right.red and not w.left.red:
                    w._red = True
                    x = x.p
                else:
                    if not w.left.red:
                        w.right._red = False
                        w._red = True
                        self.left_rotate(w)
                        w = x.p.left
                    w._red = x.p.red
                    x.p._red = False
                    w.left._red = False
                    self.right_rotate(x.p)
                    x = self.Root
        x._red = False


class UserRBtree(RBtree):
    def __init__(self):
        RBtree.__init__(self)
        self._num_of_users = 0
        self._total_friends = []

    total_friends = property(fget=lambda self: self._total_friends)

    def insert_node(self, z):
        RBtree.insert_node(self, z)
        self._num_of_users += 1

    def delete_node(self, z):
        RBtree.delete_node(self, z)
        self._num_of_users -= 1

    def delete_fix_up(self, x):
        RBtree.delete_fix_up(self, x)

    num_of_users = property(fget=lambda self: self._num_of_users)


class WordRBTree(RBtree):
    def __init__(self):
        RBtree.__init__(self)
        self.count = 0

    def word_insert_node(self, word, user_id):
        if self.search(word) == self.nil:
            z = WordRBNode(word)
            self.insert_node(z)
            z.add_user(user_id)
        else:
            x = self.search(word)
            x.add_user(user_id)


class ReadData:
    @staticmethod
    def user(tree):
        with open('user.txt') as f:
            while True:
                user_id = f.readline()
                user_id = user_id[0:-1]
                if not user_id:
                    break
                user_id = int(user_id)
                f.readline()
                user_name = f.readline()
                user_name = user_name[0:-1]
                f.readline()
                z = UserRBNode(user_id, user_name)
                tree.insert_node(z)

    @staticmethod
    def friend(tree):
        with open('friend.txt') as f:
            while True:
                personA = f.readline()
                personA = personA[0:-1]
                if not personA:
                    break
                personA = int(personA)
                personB = f.readline()
                personB = personB[0:-1]
                personB = int(personB)
                f.readline()
                x = tree.search(personA)
                y = tree.search(personB)
                x.add_friend(y)

    @staticmethod
    def word(word_t, user_t):
        with open('word.txt') as f:
            while True:
                person = f.readline()
                person = person[0:-1]
                if not person:
                    break
                person = int(person)
                f.readline()
                word = f.readline()
                word = word[0:-1]
                f.readline()
                word_t.word_insert_node(word, person)
                z = user_t.search(person)
                z.add_word(word)


def main():
    user_tree = UserRBtree()
    word_tree = WordRBTree()
    word_node = None
    ReadData.user(user_tree)
    ReadData.friend(user_tree)
    ReadData.word(word_tree, user_tree)

    while True:
        print("""0. Read data files
1. display statistics
2. Top 5 most tweeted words
3. Top 5 most tweeted users
4. Find users who tweeted a word (e.g, '연세대)
5. Find all people who are friends of the above users
6. Delete all mentions of a word
7. Delete all users who mentioned a word
8. Find strongly connected components
9. Find shortest path""", end='')
        print(""" from a given user
99. Quit
Select Menu: """, end='')

        number = int(input())
        print()

        if number == 0:
            print("Total users: %d" % user_tree.num_of_users)
            print("Total friendship records: ")
            print("Total tweets: ")
        elif number == 1:
            print("Average number of friends: ")
            print("Minimum Friends: ")
            print("Maximum number of friends: ")
        elif number == 2:
            print("2")
        elif number == 3:
            print("3")
        elif number == 4:
            print("Who tweeted the input word? ", end='')
            sen = input()
            word_node = word_tree.search(sen)
            if word_node is not word_tree.nil and word_node is not None:
                print("People who tweeted: ", end='')
                for person in word_node.user:
                    x = user_tree.search(person)
                    print(x.user_name, end=' ')
                print()
            else:
                print("No one has tweeted the word!")
        elif number == 5:
            if word_node is not word_tree.nil and word_node is not None:
                temp = list(set(word_node.user))
                for person in temp:
                    z = user_tree.search(person)
                    z.print_friend()
            else:
                print("No one has tweeted the word!")
        elif number == 6:
            print("Enter an input you want to delete: ", end='')
            input_word = input()
            del_node = word_tree.search(input_word)
            if del_node is not word_tree.nil:
                for person in del_node.user:
                    z = user_tree.search(person)
                    z.del_word(input_word)
                word_tree.delete_node(del_node)
                word_node = None
            else:
                print("Nothing to delete!")
        elif number == 7:
            print("Enter an input to delete users who tweeted this word: ", end='')
            input_word = input()
            del_node = word_tree.search(input_word)
            if del_node is not word_tree.nil:
                while del_node.user:
                    for person in del_node.user:
                        z = user_tree.search(person)
                        for i in z.word:
                            k = word_tree.search(i)
                            if z.key in k.user:
                                k.del_user(z.key)
                                if not k.user:
                                    word_tree.delete_node(k)
                        user_tree.delete_node(z)
                word_node = None
            else:
                print("Nothing to delete!")
        elif number == 8:
            print("8")
        elif number == 9:
            print("Total users: %d" % user_tree.num_of_users)
        elif number == 99:
            break
        else:
            print("Invalid input! Please re-enter")

        print()


main()
