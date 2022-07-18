import re, os, json
from pyparsing import cppStyleComment,dblQuotedString

cppStyleComment.ignore(dblQuotedString)

def print_and_log(message:str):
    print(message)
    with open("logs.txt", "a") as f:
        f.write(f"{message}\n")

# I did not write the comment remover. I had a version I made but it had bugs. This was found on the internet.
# https://stackoverflow.com/a/18381470
def remove_comments(string):
    #pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    pattern = r"(\".*?(?<!\\)\"|\'.*?(?<!\\)\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)



def remove_all_newlines(data):
    #currently has an issue with #defines. Set as false for now for hpp files
    cleaned_data = ""
    if len(data) > 0:
        if data.find("\n") > -1:
            for line in data.splitlines():
                if line.find("#") == -1 and (line.find(";") > -1 or line.find("{") > -1) and not (line.rstrip().endswith("\"") or line.rstrip().endswith("'") or line.rstrip().endswith("\\")):
                    cleaned_data = f"{cleaned_data}{line.rstrip()} "
                else :
                    cleaned_data = f"{cleaned_data}{line}\n"
        else:
            cleaned_data = data
        cleaned_data = re.sub(r'( #include)|(\t#include)', '\n#include', cleaned_data)
        cleaned_data = re.sub(r'( #define)|(\t#define)', '\n#define', cleaned_data)
    return cleaned_data

def remove_empty_lines(data):
    cleaned_data = ""
    if len(data) > 0:
        if data.find("\n") > -1:
            for line in data.splitlines():
                if len(line.rstrip())>0:
                    cleaned_data = f"{cleaned_data}{line}\n"
        else:
            cleaned_data = data
    return cleaned_data

def clean_data_etc(file_path:str, remove_comments_bool:bool, remove_empty_lines_bool:bool, remove_newlines_bool:bool, remove_extra_spaces_bool:bool, debug_mode:bool=False):
    print_and_log("Cleaning: "+file_path)
    
    with open(file_path, "r") as f:
        data = f.read()

    if remove_comments_bool:
        print_and_log(f"Removing Comments: {file_path}")
        # data = remove_comments(data) # remove comments (new way found online)
        if debug_mode:
            print_and_log(f"{file_path} before removing comments: \n{data}")
        data = cppStyleComment.suppress().transformString(data) #newer/safer method
        if debug_mode:
            print_and_log(f"{file_path} after removing comments: \n{data}")

    if remove_empty_lines_bool:
        print_and_log(f"Removing empty lines: {file_path}")
        if debug_mode:
            print_and_log(f"{file_path} before removing empty lines: \n{data}")
        data = remove_empty_lines(data)
        if debug_mode:
            print_and_log(f"{file_path} after removing empty lines: \n{data}")

    if remove_newlines_bool:
        print_and_log(f"Removing new lines: {file_path}")
        if debug_mode:
            print_and_log(f"{file_path} before removing new lines: \n{data}")
        data = remove_all_newlines(data)
        if debug_mode:
            print_and_log(f"{file_path} after removing new lines: \n{data}")
    
    if remove_extra_spaces_bool:
        if debug_mode:
            print_and_log(f"Data before removing extra spaces: {data}")
        data = re.sub(r'[ \t]+', ' ', data) # remove all excess tab or space whitespace
        data = re.sub(r'\n ', '\n', data) # remove extra space at beginning of line from last regex
        if debug_mode:
            print_and_log(f"Data after removing extra spaces: {data}")

    with open(file_path, "w") as f:
        f.write(data)

def get_directory_files():
    print_and_log("Getting directory paths of cwd")
    path = os.getcwd()

    this_directory_list = []

    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            this_directory_list.append(os.path.join(root, name))

    print_and_log(f"This directory has these files:{this_directory_list}")
    return this_directory_list

def get_ignored_files():
    print_and_log("Checking for ignored files")
    ignored_files = []

    if not os.path.isfile("ignore_these_files.txt"):
        print_and_log("No ignore_these_files.txt file found")
        return ignored_files

    with open("ignore_these_files.txt", "r") as f:
        file = f.read()
        for line in file.splitlines():
            if line.find("//") > -1:
                line = line[0:(line.find("//"))]
                line = re.sub(r'\s+', '', line)
            if len(line) > 0:
                ignored_files.append(line)
    print_and_log(f"These files will be ignored: {ignored_files}")

    return ignored_files

def main_brain():
    print_and_log("Starting Bomb's cleaning service")

    if os.path.isfile("settings.json"):
        with open("settings.json", "r") as f:
            settings = json.load(f)
            print_and_log("Settings loaded")
    else:
        print_and_log("No settings file found")
        return

    try:
        debug_mode_bool = settings["Extras"]["excessive_debug_mode"]
        remove_comments_bool = settings["Cleaner_Config"]["remove_comments"]
        remove_empty_lines_bool = settings["Cleaner_Config"]["remove_empty_lines"]
        remove_excess_spaces_bool = settings["Cleaner_Config"]["remove_excess_spaces"]
        remove_sqf_newlines_bool = settings["Cleaner_Config"]["remove_sqf_newlines"]
        remove_hppOrExt_newlines_bool = settings["Cleaner_Config"]["remove_hppOrExt_newlines"]
    except Exception as e:
        print_and_log(f"Error loading settings. Check your settings.json file. Error message:\n{e}")
        return
    


    directory_files = get_directory_files()
    ignored_files = get_ignored_files()
    for file_path in directory_files:
        ignore = False
        for ignored_file in ignored_files:
            if file_path.find(ignored_file) > -1:
                ignore = True
                break
        if not ignore:
            if file_path.find(".hpp") > -1 or file_path.find(".ext") > -1:
                clean_data_etc(file_path, remove_comments_bool, remove_empty_lines_bool, remove_hppOrExt_newlines_bool, remove_excess_spaces_bool, debug_mode_bool)
            elif file_path.find(".sqf") > -1:
                clean_data_etc(file_path, remove_comments_bool, remove_empty_lines_bool, remove_sqf_newlines_bool, remove_excess_spaces_bool, debug_mode_bool)

    print_and_log("Bomb's cleaning service has finished")

main_brain()