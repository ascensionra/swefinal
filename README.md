
# **SWE Midterm 2 Review**

This is the review for the second midterm in Downing's CS373 Software Engineering class. 

The topics to be reviewed are:

 - [Python](#python)
 - [XML and JSON](#xml-and-json)
 - [SQL](#sql)
 - [Refactoring and Design Patterns](#refactoring-and-design-patterns)

## **Python**


----------


##### **Subtopics:**

 - [Variables](#variables)
 - [Closures](#closures)
 - [Methods](#methods)
 - [Functions](#functions)
 - [Decorators](#decorators)

### **Variables**

#### **Global**
Global variables can be accessed in python by using the `global` delimiter.

```python
v1 = 1
v2 = 2
v3 = 3

def f():
	assert v1 == 1
	
	v2 = 12 # local

	global v3
	v3 = 15

f()

assert v1 == 1
assert v2 == 2
assert v3 == 15
```

#### **Class**
Class variables in python are always accessible, even the 'private' ones. Private class variables need to be prefixed with `__`, but even these can still be accessed.

```python
class A:
	v0 = 0 # normal class variable
	v1 = v0 + 1 # accessing its own class variable to make another
	__v2 = v1 + 1 # __v2 and _A__v2 become synonymous
	_A__v3 = __v2 + 1 # __v3 and _A__v3 become synonymous
	_A__v3 = _A__v2 + 1

assert hasattr(A, "v0")
assert A.v0 == 0
assert A.__dict__["v0"] == 0

assert hasattr(A, "v1")
assert A.v1 == 1
assert A.__dict__["v1"] == 1

assert not hasattr(A, "__v2") # __v2 is private
assert hasattr(A, "_A__v2") # not really!

A.__v2 = [2, 3, 4]
assert hasattr(A, "__v2") # this is different that the private __v2
assert hasattr(A, "_A__v2")
assert A.__v2 == [2, 3, 4]
assert A.__v2 is not A._A__v2
```

### **Closures**

#### **What is a CLOSURE?**
A CLOSURE is a function object that remembers values in enclosing scopes regardless of whether those scopes are still present in memory.

#### **Basic Example**
Observe the following function `generate_power_func`, which returns another function.
```python
def generate_power_func(n):
	print("id(n):", id(n))
	def nth_power(x):
		return x**n
	print("id(nth_power):", id(nth_power))
	return nth_power
```
The inner function `nth_power` is called a *closure* because it has access to n, which is defined in `generate_power_func` (the enclosing scope) even after program flow leaves it. You can see here that even in deleting `generate_power_func`, the `nth_power` function still has access to `n`.
```python
>>> to_the_4 = generate_power_func(4)
id(n): CCF7DC
id(nth_power): C46630
>>> repr(to_the_4)
'<function nth_power at 0x00C46630>'
>>> del generate_power_func
>>> to_the_4(2)
16
```

#### **Privacy Example**
Here we can create a class with an instance variable that is almost truly private.

```python
def A():
	a = [] # Variable we want to be private

	class B: # class we return with access to variable 'a'
		def get (self):
			return a
		
		def add (self, v):
			a.append(v)

	return B()
```

The function `A()` above returns class B that has access to variable `a`, but doesn't have it within its dictionary, making `a` similar to a private variable in Java. Here are some examples of the constraints on accessing this variable.

```python
x = A()
assert x.get() == [] # we can access B's get() method
x.add(2)
assert x.get() == [2] # B's add() works as well
x.add(3)
assert x.get() == [2, 3]
#x.a += [4] # AttributeError: 'A' object has no attribute 'a'
# we cannot access 'a' as a variable of an 'A' object
assert x.get() == [2, 3]
#del x.a # AttributeError: a
assert "a" not in x.__dict__
x.a = None # this works, but it isn't the same 'a'!
assert "a" in x.__dict__
assert x.get() == [2, 3]
```  

[More on Closures](http://www.shutupandship.com/2012/01/python-closures-explained.html)
### **Methods**
Python includes several types of methods when creating classes. The following example shows the constructor method `__init__`, a static method `cm`, and an instance method `im`.

```python
class A:
	__cv = 0 # class variable
	
	def __init__ (self) :
		A.__cv += 1
		self.__iv = 0 #  private instance variable
		#cm() # NameError: global name 'cm' is not defined
		A.cm() # this works
		#im() # NameError: global name 'im' is not defined
		#A.im() #TypeError: unbound method im() must be called with A instance
		self.im() # this works

	@staticmethod
	def cm () :
		A.__cv += 1
		#self.__iv += 1 # NameError: global name 'self' is not defined

	def im (self) :
		A.__cv += 1
		self.__iv += 1
		#cm()  # NameError: global name 'cm' is not defined
		A.cm()
		self.cm()   # misleading

A.cm()

x = A()
x.cm()
#A.cm(x) # does not work

x.im() 
A.im(x) # methods are really just functions!
```

### **Functions**
Python includes different types of functions such as `FunctionType`, `LambdaType` and `MethodType`. Below we show the difference.

```python

def plus_1 (x, y) :
	return x + y

assert type(plus_1) is FunctionType
assert hasattr(plus_1, "__call__")
assert plus_1(2, 3) == 5
assert reduce(plus_1, [2, 3, 4]) == 9

plus_2 = lambda x, y : x + y

assert type(plus_2) is LambdaType
assert hasattr(plus_2, "__call__")
assert plus_2(2, 3) == 5
reduce(plus_2, [2, 3, 4]) == 9

class Plus_3 (object) :
	def my_call (self, x, y) :
		return x + y

assert type(Plus_3()) is Plus_3
assert Plus_3().my_call(2, 3) == 5

assert type(Plus_3.my_call) is FunctionType
assert hasattr(Plus_3.my_call, "__call__")
#Plus_3.my_call(2, 3) # TypeError: unbound method my_call() must be called with Plus_3 instance as first argument (got int instance instead
assert Plus_3.my_call(Plus_3(), 2, 3) == 5
#reduce(Plus_3.my_call, [2, 3, 4]) # TypeError: unbound method my_call() must be called with Plus_3 instance as first argument (got int instance instead

assert type(Plus_3().my_call) is MethodType
assert str(Plus_3().my_call)[1:6] == "bound"
assert hasattr(Plus_3().my_call, "__call__")
assert Plus_3().my_call(2, 3) == 5
assert reduce(Plus_3().my_call, [2, 3, 4]) == 9

class Plus_4 (object) :
    @staticmethod
    def my_call (x, y) :
        return x + y

assert type(Plus_4.my_call) is FunctionType
assert hasattr(Plus_4.my_call, "__call__")
assert Plus_4.my_call(2, 3) == 5
assert reduce(Plus_4.my_call, [2, 3, 4]) == 9

class Plus_5 (object) :
    def __call__ (self, x, y) :
        return x + y

assert type(Plus_5()) is Plus_5
assert hasattr(Plus_5(), "__call__")
assert Plus_5()(2, 3) == 5
assert reduce(Plus_5(), [2, 3, 4]) == 9
```

### **Decorators**

#### **What is a DECORATOR?**
A decorator is just a callable that takes a function as an argument and returns a replacement function.

```python
>>> def outer(some_func):
...     def inner():
...         print "before some_func"
...			ret = some_func() # 1
...			return ret + 1
...     return inner
>>> def foo():
...     return 1
>>> decorated = outer(foo) # 2
>>> decorated()
before some_func
2
```

Python allows us to wrap a function anytime using the @ symbol.

```python
>>> add = wrapper(add) # without the @ symbol
>>> @wrapper # this is the same effect, but nicer syntax
... def add(a, b):
... 	return Coordinate(a.x + b.x, a.y + b.y)
```

[More on Decorators](http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/)

[back to top](#swe-midterm-2-review)
## **XML and JSON**


----------


##### **Subtopics:**

 - [Basic XML](#basic-xml)
 - [DTD XML](#dtd-xml)
	 - [Basic DTD](#basic-dtd)
	 - [Using ID and IDREFS](#using-id-and-idrefs)
 - [XSD XML](#xsd-xml)
 - [JSON](#json)

### **Basic XML**
Extensible Markup Language (XML) is  markup language that defines a set of rules for encoding documents in a format which is both human-readable and machine-readable.  It is useful for representing data the is being transferred between a database and a client.

```xml
<Bookstore>
   <Book ISBN="ISBN-0-13-713526-2" Price="85" Edition="3rd">
      <Title>A First Course in Database Systems</Title>
      <Authors>
         <Author>
            <First_Name>Jeffrey</First_Name>
            <Last_Name>Ullman</Last_Name>
         </Author>
         <Author>
            <First_Name>Jennifer</First_Name>
            <Last_Name>Widom</Last_Name>
         </Author>
      </Authors>
   </Book>
   <Book ISBN="ISBN-0-13-815504-6" Price="100">
      <Title>Database Systems: The Complete Book</Title>
      <Authors>
         <Author>
            <First_Name>Hector</First_Name>
            <Last_Name>Garcia-Molina</Last_Name>
         </Author>
         <Author>
            <First_Name>Jeffrey</First_Name>
            <Last_Name>Ullman</Last_Name>
         </Author>
         <Author>
            <First_Name>Jennifer</First_Name>
            <Last_Name>Widom</Last_Name>
         </Author>
      </Authors>
      <Remark>
      Buy this book bundled with "A First Course" - a great deal!
      </Remark>
   </Book>
</Bookstore>
```

### **DTD XML**
A document type definition (DTD) is a set of markup declarations that define a document type for a markup language such as XML. DTD defines the legal building blocks of an XML document.

#### **Basic DTD**

```xml
<!DOCTYPE Bookstore [
   <!ELEMENT Bookstore  (Book | Magazine)*>
   <!ELEMENT Book       (Title, Authors, Remark?)>
   <!ELEMENT Title      (#PCDATA)>
   <!ELEMENT Authors    (Author+)>
   <!ELEMENT Author     (First_Name, Last_Name)>
   <!ELEMENT First_Name (#PCDATA)>
   <!ELEMENT Last_Name  (#PCDATA)>
   <!ELEMENT Remark     (#PCDATA)>
   <!ELEMENT Magazine   (Title)>

   <!ATTLIST Book ISBN    CDATA #REQUIRED
                  Price   CDATA #REQUIRED
                  Edition CDATA #IMPLIED>

   <!ATTLIST Magazine Month CDATA #REQUIRED
                      Year  CDATA #REQUIRED>
]>

<Bookstore>
   <Book ISBN="ISBN-0-13-713526-2" Price="85" Edition="3rd">
      <Title>A First Course in Database Systems</Title>
      <Authors>
         <Author>
            <First_Name>Jeffrey</First_Name>
            <Last_Name>Ullman</Last_Name>
         </Author>
         <Author>
            <First_Name>Jennifer</First_Name>
            <Last_Name>Widom</Last_Name>
         </Author>
      </Authors>
   </Book>
   <Book ISBN="ISBN-0-13-815504-6" Price="100">
      <Title>Database Systems: The Complete Book</Title>
      <Authors>
         <Author>
            <First_Name>Hector</First_Name>
            <Last_Name>Garcia-Molina</Last_Name>
         </Author>
         <Author>
            <First_Name>Jeffrey</First_Name>
            <Last_Name>Ullman</Last_Name>
         </Author>
         <Author>
            <First_Name>Jennifer</First_Name>
            <Last_Name>Widom</Last_Name>
         </Author>
      </Authors>
      <Remark>
         Buy this book bundled with "A First Course" - a great deal!
      </Remark>
   </Book>
</Bookstore>
```

#### **Using ID and IDREFS**

```xml
<!DOCTYPE Bookstore [
   <!ELEMENT Bookstore  (Book*, Author*)>
   <!ELEMENT Book       (Title, Remark?)>
   <!ELEMENT Title      (#PCDATA)>
   <!ELEMENT Remark     (#PCDATA | BookRef)*>
   <!ELEMENT BookRef    EMPTY>
   <!ELEMENT Author     (First_Name, Last_Name)>
   <!ELEMENT First_Name (#PCDATA)>
   <!ELEMENT Last_Name  (#PCDATA)>

   <!ATTLIST Book ISBN    ID     #REQUIRED
                  Price   CDATA  #REQUIRED
                  Authors IDREFS #REQUIRED>

   <!ATTLIST BookRef book  IDREF #REQUIRED>
   <!ATTLIST Author  Ident ID    #REQUIRED>
]>

<Bookstore>
   <Book ISBN="ISBN-0-13-713526-2" Price="100" Authors="JU JW">
      <Title>A First Course in Database Systems</Title>
   </Book>
   <Book ISBN="ISBN-0-13-815504-6" Price="85" Authors="HG JU JW">
      <Title>Database Systems: The Complete Book</Title>
      <Remark>
         Amazon.com says: Buy this book bundled with
         <BookRef book="ISBN-0-13-713526-2" /> - a great deal!
      </Remark>
   </Book>
   <Author Ident="HG">
      <First_Name>Hector</First_Name>
      <Last_Name>Garcia-Molina</Last_Name>
   </Author>
   <Author Ident="JU">
      <First_Name>Jeffrey</First_Name>
      <Last_Name>Ullman</Last_Name>
   </Author>
   <Author Ident="JW">
      <First_Name>Jennifer</First_Name>
      <Last_Name>Widom</Last_Name>
   </Author>
</Bookstore>
```

### **XSD XML**
The XML Schema Definition language (XSD) enables you to define the structure and data types for XML documents.

```xml
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <xsd:element name="Bookstore">
      <xsd:complexType>
         <xsd:sequence>
            <xsd:element name="Book" type="BookType"
                         minOccurs="0" maxOccurs="unbounded" />
            <xsd:element name="Author" type="AuthorType"
                         minOccurs="0" maxOccurs="unbounded" />
         </xsd:sequence>
      </xsd:complexType>
      <xsd:key name="BookKey">
         <xsd:selector xpath="Book" />
         <xsd:field xpath="@ISBN" />
      </xsd:key>
      <xsd:key name="AuthorKey">
         <xsd:selector xpath="Author" />
         <xsd:field xpath="@Ident" />
      </xsd:key>
      <xsd:keyref name="AuthorKeyRef" refer="AuthorKey">
         <xsd:selector xpath="Book/Authors/Auth" />
         <xsd:field xpath="@authIdent" />
      </xsd:keyref>
      <xsd:keyref name="BookKeyRef" refer="BookKey">
         <xsd:selector xpath="Book/Remark/BookRef" />
         <xsd:field xpath="@book" />
      </xsd:keyref>
   </xsd:element>
   <xsd:complexType name="BookType">
      <xsd:sequence>
         <xsd:element name="Title" type="xsd:string" />
         <xsd:element name="Authors">
            <xsd:complexType>
               <xsd:sequence>
                  <xsd:element name="Auth" maxOccurs="unbounded">
                     <xsd:complexType>
                        <xsd:attribute name="authIdent" type="xsd:string"
                                       use="required" />
                     </xsd:complexType>
                  </xsd:element>
               </xsd:sequence>
            </xsd:complexType>
         </xsd:element>
         <xsd:element name="Remark" minOccurs="0">
            <xsd:complexType mixed="true">
               <xsd:sequence>
                  <xsd:element name="BookRef" minOccurs="0"
                               maxOccurs="unbounded">
                     <xsd:complexType>
                        <xsd:attribute name="book" type="xsd:string"
                                       use="required" />
                     </xsd:complexType>
                  </xsd:element>
               </xsd:sequence>
            </xsd:complexType>
         </xsd:element>
      </xsd:sequence>
      <xsd:attribute name="ISBN" type="xsd:string" use="required" />
      <xsd:attribute name="Price" type="xsd:integer" use="required" />
   </xsd:complexType>
   <xsd:complexType name="AuthorType">
      <xsd:sequence>
         <xsd:element name="First_Name" type="xsd:string" />
         <xsd:element name="Last_Name" type="xsd:string" />
      </xsd:sequence>
      <xsd:attribute name="Ident" type="xsd:string" use="required" />
   </xsd:complexType>
</xsd:schema>
```

### **JSON**
JSON Schema is a JSON media type for defining the structure of JSON data. JSON Schema provides a contract for what JSON data is required for a given application and how to interact with it.

**Schema**

```json
{ "type":"object",
  "properties": {
     "Books": {
        "type":"array",
        "items": {
           "type":"object",
           "additionalProperties":true,
           "properties": {
              "ISBN": { "type":"string", "pattern":"ISBN*" },
              "Price": { "type":"integer",
                         "minimum":0, "maximum":200 },
              "Edition": { "type":"integer", "optional": true },
              "Remark": { "type":"string", "optional": true },
              "Title": { "type":"string" },
              "Authors": {
                 "type":"array",
                 "minItems":1,
                 "maxItems":10,
                 "items": {
                    "type":"object",
                    "properties": {
                       "First_Name": { "type":"string", "optional":true },
                       "Last_Name": { "type":"string" }}}}}}},
     "Magazines": {
        "type":"array",
        "items": {
           "type":"object",
           "properties": {
              "Title": { "type":"string" },
              "Month": { "type":"string",
                         "enum":["January","February"] },
              "Year": { "type":["integer", "string"] }}}}
}}
```

**JSON**

```json
{ "Books":
  [
    { "ISBN":"ISBN-0-13-713526-2",
      "Price":85,
      "Edition":3,
      "Title":"A First Course in Database Systems",
      "Authors":[ {"First_Name":"Jeffrey", "Last_Name":"Ullman"},
                  {"First_Name":"Jennifer", "Last_Name":"Widom"} ] }
    ,
    { "ISBN":"ISBN-0-13-815504-6",
      "Price":100,
      "Remark":"Buy this book bundled with 'A First Course' - a great deal!",
      "Title":"Database Systems:The Complete Book",
      "Authors":[ {"First_Name":"Hector", "Last_Name":"Garcia-Molina"},
                  {"First_Name":"Jeffrey", "Last_Name":"Ullman"},
                  {"First_Name":"Jennifer", "Last_Name":"Widom"} ] }
  ],
  "Magazines":
  [
    { "Title":"National Geographic",
      "Month":"January",
      "Year":2009 }
    ,
    { "Title":"Newsweek",
      "Month":"February",
      "Year":"2009" }
  ]
}
```

[back to top](#swe-midterm-2-review)
## **SQL**


----------


##### **Subtopics:**

 - [Relational Algebra](#relational-algebra)
	 - [Select](#select)
	 - [Project](#project)
	 - [Cross Join](#cross-join)
	 - [Theta Join](#theta-join)
	 - [Natural Join](#natural-join)
 - [Joins](#joins)
 - [Subqueries](#subqueries)
 - [Sets](#sets)
 - [Aggregation](#aggregation)
 - [Insert, Update, Delete](#insert,-update,-delete)

### **Relational Algebra**
This section focuses on implementing and explaining relational algebra functionality in Python.
#### **Select**
Selection in relational algebra is an operation that selects tuples that satisfy the given predicate from a relation. The example below shows how selection works in python.

```python
def select (r, up) :
    return (v for v in r if up(v))

R = [{"A" : 1, "B" : 4, "C" : 3},
	{"A" : 2, "B" : 5, "C" : 2},
	{"A" : 3, "B" : 6, "C" : 1}]

assert list(select(R, lambda d : d["B"] > 4)) == 
	[{'A': 2, 'B': 5, 'C': 2},
	{'A': 3, 'B': 6, 'C': 1}])

```

#### **Project**
Projection in relational algebra is an operation that projects column(s) that satisfy a given predicate. The python example below shows how projection works.

```python
def project (r, *t) :
    return ({a : v[a] for a in t if a in v} for v in r)

R = [{"A" : 1, "B" : 4, "C" : 3},
	{"A" : 2, "B" : 5, "C" : 2},
	{"A" : 3, "B" : 6, "C" : 1}]

assert list(project(R, "B")) ==
		[{'B': 4},
		{'B': 5},
		{'B': 6}])
```
#### **Cross Join**
The Cross Join combines each tuple in relation R with each tuple in relation S.

```python
def cross_join (r, s) :
    return (dict(u, **v) for u in r for v in s)

r = [{"A" : 1, "B" : 4},
	{"A" : 2, "B" : 5},
	{"A" : 3, "B" : 6}]

s = [{"C" : 2, "D" : 7},
	{"C" : 3, "D" : 5},
	{"C" : 3, "D" : 6},
	{"C" : 4, "D" : 6}]

assert list(cross_join(r, s)) ==
	[{'A': 1, 'B': 4, 'C': 2, 'D': 7},
	{'A': 1, 'B': 4, 'C': 3, 'D': 5},
	{'A': 1, 'B': 4, 'C': 4, 'D': 6},
	{'A': 2, 'B': 5, 'C': 2, 'D': 7},
	{'A': 2, 'B': 5, 'C': 3, 'D': 5},
	{'A': 2, 'B': 5, 'C': 3, 'D': 6},
	{'A': 2, 'B': 5, 'C': 4, 'D': 6},
	{'A': 3, 'B': 6, 'C': 2, 'D': 7},
	{'A': 3, 'B': 6, 'C': 3, 'D': 5},
	{'A': 3, 'B': 6, 'C': 3, 'D': 6},
	{'A': 3, 'B': 6, 'C': 4, 'D': 6}]
```

#### **Theta Join**
Theta Join is essentially a Cross Join with a predicate.

```python
def theta_join (r, s, bp) :
    return (dict(u, **v) for u in r for v in s if bp(u, v))

r = [{"A" : 1, "B" : 4},
	{"A" : 2, "B" : 5},
	{"A" : 3, "B" : 6}]

s = [{"C" : 2, "D" : 7},
	{"C" : 3, "D" : 5},
	{"C" : 3, "D" : 6},
	{"C" : 4, "D" : 6}]

assert list(theta_join(r, s, lambda u, v : u["A"] == v["C"])) ==
	[{'A': 2, 'B': 5, 'C': 2, 'D': 7},
	{'A': 3, 'B': 6, 'C': 3, 'D': 5},
	{'A': 3, 'B': 6, 'C': 3, 'D': 6}]
```
#### **Natural Join**
The Natural Join is a Cross Join where at least one column in R matches one column in S.

```python
def match (u, v) :
    for a in u :
        for b in v :
            if (a == b) and (u[a] == v[b]) :
                return True
    return False

def natural_join (r, s) :
    return (dict(u, **v) for u in r for v in s if match(u, v))

r = [{"A" : 1, "B" : 4},
	{"A" : 2, "B" : 5},
	{"A" : 3, "B" : 6}]

s = [{"A" : 2, "D" : 7},
	{"A" : 3, "D" : 5},
	{"A" : 3, "D" : 6},
	{"A" : 4, "D" : 6}]

assert list(natural_join(r, s)) ==
	[{'A': 2, 'B': 5, 'D': 7},
	{'A': 3, 'B': 6, 'D': 5},
	{'A': 3, 'B': 6, 'D': 6}]
```

### **Joins**
This section deals with SQL joins and gives examples of the types of problems.

![SQL JOINS](https://d1b10bmlvqabco.cloudfront.net/attach/i563clif2i169a/gy0uzhyjabbsm/i98vn8cb5qm7/Visual_SQL_JOINS_orig.jpg)


----------


### **Subqueries**
This section deals with subqueries and gives examples of how they can be used.

#### **Examples**

----------


**Table Setup**
```sql
create table Student (
	sID int,
	sName text,
	GPA float,
	sizeHS int);

create table Apply (
	sID int,
	cName text,
	major text,
	decision boolean);

create table College (
	cName text,
	state char(2),
	enrollment int);
```


----------


**ID, name, and GPA of students who applied to CS:**

First, let's try this:
```sql
select sID, sName, GPA
	from Student
	inner join Apply using (sID)
	where major = 'CS';
```
This is not right, since we could get duplicate sID's if a student applied to multiple schools.

Here is the correct version:
```sql
select distinct sID, sName, GPA
	from Student
	inner join Apply using (sID)
	where major = 'CS';
```
Or we could also use a subquery like this:

```sql
select sID, sName, GPA
	from Student
	where sID in
		(select sID
			from Apply
			where major = 'CS');
```


----------
**GPA of students who applied in CS**

First, let's try this:
```sql
select GPA
	from Student
	inner join Apply using (sID)
	where major = 'CS'
	order by GPA desc;
```

This is not right, since we could get duplicates, so let's try this:

```sql
select distinct GPA
	from Student
	inner join Apply using (sID)
	where major = 'CS'
	order by GPA desc;
```

This is still not right, since we don't want distinct GPAs, we want distinct students to get the GPAs for. Let's try this using a subquery.

```sql
select GPA
	from Student
	where sID in
		(select sID
			from Apply
			where major = 'CS')
	order by GPA desc;
```


----------
**ID of students who have applied in CS but not in EE**

First, let's try this:
```sql
select sID
	from Student
	where
		sID in (select sID from Apply where major = 'CS')
		and
		sID in (select sID from Apply where major != 'EE');
```

This doesn't work, since we want to get students not in EE, not students in everything but EE (there is a difference). Here is our correction:

```sql
select sID
	from Student
	where
		sID     in (select sID from Apply where major = 'CS')
		and 
		sID not in (select sID from Apply where major = 'EE');
```

This is also right:
```sql
select distinct sID
	from Apply
	where
		(major = 'CS')
		and
		sID not in (select sID from Apply where major = 'EE');
```


----------
**Colleges with another college in the same state**

First, let's use an inner join:
```sql
select distinct R.cName, R.state
	from College as R
	inner join College as S
	where (R.cName != S.cName) and
		  (R.state = S.state);
```

Using a subquery and exists:
```sql
select cName, state
	from College as R
	where exists
		(select *
			from College as S
			where (R.cName != S.cName) and
			(R.state =  S.state));
```

Using a subquery, with group by and having:
```sql
select cName, state
	from College
	natural join
		(select State
			from College
			group by State
			having count(State) > 1) as T;
```

----------


### **Sets**

**Union**
```sql
select sName as csName from Student
union
select cName as csName from College
order by csName;
```

**Intersect**

Using Inner Join:
```sql
select *
	from
		(select sName as csName from Student) as R
		inner join
		(select cName as csName from College) as S
		using (csName);
```

Using subquery:
```sql
select sName as csName
	from Student
	where sName in
		(select cName
			from College);
```

Using subquery, with exists:
```sql
select sName as csName
	from Student
	where exists
		(select *
			from College
			where sName = cName);
```

**Difference**

Using a subquery, with not in:
```sql
select sID
	from Student
	where sID not in
		(select sID
			from Apply);
```

Using a subquery, with not exists:
```sql
select sID
	from Student
	where not exists
		(select *
			from Apply
			where Student.sID = Apply.sID);
```


----------


### **Aggregation**

**Stats on GPA of Students**
```sql
select count(*) 
	from Student;

select GPA
	from Student;

select avg(GPA)
	from Student;

select max(GPA)
	from Student;

select min(GPA)
	from Student;

select sum(GPA)
	from Student;
```

**Number of students who applied to Cornell**
```sql
select count(distinct sID)
	from Apply
	where cName = "Cornell";
```

**Majors whose applicant's max GPA is less than the average**
```sql
select major
	from Student
	inner join Apply using (sID)
	group by major
	having
		max(GPA)
		<
		(select avg(GPA) from Student);
```


----------


### **Insert, Update, Delete**

**Have students who did not apply, apply to Carnegie Mellon in CS**
```sql
insert into Apply
	select sID, 'Carnegie Mellon', 'CS', null
		from Student
		where sID not in
			(select sID
				from Apply);
```

**Delete students who applied to two or more majors**
```sql
delete
	from Student
	where sID in
		(select sID
			from Apply
			group by sID
			having count(distinct major) > 2);
```

**Update applications form Cornell to UT for those with GPA < 3.6 and have them accepted**
```sql
update Apply
	set cName = 'UT', decision = true
	where
		(cName = 'Cornell')
		and
		sID in
			(select sID
				from Student
				where GPA < 3.6);
```

[back to top](#swe-midterm-2-review)

## **Refactoring and Design Patterns**


----------


##### **Subtopics:**

 - [Inheritance](#inheritance)
 - [Composition](#composition)
 - [Refactoring](#refactoring)
	 - [Extract Method](#extract-method)
	 - [Move Method](#move-method)
	 - [Replace Conditional with Polymorphism](#replace-conditional-with-polymorphism)
	 - [Replace Temp with Query](#replace-temp-with-query)
	 - [Replace Type Code with State](#replace-type-code-with-state)
	 - [Replace Type Code with Subclasses](#replace-type-code-with-subclasses)
 - [Design Patterns](#design-patterns)
	 - [Singleton](#singleton)
	 - [Factory Method](#factory-method)
	 - [Abstract Factory](#abstract-factory)


----------
### **Inheritance**
In object-oriented programming, inheritance is when an object of class is based on another object of class, using the same implementation (inheriting from a class) specifying implementation to maintain the same behavior (realizing an interface; inheriting behavior).

```Java
// here we create a class named fruit
class Fruit {
	String name;

	public Fruit(String n) {
		this.name = n;
	}

	public String toString() {
		return this.name;
	}
}

// here we create a class 'Apple' that extends class 'Fruit'
class Apple extends Fruit {
	private boolean hasWorm;
	
	public Apple() {
		super("Apple");
		hasWorm = false;
	}

	public boolean hasWorm() {
		return hasWorm;
	}

	public void setWorm(boolean flag) {
		this.hasWorm = flag;
	}
}

public static void main(String[] args) {
	Fruit fruit = new Fruit("Random Name"); // this is a random fruit
	Apple apple = new Apple(); // this is an Apple
	Fruit fruit_apple = new Apple(); // this is a Fruit, that is actually an Apple
	
	System.out.println(fruit); // Random Name
	
	System.out.println(apple); // Apple
	
	System.out.println(fruit_apple); // Apple

	System.out.println(apple.hasWorm()); // false
	
	//System.out.println(fruit_apple.hasWorm()) // does not work, Fruit does not have a method called hasWorm
	
	// here we cast fruit_apple to be Apple
	System.out.println(((Apple)fruit_apple).hasWorm() // false
	
	//System.out.println(fruit.hasWorm()); // obviously this doesn't work either!
}
```


----------
### **Composition**
Composition over inheritance is the principle that classes should achieve polymorphic behavior and code reuse by composition (containing other classes that implement the desired functionality), instead of through inheritance (being a subclass).


----------
### **Refactoring**

#### **Extract Method**
You have a code fragment that can be grouped together.

```java
void printOwing() {
	printBanner();
	
	//print details
	System.out.println ("name: " + _name);
	System.out.println ("amount " + getOutstanding());	
	
}
```

*Turn the fragment into a method whose name explains the purpose of the method*

```java
void printOwing() {
	printBanner();
	printDetails(getOutstanding());
}

void printDetails (double outstanding) {
	System.out.println ("name:  " + _name);
	System.out.println ("amount " + outstanding);
}
```


#### **Move Method**
A method is, or will be, using or used by more features of another class than the class which it is defined.

*Create a new method with a similar body in the class it uses most. Either turn the old method into a simple delegation, or remove it altogether.*

```java
class Project {
	Person [] participants;
}

class Person {
	int id;
	boolean participate(Project p) {
		for (int i = 0; i < p.participants.length; i++) {
			if (p.participants[i].id == id) return (true);
		}
		return (false);
	}
}

... if (x.participate(p)) ...
```

After applying the move you end up with:
```java
class Project {
	Person[] participants;
	boolean participate(Person x) {
		for (int i = 0; i < participants.length; i++) {
			if (participants[i].id == x.id) return (true);
		}
		return (false);
	}
}

class Person {
	int id;
}

... if (p.participate(x)) ...
```


#### **Replace Conditional with Polymorphism**
You have a conditional that chooses different behavior depending on the type of an object.

*Move each leg of the conditional to an overriding method in a subclass. Make the original method abstract.*

```java
double getSpeed() {
	switch (_type) {
		case EUROPEAN:
			return getBaseSpeed();
		case AFRICAN:
			return getBaseSpeed() - getLoadFactor() * _numberOfCoconuts;
		case NORWEGIAN_BLUE:
			return (_isNailed) ? 0 : getBaseSpeed(_voltage);
	}
	throw new RuntimeException("Should be unreachable");
}
```

After the move:
```java
class Bird {
	...
	double getSpeed() {
		return getBaseSpeed();
	}
	...
}

class European extends Bird {
	double getSpeed() {
		return super.getSpeed();
	}
}

class African extends Bird {
	double getSpeed() {
		return getBaseSpeed() - getLoadFactor() * _numberOfCoconuts;		
	}
}

class NorwegianBlue extends Bird {
	double getSpeed() {
		return (_isNailed) ? 0 : getBaseSpeed(_voltage);
	}
}
```

#### **Replace Temp with Query**
You are using a temporary variable to hold the result of an expression.

*Extract the expression into a method. Replace all references to the temp with the new expression. The new method can then be used in other methods.*

```java
double basePrice = _quantity * _itemPrice;
if (basePrice > 1000)
	return basePrice * 0.95;
else
	return basePrice * 0.98;
```

After the extraction:
```java
if (basePrice() > 1000)
	return basePrice() * 0.95;
else
	return basePrice() * 0.98;
...
double basePrice() {
	return _quantity * _itemPrice;
}
```

#### **Replace Type Code with State**
You have a type code that affects the behavior of a class, but you cannot use subclassing.

*Replace the type code with a state object*

```java
class Employee {
	final static int ENGINEER = 1
	final static int SALESMAN = 2
	int type;
	...
}
```

After the replacement:
```java
class Employee {
	EmployeeType type;
	...
}

abstract class EmployeeType {
	static final int ENGINEER = 1;
	static final int SALESMAN = 2;
	
	abstract int getTypeCode();
	...
}

class Engineer extends EmployeeType {
	int getTypeCode() {
		return EmployeeType.ENGINEER;
	}
}

class Salesman extends EmployeeType {
	int getTypeCode() {
		return EmployeeType.SALESMAN;
	}
}
```

Better example [here](https://sourcemaking.com/refactoring/replace-type-code-with-state-strategy)

#### **Replace Type Code with Subclasses**
You have an immutable type code that affects the behavior of a class.

*Replace the type code with subclasses*

```java
class Employee...
	private int _type;
	static final int ENGINEER = 0;
	static final int SALESMAN = 1;
	static final int MANAGER = 2;

	Employee (int type) {
		_type = type;
	}
```

The first step is to use `Self Encapsulate Field` on the type code:

```java
int getType() {
	return _type;
}
```

Because the employee's constructor uses a type code as a parameter, I need to replace it with a factory method:
```java
Employee create(int type) {
	return new Employee(type);
}

private Employee (int type) {
	_type = type;
}
```

I can now start with engineer as a sublcass. First I create the subclass and the overriding method for the type code:
```java
class Engineer extends Employee {
	int getType() {
		return Employee.ENGINEER;
	}
}
```
I also need to alter the factory method to create the appropriate object:
```java
class Employee...
	static Employee create(int type) {
		if (type == ENGINEER) return new Engineer();
		else return new Employee(type);
	}
```
I continue, one by one, until all the codes are replaced with subclasses. At this point I can get rid of the type code field on employee and make getType an abstract method. At this point the factory method looks like this:
```java
abstract int getType();
static Employee create(int type) {
	switch (type) {
		case ENGINEER:
			return new Engineer();
		case SALESMAN:
			return new Salesman();
		case MANAGER:
			return new Manager();
		default:
			throw new IllegalArgumentException("Incorrect type code value");
	}
}
```
Of course this is the kind of switch statement I would prefer to avoid. But there is only one, and it is only used at creation.

Naturally once you have created the subclasses you should use `Push Down Method` and `Push Down Field` on any methods and fields that are relevant only for particular types of employee.

> [More on Refactoring](http://refactoring.com/)
> [Even more on Refactoring](https://sourcemaking.com/refactoring)

### **Design Patterns**

#### **Singleton**
Singleton pattern is one of the simplest design patterns in Java. This type of design pattern comes under creational pattern as this pattern provides one of the best ways to create an object.

This pattern involves a single class which is responsible to create an object while making sure only that single object gets created.

```java
public class SingleObject {
	//create an object of SingleObject
	private static SingleObject instance = new SingleObject();

	//make the constructor private so that this class cannot be instantiated
	private SingleObject(){}

	//get the only object available
	public static SingleObject getInstance() {
		return instance;
	}

	public void showMessage() {
		System.out.println("Hello World!");
	}
}
```
> You can also to "lazy initialization" (creation on first use) within the accessor function 

#### **Factory Method**
`Factory Method` is to create objects as `Template Method` is to implementing an algorithm. A superclass specifies all standard and generic behavior, and then delegates the creation details to subclasses that are supplied by the client.

```java
public interface Product {...}

public abstract class Creator {
	public void anOperation() {
		Product product = factoryMethod();
	}

	protected abstract Product factoryMethod();
}

public class ConcreteProduct implements Product {...}

public class ConcreteCreator extends Creator {
	protected Product factoryMethod() {
		return new ConcreteProduct();
	}
}

public class Client {
	public static void main( String[] arg ) {
		Creator creator = new ConcreteCreator();
		creator.anOperation();
	}
}
```

#### **Abstract Factory**
The purpose of the `Abtract Factory` is to provide an interface for creating families of related objects, without specifying concrete classes.

`Abstract Factory` classes are often implemented with `Factory Methods`, but they can also be implemented using Prototype. Abstract Factory might store a set of Prototypes from which to clone and return product objects.
+ Factory Method: creation through inheritance.
+ Prototype: creation through delegation.
+ Virtual Constructor: defer choice of object to create until run-time.


**Example**
```java
public abstract class CPU
{
  ...
} // class CPU

class EmberCPU extends CPU
{
  ...
} // class EmberCPU

class EmberToolkit extends ArchitectureToolkit
{
  public CPU createCPU()
  {
    return new EmberCPU();
  } // createCPU()

  public MMU createMMU()
  {
    return new EmberMMU();
  } // createMMU()
  ...
} // class EmberFactory

public abstract class ArchitectureToolkit
{
  private static final EmberToolkit emberToolkit = new EmberToolkit();
  private static final EnginolaToolkit enginolaToolkit = new EnginolaToolkit();
  ...

  // Returns a concrete factory object that is an instance of the
  // concrete factory class appropriate for the given architecture.
  static final ArchitectureToolkit getFactory(int architecture)
  {
    switch (architecture)
    {
      case ENGINOLA:
        return enginolaToolkit;

      case EMBER:
        return emberToolkit;
        ...
    } // switch
    String errMsg = Integer.toString(architecture);
    throw new IllegalArgumentException(errMsg);
  } // getFactory()

  public abstract CPU createCPU();
  public abstract MMU createMMU();
  ...
} // AbstractFactory
 
public class Client
{
  public void doIt()
  {
    AbstractFactory af;
    af = AbstractFactory.getFactory(AbstractFactory.EMBER);
    CPU cpu = af.createCPU();
    ...
  } // doIt
} // class Client
```

**Another example:**

```java
public class FactoryFmProto {
	static class Expression {
		protected String str;
		public Expression(String s) {
			str = s;
		}
		public Expression cloan() {
			return null;
		}
		public String toString() {
			return str;
		}
	}
	
	static abstract class Factory
    {
        protected Expression prototype = null;
        public Expression makePhrase()
        {
            return prototype.cloan();
        }
        public abstract Expression makeCompromise();
        public abstract Expression makeGrade();
    }

    static class PCFactory extends Factory
    {
        public PCFactory()
        {
            prototype = new PCPhrase();
        }
        public Expression makeCompromise()
        {
            return new Expression("\"do it your way, any way, or no way\"");
        }
        public Expression makeGrade()
        {
            return new Expression("\"you pass, self-esteem intact\"");
        }
    }

    static class NotPCFactory extends Factory
    {
        public NotPCFactory()
        {
            prototype = new NotPCPhrase();
        }
        public Expression makeCompromise()
        {
            return new Expression("\"my way, or the highway\"");
        }
        public Expression makeGrade()
        {
            return new Expression("\"take test, deal with the results\"");
        }
    }

    public static void main(String[] args)
    {
        Factory factory;
        if (args.length > 0)
            factory = new PCFactory();
        else
            factory = new NotPCFactory();
        for (int i = 0; i < 3; i++)
            System.out.print(factory.makePhrase() + "  ");
        System.out.println();
        System.out.println(factory.makeCompromise());
        System.out.println(factory.makeGrade());
    }

    static class PCPhrase extends Expression
    {
        static String[] list = 
        {
            "\"animal companion\"", "\"vertically challenged\"", 
                "\"factually inaccurate\"", "\"chronologically gifted\""
        };
        private static int next = 0;
        public PCPhrase()
        {
            super(list[next]);
            next = (next + 1) % list.length;
        }
        public Expression cloan()
        {
            return new PCPhrase();
        }
    }

    static class NotPCPhrase extends Expression
    {
        private static String[] list = 
        {
            "\"pet\"", "\"short\"", "\"lie\"", "\"old\""
        };
        private static int next = 0;
        public NotPCPhrase()
        {
            super(list[next]);
            next = (next + 1) % list.length;
        }
        public Expression cloan()
        {
            return new NotPCPhrase();
        }
    }
}
```

> [More on Design Patterns](https://sourcemaking.com/design_patterns)

[back to top](#swe-midterm-2-review)
