# Backupy

Python script for backup files and directories. **Save your files from loss or damage.**

[![Build Status](https://travis-ci.com/KonstantinPankratov/Backupy.svg?branch=master)](https://travis-ci.com/KonstantinPankratov/Backupy)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/KonstantinPankratov/Backupy/blob/master/LICENSE)

## Quickstart

```python
from Backupy import Backupy

backup = Backupy()
backup.add_directory('/var/www/html/assets/')
backup.start()
```

[Follow here](examples) for more examples.