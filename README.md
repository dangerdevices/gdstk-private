# GDSTK

Danger Devices internal fork of [gdstk](https://github.com/heitzmann/gdstk); primarily used by [Florist](https://github.com/dangerdevices/florist).

## About

Gdstk (GDSII Tool Kit) is a C++ library for creation and manipulation of GDSII and OASIS files.
It is also available as a Python module meant to be a successor to [Gdspy](https://github.com/heitzmann/gdspy).

Key features for the creation of complex CAD layouts are included:

* Boolean operations on polygons (AND, OR, NOT, XOR) based on clipping algorithm
* Polygon offset (inward and outward rescaling of polygons)
* Efficient point-in-polygon solutions for large array sets

## Differences from upstream

Major differences from upstream include:

- Increased performance of OASIS serialization: [#156](https://github.com/dangerdevices/gdstk-private/pull/156)
- Improved geometry accuracy: [#129](https://github.com/dangerdevices/gdstk-private/pull/129), [#199](https://github.com/dangerdevices/gdstk-private/pull/199)
- Library objects are copy-able: [#132](https://github.com/dangerdevices/gdstk-private/pull/132)
- OASIS encoding fixes: [#203](https://github.com/dangerdevices/gdstk-private/pull/203), [#208](https://github.com/dangerdevices/gdstk-private/pull/208)
- Layer filtering when reading GDSII and OASIS files: [#214](https://github.com/dangerdevices/gdstk-private/pull/214)

## Development

Install a compiler supporting C++ 11, CMake 3.26 or newer, and [`uv`](https://github.com/astral-sh/uv).

`pyproject.toml` is configured to install gdstk in editable mode, but because it is implemented with native code, you must run a build command after making changes to the headers or source files. Use `uv sync` with the `--reinstall-package` flag, which triggers a rebuild:

```
uv sync --reinstall-package gdstk
```

Use `pytest` to run the tests:

```
uv run pytest
```

### Debugging

To build gdstk with debug info included, uncomment `cmake.build-type = "debug"` in `pyproject.toml`, then run the build command above.

```
uv sync --reinstall-package gdstk
```

You can then use `lldb` or `gdb` to run a test in the debugger, setting breakpoint(s) as necessary. Note that the full path to the Python binary must be specified, which is given by `uv run which python`.

```
lldb $(uv run which python) -- -m pytest tests/cell_test.py::test_bb
```

Python loads shared libraries lazily, so gdstk is normally not accessible to the debugger until `import gdstk` runs. This makes it difficult to accurately set breakpoints before starting a unit test. LLDB's `target modules add` command can be used to eagerly load gdstk (note that the directory and file name will change depending on the platform you're using).

```
(lldb) target modules add build/cp313-cp313-macosx_15_0_arm64/python/_gdstk.cpython-313-darwin.so
```

Finally, set the desired breakpoint(s), and run the test:

```
(lldb) break set -n cell_object_bounding_box
Breakpoint 1: where = _gdstk.cpython-313-darwin.so`cell_object_bounding_box(CellObject*, _object*) + 20 at cell_object.cpp:233:5, address = 0x000000000002a6e4

(lldb) r
Process 76075 launched: '/Users/jatoben/Developer/dangerdevices/gdstk-private/.venv/bin/python' (arm64)
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0 -- /Users/jatoben/Developer/dangerdevices/gdstk-private/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/jatoben/Developer/dangerdevices/gdstk-private
configfile: pyproject.toml
collected 1 item

tests/cell_test.py::test_bb Process 76075 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
    frame #0: 0x0000000100ec66e4 _gdstk.cpython-313-darwin.so`cell_object_bounding_box(self=0x0000000101177690, (null)=0x0000000000000000) at cell_object.cpp:233:5
   230
   231  static PyObject* cell_object_bounding_box(CellObject* self, PyObject*) {
   232      Vec2 min, max;
-> 233      self->cell->bounding_box(min, max);
   234      if (min.x > max.x) {
   235          Py_INCREF(Py_None);
   236          return Py_None;
```

### Integration tests

Florist's test suite includes more thorough exercises for most of gdstk's functionality, including integration tests drawn from real designs. If you make any non-trivial changes to gdstk, it's a good idea to run them past the full Florist test suite as well as the tests in this repository.
