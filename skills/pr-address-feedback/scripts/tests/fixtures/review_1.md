> @reviewer reviewed 2 files and made 3 comments.
> *[Reviewable](https://reviewable.io/reviews/org/repo/1)* status: 3 unresolved discussions.

___
*[`src/foo.swift` line 10 at r1](https://reviewable.io/reviews/org/repo/1#-ThreadA:-ThreadA:b-123) ([raw file](https://github.com/org/repo/blob/abc/src/foo.swift#L10)):*
> ```swift
> let x = 1
> ```

Why is x hardcoded?

___
*[`src/bar.swift` line 20 at r1](https://reviewable.io/reviews/org/repo/1#-ThreadB:-ThreadB:b-456) ([raw file](https://github.com/org/repo/blob/abc/src/bar.swift#L20)):*
> ```swift
> let y = compute()
> ```

This function seems expensive, should it be cached?

___
*[`src/baz.swift` line 30 at r1](https://reviewable.io/reviews/org/repo/1#-ThreadC:-ThreadC:b-789) ([raw file](https://github.com/org/repo/blob/abc/src/baz.swift#L30)):*
> ```swift
> return nil
> ```

Returning nil here seems dangerous.

<!-- Sent from Reviewable.io -->
