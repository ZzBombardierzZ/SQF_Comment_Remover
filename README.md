# SQF_Comment_Remover
A few simple executables to remove comments, empty lines, and newlines from SQF code in 1 click.

## Purpose
The purpose of this project is to provide a simple way to remove comments, empty lines, and newlines from Arma 2 mission folders. This not only saves a lot of file size on your mission folder, but it also makes it harder for others to steal/understand your code.

## Usage
* In either usage you choose: before using the executable(s), I would make a backup of your mission folder before you start in case of any unforeseen bugs. While I don't believe any bugs still exist (I have tested this fairly thoroughly), it's always better to be safe than sorry.
* My recommended usage:
    * You should always have a local test server on your machine for testing and developing and then a dedicated one for your actual server (do not host the dedicated server on your own network...)
    * Write a ton of comments in your sqf files to help you document your own work. This is a good habit to get into. There is no penalty for adding a ton of comments now as you will remove them in the coming steps.
    * Now there are a few ways you can do this, but when you are ready to upload your current test server files to your dedicated machine, make a copy of your mission folder and run the desired executable(s) in the root of the copy, run it/them and then take them out of the mission folder. Then upload the copy to your dedicated server.
        * To be clear, mission folder looks like `DayZ_Epoch_11.Chernarus`
* Bare minimum usage:
    * Stick the desired executable inside your mission folder. Now Run it.
* What the files do:
    * `Only_Remove_Comments.exe`: Removes comments from .sqf, .hpp, and .ext files.
    * `Only_Remove_Emptylines.exe`: Removes empty lines from .sqf, .hpp, and .ext files.
    * `Only_Remove_SQF_newlines.exe`: Removes all newlines from .sqf files.
    * `Clean_it_all.exe`: (Does all of the above) Removes comments, empty lines, and newlines from .sqf files. It also removes comments and empty lines from .hpp and .ext files (not newlines).
* Warning: If you accidentally run this in somewhere like the root of your C drive, it will likely run for a long time searching for sqf, hpp, and ext files in the entire drive and modify them respective to the exe you're using. So **DO NOT DO THAT**. While I __should__ have designed it to require to be within a MPMission folder, I'm not responsible for any damage you might cause.

Let me know if you run into any issues or have any suggestions for the future. I hope you enjoy this tool.


## Update History:
* v1.0 - 6/28/22: Initial release.

## Legal
* You are welcome to use this code in any way you want.
* I am not responsible for any damage you might cause.
* I got the comment_remover code from [here](https://stackoverflow.com/a/18381470) and I do not claim credit for writing that part. Regex is powerful and I don't want to reinvent the wheel.