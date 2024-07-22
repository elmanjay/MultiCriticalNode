import subprocess
import os
yasol_directory = "/Users/lennardhansmann/Desktop/Yasol_4.0.1.5_b_mac/Yasol/Debug"


def solve(folder, instance_name):
    #yasol_directory = "/Users/lennardhansmann/Desktop/Yasol_4.0.1.5_b_mac/Yasol/Debug"
    executable_name = "Yasol"

    # Vollständiger Pfad zur ausführbaren Datei
    executable_path = os.path.join(yasol_directory, executable_name)


    if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
        # Ausführen der ausführbaren Datei im angegebenen Verzeichnis
        result = subprocess.run([f"./{executable_name}", f"{folder}/{instance_name}"], cwd=yasol_directory, capture_output=True, text=True)
        
        # Überprüfen des Rückgabewerts und Ausgabe
        print("Return code:", result.returncode)
        print("Standard Output:", result.stdout)
        print("Standard Error:", result.stderr)
    else:
        print("Die Datei existiert nicht oder ist nicht ausführbar.")

if __name__ == "__main__":
    for  filename in os.listdir(os.path.join(yasol_directory, "Train_Instances")):
        if filename.endswith(".qlp"):
            solve("Train_Instances",filename)


