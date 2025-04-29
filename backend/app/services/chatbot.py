import openai
from typing import List, Dict, Any
from app.core.config import settings

class ChatbotService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def get_response(self, query: str, candidates: List[Dict[str, Any]]) -> str:
        """Get response from OpenAI based on the query and candidate data"""
        try:
            # Prepare candidate data for the context
            context = "Available candidate data:\n"
            for candidate in candidates:
                context += f"""
                Name: {candidate['first_name']} {candidate['last_name']}
                Current Position: {candidate['current_position']}
                Years of Experience: {candidate['years_of_experience']}
                Skills: {', '.join(candidate['skills'])}
                Work Experience: {candidate['work_experience_summary']}
                ---
                """

            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": settings.CHAT_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error getting chatbot response: {str(e)}")

    def format_candidates_for_ranking(self, candidates: List[Dict[str, Any]], role: str) -> str:
        """Format candidate data for role-specific ranking"""
        prompt = f"Please rank the following candidates for the {role} role based on their experience and skills:\n\n"
        
        for candidate in candidates:
            prompt += f"""
            Candidate: {candidate['first_name']} {candidate['last_name']}
            Current Position: {candidate['current_position']}
            Years of Experience: {candidate['years_of_experience']}
            Skills: {', '.join(candidate['skills'])}
            Work Experience Summary: {candidate['work_experience_summary']}
            ---
            """
            
        prompt += f"\nPlease provide a ranked list with brief explanations for why each candidate would be suitable for the {role} role."
        return prompt

    async def rank_candidates(self, candidates: List[Dict[str, Any]], role: str) -> str:
        """Rank candidates for a specific role"""
        try:
            prompt = self.format_candidates_for_ranking(candidates, role)
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert HR assistant that helps rank candidates based on their qualifications."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error ranking candidates: {str(e)}") 