from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_async_session
from app.api.deps import get_current_user
from app.models import User, Conversation, Message, ConversationState, MessageRole
from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    Conversation as ConversationSchema,
    ConversationWithMessages,
    ChatRequest,
    ChatResponse,
)

router = APIRouter()


@router.get("/conversations", response_model=list[ConversationSchema])
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """List all conversations for the current user."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
    )
    conversations = result.scalars().all()
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Get a specific conversation with messages."""
    result = await db.execute(
        select(Conversation)
        .where(
            Conversation.id == conversation_id, Conversation.user_id == current_user.id
        )
        .options(selectinload(Conversation.messages))
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    return conversation


@router.post("/conversations", response_model=ConversationSchema)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Create a new conversation."""
    conversation = Conversation(user_id=current_user.id, **conversation_data.dict())
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation


@router.patch("/conversations/{conversation_id}", response_model=ConversationSchema)
async def update_conversation(
    conversation_id: UUID,
    update_data: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Update a conversation."""
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id, Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(conversation, field, value)

    await db.commit()
    await db.refresh(conversation)
    return conversation


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Send a message and get a response."""
    # Get or create conversation
    if request.conversation_id:
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == request.conversation_id,
                Conversation.user_id == current_user.id,
            )
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=current_user.id, state=ConversationState.INITIAL_INTENT, context={}
        )
        db.add(conversation)
        await db.flush()

    # Add user message
    user_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=request.message,
        llm_metadata={},
    )
    db.add(user_message)
    await db.flush()

    # TODO: Process message with AI and get response
    # For now, return a mock response
    assistant_response = await _generate_mock_response(conversation, request.message)

    # Add assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=assistant_response["content"],
        llm_metadata=assistant_response.get("metadata", {}),
    )
    db.add(assistant_message)

    # Update conversation state if needed
    if assistant_response.get("new_state"):
        conversation.state = assistant_response["new_state"]

    if assistant_response.get("context_update"):
        conversation.context.update(assistant_response["context_update"])

    await db.commit()
    await db.refresh(assistant_message)
    await db.refresh(conversation)

    return ChatResponse(
        conversation_id=conversation.id,
        message=assistant_message,
        state=conversation.state,
        context=conversation.context,
    )


async def _generate_mock_response(conversation: Conversation, user_message: str):
    """Generate a mock AI response based on conversation state."""

    if conversation.state == ConversationState.INITIAL_INTENT:
        return {
            "content": (
                "I'd love to help you plan your trip! To get started, could you tell me:\n\n"
                "• Where are you thinking of going?\n"
                "• When would you like to travel?\n"
                "• Who's going with you?\n\n"
                "This will help me understand what kind of experience you're looking for!"
            ),
            "new_state": ConversationState.GATHERING_CONTEXT,
            "context_update": {"started": True},
            "metadata": {"model": "mock", "tokens": 0},
        }

    elif conversation.state == ConversationState.GATHERING_CONTEXT:
        return {
            "content": (
                "Great! That sounds wonderful. Let me ask a few more questions to better understand your preferences:\n\n"
                "• What's your approximate budget for this trip?\n"
                "• Are you more interested in relaxation or adventure?\n"
                "• Any specific activities or experiences you're hoping for?\n"
                "• Are there any dietary restrictions or accessibility needs I should know about?"
            ),
            "new_state": ConversationState.REFINING_PREFERENCES,
            "context_update": {"gathering_preferences": True},
            "metadata": {"model": "mock", "tokens": 0},
        }

    elif conversation.state == ConversationState.REFINING_PREFERENCES:
        return {
            "content": (
                "Perfect! Based on what you've told me, I have some great ideas for your trip. "
                "Let me put together a few options that match your preferences.\n\n"
                "I'll include:\n"
                "• Recommended accommodations\n"
                "• Must-see attractions and hidden gems\n"
                "• Restaurant suggestions\n"
                "• A rough itinerary\n\n"
                "Give me just a moment to prepare these options for you..."
            ),
            "new_state": ConversationState.PRESENTING_OPTIONS,
            "context_update": {"ready_for_options": True},
            "metadata": {"model": "mock", "tokens": 0},
        }

    else:
        return {
            "content": (
                "I understand! Let me help you with that. "
                "Could you provide more details about what you're looking for?"
            ),
            "metadata": {"model": "mock", "tokens": 0},
        }


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """Delete a conversation."""
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id, Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    await db.delete(conversation)
    await db.commit()

    return {"message": "Conversation deleted successfully"}
