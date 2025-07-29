from enum import Enum
from typing import Union
from pydantic import BaseModel, Field


class CustomerMessageRequest(BaseModel):
    customer_id: str = Field(..., description="The ID of the customer")
    message: str = Field(..., description="The message from the customer")
    product: str = Field(..., description="The product the customer is interested in")


# Response schema
class TicketModel(BaseModel):
    id: str = Field(..., description="The ticket ID")
    title: str = Field(..., description="The title of the issue")
    severity: str = Field(..., description="The severity of the issue")
    affected_components: list[str] = Field(
        ..., description="The components affected by the issue"
    )
    reproduction_steps: list[str] = Field(
        ..., description="Steps to reproduce the issue"
    )
    priority: str = Field(..., description="The priority of the ticket")
    assigned_team: str = Field(..., description="The team assigned to the ticket")


class TicketResponse(BaseModel):
    ticket: TicketModel


class ProductRequirementModel(BaseModel):
    id: str = Field(..., description="The feature requirement ID")
    title: str = Field(..., description="The title of the feature")
    description: str = Field(..., description="Description of the feature")
    user_story: str = Field(..., description="User story for the feature")
    business_value: str = Field(
        ..., description="Business value (High/Medium/Low) with rationale"
    )
    complexity_estimate: str = Field(
        ..., description="Complexity estimate of the feature"
    )
    affected_components: list[str] = Field(
        ..., description="List of affected components"
    )
    status: str = Field(..., description="Current status of the feature requirement")


class ProductRequirementResponse(BaseModel):
    product_requirement: ProductRequirementModel


class InquiryCategory(str, Enum):
    account_management = "Account Management"
    billing = "Billing"
    usage_question = "Usage Question"
    other = "Other"


class SuggestedResource(BaseModel):
    title: str = Field(..., description="The name of the suggested resource")
    url: str = Field(..., description="The URL of the suggested resource")


class GeneralInquiryResponse(BaseModel):
    inquiry_category: InquiryCategory = Field(
        ..., description="The category of the inquiry"
    )
    requires_human_review: bool = Field(
        ..., description="Whether the inquiry requires human review"
    )
    suggested_resources: list[SuggestedResource] = Field(
        default_factory=list, description="A list of suggested resources"
    )


class MessageType(str, Enum):
    bug_report = "bug_report"
    feature_request = "feature_request"
    general_inquiry = "general_inquiry"


class MainResponse(BaseModel):
    message_type: MessageType = Field(
        ...,
        description="Type of the message: bug_report, feature_request, or general_inquiry",
    )
    confidence_score: float = Field(
        ..., description="Confidence score for the classification"
    )
    response_data: Union[
        TicketResponse, ProductRequirementResponse, GeneralInquiryResponse
    ] = Field(
        ..., description="The response data object, structure depends on message_type"
    )
    customer_response: str = Field(
        ..., description="Plain text response to the customer"
    )
