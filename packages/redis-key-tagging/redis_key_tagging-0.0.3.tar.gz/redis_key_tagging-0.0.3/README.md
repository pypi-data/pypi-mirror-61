# Redis Key Tagging

## Description

This package provides key tagging and invalidation by tag features.
It provides the ``RedisKeyTagging`` class which extends the ``Redis`` class from
[redis-py](https://github.com/andymccurdy/redis-py), so it can be switched seamlessly.

## Documentation

### Overriden method(s)

* ``set()``: The new optional keyword argument ``tags``, which must be a list of string, can be used
to associate the key being set to each of those tags.

### New method(s)

* ``delete_keys_by_tag()``: Delete all keys associated with the given tag.

## Tests

```
$ py.test
```
