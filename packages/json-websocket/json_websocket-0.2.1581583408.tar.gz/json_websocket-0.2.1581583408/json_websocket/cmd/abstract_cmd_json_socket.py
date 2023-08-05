from ..basic.abstract_json_socket import MessageType, AbstractJsonWebsocket


def merge(new_values, default_values):
    nd = {}
    for key, value in default_values.items():
        nv = new_values.get(key, None)
        if isinstance(value, dict) and isinstance(nv, dict):
            nd[key] = merge(value, nv)
        else:
            if nv is None:
                nd[key] = value
            else:
                nd[key] = nv
    return nd


def run_cmd(consumer, cmd, data):
    f = consumer.get_cmd(cmd)
    if f is None:
        raise AttributeError(str(cmd) + " not found")
    if f.accept_consumer:
        data["consumer"] = consumer
    return f(**data)


MESSAGETYPES = {
    "cmd": MessageType(
        type="cmd", data_dict={"cmd": None, "data": {}}, decode_function=run_cmd
    )
}


class AbstractCmdJsonWebsocket(AbstractJsonWebsocket):
    def __init__(self):
        AbstractJsonWebsocket.__init__(self)
        self._available_cmds = {}

        for n, t in MESSAGETYPES.items():
            self.set_message_type(n, t)

    def get_cmd(self, cmd):
        return self._available_cmds.get(cmd)

    def set_cmd(self, cmd, func):
        varnames = func.__code__.co_varnames
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)

        # print(cmd, varnames)
        setattr(call_func, "accept_consumer", "consumer" in varnames)
        setattr(call_func, "accept_source", "source" in varnames)
        self._available_cmds[cmd] = call_func

    def cmd_message(self, cmd, **data):
        return self.message_types["cmd"].encode(cmd=cmd, data=data)
