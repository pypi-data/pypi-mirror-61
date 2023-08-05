![ahd-logo](https://raw.githubusercontent.com/Descent098/ahd/master/docs/img/ahd-logo.png) [![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/Descent098/ahd/?ref=repository-badge)

# ahd; Ad-Hoc Dispatcher

*Create ad-hoc commands to be dispatched within their own namespace.*



## Quick-start

### Installation

#### From Pypi

Run ```pip install ahd``` or ```sudo pip3 install ahd```



#### From source

1. Clone this repo: (https://github.com/Descent098/ahd)
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory



### Usage

```bash
Usage:
    ahd list [-l]
    ahd [-h] [-v] [-d]
    ahd docs [-a] [-o]
    ahd config [-e] [-i CONFIG_FILE_PATH]
    ahd register <name> [<command>] [<paths>]
    ahd <name> [<command>] [<paths>]

Options:
-h, --help            show this help message and exit
-v, --version         show program's version number and exit
-l, --long            Shows all commands in configuration with paths and commands
-a, --api             shows the local API docs
-o, --offline         shows the local User docs instead of live ones
-e, --export          exports the configuration file
-i CONFIG_FILE_PATH, --import CONFIG_FILE_PATH
                    imports the configuration file
```



#### Example

Here is a quick example of creating a command that runs ```sudo apt-get update && sudo apt-get upgrade```:

1. Register the command as the name "update": ```ahd register update "sudo apt-get update && sudo apt-get upgrade"```
2. Run the command using the name "update": ```ahd update```



This example was somewhat trivial but keep in mind this effectively means you can replace any short bash scripts you are using to do things like updating multiple git repos, executing a sequence of commands to sort your downloads folder etc.



#### Arguments

##### list

The list command shows a list of your current registered commands.

**Options**:

  \- \-\-long: Shows all commands in configuration with paths and commands  

##### docs

The docs command is designed to bring up documentation as needed, you can run ```ahd docs``` to open the documentation site in the default browser.



**Options**:

  \-a \-\-api: Used to serve local API documentation (Not yet implemented)

  \-o \-\-offline: Used to serve local user documentation (Not yet implemented)



##### config

This command is used for **all** configuration management. Due to the amount of preprocessing involved in keeping ahd cross platform the dotfile is obstructed from view by default. The config command is the main interface for managing configurations manually though I would recommend using the **register** command as opposed to this, or looking at the documentation for details about [manual configuration](https://ahd.readthedocs.io/en/latest/usage#wildcards-and-cross-platform-paths).



**Options**:

  \-e \-\-export: Export the current configuration file (it's a dotfile so make sure view hidden files is enabled)

  \-i \-\-import: Import a configuration file; takes the path as an argument



##### Register

The register command allows you to register a name to be used later on. For example if I wanted to create a command that dispatched running git pull in several of my directories that is activated when I type ```ahd git-upt``` then I can just run ```ahd register git-upt "git pull" "~/path/to/project, ~/path/to/project-2, ~/path/to/project-3```



##### \<name\>

This is a placeholder value for the name of a command you have registered. Once the command is registered you can run it by using ```ahd <name>```, additionally you can override the default set commands or paths, details can be found at [https://ahd.readthedocs.io/en/latest/usage#overriding](https://ahd.readthedocs.io/en/latest/usage#overriding).





## Additional Documentation

Additional user and development/contribution documentation will be available at [https://ahd.readthedocs.io/en/latest/](https://ahd.readthedocs.io/en/latest/). Also API documentation is available at [https://kieranwood.ca/ahd](https://kieranwood.ca/ahd)





