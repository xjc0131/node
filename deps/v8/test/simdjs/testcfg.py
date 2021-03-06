# Copyright 2014 the V8 project authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


import os
import shutil
import sys

from testrunner.local import testsuite
from testrunner.objects import testcase

SIMDJS_SUITE_PATH = ["data", "src"]


class SimdJsTestSuite(testsuite.TestSuite):

  def __init__(self, name, root):
    super(SimdJsTestSuite, self).__init__(name, root)
    self.testroot = os.path.join(self.root, *SIMDJS_SUITE_PATH)
    self.ParseTestRecord = None

  def ListTests(self, context):
    tests = [
      testcase.TestCase(self, 'shell_test_runner'),
    ]
    for filename in os.listdir(os.path.join(self.testroot, 'benchmarks')):
      if (not filename.endswith('.js') or
          filename in ['run.js', 'run_browser.js', 'base.js']):
        continue
      name = filename.rsplit('.')[0]
      tests.append(
          testcase.TestCase(self, 'benchmarks/' + name))
    return tests

  def GetFlagsForTestCase(self, testcase, context):
    return (testcase.flags + context.mode_flags +
            [os.path.join(self.root, "harness-adapt.js"),
             "--harmony", "--harmony-simd",
             os.path.join(self.testroot, testcase.path + ".js"),
             os.path.join(self.root, "harness-finish.js")])

  def GetSourceForTest(self, testcase):
    filename = os.path.join(self.testroot, testcase.path + ".js")
    with open(filename) as f:
      return f.read()

  def IsNegativeTest(self, testcase):
    return False

  def IsFailureOutput(self, testcase):
    if testcase.output.exit_code != 0:
      return True
    return "FAILED!" in testcase.output.stdout

  def DownloadData(self):
    print "SimdJs download is deprecated. It's part of DEPS."

    # Clean up old directories and archive files.
    directory_old_name = os.path.join(self.root, "data.old")
    if os.path.exists(directory_old_name):
      shutil.rmtree(directory_old_name)

    archive_files = [f for f in os.listdir(self.root)
                     if f.startswith("ecmascript_simd-")]
    if len(archive_files) > 0:
      print "Clobber outdated test archives ..."
      for f in archive_files:
        os.remove(os.path.join(self.root, f))


def GetSuite(name, root):
  return SimdJsTestSuite(name, root)
