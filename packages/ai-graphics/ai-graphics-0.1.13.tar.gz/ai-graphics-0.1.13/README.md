# 1、创建项目 ai-graphics
setup.py
        
# 2、安装相关工具以及打包：
python -m pip install --user --upgrade setuptools wheel

python -m pip install --user --upgrade twine

python setup.py sdist bdist_wheel

# 3、在 https://test.pypi.org/ 注册账号 Cachcheng 并上传包
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# 或者在 https://pypi.org/ 注册账号 Cachcheng 并上传包
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

# 4、查看地址：
https://pypi.org/project/ai-graphics/
