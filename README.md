# ELEX String Table Comparison Tool

This tool was created in order to make translations for the computer game [ELEX](https://elexgame.com/) created by [Piranha Bytes](https://www.piranha-bytes.com/) (released in October 2017).
The tool allows one to change the in-game text values in an easy way.
The main purposes of this tool is:

* To create a translation for an existing ELEX modification
* To create a translation for the entire game

## Requirements
* To run this tool you need to have [Python 3.x](https://www.python.org/downloads/) installed.
* You need to have the ELEX string table files (or at least files that are formatted the same way)

## How does it work

### Basic logic

The tool compares two string tables with each other line by line.
If no difference is found for a specific line, the line will be move to the result string table w/o changing it.
If the tool spots a difference, the user gets prompted to provide an translation for it.

The tools can be configured to provide a "suggestion value" from another string table.
This text will be displayed to the user to help with the translation.

The tool can also be used without prompting the user (i.e. non-interactive).
The user then can specify a "auto fill" value that is used as translation.
This way a other tool (e.g. text editor) can be used to do the actual translation.

### Understand string tables

This tool is pretty stupid but has some handy features.
First of all, one needs to understand how in-game text is stored.
With ELEX (and probably many other games) there are multiple so called "string tables".
Each string table holds the in-game text values for a certain language.

The structure of such a string table is as follows:

~~~
ID|English_Text|English_StageDir
fffb2b00|This is a text||
fff8b11d|This is a multi line text.\r\nHere is the second line.\r\nHere is the third line|
fff85a02|This is another text|And this is some developer comment|
~~~

It's easy to see that there are three columns: `ID`, `English_Text` and `English_StageDir`.
For each in-game text there is one entry in this table having a unique identifier `ID` (never change this).
Then there are two columns that hold text.
The first one `English_Text` holds the actual text values that will be displayed in-game.
I don't really know what the last column is about.
It seems to be some developer comment or so.

This tool runs through the entire string table(s) and lets you put in new values.

### Understand the configuration

This tool has a config file called `config.json`.
In this file you configure which string table (files) the application should run through.
There are four configurations that you need to specify:

* `source` is the source string table.
* `compare` is the string table that is compared with `source`.
* `default-for-target` is used to help  with the translation. It will be used to display a "suggestion". The suggestion actually is just the value of another string table.
* `target` is the string table file your translation will be written into.

For each configuration you just specify a (display) name and the path to the actual files.
The `target` comes with some additional properties `run-with-auto-fill` and `auto-fill-value`.
If the former is set to "true" the tool runs in a non-interactive way.
This means, the tool doesn't prompt you if it spots a difference in `source` and `compare` but it automatically fills in the value specified by ´auto-fill-value`.
You may use this to do the translation with a different tool but need to recognize which texts you have to work on.

### Use the tool

The `main.py` file is the application file you have to launch using python.
You can do this with this command line command: `python3 <path-to-project>/main.py`.

By default this tool is working in the interactive mode (`run-with-auto-fill` is "false").
The tool scans the string tables given in `config.json` and prompts for a translation if it spots a difference in the in-game texts given for a specific string table identifier.

This will look like the following:

~~~
Differing value for id=ff85b8a7 (1/163)
	Original (EN)       : Increases magical energy.
	Modded (EN)         : Increases Mana.
	Suggestion (GER)    : Erhöht die magische Energie.
	Translation (GER)   : <type your translation here>
~~~

On the top line the identifier of the text value is displayed.
Next to this a counter "(1/163)" is displayed.
The first number is the current translation.
The other number is the total number of differing texts.
In this example there are 163 differing texts in total and the tool stopped at the first one.
In the last line you can type your actual translation.

You have three options what you can here here:

* Your actual translation followed by pressing ENTER.
* Just press ENTER (provide and empty text). In this case the value from the suggestion is taken as value for the translation. This is useful when you run over your own translation to double-check.
* Enter "q" to quit the tool entirely.

When you finished the editing (translated all differing texts) the tool writes _all_ entries (those that were edited and those that were not edited because there was no difference) into the file specified by `target`.

## Use Cases

### Create a translation for a modification of ELEX

This is the main use case.
Imagine you have a mod that alters some text in the game.
Now this mod is only available in one language (say English) and you want to create a translation for it (say German).
You will have to set `config.json` so that:
* `source` is the original string table for the English version of the game
* `compare` is the string table of the mod
* `default-for-target` is the original string table for the German version of the game
* `target` is the string table file your translation will be written into.

### Check your own translation

When you already have created a translation using this tool, you may want to double-check what you have changed.
Alternatively you spot bugs in your translation and you need to fix them.
You now have two options:
* Set the `default-for-target` to use your translation you've created originally. This way you get suggested with your own values and can easily take them over by just pressing ENTER in the interactive mode.
* Set the `source` to use the original string table of the target language and set `compare` and `default-for-target` to the translation you've created originally.