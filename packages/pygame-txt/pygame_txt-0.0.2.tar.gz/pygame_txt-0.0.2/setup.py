import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygame_txt", # Replace with your own username
    version="0.0.2",
    author="hazelpy",
    author_email="hazelpytv@gmail.com",
    description="Library for working with text in Pygame.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hazelpy/pygame-txt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
