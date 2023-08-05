# dingding-helper

## Usage
```
pip install dingdinghelper
```

Example

```python
from dingdinghelper import DingDingHelper

if __name__ == "__main__":
  ding = DingDingHelper()
  ding.username = '13712345678'
  ding.password = 'xxxpassword'
  ding.corpid = '...'
  ding.corpsecret = '...'
  ding.msgurl = 'https://oapi.dingtalk.com/robot/send?access_token=...'
  ding.send_msg('DingDingHelper Test')
  ding.upload_file("E:/xxx.zip", 483476421, '/xxx/')
```

## Publish to PyPI

```
pip install --user --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```
