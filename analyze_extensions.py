import json
import os
from pathlib import Path
import argparse
# Dictionary to store extensions and their jNorm values
extension_stats = {}
total_stats = {'total': 0, 'jnorm_0': 0, 'jnorm_1': 0, 'jnorm_2': 0}


def parse_args():
    parser = argparse.ArgumentParser(description='Analyze file extensions')
    parser.add_argument('--base-dir', 
                       default="results",
                       help='Base directory for analysis (default: results)')
    return parser.parse_args()

def get_extension(filename):
    """Get the compound extension from a filename (handles multi-part extensions)"""
    parts = filename.split('.')
    if len(parts) <= 1:
        return ''
    
    # Handle compound extensions like .tar.gz
    if len(parts) > 2 and parts[-2] in ['tar']:
        return f'.{parts[-2]}.{parts[-1]}'
    return f'.{parts[-1]}'

# Walk through the directory
args = parse_args()
base_dir = args.base_dir
for root, _, files in os.walk(base_dir):
    for file in files:
        if file == "jNorm_summary.json":
            file_path = Path(root) / file
            
            # Read each JSON file
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                    
                    # Analyze each artifact in the artifacts list
                    for artifact in data['artifacts']:
                        name = artifact['artifact_name']
                        jnorm = artifact['jNorm']
                        
                        # Find the extension
                        ext = get_extension(name)
                        if ext:  # Only process files with extensions
                            if ext not in extension_stats:
                                extension_stats[ext] = {'total': 0, 'jnorm_0': 0, 'jnorm_1': 0, 'jnorm_2': 0}
                            
                            extension_stats[ext]['total'] += 1
                            extension_stats[ext][f'jnorm_{jnorm}'] += 1
                            
                            # Update totals
                            total_stats['total'] += 1
                            total_stats[f'jnorm_{jnorm}'] += 1
                except json.JSONDecodeError:
                    print(f"Error reading {file_path}")
                    continue

# Print results
print("Extension Statistics:")
print("\nExt\t\tTotal\tjNorm 0\tjNorm 1\tjNorm 2\tSuccess Rate")
print("-" * 65)
for ext, stats in extension_stats.items():
    success_rate = (stats['jnorm_0'] / stats['total'] * 100) if stats['total'] > 0 else 0
    ext_padded = f"{ext}\t" if len(ext) >= 8 else f"{ext}\t\t"
    print(f"{ext_padded}{stats['total']}\t{stats['jnorm_0']}\t{stats['jnorm_1']}\t{stats['jnorm_2']}\t{success_rate:.1f}%")

# Print totals
print("-" * 65)
total_success_rate = (total_stats['jnorm_0'] / total_stats['total'] * 100) if total_stats['total'] > 0 else 0
print(f"TOTAL\t\t{total_stats['total']}\t{total_stats['jnorm_0']}\t{total_stats['jnorm_1']}\t{total_stats['jnorm_2']}\t{total_success_rate:.1f}%") 