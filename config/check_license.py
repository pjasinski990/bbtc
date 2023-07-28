import os

LICENSE_HEADER = '''"""
   Copyright (c) 2023 Nordic Semiconductor ASA

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
'''


def check_all_files():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                if not check_file_license(os.path.join(root, file)):
                    return False
    return True


def check_file_license(file_path):
    is_ok = True
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        if LICENSE_HEADER not in file_contents:
            print(f'License header not found in {file_path}')
            is_ok = False
        return is_ok


if not check_all_files():
    raise Exception('One or more Python files do not contain the license header')
