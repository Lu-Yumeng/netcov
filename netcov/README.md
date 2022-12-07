# NetCov Model Define Coverage Logic
## Init snapshot
- ```bf.init_snapshot(path, Name, overwrite = True)```
- ```self.cov = Coverage(upload, static_analysis=False, prebulit=False)```
- ```self._init_control_plane_datamodel()```
- ``` build_control_plane_datamodel(self.model)```

    After the previous three functions, the snapshot is initialized, with fixed ```network.typed_source```, ```denom```, and ```network.reachable_source = network.supported_source```.

    ```network.typed_source```, ```network.reachable_source``` and ```network.supported_sources```attributes are not fixed. 



## Batfish Query - define which nodes have been tested 
- Based on the query, it will call ```self.trace.update(convert_traceroute_traces([answer.frame()]))``` to process the traceroute answer
- Inside ```convert_traceroute_traces```, first define each traced path, and together with destination_ip, use the ```convert_traceroute_path(path, dst_ip)``` to further process tested node on every route 
- In ```convert_traceroute_path```, add all nodes with hop status ```FORWARDED```, ```ACCEPTED```, ```DELIVERED_TO_SUBNET``` and ```EXITS_NETWORK``` to ```tested_nodes```



## Display Results 
- In the [example.py](../examples/example.py) to call for displaying results: ```bf.cov.result()```
- To get the all traced nodes answered by the batfish query: ```tested_nodes = list(self.trace)```
- Used the network snapshot and traced nodes to calculated control plan coverage: ```covered_lines = control_plane_coverage(self.model, tested_nodes)``` 
- To convert every tested lines of each devices for configuration lines counting ```covered_lines = line_level_stats(covered_nodes)```, here ```covered_nodes``` is calculates using dfs on ```tested_nodes```
    - Problem: From the code below, it seems like all realted nodes's all configuration lines has been added to w/o selection 
    - 
        ```
        def line_level_stats(covered_nodes: Iterable[DNode]) -> SourceLines:
        covered_sources = SourceLines()
        for node in covered_nodes:
            if isinstance(node, ConfigNode):
                if node.lines:
                    covered_sources.add_source_lines(node.lines)
        return covered_sources
        ```
 
- Display the results in table format: ```log_metrics(covered_lines, network, "Configuration coverage")```
    - Main Idea: to intersect the tested lines with reachable nodes's configuration lines
   - ```cnt_covered``` denotes the number of a particular type of configuration lines has been covered.
    - ```config_type``` includes bgp neighbour, interface, route-map etc.
    - ```type_sources``` is fixed when init in snapshot
    - ```typed_covered_sources = covered_sources.intersect(type_sources)``` intersect covered source with typed_sources
    - ```cnt_covered = typed_covered_sources.count()``` calculate the # of lines has been covered

