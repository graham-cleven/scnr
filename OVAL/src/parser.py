#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import xml.etree.ElementTree as etree
import pprint
import oval
import traceback

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please, specify the xml filepath')
        sys.exit(1)

    read_file = sys.argv[1:][0]
    parse = oval.OvalParser(read_file)
    pp = pprint.PrettyPrinter(indent=4, compact=False)

    def generate_ps(state, object):
        pass

    def extract_states_objects():
        """
        For each definition, extract the states and objects and call generate_ps()
        """

        # pp.pprint(parse.oval["definitions"])
        exit()        

        # for each definition, get the test_refs
        for definition in parse.oval['definitions']:
            # save off definition reference string
            _definition = definition

            try:
                # get the definition object from def string
                definition = parse.oval["definitions"][definition]

                pp.pprint(definition)
                exit()
                # for criteria in criterias
                for criteria in parse.oval["definitions"][definition]:
                    pass

                # for each criterion in criteria in definition object
                for criterion in definition['criteria']:

                    # pp.pprint(criterion)

                    # save the operator for later
                    # TODO make sure this values get populated in xmlparser class
                    if criterion['params']:
                        operator = criterion['params']['operator'] #AND or OR

                    # save off negate value
                    # TODO make sure this this value gets populated in xmlparser class
                    negate = criterion['criterion']['negate']

                    # extract the test_refs and extend_definitions from definition object inside of criteria
                    test_refs = criterion['criterion']['test_ref']
                    for test_ref in test_refs:          
    
                        objects_states = {}
                        # grab the states and objects for each test_ref and extend_definitions
                        if ":tst" in test_ref:
                            # extract the objects and states from the test_ref
                            objects_states = parse.oval['tests'][test_ref]['test_meta']
                            #print("objects_states", objects_states)
    
                        # handle extened definitions
                        #elif ":def" in test_ref:
                            # get the test
                        #    pp.pprint(parse.oval['definitions'][test_ref]); exit()

                        # extract the states and objects
                        #print("_________________________________________")
                        #print(_definition)
                        if "state_ref" in objects_states:
                            # TODO make sure subexpresions are pulled out in parser class
                            state = parse.oval['states'][objects_states['state_ref']]
                            #print("state", state)
                        if "object_ref" in objects_states:
                            object = parse.oval['objects'][objects_states['object_ref']]
                            #print("object", object)

                #generate_ps(1,1)

            except Exception as e:
                traceback.print_exc()
                pass

   
    extract_states_objects()
