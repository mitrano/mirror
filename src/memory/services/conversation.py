"""ConversationService: conversation lifecycle and automatic extraction."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from memory.config import LOG_LLM_CALLS, SUMMARIZE_ENABLED, TWO_PASS_ENABLED
from memory.intelligence.embeddings import embedding_to_bytes, generate_embedding
from memory.intelligence.extraction import (
    curate_against_existing,
    extract_memories,
    extract_tasks,
    generate_conversation_summary,
    generate_conversation_title,
)
from memory.intelligence.llm_router import LLMResponse
from memory.models import Conversation, ConversationSummary, Memory, Message
from memory.storage.store import Store

if TYPE_CHECKING:
    from memory.services.memory import MemoryService
    from memory.services.tasks import TaskService


def _naive_summary(messages: list[Message]) -> str:
    """Fallback summary: first 2000 chars of joined message content."""
    parts = [msg.content[:500] for msg in messages if msg.role in ("user", "assistant")]
    return " ".join(parts)[:2000]


class ConversationService:
    def __init__(
        self,
        store: Store,
        memories: MemoryService,
        tasks: TaskService | None = None,
    ) -> None:
        self.store = store
        self.memories = memories
        if tasks is None:
            raise TypeError("ConversationService requires tasks")
        self.tasks: TaskService = tasks

    def start_conversation(
        self,
        interface: str,
        persona: str | None = None,
        journey: str | None = None,
        title: str | None = None,
    ) -> Conversation:
        """Start a new conversation."""
        conv = Conversation(
            interface=interface,
            persona=persona,
            journey=journey,
            title=title,
        )
        return self.store.create_conversation(conv)

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        token_count: int | None = None,
    ) -> Message:
        """Add a message to an existing conversation."""
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            token_count=token_count,
        )
        return self.store.add_message(msg)

    def find_by_id_prefix(self, prefix: str) -> Conversation | None:
        """Return the latest conversation whose id starts with prefix."""
        return self.store.find_conversation_by_id_prefix(prefix)

    def suggest_title(self, conversation_id: str) -> str:
        """Suggest a title for one conversation without saving it."""
        conversation = self._get_conversation_for_title_operation(conversation_id)
        messages = self.store.get_messages(conversation.id)
        if not messages:
            raise ValueError("Conversation has no messages to title")

        suggestion = generate_conversation_title(
            messages,
            on_llm_call=self._make_logger("conversation_title", conversation.id),
        )
        if not suggestion:
            raise ValueError("No title suggestion was generated")
        return self._clean_title(suggestion)

    def dry_run_metadata_lifecycle(self, conversation_id: str) -> dict:
        """Report conversation metadata lifecycle decisions without saving changes."""
        conversation = self._get_conversation_for_title_operation(conversation_id)
        messages = self.store.get_messages(conversation.id)
        metadata = self._metadata_dict(conversation)
        title_report = self._dry_run_title_lifecycle(conversation, messages, metadata)
        summary_report = self._dry_run_summary_lifecycle(conversation, messages)
        tags_report = self._dry_run_tags_lifecycle(conversation, messages)
        return {
            "conversation_id": conversation.id,
            "mode": "dry_run",
            "mutated": False,
            "metadata_lifecycle_version": 1,
            "fields": {
                "title": title_report,
                "summary": summary_report,
                "tags": tags_report,
            },
        }

    def update_title(self, conversation_id: str, title: str) -> Conversation:
        """Update a conversation title through a bounded manual-edit path."""
        if not isinstance(title, str):
            raise ValueError("title must be a string")
        clean_title = self._clean_title(title)
        conversation = self._get_conversation_for_title_operation(conversation_id)
        metadata = self._title_metadata(
            conversation,
            source="manual",
            status="manual",
            previous_title=conversation.title,
        )
        self.store.update_conversation(
            conversation.id,
            title=clean_title,
            metadata=json.dumps(metadata, ensure_ascii=False),
        )
        updated = self.store.get_conversation(conversation.id)
        if updated is None:
            raise ValueError(f"Conversation '{conversation_id}' not found")
        return updated

    def set_provisional_title(self, conversation_id: str, title: str) -> Conversation:
        """Set a first-message title that may later be improved automatically."""
        clean_title = self._clean_title(title)
        conversation = self._get_conversation_for_title_operation(conversation_id)
        metadata = self._title_metadata(
            conversation,
            source="first_user",
            status="provisional",
            previous_title=conversation.title,
        )
        self.store.update_conversation(
            conversation.id,
            title=clean_title,
            metadata=json.dumps(metadata, ensure_ascii=False),
        )
        updated = self.store.get_conversation(conversation.id)
        if updated is None:
            raise ValueError(f"Conversation '{conversation_id}' not found")
        return updated

    def _get_conversation_for_title_operation(self, conversation_id: str) -> Conversation:
        if not isinstance(conversation_id, str) or not conversation_id.strip():
            raise ValueError("conversationId is required")
        conversation = self.store.get_conversation(conversation_id)
        if conversation is None:
            conversation = self.store.find_conversation_by_id_prefix(conversation_id)
        if conversation is None:
            raise ValueError(f"Conversation '{conversation_id}' not found")
        return conversation

    def _clean_title(self, title: str) -> str:
        clean_title = " ".join(title.strip().split())
        if not clean_title:
            raise ValueError("title is required")
        if len(clean_title) > 160:
            raise ValueError("title must be at most 160 characters")
        return clean_title

    def list_recent(
        self,
        *,
        limit: int = 20,
        journey: str | None = None,
        persona: str | None = None,
    ) -> list[ConversationSummary]:
        """Return recent conversation summaries with optional filters."""
        return self.store.list_recent_conversation_summaries(
            limit=limit,
            journey=journey,
            persona=persona,
        )

    def end_conversation(
        self,
        conversation_id: str,
        extract: bool = True,
    ) -> list[Memory]:
        """End a conversation, extract memories/tasks, generate embeddings, and store them."""
        from memory.models import _now

        self.store.update_conversation(conversation_id, ended_at=_now())
        self.maybe_generate_title(conversation_id)

        if not extract:
            return []

        return self._run_extraction(conversation_id)

    def maybe_generate_title(
        self, conversation_id: str, *, source: str = "llm_auto"
    ) -> Conversation | None:
        """Generate and persist a better title when the current title is safe to replace."""
        conversation = self.store.get_conversation(conversation_id)
        if conversation is None or not self.title_needs_improvement(conversation):
            return conversation
        messages = self.store.get_messages(conversation.id)
        if not self._messages_are_titleable(messages):
            return conversation
        try:
            suggestion = generate_conversation_title(
                messages,
                on_llm_call=self._make_logger("conversation_title", conversation.id),
            )
            if not suggestion:
                return conversation
            clean_title = self._clean_title(suggestion)
            metadata = self._title_metadata(
                conversation,
                source=source,
                status="generated",
                previous_title=conversation.title,
            )
            self.store.update_conversation(
                conversation.id,
                title=clean_title,
                metadata=json.dumps(metadata, ensure_ascii=False),
            )
            return self.store.get_conversation(conversation.id)
        except Exception:
            return conversation

    def extract_conversation(self, conversation_id: str) -> list[Memory]:
        """Extract memories from an already-ended conversation."""
        return self._run_extraction(conversation_id)

    def _make_logger(self, role: str, conversation_id: str):
        if not LOG_LLM_CALLS:
            return None

        def _log(response: LLMResponse) -> None:
            self.store.log_llm_call(
                role=role,
                model=response.model,
                prompt=response.prompt or "",
                response_text=response.content,
                prompt_tokens=response.prompt_tokens,
                completion_tokens=response.completion_tokens,
                latency_ms=response.latency_ms,
                conversation_id=conversation_id,
            )

        return _log

    def _run_extraction(self, conversation_id: str) -> list[Memory]:
        """Run memory/task extraction. Marks metadata.extracted=True on success."""
        conv = self.store.get_conversation(conversation_id)
        messages = self.store.get_messages(conversation_id)

        # Extraction requires a journey and at least 4 messages.
        if not messages or not conv or not conv.journey or len(messages) < 4:
            return []

        # Load the user's first name for the transcript when available.
        user_name = "User"
        try:
            import re

            user_identity = self.store.get_identity("user", "identity")
            if user_identity and user_identity.content:
                match = re.search(
                    r"(?:You are talking to|Você está falando com) ([A-Z][a-zA-Záéíóúãõ]+)",
                    user_identity.content,
                )
                if match:
                    user_name = match.group(1)
        except Exception:
            pass

        # Extract memories through the LLM (candidate pass).
        extracted = extract_memories(
            messages,
            persona=conv.persona if conv else None,
            journey=conv.journey if conv else None,
            user_name=user_name,
            on_llm_call=self._make_logger("extraction", conversation_id),
        )

        # Curation pass: deduplicate candidates against existing memories.
        if TWO_PASS_ENABLED and extracted:
            similar: list[Memory] = []
            seen_ids: set[str] = set()
            for candidate in extracted:
                query = f"{candidate.title} {candidate.content[:60]}"
                results = self.memories.search(query, limit=3, journey=conv.journey)
                for sr in results:
                    if sr.memory.id not in seen_ids:
                        similar.append(sr.memory)
                        seen_ids.add(sr.memory.id)
            similar = similar[:15]  # Cap context size.
            extracted = curate_against_existing(
                extracted,
                similar,
                on_llm_call=self._make_logger("curation", conversation_id),
            )

        # Extract tasks through the LLM.
        try:
            extracted_tasks = extract_tasks(
                messages,
                journey=conv.journey if conv else None,
                user_name=user_name,
                on_llm_call=self._make_logger("task_extraction", conversation_id),
            )
            for et in extracted_tasks:
                existing = self.tasks.find_tasks(et.title, et.journey)
                if not existing:
                    self.tasks.add_task(
                        title=et.title,
                        journey=et.journey,
                        due_date=et.due_date,
                        stage=et.stage,
                        context=et.context,
                        source="conversation",
                    )
        except Exception:
            pass  # Task extraction failure should not block memory extraction.

        # Generate a conversation summary for embedding and storage.
        if SUMMARIZE_ENABLED:
            summary_text = generate_conversation_summary(
                messages,
                user_name=user_name,
                on_llm_call=self._make_logger("summary", conversation_id),
            )
            if not summary_text:
                summary_text = _naive_summary(messages)
        else:
            summary_text = _naive_summary(messages)

        if summary_text:
            summary_emb = generate_embedding(summary_text)
            self.store.store_conversation_embedding(
                conversation_id, embedding_to_bytes(summary_emb)
            )
            self.store.update_conversation(conversation_id, summary=summary_text[:1000])

        # Persist extracted memories with embeddings.
        stored_memories = []
        for ext in extracted:
            stored = self.memories.add_memory(
                title=ext.title,
                content=ext.content,
                memory_type=ext.memory_type,
                layer=ext.layer,
                context=ext.context,
                journey=ext.journey,
                persona=ext.persona,
                tags=ext.tags,
                conversation_id=conversation_id,
            )
            stored_memories.append(stored)

        # Mark as extracted so extract_pending skips this conversation.
        meta = self._metadata_dict(conv)
        meta["extracted"] = True
        self.store.update_conversation(
            conversation_id, metadata=json.dumps(meta, ensure_ascii=False)
        )

        return stored_memories

    def title_needs_improvement(self, conversation: Conversation) -> bool:
        """Return True when the title is missing or known to be low quality."""
        metadata = self._metadata_dict(conversation)
        if metadata.get("title_status") == "manual" or metadata.get("title_source") == "manual":
            return False
        title = (conversation.title or "").strip()
        if not title:
            return True
        if metadata.get("title_status") == "provisional":
            return True
        if title.endswith("...") or "..." in title:
            return True
        if len(title) >= 55:
            return True
        if title.lower().startswith("<skill"):
            return True
        return False

    def _messages_are_titleable(self, messages: list[Message]) -> bool:
        has_user = any(msg.role == "user" and msg.content.strip() for msg in messages)
        has_assistant = any(msg.role == "assistant" and msg.content.strip() for msg in messages)
        return has_user and has_assistant

    def _dry_run_title_lifecycle(
        self,
        conversation: Conversation,
        messages: list[Message],
        metadata: dict,
    ) -> dict:
        title = (conversation.title or "").strip()
        lock_state = "manual_locked" if self._title_is_manual(metadata) else "unlocked"
        if lock_state == "manual_locked":
            return {
                "decision": "preserve",
                "reason": "manual title lock is preserved",
                "current_value": title or None,
                "readiness": "locked",
                "provenance": metadata.get("title_source") or "manual",
                "lock_state": lock_state,
            }
        if not self._messages_are_titleable(messages):
            return {
                "decision": "defer",
                "reason": "conversation needs at least one user and one assistant message",
                "current_value": title or None,
                "readiness": "not_ready",
                "provenance": metadata.get("title_source"),
                "lock_state": lock_state,
            }
        confidence = None
        if not title:
            decision = "create"
            reason = "conversation has no title"
        elif self.title_needs_improvement(conversation):
            decision = "repair"
            reason = "current title is provisional or weak"
        else:
            refinement_evidence = self._title_refinement_evidence(conversation)
            if refinement_evidence:
                return {
                    "decision": "refine_candidate",
                    "reason": "later evidence is more specific than the current unlocked title",
                    "current_value": title or None,
                    "readiness": "ready",
                    "provenance": metadata.get("title_source"),
                    "lock_state": lock_state,
                    "confidence": refinement_evidence["confidence"],
                    "evidence": refinement_evidence,
                }
            if self._title_may_need_coherence_refinement(conversation, messages, metadata):
                decision = "refine_candidate"
                reason = "conversation has enough later context for coherence refinement"
                confidence = "low"
            else:
                decision = "keep"
                reason = "current title appears usable"
                confidence = None
        report = {
            "decision": decision,
            "reason": reason,
            "current_value": title or None,
            "readiness": "ready",
            "provenance": metadata.get("title_source"),
            "lock_state": lock_state,
        }
        if confidence:
            report["confidence"] = confidence
        return report

    def _dry_run_summary_lifecycle(
        self, conversation: Conversation, messages: list[Message]
    ) -> dict:
        if (conversation.summary or "").strip():
            return {
                "decision": "keep",
                "reason": "summary already exists",
                "current_value": conversation.summary,
                "readiness": "ready",
                "provenance": "stored",
            }
        substantive_messages = [
            msg for msg in messages if msg.role in ("user", "assistant") and msg.content.strip()
        ]
        if len(substantive_messages) >= 4:
            return {
                "decision": "create",
                "reason": "conversation has enough substance for a summary",
                "current_value": None,
                "readiness": "ready",
                "provenance": None,
            }
        return {
            "decision": "defer",
            "reason": "summary needs more conversation substance",
            "current_value": None,
            "readiness": "not_ready",
            "provenance": None,
        }

    def _dry_run_tags_lifecycle(self, conversation: Conversation, messages: list[Message]) -> dict:
        current_tags = conversation.tags
        if current_tags:
            return {
                "decision": "keep",
                "reason": "tags already exist",
                "current_value": current_tags,
                "readiness": "ready",
                "provenance": "stored",
            }
        if (conversation.summary or "").strip():
            return {
                "decision": "create",
                "reason": "summary-level substance is available for tags",
                "current_value": None,
                "readiness": "ready",
                "provenance": None,
            }
        return {
            "decision": "defer",
            "reason": "tags depend on summary-level substance",
            "current_value": None,
            "readiness": "not_ready",
            "provenance": None,
        }

    def _title_is_manual(self, metadata: dict) -> bool:
        return metadata.get("title_status") == "manual" or metadata.get("title_source") == "manual"

    def _title_may_need_coherence_refinement(
        self, conversation: Conversation, messages: list[Message], metadata: dict
    ) -> bool:
        if metadata.get("title_status") != "generated":
            return False
        return len([msg for msg in messages if msg.role in ("user", "assistant")]) >= 6

    def _title_refinement_evidence(self, conversation: Conversation) -> dict | None:
        title_terms = self._meaningful_terms(conversation.title or "")
        summary_terms = self._meaningful_terms(conversation.summary or "")
        if len(title_terms) < 2 or len(summary_terms) < 8:
            return None
        additional_terms = sorted(summary_terms - title_terms)
        if len(additional_terms) < 6:
            return None
        overlap = sorted(title_terms & summary_terms)
        confidence = "medium" if len(additional_terms) >= 10 else "low"
        return {
            "confidence": confidence,
            "title_terms": sorted(title_terms),
            "summary_specific_terms": additional_terms[:12],
            "overlap_terms": overlap[:8],
        }

    def _meaningful_terms(self, text: str) -> set[str]:
        stop_words = {
            "about",
            "after",
            "also",
            "antes",
            "com",
            "como",
            "das",
            "dos",
            "for",
            "from",
            "into",
            "mais",
            "não",
            "para",
            "pela",
            "pelo",
            "por",
            "que",
            "the",
            "uma",
            "vamos",
            "with",
            "work",
            "working",
        }
        terms = {
            token.lower()
            for token in re.findall(r"[\wÀ-ÿ]{4,}", text, flags=re.UNICODE)
        }
        return {term for term in terms if term not in stop_words}

    def _metadata_dict(self, conversation: Conversation) -> dict:
        try:
            value = json.loads(conversation.metadata or "{}")
        except json.JSONDecodeError:
            return {}
        return value if isinstance(value, dict) else {}

    def _title_metadata(
        self,
        conversation: Conversation,
        *,
        source: str,
        status: str,
        previous_title: str | None,
    ) -> dict:
        metadata = self._metadata_dict(conversation)
        if previous_title and previous_title != metadata.get("previous_title"):
            metadata["previous_title"] = previous_title
        metadata["title_source"] = source
        metadata["title_status"] = status
        return metadata
