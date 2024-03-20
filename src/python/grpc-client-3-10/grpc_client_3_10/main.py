import sys

import grpc
from helloworld.v1 import helloworld_pb2, helloworld_pb2_grpc

print(sys.version)

with grpc.insecure_channel("localhost:50052") as channel:
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name="John"))
print("Greeter client received: " + response.message)
