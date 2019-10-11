## 2019-10-11
 - Add support for PSR4 by checking the composer.json
 - Remove options `start_dir_pattern` and `namespace_prefix`
 - Removed support for padawan

## 2018-06-26
 - Message during import_use are now displayed in tooltip instead of status bar
 - New option `namespace_blank_lines` allow to configure the number of newline between `<?php` and the inserted namespace

## 2017-10-09

 - Added new option `use_todo_implement` to choose between the formats that appear in method bodies of the implemented function. Allowed values are :
    - `false` (Default) : `throw new \Exception("Method 'methodname' not implemented");`
    - `true`: `// TODO: Implement 'methodName' method.`

## 2016-04-19

 - The implemenent method doe not copy the abstract keyword anymore.
 - New option `docblock_inherit` to copy the parent docblock. Allowed values are :
    - `true` (Default) : Copy the parent docblock
    - `inheritdoc`: Add a `@{inheritDoc}` docblock

## 2016-03-15

 - Add an implement method. Useful for interface or abstract class.

## 2015-06-30

 - Add a insert_constructor_prop command to insert both contructor argument and property in one shot.

## 2015-06-29

 - Remove defaults keybindings
 - Update readme

## 2014-10-10

 - Overwrite namespace declaration when already exist

## 2014-09-10

 - Add a space in status bar message when importing namespaces

## 2014-09-04

 - Allow per-project settings
 - Add support for a configured namespace prefix to support PSR4 style libraries

## 2014-04-11

 - Better namespace declaration matching
 - New option `namespace_position` to change where the namespace is included. Allowed values are :
    - `newline` (Default) : Include the namespace on a new line after <?php
    - `inline` : Inline the namespace with the <?php (ex: Laravel convention)

## 2014-02-25

 - Update `start_dir_pattern` (close [#10](https://github.com/erichard/SublimePHPCompanion/issues/10))
