import os
import time
import shutil

# get paths and set destination folders
path = os.getcwd()
OUTS = path + "/outputs/"
RES = path + "/results"

# start time
time1 = time.time()

# run iterative vina command on all ligands --> change receptor name
for file in os.listdir(path):
    if file == "receptor.pdbqt":
        continue
    elif file.endswith(".pdbqt"):
        os.system(f"vina --config conf.txt --ligand {file}")


print("\n")
print("Starting analysis...")
dct = {}

# iterate over log files and output results in dict form
for file in os.listdir(path):
    if file.endswith("out.pdbqt"):
        with open(file, "r") as f:
            for i, line in enumerate(f):
                if i == 1:
                    dct[file] = float(line.split(":")[1].split()[0])
                elif i > 1:
                    break

# Order the dictionary to output top hits first
ordered_dict = {k: v for k, v in sorted(dct.items(), key=lambda item: item[1])}

# Output to .txt file
with open("results_sorted.txt", "w") as o:
    o.write("Sorted Docking Results\n\n")
    for k, v in ordered_dict.items():
        o.write(f"{k}: {v}\n")

print("\n")
print("Analysis complete. See your results in the results_sorted.txt file.")

time2 = time.time()
runtime = time2-time1

print("\n")
print(str(runtime/60) + " mins runtime.")

# move out structures to separate folder
if not os.path.exists(OUTS):
    os.mkdir(OUTS)
for file in os.listdir(path):
    if file.endswith("_out.pdbqt"):
        shutil.move(file, OUTS)

# move results to separate folder
if not os.path.exists(RES):
    os.mkdir(RES)
for file in os.listdir(path):
    if file.startswith("results"):
        shutil.move(file, RES)
