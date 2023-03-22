import unittest
from pytest import *
import update_versions
import tempfile
from packaging.version import parse
import re
from dataclasses import dataclass

@dataclass
class version_cfg:
    """A class to mock the version.cfg file"""
    name ="version.cfg"
    content = """# The format of the file is:
#
# package_name>=version
# package_name<=version
# package_name==version
# package_name>version
# package_name<version
[versions]
setuptools = 42.0.2
zc.buildout = 2.13.3
zc.recipe.egg = 2.0.7
Pillow > 3.4
"""
    expected = """# The format of the file is:
#
# package_name>=version
# package_name<=version
# package_name==version
# package_name>version
# package_name<version
[versions]
setuptools = 67.6.0
zc.buildout = 3.0.1
zc.recipe.egg = 2.0.7
Pillow = 9.4.0
"""
    differs = ["setuptools", "zc.buildout", "zc.recipe.egg", "Pillow"]

class test_update_versions(unittest.TestCase):
    def test_update_versions(self):
        """Test the update_versions function, 
        which should update the version.cfg file at latest version of the packages.
        This version must be greater than or equal to the expected version.
        """
        content = version_cfg.content.splitlines()
        expected = version_cfg.expected.splitlines()
        resplit = lambda line: re.split(">=|<=|=|>|<",line.strip())
        # Create a dictionary of the minimum expected results
        expected_dict = {resplit(line)[0].strip(): resplit(line)[-1].strip() \
            for line in expected \
                if resplit(line)[0].strip() in version_cfg.differs}
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmpfile:
            tmpfile.write(version_cfg.content)
            tmpfile.flush()
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as outfile:
                update_versions.update_versions(open(tmpfile.name), outfile)
                outfile.flush()
                with open(outfile.name) as f:
                    for i, line in enumerate(f):
                        prefix = line.split("=")[0].strip() if "=" in line else ""
                        if prefix in version_cfg.differs:
                            # The result must be greater than or equal to the expected result
                            result = parse(resplit(line)[1].strip())
                            expected_result = parse(expected_dict[prefix])
                            self.assertGreaterEqual(result, expected_result)
                        else:
                            # The result must be equal to the expected result for the same line
                            self.assertEqual(line.strip(), expected[i].strip())