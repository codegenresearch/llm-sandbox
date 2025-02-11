from llm_sandbox import SandboxSession
import os
from llm_sandbox.const import SupportedLanguage, DefaultImage

def run_code_in_sandbox(lang, code_snippets, libraries=None, files_to_copy=None):
    if libraries is None:
        libraries = []
    if files_to_copy is None:
        files_to_copy = {}

    with SandboxSession(lang=lang, keep_template=True, verbose=True) as session:
        for code in code_snippets:
            output = session.run(code, libraries=libraries)
            print(output)

        for local_path, container_path in files_to_copy.items():
            session.copy_to_runtime(local_path, container_path)

def run_python_code():
    code_snippets = [
        "print('Hello, World!')",
        "import numpy as np\nprint(np.random.rand())",
        "import pandas as pd\nprint(pd.__version__)"
    ]
    libraries = ["numpy", "pandas"]
    run_code_in_sandbox(SupportedLanguage.PYTHON, code_snippets, libraries)

def run_java_code():
    code_snippets = [
        """
        public class Main {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        """
    ]
    run_code_in_sandbox(SupportedLanguage.JAVA, code_snippets)

def run_javascript_code():
    code_snippets = [
        "console.log('Hello, World!')",
        """
        const axios = require('axios');
        axios.get('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => console.log(response.data));
        """
    ]
    libraries = ["axios"]
    run_code_in_sandbox(SupportedLanguage.JAVASCRIPT, code_snippets, libraries)

def run_cpp_code():
    code_snippets = [
        """
        #include <iostream>
        int main() {
            std::cout << "Hello, World!" << std::endl;
            return 0;
        }
        """,
        """
        #include <iostream>
        #include <vector>
        int main() {
            std::vector<int> v = {1, 2, 3, 4, 5};
            for (int i : v) {
                std::cout << i << " ";
            }
            std::cout << std::endl;
            return 0;
        }
        """,
        """
        #include <iostream>
        #include <vector>
        #include <algorithm>
        int main() {
            std::vector<int> v = {1, 2, 3, 4, 5};
            std::reverse(v.begin(), v.end());
            for (int i : v) {
                std::cout << i << " ";
            }
            std::cout << std::endl;
            return 0;
        }
        """
    ]
    libraries = ["libstdc++"]
    files_to_copy = {"README.md": "/sandbox/data.csv"}
    run_code_in_sandbox(SupportedLanguage.CPP, code_snippets, libraries, files_to_copy)

if __name__ == "__main__":
    # run_python_code()
    # run_java_code()
    # run_javascript_code()
    run_cpp_code()