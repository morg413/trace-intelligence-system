"""
Call Graph Builder - Map function relationships and call hierarchies
"""

from typing import List, Dict, Set
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class FunctionNode:
    """Represents a function in the call graph"""
    name: str
    file_path: str
    line_number: int
    traces: List[str] = field(default_factory=list)


@dataclass
class CallEdge:
    """Represents a function call relationship"""
    caller: str
    callee: str
    call_site_line: int


class CallGraphBuilder:
    """
    Build and analyze call graphs for C/C++ functions.
    
    Features:
    - Track function definitions and relationships
    - Find call paths to target functions
    - Associate traces with functions
    - Query caller/callee relationships
    """
    
    def __init__(self):
        self.nodes: Dict[str, FunctionNode] = {}
        self.edges: List[CallEdge] = []
        self.traces_in_function: Dict[str, List[str]] = {}
    
    def add_function(self, name: str, file_path: str, line_number: int) -> None:
        """Register a function node"""
        if name not in self.nodes:
            self.nodes[name] = FunctionNode(name, file_path, line_number)
    
    def add_call_edge(self, caller: str, callee: str, line_num: int) -> None:
        """Register a function call relationship"""
        self.edges.append(CallEdge(caller, callee, line_num))
    
    def add_trace_to_function(self, function: str, trace_id: str) -> None:
        """Associate a trace with a function"""
        if function not in self.traces_in_function:
            self.traces_in_function[function] = []
        self.traces_in_function[function].append(trace_id)
    
    def find_callers(self, func_name: str) -> List[str]:
        """Find all functions that call func_name"""
        return list(set([e.caller for e in self.edges if e.callee == func_name]))
    
    def find_callees(self, func_name: str) -> List[str]:
        """Find all functions called by func_name"""
        return list(set([e.callee for e in self.edges if e.caller == func_name]))
    
    def find_call_paths(self, target: str, max_depth: int = 10) -> List[List[str]]:
        """Find all call paths from entry points to target function"""
        paths = []
        
        def dfs(current, path, visited, depth):
            if depth > max_depth or current in visited:
                return
            
            new_visited = visited.copy()
            new_visited.add(current)
            new_path = path + [current]
            
            if current == target:
                paths.append(new_path)
            else:
                for callee in self.find_callees(current):
                    dfs(callee, new_path, new_visited, depth + 1)
        
        entry_points = ['main', 'wmain', '__main__']
        for entry in entry_points:
            if entry in self.nodes:
                dfs(entry, [], set(), 0)
        
        return paths
    
    def get_traces_in_path(self, path: List[str]) -> List[str]:
        """Get all traces along a call path"""
        traces = []
        for func in path:
            traces.extend(self.traces_in_function.get(func, []))
        return traces
    
    def get_call_graph_info(self) -> Dict:
        """Get summary information about the call graph"""
        return {
            'total_functions': len(self.nodes),
            'total_edges': len(self.edges),
            'total_traces': sum(len(t) for t in self.traces_in_function.values()),
            'entry_points': [n for n in self.nodes if n in ['main', 'wmain', '__main__']]
        }
