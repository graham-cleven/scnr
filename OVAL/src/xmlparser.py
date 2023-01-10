#!/usr/bin/env python3

import sys
import re
import xml.etree.ElementTree as etree
import pprint


class OvalError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        raise Exception(self.value)


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
        self.set_filetype()
        self.set_namespaces()
        self.get_tests()
        self.get_generator()
        self.get_definitions()
        self.get_states()
        self.get_objects()

        # pp.pprint(self.oval["definitions"])

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

    def get_generator(self):
        generator = self.root.find("oval:generator", self.ns)

        if type(generator) is etree.Element:
            # TODO set class member to platform and version
            prod_name = generator.find("common:product_name", self.ns)
            prod_version = generator.find("common:product_version", self.ns)
            schema_version = generator.find("common:schema_version", self.ns)
            timestamp = generator.find("common:timestamp", self.ns)

            if prod_name is not None:
                self.oval["generator"]["product_name"] = prod_name.text

            if prod_version is not None:
                self.oval["generator"]["product_version"] = prod_version.text

            if schema_version is not None:
                self.oval["generator"]["schema_version"] = schema_version.text

            if timestamp is not None:
                self.oval["generator"]["timestamp"] = timestamp.text

    def get_definitions(self):
        # for each definition in the file 
        for definitions in self.root.findall("oval:definitions", self.ns):

            # each member of definition, which is metadata, criteria
            for definition in definitions.findall("oval:definition", self.ns):
                _params = self.get_params(definition.items())
                self.oval["definitions"][_params["id"]] = self.get_definition(
                    definition
                )

    def get_tests(self):
        for tests in self.root.findall("oval:tests", self.ns):
            for test in tests:
                _params = self.get_params(test.items())
                _params["test_meta"] = self.get_test_metadata(test)
                self.oval["tests"][_params["id"]] = _params

    def get_test_metadata(self, test):
        _meta = {}
        for child in test:
            _meta.update(child.items())
        return _meta

    def get_definition(self, definition):
        _def = {"metadata": {}, "criteria": {}}

        _def["metadata"] = self.get_definition_metadata(definition)
        _def["criteria"] = self.get_definition_criterias(definition)

        return _def

    def get_definition_metadata(self, definition):
        _meta = {
            "title": "",
            "description": "",
            "family": "",
            "platform": "",
        }

        if type(definition) is etree.Element:
            metadata = definition.find("oval:metadata", self.ns)

            if type(metadata) is etree.Element:
                title = metadata.find("oval:title", self.ns)
                desc = metadata.find("oval:description", self.ns)
                affected = metadata.find("oval:affected", self.ns)

                if title is not None:
                    _meta["title"] = title.text

                if desc is not None:
                    _meta["description"] = desc.text

                if affected is not None:
                    params = self.get_params(affected.items())
                    if "family" in params.keys():
                        _meta["family"] = params["family"]

                    platform = affected.find("oval:platform", self.ns)

                    if platform is not None:
                        _meta["platform"] = platform.text
        return _meta

    def get_definition_criterias(self, criteria):

        _criterias = []
        criterias = criteria.findall("oval:criteria", self.ns)

        self.pp.pprint(criterias)

        for criteria in criterias:
            
            _criteria = {
                "params": {},
                "criterion": {
                    "comment": "",
                    "test_ref": [],
                    "negate": "",
                },
            }

            _criteria["params"] = self.get_params(criteria.items())

            # extract criterions from criteria
            criterions = criteria.findall(
                "oval:extend_definition", self.ns
            ) + criteria.findall("oval:criterion", self.ns)

            # handle extended_definitions in criteria
            # ex. Some rules such as "Firefox is installed" are considered definition_refs instead of test_refs
            for criterion in criterions:
                try:
                    _criteria["criterion"]["test_ref"].append(
                        self.get_params(criterion.items())["test_ref"]
                    )
                except KeyError:
                    _criteria["criterion"]["test_ref"].append(
                        self.get_params(criterion.items())["definition_ref"]
                    )
            _criterias.append(_criteria)

        return _criterias

    def get_states(self):
        _states = self.root.find("oval:states", self.ns)
        for state in _states:
            _params = self.get_params(state.items())
            self.oval["states"][_params["id"]] = _params

    def get_objects(self):
        objects = self.root.find("oval:objects", self.ns)
        for object in objects:
            _object = self.get_params(object.items())
            self.oval["objects"][_object["id"]] = _object

            for prop in object:
                self.oval["objects"][_object["id"]][prop.tag.split("}")[1]] = prop.text

    def generate_ps(self):
        pass
