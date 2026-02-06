"""
Base Pipeline Step

Why this exists:
- Enforces a consistent interface for all pipeline steps
- Makes the pipeline composable and testable
- Prevents ad-hoc step implementations
"""


class PipelineStep:
    """
    Abstract base class for all pipeline steps.
    """

    def run(self, *args, **kwargs):
        """
        Execute the pipeline step.

        All subclasses must implement this method.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement the run() method"
        )
