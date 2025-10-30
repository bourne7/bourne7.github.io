# 寻找含环的单链表的入口点

> 本文来自 https://blog.csdn.net/wuzhekai1985/article/details/6725263 本来也是个转载的，但是最终原文连接打不开了。。

问题1：如何判断单链表中是否存在环（即下图中从结点E到结点R组成的环）？

设一快一慢两个指针（Node *fast, *low）同时从链表起点开始遍历，其中快指针每次移动长度为2，慢指针则为1。则若无环，开始遍历之后fast不可能与low重合，且fast或fast->next最终必然到达NULL；若有环，则fast必然不迟于low先进入环，且由于fast移动步长为2，low移动步长为1，则在low进入环后继续绕环遍历一周之前fast必然能与low重合（且必然是第一次重合）。于是函数可写如下：


```c++
bool hasCircle(Node *head, Node *&encounter) {
    Node *fast = head, *slow = head;
    while (fast && fast->next) {
        fast = fast->next->next;
        slow = slow->next;
        if (fast == slow) {
            encounter = fast;
            return true;
        }
    }
    encounter = NULL;
    return false;
}
```

问题2：若存在环，如何找到环的入口点（即上图中的结点E）？

如图中所示，设链起点到环入口点间的距离为x，环入口点到问题1中fast与low重合点的距离为y，又设在fast与low重合时fast已绕环n周（n>0），且此时low移动总长度为s，则fast移动总长度为2s，环的长度为r。则
```
    s + nr = 2s,n>0     ①
    s = x + y           ②
    由①式得  s = nr                 
    代入②式得
    nr = x + y
    x = nr - y          ③
```

现让一指针p1从链表起点处开始遍历，指针p2从encounter处开始遍历，且p1和p2移动步长均为1。则当p1移动x步即到达环的入口点，由③式可知，此时p2也已移动x步即nr - y步。由于p2是从encounter处开始移动，故p2移动nr步是移回到了encounter处，再退y步则是到了环的入口点。也即，当p1移动x步第一次到达环的入口点时，p2也恰好到达了该入口点。于是函数可写如下：

```c++
Node *findEntry(Node *head, Node *encounter) {
    Node *p1 = head, *p2 = encounter;
    while (p1 != p2) {
        p1 = p1->next;
        p2 = p2->next;
    }
    return p1;
}
```
总结：
取一快一慢2个点的速度必须是 1 和 2 的速度，否则有可能遇不上。如果是双向链表的话，可以在构建链表的时候就排除掉这种现象。