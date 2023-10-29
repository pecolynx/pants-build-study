from concurrent import futures

import grpc
from helloworld.v1 import helloworld_pb2_grpc


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(helloworld_pb2_grpc.GreeterServicer(), server)
    server.add_insecure_port(f"[::]:50052")
    server.start()
    print('gRPC server listening at :50052')
    server.wait_for_termination()
