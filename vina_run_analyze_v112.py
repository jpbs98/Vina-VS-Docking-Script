"""
Vina Virtual Screening --> Run & Analyze
By: João Silva (jpbs98)
"""
import os

# get path
path = os.getcwd()

# run iterative vina command on all ligands --> change receptor name
for file in os.listdir(path):
    if file == "receptor.pdbqt":
        continue
    elif file.endswith(".pdbqt"):
        os.system(
            f"vina --config conf.txt --ligand {file} --log {file}_log.log")

os.system("tail -n11 *.log > results.txt")

print("\n")
print("Starting analysis...")
dct = {}

# iterate over log files and output results in dict form
for file in os.listdir(path):
    if file.endswith(".pdbqt_log.log"):
        with open(file, "r") as f:
            for i, line in enumerate(f):
                if i == 27:
                    dct[file] = float(line.split()[1])
                elif i > 27:
                    break

# Order the dictionary to output top hits first
ordered_dict = {k: v for k, v in sorted(
    dct.items(), key=lambda item: item[1])}

# Output to .txt file
with open("results_sorted.txt", "w") as o:
    o.write("Sorted Docking Results\n\n")
    for k, v in ordered_dict.items():
        o.write(f"{k}: {v}\n")

print("\n")
print("Analysis complete. See your results in the results_sorted.txt file.")
