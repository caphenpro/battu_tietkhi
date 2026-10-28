from setuptools import setup

setup(
    name="battu_tietkhi",
    version="1.2.3",
    py_modules=["battu_tietkhi","battu_cli"],
    packages=["amlich"],
    description="Thuật toán xác định tháng Can Chi Bát Tự theo kinh độ mặt trời",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="caphenpro",
    url="https://github.com/caphenpro/battu_tietkhi",
    license="MIT",
    python_requires=">=3.9",
    extras_require={"precise": ["astronomy-engine>=2.1"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Vietnamese",
    ],
)
