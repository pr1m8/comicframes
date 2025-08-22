# ComicFrames 🎨🤖

[![PyPI version](https://img.shields.io/pypi/v/comicframes.svg)](https://pypi.org/project/comicframes/)
[![Python versions](https://img.shields.io/pypi/pyversions/comicframes.svg)](https://pypi.org/project/comicframes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/comicframes.svg)](https://pypi.org/project/comicframes/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/pr1m8/comicframes/ci.yml?branch=main)](https://github.com/pr1m8/comicframes/actions)
[![codecov](https://codecov.io/gh/pr1m8/comicframes/branch/main/graph/badge.svg)](https://codecov.io/gh/pr1m8/comicframes)

> **🚀 The beginning of bringing comics to life through AI-powered animation**

**ComicFrames** is a foundational Python package for comic book analysis and the **first step toward creating animated storytelling experiences**. Starting with robust frame detection using OpenCV and computer vision, this project is evolving into a complete animation pipeline powered by state-of-the-art neural networks like RIFE, FILM, and YOLO.

## 🎯 **Vision: From Static to Animated**

This project represents the **starting point** of a larger vision: **transforming static comic books into dynamic, animated experiences**. We're building the infrastructure and tools that will eventually power:

- 🎬 **Seamless frame interpolation** for smooth panel transitions
- 🎭 **Character animation** within comic panels  
- 💬 **Speech bubble dynamics** and text-to-speech integration
- 🎨 **Style-aware animation** preserving artistic integrity
- 🎮 **Interactive comic experiences** with user-driven pacing

## 🛠️ **Current Implementation Status**

### ✅ **Production Ready (v0.1.0)**
- 📖 **PDF Processing**: High-quality comic book to image conversion with PyMuPDF
- 🔍 **OpenCV Frame Detection**: Two robust methods (threshold & Canny edge detection)
- 🏗️ **Modular Architecture**: Clean separation with processing pipelines and caching
- 🖥️ **CLI Tools**: 5 command-line utilities for batch processing
- ⚡ **Smart Caching**: Multi-level cache system with TTL and performance metrics
- 🛡️ **Type Safety**: Complete type annotations and runtime validation

### 🔄 **In Development (Neural Network Integration)**
- 🎬 **RIFE Integration**: Real-time frame interpolation (models included, implementation ongoing)
- 🎭 **FILM Integration**: Google's large motion interpolation (setup complete, API in progress)
- 🔍 **YOLO Detection**: Speech bubble and character detection (config ready, training needed)
- 🤗 **Hugging Face Pipeline**: Model hub integration for community models

### 🎯 **Future Milestones**
- 🎨 **Animation Export**: MP4/GIF generation from interpolated frames
- 💬 **Text Analysis**: OCR and speech bubble text extraction
- 🎮 **Interactive Viewer**: Web-based comic animation player
- 🎭 **Character Tracking**: Persistent character identification across panels

## 🧠 **Computer Vision & AI Foundation**

### **Current OpenCV Implementation**
ComicFrames currently uses **proven computer vision techniques** for robust frame detection:

```python
# Threshold-based detection (clean, geometric panels)
_, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Canny edge detection (complex, artistic layouts)  
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 10, 200)
contours = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
```

### **Neural Network Models (Integration Layer Ready)**
The architecture is **designed for easy model swapping** once neural implementations are complete:

- **🎬 RIFE v4.6**: 130+ FPS frame interpolation (PyTorch models downloaded)
- **🎭 FILM**: TensorFlow-based large motion interpolation (Google Research)
- **🔍 YOLOv3**: Real-time object detection (config files ready)
- **🤗 Hugging Face**: Community model integration via ModelFactory

### **Technical Architecture**
- **🔧 Plugin System**: Easy model registration and switching
- **⚡ Caching**: Intelligent model loading and result caching
- **📊 Metrics**: Performance monitoring for all processing stages
- **🏗️ Pipelines**: Chain OpenCV → Neural Network → Animation export

## 🎬 **Animation Pipeline Architecture**

### **Stage 1: Foundation (✅ Complete)**
```python
from comicframes import pdf_to_images, detect_frames

# Convert comic PDF to high-quality page images
pdf_to_images("watchmen.pdf", output_dir="./pages")

# Extract individual panels using OpenCV
frames_detected = detect_frames("./pages/page_1.png", method="threshold")
```

### **Stage 2: Neural Network Integration (🔄 In Progress)**
```python
from comicframes import ModelFactory, ProcessingPipeline

# Create interpolation pipeline (implementation ongoing)
rife_model = ModelFactory.create_model("rife_v4.6")
film_model = ModelFactory.create_model("film_net") 

# Chain frame detection → interpolation → animation
pipeline = ProcessingPipeline("comic_animation")
pipeline.add_stage(PDFProcessor())
pipeline.add_stage(FrameProcessor())
pipeline.add_stage(InterpolationProcessor(rife_model))

result = pipeline.process("comic.pdf")
```

### **Stage 3: Advanced Animation (🎯 Planned)**
```python
# Future API for complete animation generation
animator = ComicAnimator()
animator.load_comic("comic.pdf")
animator.set_transition_style("smooth")  # smooth, cinematic, dynamic
animator.add_speech_timing("auto")       # auto, manual, voice-sync
animated_comic = animator.render(output_format="mp4")
```

## 🔗 **Neural Network Models & Research**

### **🎬 Frame Interpolation Research**
- **RIFE (ECCV 2022)**: [Real-Time Intermediate Flow Estimation](https://github.com/megvii-research/ECCV2022-RIFE)
  - ⚡ **130+ FPS** on RTX 3090
  - 🎯 **State-of-the-art** interpolation quality
  - ✅ **Models Downloaded** (`external_models/ECCV2022-RIFE/`)

- **FILM (Google Research)**: [Frame Interpolation for Large Motion](https://github.com/google-research/frame-interpolation)
  - 🎭 **Large motion handling** for dramatic panel transitions
  - 🧠 **TensorFlow implementation** with pre-trained models
  - ✅ **Repository Integrated** (`external_models/frame-interpolation/`)

### **🔍 Object Detection & Analysis** 
- **YOLOv3**: Real-time object detection
  - 💬 **Speech bubble detection** and text region identification
  - 👥 **Character detection** for tracking across panels
  - ✅ **Config Ready** (`external_models/Yolo_Model/`)

### **🤗 Hugging Face Ecosystem**
```python
# Future community model integration
from comicframes import ModelFactory

# Load community-trained comic-specific models
speech_detector = ModelFactory.create_model("huggingface/comic-speech-detection")
character_classifier = ModelFactory.create_model("huggingface/comic-character-recognition")
style_interpolator = ModelFactory.create_model("huggingface/comic-style-preserving-interpolation")
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

### **🚀 Quick Start: From Comic to Animated Frames**

#### **Step 1: Basic Frame Detection (Works Now)**
```python
from comicframes import pdf_to_images, detect_frames

# Extract pages from comic PDF
pdf_to_images("watchmen.pdf", output_base_dir="./pages") 

# Detect panels using OpenCV computer vision
total_frames = detect_frames("./pages/page_1.png", 
                           min_width=100, 
                           detection_method="threshold")

print(f"Detected {total_frames} panels ready for animation")
```

#### **Step 2: Advanced Processing Pipeline**
```python
from comicframes.processing import PDFProcessor, FrameProcessor
from comicframes.core import ProcessingPipeline

# Create a complete comic processing pipeline
pipeline = ProcessingPipeline("comic_analysis")
pipeline.add_stage(PDFProcessor())      # PDF → Images
pipeline.add_stage(FrameProcessor())    # Images → Panel detection

# Process entire comic book
result = pipeline.process("comic.pdf")
print(f"Pipeline processed {len(result.data)} pages")
```

#### **Step 3: Performance & Caching**
```python
from comicframes import Settings, get_cache_manager

# Configure for optimal performance
settings = Settings(
    min_frame_width=75,      # Adjust for comic style
    min_frame_height=100,    # Filter out small panels
    enable_cache=True        # Cache processing results
)

# Monitor processing performance
cache = get_cache_manager()
stats = cache.get_cache_stats()
print(f"Cache hit ratio: {stats.hit_ratio:.2%}")
```

#### **Step 4: Neural Network Integration (Coming Soon)**
```python
# Future API - Neural network enhanced processing
from comicframes import ModelFactory
from comicframes.models import RIFEInterpolator, FILMInterpolator

# Load state-of-the-art interpolation models
rife = ModelFactory.create_model("rife_v4.6")      # 130+ FPS interpolation  
film = ModelFactory.create_model("film_net")       # Large motion handling

# Create smooth panel transitions
interpolated_frames = rife.interpolate_between_panels(
    panel_1="frame_001.png",
    panel_2="frame_002.png",
    transition_frames=8,        # 8 intermediate frames
    preserve_style=True         # Maintain comic art style
)
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

## 🗺️ **Development Roadmap: Building the Animation Future**

### **📈 Phase 1: Foundation ✅ (v0.1.0 - Current)**
**Status**: **Production Ready** - Solid computer vision foundation
- ✅ **PDF Processing**: PyMuPDF integration for high-quality page extraction
- ✅ **OpenCV Frame Detection**: Threshold & Canny edge detection algorithms
- ✅ **Processing Architecture**: Modular pipeline system with caching
- ✅ **CLI Tools**: 5 command-line utilities for batch processing
- ✅ **Developer Experience**: Type safety, documentation, testing framework

### **🚀 Phase 2: Neural Network Integration 🔄 (v0.2.0 - Q1 2024)**  
**Status**: **In Progress** - Models downloaded, API implementation ongoing
- 🔄 **RIFE Implementation**: Complete PyTorch model integration (models ready)
- 🔄 **FILM Implementation**: TensorFlow model wrapper development  
- 🔄 **YOLO Integration**: Object detection for speech bubbles and characters
- 🔄 **Model Management**: Enhanced ModelFactory with automatic downloading
- 🔄 **Performance Optimization**: GPU acceleration and batching support

### **🎬 Phase 3: Animation Generation 🎯 (v0.3.0 - Q2 2024)**
**Status**: **Planned** - Animation pipeline and export capabilities
- 🎯 **Frame Interpolation**: Smooth transitions between comic panels
- 🎯 **Animation Export**: MP4/GIF generation with customizable timing
- 🎯 **Transition Effects**: Multiple animation styles (smooth, cinematic, dynamic)
- 🎯 **Batch Animation**: Process entire comic books into animated sequences
- 🎯 **Quality Controls**: Resolution, frame rate, and compression options

### **🎮 Phase 4: Interactive Experiences 🔮 (v0.4.0 - Q3 2024)**
**Status**: **Future** - Advanced features and user interfaces
- 🔮 **Web Interface**: Browser-based comic animation viewer
- 🔮 **Speech Integration**: Text-to-speech with character voice synthesis
- 🔮 **Character Tracking**: Persistent character identification across panels
- 🔮 **Style Transfer**: Artistic style preservation during animation
- 🔮 **Interactive Timing**: User-controlled pacing and panel transitions

### **🌟 Phase 5: AI-Enhanced Storytelling 🔮 (v1.0.0 - Future)**
**Status**: **Visionary** - Advanced AI for narrative understanding  
- 🔮 **Story Analysis**: Automated narrative flow detection
- 🔮 **Emotion Detection**: Character emotional state recognition
- 🔮 **Scene Understanding**: Context-aware animation decisions
- 🔮 **Multi-language**: Global text extraction and voice synthesis
- 🔮 **Community Models**: Hugging Face Hub integration for specialized models

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
  author={ComicFrames Project},
  year={2024},
  url={https://github.com/pr1m8/comicframes},
  version={0.1.0},
  note={Foundation for neural network-based comic animation}
}
```

## 🔗 Related Projects

- [ECCV2022-RIFE](https://github.com/megvii-research/ECCV2022-RIFE) - Real-Time Intermediate Flow Estimation
- [frame-interpolation](https://github.com/google-research/frame-interpolation) - Google's FILM models
- [YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection framework
- [Hugging Face Hub](https://huggingface.co/models) - Model repository and hosting

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/pr1m8/comicframes?style=social)
![GitHub forks](https://img.shields.io/github/forks/pr1m8/comicframes?style=social)  
![GitHub issues](https://img.shields.io/github/issues/pr1m8/comicframes)
![GitHub pull requests](https://img.shields.io/github/issues-pr/pr1m8/comicframes)

## License

MIT License - see the [LICENSE](LICENSE) file for details.