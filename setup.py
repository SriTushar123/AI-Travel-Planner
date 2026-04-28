from setuptools import find_packages,setup
from typing import List

def get_requirements():
    requirements_lst = []
    try:
        with open("requirements.txt","r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if (line and line!="-e ."):
                    requirements_lst.append(line)
    except FileNotFoundError:
        print("requirements.txt was not found")
    return requirements_lst

print(get_requirements())

setup(
    name="AI-Travel-Planner",
    version="0.0.1",
    author="Tushar Srivastava",
    author_email="tusharsrivastava354@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
                    


