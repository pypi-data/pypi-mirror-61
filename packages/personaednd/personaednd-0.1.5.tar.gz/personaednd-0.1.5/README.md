# personaednd (0.1.5)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)&nbsp;[![](https://camo.githubusercontent.com/14a9abb7e83098f2949f26d2190e04fb1bd52c06/68747470733a2f2f626c61636b2e72656164746865646f63732e696f2f656e2f737461626c652f5f7374617469632f6c6963656e73652e737667)](https://github.com/sg679/personaednd/blob/master/LICENSE)

### 1. Introduction


> "plural personae : a character in a fictional presentation (such as a novel or play) —usually used in plural" 

> “Persona.” The Merriam-Webster.com Dictionary, Merriam-Webster Inc., https://www.merriam-webster.com/dictionary/personae.

***personaednd*** is a tool for generating 5th edition Dungeons & Dragons characters for both Players and DMs.

With no offense given towards those who prefer such, ***personaednd*** attempts to generate characters according to a "role player" perspective and not from a "roll player" perspective.

### 2. Installation

Installation is pretty simple and straightforward.

##### Method #1

1. Open your terminal and type ```pip3 install personaednd```.

##### Method #2

1. Open your terminal then change into the directory where you wish to clone the repository.
2. Type ```git clone https://github.com/sg679/personaednd.git``` to clone the repository, assuming Git is installed.
3. Change into the cloned repository and type ```python3 setup.py install```.

Note that the GitHub codebase may be slightly more updated than the code on PYPI.

### 3. Usage

To run, type ``` personaednd ``` in your terminal, which will run the application with the default options as defined below.

Here are some other options if you wish to fine tune your character.

```
Usage: personaednd [OPTIONS]

Options:
  -race TEXT         Character's chosen race.  [default: Aasimar; required] [Aasimar|Dragonborn|Dwarf|Dwarf, Hill|Dwarf, Mountain|Elf|Elf, Drow|Elf, Eladrin|Elf, High|Elf, Wood|Gnome|Gnome, Forest|Gnome, Rock|Half-elf|Half-orc|Halfling|Halfling, Lightfoot|Halfling, Stout|Human|Tiefling]
  -background TEXT   Character's chosen background.  [default: Acolyte; required] [Acolyte|Charlatan|Criminal|Entertainer|Folk Hero|Guild Artisan|Hermit|Noble|Outlander|Sage|Sailor|Soldier|Urchin]
  -class_ TEXT       Character's chosen class.  [default: Barbarian; required] [Barbarian|Bard|Cleric|Druid|Fighter|Monk|Paladin|Ranger|Rogue|Sorcerer|Warlock|Wizard]
  -archetype TEXT    Character's chosen archetype.
  -level INTEGER     Character's chosen class level.  [default: 1; required] [1-20]
  -variant TEXT      Determines if variant trait applies.  [default: false; required] [false|true]
  --version          Show the version and exit.
  --help             Show this message and exit.
```

###### Customization

All the character data used within the application: backgrounds, classes, feats, skills, tools, races and weapon proficiencies, are defined within a YAML file within the *sources* sub package called *sources.yml*. This file can be modified to include additional content by following the defined format.

### 4. Change Log

###### Version *0.1.5 (2.8.20)*

- Added -variant option to CLI interface. Accepts 'false' or 'true'. Defaults at 'false'.
- Added variant argument to ScoreImprovement constructor.
- Fixed Skills.select_skills overlap bug.
- Added variant argument to Skills.select_skills method.
- Proficiency bonus now uses formula to determine the value (level/4) + 1.

###### Version *0.1.4 (2.2.20)*

- Fixed a typo in the setup script at release.

###### Version *0.1.3 (2.2.20)*

- Merged version updates 0.1.2 with 0.1.3.
- Overall better ability score assignments.
- Redone the ScoreAssigner and ScoreImprovement classes. They both implement the quick build rules for each class by default.
- Added --version option to CLI interface.
- Code rewrite for the purpose of better adhering to PEP-8 coding standards.
- VERSION REBOOT - Restarted version numbering since the transformation of personaednd from a GUI to a CLI application.

###### Version *0.1.1 (1.12.20)*

- Various code tweaks and fixes.

###### Version *0.1.0 (1.4.20)*

- Fixed tool proficiency selection for Monks.
- Skilled feat now works to give a choice of three bonus skills and/or TOOLS. Previously only selected three skills.
- Renamed sub package 'app_data' to 'source'.

###### Version *0.0.9 (12.27.19)*

- Weapon Master feat now adds proficiency with four simple or martial weapons as normal.
- Fixed functionality with Lightly Armored, Moderately Armored, Heavily Armored, and Weapon Master feats in the has_requirements Feats class method.
    - If the character has Light armor proficiency they won't meet the requirements for Lightly Armored.
    - If the character has Medium armor proficiency they won't meet the requirements for Moderately Armored.
    - If the character has Heavy armor proficiency they won't meet the requirements for Heavily Armored.
    - If a character is proficient with Martial weapons, they likely have proficiency with Simple weapons too, meaning they can already use all weapons and thus won't "meet" the requirements for Weapon Master.
- Added work around for numpy bug in dice roller array.

###### Version *0.0.8 (12.22.19)*

- Code rewrite and bug fixes.

###### Version *0.0.7 (12.15.19)*

- Fixed bug in the YAML query script.

###### Version *0.0.6 (12.15.19)*

- Re-coded various sections of the program.
- Removed recipients or more accurate a 'suggestions' section from the _character.yaml file. The recipients section was originally used as a set of suggested classes that might chose a particular feat - most were left blank to begin with beforehand.
- Added background equipment list to character sheet.
- Added debugging output to 'Dice.roll_drop_lowest' method.

###### Version *0.0.5 (12.13.19)*

- Code tweaks.

###### Version *0.0.4 (12.11.19)*

- Fixed bug where generated scores never seemed to be over 15 *programmer oversight*.
- Changed score threshold to 60 from 70. It'll keep re-rolling until it meets this threshold.
- Added condition that the lowest score rolled can be no lower than 8.
- Modified 'Dice.roll_drop_lowest' to generate all six ability scores instead of one.
- Removed 'roll_ability_scores' function. Functionality transferred to 'Dice.roll_drop_lowest'.

###### Version *0.0.3 (12.8.19)*

- Character 'background' has been added to the character sheet.

###### Version *0.0.1 (12.6.19)*

- First converted to a command-line application from GUI.
- Implemented bonus languages based on character's background.
- Simplified the character database for ease of user customization.
