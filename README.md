# Sublime PHP Companion [![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=dhalsimfr&url=https://github.com/erichard/SublimePHPCompanion&title=SublimePHPCompanion&language=&tags=github&category=software) 

This Sublime Text 3 Package provides cool stuff for PHP 5.3+ coding session.

## Successor of SublimeCTagsPHP

This plugin is the successor of [SublimeCTagsPHP](https://github.com/erichard/SublimeCTagsPHP).

PHP Companion use the built-in index of Sublime Text 3 instead of CTags.

## Installation

Clone this repo in your Sublime Text 3 Package dir.

```
$ git clone https://github.com/erichard/SublimePHPCompanion "PHP Companion"
```

## Commands

### find_use

Just bring your cursor hover a class name, hit the `F5` key (default but customizable) and that's it.

It will show you the different namespace that match your class, pick up one and your done.

PHP Companion will sort your uses statement in alphabetical order.

### expand_fqcn

This command expand the class under the cursor to its FQCN (Fully Qualified Class Name).
Default mapping is set on the `F6` key.

### import_namespace

Just hit the `F4` key, it will add the namespace definition based on the absolute
filename of the current file. I use a simple trick to determine where the
namespace begun, actually the namespace will start at the first CamelCased
folder.

If a namespace is already declared, the command will shout how crazy you are in
the status bar.

**Warning:** This feature require a filename so the command won't work in an unsaved buffer.

## Settings

### exclude_dir

List of directories to exclude when searching for the class declaration file.
Path are relative to the project directory.

### start_dir_pattern

The pattern used to guess the namespace in the `import_namespace` command.
The default pattern should work for most uses cases but you can change it if
your projects are stored in different way.

## Licence

All of Sublime PHP Companion is licensed under the MIT license.

  Copyright (c) 2013 Erwan Richard <erwann.richard@gmail.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
  

## Support me

If you like this plugin and want to offer me a beer or something you can use the flattr button next to the title ;-)
