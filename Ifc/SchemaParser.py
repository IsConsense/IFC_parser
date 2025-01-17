#!/usr/bin/env python
from Misc import StatementFileReader
from ClassRegistry import create_definition

from GenericDefinition import GenericDefinition
from Entity import Entity
from Function import Function
from Type import Type
from Rule import Rule
from Schema import Schema

class SchemaParser(StatementFileReader):
    """
    Read an Express schema file and parse a definition (typically 'SCHEMA') from it
    """

    def __init__(self):
        """
        Initialise the parser
        """
        StatementFileReader.__init__(self, comment_open="(*", comment_close="*)")


    def read_schema_file(self, filename):
        """
        Open a file and read the first top-level definition from it
        """
        self.fd = open(filename, "r")
        self.reset_state()

        s = self.read_statement(permit_eof=False, zap_whitespaces=True)
        schema = self.parse_definition(s)
        
        self.fd.close()
        
        if schema.classname != "SCHEMA":
            raise SyntaxError("Invalid schema tag '{fmt}'".format(fmt=s))

        return schema


    def parse_definition(self, s):
        """
        Interprets the input string as a '<classname> [<defname> [<defspec>] ]' definition
        (eg. 'TYPE IfcDateTime = STRING'), and create a new definition instance from it.

        As each classname (eg. 'TYPE', 'ENTITY') has a different syntax, we use the
        class registry to find the appropriate definition parser.
        """
        space_pos = s.find(" ")
        if space_pos < 0:
            classname = s
            defname = ''
            defspec = ''
        else:
            classname = s[:space_pos]
            for i in xrange(space_pos + 1, len(s)):
                c = s[i]
                if not(c.isalnum() or c == "_"):
                    classname_end_pos = i
                    break
            else:
                classname_end_pos = -1

            if classname_end_pos < 0:
                defname = s[space_pos + 1:]
                defspec = ''
            else:
                defname = s[space_pos + 1:classname_end_pos]
                defspec = s[classname_end_pos:]

        return create_definition(classname, defname, defspec.strip(), self)

# vim: set sw=4 ts=4 et:
