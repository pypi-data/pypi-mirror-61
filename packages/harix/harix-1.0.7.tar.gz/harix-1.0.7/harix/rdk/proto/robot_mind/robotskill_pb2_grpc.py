# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from harix.rdk.proto.robot_mind import robotskill_pb2 as robot__mind_dot_robotskill__pb2


class RobotSkillServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.EnableSkill = channel.unary_unary(
        '/robotmind.RobotSkillService/EnableSkill',
        request_serializer=robot__mind_dot_robotskill__pb2.EnableSkillRequest.SerializeToString,
        response_deserializer=robot__mind_dot_robotskill__pb2.EnableSkillResponse.FromString,
        )
    self.HandleAction = channel.unary_unary(
        '/robotmind.RobotSkillService/HandleAction',
        request_serializer=robot__mind_dot_robotskill__pb2.ActionRequest.SerializeToString,
        response_deserializer=robot__mind_dot_robotskill__pb2.ActionResponse.FromString,
        )


class RobotSkillServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def EnableSkill(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def HandleAction(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_RobotSkillServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'EnableSkill': grpc.unary_unary_rpc_method_handler(
          servicer.EnableSkill,
          request_deserializer=robot__mind_dot_robotskill__pb2.EnableSkillRequest.FromString,
          response_serializer=robot__mind_dot_robotskill__pb2.EnableSkillResponse.SerializeToString,
      ),
      'HandleAction': grpc.unary_unary_rpc_method_handler(
          servicer.HandleAction,
          request_deserializer=robot__mind_dot_robotskill__pb2.ActionRequest.FromString,
          response_serializer=robot__mind_dot_robotskill__pb2.ActionResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'robotmind.RobotSkillService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
