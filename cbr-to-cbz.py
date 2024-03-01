import os
import subprocess
import zipfile
import shutil

def convert_folder_to_cbz(input_folder_name="input", output_folder_name="output", temp_folder_name="temp_folder"):
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Create input, output, and temp folders in the script directory
    input_folder = os.path.join(script_directory, input_folder_name)
    output_folder = os.path.join(script_directory, output_folder_name)
    temp_folder = os.path.join(script_directory, temp_folder_name)

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(temp_folder, exist_ok=True)

    try:
        # Specify the full path to UnRAR.exe
        unrar_executable = os.path.join(script_directory, "UnRAR.exe")

        # Iterate through all files in the input folder
        for input_cbr_filename in os.listdir(input_folder):
            if input_cbr_filename.lower().endswith(".cbr"):
                input_cbr_path = os.path.join(input_folder, input_cbr_filename)

                # Construct the output CBZ file name
                output_cbz_filename = os.path.splitext(input_cbr_filename)[0] + ".cbz"
                output_cbz_path = os.path.join(output_folder, output_cbz_filename)

                # Construct the extraction command
                extract_command = [unrar_executable, "x", "-y", input_cbr_path, temp_folder]

                # Run the extraction command using subprocess
                subprocess.run(extract_command, check=True)

                # Create a .cbz file and add the extracted contents
                with zipfile.ZipFile(output_cbz_path, 'w', zipfile.ZIP_DEFLATED) as cbz_file:
                    for root, dirs, files in os.walk(temp_folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, temp_folder)
                            cbz_file.write(file_path, arcname=rel_path)

                print(f"Conversion successful: {input_cbr_filename} -> {output_cbz_filename}")

    except Exception as e:
        print(f"Conversion failed: {e}")

    finally:
        # Clean up the temporary folder
        shutil.rmtree(temp_folder)

if __name__ == "__main__":
    # Perform the conversion for all files in the input folder
    convert_folder_to_cbz()
