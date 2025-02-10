from llm_sandbox import SandboxSession


def run_python_code():
    with SandboxSession(lang="python", keep_template=True, verbose=True) as session:
        code = "print('Hello, World!')"
        output = session.run(code)
        print(output)

        code = """
        import numpy as np
        print(np.random.rand())
        """
        output = session.run(code, libraries=["numpy"])
        print(output)

        session.execute_command("pip install pandas")
        code = "import pandas as pd\nprint(pd.__version__)"
        output = session.run(code)
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
        output = session.run(code)
        print(output)


def run_javascript_code():
    with SandboxSession(lang="javascript", keep_template=True, verbose=True) as session:
        code = "console.log('Hello, World!')"
        output = session.run(code)
        print(output)

        code = """
        const axios = require('axios');
        axios.get('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => console.log(response.data));
        """
        output = session.run(code, libraries=["axios"])
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
        output = session.run(code)
        print(output)

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
        output = session.run(code)
        print(output)

        # Run with libraries
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
        output = session.run(code, libraries=["libstdc++"])
        print(output)


if __name__ == "__main__":
    run_python_code()
    run_java_code()
    run_javascript_code()
    run_cpp_code()