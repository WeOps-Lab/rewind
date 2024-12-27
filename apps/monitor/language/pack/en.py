MONITOR_OBJECT_TYPE = {
    "OS": "OS",
    "Web": "Web",
    "K8S": "K8S",
    "Device": "Device",
    "System": "System",
}

MONITOR_OBJECT = {
    "Host": "Host",
    "Website": "Website",
    "Cluster": "Cluster",
    "Pod": "Pod",
    "Node": "Node",
    "Switch": "Switch",
    "Router": "Router",
    "Loadbalance": "Loadbalance",
    "Firewall": "Firewall",
    "Detection Device": "Detection Device",
    "Bastion Host": "Bastion Host",
    "Scanning Device": "Scanning Device",
    "Audit System": "Audit System",
}

MONITOR_OBJECT_PLUGIN = {
    "Host General": {
        "name": "Host",
        "desc": "The host monitoring plugin is used to collect and analyze performance data of hosts, including CPU, memory, disk, and network usage."
    },
    "Host SNMP": {
        "name": "Host（SNMP）",
        "desc": "The SNMP plugin is used to monitor and manage the status of hosts through SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, thereby optimizing network performance and improving management efficiency."
    },
    "Website General": {
        "name": "Website",
        "desc": "The purpose of the website monitoring HTTP plugin is to periodically check the availability and performance of HTTP/HTTPS connections."
    },
    "K8S General": {
        "name": "K8S",
        "desc": "The K8S monitoring plugin is used to monitor the status and health of Kubernetes clusters, including the performance metrics of nodes, containers, and pods."
    },
    "Switch SNMP General": {
        "name": "Switch General（SNMP）",
        "desc": "The SNMP general plugin is used to monitor and manage the status of switches through SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, thereby optimizing network performance and improving management efficiency."
    },
    "Router SNMP General": {
        "name": "Router General（SNMP）",
        "desc": "The SNMP general plugin is used to monitor and manage the status of routers through SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, thereby optimizing network performance and improving management efficiency."
    },
    "Loadbalance SNMP General": {
        "name": "Loadbalance General（SNMP）",
        "desc": "The SNMP general plugin is used to monitor and manage the status of loadbalances through SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, thereby optimizing network performance and improving management efficiency."
    },
    "Firewall SNMP General": {
        "name": "Firewall General（SNMP）",
        "desc": "The SNMP general plugin is used to monitor and manage the status of firewalls through SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, thereby optimizing network performance and improving management efficiency."
    },
    "Detection Device SNMP General": {
        "name": "Detection Device General（SNMP）",
        "desc": "The SNMP general plugin is used to monitor and manage the status of detection devices through SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, thereby optimizing network performance and improving management efficiency."
    },
    "Bastion Host SNMP General": {
        "name": "Bastion Host General（SNMP）",
        "desc": "The SNMP general plugin is used to monitor and manage the status of bastion hosts through SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, thereby optimizing network performance and improving management efficiency."
    },
    "Scanning Device SNMP General": {
        "name": "Scanning Device General（SNMP）",
        "desc": "The SNMP general plugin is used to monitor and manage the status of scanning devices through SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, thereby optimizing network performance and improving management efficiency."
    },
    "Audit System SNMP General": {
        "name": "Audit System General（SNMP）",
        "desc": "The SNMP general plugin is used to monitor and manage the status of audit systems through SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, thereby optimizing network performance and improving management efficiency."
    },
}

MONITOR_OBJECT_METRIC_GROUP = {
    "Host": {
        "CPU": "CPU",
        "CPU Load": "CPU Load",
        "DISK": "Disk",
        "SWAP": "SWAP",
        "MEMORY": "Memory",
        "Net": "Net",
        "UDP": "UDP",
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
    },
    "Website": {
        "HTTP": "HTTP",
    },
    "Cluster": {
        "Counts": "Counts",
        "Utilization": "Utilization",
    },
    "Pod": {
        "Status": "Status",
        "CPU": "CPU",
        "Memory": "Memory",
        "Disk": "Disk",
        "Network": "Network",
    },
    "Node": {
        "Status": "Status",
        "CPU": "CPU",
        "Memory": "Memory",
        "Disk": "Disk",
        "Network": "Network",
        "Load": "Load",
    },
    "Switch": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
    },
    "Router": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
    },
    "Loadbalance": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
    },
    "Firewall": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
    },
    "Detection Device": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
    },
    "Bastion Host": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
    },
    "Scanning Device": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
    },
    "Audit System": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
    }
}

MONITOR_OBJECT_METRIC = {
    "Host": {
        "cpu_summary.usage": {
            "name": "CPU Usage Rate",
            "desc": "Current CPU usage percentage, representing the percentage of CPU that is currently in use. Calculated as the total time in user mode, system mode, interrupts, etc., divided by total time."
        },
        "cpu_summary.idle": {
            "name": "CPU Idle Rate",
            "desc": "Current CPU idle percentage, representing the proportion of time the CPU is not performing any work."
        },
        "cpu_summary.iowait": {
            "name": "Percentage of Time Waiting for IO",
            "desc": "Percentage of time the CPU is idle waiting for I/O operations to complete. Calculated as the time spent waiting for I/O divided by total time."
        },
        "cpu_summary.system": {
            "name": "System Usage Rate",
            "desc": "Percentage of CPU time spent in kernel mode (system tasks), reflecting the time the CPU spends processing system tasks."
        },
        "cpu_summary.user": {
            "name": "User Usage Rate",
            "desc": "Percentage of CPU time spent in user mode, reflecting the time the CPU spends running user programs."
        },
        "load1": {
            "name": "1 Minute Average Load",
            "desc": "Average system load over the last 1 minute, represented as the number of processes running and queued."
        },
        "load5": {
            "name": "5 Minute Average Load",
            "desc": "Average system load over the last 5 minutes, reflecting trends in overall system performance and load."
        },
        "load15": {
            "name": "15 Minute Average Load",
            "desc": "Average system load over the last 15 minutes, providing an overview of the long-term load state of the system."
        },
        "io.w_s": {
            "name": "Disk Write Rate",
            "desc": "Number of write operations per second on the disk, reflecting the frequency and performance of write operations."
        },
        "io.rkb_s": {
            "name": "Disk Read Rate",
            "desc": "Number of read operations per second on the disk, reflecting the frequency and performance of read operations."
        },
        "disk.is_use": {
            "name": "Disk Usage Rate",
            "desc": "Percentage of disk space used relative to total space, indicating the extent of storage utilization."
        },
        "disk.used": {
            "name": "Disk Used Size",
            "desc": "Size of the disk space that is currently used, measured in bytes."
        },
        "env.procs": {
            "name": "Total Number of Processes",
            "desc": "Number of all processes currently running in the system, reflecting the concurrent processing capacity of the system."
        },
        "env.proc_running_current": {
            "name": "Number of Running Processes",
            "desc": "Number of currently active running processes, indicating the current load situation of the system."
        },
        "env.procs_blocked_current": {
            "name": "Number of IO Blocked Processes",
            "desc": "Number of processes currently blocked waiting for I/O operations, indicating I/O performance bottlenecks in the system."
        },
        "mem.total": {
            "name": "Total Physical Memory Size",
            "desc": "Total physical memory installed on the current machine, measured in kilobytes (KB)."
        },
        "mem.free": {
            "name": "Free Physical Memory Amount",
            "desc": "Amount of free physical memory available on the current machine, measured in kilobytes (KB)."
        },
        "mem.cached": {
            "name": "Cache Memory Size",
            "desc": "Amount of physical memory used for cache on the current machine, measured in kilobytes (KB)."
        },
        "mem.buffer": {
            "name": "Buffer Memory Size",
            "desc": "Amount of physical memory used for buffers on the current machine, measured in kilobytes (KB)."
        },
        "mem.usable": {
            "name": "Available Memory for Applications",
            "desc": "Amount of physical memory available for applications to use on the current machine, measured in kilobytes (KB)."
        },
        "mem.pct_usable": {
            "name": "Available Memory Percentage for Applications",
            "desc": "Percentage of total physical memory available for applications to use on the current machine."
        },
        "mem.used": {
            "name": "Memory Used by Applications",
            "desc": "Amount of physical memory used by applications on the current machine, measured in kilobytes (KB)."
        },
        "mem.pct_used": {
            "name": "Application Memory Usage Percentage",
            "desc": "Percentage of physical memory in use by applications on the current machine."
        },
        "mem.psc_used": {
            "name": "Used Physical Memory Amount",
            "desc": "Amount of physical memory that is currently in use, measured in kilobytes (KB)."
        },
        "mem.shared": {
            "name": "Shared Memory Usage",
            "desc": "Amount of shared memory in use on the current machine, measured in kilobytes (KB)."
        },
        "swap.free": {
            "name": "SWAP Free Amount",
            "desc": "Amount of free swap space currently available, measured in bytes."
        },
        "swap.total": {
            "name": "SWAP Total Amount",
            "desc": "Total size of swap space currently available, measured in bytes."
        },
        "swap.used": {
            "name": "SWAP Used Amount",
            "desc": "Amount of swap space that is currently in use, measured in bytes."
        },
        "swap.pct_used": {
            "name": "SWAP Used Percentage",
            "desc": "Percentage of swap space that is currently in use relative to total swap space."
        },
        "net.speed_packets_recv": {
            "name": "Incoming Packets on NIC",
            "desc": "Number of packets received per second by the network interface card (NIC)."
        },
        "net.speed_packets_sent": {
            "name": "Outgoing Packets on NIC",
            "desc": "Number of packets sent per second by the network interface card (NIC)."
        },
        "net.speed_recv": {
            "name": "Incoming Bytes on NIC",
            "desc": "Number of bytes received per second by the network interface card (NIC)."
        },
        "net.speed_sent": {
            "name": "Outgoing Bytes on NIC",
            "desc": "Number of bytes sent per second by the network interface card (NIC)."
        },
        "net.errors": {
            "name": "NIC Error Packets",
            "desc": "Total number of send or receive errors detected by the network card driver."
        },
        "net.dropped": {
            "name": "NIC Dropped Packets",
            "desc": "Total number of packets dropped by the network card driver."
        },
        "net.collisions": {
            "name": "NIC Collision Packets",
            "desc": "Total number of collisions detected on the network card."
        },
        "netstat.cur_udp_indatagrams": {
            "name": "UDP Incoming Packets Amount",
            "desc": "Number of UDP datagrams received by the network interface."
        },
        "netstat.cur_udp_outdatagrams": {
            "name": "UDP Outgoing Packets Amount",
            "desc": "Number of UDP datagrams sent by the network interface."
        },
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    },
    "Website": {
        "http_success.rate": {
            "name": "Probe Status",
            "desc": "This metric indicates the success status of the probe operation. A successful status is represented by 1, while a failure is represented by 0. Monitoring this metric is crucial for ensuring the availability of the system, as it provides a quick indication of the health status of the monitored target. If the value is 0, further investigation is needed to determine the cause of the failure."
        },
        "http_total.duration": {
            "name": "HTTP Duration",
            "desc": "This metric represents the total time taken from initiating an HTTP request to receiving the HTTP response. It is used to assess the performance of web services, especially when handling user requests. An extended duration may indicate lower backend processing efficiency or network latency, which can adversely affect the user experience. It is crucial for enhancing system responsiveness and optimizing performance."
        },
        "http_dns.lookup.time": {
            "name": "DNS Lookup Time",
            "desc": "This metric indicates the time taken to perform DNS resolution. DNS resolution is the process of converting a domain name to an IP address, and higher lookup times can lead to delays and affect user access speeds. Monitoring this metric can help identify potential DNS issues and optimize the performance of domain name resolution in the system."
        },
        "http_ssl": {
            "name": "HTTP SSL",
            "desc": "This metric represents the status of the SSL/TLS connection during an HTTP request. A value of 1 indicates that the connection was successful and encrypted using SSL/TLS, while a value of 0 indicates that encryption is not in use or that the connection has failed. It is commonly used to monitor and confirm whether a web service is securely delivered over SSL/TLS."
        },
        "http_status_code": {
            "name": "HTTP Status Code",
            "desc": "This metric represents the HTTP response status code for an HTTP request. It captures the value of the HTTP response status codes, such as 200 (OK), 404 (Not Found), 500 (Internal Server Error), etc. These status codes are vital for monitoring the health and performance of web applications, assisting in identifying potential issues."
        },
        "http.redirects.count": {
            "name": "Redirects Count",
            "desc": "This metric records the number of redirects that occurred during the processing of an HTTP request. Frequent redirects may indicate overly complex URL structures, leading to prolonged user waiting times. Monitoring this metric aids in identifying unnecessary redirects, allowing for the optimization of URL structures and enhancing user experience."
        },
        "http_content.length.gauge": {
            "name": "HTTP Content Length",
            "desc": "This metric indicates the length of the HTTP response content in bytes. Larger content lengths can result in extended data transfer times and consume more bandwidth. Monitoring this metric is crucial for optimizing website performance or analyzing bandwidth usage. Understanding the size of the response content can assist developers in making optimizations."
        }
    },
    "Cluster": {
        "cluster_pod_count": {
            "name": "Pod Count",
            "desc": "It is used to count the total number of Pods currently present in the Kubernetes cluster. This metric returns the count of Pods running in the cluster, including those across all namespaces."
        },
        "cluster_node_count": {
            "name": "Node Count",
            "desc": "It is used to count the total number of nodes currently available in the Kubernetes cluster. This metric returns the number of nodes in the cluster, helping users understand the scale and resources of the cluster."
        },
        "cluster_cpu_utilization": {
            "name": "CPU Utilization",
            "desc": "Represents the current CPU utilization of the cluster, typically expressed as a percentage."
        },
        "cluster_memory_utilization": {
            "name": "Memory Utilization",
            "desc": "Shows the current memory utilization of the cluster, expressed as a percentage."
        }
    },
    "Pod": {
        "pod_status": {
            "name": "Pod Status",
            "desc": "Retrieves the current status of the Pod, such as Running, Stopped, etc."
        },
        "pod_restart_count": {
            "name": "Restart Count",
            "desc": "Monitors the restart counts of containers in the Pod to assess stability and frequency of issues."
        },
        "pod_cpu_utilization": {
            "name": "CPU Utilization",
            "desc": "Calculates the CPU utilization of a Pod, reflecting the difference between container CPU limits and requests."
        },
        "pod_memory_utilization": {
            "name": "Memory Utilization",
            "desc": "Calculates the memory utilization of the Pod as a ratio of memory limits to requests."
        },
        "pod_io_writes": {
            "name": "I/O Write Rate",
            "desc": "This metric represents the number of I/O write operations performed by a specific Pod over a specified time period. The write count can help analyze the write demands of the application on the storage system."
        },
        "pod_io_read": {
            "name": "I/O Read Rate",
            "desc": "This metric represents the number of I/O read operations performed by a specific Pod over a specified time period. The read count can help analyze the read demands of the application on the storage system."
        },
        "pod_network_in": {
            "name": "Network In",
            "desc": "Monitors the inbound network traffic of a Pod, calculated based on the number of containers and IPs."
        },
        "pod_network_out": {
            "name": "Network Out",
            "desc": "Monitors the outbound network traffic of a Pod, calculated based on the number of containers and IPs."
        }
    },
    "Node": {
        "node_status_condition": {
            "name": "Node Status",
            "desc": "Node Status indicates the current operational state of the node, such as “Running” or “Stopped.” It helps administrators monitor and manage nodes within the Kubernetes cluster."
        },
        "node_cpu_utilization": {
            "name": "CPU Utilization",
            "desc": "CPU Utilization indicates the current usage level of the node's CPU relative to its total available CPU resources. Monitoring this metric helps identify CPU bottlenecks and optimize resource allocation."
        },
        "node_memory_usage": {
            "name": "Application Memory Usage",
            "desc": "Application Memory Usage represents the total amount of memory utilized by applications running on the node. This metric helps understand the memory demands of applications and their impact on system performance."
        },
        "node_memory_utilization": {
            "name": "Application Memory Utilization Rate",
            "desc": "Application Memory Utilization Rate is the ratio of memory used by the application to its configured memory limits. By monitoring this metric, users can determine if adjustments to memory limits are needed."
        },
        "node_physical_memory_usage": {
            "name": "Physical Memory Usage",
            "desc": "Physical Memory Usage refers to the total amount of physical memory actually used by the node. Understanding this metric helps administrators identify if there is a need to expand physical memory to support higher loads."
        },
        "node_physical_memory_utilization": {
            "name": "Physical Memory Utilization Rate",
            "desc": "Physical Memory Utilization Rate represents the percentage of physical memory used compared to the total available physical memory. This metric helps assess the memory pressure and health status of the node."
        },
        "node_io_read": {
            "name": "Disk Write Rate",
            "desc": "Disk Write Rate indicates the rate of write operations performed by the node over a specified period. This metric is crucial for monitoring the disk write performance of applications."
        },
        "node_io_write": {
            "name": "Disk Read Rate",
            "desc": "Disk Read Rate indicates the rate of read operations performed by the node over a specified period. This metric helps assess the data reading performance of applications and storage load."
        },
        "node_network_receive": {
            "name": "Incoming Bytes on NIC",
            "desc": "Network In refers to the volume of data traffic received through the network interface. Monitoring this metric helps analyze if network bandwidth is sufficient and the overall network performance."
        },
        "node_network_transmit": {
            "name": "Outgoing Bytes on NIC",
            "desc": "Network Out refers to the volume of data traffic sent through the network interface. This metric helps understand the node's network egress demands and potential bottlenecks."
        },
        "node_cpu_load1": {
            "name": "1 Minute Average Load",
            "desc": "1 Minute Average Load indicates the average load on the system over the last minute. This metric helps provide a real-time understanding of the system’s load level."
        },
        "node_cpu_load5": {
            "name": "5 Minute Average Load",
            "desc": "5 Minute Average Load indicates the average load on the system over the last 5 minutes. This metric helps identify load trends and their impact on system performance."
        },
        "node_cpu_load15": {
            "name": "15 Minute Average Load",
            "desc": "15 Minute Average Load indicates the average load on the system over the last 15 minutes. Monitoring this metric helps administrators understand the long-term load state of the system."
        }
    },
    "Switch": {
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    },
    "Router": {
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    },
    "Loadbalance": {
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    },
    "Firewall": {
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    },
    "Detection Device": {
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    },
    "Bastion Host": {
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    },
    "Scanning Device": {
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    },
    "Audit System": {
        "sysUpTime": {
            "name": "System Uptime",
            "desc": "This metric indicates the uptime of the device since the last restart, measured in days. By monitoring the uptime, network administrators can understand the stability and reliability of the device and identify potential reboot or failure issues."
        },
        "ifAdminStatus": {
            "name": "Interface Admin Status",
            "desc": "This metric indicates the administrative status of the network switch interface. It serves to indicate whether the interface is enabled (up) or disabled (down) by an administrator, along with other states such as testing or not present. This information is vital for network management and troubleshooting."
        },
        "ifOperStatus": {
            "name": "Interface Oper Status",
            "desc": "This metric reflects the actual operational status of the network switch interface, indicating whether the interface is operational. Unlike the administrative status, the operational status shows whether the interface can successfully receive and send traffic, which is crucial for monitoring network health."
        },
        "ifHighSpeed": {
            "name": "Interface Bandwidth",
            "desc": "This metric indicates the maximum data transmission speed supported by the network interface, usually measured in KB per second. Understanding the maximum speed of the interface helps administrators optimize traffic and utilize network resources effectively."
        },
        "ifInErrors": {
            "name": "Incoming Errors Rate (per second)",
            "desc": "This metric calculates the average rate of incoming error packets over the past 5 minutes, measured in packets per second. Monitoring incoming errors allows administrators to detect potential issues, such as physical connection faults or configuration errors, in a timely manner."
        },
        "ifOutErrors": {
            "name": "Outgoing Errors Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing error packets over the past 5 minutes, measured in packets per second. Monitoring outgoing errors is essential for identifying transmission issues and ensuring data integrity."
        },
        "ifInDiscards": {
            "name": "Incoming Discards Rate (per second)",
            "desc": "This metric represents the average rate of incoming discarded packets over the past 5 minutes, measured in packets per second. Packet discards may indicate network congestion or resource shortages, and monitoring this metric can help administrators optimize network performance."
        },
        "ifOutDiscards": {
            "name": "Outgoing Discards Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing discarded packets over the past 5 minutes, measured in packets per second. Monitoring outgoing discards can help identify network transmission issues and misconfigurations."
        },
        "ifInUcastPkts": {
            "name": "Incoming Unicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming unicast packets over the past 5 minutes, measured in packets per second. Monitoring unicast packets is crucial for assessing interface utilization and traffic load."
        },
        "ifOutUcastPkts": {
            "name": "Outgoing Unicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing unicast packets over the past 5 minutes, measured in packets per second. By monitoring the number of unicast packets, administrators can assess the transmission performance of the interface and the usage of traffic."
        },
        "ifInBroadcastPkts": {
            "name": "Incoming Broadcast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming broadcast packets over the past 5 minutes, measured in packets per second. Monitoring broadcast traffic can help administrators identify potential bottlenecks and efficiency issues in the network."
        },
        "ifOutBroadcastPkts": {
            "name": "Outgoing Broadcast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing broadcast packets over the past 5 minutes, measured in packets per second. Understanding broadcast traffic is important for controlling network traffic and preventing network congestion."
        },
        "ifInMulticastPkts": {
            "name": "Incoming Multicast Packets Rate (per second)",
            "desc": "This metric indicates the average rate of incoming multicast packets over the past 5 minutes, measured in packets per second. Monitoring multicast packets is crucial for performance assessment of specific applications, such as multimedia streaming."
        },
        "ifOutMulticastPkts": {
            "name": "Outgoing Multicast Packets Rate (per second)",
            "desc": "This metric calculates the average rate of outgoing multicast packets over the past 5 minutes, measured in packets per second. Understanding multicast traffic helps administrators optimize bandwidth usage and improve network efficiency."
        },
        "ifInOctets": {
            "name": "Interface Incoming Traffic Rate (per second)",
            "desc": "This metric indicates the average rate of bytes received over the past 5 minutes, converted to megabytes (MB). Monitoring byte traffic helps evaluate the load on the interface and bandwidth usage."
        },
        "ifOutOctets": {
            "name": "Interface Outgoing Traffic Rate (per second)",
            "desc": "This metric calculates the average rate of bytes sent over the past 5 minutes, measured in megabytes (MB). Monitoring outgoing traffic is crucial for ensuring data transmission quality and optimizing network performance."
        },
        "iftotalInOctets": {
            "name": "Device Total Incoming Traffic (per second)",
            "desc": "This metric indicates the average rate of total bytes received by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the incoming byte counts from multiple interfaces, this metric helps administrators obtain an overview of the device's incoming traffic, supporting overall traffic monitoring and capacity planning."
        },
        "iftotalOutOctets": {
            "name": "Device Total Outgoing Traffic (per second)",
            "desc": "This metric represents the average rate of total bytes sent by the entire device over the past 5 minutes, measured in megabytes per second (MB/s). By summing the outgoing byte counts from multiple interfaces, this metric allows administrators to comprehensively assess the sending performance of the entire system, enabling more effective traffic management and optimization."
        }
    }
}

LANGUAGE_DICT = {
    "MONITOR_OBJECT_TYPE": MONITOR_OBJECT_TYPE,
    "MONITOR_OBJECT": MONITOR_OBJECT,
    "MONITOR_OBJECT_PLUGIN": MONITOR_OBJECT_PLUGIN,
    "MONITOR_OBJECT_METRIC_GROUP": MONITOR_OBJECT_METRIC_GROUP,
    "MONITOR_OBJECT_METRIC": MONITOR_OBJECT_METRIC,
}
