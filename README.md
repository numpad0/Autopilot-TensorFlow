# Autopilot-TensorFlow
A TensorFlow implementation of this [Nvidia paper](https://arxiv.org/pdf/1604.07316.pdf) with some changes.

#How to Use
Download the dataset ([from author's repo](https://github.com/SullyChen/Autopilot-TensorFlow)) and extract into the repository folder

Use `python train.py` to train the model

Use `python run.py` to run the model on a live webcam feed

Use `python run_dataset.py` to run the model on the dataset

To visualize training using Tensorboard use `tensorboard --logdir=./logs`, then open http://0.0.0.0:6006/ into your web browser.


# How to get it running on Windows with CUDA
## (For those who don't have a Linux box with a good GPU)

- Python __3.5.2__ from https://www.python.org/downloads/release/python-352/
- CUDA Toolkit from https://developer.nvidia.com/cuda-toolkit
- CuDNN(copy to CUDA install dir) from https://developer.nvidia.com/rdp/cudnn-download
- Tensorflow-gpu from https://www.tensorflow.org/install/install_windows

- pip install following from http://www.lfd.uci.edu/~gohlke/pythonlibs/
- numpy
- scipy
- opencv

- pip install pillow

- python run_dataset.py





