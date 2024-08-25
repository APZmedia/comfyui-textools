from setuptools import setup, find_packages
import sys
import os

def print_status(message):
    """Utility function to print status messages."""
    print(f"[STATUS] {message}")

try:
    print_status("Starting the setup process...")

    # Check Python version
    if sys.version_info < (3, 7):
        print_status("Python 3.7 or higher is required.")
        sys.exit(1)
    print_status(f"Python version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected.")

    # Check if README.md exists
    readme_file = 'README.md'
    if not os.path.isfile(readme_file):
        print_status(f"Warning: {readme_file} not found. Please ensure that it is present.")
    else:
        print_status(f"{readme_file} found.")

    # Attempt to open and read the README.md file
    try:
        long_description = open(readme_file).read()
        print_status(f"Successfully read {readme_file}.")
    except Exception as e:
        print_status(f"Error reading {readme_file}: {e}")
        long_description = 'A description of the package.'  # Fallback description

    # Proceed with setup
    setup(
        name='ComfyUI-APZmedia-textTools',
        version='0.1.0',
        description='Nodes for applying rich text overlays on images and videos.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Pablo Apiolazza',
        author_email='pablo@apzmedia.com',
        url='https://github.com/APZmedia/comfyui-textools',
        packages=find_packages(),
        install_requires=[
            'Pillow>=8.0.0',
            'torch>=1.7.0',
        ],
        python_requires='>=3.7',

        entry_points={
            'comfyui.custom_nodes': [
                'APZmediaImageRichTextOverlay = nodes.apzImageRichTextOverlay:APZmediaImageRichTextOverlay',
            ]
        }
    )

    print_status("Setup completed successfully.")

except Exception as e:
    print_status(f"Setup failed: {e}")
    sys.exit(1)
