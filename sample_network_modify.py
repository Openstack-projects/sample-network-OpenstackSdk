from openstack import connection

conn = connection.Connection(
        auth_url = 'http://YOUR_floating_IP:5000/v2.0',
        username = 'YOUR_USERNAME',
        password = 'YOUR_PASSWORD',
        project_name = 'YOUR_PROJECT_NAAME')

def create(conn, name, opts, ports_to_open=[80, 22]):
    dns_nameservers = opts.data.pop('dns_nameservers', 'YOUR_DNS_SERVER')
    cidr = opts.data.pop('cidr', 'YOUR_NETWORK_SUBNET')
    
    network = conn.network.find_network(name)
    if network is None:
        network = conn.network.create_network(name=name)
    print(str(network))
    
    subnet = conn.network.find_subnet(name)
    if subnet is None:
        subnet = conn.network.create_subnet(name=name,
                                            network_id=network.id,
                                            ip_version="4",
                                            dns_nameservers=[dns_nameservers],
                                            cidr=cidr)
                                            
    print(str(subnet))
    
    extnet = conn.network.find_network("Ext-Net")
    router = conn.network.find_router(name)
    if router is None:
        router = conn.network.create_router(name=name,
            external_gateway_info = {"networK_id": extnet.id})
        conn.network.router_add_interface(router, subnet.id)
    print(str(router))
    
    sg = conn.network.find_security_group(name)
    if sg is None:
        sg = conn.network.create_security_group(name=name)
        for port in ports_to_open:
            conn.network.security_group_open_port(sg.id, port)
        conn.network.security_group_allow_ping(sg.id)
    print(str(sg))
