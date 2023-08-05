# Changelog

## [1.6][2020-02-07]

### Changed

- converted old CircleCI 1.0 job to 2.0
- added tox to be able to run locally and CircleCI
- updated README with working images
- refactored setup.py so that numpy is not required to be installed when running `setup.py` commands
- fixed some flake8 issues
- black-ified coode
- fixed tests code to support py35+
- updated cpp library with the latest cython 0.29.14 (previously 0.23.4)

## [1.5][2020-01-28]

### Changed

- removed pytest from `install_requires`

## [1.4][2019-12-16]

### Changed

- pinned libraries to python2 friendly versions.
- removed stdint include to allow compiling with MSVC

## [1.3][2016-01-22]

### Changed

- all interior nodes of a tree at a given depth now share their hyperplane. This drastically reduces the memory footprint
  of the tree without affecting the guarantees of the data structure (which relies on the hyperplanes being independently drawn
  _between_ the trees in the forest
- this changes the structure of the model pickles, but pickles of older versions should continue to deserialize correctly

## [1.2][2016-01-06]

### Changed

- `fit` can be safely called multiple times on the same model instance.
- `shrink_to_fit` removed, reducing dependency on C++11 stdlib.
- not calling `float` on the Cython version any more.
