# Java 随机数源码学习

2019-02-02

先看一下JDK源码：

```java
   /**
     * Returns a pseudorandom, uniformly distributed {@code int} value
     * between 0 (inclusive) and the specified value (exclusive), drawn from
     * this random number generator's sequence.  The general contract of
     * {@code nextInt} is that one {@code int} value in the specified range
     * is pseudorandomly generated and returned.  All {@code bound} possible
     * {@code int} values are produced with (approximately) equal
     * probability.  The method {@code nextInt(int bound)} is implemented by
     * class {@code Random} as if by:
     *  <pre> {@code
     * public int nextInt(int bound) {
     *   if (bound <= 0)
     *     throw new IllegalArgumentException("bound must be positive");
     *
     *   if ((bound & -bound) == bound)  // i.e., bound is a power of 2
     *     return (int)((bound * (long)next(31)) >> 31);
     *
     *   int bits, val;
     *   do {
     *       bits = next(31);
     *       val = bits % bound;
     *   } while (bits - val + (bound-1) < 0);
     *   return val;
     * }}</pre>
     *
     * <p>The hedge "approximately" is used in the foregoing description only
     * because the next method is only approximately an unbiased source of
     * independently chosen bits.  If it were a perfect source of randomly
     * chosen bits, then the algorithm shown would choose {@code int}
     * values from the stated range with perfect uniformity.
     * <p>
     * The algorithm is slightly tricky.  It rejects values that would result
     * in an uneven distribution (due to the fact that 2^31 is not divisible
     * by n). The probability of a value being rejected depends on n.  The
     * worst case is n=2^30+1, for which the probability of a reject is 1/2,
     * and the expected number of iterations before the loop terminates is 2.
     * <p>
     * The algorithm treats the case where n is a power of two specially: it
     * returns the correct number of high-order bits from the underlying
     * pseudo-random number generator.  In the absence of special treatment,
     * the correct number of <i>low-order</i> bits would be returned.  Linear
     * congruential pseudo-random number generators such as the one
     * implemented by this class are known to have short periods in the
     * sequence of values of their low-order bits.  Thus, this special case
     * greatly increases the length of the sequence of values returned by
     * successive calls to this method if n is a small power of two.
     *
     * @param bound the upper bound (exclusive).  Must be positive.
     * @return the next pseudorandom, uniformly distributed {@code int}
     *         value between zero (inclusive) and {@code bound} (exclusive)
     *         from this random number generator's sequence
     * @throws IllegalArgumentException if bound is not positive
     * @since 1.2
     */
    public int nextInt(int bound) {
        if (bound <= 0)
            throw new IllegalArgumentException(BadBound);

        int r = next(31);
        int m = bound - 1;
        if ((bound & m) == 0)  // i.e., bound is a power of 2
            r = (int)((bound * (long)r) >> 31);
        else {
            for (int u = r;
                 u - (r = u % bound) + m < 0;
                 u = next(31))
                ;
        }
        return r;
    }
```

先看一下这一段：

```java
if ((bound & m) == 0) // i.e., bound is a power of 2
    r = (int)((bound * (long)r) >> 31);
```

这里很巧妙的用 bound & m 来判断出 bound 是一个2的n次方数字。如果当 bound 是2的n次方，那么只需要通过乘以bound，然后位移，就能按照比例来讲r映射到bound以内，因为刚好是倍数关系。实际上这个方位非常小，因为一共就31个这样的数字。

如果走到了else里面的话，可以想象一个 2^30 &lt; bound &lt; 2^31, 很明显，此时如果将r按照这个比例来缩小的话，在位于这个不等式左边区间的r，会有很大的优势，这个优势会随着 bound 的变大而变大，所以当r“不小心”落在了这个边缘区域的时候，就需要重新生成。可以肯定的是，r落在这个区域的概率是一定小于0.5的，所以这个重新生成的次数也不会太多。

关于如何判断这个r是落在了右边的区域，这里也用了很巧妙的方法：先用u减去u自身对bound的取模，得到的是u里面能被bound整除的部分，如果u真的是在上面提及到的那个“多余的部分”，那么再加上bound-1，就一定会超出 2^31 - 1，这样的话，就会变成负数。

那么这里又有一个问题了，为什么 **u - \(r = u % bound\) + m &lt; 0** 这里是 m 而不是 bound 呢？这里我觉得有点奇怪，因为 **u - \(r = u % bound\)** 之后的值 **u**，大部分情况下只需要加上 bound-1 就可以大于 2^31-1 了，但是如果这个 u 恰好取到了 2^31-1 这个值，并且刚好 bound = 2 ^ 30 ， 那么这个时候是不会满足循环的判断条件的，刚好属于不平均分配，所以我觉得这个时候仍然需要再next一次。不过这个概率太小了。所以这里减去 m 或者 bound 我觉得都是没什么问题的。

最后由于 **r = u % bound** ,所以自然有 r 取值范围是 **\[0,bound\)** 了。

上面写了这么多，我觉得最有用的就是那个判断一个数字是否 2 的 n 次方这个方法了，非常简洁高效。

