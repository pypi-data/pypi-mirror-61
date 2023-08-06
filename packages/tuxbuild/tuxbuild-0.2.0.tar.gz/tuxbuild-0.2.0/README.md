<div align="center">
  <img src="https://gitlab.com/Linaro/tuxbuild/raw/master/tuxbuild_logo.png" alt="TuxBuild Logo" width="50%" />
</div>

# TuxBuild

[![Pipeline Status](https://gitlab.com/Linaro/tuxbuild/badges/master/pipeline.svg)](https://gitlab.com/Linaro/tuxbuild/pipelines)
[![coverage report](https://gitlab.com/Linaro/tuxbuild/badges/master/coverage.svg)](https://gitlab.com/Linaro/tuxbuild/commits/master)
[![PyPI version](https://badge.fury.io/py/tuxbuild.svg)](https://pypi.org/project/tuxbuild/)
[![Docker Pulls](https://img.shields.io/docker/pulls/tuxbuild/tuxbuild.svg)](https://hub.docker.com/r/tuxbuild/tuxbuild)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - License](https://img.shields.io/pypi/l/tuxbuild)](https://gitlab.com/Linaro/tuxbuild/blob/master/LICENSE)

The _fun_ Linux kernel builder

TuxBuild is a cloud-native highly concurrent Linux build service.

![tuxbuild screencast](https://people.linaro.org/~dan.rue/tuxbuild/demo.gif "tuxbuild screencast")

## Status: Early Access

Tuxbuild is currently under active development, but we want to hear from you!
If you are interested in joining the waiting list, or have questions, feedback,
or feature requests, please email us at tuxbuild@linaro.org.

## Install Using PIP

TuxBuild requires Python version 3.6 or greater, and is available using pip.

To install tuxbuild on your system globally:
```
sudo pip3 install -U tuxbuild
```

To install tuxbuild to your home directory at ~/.local/bin:
```
pip3 install -U --user tuxbuild
```

To upgrade tuxbuild to the latest version, run the same command you ran to
install it.

## Install Using Docker

TuxBuild is also available as a docker container at
[tuxbuild/tuxbuild](https://hub.docker.com/r/tuxbuild/tuxbuild).

For example, to run tuxbuild via docker:

```
docker run tuxbuild/tuxbuild tuxbuild build --help
```

## Setup

The Authentication token needs to be stored in `~/.config/tuxbuild/config.ini`.
The minimal format of the ini file is given below:

```
$ cat ~/.config/tuxbuild/config.ini
[default]
token=vXXXXXXXYYYYYYYYYZZZZZZZZZZZZZZZZZZZg
```

Alternatively, the `TUXBUILD_TOKEN` environment variable may be provided.

## Examples

### Tuxbuild one-off

Submit a build request using the tuxbuild command line interface. This will
wait for the build to complete before returning by default.

```
tuxbuild build --git-repo 'https://github.com/torvalds/linux.git' --git-ref master --target-arch arm64 --kconfig defconfig --toolchain gcc-9
```

### Tuxbuild set

Create a tuxbuild config file with a basic set of build combinations defined.

```
cat <<EOF > basic.yaml
sets:
  - name: basic
    builds:
      - {target_arch: arm64, toolchain: gcc-9, kconfig: defconfig}
      - {target_arch: arm64, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: arm64, toolchain: gcc-9, kconfig: allyesconfig}
      - {target_arch: arm, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: x86, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: x86, toolchain: clang-9, kconfig: allmodconfig}
      - {target_arch: x86, toolchain: gcc-9, kconfig: allyesconfig}
      - {target_arch: i386, toolchain: gcc-9, kconfig: allmodconfig}
      - {target_arch: riscv, toolchain: gcc-9, kconfig: allyesconfig}
EOF
# Build the build set defined in the config file named 'basic.yaml'
tuxbuild build-set --git-repo 'https://github.com/torvalds/linux.git' --git-ref master --tux-config basic.yaml --set-name basic
```

All the parameters can be specified in the build-set itself and invoke tuxbuild "tuxbuild build-set  --tux-config <basic>.yaml --set-name <set-name>"

## Argument Reference

### target_arch
target_arch supports `arm64`, `arm`, `x86`, `i386`, `mips`, `arc`, `riscv`

### toolchain
toolchain supports `gcc-8`, `gcc-9`, `clang-8`, `clang-9`

### kconfig

The kconfig argument is a string or a list of strings that are used to define
what kernel config to use.

The first argument must be a defconfig argumnet that ends in "config", such as
"defconfig" or "allmodconfig".

Subsequent arguments may be specified to enable/disable individual config
options, an config fragment that exists in tree at `kernel/configs/`, or a url
to an externally hosted config fragment.

All config options and fragments specified will be merged in the order that
they are specified.

#### kconfig Examples

Simple defconfig build:
- `tuxbuild --kconfig defconfig ...`
- yaml (string): `kconfig: defconfig`
- yaml (list): `kconfig: [defconfig]`

Enable or disable individual options:
- `tuxbuild --kconfig defconfig --kconfig "CONFIG_COMPILE_TEST=y" --kconfig
  "CONFIG_PROFILE_ALL_BRANCHES=n"`
- yaml: `kconfig: [defconfig, "CONFIG_COMPILE_TEST=y",
  "CONFIG_PROFILE_ALL_BRANCHES=n"]`

Using external fragment files:
- `tuxbuild --kconfig defconfig --kconfig
  "https://gist.githubusercontent.com/danrue/9e1e4d90149daadd5199256cc18a0499/raw/752138764ec039e4593185bfff888250a3d7692f/gistfile1.txt"`
- yaml: `kconfig: [defconfig,
  "https://gist.githubusercontent.com/danrue/9e1e4d90149daadd5199256cc18a0499/raw/752138764ec039e4593185bfff888250a3d7692f/gistfile1.txt"]`

Using in-tree fragment files. The file referenced needs to exist in
`kernel/configs/`:
- `tuxbuild --kconfig defconfig --kconfig "kvm_guest.config"`
- yaml: `kconfig: [defconfig, "kvm_guest.config"]`

All of these options can be combined. They will be merged in the order they are
specified:
- `tuxbuild --kconfig allnoconfig --kconfig "kvm_guest.config" --kconfig
  "https://gist.githubusercontent.com/danrue/9e1e4d90149daadd5199256cc18a0499/raw/752138764ec039e4593185bfff888250a3d7692f/gistfile1.txt"
  --kconfig CONFIG_COMPILE_TEST=y --kconfig "CONFIG_PROFILE_ALL_BRANCHES=n"`
- yaml:
```yaml
kconfig:
  - allnoconfig
  - kvm_guest.configs
  - https://gist.githubusercontent.com/danrue/9e1e4d90149daadd5199256cc18a0499/raw/752138764ec039e4593185bfff888250a3d7692f/gistfile1.txt
  - CONFIG_COMPILE_TEST=y
  - CONFIG_PROFILE_ALL_BRANCHES=n
```

### kconfig_allconfig

The kconfig_allconfig argument is a string that is used to pass a filename to
be used with allyesconfig/allmodconfig/allnoconfig/randconfig kconfig
parameter.

The parameter can not be used with any other defconfig.

The argument is passed as an environment variable to the make command as
"KCONFIG_ALLCONFIG=<argument>".

example:
- `tuxbuild --kconfig allmodconfig --kconfig-allconfig "arch/arm64/configs/defconfig"`

## Support

If you have any questions or concerns, please email them to
tuxbuild@linaro.org. Please include the build ID with any build-specific
questions.
