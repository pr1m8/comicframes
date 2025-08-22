# ComicFrames

[![PyPI version](https://img.shields.io/pypi/v/comicframes.svg)](https://pypi.org/project/comicframes/)
[![Python versions](https://img.shields.io/pypi/pyversions/comicframes.svg)](https://pypi.org/project/comicframes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/comicframes.svg)](https://pypi.org/project/comicframes/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/yourusername/comicframes/ci.yml?branch=main)](https://github.com/yourusername/comicframes/actions)
[![codecov](https://codecov.io/gh/yourusername/comicframes/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/comicframes)
[![Documentation Status](https://readthedocs.org/projects/comicframes/badge/?version=latest)](https://comicframes.readthedocs.io/en/latest/?badge=latest)

🎨 **A powerful Python package for comic book analysis, frame detection, and animation creation.**

Transform comic books into interactive experiences with AI-powered frame detection, interpolation, and processing pipelines.

## Features

### Core Functionality
- 📖 **PDF Processing**: Convert comic books to high-quality page images
- 🔍 **Frame Detection**: AI-powered panel extraction with multiple algorithms
- 🎬 **Frame Interpolation**: Create smooth animations using RIFE and FILM models
- 💬 **Speech Bubble Detection**: Identify and extract dialogue using YOLO
- 👥 **Character Recognition**: Detect and classify comic characters
- 🎨 **Visual Analysis**: Advanced computer vision for comic understanding

### Architecture & Performance
- ⚡ **High Performance**: Multi-level caching with intelligent TTL management
- 🔄 **Processing Pipelines**: Chain operations with real-time metrics
- 🏗️ **Modular Design**: Plugin architecture for easy model integration
- ⚙️ **Smart Configuration**: Environment-based settings with validation
- 📊 **Model Registry**: Centralized AI model management and loading

### Developer Experience
- 🛡️ **Type Safety**: Complete type annotations and runtime validation
- 🔄 **Backward Compatible**: Legacy APIs preserved for easy migration
- 🖥️ **Rich CLI**: 5+ command-line tools for batch processing
- 🧩 **Extensible**: Simple APIs for custom processors and models
- 📈 **Analytics**: Built-in performance monitoring and cache statistics

## 🤖 AI Models & Integration

ComicFrames integrates with state-of-the-art AI models for comic analysis:

### Frame Interpolation Models
- 🎬 **RIFE (Real-Time Intermediate Flow Estimation)**: [megvii-research/ECCV2022-RIFE](https://github.com/megvii-research/ECCV2022-RIFE)
- 🎭 **FILM (Frame Interpolation for Large Motion)**: [google-research/frame-interpolation](https://github.com/google-research/frame-interpolation)

### Computer Vision Models
- 🔍 **YOLO**: Object detection for speech bubbles and characters
- 🖼️ **OpenCV**: Traditional computer vision for frame detection

### Hugging Face Integration
- 🤗 **Model Hub**: Access to pre-trained models via Hugging Face Hub
- 📦 **Easy Loading**: Automatic model downloading and caching
- 🔄 **Model Versioning**: Consistent model management across environments

```python
# Example: Using Hugging Face models (coming soon)
from comicframes import ModelFactory

# Load frame interpolation model from Hugging Face
interpolator = ModelFactory.create_model("huggingface/comic-frame-interpolation")

# Load speech bubble detection model
detector = ModelFactory.create_model("huggingface/comic-speech-detection")
```

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

## 🚀 Roadmap

### Current Features ✅
- PDF to image conversion with high quality
- OpenCV-based frame detection (threshold & Canny)
- Multi-level caching system with TTL
- Processing pipelines with metrics
- CLI tools for batch processing

### Coming Soon 🔄
- **RIFE Integration**: Real-time frame interpolation
- **FILM Integration**: Large motion frame interpolation  
- **YOLO Integration**: Speech bubble and character detection
- **Hugging Face Models**: Pre-trained comic analysis models
- **Animation Export**: MP4/GIF generation from frames
- **Web Interface**: Browser-based comic processing

### Future Enhancements 🔮
- Character emotion detection
- Story flow analysis
- Automated comic summarization
- Multi-language speech bubble text extraction
- Comic style transfer and generation

## 🏷️ Tags

`computer-vision` `comic-analysis` `frame-detection` `animation` `ai` `machine-learning` `opencv` `yolo` `rife` `film` `huggingface` `python` `cli` `processing-pipeline` `caching`

## 🤝 Contributing

We welcome contributions! ComicFrames is designed to be easily extensible:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Add your processor/model**: Follow our plugin architecture
4. **Add tests**: Ensure your code is well-tested
5. **Submit a PR**: We'll review and merge

See our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

## 📚 Citation

If you use ComicFrames in your research, please cite:

```bibtex
@software{comicframes2024,
  title={ComicFrames: AI-Powered Comic Book Analysis and Animation},
  author={ComicFrames Team},
  year={2024},
  url={https://github.com/yourusername/comicframes},
  version={0.1.0}
}
```

## 🔗 Related Projects

- [ECCV2022-RIFE](https://github.com/megvii-research/ECCV2022-RIFE) - Real-Time Intermediate Flow Estimation
- [frame-interpolation](https://github.com/google-research/frame-interpolation) - Google's FILM models
- [YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection framework
- [Hugging Face Hub](https://huggingface.co/models) - Model repository and hosting

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/comicframes?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/comicframes?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/comicframes)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/comicframes)

## License

MIT License - see the [LICENSE](LICENSE) file for details.