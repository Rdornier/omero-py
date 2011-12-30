#!/usr/bin/env python

"""
   Test of the omero db control.

   Copyright 2009 Glencoe Software, Inc. All rights reserved.
   Use is subject to license terms supplied in LICENSE.txt

"""

import unittest, os, subprocess, StringIO
from path import path
from omero.plugins.db import DatabaseControl
from omero.cli import Context, CLI, NonZeroReturnCode
from clitest.mocks import MockCLI

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.cli = MockCLI()
        self.cli.register("db", DatabaseControl, "TEST")
        db = self.cli.controls["db"]
        data = db.loaddefaults()
        self.data = {}
        for x in ("version", "patch"):
            self.data[x] = data.properties.getProperty("omero.db."+x)

    def invoke(self, string, strict=True):
        self.cli.invoke(string % self.data, strict=strict)

    def testBadVersionDies(self):
        self.assertRaises(NonZeroReturnCode, self.invoke, "db script NONE NONE pw")

    def testPasswordIsAskedForAgainIfDiffer(self):
        self.expectPassword("ome")
        self.expectConfirmation("bad")
        self.expectPassword("ome")
        self.expectConfirmation("ome")
        self.invoke("db script '' ''")

    def testPasswordIsAskedForAgainIfEmpty(self):
        self.expectPassword("")
        self.expectPassword("ome")
        self.expectConfirmation("ome")
        self.invoke("db script %(version)s %(patch)s")

    def testPassword(self):
        self.expectPassword("ome")
        self.expectConfirmation("ome")
        self.invoke("db password")

    def testAutomatedPassword(self):
        self.invoke("db password ome")

    def testScript(self):
        self.expectVersion(self.data["version"])
        self.expectPatch(self.data["patch"])
        self.expectPassword("ome")
        self.expectConfirmation("ome")
        self.invoke("db script")

    def testAutomatedScript1(self):

        # This should not be asked for, but ignoring for the moment
        self.expectVersion(self.data["version"])

        self.expectPatch(self.data["patch"])
        self.expectPassword("ome")
        self.expectConfirmation("ome")
        self.invoke("db script %(version)s")

    def testAutomatedScript2(self):
        self.expectPassword("ome")
        self.expectConfirmation("ome")
        self.invoke("db script %(version)s %(patch)s")

    def testAutomatedScript3(self):
        self.invoke("db script %(version)s %(patch)s ome")

    def expectPassword(self, pw, user="root"):
        self.cli.expect("Please enter password for OMERO %s user: " % user, pw)

    def expectConfirmation(self, pw, user="root"):
        self.cli.expect("Please re-enter password for OMERO %s user: " % user, pw)

    def expectVersion(self, version):
        self.cli.expect("Please enter omero.db.version [%s]: " % \
                self.data["version"], version)

    def expectPatch(self, patch):
        self.cli.expect("Please enter omero.db.patch [%s]: " % \
                self.data["patch"], patch)

if __name__ == '__main__':
    unittest.main()
