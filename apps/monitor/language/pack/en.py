MONITOR_OBJECT_TYPE = {
    "OS": "OS",
    "Web": "Web",
    "K8S": "K8S",
    "Network Device": "Network Device",
    "Hardware Device": "Hardware Device",
    "Other": "Other",
}

MONITOR_OBJECT = {
    "Host": "Host",
    "Website": "Website",
    "Ping": "Ping",
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
    "Storage": "Storage",
    "Hardware Server": "Hardware Server",
    "SNMP Trap": "SNMP Trap"
}

MONITOR_OBJECT_PLUGIN = {
    "Host": {
        "name": "Host",
        "desc": "The host monitoring plugin is used to collect and analyze the performance data of the host, including CPU, memory, disk, and network usage."
    },
    "Website": {
        "name": "Website Monitoring",
        "desc": "The website monitoring plugin is used to periodically check the availability and performance of HTTP/HTTPS connections."
    },
    "Ping": {
        "name": "Ping",
        "desc": "Ping is used to check the connectivity and response time of a target host or network device by sending ICMP Echo requests."
    },
    "K8S": {
        "name": "K8S",
        "desc": "The K8S monitoring plugin is used to monitor the status and health of Kubernetes clusters, including performance metrics of nodes, containers, and pods."
    },
    "Switch SNMP General": {
        "name": "Switch General (SNMP)",
        "desc": "The SNMP General plugin is used to monitor and manage the status of switches via SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, to optimize network performance and improve management efficiency."
    },
    "Router SNMP General": {
        "name": "Router General (SNMP)",
        "desc": "The SNMP General plugin is used to monitor and manage the status of routers via SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, to optimize network performance and improve management efficiency."
    },
    "Loadbalance SNMP General": {
        "name": "Load Balancer General (SNMP)",
        "desc": "The SNMP General plugin is used to monitor and manage the status of load balancers via SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, to optimize network performance and improve management efficiency."
    },
    "Firewall SNMP General": {
        "name": "Firewall General (SNMP)",
        "desc": "The SNMP General plugin is used to monitor and manage the status of firewalls via SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, to optimize network performance and improve management efficiency."
    },
    "Detection Device SNMP General": {
        "name": "Detection Device General (SNMP)",
        "desc": "The SNMP General plugin is used to monitor and manage the status of detection devices via SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, to optimize network performance and improve management efficiency."
    },
    "Bastion Host SNMP General": {
        "name": "Bastion Host General (SNMP)",
        "desc": "The SNMP General plugin is used to monitor and manage the status of bastion hosts via SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, to optimize network performance and improve management efficiency."
    },
    "Scanning Device SNMP General": {
        "name": "Scanning Device General (SNMP)",
        "desc": "The SNMP General plugin is used to monitor and manage the status of scanning devices via SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, to optimize network performance and improve management efficiency."
    },
    "Storage SNMP General": {
        "name": "Storage Device General (SNMP)",
        "desc": "The SNMP General plugin is used to monitor and manage the status of storage devices via SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, to optimize network performance and improve management efficiency."
    },
    "Storage IPMI": {
        "name": "Storage Device General (IPMI)",
        "desc": "The IPMI monitoring plugin communicates with hardware to provide real-time monitoring of system health status, hardware sensor data, and power management."
    },
    "Hardware Server SNMP General": {
        "name": "Hardware Server General (SNMP)",
        "desc": "The SNMP General plugin is used to monitor and manage the status of hardware servers via SNMP. Administrators can obtain key information about the device, such as interface traffic, error statistics, and status information, to optimize network performance and improve management efficiency."
    },
    "Hardware Server IPMI": {
        "name": "Hardware Server General (IPMI)",
        "desc": "The IPMI monitoring plugin communicates with hardware to provide real-time monitoring of system health status, hardware sensor data, and power management."
    },
    "SNMP Trap": {
        "name": "SNMP Trap",
        "desc": "The SNMP Trap monitoring plugin is used to receive and process alarms or status notifications (Trap messages) actively pushed by network devices, enabling real-time monitoring and fault alerts."
    }
}

MONITOR_OBJECT_METRIC_GROUP = {
    "Host": {
        "CPU": "CPU",
        "System": "System", 
        "Disk IO": "Disk IO", 
        "DISK": "Disk",
        "Process": "Process",
        "MEMORY": "Memory",
        "Net": "Net",
    },
    "Website": {
        "HTTP": "HTTP",
    },
    "Ping": {
        "Ping": "Ping",
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
        "Net": "Net",
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
    "Storage": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
         "Power": "Power", 
        "Environment": "Environment",       
    },
    "Hardware Server": {
        "Base": "Base",
        "Status": "Status",
        "Bandwidth": "Bandwidth",
        "Packet Error": "Packet Error",
        "Packet Loss": "Packet Loss",
        "Packet": "Packet",
        "Traffic": "Traffic",
        "Power": "Power", 
        "Environment": "Environment",            
    },
    "SNMP Trap": {        
    }
}

MONITOR_OBJECT_METRIC = {
    "Host":{
    "cpu_summary.usage": {
        "name": "CPU Usage Rate",
        "desc": "Displays the CPU usage rate to indicate the system's load. It is derived by subtracting the idle from total. This metric is crucial for monitoring system performance."
    },
    "cpu_summary.idle": {
        "name": "CPU Idle Rate",
        "desc": "Displays the CPU idle rate, representing the amount of unused CPU resources in the system. It helps to know if the system is under high load. This metric is crucial for analyzing system performance and efficiency."
    },
    "cpu_summary.iowait": {
        "name": "Percentage of Time Waiting for IO",
        "desc": "Displays the percentage of CPU time spent waiting for IO operations, indicating the impact of disk or network performance on the system. Reducing wait time helps improve system performance. This metric is very useful for analyzing system bottlenecks."
    },
    "cpu_summary.system": {
        "name": "System Usage Rate",
        "desc": "Displays the system usage rate, showing the CPU resources consumed by kernel processes. Analyzing this value helps optimize system kernel performance and stability."
    },
    "cpu_summary.user": {
        "name": "User Usage Rate",
        "desc": "Displays the percentage of CPU resources used by user processes, helping understand the performance of applications and services. This metric is helpful in understanding the CPU consumption of specific applications."
    },
    "load1": {
        "name": "1 Minute Average Load",
        "desc": "Displays the average system load over the last 1 minute, providing a snapshot of short-term system activity. This metric helps monitor system performance in real-time."
    },
    "load5": {
        "name": "5 Minute Average Load",
        "desc": "Displays the average system load over the last 5 minutes, reflecting the medium-term load on the system. This medium-term metric helps identify sustained and intermittent high load situations."
    },
    "load15": {
        "name": "15 Minute Average Load",
        "desc": "Displays the average system load over the last 15 minutes, providing long-term load observation to understand the overall performance trend of the system."
    },
    "diskio_writes": {
        "name": "Disk I/O Write Rate",
        "desc": "Counts the number of data write operations to the disk in the specified time interval."
    },
    "diskio_write_bytes": {
        "name": "Disk I/O Write Bytes Rate",
        "desc": "Counts the number of bytes written to the disk in the specified time interval, represented in megabytes (MB)."
    },
    "diskio_write_time": {
        "name": "Disk I/O Write Time Rate",
        "desc": "Counts the time taken to write data to the disk in the specified time interval, represented in seconds (s)."
    },
    "diskio_reads": {
        "name": "Disk I/O Read Rate",
        "desc": "Counts the number of data read operations from the disk in the specified time interval."
    },
    "diskio_read_bytes": {
        "name": "Disk I/O Read Bytes Rate",
        "desc": "Counts the number of bytes read from the disk in the specified time interval, represented in megabytes (MB)."
    },
    "diskio_read_time": {
        "name": "Disk I/O Read Time Rate",
        "desc": "Counts the time taken to read data from the disk in the specified time interval, represented in seconds (s)."
    },
    "disk.is_use": {
        "name": "Disk Usage Rate",
        "desc": "Displays the percentage of disk space used, helping understand the utilization of disk resources. This metric is important for preventing disk overflow."
    },
    "disk.used": {
        "name": "Disk Used Size",
        "desc": "Displays the actual used disk space (in GB), used to determine disk capacity usage. This metric is helpful for monitoring disk space usage."
    },
    "env.procs": {
        "name": "Total Number of Processes",
        "desc": "Displays the total number of processes running on the system, helping understand the load distribution. This metric is important for monitoring the overall operation of the system."
    },
    "env.proc_running_current": {
        "name": "Number of Running Processes",
        "desc": "Displays the number of processes currently running, used to assess the concurrency. This metric is valuable for real-time monitoring of system load."
    },
    "env.procs_blocked_current": {
        "name": "Number of IO Blocked Processes",
        "desc": "Displays the number of processes currently blocked by IO operations. Analyzing this value helps optimize the system and reduce bottlenecks. This metric is helpful for identifying IO bottlenecks."
    },
    "mem.total": {
        "name": "Total Physical Memory Size",
        "desc": "Displays the total physical memory of the system (in GB), providing an overview of system resource configuration. This metric is important for understanding the base configuration of system resources."
    },
    "mem.free": {
        "name": "Free Physical Memory Amount",
        "desc": "Displays the amount of free physical memory currently available (in GB), helping understand the available resources. This metric is crucial for keeping track of memory resource usage."
    },
    "mem.cached": {
        "name": "Cache Memory Size",
        "desc": "Displays the amount of memory used for caching (in GB), used to improve system performance. This metric is important for understanding memory caching strategies."
    },
    "mem.buffer": {
        "name": "Buffer Memory Size",
        "desc": "Displays the amount of memory used for buffering (in GB), ensuring stable data transfer. This metric is crucial for performance optimization strategies."
    },
    "mem.usable": {
        "name": "Available Memory for Applications",
        "desc": "Displays the memory available for applications (in GB), ensuring smooth application operation. This metric is important for maintaining application performance and stability."
    },
    "mem.pct_usable": {
        "name": "Available Memory Percentage for Applications",
        "desc": "Displays the percentage of memory available, helping determine if there is sufficient memory to support applications. This metric is useful for monitoring memory pressure and capacity planning strategies."
    },
    "mem.used": {
        "name": "Memory Used by Applications",
        "desc": "Displays the memory used by applications (in GB), analyzing this value helps optimize application memory usage. This metric is crucial for monitoring application resource consumption."
    },
    "mem.pct_used": {
        "name": "Application Memory Usage Percentage",
        "desc": "Displays the percentage of memory used by applications, understanding memory usage distribution. This metric is valuable for optimizing memory usage."
    },
    "mem.psc_used": {
        "name": "Used Physical Memory Amount",
        "desc": "Displays the total amount of physical memory used by the system (in GB), helping understand the overall distribution of memory resources. This metric is crucial for gaining a comprehensive understanding of system memory usage."
    },
    "mem.shared": {
        "name": "Shared Memory Usage",
        "desc": "Displays the usage of shared memory (in GB), used for data sharing between processes. This metric helps optimize system memory allocation strategies."
    },
    "net.speed_packets_recv": {
        "name": "Incoming Packets on NIC",
        "desc": "Displays the number of data packets received by the network interface per unit of time, used to evaluate network reception performance. This metric is crucial for monitoring network traffic."
    },
    "net.speed_packets_sent": {
        "name": "Outgoing Packets on NIC",
        "desc": "Displays the number of data packets sent by the network interface per unit of time, used to evaluate network transmission performance. This metric is crucial for monitoring network traffic."
    },
    "net.speed_recv": {
        "name": "Incoming Bytes on NIC",
        "desc": "Displays the number of bytes received by the network interface per unit of time (in MB), used to evaluate network bandwidth utilization. This metric is important for monitoring network bandwidth."
    },
    "net.speed_sent": {
        "name": "Outgoing Bytes on NIC",
        "desc": "Displays the number of bytes sent by the network interface per unit of time (in MB), used to evaluate network bandwidth utilization. This metric is crucial for monitoring network bandwidth."
    },
    "net.errors_in": {
        "name": "NIC Error Packets",
        "desc": "Displays the number of error packets received by the network interface, used to detect network issues. This metric is helpful for identifying network faults and abnormal traffic."
    },
    "net.errors_out": {
        "name": "NIC Error Packets",
        "desc": "Displays the number of error packets sent by the network interface, helping understand network transmission errors. This metric is helpful for identifying network faults and abnormal traffic."
    },
    "net.dropped_in": {
        "name": "NIC Dropped Packets",
        "desc": "Displays the number of dropped packets received by the network interface, indicating network congestion. This metric is crucial for monitoring network reliability."
    },
    "net.dropped_out": {
        "name": "NIC Dropped Packets",
        "desc": "Displays the number of dropped packets sent by the network interface, indicating network transmission congestion. This metric is crucial for monitoring network reliability."
    }
},
    "Website": {
    "http_success.rate": {
        "name": "Success Rate",
        "desc": "Measures the success rate of multiple nodes probing targets (the percentage of successful responses out of the total number of requests)."
    },
    "http_duration": {
        "name": "Response Time",
        "desc": "This metric represents the total time taken from initiating an HTTP request to receiving the HTTP response. It is used to assess the performance of web services, especially when handling user requests. An extended duration may indicate lower backend processing efficiency or network latency, which can adversely affect the user experience. It is crucial for enhancing system responsiveness and optimizing performance."
    },
    "http_code": {
        "name": "HTTP Code",
        "desc": "This metric represents the HTTP response status code for an HTTP request. It captures the value of the HTTP response status codes, such as 200 (OK), 404 (Not Found), 500 (Internal Server Error), etc. These status codes are vital for monitoring the health and performance of web applications, assisting in identifying potential issues."
    },
    "http_content.length": {
        "name": "HTTP Content Length",
        "desc": "This metric indicates the length of the HTTP response content in bytes. Larger content lengths can result in extended data transfer times and consume more bandwidth. Monitoring this metric is crucial for optimizing website performance or analyzing bandwidth usage. Understanding the size of the response content can assist developers in making optimizations."
    }
},
    "Ping":{
    "ping_ttl": {
        "name": "Average TTL",
        "desc": "Represents the average 'hop count' (or time) allowed for ping packets from the source device to the target. This metric helps identify if packets take an abnormal number of hops or if there are route anomalies. Higher TTL values indicate longer paths."
    },
    "ping_response_time": {
        "name": "Average Response Time",
        "desc": "Represents the average ping response time of the target device over a period. This metric helps evaluate latency between the source and target device. Lower average response time indicates good network performance."
    },
    "ping_packet_transmission_rate": {
        "name": "Packet Transmission Rate",
        "desc": "Represents the percentage of successfully received packets out of the total packets transmitted. This metric measures network quality and transmission reliability. Low packet loss indicates stable and reliable connectivity."
    },
    "ping_packet_loss_rate": {
        "name": "Packet Loss Rate",
        "desc": "Represents the percentage of packets lost during ping requests. This metric helps identify unstable network connections or transmission problems. Lower loss rates indicate more stable connectivity."
    },
    "ping_error_response_code": {
        "name": "Ping State",
        "desc": "Represents the resulting code after a ping operation. A code of 0 indicates success, while non-zero values indicate potential issues with the network or host. This metric helps quickly detect network connectivity errors."
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
    "desc": "Node Status indicates the current operational state of the node, such as 'Running' or 'Stopped.' It helps administrators monitor and manage nodes within the Kubernetes cluster."
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
    "Storage": {
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
  },"ipmi_chassis_power_state": {
        "name": "Power State",
        "desc": "The power state indicator is used to monitor if the device is powered on. Its value can indicate whether the power is on or off. It is mainly used for remote management and monitoring of the device's power state."
    },
    "ipmi_power_watts": {
        "name": "Power",
        "desc": "The power indicator is measured in watts and reflects the current power consumption of the device. This indicator helps evaluate the device's energy efficiency and power consumption trends. It facilitates the implementation of energy-saving policies and resource optimization."
    },
    "ipmi_voltage_volts": {
        "name": "Voltage",
        "desc": "The voltage indicator measured in volts monitors the voltage levels of different power rails within the device. Stable voltage supply is crucial for the reliability of the device. This indicator helps quickly identify electrical issues, ensuring normal operation."
    },
    "ipmi_fan_speed_rpm": {
        "name": "Fan Speed",
        "desc": "The fan speed indicator is measured in rotations per minute (rpm) and monitors the fan's operation status within the device. Efficient fan operation is key to maintaining device temperature. It helps prevent overheating and ensures the device's stable long-term operation."
    },
    "ipmi_temperature_celsius": {
        "name": "Temperature",
        "desc": "The temperature indicator measured in degrees Celsius monitors the internal temperature of the device. Monitoring temperature prevents heat accumulation and avoids device overheating. It is crucial for maintaining system stability and longevity."
    }
    },
    "Hardware Server": {
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
  },"ipmi_chassis_power_state": {
        "name": "Power State",
        "desc": "The power state indicator is used to monitor if the device is powered on. Its value can indicate whether the power is on or off. It is mainly used for remote management and monitoring of the device's power state."
    },
    "ipmi_power_watts": {
        "name": "Power",
        "desc": "The power indicator is measured in watts and reflects the current power consumption of the device. This indicator helps evaluate the device's energy efficiency and power consumption trends. It facilitates the implementation of energy-saving policies and resource optimization."
    },
    "ipmi_voltage_volts": {
        "name": "Voltage",
        "desc": "The voltage indicator measured in volts monitors the voltage levels of different power rails within the device. Stable voltage supply is crucial for the reliability of the device. This indicator helps quickly identify electrical issues, ensuring normal operation."
    },
    "ipmi_fan_speed_rpm": {
        "name": "Fan Speed",
        "desc": "The fan speed indicator is measured in rotations per minute (rpm) and monitors the fan's operation status within the device. Efficient fan operation is key to maintaining device temperature. It helps prevent overheating and ensures the device's stable long-term operation."
    },
    "ipmi_temperature_celsius": {
        "name": "Temperature",
        "desc": "The temperature indicator measured in degrees Celsius monitors the internal temperature of the device. Monitoring temperature prevents heat accumulation and avoids device overheating. It is crucial for maintaining system stability and longevity."
    }
},
    "SNMP Trap": {        
    }
}

LANGUAGE_DICT = {
    "MONITOR_OBJECT_TYPE": MONITOR_OBJECT_TYPE,
    "MONITOR_OBJECT": MONITOR_OBJECT,
    "MONITOR_OBJECT_PLUGIN": MONITOR_OBJECT_PLUGIN,
    "MONITOR_OBJECT_METRIC_GROUP": MONITOR_OBJECT_METRIC_GROUP,
    "MONITOR_OBJECT_METRIC": MONITOR_OBJECT_METRIC,
}
