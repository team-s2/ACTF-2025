# easy_log

## Background

The idea is from [斐波那契数列 - OI Wiki](https://oi-wiki.org/math/combinatorics/fibonacci/), how can we construct a fib-group mod n.

## Analysis

```python
Point = namedtuple("Point", "x y")
O = "Origin"

def point_addition(P, Q, n):
	if P == O:
		return Q
	if Q == O:
		return P
	x = (P.x * Q.y + P.y * Q.x - P.x * Q.x) % n
	y = (P.x * Q.x + P.y * Q.y) % n
	return Point(x, y)
	
def double_and_add(k, P, n):
	Q = P
	R = O
	while(k > 0):
		if k & 1:
			R = point_addition(R, Q, n)
		k >>= 1
		Q = point_addition(Q, Q, n)
	return R
```

The add operation is

$$x'=x_{0}y_{1}+x_{1}y_{0}-x_{0}x_{1}$$

$$y'=x_{0}x_{1}+y_{0}y_{1}$$

If you write it in matrix form, it becomes:

$$
\left(
\begin{matrix}
y-x & x \\ 
x & y
\end{matrix}
\right)
$$

Then you can just use this matrix to solve this problem, or you can analysis more.

G2 is in the fibonacci sequence, and flag2 * G2 is also the element of fib-group, if you search the Internet you will find the pisano periods, and you can calculate the order of this fib-group.

However, G1 is not a fibonacci sequence according to Cassini's identity. You can just use Cassini's identity, constructing $y^{2}-xy-x^{2}$, which is also a group.

Part 1 is an easy dlp, you can quickly solve it, Part 2 asks you to find a smooth p, and solve it like part 1.