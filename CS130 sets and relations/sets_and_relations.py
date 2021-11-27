from itertools import chain, combinations, product

# Change this to generate a larger sample
NUMBER = 200
# Both of the sets below give an idea of what a relation or similar would
# do the the set Z, N or R, but are not necessarily accurate.
Z = tuple(range(-NUMBER, NUMBER+1)) # A sample of integers
N  = tuple(range(0, NUMBER+1)) # A sample of natural numbers
R = tuple([x/100 for x in Z]) # A sample of real numbers

#---------------- PREDEFINED FUNCTIONS ----------------#

# Takes a set and returns it's power set
def power_set(s):
    return tuple(chain.from_iterable(combinations(s, x) for x in range(len(s)+1)))

# Takes two sets, a and b, and returns their cartesian product
def cartesian_product(a,b):
    return tuple(product(a,b))

# Takes an element a, a relation and a set and returns the equivalence classes
def equivalence_class(a, r, s):
    return tuple([x for x in s if (a,x) in r])

# Takes a set and a relation and generates the quotient
def quotient(s, r):
    return tuple({equivalence_class(a, r, s) for a in s if equivalence_class(a, r, s) != ()})

# Takes two sets and returns the union
def union(s1,s2):
    return tuple(set(s1 + s2))

# Takes two sets and returns the intersection
def intersection(s1,s2):
    return tuple([x for x in s1 if x in s2])

# Takes two sets and returns the set difference
def set_minus(s1,s2):
    return tuple([x for x in s1 if x not in s2])

# Returns the equivalence relation for s1 and s2
def equivalence_relation(s1,s2):
    return [(x,y) for x,y in cartesian_product(s1,s2) if x == y]

# Returns the equinumerosity relation for s1 and s2
def equinumerosity_relation(s1,s2):
    return [(a,b) for a, b in cartesian_product(s1,s2) if len(a) == len(b)]

# Does some dodgy formatting to change python tuples into
# something resembling a set. Not very reliable.
def setify(s):
    return str(s).replace(",)", "}").replace(")","}").replace("(", "{").replace("{}", "∅").replace("'", "")

#------------------------------------------------------#

# Define your own functions here:

def example_1():
    r = equivalence_relation(N,N)
    print("Pairs in set:")
    print((1,2) in r) # Is the pair (1,2) in the equivalence relation
    print((6,6) in r) # True

    c = (1,2,3)
    print("Power set:\n", power_set(c)) # The power set of c
    print("Formatted power set:\n", setify(power_set(c))) # The formatted power set of c

    r2 = [(x,y) for x,y in cartesian_product(N,N) if x > y] # > relation on natural numbers

    e = equivalence_class(34, r2, N) # The equivalence class [34] for the set N related by r2
    print("Equivalence class [34]:\n",e)

    q = sorted(quotient(N, r)) # The quotient of the natural numbers and the equivalence relation
    print("Quotient:\n",q) # This is [(x) for x in natural numbers]

def example_2():
    # Problem set 3, question 1a
    s = (1,2,3,4,5)
    f = [(x,6-x) for x in s]
    g = [(x,min(3,x)) for x in s]
    h = [(x,x) for x in s]
    print(f)
    print(g)
    print(h)

def example_3():
    # Problem set 2, question 8c
    # NOTE: NUMBER needs to be set to at least 800 for this to work
    def Q(a,b):
        return a==b
    r = [(a,b) for a,b in cartesian_product(N,N) if a-b <= 5 and Q(a,b)]
    print(equivalence_class(800, r, N))

def example_4():
    # From "Set cardinality 01-2 Equinumerosity and set cardinality" lecture
    s = ('a','b','c')
    s2 = power_set(s)
    e = equinumerosity_relation(s2,s2)
    q = sorted(quotient(s2, e))
    print(q)

def example_5():
    # From "Relations 02-5 Equivalence relations: examples" lecture
    # This is the congruence mod 12 relation on the natural numbers
    r = [(x,y) for x,y in cartesian_product(N,N) if x-y % 12 == 0]
    q = sorted(quotient(Z,r))
    # In the lecture, it is said that the quotient is equal to the set of equivalence classes
    # These were described as the residue classes mod 12
    e = sorted([equivalence_class(x, r, Z) for x in range(12)])
    print(q)
    print(e == q) # True

# Call the functions here:
example_5()
    
