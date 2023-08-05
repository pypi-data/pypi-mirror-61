#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自然语言识别接口
"""

from harix.rdk.proto.common import common_pb2


def convert_header(input_header):
    common_req_info = common_pb2.CommonReqInfo(
        tenant_id=input_header["tenant_id"],
        user_id=input_header["user_id"],
        robot_id=input_header["robot_id"],
        robot_type=input_header["robot_type"],
        service_code=input_header["service_code"],
        seq=input_header["seq"]
    )
    return common_req_info
