---
layout: docs
seotitle: Generating Test Cases | NLP Test | John Snow Labs
title: Generating Test Cases
permalink: /docs/pages/docs/generate
key: docs-install
modify_date: "2023-03-28"
header: true
---

<div class="main-docs" markdown="1"><div class="h3-box" markdown="1">

The `generate()` method automatically generates test cases (based on the provided configuration). 

### Configuring Tests

The configuration for the tests can be passed in the form of a YAML file or using the `configure()` method.

#### Using the YAML Configuration File

```bash 
tests:
  defaults:
    min_pass_rate: 0.65     
    
  robustness:
    lowercase:
      min_pass_rate: 0.60
    uppercase:
      min_pass_rate: 0.60
```

```python
from nlptest import Harness

# Create test Harness with config file
h = Harness(task='text-classification', model='path/to/local_saved_model', hub='spacy', data='test.csv', config='config.yml')
```

#### Using the `.configure()` Method

```python
from nlptest import Harness

# Create test Harness without config file
h = Harness(task='text-classification', model='path/to/local_saved_model', hub='spacy', data='test.csv')

h.configure(
  {
    'tests': {
      'defaults': {
          'min_pass_rate': 0.65
      },
      'robustness': {
          'lowercase': { 'min_pass_rate': 0.60 }, 
          'uppercase': { 'min_pass_rate': 0.60 }
        }
      }
  }
 )
```

</div><div class="h3-box" markdown="1">

### Generating Test Cases

Generating the test cases based on the configuration is as simple as calling the following method:

```python
h.generate()
```

</div><div class="h3-box" markdown="1">

### Viewing Test Cases

After generating test cases you can retrieve them by calling the following method: 

```python
h.testcases()
```

This method returns the produced test cases in form of a Pandas data frame – making them easy to edit, filter, import, or export. We can manually review the list of generated test cases, and decide on which ones to keep or edit. 

A sample test cases dataframe looks like the one given below:

{:.table2}
| category  | test_type |  original | test_case | expected_result | 
| - | - | - | - | - |
|robustness| lowercase | I live in Berlin | i live in berlin | berlin: LOC |
|robustness| uppercase | I live in Berlin | I LIVE IN BERLIN | BERLIN: LOC |


</div></div>