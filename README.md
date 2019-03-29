
# csvWatchSensor

This sensor monitors a directory specified in the config.schema.yaml file. The directory you specify will contain a sub directory called 'addXmcDevices'. This sub directory will be automatically created if the containing directory has write permissions. 

## Installation

### location
place the pack in the '/opt/stackstormpacks/' directory and untar as necessary.

### Install the pack

```
$ st2 run packs.setup_virtualenv packs=my_xmc
```

### Configure the pack
This pack is configured via the config.schema.yaml file. 

Three variables exist as shown below in teh config.schema.yaml file. The path for the directory that will be monitored for the insertion of a CSV file, the pollTime interval timer, and the triggerTime delay timer. It is necessary to be able to pace-out the triggers in order to spread the workload for XMC over time to ensure that XMC does not consume too many network resources if large amounts of devices are added.

```
more config.schema.yaml

---

  path:
    description: "The path to monitor for CSV files."
    type: "string"
    default: "/home/st2/addXmcDevices"
    required: False

  pollTime:
    description: "The time interval in seconds between polling."
    type: "integer"
    default: 5
    required: False

  triggerTime:
    description: "The time interval in seconds between each trigger."
    type: "integer"
    default: 1
    required: False
```

### Register the pack
```
st2ctl reload --register-all
```

### Enable or Disable the rule.

```
$ st2 rule enable my_xmc.addDevicesToXMC
$ st2 rule disable my_xmc.addDevicesToXMC
```

## The Rule
```
user@u16-04:~$ st2 rule get  my_xmc.addDeviceToXMC
+-------------+------------------------------------------------------------+
| Property    | Value                                                      |
+-------------+------------------------------------------------------------+
| id          | 5c9a7494685c2c207095bd64                                   |
| uid         | rule:my_xmc:addDeviceToXMC                                 |
| ref         | my_xmc.addDeviceToXMC                                      |
| pack        | my_xmc                                                     |
| name        | addDeviceToXMC                                             |
| description | Add Devices to XMC when a CSV file is detected.            |
| enabled     | True                                                       |
| action      | {                                                          |
|             |     "ref": "my_xmc.addDeviceToXMC",                        |
|             |     "parameters": {                                        |
|             |         "profile": "{{trigger.profile}}",                  |
|             |         "deviceName": "{{trigger.deviceName}}",            |
|             |         "deviceIpAddress": "{{trigger.deviceIpAddress}}",  |
|             |         "xmcIpAddress": "10.174.0.10",                     |
|             |         "site": "{{trigger.site}}"                         |
|             |     }                                                      |
|             | }                                                          |
| criteria    |                                                            |
| tags        |                                                            |
| trigger     | {                                                          |
|             |     "type": "my_xmc.csvWatchSensor",                       |
|             |     "ref": "my_xmc.csvWatchSensor",                        |
|             |     "parameters": {}                                       |
|             | }                                                          |
| type        | {                                                          |
|             |     "ref": "standard",                                     |
|             |     "parameters": {}                                       |
|             | }                                                          |
+-------------+------------------------------------------------------------+
user@u16-04:~$

```

### The Workflow Metadata
```
user@u16-04:~$ st2 action get  my_xmc.addDeviceToXMC
+-------------+--------------------------------------------------------------+
| Property    | Value                                                        |
+-------------+--------------------------------------------------------------+
| id          | 5c978c3c685c2c5747e7205c                                     |
| uid         | action:my_xmc:addDeviceToXMC                                 |
| ref         | my_xmc.addDeviceToXMC                                        |
| pack        | my_xmc                                                       |
| name        | addDeviceToXMC                                               |
| description | Add a device to XMC via the GraphQL North Bound Interface.   |
| enabled     | True                                                         |
| entry_point | workflows/addDeviceToXMC.yaml                                |
| runner_type | mistral-v2                                                   |
| parameters  | {                                                            |
|             |     "skip_notify": {                                         |
|             |         "default": [],                                       |
|             |         "type": "array",                                     |
|             |         "description": "List of tasks to skip notifications  |
|             | for."                                                        |
|             |     },                                                       |
|             |     "profile": {                                             |
|             |         "position": 3,                                       |
|             |         "required": true,                                    |
|             |         "type": "string",                                    |
|             |         "description": "The XMC device login credential      |
|             | profile that will be used to access the device. "            |
|             |     },                                                       |
|             |     "task": {                                                |
|             |         "type": "string",                                    |
|             |         "description": "The name of the task to run for      |
|             | reverse workflow."                                           |
|             |     },                                                       |
|             |     "workflow": {                                            |
|             |         "type": "string",                                    |
|             |         "description": "The name of the workflow to run if   |
|             | the entry_point is a workbook of many workflows. The name    |
|             | should be in the format                                      |
|             | "<pack_name>.<action_name>.<workflow_name>". If entry point  |
|             | is a workflow or a workbook with a single workflow, the      |
|             | runner will identify the workflow automatically."            |
|             |     },                                                       |
|             |     "xmcPassword": {                                         |
|             |         "default": "$password$",                             |
|             |         "position": 7,                                       |
|             |         "type": "string",                                    |
|             |         "description": "The XMC password login credential."  |
|             |     },                                                       |
|             |     "site": {                                                |
|             |         "default": "/World",                                 |
|             |         "position": 4,                                       |
|             |         "type": "string",                                    |
|             |         "description": "The XMC site that the device will be |
|             | reside."                                                     |
|             |     },                                                       |
|             |     "context": {                                             |
|             |         "default": {},                                       |
|             |         "type": "object",                                    |
|             |         "description": "Additional workflow inputs."         |
|             |     },                                                       |
|             |     "xmcUsername": {                                         |
|             |         "default": "root",                                   |
|             |         "position": 6,                                       |
|             |         "type": "string",                                    |
|             |         "description": "The XMC username login credential."  |
|             |     },                                                       |
|             |     "deviceName": {                                          |
|             |         "position": 1,                                       |
|             |         "required": true,                                    |
|             |         "type": "string",                                    |
|             |         "description": "The name that XMC will use for the   |
|             | device."                                                     |
|             |     },                                                       |
|             |     "deviceIpAddress": {                                     |
|             |         "position": 2,                                       |
|             |         "required": true,                                    |
|             |         "type": "string",                                    |
|             |         "description": "The IPv4 address of the device to be |
|             | added to XMC."                                               |
|             |     },                                                       |
|             |     "xmcIpAddress": {                                        |
|             |         "default": "10.174.0.10",                            |
|             |         "position": 5,                                       |
|             |         "required": false,                                   |
|             |         "type": "string",                                    |
|             |         "description": "The IPv4 address of the XMC console. |
|             | "                                                            |
|             |     }                                                        |
|             | }                                                            |
| notify      |                                                              |
| tags        |                                                              |
+-------------+--------------------------------------------------------------+
user@u16-04:~$

```
### The Workflow
```
/opt/stackstorm/packs/my_xmc# more actions/workflows/addDeviceToXMC.yaml
---
version: '2.0'

my_xmc.addDeviceToXMC:
  input:
    - profile
    - xmcPassword
    - site
    - xmcUsername
    - deviceName
    - deviceIpAddress
    - xmcIpAddress
  tasks:
    addXmcDevice:
      # [105, 26]
      action: core.http
      input:
        username: "<% $.xmcUsername %>"
        password: "<% $.xmcPassword %>"
        body: "{ \"query\": \"mutation{network{createDevices(input:{devices:[{ni
ckName:\\\"<%$.deviceName%>\\\",ipAddress:\\\"<%$.deviceIpAddress%>\\\",profileN
ame:\\\"<%$.profile%>\\\",siteLocation:\\\"<%$.site%>\\\"}]}){message,status}}}\
"}"
        url: "https://<% $.xmcIpAddress %>:8443/nbi/graphql/"
        headers: {"Content-Type": "application/json"}
        allow_redirects: true
        method: "POST"
        verify_ssl_cert: false

root@u16-04:/opt/stackstorm/packs/my_xmc#

```


### Enable or Disable the Sensor.
```
$ st2 sensor disable my_xmc.csvWatchSensor
$ st2 sensor enable my_xmc.csvWatchSensor

```

## Operation
Place file in the /your/path/addXmcDevices  directory.

The sensor will detect the file's presence upon the next poll, process it (injects triggers to EWC) and change its extension from '.csv' to to ‘.csvprocessed’ to prevent it from being processed a second time.

```
### File Format
In order for the workflow to function properly the File format must conform to the following. 

user@u16-04:/home/st2/addXmcDevices$ more devices.csv
#IP, DeviceName, DeviceProfile,  Site
10.174.0.1, kvmHypervisor, legacyBrocade,  /World
10.174.0.60,  SLX9540-Leaf-1, legacyBrocade,  /World
10.174.0.61,  SLX9140-Leaf-2, legacyBrocade,  /World
10.174.0.62,  SLX9240-Spine-1, legacyBrocade,  /World
10.174.0.63,  SLX9240-Leaf-1, legacyBrocade,  /World
10.174.0.64,  X440-G2, legacyBrocade,  /World
10.174.0.254,  VDX-6720,  public_v1_Profile,  /World
```

T
