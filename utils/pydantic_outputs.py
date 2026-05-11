from pydantic import BaseModel, Field


class TemplateOutput(BaseModel):
    template: str = Field(description="Angular HTML template of the translated component")


class TypeScriptComponentOutput(BaseModel):
    template: str = Field(description="Angular HTML template of the translated component")
    component: str = Field(
        description="Standalone Angular Typescript component implementing the logic of translated view")


class ViewGenerationOutput(BaseModel):
    template: str = Field(description="Angular HTML template of the translated component")
    component: str = Field(
        description="Standalone Angular Typescript component implementing the logic of translated view")
    styling: str = Field(
        description="SCSS styling to apply to the generated component as similar as possible to the styling of source view")
