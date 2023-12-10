shared = {
    'checkbox_high_options':["Q8_0", "F16", "F32"],
    'checkbox_options': [
    "q4_0", "q4_1", "q5_0", "q5_1", "q2_K", "q3_K", "q3_K_S", "q3_K_M", "q3_K_L",
    "q4_K", "q4_K_S", "q4_K_M", "q5_K", "q5_K_S", "q5_K_M", "q6_K", "q8_0", "F16", "F32"],
    'api_endpoint': {'url': 'https://status-gg-spaces-mm.trycloudflare.com'},
    'gradio': {},
    'parameters': {
        'mirostat': [0, [0, 1, 2]],  # Dropdown
        'mirostat_eta': [0.1, (0.0, 1.0)],
        'mirostat_tau': [0.1, (0.0, 1.0)],
        'num_ctx': [4096, (1024, 16912)],
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
        'top_p': [1.0, (0.1, 1.0)],

    }
}