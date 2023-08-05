import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mypkg-zmhus",
    version="0.0.5",
    author="zmhus",
    author_email="zmhus@foxmail.com",
    description="just for test",
    packages=setuptools.find_packages(),
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # py_modules=["mysqlutils", "test1"],
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    # python_requires='>=3.6',
)
