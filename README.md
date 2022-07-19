# SQF_Comment_Remover
A few simple executables to remove comments, empty lines, and newlines from SQF code in 1 click.

## Purpose
The purpose of this project is to provide a simple way to remove comments, empty lines, and newlines from Arma 2 mission folders. This not only saves a lot of file size on your mission folder, but it also makes it harder for others to steal/understand your code.

## Usage
* In either usage you choose: before using the executable(s), I would **make a backup of your mission folder** before you start in case of any unforeseen bugs. While I don't believe any bugs still exist (I have tested this fairly thoroughly), it's always better to be safe than sorry.
* My recommended usage:
    * You should always have a local test server on your machine for testing and developing and then a dedicated one for your actual server (do not host the dedicated server on your own network...)
    * Write a ton of comments in your sqf files to help you document your own work. This is a good habit to get into. There is no penalty for adding a ton of comments now as you will remove them in the coming steps.
    * Now there are a few ways you can do this, but when you are ready to upload your current test server files to your dedicated machine, make a copy of your mission folder and run the executable in the root of the copy, run it/them and then take them out of the mission folder. Then upload the copy to your dedicated server.
        * To be clear, mission folder looks like `DayZ_Epoch_11.Chernarus`
* Bare minimum usage:
    * Stick the executable and settings inside your mission folder. Now Run it. Now remove the executable and settings from the mission folder. Now upload the mission folder to your dedicated server.
* What the settings do:
    * `remove_comments`: Removes comments from .sqf, .hpp, and .ext files.
    * `remove_empty_lines`: Removes empty lines from .sqf, .hpp, and .ext files.
    * `remove_excess_spaces`: Removes excess spaces from .sqf, .hpp, and .ext files.
    * `remove_sqf_newlines`: Removes all newlines from .sqf files except #include and #define lines.
    * `remove_hppOrExt_newlines`: Removes all newlines from .hpp and .ext files except #include and #define lines.
    * `excessive_debug_mode`: Logs the before and after for each file for each step. This is only useful for testing and debugging. Not recommended to use unless there are issues you are reporting back to me.
    * `optional_specified_folder_path`: If you want to specify a folder path to remove comments from, you can do so by setting the `optional_specified_folder_path` to the path you want to remove comments and clean from. **Otherwise** it will use the current working directory of the executable and do any subfolders within it.
        * An example of a folder path: `C:\MyServer\Server\MPMissions\DayZ_Epoch_11.Chernarus`
* Warning: If you accidentally run this in somewhere like the root of your C drive, it will likely run for a long time searching for sqf, hpp, and ext files in the entire drive and modify them respective to the exe you're using. So **DO NOT DO THAT**. While I __should__ have designed it to require to be within a MPMission folder, I'm not responsible for any damage you might cause.

Let me know if you run into any issues or have any suggestions for the future. I hope you enjoy this tool.


## Update History:
* v1.4 - 7/19/2020
    * Added `optional_specified_folder_path`
    * Fixed errors with #ifndef, #endif, #if, #else and #ifdef
* v1.3 - 7/18/22: 
    * Adds option to ignore certain files/paths from the cleaner using ignore_these_files.txt 
    * Adds optional extra logging when running myApp.py rather than one of the executables. 
    * Switched from multiple executables to one executable using setttings.json
    * Should parse a little bit better, getting rid of even more unnecessary whitespace and such.
* v1.2 - 7/1/22: Updated all exes to fix issue with files being wiped with newline remover and empty line remover. Also added Excess whitespace remover and included it into clean_it_all. Turns several spaces or tabs into 1 space.
* v1.1 - 6/28/22: New comment parsing method. Fixes issues with strings such as `https://` and similar which ARE NOT comments.
* v1.0 - 6/28/22: Initial release.

## Legal
* You are welcome to use this code in any way you want.
* I am not responsible for any damage you might cause.
* I got the original comment_remover code from [here](https://stackoverflow.com/a/18381470) and I do not claim credit for writing that part. Regex is powerful and I don't want to reinvent the wheel. This comment_remover code is no longer in use. I am **now** using [this method](https://stackoverflow.com/a/1656009)
