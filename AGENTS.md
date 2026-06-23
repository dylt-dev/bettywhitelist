#### db/bwl.db in source control

Having live data in source control can be problematic, but it's useful to have a substantially populated bwl.db in github. In part this is to address something OpenCode did, when it decided to add a tearDown which deleted the database, which was the only example of how the database ought to look. This would not have been a problem, except it wasn't in source control, so it *was* a problem. The ./db/bwl/db file should never represent actual production data, which would live on a server in a separate path, receive backup and other TLC, etc.


#### tools/ folder for tests (or lack thereof)

Other projects have standardized on a tools/ folder for putting test scripts, one-per-task. But Python already has nice standards around where to put tests and how to write them. And while sometimes it's easy to code splunge tests in bash, in general we should keep everything Python that we can. bettywhitelist is a Python web app. Keeping it Python keeps it simple.


### tests

#### test/util.py

util.py has a Tests folder. It doesn't matter if the Tests folder contains actual tests, according to unittest naming patterns. It's still a useful place for utility functions that can be run as one-offs for maintenance. Don't consider its Tests class 'stale' just because it appears to not have any tests.
