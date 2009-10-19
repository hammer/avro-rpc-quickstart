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
import socket

import avro.ipc as ipc
import avro.genericipc as genericipc
import avro.protocol as protocol
import avro.schema as schema

PROTOCOL = protocol.parse(open("../avro/mail.avpr").read())

SERVER_ADDRESS = ('localhost', 9090)

class MailResponder(genericipc.Responder):
    def __init__(self):
        ipc.ResponderBase.__init__(self, PROTOCOL)

    def invoke(self, msg, req):
        if msg.getname() == 'send':
            req_content = req.values()[0]
            resp = "Sent message to %(to)s from %(from)s with body %(body)s" % \
                   req_content
            return resp
        else:
            raise schema.AvroException("unexpected message:", msg.getname())

def start_server():
    ipc.SocketServer(MailResponder(), SERVER_ADDRESS)

# TODO(hammer): daemonize server
# TODO(hammer): serialize records sent to server to a file
# TODO(hammer): implement new method, replay_history(), to serve file to client
if __name__ == '__main__':
    # I miss TServer and friends
    start_server()

    # No cleanup; it's broken anyways. Just go kill the process.

