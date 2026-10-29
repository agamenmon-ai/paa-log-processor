import json
import pprint

def load_log_file(file_path):
    """
    Safely reads a raw device log file and returns a list of lines.
    Handles I/O and encoding exceptions.
    """
    try:
        with open("/content/paa-ipamplifier-2026-08-31T08_25_21.370Z.log", "r", encoding="utf-8") as file:
            log_lines = file.readlines()
        print(f"[OK]: File successfully loaded. Total lines: {len(log_lines)}")
        return log_lines
    except FileNotFoundError:
        print(f"[ERROR]: Log file not found at path: {file_path}")
        return []
    except UnicodeDecodeError as err:
        print(f"[ERROR]: Encoding issue while reading the file: {err}")
        return []

def filter_noise(log_lines, noise_keyword="Received ping response"):
    """
    Filters out routine noise (like continuous pings) to keep only valuable events.
    """
    clean_logs = [
        line.strip() for line in log_lines 
        if noise_keyword not in line and line.strip() != ""
    ]
    return clean_logs

def extract_rpc_connections(log_lines):
    """
    Extracts endpoints of new JSON RPC connections from the filtered logs.
    """
    new_connections = [
        line.split()[-1].strip('"') 
        for line in log_lines 
        if "New Json Rpc Connection" in line
    ]
    return new_connections

def count_log_events(log_lines, target_keyword):
    """
    Counts total occurrences of a specific keyword/event in the log lines.
    """
    matched_lines = [line for line in log_lines if target_keyword in line]
    return len(matched_lines)

if __name__ == "__main__":
    print("--- Starting PAA Log Processor Utility ---\n")
    
    target_log_file = "paa_device.log"
    
    # 1. Create a sample log file for demonstration purposes
    try:
        with open(target_log_file, "w", encoding="utf-8") as dummy:
            dummy.write("2026-08-31T08:25:21 [INFO] System boot sequence initialized\n")
            dummy.write("2026-08-31T08:25:22 [DEBUG] Received ping response from gateway\n")
            dummy.write('2026-08-31T08:25:25 New Json Rpc Connection from "172.17.40.40:53544"\n')
            dummy.write("2026-08-31T08:25:28 [DEBUG] Received ping response from gateway\n")
            dummy.write("2026-08-31T08:25:30 Set Volume: 85 (MQTT topic updated)\n")
    except OSError:
        pass

    # 2. Read and Process the log data
    raw_lines = load_log_file(target_log_file)
    
    if raw_lines:
        filtered_lines = filter_noise(raw_lines)
        connections = extract_rpc_connections(filtered_lines)
        volume_events_count = count_log_events(filtered_lines, "Volume")

        # 3. Compile a structured analytical report
        report_data = {
            "total_raw_lines": len(raw_lines),
            "total_filtered_lines": len(filtered_lines),
            "rpc_connections_found": connections,
            "volume_events_count": volume_events_count,
            "filtered_sample": filtered_lines[:10] # Keep a clean sample
        }

        pprint.pprint(report_data)

        # 4. Export the final report to JSON
        output_filename = "paa_structured_report.json"
        try:
            with open(output_filename, "w", encoding="utf-8") as out_file:
                json.dump(report_data, out_file, indent=4, ensure_ascii=False)
            print(f"\n[SUCCESS]: Structured report successfully saved to {output_filename}")
        except (TypeError, OSError) as err:
            print(f"[FAIL]: Could not save JSON report: {err}")
