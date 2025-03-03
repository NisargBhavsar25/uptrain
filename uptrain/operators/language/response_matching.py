"""
Implements operator to calculate the matching score between llm-generated response and ground_truth response.
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
class ResponseMatchingScore(ColumnOp):
    """
    Operator to compare the llm-generated text with the gold response using the defined score metric.

     Attributes:
        col_response (str): Column name for the llm generated responses
        col_ground_truth (str): Column name for the ground truth responses
        method (str): (Literal["rouge", "exact", "llm"]): Method to calculate the score

    Raises:
        Exception: Raises exception for any failed evaluation attempts

    """

    col_question: str = "question"
    col_response: str = "response"
    col_ground_truth: str = "ground_truth"
    method: str = t.Literal["exact", "rouge", "llm"]
    col_out: str = "score_response_match"
    scenario_description: t.Union[str, list[str], None] = None

    def setup(self, settings: t.Optional[Settings] = None):
        from uptrain.framework.remote import APIClient
        assert settings is not None
        if self.method not in ["exact", "rouge", "llm"]:
            raise Exception(f"Metric: {self.method} is not supported yet.")
        self._api_client = APIClient(settings)
        return self

    def run(self, data: pl.DataFrame) -> TYPE_TABLE_OUTPUT:
        data_send = polars_to_json_serializable_dict(data)
        for row in data_send:
            row["question"] = row.pop(self.col_question)
            row["response"] = row.pop(self.col_response)
            row["ground_truth"] = row.pop(self.col_ground_truth)

        try:
            results = self._api_client.evaluate(
                "ResponseMatching", data_send, {
                    "type": self.method,
                    "scenario_description": self.scenario_description            
                })

        except Exception as e:
            logger.error(f"Failed to run evaluation for `ResponseMatchingScore`: {e}")
            raise e

        assert results is not None
        return {"output": data.with_columns(pl.from_dicts(results).rename({"score_response_match": self.col_out}))}



@register_op
class ValidResponseScore(ColumnOp):
    """
    Operator to check if the response is valid is not.
     Attributes:
        col_response (str): Column name for the responses
        col_out (str): Column name for the output score

    Raises:
        Exception: Raises exception for any failed evaluation attempts

    """

    col_response: str = "response"
    col_out: str = "score_valid_response"
    scenario_description: t.Union[str, list[str], None] = None

    def setup(self, settings: t.Optional[Settings] = None):
        from uptrain.framework.remote import APIClient
        assert settings is not None
        self._api_client = APIClient(settings)
        return self

    def run(self, data: pl.DataFrame) -> TYPE_TABLE_OUTPUT:
        data_send = polars_to_json_serializable_dict(data)
        for row in data_send:
            row["response"] = row.pop(self.col_response)

        try:
            results = self._api_client.evaluate("valid_response", data_send, {"scenario_description": self.scenario_description})

        except Exception as e:
            logger.error(f"Failed to run evaluation for `ResponseMatchingScore`: {e}")
            raise e

        assert results is not None
        return {"output": data.with_columns(pl.from_dicts(results).rename({"score_valid_response": self.col_out}))}
