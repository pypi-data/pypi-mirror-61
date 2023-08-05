# DRFTypeGen

**DRFTypeGen** is a app to enable user to generate type information for various languages.

## Why?
Nowadays we use statically-typed languages in many consumer apps for our APIs. Of course there are 'schemas' to describe your API but generating types are better. This will enable projects to generate relevant type file(s) for using in other projects.

## Installation
1. Install from pip:

   ```bash
   pip install drftypgen
   ```

2.  Add `drftypegen` in your `INSTALLED_APP`.

## Usage
### TypeScript
```python
from drftypgen.compilers import TypeScriptCompiler
tscompiler = TypeScriptCompiler()
types_data = tscompiler.generate()

```
Now you can save the `types_data` in file or serve in a view.

Or, you can generate TypeScript File with this management command with optional filename with `--file` option:

```bash
./manage.py genTSTypes
```

## TODO
1. ~~Support for Wagtail~~
2. Support for Dart
