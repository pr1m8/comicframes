"""Command-line interface for the comicframes package."""

import argparse
import os
import sys
from pathlib import Path

# Legacy imports for backward compatibility
from .pdf_processor import pdf_to_images
from .frame_detector import extract_and_save_frames

# New architecture imports
from .processing import PDFProcessor, FrameProcessor
from .core import ProcessingPipeline
from .config import get_settings
from .cache import get_cache_manager


def pdf_to_images_cli():
    """CLI entry point for PDF to images conversion."""
    parser = argparse.ArgumentParser(description="Convert PDF comic book to images")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--output-dir", 
        help="Output directory (default: Data/Augmented_Data)",
        default=None
    )
    parser.add_argument(
        "--no-frame-detection",
        action="store_true",
        help="Skip automatic frame detection"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file '{args.pdf_path}' not found")
        sys.exit(1)
    
    try:
        output_dir = pdf_to_images(
            args.pdf_path, 
            args.output_dir, 
            detect_frames_enabled=not args.no_frame_detection
        )
        print(f"Successfully extracted images to: {output_dir}")
    except Exception as e:
        print(f"Error processing PDF: {e}")
        sys.exit(1)


def extract_frames_cli():
    """CLI entry point for frame extraction."""
    parser = argparse.ArgumentParser(description="Extract frames from comic page images")
    parser.add_argument("pages_dir", help="Directory containing comic page images")
    parser.add_argument("output_dir", help="Output directory for extracted frames")
    parser.add_argument(
        "--min-width", 
        type=int, 
        default=75, 
        help="Minimum frame width (default: 75)"
    )
    parser.add_argument(
        "--min-height", 
        type=int, 
        default=100, 
        help="Minimum frame height (default: 100)"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pages_dir):
        print(f"Error: Pages directory '{args.pages_dir}' not found")
        sys.exit(1)
    
    try:
        total_frames = extract_and_save_frames(
            args.pages_dir, 
            args.output_dir,
            args.min_width,
            args.min_height
        )
        print(f"Successfully extracted {total_frames} frames")
    except Exception as e:
        print(f"Error extracting frames: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Comics processing toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # PDF processing subcommand
    pdf_parser = subparsers.add_parser("pdf", help="Convert PDF to images")
    pdf_parser.add_argument("pdf_path", help="Path to the PDF file")
    pdf_parser.add_argument("--output-dir", help="Output directory")
    pdf_parser.add_argument("--no-frame-detection", action="store_true")
    
    # Frame extraction subcommand
    frames_parser = subparsers.add_parser("extract", help="Extract frames from images")
    frames_parser.add_argument("pages_dir", help="Directory containing comic pages")
    frames_parser.add_argument("output_dir", help="Output directory")
    frames_parser.add_argument("--min-width", type=int, default=75)
    frames_parser.add_argument("--min-height", type=int, default=100)
    
    args = parser.parse_args()
    
    if args.command == "pdf":
        pdf_to_images(args.pdf_path, args.output_dir, not args.no_frame_detection)
    elif args.command == "extract":
        extract_and_save_frames(args.pages_dir, args.output_dir, args.min_width, args.min_height)
    else:
        parser.print_help()


def pipeline_cli():
    """CLI entry point for processing pipeline."""
    parser = argparse.ArgumentParser(description="Run complete comic processing pipeline")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--min-width", type=int, default=75, help="Minimum frame width")
    parser.add_argument("--min-height", type=int, default=100, help="Minimum frame height")
    parser.add_argument("--model", help="Frame detection model to use")
    parser.add_argument("--disable-cache", action="store_true", help="Disable caching")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file '{args.pdf_path}' not found")
        sys.exit(1)
    
    try:
        # Create processors
        pdf_processor = PDFProcessor(cache_enabled=not args.disable_cache)
        frame_processor = FrameProcessor(
            model_name=args.model, 
            cache_enabled=not args.disable_cache
        )
        
        # Create pipeline
        pipeline = ProcessingPipeline("comic_processing")
        pipeline.add_stage(pdf_processor, name="pdf_extraction", output_base_dir=args.output_dir)
        pipeline.add_stage(
            frame_processor, 
            name="frame_detection",
            min_width=args.min_width,
            min_height=args.min_height
        )
        
        # Execute pipeline
        result = pipeline.process(args.pdf_path)
        
        if result.success:
            print(f"Pipeline completed successfully in {result.processing_time:.2f}s")
            print(f"Processed {len(result.data)} pages")
            
            # Print metrics
            metrics = result.metrics
            if metrics and 'stage_results' in metrics:
                print("\nStage Results:")
                for stage in metrics['stage_results']:
                    cache_status = " (cached)" if stage.get('cache_hit') else ""
                    print(f"  {stage['stage']}: {stage['time']:.2f}s{cache_status}")
        else:
            print(f"Pipeline failed: {result.message}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error running pipeline: {e}")
        sys.exit(1)


def cache_cli():
    """CLI entry point for cache management."""
    parser = argparse.ArgumentParser(description="Manage ComicFrames cache")
    subparsers = parser.add_subparsers(dest="action", help="Cache actions")
    
    # Stats command
    subparsers.add_parser("stats", help="Show cache statistics")
    
    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear cache")
    clear_parser.add_argument("--type", choices=["all", "frames", "models", "processing"],
                             default="all", help="Type of cache to clear")
    
    # Cleanup command
    subparsers.add_parser("cleanup", help="Clean up expired cache entries")
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        return
    
    cache_manager = get_cache_manager()
    
    if args.action == "stats":
        stats = cache_manager.get_cache_stats()
        print("Cache Statistics:")
        print("=" * 40)
        
        for cache_name, cache_stats in stats.items():
            print(f"\n{cache_name.replace('_', ' ').title()}:")
            for key, value in cache_stats.items():
                print(f"  {key}: {value}")
    
    elif args.action == "clear":
        if args.type == "all":
            cache_manager.clear_all()
            print("Cleared all caches")
        elif args.type == "frames" and cache_manager.frame_cache:
            cache_manager.frame_cache.clear()
            print("Cleared frame cache")
        elif args.type == "models" and cache_manager.model_cache:
            cache_manager.model_cache.clear()
            print("Cleared model cache")
        elif args.type == "processing" and cache_manager.processing_cache:
            cache_manager.processing_cache.clear()
            print("Cleared processing cache")
    
    elif args.action == "cleanup":
        cache_manager.cleanup_expired()
        print("Cleaned up expired cache entries")


def models_cli():
    """CLI entry point for model management."""
    parser = argparse.ArgumentParser(description="Manage ComicFrames models")
    subparsers = parser.add_subparsers(dest="action", help="Model actions")
    
    # List command
    subparsers.add_parser("list", help="List available models")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show model information")
    info_parser.add_argument("model_name", help="Name of the model")
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        return
    
    if args.action == "list":
        from .models import ModelFactory
        models = ModelFactory.list_available_models()
        
        print("Available Models:")
        print("=" * 50)
        
        for name, config in models.items():
            print(f"\n{name}:")
            print(f"  Type: {config['type']}")
            print(f"  Input Size: {config['input_size']}")
            if config['model_path']:
                print(f"  Path: {config['model_path']}")
            if config['download_url']:
                print(f"  Download URL: {config['download_url']}")
    
    elif args.action == "info":
        try:
            from .models import ModelFactory
            model = ModelFactory.create_model(args.model_name)
            info = model.get_model_info()
            
            print(f"Model Information: {args.model_name}")
            print("=" * 50)
            
            for key, value in info.items():
                print(f"{key}: {value}")
                
        except Exception as e:
            print(f"Error getting model info: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
