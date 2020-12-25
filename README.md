# Miner metrics exporter for prometheus
prometheus rule examples:<br>

### Claymore/PhoenixMiner
```  - job_name: 'fermname'
    metrics_path: '/claymore/192.168.75.91/3333'
    static_configs:
      - targets: ['localhost:5000'] 
```

fermname - replace with your ferm name<br>
192.168.75.91 - replace with miner ip address <br>
3333 - replace with miner data port<br>


### GMiner
```  - job_name: 'mini'
    metrics_path: '/gminer/192.168.75.92/10555'
    static_configs:
      - targets: ['localhost:5000'] 
```

fermname - replace with your ferm name<br>
192.168.75.92 - replace with miner ip address <br>
10555 - replace with miner data port<br>


### nanominer
```  - job_name: 'mini'
    metrics_path: '/nanominer/192.168.75.92/3333'
    static_configs:
      - targets: ['localhost:5000']
```

fermname - replace with your ferm name<br>
192.168.75.92 - replace with miner ip address <br>
3333 - replace with miner data port<br>



### teamredminer
```  - job_name: 'mini'
    metrics_path: '/teamredminer/192.168.75.92/4028'
    static_configs:
      - targets: ['localhost:5000']
```

fermname - replace with your ferm name<br>
192.168.75.92 - replace with miner ip address <br>
4028 - replace with miner data port<br>
