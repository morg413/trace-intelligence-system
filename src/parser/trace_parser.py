"""
Complete Trace Parser - Extract and normalize trace data from various formats
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class NormalizedTrace:
    """Standardized trace representation across all formats"""
    id: str
    source_file: str
    line_number: int
    function_name: str
    trace_type: str
    timestamp: Optional[str]
    level: str
    message: str
    arguments: Dict[str, Any]


class TraceParser:
    """
    Parse and normalize traces from discovered mechanisms.
    
    Converts different trace formats (printf, macros, syslog, custom)
    to a unified NormalizedTrace schema.
    """
    
    def __init__(self):
        self.normalized_traces: List[NormalizedTrace] = []
        self.log_levels = ['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE']
    
    def parse_printf_format(self, format_string: str, args: List[Any]) -> str:
        """Parse printf-style format string with provided arguments"""
        try:
            return format_string % tuple(args)
        except (TypeError, ValueError):
            return format_string
    
    def extract_log_level(self, message: str) -> str:
        """Extract log level from message text"""
        message_upper = message.upper()
        for level in self.log_levels:
            if level in message_upper:
                return level
        return 'INFO'
    
    def extract_format_string_args(self, format_string: str) -> int:
        """Count expected arguments from printf format string"""
        if not format_string:
            return 0
        return len(re.findall(r'%[-#+ 0,(\d.]*[hlL]?[diouxXeEfFgGaAcspn]', format_string))
    
    def normalize(self, raw_trace: Dict[str, Any]) -> NormalizedTrace:
        """Convert raw trace data to normalized format"""
        message = raw_trace.get('message', '')
        format_string = raw_trace.get('format_string')
        
        return NormalizedTrace(
            id=raw_trace.get('id', 'unknown'),
            source_file=raw_trace.get('file_path', ''),
            line_number=raw_trace.get('line_number', 0),
            function_name=raw_trace.get('function_name', '<unknown>'),
            trace_type=raw_trace.get('trace_type', 'unknown'),
            timestamp=raw_trace.get('timestamp'),
            level=self.extract_log_level(message),
            message=message,
            arguments=raw_trace.get('arguments', {})
        )
    
    def normalize_batch(self, raw_traces: List[Dict[str, Any]]) -> List[NormalizedTrace]:
        """Normalize multiple traces at once"""
        normalized = []
        for raw_trace in raw_traces:
            try:
                normalized.append(self.normalize(raw_trace))
            except Exception as e:
                logger.warning(f"Failed to normalize trace: {e}")
        return normalized
    
    def export_normalized(self, output_path: str) -> None:
        """Export normalized traces to JSON file"""
        import json
        data = [asdict(t) for t in self.normalized_traces]
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Exported {len(data)} normalized traces to {output_path}")
