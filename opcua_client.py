from IPython import embed
from opcua import Client
class SubHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New data change event:{}".format(val))

if __name__ == "__main__":
    server_url="opc.tcp://10.6.0.75:4840"
    client = Client(server_url)    #连接服务器

    # try:
    client.connect()
    root = client.get_root_node()    #获取根节点
    # obj2 = root.get_children()    #获取所有节点列表
    struct = client.get_node("ns=2;i=2")
    struct_array = client.get_node("ns=2;i=3")
    print("struct:{}".format(struct))
    print("struct_array:{}".format(struct_array))    
    msclt_tss = SubHandler()    #订阅信息回调类

    before = struct.get_value()
    before_array = struct_array.get_value()
    print("before:{}".format(before))
    print("before_array:{}".format(before_array))

    #订阅节点
    handler = SubHandler()
    sub = client.create_subscription(500,handler)
    handle = sub.subscribe_data_change(struct_array)

    sub_tss = client.create_subscription(100, msclt_tss)    #调用接收信息的类
    embed()
    # finally:
    #     client.disconnect()

