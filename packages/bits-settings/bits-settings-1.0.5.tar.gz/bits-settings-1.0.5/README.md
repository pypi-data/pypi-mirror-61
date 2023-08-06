# bits-bitsdb
BITSdb Python Package

By default, this looks for settings in "etc/config.yaml".

Example usage:

```
"""Example usage of bits-settings."""
from bits.settings import Settings

filename = '/path/to/my/config.yaml'

s = Settings(filename)

settings = s.get()
```
