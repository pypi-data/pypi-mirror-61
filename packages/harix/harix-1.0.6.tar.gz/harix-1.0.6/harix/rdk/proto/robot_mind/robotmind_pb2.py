# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: robot-mind/robotmind.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from harix.rdk.proto.common import common_pb2 as common_dot_common__pb2
from harix.rdk.proto.robot_mind import robotskill_pb2 as robot__mind_dot_robotskill__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='robot-mind/robotmind.proto',
  package='robotmind',
  syntax='proto3',
  serialized_options=_b('\n%com.cloudminds.harix.skill.robotskillB\017RobotSkillProtoP\001Z7cloudminds.com/harix/harix-skill-robot/proto/robot-mind'),
  serialized_pb=_b('\n\x1arobot-mind/robotmind.proto\x12\trobotmind\x1a\x13\x63ommon/common.proto\x1a\x1brobot-mind/robotskill.proto\"\\\n\x14RegisterSkillRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\nskill_addr\x18\x02 \x01(\t\x12\x0e\n\x06skills\x18\x03 \x03(\t\x12\x12\n\nskill_info\x18\x04 \x01(\t2\xf2\x01\n\x10RobotMindService\x12M\n\rRegisterSkill\x12\x1f.robotmind.RegisterSkillRequest\x1a\x19.robotmind.ActionResponse\"\x00\x12J\n\x11SendUnknownAction\x12\x18.robotmind.ActionRequest\x1a\x19.robotmind.ActionResponse\"\x00\x12\x43\n\nSendAction\x12\x18.robotmind.ActionRequest\x1a\x19.robotmind.ActionResponse\"\x00\x42s\n%com.cloudminds.harix.skill.robotskillB\x0fRobotSkillProtoP\x01Z7cloudminds.com/harix/harix-skill-robot/proto/robot-mindb\x06proto3')
  ,
  dependencies=[common_dot_common__pb2.DESCRIPTOR,robot__mind_dot_robotskill__pb2.DESCRIPTOR,])




_REGISTERSKILLREQUEST = _descriptor.Descriptor(
  name='RegisterSkillRequest',
  full_name='robotmind.RegisterSkillRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='robotmind.RegisterSkillRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='skill_addr', full_name='robotmind.RegisterSkillRequest.skill_addr', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='skills', full_name='robotmind.RegisterSkillRequest.skills', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='skill_info', full_name='robotmind.RegisterSkillRequest.skill_info', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=91,
  serialized_end=183,
)

DESCRIPTOR.message_types_by_name['RegisterSkillRequest'] = _REGISTERSKILLREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RegisterSkillRequest = _reflection.GeneratedProtocolMessageType('RegisterSkillRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERSKILLREQUEST,
  '__module__' : 'robot_mind.robotmind_pb2'
  # @@protoc_insertion_point(class_scope:robotmind.RegisterSkillRequest)
  })
_sym_db.RegisterMessage(RegisterSkillRequest)


DESCRIPTOR._options = None

_ROBOTMINDSERVICE = _descriptor.ServiceDescriptor(
  name='RobotMindService',
  full_name='robotmind.RobotMindService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=186,
  serialized_end=428,
  methods=[
  _descriptor.MethodDescriptor(
    name='RegisterSkill',
    full_name='robotmind.RobotMindService.RegisterSkill',
    index=0,
    containing_service=None,
    input_type=_REGISTERSKILLREQUEST,
    output_type=robot__mind_dot_robotskill__pb2._ACTIONRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SendUnknownAction',
    full_name='robotmind.RobotMindService.SendUnknownAction',
    index=1,
    containing_service=None,
    input_type=robot__mind_dot_robotskill__pb2._ACTIONREQUEST,
    output_type=robot__mind_dot_robotskill__pb2._ACTIONRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SendAction',
    full_name='robotmind.RobotMindService.SendAction',
    index=2,
    containing_service=None,
    input_type=robot__mind_dot_robotskill__pb2._ACTIONREQUEST,
    output_type=robot__mind_dot_robotskill__pb2._ACTIONRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ROBOTMINDSERVICE)

DESCRIPTOR.services_by_name['RobotMindService'] = _ROBOTMINDSERVICE

# @@protoc_insertion_point(module_scope)
