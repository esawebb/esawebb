"""
This file is autoloaded on python start.

Currently is used to import coverage on startup in order to watch any process creation, allowing parallel test
reporting. If coverage is uninstalled from this project for any reason, the lines referencing coverage must be removed
or even the file if it's not needed anymore.

For more information see: https://coverage.readthedocs.io/en/coverage-5.2/subprocess.html
"""

import coverage
coverage.process_startup()
