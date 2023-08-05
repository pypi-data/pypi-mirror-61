import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scraperapi_sdk", # Replace with your own username
    version="0.2.2",
    author="ScraperAPI",
    author_email="dan@scraperapi.com",
    description="Scraper API SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://scraperapi.com",
    packages=setuptools.find_packages(),
    classifiers=[
    ],
    python_requires='>=3.0',
)