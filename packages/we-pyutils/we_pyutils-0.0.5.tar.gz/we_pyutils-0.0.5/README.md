# we_pyutils
> WE Python Utils
## 上传
```sh
python setup.py bdist_egg # 生成类似 edssdk-0.0.1-py2.7.egg，支持 easy_install
python setup.py sdist     # 生成类似 edssdk-0.0.1.tar.gz，支持 pip
twine upload dist/we_pyutils-0.0.X.tar.gz
```