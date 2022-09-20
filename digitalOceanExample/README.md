Follow this guide https://www.digitalocean.com/community/tutorials/how-to-build-a-neural-network-to-translate-sign-language-into-english

# Mac

MacOS version: 12.6
python version: 3.9.8

`pip install torch torchvision opencv-python numpy grpcio onnx onnxruntime`

## Issues

1. <b>"AssertionError: Could not find "cmake" executable!</b>
   Run "brew install cmake"

2. <b>The clang compiler does not support 'faltivec'</b>
   Run `brew install openblas` then `OPENBLAS="$(brew --prefix openblas)" pip install numpy`

3. <b>pip install onnx failed</b>
   `brew install cmake`
   `brew install protobuf`
   `pip install onnx --no-use-pep517`