## The `transferer` Class

Two types of threads access `obj`, a `transferer` object:

### Caller Threads

They execute `obj.call` and block until the result is returned.

1. Extractor threads
