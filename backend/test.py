"""
This is a file showing how to use unittest in Python.
"""

import unittest

# 测试以类的形式组织
# 测试以函数的形式运行


# 继承unittest.TestCase
class TestStringMethods(unittest.TestCase):
    def test_example(self):
        self.assertEqual("foo".upper(), "FOO")
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())
        with self.assertRaises(TypeError):
            raise TypeError


if __name__ == "__main__":
    unittest.main()
