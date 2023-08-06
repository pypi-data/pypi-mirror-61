# lvmcache2mqtt

Python module to publish LVM cache (dmcache) statistics to MQTT. Data can then, for instance, be used for visualization in grafana or like.

## Configuration

Configuration example:

```yaml
mqtt:
    host: mqtt_broker_hostname

devices:
    - device: /dev/mapper/cached-device
      device_alias: some_alias
      target_topic: mqtt/topic/to/publish/to
```

## Usage

Install python module with ``pip install lvmcache2mqtt``.

Run with ``python -m lvmcache2mqtt``
