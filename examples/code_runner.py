from llm_sandbox import SandboxSession
from llm_sandbox.utils import get_libraries_installation_command, get_code_execution_command, SupportedLanguage

def run_code(session, code, libraries=None):
    if libraries:
        installation_command = get_libraries_installation_command(session.lang, libraries)
        if installation_command:
            session.execute_command(installation_command)
    
    execution_commands = get_code_execution_command(session.lang, code)
    for command in execution_commands:
        output = session.run(command)
        print(output)

def run_python_code():
    with SandboxSession(lang=SupportedLanguage.PYTHON, keep_template=True, verbose=True) as session:
        run_code(session, "print('Hello, World!')")
        run_code(session, "import numpy as np\nprint(np.random.rand())", libraries=["numpy"])
        run_code(session, "import pandas as pd\nprint(pd.__version__)", libraries=["pandas"])
        session.copy_to_runtime("README.md", "/sandbox/data.csv")

def run_java_code():
    with SandboxSession(lang=SupportedLanguage.JAVA, keep_template=True, verbose=True) as session:
        code = """
        public class Main {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        """
        run_code(session, code)

def run_javascript_code():
    with SandboxSession(lang=SupportedLanguage.JAVASCRIPT, keep_template=True, verbose=True) as session:
        run_code(session, "console.log('Hello, World!')")
        code = """
        const axios = require('axios');
        axios.get('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => console.log(response.data));
        """
        run_code(session, code, libraries=["axios"])

def run_cpp_code():
    with SandboxSession(lang=SupportedLanguage.CPP, keep_template=True, verbose=True) as session:
        code1 = """
        #include <iostream>
        int main() {
            std::cout << "Hello, World!" << std::endl;
            return 0;
        }
        """
        run_code(session, code1)
        
        code2 = """
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
        """
        run_code(session, code2)
        
        code3 = """
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
        run_code(session, code3, libraries=["libstdc++"])

if __name__ == "__main__":
    # run_python_code()
    # run_java_code()
    # run_javascript_code()
    run_cpp_code()