import tempfile
from io import BytesIO
from pathlib import Path

import polars as pl
import streamlit as st

from typed_etl import (
    ETLPipeline,
    drop_duplicates,
    fill_nulls,
)

st.set_page_config(
    page_title="Typed ETL Demo",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Typed ETL Demo")

st.markdown(
    """
Upload a CSV file and run a complete ETL pipeline.

Features:
- Remove duplicates
- Fill null values
- Rename columns
- Type casting
- Download processed output
"""
)

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"],
)

if uploaded_file:
    st.success("File uploaded successfully!")

    input_df = pl.read_csv(uploaded_file)

    st.subheader("Raw Data")

    st.dataframe(
        input_df.to_pandas(),
        use_container_width=True,
    )

    if st.button("Run ETL Pipeline"):
        with st.spinner("Running ETL pipeline..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = Path(tmpdir) / "input.csv"

                output_path = Path(tmpdir) / "output.csv"

                input_df.write_csv(input_path)

                pipeline = ETLPipeline(
                    input_path=input_path,
                    output_path=output_path,
                    overwrite=True,
                )

                def clean_duplicates(
                    df: pl.DataFrame,
                ) -> pl.DataFrame:
                    first_column = df.columns[0]

                    return drop_duplicates(
                        df,
                        subset=[first_column],
                    )

                def fill_missing(
                    df: pl.DataFrame,
                ) -> pl.DataFrame:
                    values = {}

                    for col, dtype in df.schema.items():
                        if dtype == pl.String:
                            values[col] = "Unknown"

                    if values:
                        return fill_nulls(
                            df,
                            values,
                        )

                    return df

                pipeline.add_transformation(clean_duplicates)

                pipeline.add_transformation(fill_missing)

                result = pipeline.run()

                st.success("Pipeline completed!")

                st.subheader("Processed Data")

                st.dataframe(
                    result.to_pandas(),
                    use_container_width=True,
                )

                csv_bytes = result.write_csv().encode("utf-8")

                st.download_button(
                    "Download Processed CSV",
                    csv_bytes,
                    file_name="processed.csv",
                    mime="text/csv",
                )

                parquet_buffer = BytesIO()

                result.write_parquet(parquet_buffer)

                st.download_button(
                    "Download Parquet",
                    parquet_buffer.getvalue(),
                    file_name="processed.parquet",
                    mime="application/octet-stream",
                )
