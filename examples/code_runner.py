from llm_sandbox import SandboxSession
from llm_sandbox.utils import get_libraries_installation_command, get_code_execution_command


def run_python_code():
    with SandboxSession(lang="python", keep_template=True, verbose=True) as session:
        output = session.run("print('Hello, World!')")
        print(output)

        output = session.run(
            "import numpy as np\nprint(np.random.rand())", 
            libraries=["numpy"]
        )
        print(output)

        install_command = get_libraries_installation_command("python", ["pandas"])
        session.execute_command(install_command)
        output = session.run("import pandas as pd\nprint(pd.__version__)")
        print(output)

        session.copy_to_runtime("README.md", "/sandbox/data.csv")


def run_java_code():
    with SandboxSession(lang="java", keep_template=True, verbose=True) as session:
        code = """
        public class Main {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        """
        execution_commands = get_code_execution_command("java", "Main.java")
        session.run(code, execution_commands=execution_commands)


def run_javascript_code():
    with SandboxSession(lang="javascript", keep_template=True, verbose=True) as session:
        output = session.run("console.log('Hello, World!')")
        print(output)

        code = """
        const axios = require('axios');
        axios.get('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => console.log(response.data));
        """
        install_command = get_libraries_installation_command("javascript", ["axios"])
        session.execute_command(install_command)
        output = session.run(code)
        print(output)


def run_cpp_code():
    with SandboxSession(lang="cpp", keep_template=True, verbose=True) as session:
        code = """
        #include <iostream>
        int main() {
            std::cout << "Hello, World!" << std::endl;
            return 0;
        }
        """
        execution_commands = get_code_execution_command("cpp", "main.cpp")
        session.run(code, execution_commands=execution_commands)

        code = """
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
        session.run(code, execution_commands=execution_commands)

        code = """
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
        session.run(code, execution_commands=execution_commands, libraries=["libstdc++"])


if __name__ == "__main__":
    # run_python_code()
    # run_java_code()
    # run_javascript_code()
    run_cpp_code()