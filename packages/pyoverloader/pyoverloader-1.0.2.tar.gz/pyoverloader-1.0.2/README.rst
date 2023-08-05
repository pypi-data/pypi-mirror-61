pyover
Another python overloading library

Usage: ::
  from pyover import overload, This

  class Foo:
  
    @overload(This, int) # We need to add 'This' to overload method (class or instance)
    def bar(self, x):
      print(x**2)
    
    @bar.overload(This, str)
    def bar(self, x):
      print(x + x)
    
  @overload(int, int)
  def spam(x, y):
    print(x - y)

  @spam.overload(str, int)
  def spam(x, y):
    print(x + " - %i" % y)

  obj = Foo()
  obj.bar(3) # 9
  obj.bar('egg') # eggegg

  spam(3, 2) # 1
  spam('3', 2) # 3 - 2 
