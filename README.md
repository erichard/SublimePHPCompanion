# Sublime PHP Companion [![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=erichard&url=https://github.com/erichard/SublimePHPCompanion&title=SublimePHPCompanion&language=&tags=github&category=software) 

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


## Support me

This plugin is free and will always be. 

But if you like it and want to offer me a beer or something 
you can use the flattr button next to the title ;-)

