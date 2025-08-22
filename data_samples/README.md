# Data Samples

This directory contains sample data and test files for ComicFrames development and testing.

## Contents

### Data/
Original data directory structure:
- **Augmented_Data/**: Processed comic data with extracted frames
  - `watchmen-ch.-1/`: Sample Watchmen comic chapter
    - `raw_image/`: Original page images extracted from PDF
    - `detected_frames/`: Pages with frame detection annotations
    - `frame_data/`: Individual extracted frame images
- **Train_Data/**: Source PDF files for processing
  - `watchmen-ch.-1.pdf`: Sample comic book PDF

### test_data/
Test files for development:
- Sample frame images
- Test cases for frame detection
- Validation data

## Usage

### With Legacy API
```python
from comicframes import pdf_to_images, extract_and_save_frames

# Process the sample PDF
pdf_to_images('data_samples/Data/Train_Data/watchmen-ch.-1.pdf')

# Extract frames from sample images
extract_and_save_frames(
    'data_samples/Data/Augmented_Data/watchmen-ch.-1/raw_image',
    'data_samples/Data/Augmented_Data/watchmen-ch.-1'
)
```

### With New Architecture
```python
from comicframes.processing import PDFProcessor, FrameProcessor
from comicframes.core import ProcessingPipeline

# Create pipeline
pipeline = ProcessingPipeline("sample_processing")
pipeline.add_stage(PDFProcessor())
pipeline.add_stage(FrameProcessor())

# Process sample data
result = pipeline.process('data_samples/Data/Train_Data/watchmen-ch.-1.pdf')
```

### CLI Usage
```bash
# Process sample PDF
comicframes-pipeline data_samples/Data/Train_Data/watchmen-ch.-1.pdf

# Extract frames from sample
comicframes-extract data_samples/Data/Augmented_Data/watchmen-ch.-1/raw_image ./output
```

## Data Structure

```
data_samples/Data/Augmented_Data/watchmen-ch.-1/
├── raw_image/           # Original page images (29 pages)
│   ├── comic_page_0.png
│   ├── comic_page_1.png
│   └── ...
├── detected_frames/     # Pages with detection overlays
│   ├── comic_page_0.png
│   └── ...
└── frame_data/         # Individual extracted frames (200+ frames)
    ├── page_0_frame_1_total_1.png
    ├── page_1_frame_1_total_2.png
    └── ...
```

## Note

This sample data is used for:
- Testing frame detection algorithms
- Validating processing pipelines  
- Performance benchmarking
- Development and debugging

The Watchmen sample provides good variety in:
- Panel layouts (regular grids, splash pages, irregular panels)
- Art styles (detailed artwork, varying contrast)
- Content types (character dialogue, action scenes, close-ups)
