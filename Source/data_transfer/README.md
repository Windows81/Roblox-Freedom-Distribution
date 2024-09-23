## The `transferer` Class

There are two types of threads which access `obj`, which is a `transferer` object:

### Caller Threads

They execute `obj.call(a, b)` with some arbitary argument data and block (i.e., wait) until the result is returned. The `a` and `b` refer to that data.

### Extractor Threads

From `(a, b) = obj.extract()`, they take queued data that was previously specified in `obj.call`. They do something with that data and return the result `r`. That result is passed into `obj.insert(r)` is then forwarded to the caller thread.

In RFD, extractor threads cycle through `"/rfd/data-transfer"` in a hard-to-explain way.

Ask VisualPlugin directly if you need further advice.
