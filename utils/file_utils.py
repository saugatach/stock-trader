import os

def clean_path(data_file, config):
    """Ensure the provided file path is a full path and create necessary directories."""
    if not os.path.isabs(data_file):
        data_folder = config.get('data', 'data')
        full_path = os.path.join(data_folder, data_file)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        return full_path
    return data_file