# testreport-ng


[![PyPI version](https://badge.fury.io/py/testreportng.svg)](https://badge.fury.io/py/testreportng)
![CI Status](https://github.com/williamfzc/testreportng/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/williamfzc/testreportng/branch/master/graph/badge.svg?token=18PMrmYcAk)](https://codecov.io/gh/williamfzc/testreportng)

next generation of test report, for unittest.

## goal

`unittest` is the standard library of Python. It's powerful and robust, but not designed for human I think.

Because of its weird API, I have already felt tired to hack `unittest` again, again and again. This package offers a middle layer, which is really easy to extend, on the top of `unittest`. 

Based on this repo, you can easily get results from cases or suites, build your own report, or something else. 

## example

```bash
pip install testreportng
```

`NGCase` is a subclass of `unittest.TestCase`, with result collector.

```python
from testreportng import NGCase
import unittest


class NewCase(NGCase):
    def test_pass(self):
        self.assertTrue(True)

    def test_fail(self):
        self.assertTrue(False)

    def test_error(self):
        raise RuntimeError("some error")

# same as unittest.TestCase
runner = unittest.TextTestRunner()
suite = unittest.TestSuite(unittest.TestLoader().loadTestsFromTestCase(NewCase))
runner.run(suite)

# after running, you can access results easily (NGResult object)
result = NewCase.ng_result

# get summary?
print(result.summary())
# {'name': 'NewCase', 'total': 3, 'pass': 1, 'fail': 1, 'error': 1, 'skip': 0}

# programmable?
print(result.data)
"""
{'test_error': <NGCaseDetail name=test_error status=error>, 'test_fail': <NGCaseDetail name=test_fail status=fail>, 'test_pass': <NGCaseDetail name=test_pass status=
pass>}
"""

# to json string?
print(result.to_json())
"""
{
	"test_error": {
		"name": "test_error",
		"status": "error",
		"reason": "",
		"error": "RuntimeError()",
		"traceback": ["  File \"C:\\Python37\\lib\\unittest\\case.py\", lin ... "]
		"start_time": "20191114141643485",
		"end_time": "20191114141643485",
		"duration": "0"
	},
    ...
}
"""

# or, you prefer a dict
for name, case in result.to_dict().items():
    print(f"case: {name}, result: {case}")
    # ...
```

Based on it, building plugins has become very simple. You can use built-in plugins in `ext` for different kinds of functions, such as HTML report?

```python
runner = unittest.TextTestRunner()
suite = unittest.TestSuite(unittest.TestLoader().loadTestsFromTestCase(NewCase))
runner.run(suite)

result = NewCase.ng_result
html = HtmlReporter.render("YOUR_TEST_NAME", result)
with open("your_report.html", "w+") as f:
    f.write(html)
```

you can see a html report ...

![report.png](https://i.loli.net/2019/11/14/HGJDKSbizkMrEX6.png)

more example:

- [in production: working with `suite`](./example/suite.py)
- [build your own html report easily](./example/report.py)
- [flexible hook](./example/hook.py)
- [use built-in html report](./example/ext.py)
- ...

## design

Without stepping into `unittest`, this repo builds another layer for plugins. Developers can easily build their own functions / tools without accessing `unittest` itself.

## why not ...

### py.test?

Personal preferences. `unittest` is a built-in package, and I prefer the standard way.

### other third-party runner?

The most of them hacked the `unittest` module directly. So if you want to add some new functions or do some customization, you need to access `unittest` too ... with its weird API.

some eg:

- tungwaiwip / [HTMLTestRunner](https://github.com/tungwaiyip/HTMLTestRunner)
- oldani / [HtmlTestRunner](https://github.com/oldani/HtmlTestRunner)
- ...

actually they nearly do the same things, with lots of redundant codes between them. Maybe they are good, but we should not waste too much time on doing the same things.

## requirements

- python 3.6+ (because of typing hints)
- and nothing else

## license

[MIT](LICENSE)
