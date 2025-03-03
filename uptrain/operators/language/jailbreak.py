"""
Implements operators related to jailbreaking of LLMs
"""

from __future__ import annotations
import typing as t

from loguru import logger
import polars as pl

if t.TYPE_CHECKING:
    from uptrain.framework import Settings
from uptrain.operators.base import *
from uptrain.utilities import polars_to_json_serializable_dict

@register_op
class JailbreakDetectionScore(ColumnOp):
    """
    Operator to check whether the user is trying to jailbreak the LLM.

    Attributes:
        col_question (str): Column name for the questions
        model_purpose (str): The purpose of the LLM

    Raises:
        Exception: Raises exception for any failed evaluation attempts

    """

    col_question: str = "question"
    model_purpose: str = "To help the user with its queries while preventing responses for any illegal, immoral or abusive requests."
    col_out: str = "score_jailbreak_attempted"

    def setup(self, settings: t.Optional[Settings] = None):
        from uptrain.framework.remote import APIClient
        assert settings is not None
        self._api_client = APIClient(settings)
        return self

    def run(self, data: pl.DataFrame) -> TYPE_TABLE_OUTPUT:
        data_send = polars_to_json_serializable_dict(data)
        for row in data_send:
            row["question"] = row.pop(self.col_question)

        try:
            results = self._api_client.evaluate(
                "JailbreakDetection", data_send, {
                    "model_purpose": self.model_purpose
                })

        except Exception as e:
            logger.error(f"Failed to run evaluation for `JailbreakDetectionScore`: {e}")
            raise e

        assert results is not None
        return {"output": data.with_columns(pl.from_dicts(results).rename({"score_jailbreak_attempted": self.col_out}))}

