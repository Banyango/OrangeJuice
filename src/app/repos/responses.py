from pydantic import BaseModel, Field

class RepoResponseModel(BaseModel):
    name: str = Field(
        description="The name of the repository",
        example="example-repo"
    )