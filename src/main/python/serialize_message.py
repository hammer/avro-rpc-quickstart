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
from avro.genericio import DatumWriter, DatumReader
from avro.io import DataFileReader, DataFileWriter, Encoder

PROTOCOL = protocol.parse(open("../avro/mail.avpr").read())

# There must be a better way to get schemas from a protocol
MESSAGE_SCHEMA = PROTOCOL.gettypes()['Message']

OUTFILE_NAME = 'avro.out'

if __name__ == '__main__':
    if len(sys.argv) != 5:
        raise UsageError("Usage: <to> <from> <body> <count>")

    # fill in the Message record
    message = dict()
    message['to'] = sys.argv[1]
    message['from'] = sys.argv[2]
    message['body'] = sys.argv[3]

    # grab the number of copies of the record to write
    try:
        num_records = int(sys.argv[4])
    except:
        num_records = 1

    # write the Message record to a file
    w = file(OUTFILE_NAME, 'w')
    dw = DatumWriter(MESSAGE_SCHEMA)
    dfw = DataFileWriter(MESSAGE_SCHEMA, w, dw)
    for i in range(num_records):
        dfw.append(message)
    dfw.close()

    # read the Message records from the file
    r = file(OUTFILE_NAME, 'r')
    dr = DatumReader(expected = MESSAGE_SCHEMA)
    dfr = DataFileReader(r, dr)
    for record in dfr:
        print record
    dfr.close()
