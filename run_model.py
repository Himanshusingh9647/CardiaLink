"""
Module to run the heart disease model training
"""
# Explicitly import the modules to help IDE recognize them
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping

# Run the model training script
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    from src.components.model import v 