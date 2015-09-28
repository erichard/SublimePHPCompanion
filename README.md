# Sublime PHP Companion

This Sublime Text 3 Package provides cool stuff for PHP 5.3+ coding session.

## Successor of SublimeCTagsPHP

This plugin is the successor of [SublimeCTagsPHP](https://github.com/erichard/SublimeCTagsPHP). PHP Companion use the built-in index of Sublime Text 3 instead of CTags.

**Warning!** PHP Companion does not work on Sublime Text 2 and never will.

## Installation

### Package control

Just search for PHP Companion in package control and you're ready.

### Keybinding

The package no longer provides keybindings. You will have to install your own shortcuts. The [Default.sublime-keymap-sample](/Default.sublime-keymap-sample) will give you the shortcuts I personally use.

## Commands

### find_use

Just bring your cursor hover a class name, hit the `F5` key (personal shortcut) and that's it.

It will show you the different namespace that match your class, pick up one and your done.

PHP Companion will sort your uses statement in alphabetical order. This can be
configured to sort by line length with the `use_sort_length` user setting.

### expand_fqcn

This command expand the class under the cursor to its FQCN (Fully Qualified Class Name).
You have two keys for this command `F6` and `shift+F6` (personal shortcut) that respectively expand
without and with the leading namespace separator `\`.

### import_namespace

Just hit the `F4` key (personal shortcut), it will add the namespace definition based on the absolute
filename of the current file. I use a simple trick to determine where the
namespace begun, actually the namespace will start at the first CamelCased
folder.

If a namespace is already declared, the command will shout how crazy you are in
the status bar.

**Warning:** This feature require a filename so the command won't work in an unsaved buffer.

### goto_definition_scope

Hit `shift+F12` (personal shortcut) to search for a method definition based on the current scope. It will fallback to
the "goto_definition" command if a match was not found.

### insert_php_constructor_property

Hit `F7` (personal shortcut) to insert both a constructor argument and its according property. The property will be `private` by default but you can change it with the `visibility` setting.

### padawan_start_server

This command will start padawan.php server, so that you'll be able to get completions

### padawan_stop_server

This command will stop padawan.php server, so that you'll have default sublime completions

### padawan_generate_index

This command will generate index for the composer project that current file belongs to.
**Warning:** This command require a filename so the command won't work in an unsaved buffer.

### padawan_plugin_add

This command will install(download and register) plugin by it's name.
You can find [plugins list here](
https://github.com/mkusher/padawan.php/wiki/Plugins-list)
**Warning:** You have to configure composer command for plugin installation

### padawan_plugin_remove

This command will remove plugin.
**Warning:** You have to configure composer command for plugin removing

## Settings

Settings can be stored either in your system wide "PHP Companion.sublime-settings" file or in the project
settings file. This allows you to set preferences per-project if you need to.

If you're storing settings in a project file, put them in a phpcompanion node like this:

```
"phpcompanion": {
    "namespace_prefix": "VendorName\Project\Foo\Bar",
    "exclude_dir": [
        "vendor",
        "build"
    ]
}
```

### exclude_dir

List of directories to exclude when searching for the class declaration file.
Path are relative to the project directory.

Please note that the filtering is done after the search in the index. So this option has no impact on performance,
it's just a convenient way to avoid duplicate namespace declaration in some case.

### start_dir_pattern

The pattern used to guess the namespace in the `import_namespace` command.
The default pattern should work for most uses cases but you can change it if
your projects are stored in different way.

### namespace_prefix

If you have a namespace which is not fully exposed by the file path, you can set a namespace prefix. For example, suppose you have a class in

```
src/Foo/Bar.php
```

adding a namespace_prefix of 'Vendor\Project' would result in a resolved namespace declaration of

```
namespace Vendor\Project\Foo;
```

### use_sort_length

When importing use statements with the `find_use` command, sort statements by the length of the line.

### padawan_composer

Command for running composer, e.g. `php /path/to/composer.phar` or `composer.phar` depending
on the place, where you've installed composer.

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
