[![PyPI version](https://badge.fury.io/py/tinyaes.svg)](https://badge.fury.io/py/tinyaes)

# tiny-AES-c Cython wrapper

`tinyaes` is a few lines Cython wrapper for the
[`tiny-AES-c`](https://github.com/kokke/tiny-AES-c), a _Small portable
AES128/192/256 in C_.

The library offers a few modes, CTR mode is the only one currently wrapped.
Given the C API works modifying a buffer inplace, the wrapper offers:

- `CTR_xcrypt_buffer(..)` that works on all bytes convertible types, and
  encrypting a copy of the buffer,
- `CTR_xcrypt_buffer_inplace(..)` that works on `bytearray`s only, modifying
  the buffer inplace.

## Release notes

- 1.0.0a2 (Jan 29, 2020): first public release
- 1.0.0a3 (Feb 7, 2020): fix bytes inplace mutation error
