from llm_sandbox import SandboxSession
from llm_sandbox.utils import get_code_execution_command, get_libraries_installation_command

def run_code(session, code, libraries=None):
    if libraries:
        install_command = get_libraries_installation_command(session.lang, libraries)
        if install_command:
            session.execute_command(install_command)
    execution_commands = get_code_execution_command(session.lang, code)
    for command in execution_commands:
        output = session.run(command)
        print(output)

def run_python_code():
    with SandboxSession(lang="python", keep_template=True, verbose=True) as session:
        run_code(session, "print('Hello, World!')")
        run_code(session, "import numpy as np\nprint(np.random.rand())", libraries=["numpy"])
        run_code(session, "import pandas as pd\nprint(pd.__version__)", libraries=["pandas"])
        session.copy_to_runtime("README.md", "/sandbox/data.csv")

def run_java_code():
    with SandboxSession(lang="java", keep_template=True, verbose=True) as session:
        code = """\n        public class Main {\n            public static void main(String[] args) {\n                System.out.println("Hello, World!");\n            }\n        }\n        """
        run_code(session, code)

def run_javascript_code():
    with SandboxSession(lang="javascript", keep_template=True, verbose=True) as session:
        run_code(session, "console.log('Hello, World!')")
        code = """\n        const axios = require('axios');\n        axios.get('https://jsonplaceholder.typicode.com/posts/1')\n            .then(response => console.log(response.data));\n        """
        run_code(session, code, libraries=["axios"])

def run_cpp_code():
    with SandboxSession(lang="cpp", keep_template=True, verbose=True) as session:
        code = """\n        #include <iostream>\n        int main() {\n            std::cout << "Hello, World!" << std::endl;\n            return 0;\n        }\n        """
        run_code(session, code)

        code = """\n        #include <iostream>\n        #include <vector>\n        int main() {\n            std::vector<int> v = {1, 2, 3, 4, 5};\n            for (int i : v) {\n                std::cout << i << " ";\n            }\n            std::cout << std::endl;\n            return 0;\n        }\n        """
        run_code(session, code)

        code = """\n        #include <iostream>\n        #include <vector>\n        #include <algorithm>\n        int main() {\n            std::vector<int> v = {1, 2, 3, 4, 5};\n            std::reverse(v.begin(), v.end());\n            for (int i : v) {\n                std::cout << i << " ";\n            }\n            std::cout << std::endl;\n            return 0;\n        }\n        """
        run_code(session, code, libraries=["libstdc++"])

if __name__ == "__main__":
    # run_python_code()
    # run_java_code()
    # run_javascript_code()
    run_cpp_code()