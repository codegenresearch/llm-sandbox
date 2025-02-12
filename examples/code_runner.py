from llm_sandbox import SandboxSession


def run_python_code():
    with SandboxSession(lang="python", keep_template=True, verbose=True) as session:
        output = session.run("print('Hello, World!')")
        print(output)

        output = session.run(
            "import numpy as np\nprint(np.random.rand())", libraries=["numpy"]
        )
        print(output)

        session.execute_command("pip install pandas")
        output = session.run("import pandas as pd\nprint(pd.__version__)")
        print(output)

        session.copy_to_runtime("README.md", "/sandbox/data.csv")


def run_java_code():
    with SandboxSession(lang="java", keep_template=True, verbose=True) as session:
        output = session.run(
            """\n            public class Main {\n                public static void main(String[] args) {\n                    System.out.println("Hello, World!");\n                }\n            }\n            """,
        )
        print(output)


def run_javascript_code():
    with SandboxSession(lang="javascript", keep_template=True, verbose=True) as session:
        output = session.run("console.log('Hello, World!')")
        print(output)

        output = session.run(
            """\n            const axios = require('axios');\n            axios.get('https://jsonplaceholder.typicode.com/posts/1')\n                .then(response => console.log(response.data));\n            """,
            libraries=["axios"],
        )
        print(output)


def run_cpp_code():
    with SandboxSession(lang="cpp", keep_template=True, verbose=True) as session:
        output = session.run(
            """\n            #include <iostream>\n            int main() {\n                std::cout << "Hello, World!" << std::endl;\n                return 0;\n            }\n            """,
        )
        print(output)

        output = session.run(
            """\n            #include <iostream>\n            #include <vector>\n            int main() {\n                std::vector<int> v = {1, 2, 3, 4, 5};\n                for (int i : v) {\n                    std::cout << i << " ";\n                }\n                std::cout << std::endl;\n                return 0;\n            }\n            """,
        )
        print(output)

        # run with libraries
        output = session.run(
            """\n            #include <iostream>\n            #include <vector>\n            #include <algorithm>\n            int main() {\n                std::vector<int> v = {1, 2, 3, 4, 5};\n                std::reverse(v.begin(), v.end());\n                for (int i : v) {\n                    std::cout << i << " ";\n                }\n                std::cout << std::endl;\n                return 0;\n            }\n            """,
            libraries=["libstdc++"],
        )
        print(output)


if __name__ == "__main__":
    # run_python_code()
    # run_java_code()
    # run_javascript_code()
    run_cpp_code()