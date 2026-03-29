"""
Command-line interface for Trace Intelligence System
"""

import argparse
import logging
from pathlib import Path
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Trace Intelligence System - C/C++ debugging tool'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    scan_parser = subparsers.add_parser('scan', help='Scan repository for traces')
    scan_parser.add_argument('repo_path', help='Path to C/C++ repository')
    scan_parser.add_argument('--output', '-o', default='traces.json',
                            help='Output JSON file')
    
    analyze_parser = subparsers.add_parser('analyze', help='Analyze runtime logs')
    analyze_parser.add_argument('log_file', help='Path to log file')
    analyze_parser.add_argument('--traces', '-t', required=True,
                               help='Trace database JSON file')
    analyze_parser.add_argument('--output', '-o', default='analysis.json',
                               help='Output JSON file')
    
    graph_parser = subparsers.add_parser('graph', help='Analyze call graph')
    graph_parser.add_argument('--target', '-t', help='Target function name')
    graph_parser.add_argument('--traces', required=True,
                             help='Trace database JSON file')
    
    args = parser.parse_args()
    
    if args.command == 'scan':
        handle_scan(args)
    elif args.command == 'analyze':
        handle_analyze(args)
    elif args.command == 'graph':
        handle_graph(args)
    else:
        parser.print_help()


def handle_scan(args):
    """Handle scan command"""
    from src.scanner.trace_scanner import TraceScanner
    
    try:
        scanner = TraceScanner()
        scanner.discover_printf_traces()
        scanner.discover_macro_traces()
        scanner.discover_syslog_traces()
        
        result = scanner.export_results()
        logger.info(f"Scan complete!")
        logger.info(f"Output: {result}")
        
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        sys.exit(1)


def handle_analyze(args):
    """Handle analyze command"""
    logger.info(f"Analyzing logs: {args.log_file}")
    logger.info(f"Using traces: {args.traces}")


def handle_graph(args):
    """Handle graph command"""
    logger.info(f"Call graph analysis for: {args.target}")


if __name__ == '__main__':
    main()
