
<img width=300 src=https://user-images.githubusercontent.com/2152766/59975170-e925e880-95ac-11e9-9751-c37ff554b5f1.png>

> "Works on *your* machine"

A [Rez](https://github.com/nerdvegas/rez) superset, on PyPI, for Python 2 and 3, with extended support for Windows, an editable [wiki](https://github.com/mottosso/bleeding-rez/wiki) and independent [roadmap](https://github.com/mottosso/bleeding-rez/wiki/Bleeding-Roadmap-2019).

<br>

#### Build Status

<table>
    <tr>
        <td><code>master</code></td>
        <td width=150px><a href=https://mottosso.visualstudio.com/bleeding-rez/_build?definitionId=1><img src=https://img.shields.io/azure-devops/build/mottosso/df4341a8-04df-420f-9aa6-91a53513dd14/1/master.svg?label=Windows></a></td>
        <td width=150px><a href=https://mottosso.visualstudio.com/bleeding-rez/_build?definitionId=1><img src=https://img.shields.io/azure-devops/build/mottosso/df4341a8-04df-420f-9aa6-91a53513dd14/1/master.svg?label=Linux></a></td>
        <td width=150px><a href=https://mottosso.visualstudio.com/bleeding-rez/_build?definitionId=1><img src=https://img.shields.io/azure-devops/build/mottosso/df4341a8-04df-420f-9aa6-91a53513dd14/1/master.svg?label=MacOS></a></td>
    </tr>
    <tr>
        <td><code>dev</code></td>
        <td width=150px><a href=https://mottosso.visualstudio.com/bleeding-rez/_build?definitionId=1><img src=https://img.shields.io/azure-devops/build/mottosso/df4341a8-04df-420f-9aa6-91a53513dd14/1/dev.svg?label=Windows></a></td>
        <td width=150px><a href=https://mottosso.visualstudio.com/bleeding-rez/_build?definitionId=1><img src=https://img.shields.io/azure-devops/build/mottosso/df4341a8-04df-420f-9aa6-91a53513dd14/1/dev.svg?label=Linux></a></td>
        <td width=150px><a href=https://mottosso.visualstudio.com/bleeding-rez/_build?definitionId=1><img src=https://img.shields.io/azure-devops/build/mottosso/df4341a8-04df-420f-9aa6-91a53513dd14/1/dev.svg?label=MacOS></a></td>
    </tr>
</table>

[![](https://badge.fury.io/py/bleeding-rez.svg)](https://pypi.org/project/bleeding-rez/)

<br>

### What is Rez

Rez is a command-line utility for Windows, Linux and MacOS, solving the problem of creating a reproducible environment for your software projects on any machine in any pre-existing environment. It does so by resolving a "request" into a deterministic selection of "packages". Each package is a versioned collection of files with some metadata that you self-host and the resulting "context" is generated on-demand.

```bash
$ rez env Python-3.7 PySide2-5.12 six requests
> $ echo Hello reproducible environment!
```

- [Safety](#safety)
- [Production Configurations](#production-configurations)
- [Backwards Compatibility](#backwards-compatibility)
- [Known Issues](#known-issues)
- [FAQ](#faq)
- [Comparisons](#comparisons) (wip)

<br>

### Ecosystem

A small but growing number of companion projects for bleeding- and nerdvegas-rez.

- `rez-installz` - Native package manager for bleeding-rez
- [`rez-localz`](https://github.com/mottosso/rez-localz) - Package localisation from network or cloud storage
- [`rez-scoopz`](https://github.com/mottosso/rez-scoopz) - Install from [500+ system packages](https://github.com/ScoopInstaller/Main/tree/master/bucket) for Windows as a Rez package
- [`rez-pipz`](https://github.com/mottosso/rez-pipz) - Build and install any [PyPI](https://pypi.org) compatible project as a Rez package
- `rez-cmakez` - Build your projects using CMake
- `rez-yumz` - Install from a selection of [80,000+ RPM packages](https://centos.pkgs.org/7/centos-x86_64/) and counting
- `rez-vcpkgz` - Install any of the [1000+ C++ libraries](https://github.com/Microsoft/vcpkg/tree/master/ports) as a Rez package
- `rez-conanz` - Install any of the [200+ C++ libraries](https://conan.io/) as a Rez package
- `rez-npm` - Install any of the [1000+ JavaScript libraries](https://www.npmjs.com/get-npm) as a Rez package
- [`rez-allzpark`](https://allzpark.sh) - Visual application launcher and Rez debugging tool
- [`rez-for-projects`](https://github.com/mottosso/rez-for-projects) - A set of example packages for use of Rez (and Allspark) with project and application configurations
- `rez-performance` - Test the impact of x-number of packages with y-level of complexity in your network environment to make better integration and deployment decisions.
- `rez-releaz` - Secure package releases with Git integration
- `rez-guiz` - Old-school visual editor of Rez contexts
- `rez-flowchartz` - Visualise package dependencies as a flowchart, useful for debugging
- `rez-...` Your project here!

<br>

### Quickstart

Here's how to install and use bleeding-rez on your machine.

```bash
$ pip install bleeding-rez
$ rez bind --quickstart
$ rez --version
2.33.0
$ rez env
> $ echo Hello World!
Hello World!
```

> The `>` character denotes that you are in a resolved environment, great job!

Now head over to the [**Quickstart Guide**](https://github.com/mottosso/bleeding-rez/wiki/Quickstart) for your first look at what it can do!

<details><summary><b>Advanced</b></summary>

You may alternatively install directly from the GitHub repository using one of the following commands.

```bash
$ pip install git+https://github.com/mottosso/bleeding-rez.git
$ pip install git+https://github.com/mottosso/bleeding-rez.git@dev
$ pip install git+https://github.com/mottosso/bleeding-rez.git@feature/windows-alias-additional-argument
```

</details>

<details><summary><b>Developer</b></summary>

The developer approach maintains Git history and enables you to contribute back to this project (yay!)

```bash
$ python -m virtualenv rez-dev
$ rez-dev\Scripts\activate
(rez) $ git clone https://github.com/mottosso/bleeding-rez.git
(rez) $ cd rez
(rez) $ pip install . -e
```

> Use `. rez-dev\bin\activate` on Linux and MacOS

</details>

<br>

### Safety

How do you test whether your new software runs on another machine? You could run it on another machine. Or you could run it with bleeding-rez.

In order to guarantee that what works on your machine works everywhere, the environment generated by bleeding-rez is "isolated". Akin to what you get out of a Docker container. It contains only the bare essentials provided with a new install of your OS, everything else being provided by your packages.

```
C:\
 __________   __________   __________
|          | |          | |          |
| packageA | | packageB | | packageC |
|__________| |__________| |__________|
      |            |            |
 ____ v __________ v __________ v ___
|                                    |
|              Clean OS              |
|____________________________________|
```

Conversely, nerdvegas/rez *sometime* inherits the environment of the parent shell, resulting in a mix of variables coming from packages, and some coming from the parent. How does it determine whether to inherit? If a package references a variable, it is overwritten. Otherwise, inherited.

This is one of the core differences between nerdvegas- and bleeding-rez, and is what makes bleeding-rez safe and predictable.

##### Why is that important?

- **Incorrect assumptions** Consider developing a library on your machine that takes the environment variable `MY_VARIABLE` for granted. Everything runs, until it comes time to make a release. Once released, your users complain that your software doesn't work, and yet on your machine it does!
- **Bad remote environment** A user gets in touch to complain that your Python library doesn't run on his machine. Why? Because his local `PYTHONHOME` is set to his system Python distribution, rather than the one `required` by your package.
- **Bad local environment** Another user gets in touch saying his Python application complains about not finding PySide2. On your machine it runs just fine, but you later find out that your system Python had PySide2 installed.
- **Any other experience?** Let [me know](https://github.com/mottosso/bleeding-rez/issues)!

<br>

### Production Configurations

Unlike nerdvegas/rez, bleeding-rez fully supports packaging of production environments, also known as "profiles".

- See [Allzpark](https://allzpark.com/) for an example of what that means to you

<br>

### Backwards Compatibility

Some features have been disabled by default. If you encounter any issues, here is how can re-enable them.

**rezconfig.py**

Apply all of these for full compatibility with nerdvegas/rez

```python
import os

# bleeding-rez does not affect file permissions at all
# as it can cause issues on SMB/CIFS shares
make_package_temporarily_writable = True

# bleeding-rez does not support Rez 1 or below
disable_rez_1_compatibility = False

# nerdvegas/rez inherits all values, except under special circumstances.
# See https://github.com/mottosso/bleeding-rez/issues/70
# Can also be passed interactively, to override whatever is set here.
#   $ rez env --inherited  # = True
#   $ rez env --isolated   # = False
inherit_parent_environment = True

# bleeding-rez simplifies the map for Windows
# You can undo this simplification like this.
platform_map = {}

# On Windows, the default shell for bleeding-rez is PowerShell
default_shell = "cmd" if os.name == "nt" else None
```

<br>

### Known Issues

- The (deprecated) `rezbuild.py` build system doesn't appear to work without `inherit_parent_environment = True`

<br>

### FAQ

##### <blockquote>Should I use nerdvegas/rez or bleeding-rez?</blockquote>

If you need to use Rez on Windows with Python 2 and 3, and prefer a simplified installation procedure via PyPI along with the protection of an isolated environment then bleeding-rez is for you.

##### <blockquote>Why does bleeding-rez exist?</blockquote>

bleeding-rez started off as a fork from which to make PRs to nerdvegas/rez, but eventually started to diverge, now bleeding-rez is a true fork featuring additional safety and cross-platform compatibility, especially with Windows.

##### <blockquote>Are there any similar projects to bleeding-rez?</blockquote>

Yes, to some extent. Have a look at these.

| Project | Scope | Shared Packages | Commercial
|:--------|:------|:----------------|:-----------------
| [bleeding-rez](https://github.com/mottosso/bleeding-rez) | ESAP | x
| [rez](https://github.com/nerdvegas/rez) | ES | x
| [Stash](http://stashsoftware.com) | ESAP | x | x
| [be](https://github.com/mottosso/be) | ESAP | x
| [Ecosystem](https://github.com/PeregrineLabs/Ecosystem) | E | x
| [add](https://github.com/mottosso/add) | E | x
| [avalon](http://getavalon.github.io) | EA | x
| [miniconda](https://conda.io/en/latest/) | S |
| [virtualenv](https://github.com/pypa/virtualenv) | S | 
| [venv](https://docs.python.org/3/library/venv.html) | S |
| [pipenv](https://docs.pipenv.org/en/latest/) | S |
| [poetry](https://github.com/sdispater/poetry) | S |
| [hatch](https://github.com/ofek/hatch)  | S |
| [nixpkgs](https://nixos.org/nixpkgs/)   | S | x
| [scoop](https://scoop.sh)               | S | 
| [fips](https://github.com/floooh/fips)  | S | 
| [spack](https://spack.io)  | ESA |

- **Project** Name of project
- **Shared** Whether packages are re-installed per environment, or shared amongst them
- **Scope** Usecases covered by project
    - **E** Environment management, per-package control over what is should look like when requested
    - **S** Software builds, e.g. via cmake
    - **A** Application versioning, along with associated dependencies
    - **P** Project versioning, with associated software and application dependencies

##### <blockquote>How can I get involved?</blockquote>

I'm glad you asked! You're welcome to fork this repository and make a pull-request with your additions. Don't worry too much about the details, automated tests will kick in any time you update your PR. You can also contribute by looking through this README or the [wiki](https://github.com/mottosso/bleeding-rez/wiki) for things to improve, and generally just being part of the project. Welcome aboard!

##### <blockquote>How do I report a bug?</blockquote>

You can do that in the [issues section](https://github.com/mottosso/bleeding-rez/issues), try and be specific.

##### <blockquote>What's the advantage of bleeding-rez over Python's virtualenv/venv or Conda?</blockquote>

Aside from those being strictly limited to Python packages and Rez being language agnostic, both venv and Conda couple the installation of packages with their environment, meaning installed packages cannot be shared with other environments. Consider having installed a series of packages, such as PySide2, PyOpenGL, pyglet and other somewhat large libraries. You'll need to spend both time and disk space for each environment you make; essentially once per project.

On the other side of the spectrum, you've got the global installation directory for something like Python, the `site-packages` directory. Why not just install everything there, and let whichever project you work on use what it needs? The problem is version. If one of your projects require PySide2-5.9 but another requires 5.13 there isn't much you can do.

Enter Rez. With Rez, you can install every package under the sun, for all platforms at once, and establish environment dynamically as you either run, build or develop your project.

```bash
cd my_project
rez env git-2.1 vs-2017 PySide2-5.13 python-3.7 pyglet-1.1b0 PyOpenGL-3.1 -- python setup.py bdist_wheel
```

That means, less disk space is used and that every package you install is an investment into future projects. At some point, your repository of packages gets so large that a single computer or disk is not enough to contain them all, and that's exactly the kind of situation Rez excels at solving, with a `memcached` backend for performance and multi-repository support via the `REZ_PACKAGES_PATH` environment variable which works much like `PYTHONPATH` for Python.

Some of the largest consumers of packages, Animal Logic, hosts thousands of gigabytes of actively used packages across thousands of computers within a shared environment.

<br>

### Comparisons

In addition to the high-level comparisons [above](https://github.com/mottosso/bleeding-rez#are-there-any-similar-projects-to-bleeding-rez), these are a few more in-depth comparisons with projects of particular interest.

<br>

#### Docker

Ever wanted to run graphical applications, like Maya, in a Docker container? Now bleeding-rez can give you the next best thing. Full compartmentalisation whilst retaining access to system hardware like your GPU.

Like a Docker container, the environment within is completely independent of the environment from which it was entered.

```bash
$ export MY_VARIABLE=true
$ docker run -ti --rm centos:7
> $ echo $MY_VARIABLE
$MY_VARIABLE
```

Like `docker run`, environment variables can be passed into a resolved context like this.

```bash
$ docker run -e key=value centos:7
$ rez env -e key=value python-3.7
```
