"""
Advanced usage examples for the new ComicFrames architecture.
"""

from pathlib import Path
from comicframes import (
    Settings, get_settings, set_settings,
    CacheManager, get_cache_manager,
    Frame, ComicPage, ProcessingResult,
    ModelFactory
)
from comicframes.processing import PDFProcessor, FrameProcessor
from comicframes.core import ProcessingPipeline
from comicframes.config import ModelType


def example_configuration():
    """Example of custom configuration."""
    print("=== Configuration Example ===")
    
    # Get current settings
    settings = get_settings()
    print(f"Default cache dir: {settings.cache_dir}")
    print(f"Default min frame size: {settings.min_frame_width}x{settings.min_frame_height}")
    
    # Create custom settings
    custom_settings = Settings(
        project_root=Path.cwd(),
        min_frame_width=100,
        min_frame_height=150,
        enable_cache=True,
        device="cpu"
    )
    
    set_settings(custom_settings)
    print(f"Updated min frame size: {custom_settings.min_frame_width}x{custom_settings.min_frame_height}")


def example_caching():
    """Example of cache management."""
    print("\n=== Caching Example ===")
    
    cache_manager = get_cache_manager()
    
    # Store some data in different caches
    cache_manager.set_frame_data("test_frame", {"width": 100, "height": 200})
    cache_manager.set_processing_data("test_process", [1, 2, 3, 4, 5])
    cache_manager.set_memory_data("test_memory", "Hello, World!")
    
    # Retrieve data
    frame_data = cache_manager.get_frame_data("test_frame")
    process_data = cache_manager.get_processing_data("test_process")
    memory_data = cache_manager.get_memory_data("test_memory")
    
    print(f"Frame data: {frame_data}")
    print(f"Process data: {process_data}")
    print(f"Memory data: {memory_data}")
    
    # Get cache statistics
    stats = cache_manager.get_cache_stats()
    print(f"Cache stats: {stats}")


def example_models():
    """Example of model management."""
    print("\n=== Models Example ===")
    
    # List available models
    models = ModelFactory.list_available_models()
    print("Available models:")
    for name, config in models.items():
        print(f"  {name}: {config['type']}")
    
    # Create a frame detection model
    try:
        detector = ModelFactory.create_default_model(ModelType.FRAME_DETECTION)
        print(f"Created detector: {detector.model_name}")
        
        # Load the model
        load_result = detector.load()
        print(f"Model load result: {load_result.success}")
        
        # Get model info
        info = detector.get_model_info()
        print(f"Model info: {info}")
        
    except Exception as e:
        print(f"Model example failed: {e}")


def example_processing_pipeline():
    """Example of using processing pipeline."""
    print("\n=== Processing Pipeline Example ===")
    
    # Check if test PDF exists
    pdf_path = "data_samples/Data/Train_Data/watchmen-ch.-1.pdf"
    if not Path(pdf_path).exists():
        print(f"Test PDF not found: {pdf_path}")
        print("Create a sample PDF or update the path to run this example")
        return
    
    try:
        # Create processors
        pdf_processor = PDFProcessor(cache_enabled=True)
        frame_processor = FrameProcessor(cache_enabled=True)
        
        # Create pipeline
        pipeline = ProcessingPipeline("comic_processing_example")
        pipeline.add_stage(pdf_processor, name="pdf_extraction")
        pipeline.add_stage(frame_processor, name="frame_detection", save_frames=True)
        
        # Execute pipeline
        print(f"Processing {pdf_path}...")
        result = pipeline.process(pdf_path)
        
        if result.success:
            pages = result.data
            print(f"Successfully processed {len(pages)} pages")
            print(f"Total processing time: {result.processing_time:.2f}s")
            
            # Show frame counts per page
            total_frames = 0
            for page in pages:
                frame_count = len(page.frames)
                total_frames += frame_count
                print(f"  Page {page.page_number}: {frame_count} frames")
            
            print(f"Total frames detected: {total_frames}")
            
            # Show pipeline metrics
            metrics = pipeline.get_metrics()
            print(f"Pipeline metrics: {metrics}")
            
        else:
            print(f"Pipeline failed: {result.message}")
            
    except Exception as e:
        print(f"Pipeline example failed: {e}")


def example_custom_processor():
    """Example of creating a custom processor."""
    print("\n=== Custom Processor Example ===")
    
    from comicframes.core.base_processor import BaseProcessor
    import time
    
    class TextDetectionProcessor(BaseProcessor):
        """Custom processor for detecting text in frames."""
        
        def __init__(self):
            super().__init__("text_detector", cache_enabled=True)
        
        def _process(self, comic_page: ComicPage) -> ComicPage:
            """Detect text in all frames of a page."""
            # Simulate text detection processing
            time.sleep(0.1)  # Simulate processing time
            
            for frame in comic_page.frames:
                # Simple text detection simulation
                frame.has_text = frame.bbox.area > 5000  # Larger frames likely have text
                frame.metadata['text_confidence'] = 0.8 if frame.has_text else 0.2
            
            return comic_page
    
    # Create test data
    test_page = ComicPage(page_number=1)
    test_page.frames = [
        Frame(bbox=type('BBox', (), {'area': 10000})(), frame_number=1),
        Frame(bbox=type('BBox', (), {'area': 3000})(), frame_number=2),
        Frame(bbox=type('BBox', (), {'area': 8000})(), frame_number=3),
    ]
    
    # Process with custom processor
    text_processor = TextDetectionProcessor()
    result = text_processor.process(test_page)
    
    if result.success:
        processed_page = result.data
        print("Text detection results:")
        for frame in processed_page.frames:
            print(f"  Frame {frame.frame_number}: has_text={frame.has_text}")
    
    # Show processor metrics
    metrics = text_processor.get_metrics()
    print(f"Custom processor metrics: {metrics}")


def main():
    """Run all examples."""
    print("ComicFrames Advanced Usage Examples")
    print("=" * 50)
    
    try:
        example_configuration()
        example_caching()
        example_models()
        example_processing_pipeline()
        example_custom_processor()
        
        print("\n=== All examples completed! ===")
        
    except Exception as e:
        print(f"Example failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
