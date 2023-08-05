# internal
APP_ID: bytes
AUTH_CODE: int

# Message
def cq_send_private_msg(auth_code: int, qq: int, msg: bytes) -> int: ...
def cq_send_group_msg(auth_code: int,group_id:int,msg:bytes) -> int: ...
def cq_send_discuss_msg(auth_code: int,discuss_id:int,msg:bytes) -> int: ...
def cq_delete_msg(auth_code: int,msg_id:int) -> int: ...

# friend operation
def cq_send_like(auth_code: int, qq:int) -> int: ...
def cq_send_like_v2(auth_code: int, qq:int) -> int: ...

# group operation
def cq_set_group_kick(auth_code: int, group_id:int, qq:int, reject_add_request: int) -> int: ...
def cq_set_group_ban(auth_code: int, group_id: int, qq: int, duration: int) -> int: ...
def cq_set_group_anonymous_ban(auth_code: int, group_id: int, anonymous: bytes, duration: int) -> int: ...
def cq_set_group_whole_ban(auth_code: int, group_id: int, enable: int) -> int: ...
def cq_set_group_admin(auth_code: int, group_id: int, qq: int, set: int) -> int: ...
def cq_set_group_anonymous(auth_code: int, group_id: int, enable: int) -> int: ...
def cq_set_group_card(auth_code: int, group_id: int, qq: int, new_card: bytes) -> int: ...
def cq_set_group_leave(auth_code: int, group_id: int, is_dismiss: int) -> int: ...
def cq_set_group_special_title(auth_code: int, group_id: int, qq: int, new_special_title: bytes, duration: int) -> int: ...
def cq_set_discuss_leave(auth_code: int, discuss_id: int) -> int: ...

# request
def cq_set_friend_add_request(auth_code: int, response_flag: bytes, response_operation: int, remark: bytes) -> int: ...
def cq_set_group_add_request(auth_code: int, response_flag: bytes, request_type: int, response_operation: int) -> int: ...
def cq_set_group_add_request_v2(auth_code: int, response_flag: bytes, request_type: int, response_operation: int, reason: bytes) -> int: ...

# QQ Information
def cq_get_login_qq(auth_code: int) -> int: ...
def cq_get_login_nick(auth_code: int) -> bytes: ...
def cq_get_stranger_info(auth_code: int, qq: int, no_cache: int) -> bytes: ...
def cq_get_friend_list(auth_code: int, reserved: int) -> bytes: ...
def cq_get_group_list(auth_code: int) -> bytes: ...
def cq_get_group_info(auth_code: int, group_id: int, no_cache: int) -> bytes: ...
def cq_get_group_member_list(auth_code: int, group_id: int) -> bytes: ...
def cq_get_group_member_info_v2(auth_code: int, group_id: int, qq: int, no_cache: int) -> bytes: ...

# CoolQ
def cq_get_cookies(auth_code: int) -> bytes: ...
def cq_get_cookies_v2(auth_code: int, domain: bytes) -> bytes: ...
def cq_get_csrf_token(auth_code: int) -> int: ...
def cq_get_app_directory(auth_code: int) -> bytes: ...
def cq_get_record(auth_code: int, file: bytes, out_format: bytes) -> bytes: ...
def cq_get_record_v2(auth_code: int, file: bytes, out_format: bytes) -> bytes: ...
def cq_get_image(auth_code: int, file: bytes) -> bytes: ...
def cq_can_send_image(auth_code: int) -> int: ...
def cq_can_send_record(auth_code: int) -> int: ...
def cq_add_log(auth_code: int, level: int, category: bytes, log_msg: bytes) -> int: ...
def cq_set_fatal(auth_code: int, error_info: bytes) -> int: ...
def cq_set_restart(auth_code: int) -> int: ...