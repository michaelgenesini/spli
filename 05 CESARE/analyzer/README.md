# 2: ANALYZER

##### How to configure

Edit **general.conf.txt**

##### Howt to Analyze WebSocket

Add the following lines to **general.conf.txt**
```shell
websocket
	run print
end_websocket
```

##### Howt to Analyze SSH

Add the following lines to **general.conf.txt**
```shell
ssh
	run print
end_ssh
```

##### Howt to run

```shell
$ ./run.sh
```