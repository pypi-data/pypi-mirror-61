Cannonical source for classifiers on PyPI (pypi.org).

# Usage
Check if a classifier is valid:

```
>>> from packaging_classifiers import classifiers
>>> 'License :: OSI Approved' in classifiers
True
>>> 'Fuzzy :: Wuzzy :: Was :: A :: Bear' in classifiers
False
>>>
```

Determine if a classifier is deprecated:

```
>>> from packaging_classifiers import deprecated_classifiers
>>> 'License :: OSI Approved' in deprecated_classifiers
False
>>> 'Natural Language :: Ukranian' in deprecated_classifiers
True
>>> deprecated_classifiers["Natural Language :: Ukranian"].deprecated_by
['Natural Language :: Ukrainian']
```

Get a pre-sorted list of classifiers:

```
>>> from packaging_classifiers import sorted_classifiers
>>> sorted_classifiers[0]
'Development Status :: 1 - Planning'
>>> sorted_classifiers[-1]
'Typing :: Typed'
```
