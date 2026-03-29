import json


class TraceInfo:
    def __init__(self, trace_type, details):
        self.trace_type = trace_type
        self.details = details


class ScanResult:
    def __init__(self):
        self.traces = []

    def add_trace(self, trace_info):
        self.traces.append(trace_info)

    def export_to_json(self):
        return json.dumps([trace.__dict__ for trace in self.traces], indent=4)


class TraceScanner:
    def __init__(self):
        self.scan_result = ScanResult()

    def discover_printf_traces(self):
        # Logic to discover printf traces
        printf_trace = TraceInfo('printf', 'Example printf trace detail')
        self.scan_result.add_trace(printf_trace)

    def discover_macro_traces(self):
        # Logic to discover macro traces
        macro_trace = TraceInfo('macro', 'Example macro trace detail')
        self.scan_result.add_trace(macro_trace)

    def discover_syslog_traces(self):
        # Logic to discover syslog traces
        syslog_trace = TraceInfo('syslog', 'Example syslog trace detail')
        self.scan_result.add_trace(syslog_trace)

    def export_results(self):
        return self.scan_result.export_to_json()


# Example usage
if __name__ == '__main__':
    scanner = TraceScanner()
    scanner.discover_printf_traces()
    scanner.discover_macro_traces()
    scanner.discover_syslog_traces()
    print(scanner.export_results())