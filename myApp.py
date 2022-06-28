import re, os
from pyparsing import cppStyleComment,dblQuotedString

cppStyleComment.ignore(dblQuotedString)

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
                if line.find("#") == -1 and line.find(";") > -1:
                    cleaned_data += line.rstrip() + " "
                else :
                    cleaned_data += line + "\n"
        cleaned_data = re.sub(r'( #include)|(\t#include)', '\n#include', cleaned_data)
        cleaned_data = re.sub(r'( #define)|(\t#define)', '\n#define', cleaned_data)
    return cleaned_data

def remove_empty_lines(data):
    cleaned_data = ""
    if len(data) > 0:
        if data.find("\n") > -1:
            for line in data.splitlines():
                if len(line.rstrip())>0:
                    cleaned_data += line + "\n"
    return cleaned_data

def clean_data_etc(file_path:str, remove_comments_bool:bool, remove_empty_lines_bool:bool, remove_newlines_bool:bool):
    print("Cleaning: "+file_path)
    
    with open(file_path, "r") as f:
        data = f.read()

    if remove_comments_bool:
        print("Removing Comments: "+file_path)
        # data = remove_comments(data) # remove comments (new way found online)
        data = cppStyleComment.suppress().transformString(data) #newer/safer method

    if remove_empty_lines_bool:
        print("Removing empty lines: "+file_path)
        data = remove_empty_lines(data)

    if remove_newlines_bool:
        print("Removing new lines: "+file_path)
        data = remove_all_newlines(data)

    with open(file_path, "w") as f:
        f.write(data)

def get_directory_files():
    print("Getting directory paths of cwd")
    path = os.getcwd()

    this_directory_list = []

    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            this_directory_list.append(os.path.join(root, name))

    print("This directory has these files:" + str(this_directory_list))
    return this_directory_list

def main_brain():
    print("Starting Bomb's cleaning service")
    directory_files = get_directory_files()
    for file_path in directory_files:
        if file_path.find(".hpp") > -1 or file_path.find(".ext") > -1:
            clean_data_etc(file_path, True, False, False)
        elif file_path.find(".sqf") > -1:
            clean_data_etc(file_path, True, False, False)

    print("Bomb's cleaning service has finished")

main_brain()