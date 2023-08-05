# pyyaml-plus

夸文件引用工具，支持跨文件引用变量

文件a.yml:
```
import:
  - b.yml

usr2:
  name: b
  psw: 456
  aslw:
    <<: *usr1
```
文件b.yml:

```
import:
  - eg_folder/c.yml

usr1: &usr1
  <<: *usr3
```

引用：

```
from yamlplus import load

with open('a.yml') as f:
    result = load(f.read())
    print(result)

```