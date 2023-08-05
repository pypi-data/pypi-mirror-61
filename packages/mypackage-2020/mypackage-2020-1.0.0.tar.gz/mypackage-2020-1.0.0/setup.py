import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mypackage-2020",      #这里必须是一个唯一名字
    version="1.0.0",    #版本号
    packages=setuptools.find_packages(), # 若发布无包模块,使用py_modules
    author="Example Author",   #作者
    author_email="author@example.com",   #作者邮箱
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",   #项目开源地址
    classifiers=[        #项目分类描述
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pymysql'],    #项目依赖的库
    python_requires='>=3.6',    #适用的 python 版本
)



