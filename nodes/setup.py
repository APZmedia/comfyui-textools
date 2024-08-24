from setuptools import setup, find_packages

setup(
    name='ComfyUI-APZmedia-textTools',  # Your package name
    version='0.1.0',  # Initial version
    description='Nodes for applying rich text overlays on images and videos.',
    long_description=open('README.md').read(),  # Assuming a README.md is present
    long_description_content_type='text/markdown',
    author='Pablo Apiolazza',  # Replace with your name
    author_email='pablo@apzmedia.com',  # Replace with your email
    url='https://github.com/APZmedia/comfyui-textools',  # Replace with your GitHub or project URL
    packages=find_packages(),  # Automatically find packages in your directory
    install_requires=[
        'Pillow>=8.0.0',  # Image processing library
        'torch>=1.7.0',   # PyTorch for tensor operations
    ],
    python_requires='>=3.7',  # Specify minimum Python version

    # Entry points for integrating custom nodes
    entry_points={
        'comfyui.custom_nodes': [
            'APZmediaImageRichTextOverlay = rich_text_overlay.nodes.APZmediaImageRichTextOverlay:APZmediaImageRichTextOverlay',
        ]
    }
)
