# BASIC Wrangler

A BASIC program listing line renumberer/cruncher (aka, a minifier).

**_This program is currently in beta testing._** It will probably break your program. The documentation is minimal. Things will change frequently.

What if you could turn this:

![Example 1](docs/images/example1.png)

Into this:

![Example 2](docs/images/example2.png)

And _then_ turn that into this:

![Example 3](docs/images/example3.png)

With BASIC Wrangler, you can!

## Purpose

The purpose of BASIC Wrangler is to allow you to write BASIC programs using labels in a dialect-agnostic way. It also combines and crunches lines to take up the least amount of space on output, thus saving you memory. It is designed to be able to work with almost any dialect of line numbered BASIC.

## Installation

To install with pip, type:

```Batchfile
pip install basic-wrangler
```

There is also a standalone version available for Windows under the Release tab.

If you are not running Windows 10, you may need to download the x86 version of the [Visual C++ Redistributable for Visual Studio 2015](https://www.microsoft.com/en-us/download/details.aspx?id=48145). The standalone version does not work on Windows XP.

## Basic Usage

To load the GUI, type `bw` (a harmless console window might open up behind the main window -- ignore it). Type `bw -h` for CLI help. For more, check out [the Manual](docs/Manual.asc) in the docs directory.

## Some of the Planned Features

- [x] Built-in conversion from numbered listings routine
- [x] A GUI
- [x] Output to clipboard when pasting
- [ ] Preprocessor macros like includes and ifs
- [ ] Renaming variables
- [ ] Support for external tokenizers by accounting for how many bytes each token uses
- [x] Support for output to files that can be transferred directly into disk images

## Changelog

See [CHANGELOG.md](CHANGELOG.md)

## Getting Support

If you have any issues, you can either report them at [the Issues tab](https://github.com/pahandav/basic-wrangler/issues) or you can report them at [the AtariAge Release thread](https://atariage.com/forums/topic/297649-basic-wrangler-a-line-cruncherrenumberer/). There might also be useful information at [my blog](https://oldschoolbasic.blogspot.com/).

## Attribution

Program icon based on an icon made by [Retinaicons](http://www.flaticon.com/authors/retinaicons) from [www.flaticon.com](http://www.flaticon.com).
