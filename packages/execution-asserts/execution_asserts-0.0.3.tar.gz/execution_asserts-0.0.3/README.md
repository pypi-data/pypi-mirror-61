[![PyPI version](https://badge.fury.io/py/execution-asserts.svg)](https://badge.fury.io/py/execution-asserts)
[![PyPI download month](https://img.shields.io/pypi/dm/execution-asserts.svg)](https://pypi.python.org/pypi/execution-asserts/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/execution-asserts.svg)](https://pypi.python.org/pypi/execution-asserts/)


# execution-asserts

A collection of asserts for testing performance of the methods.

## List of asserts
    
   `assertMaximumExecutionTime(max_execution_time_seconds, func, *args, **kwargs)`
   
        
   `assertMaximumMemoryUsage(max_memory_usage, func, *args, **kwargs)`

## How to use 

Look at this sample :
    
    import unittest

    from execution_assets import ExecutionTest
    
    def my_method(input_parameter):
        pass
     
     
    class MyTestCase(unittest.TestCase, ExecutionTest):
        def test_execution_time(self):
            self.assertMaximumExecutionTime(0.3, my_method, 'test_value')
            
        def test_memory_usage(self):
            self.assertMaximumMemoryUsage(12, my_method, 'test_value')
