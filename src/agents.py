import os
import json
import re
import streamlit as st
from typing import List, Dict
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GrowwPulseOrchestrator:
    def __init__(self):
        # Safely attempt to get from st.secrets, fallback to os.getenv
        api_key = None
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass
            
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY")
            
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        
        # Internal State
        self.state = {
            "themes": [],
            "quotes": [],
            "actionable_ideas": [],
            "draft_note": "",
            "review_status": "PENDING",
            "feedback": "",
            "iterations": 0
        }

    def _call_llm(self, prompt: str):
        """Helper to call Groq API"""
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0,
        )
        return response.choices[0].message.content

    def analyst_agent(self, reviews: List[str]):
        """Groups reviews into max 5 themes and selects 3 quotes."""
        print("Agent: Analyst -> Processing reviews...")
        context = "\n".join(reviews)[:15000]
        
        prompt = f"""You are a Data Analyst for Groww. Analyze these reviews:
{context}

CONSTRAINTS:
1. Extract EXACTLY 5 themes (theme name and short description).
2. Extract EXACTLY 3 representative user quotes.

Output strictly as JSON:
{{
  "themes": [{{"theme": "...", "description": "..."}}],
  "quotes": ["...", "...", "..."]
}}"""
        
        raw_output = self._call_llm(prompt)
        # Parse JSON
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            self.state["themes"] = data.get("themes", [])
            self.state["quotes"] = data.get("quotes", [])
        return "Analyst finished."

    def pm_agent(self):
        """Generates 3 actionable product ideas."""
        print("Agent: Product Manager -> Generating ideas...")
        themes_text = "\n".join([f"- {t['theme']}: {t['description']}" for t in self.state["themes"]])
        
        prompt = f"""You are a PM at Groww. Based on these themes:
{themes_text}

Generate 3 highly actionable product roadmap ideas.
Output as a numbered list."""

        raw_output = self._call_llm(prompt)
        self.state["actionable_ideas"] = [line for line in raw_output.split('\n') if line.strip() and line[0].isdigit()][:3]
        return "PM finished."

    def writer_agent(self):
        """Drafts the markdown note (<250 words)."""
        print("Agent: Copywriter -> Drafting the pulse...")
        
        feedback_str = f"REVISION FEEDBACK: {self.state['feedback']}" if self.state["feedback"] else ""
        
        prompt = f"""You are a professional Copywriter for Groww. Create a Weekly Pulse note.
        
THEMES: {self.state['themes']}
QUOTES: {self.state['quotes']}
IDEAS: {self.state['actionable_ideas']}

CRITICAL CONSTRAINTS:
1. Do NOT use any Markdown symbols (no #, no ##, no **).
2. Use ALL CAPS for section headings (e.g., WEEKLY PULSE, KEY THEMES, USER QUOTES, IDEAS FOR IMPROVEMENT).
3. The total word count MUST be under 250 words.
4. Keep it clean, scannable, and professional.
{feedback_str}"""

        self.state["draft_note"] = self._call_llm(prompt)
        return "Writer finished."

    def reviewer_agent(self):
        """Enforces constraints and PII rules."""
        print("Agent: Reviewer -> Validating draft...")
        draft = self.state["draft_note"]
        word_count = len(draft.split())
        
        prompt = f"""You are a QA Reviewer. Check this draft:
{draft}

Does it meet these rules?
- Under 250 words? (Current count: {word_count})
- Professional tone?
- No PII (names/emails)?

Output strictly as JSON:
{{
  "status": "APPROVED" or "REJECTED",
  "feedback": "..."
}}"""

        raw_output = self._call_llm(prompt)
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            self.state["review_status"] = data.get("status", "REJECTED")
            self.state["feedback"] = data.get("feedback", "")
            
        # Hard override for word count
        if word_count > 250:
            self.state["review_status"] = "REJECTED"
            self.state["feedback"] = f"Draft is {word_count} words. Please cut it down below 250."
            
        return "Reviewer finished."

    def run_workflow(self, reviews: List[str]):
        """Main loop managing the agent conversation."""
        # Step 1: Analyst
        yield "Analyst", self.analyst_agent(reviews)
        
        # Step 2: PM
        yield "Product Manager", self.pm_agent()
        
        # Step 3: Loop between Writer and Reviewer
        for i in range(3):
            self.state["iterations"] = i + 1
            yield "Writer", self.writer_agent()
            yield "Reviewer", self.reviewer_agent()
            
            if self.state["review_status"] == "APPROVED":
                break
                
        yield "Final", "Workflow Complete"

if __name__ == "__main__":
    # Example local run
    orchestrator = GrowwPulseOrchestrator()
    for agent, msg in orchestrator.run_workflow(["Great app!", "KYC is slow", "I love the UI"]):
        print(f"[{agent}]: {msg}")
    print("\nFINAL DRAFT:\n", orchestrator.state["draft_note"])
