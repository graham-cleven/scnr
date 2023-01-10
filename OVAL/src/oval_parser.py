#!/usr/bin/env python3

from ast import operator
import sys
import re
from xml.etree.ElementPath import get_parent_map
import xml.etree.ElementTree as etree
import pprint

from attr import attributes


class OvalParser:
    """
    Parse OVAL files
    """

    def __init__(self, xml_file):
        self.pp = pprint.PrettyPrinter(indent=4, compact=False)

        if len(xml_file) < 5:
            print("Please, specify the xml filepath")
            sys.exit(1)

        try:
            self.xmL = etree.parse(xml_file)
        except OSError as e:
            print('Was not possible to open the file %s. "%s"' % (xml_file, e))
            sys.exit(1)

        self.oval = {
            "filetype": "",
            "generator": {
                "product_name": "",
                "product_version": "",
                "schema_version": "",
                "timestamp": "",
            },
            "definitions": {},
            "tests": {},
            "objects": {},
            "states": {},
        }

        self.root = self.xmL.getroot()
        self.criterias = []
        self.set_filetype()
        self.set_namespaces()
        self.get_definitions()

    def get_params(self, items):
        _params = {}
        if type(items) is list or tuple:
            for x, v in items:
                _params[x] = v

        return _params

    def set_filetype(self):
        _def = " ".join(str(v) for v in self.root.items())

        pattern = re.compile("#(ios|independent|unix)")
        check = pattern.findall(_def)

        if "independent" and "ios" in check:
            self.oval["filetype"] = "independent"
        elif "ios" in check:
            self.oval["filetype"] = "ios"
        elif "unix" in check:
            self.oval["filetype"] = "unix"

    def set_namespaces(self):
        self.ns = {
            "oval": "http://oval.mitre.org/XMLSchema/oval-definitions-5",
            "common": "http://oval.mitre.org/XMLSchema/oval-common-5",
            "ios": "http://oval.mitre.org/XMLSchema/oval-definitions-5#ios",
            "unix": "http://oval.mitre.org/XMLSchema/oval-definitions-5#unix",
            "independent": "http://oval.mitre.org/XMLSchema/oval-definitions-5\
            #independent",
        }

    def get_operator(self, criteria):
        attributes = criteria.items()
        return [item for item in attributes if item[0] == "operator"][0][1]

    def get_criteria(self, criteria):

        criterias = []

        for object in criteria.iter():
            if object.tag.endswith("criteria"):
                # start a new critera "container"
                criteria = {
                    "operator": self.get_operator(object),
                    "criterion" : [],
                    # may have nested criteria or criterion
                }

            if object.tag.endswith("criterion"):

                # define the criterion container
                criterion = {"comment": "", "test_ref": ""}

                # if criterions is found, extract comment and test_ref
                # append the criterion to the criterion container
                criterion["comment"] = [
                    item for item in object.items() if item[0] == "comment"
                ][0][1]
                criterion["test_ref"] = [
                    item for item in object.items() if item[0] == "test_ref"
                ][0][1]

                # append criterion container to the criteria container
                criteria["criterion"].append(criterion)

            if object.tag.endswith("extend_definition"):
                pass
        
            criterias.append(criteria)

        return criterias

    def get_definition(self, definition):
        """
        Called once for each definition in the file
        Returns the definition criteria

        """

        # ignore all definitions that are not vulnerabilities
        def_class = self.get_params(definition.items())["class"]
        if def_class == "vulnerability":

            # grab the top level criteria
            _criteria = definition.findall("oval:criteria", self.ns)[0]

            # extract the operator
            operator = self.get_operator(_criteria)

            # define criteria
            definition_parsed = {
                "operator": operator,
                "criteria": [],
            }

            # grab the criteria
            definition_parsed['criteria'] = self.get_criteria(_criteria)
            #self.get_criteria(_criteria)

            return definition_parsed

    def get_definitions(self):
        # for each definition in the file
        for definition in self.root.findall("oval:definitions", self.ns)[0]:

            # get the string identifier of the definition (def:####)
            def_id = self.get_params(definition.items())["id"]

            # append the definition object to the oval object with a key equal to the def_id
            self.oval["definitions"][def_id] = self.get_definition(definition)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please, specify the xml filepath")
        sys.exit(1)

    read_file = sys.argv[1:][0]
    parse = OvalParser(read_file)
    pp = pprint.PrettyPrinter(indent=4, compact=False)

    pp.pprint(parse.oval["definitions"])
