
# pklcache

The name stands for pickle cache, and it is a quick and *dirty* way of caching function results on disk using `pickle`.

This can be helpful for example in some machine learning tasks, where you have to preprocess the data with many time-consuming steps, and you want to not recompute things every time you run your program. 

### Example
```
from pklcache import cache

@cache("foo_cache.pkl")
def foo(args):
    # time consuming operations here...
    return result
```
If you run the program
```
result = foo()  #foo executed
```
And if you run it again
```
result = foo()  #foo not executed, load result from disk
```

The first time `foo` is called its result is saved on disk on `foo_cache.pkl`. If then the function is called another time or the program is run again, `foo` is not executed, instead its return value is loaded from disk and returned.


### Args

`@cache(fpath, enabled=True)`
- `fpath`: is the cache file path
- `enabled`: if `False` the store/load is disabled and the function is executed like if it wasn't decorated. Useful during development and debugging.  
