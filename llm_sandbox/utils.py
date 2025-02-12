import docker
import docker.errors
from typing import List, Optional
import os
from docker import DockerClient
from llm_sandbox.const import SupportedLanguage, DefaultImage


def image_exists(client: DockerClient, image: str) -> bool:
    """\n    Check if a Docker image exists\n    :param client: Docker client\n    :param image: Docker image\n    :return: True if the image exists, False otherwise\n    """
    try:
        client.images.get(image)
        return True
    except docker.errors.ImageNotFound:
        return False
    except Exception as e:
        raise e


def get_libraries_installation_command(
    lang: str, libraries: List[str]
) -> Optional[str]:
    """\n    Get the command to install libraries for the given language\n    :param lang: Programming language\n    :param libraries: List of libraries\n    :return: Installation command\n    """
    if lang == SupportedLanguage.PYTHON:
        return f"pip install {' '.join(libraries)}"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return f"yarn add {' '.join(libraries)}"
    elif lang == SupportedLanguage.CPP:
        return f"apt-get update && apt-get install -y {' '.join(libraries)}"
    elif lang == SupportedLanguage.GO:
        return f"go get {' '.join(libraries)}"
    elif lang == SupportedLanguage.RUBY:
        return f"gem install {' '.join(libraries)}"
    else:
        raise ValueError(f"Language {lang} is not supported")


def get_code_file_extension(lang: str) -> str:
    """\n    Get the file extension for the given language\n    :param lang: Programming language\n    :return: File extension\n    """
    if lang == SupportedLanguage.PYTHON:
        return "py"
    elif lang == SupportedLanguage.JAVA:
        return "java"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return "js"
    elif lang == SupportedLanguage.CPP:
        return "cpp"
    elif lang == SupportedLanguage.GO:
        return "go"
    elif lang == SupportedLanguage.RUBY:
        return "rb"
    else:
        raise ValueError(f"Language {lang} is not supported")


def get_code_execution_command(lang: str, code_file: str) -> str:
    """\n    Get the command to execute the code\n    :param lang: Programming language\n    :param code_file: Path to the code file\n    :return: Execution command\n    """
    if lang == SupportedLanguage.PYTHON:
        return f"python {code_file}"
    elif lang == SupportedLanguage.JAVA:
        class_name = os.path.splitext(os.path.basename(code_file))[0]
        return f"javac {code_file} && java {class_name}"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return f"node {code_file}"
    elif lang == SupportedLanguage.CPP:
        executable = os.path.splitext(code_file)[0]
        return f"g++ {code_file} -o {executable} && ./{executable}"
    elif lang == SupportedLanguage.GO:
        return f"go run {code_file}"
    elif lang == SupportedLanguage.RUBY:
        return f"ruby {code_file}"
    else:
        raise ValueError(f"Language {lang} is not supported")


def run_code_in_sandbox(lang: str, code: str, libraries: List[str] = None):
    client = docker.from_env()
    image = DefaultImage.__dict__.get(lang.upper())
    if not image:
        raise ValueError(f"No default image found for language {lang}")
    
    if not image_exists(client, image):
        print(f"Pulling image {image}...")
        client.images.pull(image)
    
    code_file = f"code.{get_code_file_extension(lang)}"
    commands = [
        f"echo '{code}' > {code_file}",
        "chmod +x " + code_file if lang == SupportedLanguage.CPP else "",
        get_libraries_installation_command(lang, libraries) if libraries else "",
        get_code_execution_command(lang, code_file)
    ]
    
    container = client.containers.run(
        image,
        command="/bin/sh -c '" + " && ".join(filter(None, commands)) + "'",
        detach=True,
        stdout=True,
        stderr=True,
        remove=True
    )
    
    output, errors = container.communicate()
    print("Output:", output.decode())
    if errors:
        print("Errors:", errors.decode())


if __name__ == "__main__":
    # Example usage
    run_code_in_sandbox("python", "print('Hello, World!')")
    run_code_in_sandbox("java", """\n        public class Main {\n            public static void main(String[] args) {\n                System.out.println("Hello, World!");\n            }\n        }\n    """)
    run_code_in_sandbox("javascript", "console.log('Hello, World!')")
    run_code_in_sandbox("cpp", """\n        #include <iostream>\n        int main() {\n            std::cout << "Hello, World!" << std::endl;\n            return 0;\n        }\n    """)
    run_code_in_sandbox("go", """\n        package main\n        import "fmt"\n        func main() {\n            fmt.Println("Hello, World!")\n        }\n    """)
    run_code_in_sandbox("ruby", "puts 'Hello, World!'")