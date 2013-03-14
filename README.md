Sublime PHP Companion
=====================

This Sublime Text 3 Package provides cool stuff for PHP 5.3+ coding session.

Successor of SublimeCTagsPHP
----------------------------

This plugin is the successor of [SublimeCTagsPHP](https://github.com/erichard/SublimeCTagsPHP).

PHP Companion use the built-in index of Sublime Text 3 instead of CTags.

Installation
----------------------------

Clone this repo in your Sublime Text 3 Package dir.

```
$ git clone https://github.com/erichard/SublimePHPCompanion "PHP Companion"
```

find_use
--------

Just bring your cursor hover a class name, hit the F5 key (default but customizable) and that's it.

It will show you the different namespace that match your class, pick up one and your done.

PHP Companion will sort your uses statement in alphabetical order.


import_namespace
----------------

Just hit the F4 key, it will add the namespace definition based on the absolute
filename of the current file. I use a simple trick to determine where the
namespace begun, actually the namespace will start at the first CamelCased
folder.

If a namespace is already declared, the command will shout how crazy you are in
the status bar.

**Warning:** This feature require a filename so the command won't work in an unsaved buffer.
