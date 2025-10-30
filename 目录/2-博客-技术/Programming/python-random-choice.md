# Python random choice

2019-02-02

```python
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(random.choice(a))
print(random.choices(a, [0, 0, 0, 0, 0, 0, 0, 0, 1], k=1))
```

根据官方文档 [https://docs.python.org/3/library/random.html](https://docs.python.org/3/library/random.html) ，从3.6开始，python有了一个新的伪随机array生成方法。

上图的2行输出，第一行是输出 a 中的一个随机元素。第二行是输出随机的一个list，长度是k，并且可以自己加权重，权重也是一个list。这个函数看上去非常好用，在数据处理的时候很不错。

