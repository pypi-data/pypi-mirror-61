# qt-ci-util
Some basic python methods for building CI for qt projects.

## Usage

```
pip install qtciutil
```

Script example:

```python
import qtciutil
# Get Qt Version
qt_version_str = qtciutil.qt_version()
# Build Qt Project
qtciutil.build('/home/l2m2/workspace/xxx/src/xxx.pro', '/home/l2m2/workspace/xxx/build', 'debug')
# Unit Test
qtciutil.unit_test('/home/l2m2/workspace/xxx/test/test.pro', '/home/l2m2/workspace/xxx/build', '/home/l2m2/workspace/xxx/dist')
```

## License
MIT

## Publish to PyPI

```
pip install --user --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```

## Reference

- https://juejin.im/post/5d8814adf265da03be491737