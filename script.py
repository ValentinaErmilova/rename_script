import os
import re

def replace_text_in_files(directory, replacements, file_extensions=None):
    for root, _, files in os.walk(directory):

        if root.find("idea") > -1 or root.find("svn") > -1:
            continue
        for filename in files:
            if file_extensions and not any(filename.endswith(ext) for ext in file_extensions):
                continue

            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                modified_content = content
                for pattern, replacement in replacements.items():
                    modified_content = re.sub(pattern, replacement, modified_content)

                if modified_content != content:  # Only write if changes were made
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    print(f"Modified: {filepath}")
                else:
                    print(f"No changes in: {filepath}")

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

def rename_files_by_regex(directory_path, replacements):
    for root, _, files in os.walk(directory_path):
        old_filepath = os.path.join(directory_path, root)
        if root.find("idea") > -1 or root.find("svn") > -1:
            continue
        for pattern, replacement in replacements.items():
            match = re.search(pattern, root)
            if match:
                new_filename = re.sub(pattern, replacement, root)
                new_filepath = os.path.join(directory_path, new_filename)
                try:
                    os.rename(old_filepath, new_filepath)
                    print(f"Renamed '{root}' to '{new_filename}'")
                except FileExistsError:
                    print(f"Error: '{new_filepath}' already exists. Skipping.")
                except Exception as e:
                    print(f"Error renaming '{root}': {e}")

if __name__ == "__main__":
    target_directory = 'C:\\SVN\\ER-Telecom_product\\AM-Correlation_Engine'
    files_replacements = {
        r'^package com.netcracker' : 'package ru.austromyrtus'
        , r'^import com.netcracker' : 'import ru.austromyrtus'
        , r'^import static com.netcracker' : 'import static ru.austromyrtus'
        , r'(com.netcracker)': 'ru.austromyrtus'
        , r'(nc.)': 'am.'
        , r'\b[N][C]s*' : 'AM'
        , r'\b[n][n]s*': 'am'
        # , r'\b[n][c][_]s*': 'am_'
        #, r'[nc][nc]_': 'am_'
        , r'(ncobject)': 'amobject'
        , r'(netcracker)': 'austromyrtus'
        , r'(NetCracker)': 'Austromyrtus'
        , r'(NETCRACKER)': 'AUSTROMYRTUS'
        , r'(_NC_)': '_AM_'
        , r'"(com/netcracker/)"gm': 'ru/austromyrtus/'
    }
    directory_replacements = {
        r'\b(com)' : 'ru'
        , r'\b(netcracker)': 'austromyrtus'
    }
    file_types_to_process = ['.txt', '.java', '.sql', '.sqt', '.html', '.xml', '.jsp', '.list', '.lst']
    #rename_files_by_regex(target_directory, directory_replacements)
    #rename_files_by_regex(target_directory, directory_replacements)
    replace_text_in_files(target_directory, files_replacements, file_types_to_process)