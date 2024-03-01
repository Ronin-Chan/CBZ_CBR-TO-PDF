import os
import img2pdf
from zipfile import ZipFile
import shutil

def cbz_to_pdf(cbz_file, output_folder):
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_cbz_conversion")
    
    try:
        os.makedirs(temp_dir, exist_ok=True)
        
        with ZipFile(cbz_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Check if there's a single subfolder, move files directly if found
        subfolders = [f for f in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, f))]
        
        if len(subfolders) == 1:
            subfolder_path = os.path.join(temp_dir, subfolders[0])

            for file in os.listdir(subfolder_path):
                source_path = os.path.join(subfolder_path, file)
                dest_path = os.path.join(temp_dir, file)
                shutil.move(source_path, dest_path)

        image_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        if not image_files:
            raise ValueError("No valid image files found in the extracted directory.")

        # Modify the PDF file path to save it in the output folder
        pdf_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(cbz_file))[0] + ".pdf")

        with open(pdf_file_path, 'wb') as pdf_output:
            pdf_output.write(img2pdf.convert(image_files))

        print(f"Conversion successful. PDF saved to: {pdf_file_path}")

    except Exception as e:
        print(f"Error during conversion: {e}")

    finally:
        # Remove the temp_cbz_conversion folder
        shutil.rmtree(temp_dir, ignore_errors=True)

def process_folder(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.cbz'):
            cbz_file_path = os.path.join(input_folder, filename)
            cbz_to_pdf(cbz_file_path, output_folder)

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_directory, "input")
    output_folder = os.path.join(script_directory, "output")
    
    os.makedirs(output_folder, exist_ok=True)
    
    process_folder(input_folder, output_folder)
