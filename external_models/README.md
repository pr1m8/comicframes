# External Models

This directory contains external model implementations that are integrated with ComicFrames.

## Contents

### ECCV2022-RIFE
- **Purpose**: Video frame interpolation using RIFE (Real-Time Intermediate Flow Estimation)
- **Source**: https://github.com/megvii-research/ECCV2022-RIFE
- **Integration**: Used by `RIFEInterpolator` in `comicframes.models.interpolation_models`
- **Models**: Pre-trained models for frame interpolation

### frame-interpolation
- **Purpose**: Google's FILM (Frame Interpolation for Large Motion) implementation
- **Source**: https://github.com/google-research/frame-interpolation
- **Integration**: Used by `FILMInterpolator` in `comicframes.models.interpolation_models`
- **Models**: TensorFlow-based frame interpolation models

### Yolo_Model
- **Purpose**: YOLO object detection for comic analysis
- **Integration**: Used by `YOLODetector` in `comicframes.models.object_detection_model`
- **Use Cases**: 
  - Speech bubble detection
  - Character detection
  - Panel boundary detection

## Integration Status

| Model | Status | ComicFrames Integration |
|-------|--------|------------------------|
| RIFE | ⚠️ Partial | Model registry configured, implementation TODO |
| FILM | ⚠️ Partial | Model registry configured, implementation TODO |
| YOLO | ⚠️ Partial | Model registry configured, implementation TODO |

## Usage

These models are automatically available through the ComicFrames model system:

```python
from comicframes import ModelFactory
from comicframes.config import ModelType

# Create interpolation model
interpolator = ModelFactory.create_model("rife_v4.6")

# Create object detection model  
detector = ModelFactory.create_model("yolov3")

# List all available models
models = ModelFactory.list_available_models()
```

## Development

To fully integrate these models:

1. **RIFE Integration**: Complete `RIFEInterpolator._load_model()` and `_predict()` methods
2. **FILM Integration**: Complete `FILMInterpolator._load_model()` and `_predict()` methods  
3. **YOLO Integration**: Complete `YOLODetector._load_model()` and `_predict()` methods

Each model should follow the `BaseModel` interface for consistent integration.
