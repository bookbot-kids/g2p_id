from setuptools import find_packages, setup
import os

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")) as f:
    long_description = f.read()

install_requires = ["num2words", "nltk", "onnxruntime"]

if __name__ == "__main__":
    setup(
        name="g2p_id",
        description="Indonesian G2P.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="w11wo",
        author_email="wilson@bookbotkids.com",
        url="https://github.com/bookbot-kids/g2p_id",
        license="Apache License",
        packages=find_packages(),
        install_requires=install_requires,
        include_package_data=True,
        platforms=["linux", "unix", "windows"],
        python_requires=">=3.6",
    )
