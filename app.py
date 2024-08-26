{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.10.14","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kaggle":{"accelerator":"nvidiaTeslaT4","dataSources":[],"dockerImageVersionId":30762,"isInternetEnabled":true,"language":"python","sourceType":"notebook","isGpuEnabled":true}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"pip install transformers Pillow requests","metadata":{"_uuid":"8f2839f25d086af736a60e9eeb907d3b93b6e0e5","_cell_guid":"b1076dfc-b9ad-4769-8c92-a6c4dae69d19","trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"code","source":"!pip install bitsandbytes>=0.39.0\n!pip install --upgrade accelerate transformers","metadata":{"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"code","source":"!pip install -q streamlit\n!npm install localtunnel","metadata":{"trusted":true},"execution_count":null,"outputs":[]},{"cell_type":"code","source":"%%writefile app.py\nimport streamlit as st\nfrom PIL import Image\nimport torch\nfrom transformers import AutoModelForCausalLM, AutoProcessor\n\n# Load the pre-trained model and processor\nmodel_id = \"microsoft/Phi-3.5-vision-instruct\"\nmodel = AutoModelForCausalLM.from_pretrained(\n    model_id,\n    device_map=\"cuda\",\n    trust_remote_code=True,\n    load_in_4bit=True,\n    _attn_implementation='eager'\n)\n\nprocessor = AutoProcessor.from_pretrained(model_id,\n                                          trust_remote_code=True,\n                                          num_crops=4\n                                         )\n\n# Create a Streamlit application\nst.title(\"Instagram Caption Generator📝\")\nst.write(\"Upload an image and get captions for Instagram posts!\")\n\n# Create an uploader for the image\nuploaded_image = st.file_uploader(\"Upload an image\", type=[\"jpg\", \"png\", \"jpeg\"])\n\nif uploaded_image is not None:\n    # Display the uploaded image\n    st.write(\"Uploaded Image:\")\n    st.image(uploaded_image, width=400)\n\n    # Open the image using PIL\n    image = Image.open(uploaded_image)\n\n    # Create a placeholder for the image\n    placeholder = \"<|image_1|>\"\n\n    # Create a message with the placeholder\n    messages = [\n        {\"role\": \"user\", \"content\": placeholder + \"generate 5 captions based on the provided image for instagram post remember each caption should be a medium length sentence and use emojis\"},\n    ]\n\n    # Process the message and image\n    prompt = processor.tokenizer.apply_chat_template(\n        messages,\n        tokenize=False,\n        add_generation_prompt=True\n    )\n\n    inputs = processor(prompt, [image], return_tensors=\"pt\").to(\"cuda:0\")\n\n    # Generate the description\n    generation_args = {\n        \"max_new_tokens\": 1000,\n        \"temperature\": 1,\n        \"do_sample\": False,\n    }\n\n    generate_ids = model.generate(**inputs,\n                                  eos_token_id=processor.tokenizer.eos_token_id,\n                                  **generation_args\n                                 )\n\n    # Remove input tokens\n    generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]\n    response = processor.batch_decode(generate_ids,\n                                      skip_special_tokens=True,\n                                      clean_up_tokenization_spaces=False)[0]\n\n    # Display the description\n    st.write(\"Captions:\")\n    st.write(response)","metadata":{"execution":{"iopub.status.busy":"2024-08-26T17:26:49.499157Z","iopub.execute_input":"2024-08-26T17:26:49.499895Z","iopub.status.idle":"2024-08-26T17:26:49.514022Z","shell.execute_reply.started":"2024-08-26T17:26:49.499849Z","shell.execute_reply":"2024-08-26T17:26:49.513127Z"},"trusted":true},"execution_count":1,"outputs":[{"name":"stdout","text":"Overwriting app.py\n","output_type":"stream"}]},{"cell_type":"code","source":"!curl ipv4.icanhazip.com","metadata":{"execution":{"iopub.status.busy":"2024-08-26T17:26:56.018080Z","iopub.execute_input":"2024-08-26T17:26:56.018469Z","iopub.status.idle":"2024-08-26T17:26:57.040131Z","shell.execute_reply.started":"2024-08-26T17:26:56.018410Z","shell.execute_reply":"2024-08-26T17:26:57.038855Z"},"trusted":true},"execution_count":2,"outputs":[{"name":"stdout","text":"34.168.168.211\n","output_type":"stream"}]},{"cell_type":"code","source":"!streamlit run app.py &>./logs.txt & npx localtunnel --port 8501","metadata":{"execution":{"iopub.status.busy":"2024-08-26T17:27:04.050516Z","iopub.execute_input":"2024-08-26T17:27:04.050923Z"},"trusted":true},"execution_count":null,"outputs":[{"name":"stdout","text":"your url is: https://sad-donuts-punch.loca.lt\n","output_type":"stream"}]},{"cell_type":"code","source":"","metadata":{},"execution_count":null,"outputs":[]}]}