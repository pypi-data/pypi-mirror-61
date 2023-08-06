# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project attempts to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

This version finally brings experimental Python 3 support to lib5c!

Currently all tests pass under both Python 2.7 and Python 3.7, but it's possible
that Python 3 bugs exist in areas with low test coverage. We anticipate fixing
these bugs and releasing a new version with "official" Python 3 support soon.

### Added
 - Experimental Python 3 support, see [#54](https://bitbucket.org/creminslab/lib5c/issues/54/add-python3-support).

### Fixed
 - You can now pass a `(positions, labels)` tuple to the `xticks` and `yticks`
   kwargs of a function decorated with `@plotter`, see [#25](https://bitbucket.org/creminslab/lib5c/issues/25/plotting-api-should-support-custom-tick).

### Updates/maintenance
 - Bumped minimum `matplotlib` dependency, see [#59](https://bitbucket.org/creminslab/lib5c/issues/59/importerror-cannot-import-name-to_rgba).
 - Minor documentation improvements, see [#63](https://bitbucket.org/creminslab/lib5c/issues/63/docs-pep-8-link-in-testing-building-and),
   [#64](https://bitbucket.org/creminslab/lib5c/issues/64/docs-installing-from-a-tarball-section-on),
   and [18a7f6](https://bitbucket.org/creminslab/lib5c/commits/18a7f6).
 - Changed testing/linting to use [tox](https://tox.readthedocs.io/en/latest/).
 - Reduced the fragility of many doctest cases that relied on the ordering of
   dictionary keys.
 - Streamlined Docker image build so that building the wheel beforehand is no
   longer necessary, see [#67](https://bitbucket.org/creminslab/lib5c/issues/67/docker-build-should-not-require-any-prereq).
 - We now use [setuptools-scm](https://pypi.org/project/setuptools-scm/) to
   manage version information instead of versioneer.

## 0.5.5 - 2020-02-04

### Changed
 - Enabled extrapolation in `lib5c.util.lowess.lowess_fit()`, see [#60](https://bitbucket.org/creminslab/lib5c/issues/60/lowess_fit-should-allow-extrapolation).

### Updates/maintenance
 - Enforce maximum supported version of `statsmodels` since they are no longer building Python 2 wheels.

## 0.5.4 - 2019-06-07

First wave of major heatmap plotting upgrades plus streamlining of the release
process via Bitbucket Pipelines.

### Added
- A changelog, see [#47](https://bitbucket.org/creminslab/lib5c/issues/47).

### Changed
- ExtendableHeatmap ChIP-seq track and gene track plotting are now faster
  thanks to the use of PolyCollection and LineCollection, see [#28](https://bitbucket.org/creminslab/lib5c/issues/28).

### Fixed
- Bug [#56](https://bitbucket.org/creminslab/lib5c/issues/56).

### Updates/maintenance
- Updated `flake8` configuration (to match previous behavior when using latest
  version of `flake8`).
- Simplified `.gitignore`.
- Tests are now performed by Bitbucket Pipelines on every push.
- Reworked documentation to use [Read the Docs](https://readthedocs.org/).
- Moved tutorials to new `tutorials/` directory under project root.
- Tutorials are now built and published as an independent step in Bitbucket
  Pipelines, separate from the documentation build process.
- Deployment to PyPI and Docker Hub is now performed on tag push by Bitbucket
  Pipelines.

## 0.5.3 - 2018-10-15

First official release, corresponds to what was used in the final version of
[this paper](https://doi.org/10.1016/j.cels.2019.02.006).

## Diffs
- [0.5.5](https://bitbucket.org/creminslab/lib5c/branches/compare/0.5.5..0.5.4#diff)
- [0.5.4](https://bitbucket.org/creminslab/lib5c/branches/compare/0.5.4..0.5.3#diff)
- [0.5.3](https://bitbucket.org/creminslab/lib5c/src/0.5.3)
