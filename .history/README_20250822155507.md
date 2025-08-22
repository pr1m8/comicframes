# ComicFrames

A Python package for comic book frame detection and processing.

## Features

### Core Functionality
- Convert PDF comic books to individual page images
- Detect and extract frames/panels from comic pages
- Support for different detection methods (threshold-based and Canny edge detection)
- Frame interpolation for animation creation (RIFE, FILM)
- Object detection for speech bubbles and characters (YOLO)

### Architecture & Performance
- **Modular Architecture**: Extensible plugin system for models and processors
- **Multi-level Caching**: File-based and in-memory caching with TTL
- **Processing Pipelines**: Chain operations with metrics and error handling
- **Configuration Management**: Environment-based settings with validation
- **Model Registry**: Centralized model management and loading

### Developer Experience
- **Type Safety**: Full type annotations and data validation
- **Backward Compatibility**: Legacy APIs preserved
- **CLI Tools**: Comprehensive command-line interface
- **Extensible**: Easy to add custom processors and models
- **Metrics**: Built-in performance monitoring and cache statistics

## Installation

### Using uv (recommended)

```bash
# Install the package in development mode
uv pip install -e .

# Or install from the package
uv pip install comicframes
```

### Using pip

```bash
# Install the package in development mode
pip install -e .

# Install dependencies
pip install -r requirements.txt
```

## Usage

### As a Python Package

#### Legacy API (Backward Compatible)
```python
from comicframes import pdf_to_images, extract_and_save_frames

# Convert PDF to images
pdf_to_images("comic.pdf", output_base_dir="./output")

# Extract frames from a directory of images
extract_and_save_frames("./pages", "./output")
```

#### New Architecture
```python
from comicframes.processing import PDFProcessor, FrameProcessor
from comicframes.core import ProcessingPipeline

# Create processors
pdf_processor = PDFProcessor()
frame_processor = FrameProcessor()

# Process individually
pdf_result = pdf_processor.process("comic.pdf")
frame_result = frame_processor.process(pdf_result.data[0])

# Or use a pipeline
pipeline = ProcessingPipeline("comic_processing")
pipeline.add_stage(pdf_processor)
pipeline.add_stage(frame_processor)

result = pipeline.process("comic.pdf")
```

#### Configuration and Caching
```python
from comicframes import Settings, get_cache_manager

# Configure settings
settings = Settings(min_frame_width=100, enable_cache=True)

# Manage cache
cache = get_cache_manager()
stats = cache.get_cache_stats()
cache.clear_all()
```

### Command Line Interface

#### Convert PDF to Images

```bash
# Basic usage
comicframes-pdf comic.pdf

# Specify output directory
comicframes-pdf comic.pdf --output-dir ./my_output

# Skip automatic frame detection
comicframes-pdf comic.pdf --no-frame-detection
```

#### Extract Frames from Images

```bash
# Basic usage
comicframes-extract ./pages ./output

# With custom minimum frame sizes
comicframes-extract ./pages ./output --min-width 100 --min-height 150
```

#### New Commands

```bash
# Complete processing pipeline
comicframes-pipeline comic.pdf --output-dir ./output --model opencv_contours

# Cache management
comicframes-cache stats
comicframes-cache clear --type processing
comicframes-cache cleanup

# Model management
comicframes-models list
comicframes-models info opencv_contours
```

## Project Structure

```
comicframes/                    # Clean, organized root
├── src/comicframes/           # Main package source
│   ├── config/               # Configuration management
│   ├── cache/                # Caching system
│   ├── core/                 # Core abstractions
│   ├── models/               # Model implementations
│   ├── processing/           # High-level processors
│   ├── pdf_processor.py      # Legacy compatibility
│   ├── frame_detector.py     # Legacy compatibility
│   └── cli.py               # Command-line interface
├── external_models/          # External model integrations
│   ├── ECCV2022-RIFE/       # RIFE frame interpolation
│   ├── frame-interpolation/  # Google FILM models
│   └── Yolo_Model/          # YOLO object detection
├── data_samples/             # Sample data and tests
│   ├── Data/                # Sample comic data
│   └── test_data/           # Test files
├── examples/                 # Usage examples
├── tests/                    # Test suite
├── docs/                     # Documentation
└── scripts/                  # Utility scripts
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/

# Lint code
flake8 src/
```

### Building the Package

```bash
# Build wheel and source distribution
python -m build

# Install locally
uv pip install dist/comicframes-*.whl
```

## Dependencies

- **pymupdf**: PDF processing
- **opencv-python**: Computer vision and image processing
- **numpy**: Numerical operations
- **pillow**: Image manipulation

## TODO

- Remove title page detection
- Consistent counting methodology for page_total
- Speech bubble classification
- Character identification
- Integration with YOLO models

## License

MIT License
