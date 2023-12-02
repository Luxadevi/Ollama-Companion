shared = {
    'api_endpoint': {"url": "http://127.0.0.1:11434"},  # Updated API URL
    'gradio': {},
    'parameters': {
        'mirostat': [0, [0, 1, 2]],  # Dropdown
        'mirostat_eta': [0.1, (0.0, 1.0)],
        'mirostat_tau': [0.1, (0.0, 1.0)],
        'num_ctx': [4096, (1024, 8192)],
        'num_gqa': [256, (128, 512)],
        'num_gpu': [0, (1, 250)],
        'num_thread': [0, (0, 64)],
        'repeat_last_n': [0, (0, 32000)],
        'repeat_penalty': [1.0, (0.5, 2.0)],
        'temperature': [0.8, (0.1, 1.0)],
        'seed': [None, (0, 10000)],  # None indicates no default value
        'tfs_z': [1, (1, 20)],  # Slider from 1 to 20
        'num_predict': [256, (128, 512)],
        'top_k': [0, (0, 100)],
        'top_p': [1.0, (0.1, 1.0)]
    }
}