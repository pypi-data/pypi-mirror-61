# A python config system (APCS)


## Notice

code are copied and modified from [addict](https://github.com/mewwts/addict) and [mmcv](https://github.com/open-mmlab/mmcv)

## install

```
pip install apcs

```
or 

```
git clone git@github.com:wangjie-ruc/apcs.git
cd apcs
python setup.py install
```
## usage


```python
# test/config.py

root = '/home/zhangsan/data'
batch_size = 32
gpus = [0, 1, 2]
model_kwargs = dict(num_classes=10, kwargs=dict(pretrained=False))
```

```python test/test1.py```

```python
#  test/test1.py

from apcs import Config

def main():
    cfg = Config.fromfile('test/config.py')
    print(cfg.root)
    print(cfg.gpus)

if __name__ == '__main__':
    main()

```

```python test/test2.py test/config.py --gpus 0 1 2 3 --model_kwargs.num_classes 100   --model_kwargs.kwargs.pretrained```

```python
# test/test2.py

from apcs import Config

def main():
    # the action of boolean variables is just reversing the default value
    # e.g. if pretrained is defined True in config file, 
    # "store_false" is chosen for argparser action, and vice versa
    parser, cfg = Config.auto_argparser()
    args = parser.parse_args()
    cfg.merge_from_options(args)

    print(cfg.gpus)
    print(cfg.model_kwargs)

if __name__ == '__main__':
    main()

```