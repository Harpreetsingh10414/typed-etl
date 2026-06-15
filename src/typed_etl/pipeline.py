from collections.abc import Callable
from pathlib import Path
from time import perf_counter

import polars as pl

from typed_etl.exceptions import PipelineExecutionError
from typed_etl.file_reader import read_file
from typed_etl.logger import get_logger
from typed_etl.models import ValidationConfig
from typed_etl.validator import validate_dataframe
from typed_etl.writer import write_file

Transformation = Callable[
    [pl.DataFrame],
    pl.DataFrame,
]


class ETLPipeline:
    """
    End-to-end ETL pipeline.
    """

    def __init__(
        self,
        input_path: str | Path,
        output_path: str | Path,
        validation_config: ValidationConfig | None = None,
        overwrite: bool = False,
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.validation_config = validation_config
        self.overwrite = overwrite

        self.transformations: list[Transformation] = []

    def add_transformation(
        self,
        transformation: Transformation,
    ) -> None:
        """
        Register transformation.
        """

        self.transformations.append(transformation)

    def run(self) -> pl.DataFrame:
        """
        Execute ETL pipeline.
        """

        logger = get_logger()

        start_time = perf_counter()

        logger.info(
            "pipeline_started",
            input_path=str(self.input_path),
            output_path=str(self.output_path),
        )

        try:
            df = read_file(
                self.input_path,
            )

            if self.validation_config is not None:
                validate_dataframe(
                    df,
                    self.validation_config,
                )

            for index, transformation in enumerate(
                self.transformations,
                start=1,
            ):
                logger.info(
                    "transformation_started",
                    step=index,
                    name=transformation.__name__,
                )

                df = transformation(df)

                logger.info(
                    "transformation_completed",
                    step=index,
                    rows=df.height,
                    columns=df.width,
                )

            write_file(
                df,
                self.output_path,
                overwrite=self.overwrite,
            )

            duration = perf_counter() - start_time

            logger.info(
                "pipeline_completed",
                duration_seconds=round(
                    duration,
                    3,
                ),
                rows=df.height,
                columns=df.width,
            )

            return df

        except Exception as exc:
            logger.exception(
                "pipeline_failed",
                error=str(exc),
            )

            raise PipelineExecutionError(str(exc)) from exc
