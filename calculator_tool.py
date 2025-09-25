from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from typing import Union

class CalculatorInput(BaseModel):
    a: int = Field(..., description="First number")
    b: int = Field(..., description="Second number")
    op: str = Field(..., description="Operations done are add, subtract, multiply, divide")

class CalculatorTool(StructuredTool):
    name: str = "calculator"
    description: str = "This tool performs a basic arithmetic operation between two numbers."
    args_schema: type[CalculatorInput] = CalculatorInput

    def _run(self, a: int, b: int, op: str) -> Union[int, float]:
        if op == "add":
            return a + b
        elif op == "subtract":
            return a - b
        elif op == "multiply":
            return a * b
        elif op == "divide":
            return a / b
        else:
            return "The agent cannot do further calculation"
# @tool
# def add(a: int, b: int) -> int:
#     """Add two numbers."""
#     return a + b

# @tool
# def subtract(a: int, b: int) -> int:
#     """Subtract two numbers."""
#     return a - b

# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b

# @tool
# def divide(a: int, b: int) -> Union[int, float]:
#     """Divide two numbers."""
#     return a / b


# print(multiply.name)
# print(multiply.description)
# print(multiply.args)
