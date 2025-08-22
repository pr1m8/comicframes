# ComicFrames Architecture

This document describes the architecture of the ComicFrames package after the major refactoring.

## Overview

ComicFrames is now organized into a modular, extensible architecture with proper separation of concerns, caching, configuration management, and model abstraction.

## Directory Structure

```
src/comicframes/
├── __init__.py              # Main package exports
├── cli.py                   # Command-line interfaces
├── pdf_processor.py         # Legacy PDF processing (backward compatibility)
├── frame_detector.py        # Legacy frame detection (backward compatibility)
├── utils.py                 # Legacy utilities (backward compatibility)
│
├── config/                  # Configuration management
│   ├── __init__.py
│   ├── settings.py          # Global settings
│   ├── cache_config.py      # Cache configuration
│   └── model_config.py      # Model registry and configuration
│
├── cache/                   # Caching system
│   ├── __init__.py
│   ├── file_cache.py        # File-based caching
│   ├── memory_cache.py      # In-memory caching
│   └── cache_manager.py     # Central cache management
│
├── core/                    # Core abstractions
│   ├── __init__.py
│   ├── data_structures.py   # Data models (Frame, ComicPage, etc.)
│   ├── base_processor.py    # Base class for processors
│   ├── base_model.py        # Base class for ML models
│   └── pipeline.py          # Processing pipeline
│
├── models/                  # Model implementations
│   ├── __init__.py
│   ├── model_factory.py     # Factory for creating models
│   ├── frame_detection_model.py    # OpenCV frame detection
│   ├── interpolation_models.py     # RIFE, FILM interpolation
│   └── object_detection_model.py   # YOLO detection
│
└── processing/              # High-level processors
    ├── __init__.py
    ├── pdf_processor.py     # PDF processing with new architecture
    ├── frame_processor.py   # Frame detection with new architecture
    └── interpolation_processor.py  # Frame interpolation
```

## Key Components

### 1. Configuration System (`config/`)

- **Settings**: Global configuration with environment variable support
- **CacheConfig**: Cache-specific configuration
- **ModelConfig**: Model registry and configuration
- **ModelRegistry**: Central registry of available models

### 2. Caching System (`cache/`)

- **FileCache**: Persistent file-based caching with TTL and size limits
- **MemoryCache**: Fast in-memory caching with LRU eviction
- **CacheManager**: Unified interface for all cache types

### 3. Core Abstractions (`core/`)

- **Data Structures**: Type-safe data models (Frame, ComicPage, BoundingBox, etc.)
- **BaseProcessor**: Abstract base for all processing operations
- **BaseModel**: Abstract base for all ML models
- **ProcessingPipeline**: Chain multiple processors together

### 4. Model System (`models/`)

- **ModelFactory**: Create model instances by name or type
- **Frame Detection**: OpenCV-based contour detection
- **Interpolation**: RIFE and FILM frame interpolation (TODO)
- **Object Detection**: YOLO-based detection (TODO)

### 5. Processing Modules (`processing/`)

- **PDFProcessor**: Extract pages from PDF files
- **FrameProcessor**: Detect frames in comic pages
- **InterpolationProcessor**: Generate interpolated frames

## Key Features

### 1. Backward Compatibility

All existing APIs are preserved for backward compatibility:

```python
# Old way (still works)
from comicframes import pdf_to_images, detect_frames

# New way
from comicframes.processing import PDFProcessor, FrameProcessor
```

### 2. Configuration Management

```python
from comicframes import Settings, get_settings

settings = get_settings()
settings.min_frame_width = 100
settings.enable_cache = True
```

### 3. Caching System

```python
from comicframes import get_cache_manager

cache = get_cache_manager()
cache.set_frame_data("key", data)
data = cache.get_frame_data("key")
```

### 4. Model Management

```python
from comicframes import ModelFactory
from comicframes.config import ModelType

# Create specific model
detector = ModelFactory.create_model("opencv_contours")

# Create default model for type
detector = ModelFactory.create_default_model(ModelType.FRAME_DETECTION)
```

### 5. Processing Pipelines

```python
from comicframes.processing import PDFProcessor, FrameProcessor
from comicframes.core import ProcessingPipeline

pipeline = ProcessingPipeline("comic_processing")
pipeline.add_stage(PDFProcessor())
pipeline.add_stage(FrameProcessor())

result = pipeline.process("comic.pdf")
```

## CLI Commands

The package now provides several CLI commands:

- `comicframes-pdf`: Convert PDF to images (legacy)
- `comicframes-extract`: Extract frames from images (legacy)
- `comicframes-pipeline`: Run complete processing pipeline
- `comicframes-cache`: Manage cache (stats, clear, cleanup)
- `comicframes-models`: Manage models (list, info)

## Performance Optimizations

### 1. Intelligent Caching

- **Multi-level caching**: Memory, file-based, and processing caches
- **TTL-based expiration**: Automatic cleanup of stale data
- **Size limits**: Prevents cache from consuming too much storage
- **Cache hit tracking**: Monitors cache effectiveness

### 2. Lazy Loading

- Models are loaded only when needed
- Image data is loaded on demand
- Configuration is cached across requests

### 3. Processing Metrics

- Processing time tracking
- Success/failure rates
- Cache hit rates
- Stage-level metrics in pipelines

## Extension Points

### 1. Custom Processors

```python
from comicframes.core import BaseProcessor

class CustomProcessor(BaseProcessor):
    def _process(self, data):
        # Your processing logic
        return processed_data
```

### 2. Custom Models

```python
from comicframes.core import BaseModel

class CustomModel(BaseModel):
    def _load_model(self):
        # Load your model
        return model
    
    def _predict(self, input_data):
        # Make predictions
        return predictions
```

### 3. Custom Cache Backends

The cache system is extensible to support different backends (Redis, database, etc.).

## Integration with Existing Codebases

The refactored architecture integrates the existing external models:

- **ECCV2022-RIFE**: Frame interpolation models (to be integrated)
- **frame-interpolation**: Google's FILM models (to be integrated)
- **Yolo_Model**: Object detection (to be integrated)

These will be properly wrapped in the new model abstraction system.

## Future Enhancements

1. **Model Integration**: Complete RIFE, FILM, and YOLO integrations
2. **Distributed Processing**: Support for distributed/parallel processing
3. **Model Training**: APIs for training custom models
4. **Web Interface**: Web-based UI for processing pipelines
5. **Database Backend**: Optional database storage for metadata
6. **GPU Acceleration**: Automatic GPU utilization when available
