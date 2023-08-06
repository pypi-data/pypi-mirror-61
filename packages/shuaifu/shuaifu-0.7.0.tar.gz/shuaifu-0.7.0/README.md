# Shuaifu
Yet another language

## Install

```shell
pip install shuaifu
```

## Usage

```python
import shuaifu

shuaifu.believe() # print believe words 
print(shuaifu.get_version()) # print version
print(shuaifu.translate('woxbyhukfu!')) # translate into pinyin
```

or

```python
import shuaifu

shuaifu.xbyh() # uuiuxbyhwfbf
print(shuaifu.bjbf()) # uuiubjbf
print(shuaifu.fjyi('woxbyhukfu!')) # fjyidcpbyb
```

### Advanced Usage

```python
import shuaifu

@shuaifu.believe
def hello(name):
    print('Hello '+ name)
    
if __name__ == '__main__':
    hello('World')
```

the output will be

```text
函数hello受到了感化,函数hello开始信仰帅副了!
函数hello沐浴教旨,努力工作,终于有了结果
Hello World
```