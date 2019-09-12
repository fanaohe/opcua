from opcua import ua, Server
import random
from opcua.common.callback import CallbackType

def create_monitored_items(event, dispatcher):
    '''
    连接成功后默认订阅最深节点，在每次订阅节点时都会打印订阅的节点的ns和i地址
    ns:地址空间序号
    i:深度序号
    '''
    print("Monitored Item")     
    print(event.response_params)
    for idx in range(len(event.response_params)) :
        if (event.response_params[idx].StatusCode.is_good()) :
            nodeId = event.request_params.ItemsToCreate[idx].ItemToMonitor.NodeId
            print("Node {0} was created".format(nodeId))


def modify_monitored_items(event, dispatcher):
    '''
    当修改比率的时候调用
    '''
    print('modify_monitored_items')


def delete_monitored_items(event, dispatcher):
    '''
    删除订阅的时候
    '''
    print('delete_monitored_items')

if __name__ == "__main__":
    server = Server()
    
    server.set_endpoint("opc.tcp://0.0.0.0:4840/discovery")    #客户端连接路由
    server.set_server_name("new demo opcua")          #设置服务器连接后的名称
    
    # setup  namespace
    uri = "http://examples.io"# 创建名称空间（这不是必须的，但是这是一种规范）
    idx = server.register_namespace(uri) #注册名称空间


    objs = server.get_objects_node()     #获取服务器节点对象。
    myobj = objs.add_object(idx, "Devices")    # 向节点对象填充地址节点
    myobj2 = myobj.add_variable(idx,"iii",ua.Variant(20,ua.VariantType.Int32))     #向Devices对象添加tag
    myvar = myobj.add_variable(idx,"humidity",ua.Variant(0,ua.VariantType.Int32))     #向Devices对象添加tag
    myvar2 = myvar.add_variable(idx,"[hhhh]",10)
    myvar.set_writable()    #将myvar设置为客户端可写的
    myvar2.set_writable()    #客户端可写的

    server.start()     #启动服务

    server.historize_node_data_change(myvar, period=None, count=100)    #将myvar标签设置为可变的历史数据

    server.subscribe_server_callback(CallbackType.ItemSubscriptionCreated, create_monitored_items)        #客户端连接成功后的回调
    server.subscribe_server_callback(CallbackType.ItemSubscriptionModified, modify_monitored_items)       #修改订阅时回调
    server.subscribe_server_callback(CallbackType.ItemSubscriptionDeleted, delete_monitored_items)        #删除订阅的时候回调
    
    try:
        import time
        count=0
        while True:
            time.sleep(3)
            value=random.randint(100,1000)
            myvar.set_value(value)
            count += 1
    finally:
        server.stop()


print("wwwww")






