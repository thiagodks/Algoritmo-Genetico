import functools

class A:
	def trackcalls(func):
	    @functools.wraps(func)
	    def wrapper(*args, **kwargs):
	        wrapper.has_been_called = True
	        return func(*args, **kwargs)
	    wrapper.has_been_called = False
	    return wrapper		

	@trackcalls
	def example(self):
	    pass

	def teste(self):

		if self.example.has_been_called:
		   print("foo bar")


a = A()
# a.example()
a.teste()
#Actual Code!: