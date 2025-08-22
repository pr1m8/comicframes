"""Processing pipeline for chaining operations."""

from typing import List, Any, Dict, Optional, Callable
import time
import logging

from .base_processor import BaseProcessor
from .data_structures import ProcessingResult


logger = logging.getLogger(__name__)


class ProcessingPipeline:
    """Pipeline for chaining multiple processing operations."""
    
    def __init__(self, name: str = "pipeline"):
        """
        Initialize processing pipeline.
        
        Args:
            name: Name of the pipeline
        """
        self.name = name
        self.stages: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {}
    
    def add_stage(
        self, 
        processor: BaseProcessor, 
        name: Optional[str] = None,
        condition: Optional[Callable[[Any], bool]] = None,
        **kwargs
    ) -> "ProcessingPipeline":
        """
        Add a processing stage to the pipeline.
        
        Args:
            processor: Processor to add
            name: Optional name for the stage
            condition: Optional condition function to determine if stage should run
            **kwargs: Additional arguments to pass to the processor
            
        Returns:
            Self for method chaining
        """
        stage = {
            'processor': processor,
            'name': name or processor.name,
            'condition': condition,
            'kwargs': kwargs
        }
        self.stages.append(stage)
        return self
    
    def process(self, input_data: Any, **global_kwargs) -> ProcessingResult:
        """
        Execute the pipeline on input data.
        
        Args:
            input_data: Initial input data
            **global_kwargs: Global arguments passed to all stages
            
        Returns:
            ProcessingResult with final output and pipeline metrics
        """
        start_time = time.time()
        current_data = input_data
        stage_results = []
        
        try:
            for i, stage in enumerate(self.stages):
                stage_start_time = time.time()
                
                # Check condition if provided
                if stage['condition'] and not stage['condition'](current_data):
                    logger.debug(f"Skipping stage {i}: {stage['name']} (condition not met)")
                    continue
                
                # Merge global and stage-specific kwargs
                kwargs = {**global_kwargs, **stage['kwargs']}
                
                # Execute stage
                logger.debug(f"Executing stage {i}: {stage['name']}")
                result = stage['processor'].process(current_data, **kwargs)
                
                stage_time = time.time() - stage_start_time
                
                if result.success:
                    current_data = result.data
                    stage_results.append({
                        'stage': stage['name'],
                        'success': True,
                        'time': stage_time,
                        'cache_hit': result.cache_hit
                    })
                    logger.debug(f"Stage {i} completed in {stage_time:.2f}s")
                else:
                    # Pipeline fails if any stage fails
                    stage_results.append({
                        'stage': stage['name'],
                        'success': False,
                        'time': stage_time,
                        'error': str(result.error)
                    })
                    
                    total_time = time.time() - start_time
                    return ProcessingResult.error_result(
                        error=result.error,
                        processing_time=total_time,
                        message=f"Pipeline '{self.name}' failed at stage {i}: {stage['name']}",
                        metrics={'stage_results': stage_results}
                    )
            
            total_time = time.time() - start_time
            self._update_metrics(total_time, True, stage_results)
            
            return ProcessingResult.success_result(
                data=current_data,
                processing_time=total_time,
                message=f"Pipeline '{self.name}' completed successfully",
                metrics={
                    'stage_results': stage_results,
                    'total_stages': len(self.stages),
                    'executed_stages': len(stage_results)
                }
            )
            
        except Exception as e:
            total_time = time.time() - start_time
            self._update_metrics(total_time, False, stage_results)
            
            return ProcessingResult.error_result(
                error=e,
                processing_time=total_time,
                message=f"Pipeline '{self.name}' failed with unexpected error: {str(e)}",
                metrics={'stage_results': stage_results}
            )
    
    def _update_metrics(self, total_time: float, success: bool, stage_results: List[Dict]) -> None:
        """Update pipeline metrics."""
        if 'total_runs' not in self.metrics:
            self.metrics['total_runs'] = 0
            self.metrics['successful_runs'] = 0
            self.metrics['failed_runs'] = 0
            self.metrics['total_time'] = 0.0
            self.metrics['average_time'] = 0.0
        
        self.metrics['total_runs'] += 1
        self.metrics['total_time'] += total_time
        
        if success:
            self.metrics['successful_runs'] += 1
        else:
            self.metrics['failed_runs'] += 1
        
        self.metrics['average_time'] = self.metrics['total_time'] / self.metrics['total_runs']
        self.metrics['success_rate'] = self.metrics['successful_runs'] / self.metrics['total_runs']
        
        # Update stage-specific metrics
        for stage_result in stage_results:
            stage_name = stage_result['stage']
            if stage_name not in self.metrics:
                self.metrics[stage_name] = {
                    'runs': 0,
                    'successes': 0,
                    'total_time': 0.0,
                    'cache_hits': 0
                }
            
            stage_metrics = self.metrics[stage_name]
            stage_metrics['runs'] += 1
            stage_metrics['total_time'] += stage_result['time']
            
            if stage_result['success']:
                stage_metrics['successes'] += 1
            
            if stage_result.get('cache_hit'):
                stage_metrics['cache_hits'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get pipeline metrics."""
        return self.metrics.copy()
    
    def reset_metrics(self) -> None:
        """Reset pipeline metrics."""
        self.metrics.clear()
    
    def clear_cache(self) -> None:
        """Clear cache for all processors in the pipeline."""
        for stage in self.stages:
            stage['processor'].clear_cache()
    
    def get_stage_info(self) -> List[Dict[str, Any]]:
        """Get information about all stages in the pipeline."""
        return [
            {
                'name': stage['name'],
                'processor_type': type(stage['processor']).__name__,
                'has_condition': stage['condition'] is not None,
                'kwargs': stage['kwargs']
            }
            for stage in self.stages
        ]
