import tlsh
from collections import defaultdict
import argparse
import os
import json

all_diffoscope_files = []
all_sources = []

def parse_args():
    parser = argparse.ArgumentParser(description='Process release consistency')
    parser.add_argument('--base-dir', 
                       default="results",
                       help='Base directory for processing (default: results)')
    return parser.parse_args()

args = parse_args()

def get_unified_diff(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    s = ''
    unified_diff = data.get('unified_diff', '')
    if unified_diff:
        s += unified_diff
    if 'details' in data:
        s += process_details(data['details'])
    
    return s

def process_details(details):
    s = ''
    for detail in details:
        unified_diff = detail.get('unified_diff', '')
        if unified_diff:
            s += unified_diff
    if 'details' in details:
        s += process_details(details['details'])

    return s

for root, dirs, files in os.walk(args.base_dir):
    for file in files:
        if file.endswith(".diffoscope.json"):
            all_diffoscope_files.append(os.path.join(root, file))
            all_sources.append(get_unified_diff(os.path.join(root, file)))

similarity_matrix = []
similarity_matrix_visited = []
for i in range(len(all_sources)):
    similarity_matrix.append([-1] * len(all_sources))
    similarity_matrix_visited.append([False] * len(all_sources))


for i in range(len(all_sources)):
    row = []
    for j in range(len(all_sources)):
        if similarity_matrix_visited[i][j] or similarity_matrix_visited[j][i]:
            continue
        
        source1 = all_sources[i].encode()
        source2 = all_sources[j].encode()

        tlsh1 = tlsh.hash(source1)
        tlsh2 = tlsh.hash(source2)

        if source1 == source2:
            score = 0
        elif tlsh1 == 'TNULL' or tlsh2 == 'TNULL':
            score = -1
        else:
            score = tlsh.diff(tlsh1, tlsh2)

        similarity_matrix_visited[i][j] = True
        similarity_matrix_visited[j][i] = True
        similarity_matrix[i][j] = score
        similarity_matrix[j][i] = score
    
print("[")
for row in similarity_matrix:
    print(row)
print("]")
for i in range(len(all_diffoscope_files)):
    print(f'{i}: {all_diffoscope_files[i]}')

too_small = set()
clusters = defaultdict(set)
visited_matrix = []
for i in range(len(similarity_matrix)):
    visited_matrix.append([False] * len(similarity_matrix[i]))

for i in range(len(similarity_matrix)):
    for j in range(len(similarity_matrix[i])):
        if i == j:
            continue
        # if similarity_matrix[i][j] == -1 and not visited_matrix[i][j]:
        #     if len(all_sources[i]) < len(all_sources[j]):
        #         too_small.add(all_sources[i])
        #     else:
        #         too_small.add(all_sources[j])
        elif similarity_matrix[i][j] <= 1000 and not visited_matrix[i][j]:
            clusters[all_diffoscope_files[i]].add(all_diffoscope_files[j])
            for k in range(len(similarity_matrix)):
                visited_matrix[j][k] = True

    visited_matrix[i][j] = True
    

with open('text-clusters-too-small.txt', 'w') as f:
    for file in too_small:
        f.write(file + "\n")

with open('text-clusters.txt', 'w') as f:
    for cluster in clusters:
        f.write(str(cluster) + ": " + str(clusters[cluster]) + "\n")