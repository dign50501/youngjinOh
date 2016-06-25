import sys
sys.setrecursionlimit(1500)

count_user = 0
count_word = 0

WHITE = 0
GRAY = 1
BLACK = 2


INFTY = 1E10


class Heap:
    def __init__(self):
        self.nelem = 0
        self.A = []

    def parent(self, n):
        return (n-1) // 2

    def left(self, n):
        return 2 * n + 1

    def right(self, n):
        return 2 * n + 2

    def compare(self, a, b):
        return a - b > 0

    def exchange(self, i, j):
        A = self.A
        A[i], A[j] = A[j], A[i]

    def heapify(self, i):
        A = self.A
        l = self.left(i)
        r = self.right(i)
        if l < self.nelem and self.compare(A[l], A[i]):
            largest = l
        else:
            largest = i
        if r < self.nelem and self.compare(A[r], A[largest]):
            largest = r
        if largest != i:
            self.exchange(i, largest)
            self.heapify(largest)


class PriorNode:
    def __init__(self, key, n):
        self.ndx = 0
        self.n = n
        self.key = key

    def __repr__(self):
        return "(%d:%d,%d)" % (self.ndx,self.n, self.key)


class MaxQueue(Heap):
    def __init__(self):
        super().__init__()

    def compare(self, a, b):
        return a.key > b.key

    def exchange(self, i, j):
        A = self.A
        A[i].ndx = j
        A[j].ndx = i
        super().exchange(i, j)

    def update_key(self, i):
        parent = lambda x: self.parent(i)
        compare = lambda a,b: self.compare(a, b)
        A = self.A
        while i > 0 and not compare(A[parent(i)], A[i]):
            self.exchange(i, parent(i))
            i = parent(i)

    def increase_key(self,i,key):
        A = self.A
        if key < A[i].key:
            print ("Error")
            sys.exit(-1)
        A[i].key = key
        self.update_key(i)

    def insert(self,n):
        A = self.A
        while len(A) < self.nelem:
            A.append(None)
        i = self.nelem
        A.append(None)
        self.nelem += 1
        A[i] = n
        A[i].ndx = i
        self.update_key(i)

    def extract(self):
        elem = self.A[0]
        self.exchange(0,self.nelem-1)
        self.nelem -= 1
        self.heapify(0)
        return elem

    def is_empty(self):
        return self.nelem == 0


class MinQueue(MaxQueue):
    def __init__(self):
        super().__init__()

    def compare(self,a,b):
        return a.key < b.key

    def update_key(self,i):
        parent = lambda x: self.parent(i)
        A = self.A
        while i > 0 and not self.compare(A[parent(i)], A[i]):
            self.exchange(i,parent(i))
            i = parent(i)

    def decrease_key(self,i,key):
        A = self.A
        if key > A[i].key:
            print ("Error")
            sys.exit(-1)
        A[i].key = key
        self.update_key(i)

    def __repr__(self):
        return "%a %a" % (self.nelem, self.A)


class Adj:
    def __init__(self, n=0): # if does not work delete
        self.n = n
        self.next = None


class Weight(Adj):
    def __init__(self, n, w):
        super().__init__(n)
        self.w = w


class Vertex:
    def __init__(self, name):
        self.parent = -1
        self.name = name
        self.n = 0
        self.first = None

    def add(self, v):
        a = Adj()
        a.n = v.n
        a.next = self.first
        self.first = a

    def copy(self, other):
        self.parent = other.parent
        self.name = other.name
        self.n = other.n
        self.first = other.first


class DijkVertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
        self.d = INFTY
        self.priority = None

    def __repr__(self):
        return "(%a %a %a)" % (self.name,self.n,self.d)

    def add(self, v, w):
        a = Weight(v, w)
        a.next = self.first
        self.first = a

    def set_priority(self,n):
        self.priority = n

    def decrease_key(self, q):
        prio = self.priority
        ndx = prio.ndx
        q.decrease_key(ndx, self.d)


class Dijkstra:
    def __init__(self):
        self.vertices = []
        self.q = MinQueue()

    def add_vertex(self, name):
        n = len(self.vertices)
        v = DijkVertex(name)
        v.n = n
        self.vertices.append(v)
        return v

    def get_vertex(self,name):
        for v in self.vertices:
            if v.name == name:
                return v
        return None

    def print_vertex(self, n, tree):
        a = tree.search(self.vertices[n].name)
        print(a.user_name, end=': ')
        if self.vertices[n].d == INFTY:
            print("not reachable")
        else:
            print(self.vertices[n].d)

    def print_vertices(self,tree):
        for i in range(len(self.vertices)):
            self.print_vertex(i, tree)

    def relax(self, u):
        vset = self.vertices
        q = self.q
        p = u.first
        while p:
            v = p.n
            d = u.d + p.w
            if d < v.d:
                v.d = d
                v.parent = u.n
                v.decrease_key(q)
            p = p.next

    def shortest_path(self):
        q = self.q
        vset = self.vertices
        for v in vset:
            n = PriorNode(v.d, v.n)
            v.set_priority(n)
            q.insert(n)
        while not q.is_empty():
            u = q.extract()
            self.relax(vset[u.n])


class Adj2:
    def __init__(self):
        self.n = 0
        self.next = None


class Vertex2:
    def __init__(self, name):
        self.color = WHITE
        self.parent = -1
        self.name = name
        self.n = 0
        self.first = None

    def add(self, v):
        a = Adj2()
        a.n = v.n
        a.next = self.first
        self.first = a

    def copy(self, other):
        self.color = other.color
        self.parent = other.parent
        self.name = other.name
        self.n = other.n
        self.first = other.first


class DFSVertex(Vertex2):
    def __init__(self, name):
        super().__init__(name)
        self.d = 0
        self.f = 0

    def copy(self, other):
        super().copy(other)
        self.d = other.d
        self.f = other.f


class Queue:
    def __init__(self):
        self.front = 0
        self.rear = 0
        self.sz = 0
        self.buf = []

    def create_queue(self,sz):
        self.sz = sz
        self.buf = list(range(sz))  # malloc(sizeof(int)*sz)

    def enqueue(self,val):
        self.buf[self.rear] = val
        self.rear = (self.rear + 1) % self.sz

    def dequeue(self):
        res = self.buf[self.front]
        self.front = (self.front + 1) % self.sz
        return res

    def is_empty(self):
        return self.front == self.rear


def print_vertex(vertices,n):
    print(vertices[n].name, end=' ')
    print(vertices[n].color, end=' ')
    print(vertices[n].parent, end=' ')
    print(vertices[n].d, end=':')
    p = vertices[n].first
    while p:
        print(vertices[p.n].name, end = ' ')
        p = p.next
    print('')


def g_transpose(vertices, vertices1):
    for i in range(len(vertices1)):
        vertices1[i].first = None
    for v in vertices:
        p = v.first
        while p:
            vertices1[p.n].add(v)
            p = p.next


class DepthFirstSearch:
    def __init__(self):
        self.time = 0
        self.vertices = None

    def set_vertices(self, vertices):
        self.vertices = vertices
        for i in range(len(self.vertices)):
            self.vertices[i].n = i

    def dfs(self):
        for u in self.vertices:
            u.color = WHITE
            u.parent = -1
        self.time = 0
        for u in self.vertices:
            if u.color == WHITE:
                self.dfs_visit(u)

    def dfs_visit(self, u):
        self.time += 1
        u.d = self.time
        u.color = GRAY
        v = u.first
        while v:
            if self.vertices[v.n].color == WHITE:
                self.vertices[v.n].parent = u.n
                self.dfs_visit(self.vertices[v.n])
            v = v.next
        u.color = BLACK
        self.time += 1
        u.f = self.time

    def print_scc(self, u, tree):
        x = tree.search(u.name)
        print(x.user_name, end=" ")
        vset = self.vertices
        if u.parent >= 0:
            self.print_scc(vset[u.parent], tree)

    def scc_find(self, u, tree):
        u.color = GRAY
        v = u.first
        found = False
        while v:
            if self.vertices[v.n].color == WHITE:
                found = True
                self.vertices[v.n].parent = u.n
                self.scc_find(self.vertices[v.n], tree)
            v = v.next
        if not found:
            print("SCC:", end=" ")
            self.print_scc(u, tree)
            print("")
        u.color = BLACK

    def print_vertex(self,n):
        print(self.vertices[n].name, end=' ')
        print(self.vertices[n].color, end=' ')
        print(self.vertices[n].parent, end=' ')
        print(self.vertices[n].d, end=' ')
        print(self.vertices[n].f, end=':')
        p = self.vertices[n].first
        while p:
            print(self.vertices[p.n].name, end = ' ')
            p = p.next
        print('')

    def print_vertices(self):
        for i in range(len(self.vertices)):
            self.print_vertex(i)

    def transpose(self):
        vertices1 = []
        for v in self.vertices:
            v1 = DFSVertex(v.name)
            v1.copy(v)
            vertices1.append(v1)
        g_transpose(self.vertices, vertices1)
        self.set_vertices(vertices1)

    def left(self, n):
        return 2*n+1

    def right(self, n):
        return 2*n+2

    def heapify(self, A, i, heapsize):
        vset = self.vertices
        l = self.left(i)
        r = self.right(i)
        if l < heapsize and vset[A[l]].f < vset[A[i]].f:
            largest = l
        else:
            largest = i
        if r < heapsize and vset[A[r]].f < vset[A[largest]].f:
            largest = r
        if largest != i:
            A[i], A[largest] = A[largest], A[i]
            self.heapify(A, largest, heapsize)

    def buildheap(self, A):
        for i in range(len(A)//2 + 1, 0, -1):
            self.heapify(A, i-1, len(A))

    def heapsort(self, A):
        self.buildheap(A)
        for i in range(len(A), 1, -1):
            A[i-1],A[0] = A[0], A[i-1]
            self.heapify(A, 0, i - 1)

    def sort_by_f(self):
        vset = self.vertices
        sorted_indices = list(range(len(vset)))
        self.heapsort(sorted_indices)
        return sorted_indices

    def scc(self, tree):
        self.dfs()
        #self.print_vertices()
        self.transpose()
        sorted = self.sort_by_f()
        vset = self.vertices
        for v in vset:
            v.color = WHITE
            v.parent = -1
        for n in sorted:
            if self.vertices[n].color == WHITE:
                self.scc_find(vset[n], tree)


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
        self._friends = []  # friends will be saved in linked lists
        self._followers = []  # followers
        self._word = []  # words will be linked lists
        self._num_of_friends = 0
        self._num_of_words = 0

    word = property(fget=lambda self: self._word)
    num_of_words = property(fget=lambda self: self._num_of_words)
    user_name = property(fget=lambda self: self._user_name)
    num_of_friends = property(fget=lambda self: self._num_of_friends)
    followers = property(fget=lambda self: self._followers)
    friends = property(fget=lambda self: self._friends)

    def add_friend(self, friend):
        self._friends.append(friend)
        self._friends = list(set(self._friends))
        self._num_of_friends = len(self._friends)

    def del_friend(self, friend):
        if friend in self._friends:
            self._friends.remove(friend)
            self._num_of_friends = len(self._friends)
        else:
            pass

    def add_follower(self, follower):  # might not be used
        self._followers.append(follower)
        self._followers = list(set(self._followers))

    def del_follower(self, follower):  # might not be used
        if follower in self.followers:
            self._followers.remove(follower)
        else:
            pass

    def add_word(self, input_word):
        self._word.append(input_word)
        self._num_of_words = len(self._word)

    def del_word(self, input_word):
        self._word.remove(input_word)
        self._num_of_words = len(self._word)


class FriendRBNode(RBNode):
    def __init__(self, num_of_friends, user_id, user_name):
        RBNode.__init__(self, num_of_friends)
        self._user_id = user_id
        self._user_name = user_name

    user_name = property(fget=lambda self: self._user_name)
    user_id = property(fget=lambda self: self._user_id)


# for users who have the most tweets
class UserWordRBNode(RBNode):
    def __init__(self, num_of_words, user_id, user_name):
        RBNode.__init__(self, num_of_words)
        self._user_id = user_id
        self._user_name = user_name
        self.visited = False

    user_name = property(fget=lambda self: self._user_name)
    user_id = property(fget=lambda self: self._user_id)


class WordRBNode(RBNode):

    def __init__(self, word):
        RBNode.__init__(self, word)
        self._user = []
        self._num_of_users = 0

    user = property(fget=lambda self: self._user)
    num_of_users = property(fget=lambda self: self._num_of_users)

    def add_user(self, user_id):
        self._num_of_users += 1
        self._user.append(user_id)

    def del_user(self, user_id):
        self._num_of_users -= 1
        self._user.remove(user_id)

    def temp_num_of_users(self):
        return len(self._user)


class WordArrangedRBNode(RBNode):
    def __init__(self, num_of_users, word):
        RBNode.__init__(self, num_of_users)
        self._word = word
        self.visited = False

    word = property(fget=lambda self: self._word)


class RBtree:
    def __init__(self):
        self._nil = RBNode(None)
        self._root = self._nil

    nil = property(fget=lambda self: self._nil)
    Root = property(fget=lambda self: self._root)

    def in_order_walk(self, x=None):
        if x is None:
            x = self.Root
        if x != self.nil:
            self.in_order_walk(x.left)
            print(x.key)
            self.in_order_walk(x.right)

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
            x = self.Root
        while x.left != self.nil:
            x = x.left
        return x

    def maximum(self, x=None):
        if x is None:
            x = self.Root
        while x.left != self.nil:
            x = x.right
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

    def find_all_user_name(self, vertex, x=None):
        if x is None:
            x = self.Root
        if x != self.nil:
            self.find_all_user_name(vertex, x.left)
            vertex.append(x.key)
            self.find_all_user_name(vertex,x.right)

    def insert_node(self, z):
        RBtree.insert_node(self, z)
        self._num_of_users += 1

    def delete_node(self, z):
        RBtree.delete_node(self, z)
        self._num_of_users -= 1

    def delete_fix_up(self, x):
        RBtree.delete_fix_up(self, x)

    num_of_users = property(fget=lambda self: self._num_of_users)


# arranged by number of friends
class FriendRBTree(RBtree):
    def __init__(self):
        RBtree.__init__(self)

    def rearrange_by_friend(self, input_tree, tree, x=None):
        if x is None:
            x = input_tree.Root
        if x != input_tree.nil:
            a = FriendRBNode(x.num_of_friends, x.key, x.user_name)
            tree.insert_node(a)
            self.rearrange_by_friend(input_tree, tree, x.left)
            self.rearrange_by_friend(input_tree, tree, x.right)
        return tree

    def counting(self, x=None):
        count = 0
        if x is None:
            x = self.Root
        if x != self.nil:
            count = x.key + self.counting(x.left) + self.counting(x.right)
        return count


# arranged by number of users in a word
class WordArrangedRBTREE(RBtree):
    def __init__(self):
        RBtree.__init__(self)

    def rearrange_by_friend(self, input_tree, tree, x=None):
        if x is None:
            x = input_tree.Root
        if x != input_tree.nil:
            a = WordArrangedRBNode(x.num_of_users, x.key)
            tree.insert_node(a)
            self.rearrange_by_friend(input_tree, tree, x.left)
            self.rearrange_by_friend(input_tree, tree, x.right)
        return tree

    def backward(self, x=None):
        if x is None:
            x = self.Root
        if x != self.nil:
            self.backward(x.right)
            print(x.word, end=' : ')
            print(x.key, end=' tweets')
            print()
            self.backward(x.left)

    def top_five_words(self, x=None):
        global count_word
        if x is None:
            x = self.Root
        if x != self.nil:
            self.top_five_words(x.right)
            if not x.visited and count_word < 5:
                count_word += 1
                x.visited = True
                print(count_word, end ='. ')
                print(x.word, end=' : ')
                print(x.key, end=' tweets')

                print()
                self.top_five_words(x.left)


# arranged by number of tweets
class UserWordRBTree(RBtree):
    def __init__(self):
        RBtree.__init__(self)

    def rearrange_by_friend(self, input_tree, tree, x=None):
        if x is None:
            x = input_tree.Root
        if x != input_tree.nil:
            a = UserWordRBNode(x.num_of_words, x.key, x.user_name)
            tree.insert_node(a)
            self.rearrange_by_friend(input_tree, tree, x.left)
            self.rearrange_by_friend(input_tree, tree, x.right)
        return tree

    def count_all(self, x=None):  # not used because there is a faster one
        count = 0
        if x is None:
            x = self.Root
        if x != self.nil:
            count = x.key + self.count_all(x.left) + self.count_all(x.right)
        return count

    def count_node(self, x=None):  # not used because there exists a faster one
        count = 0
        if x is None:
            x = self.Root
        if x != self.nil:
            count = 1 + self.count_node(x.left) + self.count_node(x.right)
        return count

    def backward(self, x=None):
        if x is None:
            x = self.Root
        if x != self.nil:
            self.backward(x.right)
            print(x.user_name, end=' : ')
            print(x.key, end=' tweets')
            print()
            self.backward(x.left)

    def top_five_users(self, x=None):
        global count_user
        if x is None:
            x = self.Root
        if x != self.nil:
            self.top_five_users(x.right)
            if not x.visited and count_user < 5:
                count_user += 1
                x.visited = True
                print(count_user, end ='. ')
                print(x.user_name, end=' : ')
                print(x.key, end=' tweets')

                print()
                self.top_five_users(x.left)

    def top_five_users_friend(self, tree, x=None):
        global count_user
        if x is None:
            x = self.Root
        if x != self.nil:
            self.top_five_users_friend(tree, x.right)
            if not x.visited and count_user < 5:
                count_user += 1
               # x.visited = True
                print("Friend of ", end='')
                print(x.user_name, end=' : ')
                alpha = tree.search(x.user_id)
                for friend in alpha.friends:
                    k = tree.search(friend)
                    print(k.user_name, end=' ')
                print()
                self.top_five_users_friend(tree, x.left)


class WordRBTree(RBtree):
    def __init__(self):
        RBtree.__init__(self)
        self._num_of_words = 0

    num_of_words = property(fget=lambda self: self._num_of_words)

    def word_insert_node(self, word, user_id):
        self._num_of_words += 1
        if self.search(word) == self.nil:
            z = WordRBNode(word)
            self.insert_node(z)
            z.add_user(user_id)
        else:
            x = self.search(word)
            x.add_user(user_id)

    def delete_node(self, z):
        self._num_of_words -= z.num_of_users
        RBtree.delete_node(self, z)

    def delete_node2(self, users):
        self._num_of_words -= users


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
                x.add_friend(personB)
                y.add_follower(personA)

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
    global count_user
    global count_word
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
        number = input()
        print()

        if number == '0' or number == '1' or number == '2' or number == '3':
            alpha = FriendRBTree()
            alpha = alpha.rearrange_by_friend(user_tree, alpha)
            count = alpha.counting()

            # num of words a user tweeted
            beta = UserWordRBTree()
            beta = beta.rearrange_by_friend(user_tree, beta)

            # num of users a word has
            gamma = WordArrangedRBTREE()
            gamma = gamma.rearrange_by_friend(word_tree, gamma)
            if number == '0':
                print("Total users: %d" % user_tree.num_of_users)
                print("Total friendship records: %d" % count)
                print("Total tweets: %d" % word_tree.num_of_words)
            elif number == '1':
                print("Average number of friends: %f" % (count / user_tree.num_of_users))
                print("Minimum number of Friends: %d" % alpha.minimum().key)
                print("Maximum number of friends: %d" % alpha.maximum().key)
                print()
                print("Average tweets per user: %f"
                      % (word_tree.num_of_words / user_tree.num_of_users))
                print("Minimum tweets per user: %d" % beta.minimum().key)
                print("Maximum tweets per user: %d" % beta.maximum().key)
            elif number == '2':
                print("Top 5 most tweeted words: ")
                count_word = 0
                gamma.top_five_words()
            elif number == '3':
                print("Top 5 most tweeted users: ")
                count_user = 0
                beta.top_five_users()

        elif number == '4':
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
        elif number == '5':
            count_user = 0
            beta = UserWordRBTree()
            beta = beta.rearrange_by_friend(user_tree, beta)

            print("-------Friends of the Top 5 users-------")
            beta.top_five_users_friend(user_tree)
            print()

            print("------Friends of the people who tweeted above word------")
            if word_node is not word_tree.nil and word_node is not None:
                temp = list(set(word_node.user))
                for person in temp:
                    z = user_tree.search(person)
                    print("Friend of", end=' ')
                    print(z.user_name, end=' ')
                    print(": ", end='')
                    for i in z.friends:
                        fr = user_tree.search(i)
                        print(fr.user_name, end=' ')
                    print()
            else:
                print("No one has tweeted the word!")
        elif number == '6':
            print("Enter an input you want to delete: ", end='')
            input_word = input()
            del_node = word_tree.search(input_word)
            if del_node is not word_tree.nil:
                for person in del_node.user:
                    z = user_tree.search(person)
                    z.del_word(input_word)
                word_tree.delete_node(del_node)
                word_node = None
                print("Delete complete!")
            else:
                print("Nothing to delete!")
        elif number == '7':
            print("Enter an input to delete users who tweeted this word: ", end='')
            input_word = input()
            del_node = word_tree.search(input_word)
            if del_node is not word_tree.nil:
                while del_node.user:
                    for person in del_node.user:
                        z = user_tree.search(person)  # z is a UserRBNode
                        while z.followers:
                            for i in z.followers:
                                tr = user_tree.search(i)
                                if tr is not user_tree.nil and tr is not None:
                                    tr.del_friend(z.key)
                                z.del_follower(i)

                        for i in z.word:
                            k = word_tree.search(i)
                            if z.key in k.user:
                                word_tree.delete_node2(1)
                                k.del_user(z.key)
                                if not k.user:
                                    word_tree.delete_node(k)
                        user_tree.delete_node(z)
                word_node = None
                print("Delete complete!")
            else:
                print("Nothing to delete!")
        elif number == '8':
            vertex = []
            user_tree.find_all_user_name(vertex)
            dfs_ver = [None] * user_tree.num_of_users
            count = 0
            dfs_dic = {}
            for i in vertex:
                dfs_ver[count] = DFSVertex(i)
                count += 1
            for i in dfs_ver:
                dfs_dic[i.name] = i
            DFS = DepthFirstSearch()
            DFS.set_vertices(dfs_ver)
            for i in range(0, user_tree.num_of_users):
                x = user_tree.search(dfs_ver[i].name)  # friend of i (i is user_id)
                for friend in x.friends:
                    a = dfs_dic.get(friend)
                    dfs_ver[i].add(a)
            print("-------- Strongly Connected Components -------")
            DFS.scc(user_tree)
        elif number == '9':
            print("Please enter the start user (ex. 105063898)", end='')
            start_vertex = int(input())
            g = Dijkstra()
            vertex = []
            ver_dic = {}
            user_tree.find_all_user_name(vertex)
            vertex_array = [None] * user_tree.num_of_users

            count = 0
            for i in vertex:
                vertex_array[count] = g.add_vertex(i)
                count += 1

            for i in vertex_array:
                ver_dic[i.name] = i

            for i in range(0, user_tree.num_of_users):
                x = user_tree.search(vertex_array[i].name)
                for friend in x.friends:
                    a = user_tree.search(friend)
                    b = ver_dic.get(friend)
                    vertex_array[i].add(b, a.num_of_friends)
            start_node = ver_dic.get(start_vertex)
            start_node.d = 0
            g.shortest_path()
            g.print_vertices(user_tree)

        elif number == '99':
            break
        else:
            print("Invalid input! Please re-enter")

        print()


main()
