# Sublime PHP Companion

This Sublime Text 3 Package provides cool stuff for PHP 5.3+ coding session.

**Note** I am looking for a maintainer for this project because I have switched to vim.

## Installation

### Package control

Just search for PHP Companion in package control and you're ready.

### Keybinding

The package no longer provides keybindings. You will have to install your own shortcuts. The [Default.sublime-keymap-sample](/Default.sublime-keymap-sample) will give you the shortcuts I personally use.

## Commands

### find_use

Just place your cursor on a class name, hit the <kbd>F5</kbd> key (personal shortcut) and that's it.

It will show you the different namespace that match your class, pick up one and you're done.

PHP Companion will sort your uses statement in alphabetical order. This can be
configured to sort by line length with the `use_sort_length` user setting.

### expand_fqcn

This command expands the class under the cursor to its FQCN (Fully Qualified Class Name).
You have two keys for this command <kbd>F6</kbd> and <kbd>shift+F6</kbd> (personal shortcut) that respectively expand
with and without the leading namespace separator `\`.

### import_namespace

Just hit the <kbd>F4</kbd> key (personal shortcut), it will add the namespace definition based on the absolute
filename of the current file. I use a simple trick to determine where the
namespace begun, actually the namespace will start at the first CamelCased
folder.

If a namespace is already declared, the command will shout how crazy you are in
the status bar.

**Warning:** This feature requires a filename so the command won't work in an unsaved buffer.

### goto_definition_scope

Hit <kbd>shift+F12</kbd> (personal shortcut) to search for a method definition based on the current scope. It will fallback to
the "goto_definition" command if a match was not found.

### insert_php_constructor_property

Hit <kbd>F7</kbd> (personal shortcut) to insert both a constructor argument and its according property. The property will be `private` by default but you can change it with the `visibility` setting.

### implement

Place your cursor on a class, abstract class or an interface name and hit the <kbd>F3</kbd> key (personal shortcut). Matching interfaces or classes will be shown. Select one and then import all or one of the methods from that interface or class.

See `use_todo_implement` setting.


## Settings

Settings can be stored either in your system wide "PHP Companion.sublime-settings" file or in the project
settings file. This allows you to set preferences per-project if you need to.

If you're storing settings in a project file, put them in a phpcompanion node like this:

```
"phpcompanion": {
    "exclude_dir": [
        "vendor",
        "build"
    ]
}
```

### exclude_dir

List of directories to exclude when searching for the class declaration file.
Path is relative to the project directory.

Please note that the filtering is done after the search in the index. So this option has no impact on performance,
it's just a convenient way to avoid duplicate namespace declaration in some case.

### use_sort_length

When importing use statements with the <kbd>find_use</kbd> command, sort statements by the length of the line.

### use_todo_implement

When an interface or abstract class is implemented, this option is used to customize the method body of the newly added methods.

The available options are true and false.

`"use_todo_implement": true`:
```
public function methodName()
{
    // TODO: Implement 'methodName' method.
}
```

`"use_todo_implement": false`:
```
public function methodName()
{
    throw new \Exception("Method 'methodname' not implemented");
}
```

## Successor of SublimeCTagsPHP

This plugin is the successor of [SublimeCTagsPHP](https://github.com/erichard/SublimeCTagsPHP). PHP Companion uses the built-in index of Sublime Text 3 instead of CTags.

**Warning!** PHP Companion does not work on Sublime Text 2 and never will.


## Licence

All of Sublime PHP Companion is licensed under the MIT license.

  Copyright (c) 2013-2020 Erwan Richard

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
