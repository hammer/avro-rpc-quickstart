#!/usr/bin/env python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

from avro import protocol
from avro.genericio import DatumWriter
from avro.io import Encoder

PROTOCOL = protocol.parse(open("../avro/mail.avpr").read())

MESSAGE_SCHEMA = PROTOCOL.gettypes()['Message']

SAMPLE_RECORD = {'to': 'jeff',
                 'from': 'pat',
                 'body': 'hello_jeff'}

OUTFILE_NAME = 'avro.out'

def write_datum_to_file(schema, datum, outfile_name):
    outfile = file(outfile_name, 'w')
    outcoder = Encoder(outfile)

    writer = DatumWriter(schema)
    writer.write(datum, outcoder)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise UsageError("Usage: <to> <from> <body>")

    # fill in the Message record
    message = dict()
    message['to'] = sys.argv[1]
    message['from'] = sys.argv[2]
    message['body'] = sys.argv[3]

    # Write the Message record to a file
    write_datum_to_file(MESSAGE_SCHEMA, message, OUTFILE_NAME)


    
