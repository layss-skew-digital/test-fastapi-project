import os
import json
import uuid
from typing import Union
from openai import OpenAI
from schamas import (
    CustomerMessageRequest,
    MainResponse,
    MessageType,
    TicketResponse,
    TicketModel,
    ProductRequirementResponse,
    ProductRequirementModel,
    GeneralInquiryResponse,
    InquiryCategory,
    SuggestedResource,
)


class CustomerSupportAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def classify_and_generate_response(
        self, request: CustomerMessageRequest
    ) -> MainResponse:
        """
        Classify customer message and generate appropriate structured response
        """
        # Step 1: Classify the message type
        message_type, confidence_score = self._classify_message_type(request.message)

        # Step 2: Generate response data based on classification
        response_data = self._generate_response_data(request, message_type)

        # Step 3: Generate customer response
        customer_response = self._generate_customer_response(
            request, message_type, response_data
        )

        return MainResponse(
            message_type=message_type,
            confidence_score=confidence_score,
            response_data=response_data,
            customer_response=customer_response,
        )

    def _classify_message_type(self, message: str) -> tuple[MessageType, float]:
        """
        Classify the message into bug_report, feature_request, or general_inquiry
        """
        prompt = f"""
        Analyze the following customer support message and classify it into one of three categories:
        
        Categories:
        1. bug_report - Issues, errors, problems, crashes, malfunctions
        2. feature_request - New features, improvements, enhancements, suggestions
        3. general_inquiry - Questions, account issues, billing, usage questions, general support
        
        Message: "{message}"
        
        Respond with a JSON object containing:
        - "classification": one of "bug_report", "feature_request", "general_inquiry"
        - "confidence_score": a float between 0.0 and 1.0
        - "reasoning": brief explanation of the classification
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        try:
            # try to parse the response as json
            result = json.loads(response.choices[0].message.content)
            return MessageType(result["classification"]), result["confidence_score"]
        except (json.JSONDecodeError, KeyError):
            # Fallback classification
            return MessageType.general_inquiry, 0.5

    def _generate_response_data(
        self, request: CustomerMessageRequest, message_type: MessageType
    ) -> Union[TicketResponse, ProductRequirementResponse, GeneralInquiryResponse]:
        """
        Generate structured response data based on message type
        """
        if message_type == MessageType.bug_report:
            return self._generate_bug_report_data(request)
        elif message_type == MessageType.feature_request:
            return self._generate_feature_request_data(request)
        else:
            return self._generate_general_inquiry_data(request)

    def _generate_bug_report_data(
        self, request: CustomerMessageRequest
    ) -> TicketResponse:
        """
        Generate structured bug report data
        """
        prompt = f"""
        Analyze this bug report message and extract structured information:
        
        Message: "{request.message}"
        Product: "{request.product}"
        
        Generate a JSON response with:
        - "title": concise issue title
        - "severity": "Low", "Medium", "High", or "Critical"
        - "affected_components": list of affected components
        - "reproduction_steps": list of steps to reproduce
        - "priority": "Low", "Medium", "High", or "Urgent"
        - "assigned_team": appropriate team name
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        try:
            data = json.loads(response.choices[0].message.content)
            ticket = TicketModel(
                id=f"BUG-{str(uuid.uuid4())[:4].upper()}",
                title=data["title"],
                severity=data["severity"],
                affected_components=data["affected_components"],
                reproduction_steps=data["reproduction_steps"],
                priority=data["priority"],
                assigned_team=data["assigned_team"],
            )
            return TicketResponse(ticket=ticket)
        except (json.JSONDecodeError, KeyError):
            # Fallback data
            ticket = TicketModel(
                id=f"BUG-{str(uuid.uuid4())[:4].upper()}",
                title="Bug Report",
                severity="Medium",
                affected_components=["General"],
                reproduction_steps=["Steps to reproduce not specified"],
                priority="Medium",
                assigned_team="Support Team",
            )
            return TicketResponse(ticket=ticket)

    def _generate_feature_request_data(
        self, request: CustomerMessageRequest
    ) -> ProductRequirementResponse:
        """
        Generate structured feature request data
        """
        prompt = f"""
        Analyze this feature request message and extract structured information:
        
        Message: "{request.message}"
        Product: "{request.product}"
        
        Generate a JSON response with:
        - "title": concise feature title
        - "description": detailed feature description
        - "user_story": user story format "As a [user], I want [feature] so that [benefit]"
        - "business_value": "High", "Medium", or "Low" with brief rationale
        - "complexity_estimate": "Low", "Medium", or "High"
        - "affected_components": list of components that would be affected
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        try:
            data = json.loads(response.choices[0].message.content)
            requirement = ProductRequirementModel(
                id=f"FR-{str(uuid.uuid4())[:4].upper()}",
                title=data["title"],
                description=data["description"],
                user_story=data["user_story"],
                business_value=data["business_value"],
                complexity_estimate=data["complexity_estimate"],
                affected_components=data["affected_components"],
                status="Under Review",
            )
            return ProductRequirementResponse(product_requirement=requirement)
        except (json.JSONDecodeError, KeyError):
            # Fallback data
            requirement = ProductRequirementModel(
                id=f"FR-{str(uuid.uuid4())[:4].upper()}",
                title="Feature Request",
                description="New feature requested by customer",
                user_story="As a user, I want this feature so that I can benefit from it",
                business_value="Medium - Customer requested feature",
                complexity_estimate="Medium",
                affected_components=["General"],
                status="Under Review",
            )
            return ProductRequirementResponse(product_requirement=requirement)

    def _generate_general_inquiry_data(
        self, request: CustomerMessageRequest
    ) -> GeneralInquiryResponse:
        """
        Generate structured general inquiry data
        """
        prompt = f"""
        Analyze this general inquiry message and classify it:
        
        Message: "{request.message}"
        Product: "{request.product}"
        
        Classify into one of these categories:
        - "Account Management" - account issues, login problems, profile changes
        - "Billing" - payment issues, subscription questions, pricing
        - "Usage Question" - how to use features, tutorials, guides
        - "Other" - anything else
        
        Also determine if it requires human review (true/false) and suggest 1-3 relevant resources.
        
        Respond with JSON:
        - "category": one of the categories above
        - "requires_human_review": boolean
        - "suggested_resources": list of objects with "title" and "url"
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        try:
            data = json.loads(response.choices[0].message.content)
            resources = [
                SuggestedResource(title=resource["title"], url=resource["url"])
                for resource in data.get("suggested_resources", [])
            ]

            return GeneralInquiryResponse(
                inquiry_category=InquiryCategory(data["category"]),
                requires_human_review=data["requires_human_review"],
                suggested_resources=resources,
            )
        except (json.JSONDecodeError, KeyError):
            # Fallback data
            return GeneralInquiryResponse(
                inquiry_category=InquiryCategory.other,
                requires_human_review=True,
                suggested_resources=[
                    SuggestedResource(
                        title="Help Center", url="https://help.example.com"
                    )
                ],
            )

    def _generate_customer_response(
        self,
        request: CustomerMessageRequest,
        message_type: MessageType,
        response_data: Union[
            TicketResponse, ProductRequirementResponse, GeneralInquiryResponse
        ],
    ) -> str:
        """
        Generate a friendly, helpful response to the customer
        """
        if message_type == MessageType.bug_report:
            ticket = response_data.ticket
            return f"""Thank you for reporting this issue. I've created a ticket (ID: {ticket.id}) and assigned it to our {ticket.assigned_team} team. They'll investigate this {ticket.severity.lower()} priority issue and get back to you soon. We appreciate you helping us improve our product!"""

        elif message_type == MessageType.feature_request:
            requirement = response_data.product_requirement
            return f"""Thank you for your feature request! I've logged this as requirement {requirement.id} and our product team will review it. We value your input and will consider this {requirement.business_value.lower()} business value feature for future updates. We'll keep you updated on the progress."""

        else:  # general_inquiry
            inquiry = response_data
            if inquiry.requires_human_review:
                return f"""Thank you for your inquiry about {request.product}. This requires personal attention, so I've escalated it to our support team. They'll get back to you within 24 hours. In the meantime, you might find these resources helpful: {', '.join([r.title for r in inquiry.suggested_resources])}."""
            else:
                return f"""Thank you for your question about {request.product}! I hope the information provided helps. If you need further assistance, don't hesitate to reach out again."""
