# QueryTree

QueryTree is a python data structure that lets you quickly access deeply nested data and load/save it in any major format.

With QueryTree, you don't have to check for the esistance of (or create) any intermediate nodes.

```python
json_str = """
{
    "foo": {
        "bar": [
            {
                "baz": {
                    "n": 1
                }
            },
            {
                "baz": {
                    "n": 1
                },
                "buz": {
                    "k": 2
                }
            }
        ]
    }
}
"""

tree = Tree.parse_json(json_str)
print(tree['foo.bar.0.baz.n'])  # 1
print(tree['foo.bar.1.buz.k'])  # 2

# accessing nonexistant locations isn't a problem
print(tree['foo.bar.0.buz.k'])  # None
print(tree['something.else'])   # None

# assign values
tree['foo.bar.0.baz.n'] = 99
tree['foo.foo'] = {"myvalue": "a value"}

# save as any format
print(tree.to_yaml())
```
Outputs:
```yaml
foo:
  bar:
  - baz:
      n: 99
  - baz:
      n: 1
    buz:
      k: 2
  foo:
    myvalue: a value
```
