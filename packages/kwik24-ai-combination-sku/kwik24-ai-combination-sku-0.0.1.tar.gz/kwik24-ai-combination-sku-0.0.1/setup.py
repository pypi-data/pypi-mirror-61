import setuptools

with open("ReadMe.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kwik24-ai-combination-sku",
    version="0.0.1",
    author="Santosh Kumar Waddi",
    author_email="santosh.waddi@bigbasket.com",
    description="Combination SKU",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/kwik24/kwik24_ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)